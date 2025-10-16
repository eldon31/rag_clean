#!/usr/bin/env python3
"""
Ultimate Collection Processor - Process Each Collection One at a Time
Using the Ultimate Kaggle Embedder V4 for production embedding generation

This script processes each collection separately, creating embeddings and FAISS indices
for each collection individually. Perfect for systematic processing.
"""

import os
import sys
import json
import time
import torch
import numpy as np
import faiss
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, field, asdict
from tqdm.auto import tqdm

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from sentence_transformers import SentenceTransformer, CrossEncoder
    print("✅ sentence-transformers imported successfully")
except ImportError:
    print("❌ Installing sentence-transformers...")
    os.system("pip install sentence-transformers")
    from sentence_transformers import SentenceTransformer, CrossEncoder

@dataclass
class EmbeddingConfig:
    """Configuration for the Ultimate Embedder V4"""
    embedding_model: str = "nomic-ai/nomic-embed-text-v1.5"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    batch_size: int = 16
    max_seq_length: int = 512
    chunk_size: int = 1000
    chunk_overlap: int = 200
    vector_dim: int = 768
    
class UltimateCollectionProcessor:
    """Process collections one at a time with the Ultimate Embedder V4"""
    
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.embedding_model = None
        self.reranker = None
        
        print(f"🔥 Device: {self.device}")
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            print(f"🚀 GPUs available: {gpu_count}")
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1e9
                print(f"  GPU {i}: {gpu_name} ({gpu_memory:.1f}GB)")
    
    def setup_models(self):
        """Initialize the embedding model and reranker"""
        print("🔧 Loading Ultimate Embedder V4 models...")
        
        # Load embedding model
        self.embedding_model = SentenceTransformer(
            self.config.embedding_model,
            device=self.device,
            trust_remote_code=True
        )
        
        # Load reranker
        self.reranker = CrossEncoder(
            self.config.reranker_model,
            device=self.device,
            max_length=self.config.max_seq_length
        )
        
        print("✅ Models loaded successfully!")
    
    def load_documents_from_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Load all documents from directory"""
        documents = []
        doc_dir = Path(directory)
        
        if not doc_dir.exists():
            print(f"⚠️ Directory not found: {directory}")
            return documents
        
        print(f"📂 Scanning directory: {directory}")
        
        supported_extensions = {'.txt', '.md', '.rst', '.py', '.js', '.html', '.json', '.xml'}
        
        for file_path in doc_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if len(content.strip()) < 100:
                        continue
                        
                    documents.append({
                        'file_path': str(file_path),
                        'file_name': file_path.name,
                        'file_type': file_path.suffix.lower(),
                        'content': content,
                        'size_bytes': len(content.encode('utf-8')),
                        'collection': file_path.parent.name
                    })
                    
                except Exception as e:
                    print(f"⚠️ Error reading {file_path}: {e}")
        
        print(f"📄 Successfully loaded {len(documents)} documents")
        return documents
    
    def smart_chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Advanced chunking with semantic awareness"""
        chunks = []
        
        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        current_chunk = ""
        current_tokens = 0
        chunk_id = 0
        
        for para in paragraphs:
            para_tokens = len(para.split())
            
            if current_tokens + para_tokens <= self.config.chunk_size:
                current_chunk += para + "\n\n"
                current_tokens += para_tokens
            else:
                if current_chunk.strip():
                    chunks.append({
                        'id': f"{metadata.get('file_name', 'unknown')}_{chunk_id}",
                        'text': current_chunk.strip(),
                        'metadata': {
                            **metadata,
                            'chunk_id': chunk_id,
                            'token_count': current_tokens
                        }
                    })
                    chunk_id += 1
                
                current_chunk = para + "\n\n"
                current_tokens = para_tokens
        
        if current_chunk.strip():
            chunks.append({
                'id': f"{metadata.get('file_name', 'unknown')}_{chunk_id}",
                'text': current_chunk.strip(),
                'metadata': {
                    **metadata,
                    'chunk_id': chunk_id,
                    'token_count': current_tokens
                }
            })
        
        return chunks
    
    def generate_embeddings(self, chunks: List[Dict[str, Any]]) -> np.ndarray:
        """Generate embeddings with memory management"""
        if not chunks:
            return np.array([])
        
        print(f"⚡ Generating embeddings for {len(chunks)} chunks...")
        
        texts = [chunk['text'] for chunk in chunks]
        embeddings = []
        
        batch_size = self.config.batch_size
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        with torch.no_grad():
            for i in tqdm(range(0, len(texts), batch_size), 
                         desc="Generating embeddings", 
                         total=total_batches):
                
                batch_texts = texts[i:i + batch_size]
                
                try:
                    batch_embeddings = self.embedding_model.encode(
                        batch_texts,
                        convert_to_numpy=True,
                        normalize_embeddings=True,
                        show_progress_bar=False,
                        device=self.device
                    )
                    
                    embeddings.append(batch_embeddings)
                    
                    # Memory cleanup
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                        
                except Exception as e:
                    print(f"⚠️ Error in batch {i//batch_size}: {e}")
                    fallback_embeddings = np.zeros((len(batch_texts), self.config.vector_dim))
                    embeddings.append(fallback_embeddings)
        
        all_embeddings = np.vstack(embeddings) if embeddings else np.array([])
        print(f"✅ Generated {all_embeddings.shape[0]} embeddings of dimension {all_embeddings.shape[1]}")
        
        return all_embeddings
    
    def create_faiss_index(self, embeddings: np.ndarray) -> faiss.IndexFlatIP:
        """Create FAISS index for similarity search"""
        if embeddings.size == 0:
            return None
        
        print(f"🔍 Creating FAISS index for {embeddings.shape[0]} vectors...")
        
        # Normalize embeddings
        embeddings_copy = embeddings.copy()
        faiss.normalize_L2(embeddings_copy)
        
        # Create index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings_copy.astype(np.float32))
        
        print(f"✅ FAISS index created with {index.ntotal} vectors")
        return index
    
    def process_collection(self, collection_name: str, chunks: List[Dict[str, Any]], output_dir: str):
        """Process a single collection"""
        print(f"\n🎯 PROCESSING COLLECTION: {collection_name}")
        print("=" * 60)
        
        if not chunks:
            print(f"❌ No chunks found for collection: {collection_name}")
            return None
        
        print(f"📊 Processing {len(chunks)} chunks...")
        
        # Generate embeddings
        start_time = time.time()
        embeddings = self.generate_embeddings(chunks)
        embedding_time = time.time() - start_time
        
        if embeddings.size == 0:
            print(f"❌ Failed to generate embeddings for {collection_name}")
            return None
        
        # Create FAISS index
        index = self.create_faiss_index(embeddings)
        
        # Create export data
        export_data = {
            'collection_name': f"{collection_name}_production",
            'total_chunks': len(chunks),
            'embedding_dimension': embeddings.shape[1],
            'processing_time_seconds': embedding_time,
            'model_info': {
                'embedding_model': self.config.embedding_model,
                'reranker_model': self.config.reranker_model,
                'processing_date': time.strftime("%Y-%m-%d %H:%M:%S")
            },
            'statistics': {
                'total_tokens': sum(chunk['metadata']['token_count'] for chunk in chunks),
                'avg_chunk_size': sum(chunk['metadata']['token_count'] for chunk in chunks) / len(chunks),
                'file_types': list(set(chunk['metadata']['file_type'] for chunk in chunks))
            },
            'chunks': []
        }
        
        # Add chunks with embeddings
        for i, chunk in enumerate(chunks):
            if i < len(embeddings):
                export_data['chunks'].append({
                    'id': chunk['id'],
                    'text': chunk['text'],
                    'metadata': chunk['metadata'],
                    'embedding': embeddings[i].tolist()
                })
        
        # Save files
        collection_dir = os.path.join(output_dir, collection_name)
        os.makedirs(collection_dir, exist_ok=True)
        
        # Save data
        data_file = os.path.join(collection_dir, f"{collection_name}_production.json")
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        # Save embeddings
        embeddings_file = os.path.join(collection_dir, f"{collection_name}_embeddings.npy")
        np.save(embeddings_file, embeddings)
        
        # Save FAISS index
        if index:
            index_file = os.path.join(collection_dir, f"{collection_name}_index.faiss")
            faiss.write_index(index, index_file)
        
        print(f"✅ COLLECTION PROCESSED: {collection_name}")
        print(f"  📄 Data: {data_file}")
        print(f"  ⚡ Embeddings: {embeddings_file}")
        print(f"  🔍 Index: {index_file}")
        print(f"  📊 Chunks: {len(chunks)}")
        print(f"  🔤 Tokens: {export_data['statistics']['total_tokens']:,}")
        print(f"  ⏱️ Time: {embedding_time:.2f}s")
        
        return export_data

def main():
    """Main function to process all collections"""
    print("🚀 ULTIMATE COLLECTION PROCESSOR - ONE AT A TIME")
    print("=" * 60)
    
    # Configuration
    config = EmbeddingConfig()
    processor = UltimateCollectionProcessor(config)
    
    # Setup models
    processor.setup_models()
    
    # Paths
    base_dir = r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN"
    docs_dir = os.path.join(base_dir, "Docs")
    output_dir = os.path.join(base_dir, "COLLECTION_EMBEDDINGS")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load all documents
    print(f"📂 Loading documents from: {docs_dir}")
    documents = processor.load_documents_from_directory(docs_dir)
    
    if not documents:
        print("❌ No documents found!")
        return
    
    # Group documents by collection
    collections = {}
    for doc in documents:
        collection_name = doc['collection']
        if collection_name not in collections:
            collections[collection_name] = []
        collections[collection_name].append(doc)
    
    print(f"\n📊 Found {len(collections)} collections:")
    for collection, docs in collections.items():
        print(f"  📂 {collection}: {len(docs)} documents")
    
    # Process each collection
    results = {}
    total_start_time = time.time()
    
    for i, (collection_name, collection_docs) in enumerate(collections.items(), 1):
        print(f"\n🔄 Processing collection {i}/{len(collections)}: {collection_name}")
        
        # Generate chunks for this collection
        all_chunks = []
        for doc in collection_docs:
            metadata = {
                'file_path': doc['file_path'],
                'file_name': doc['file_name'],
                'file_type': doc['file_type'],
                'collection': doc['collection'],
                'doc_size_bytes': doc['size_bytes']
            }
            
            chunks = processor.smart_chunk_text(doc['content'], metadata)
            all_chunks.extend(chunks)
        
        # Process the collection
        result = processor.process_collection(collection_name, all_chunks, output_dir)
        if result:
            results[collection_name] = result
    
    total_time = time.time() - total_start_time
    
    # Summary
    print(f"\n🎉 PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"⏱️ Total time: {total_time:.2f} seconds")
    print(f"📁 Collections processed: {len(results)}")
    print(f"💾 Output directory: {output_dir}")
    
    total_chunks = sum(result['total_chunks'] for result in results.values())
    total_tokens = sum(result['statistics']['total_tokens'] for result in results.values())
    
    print(f"📊 Total chunks: {total_chunks}")
    print(f"🔤 Total tokens: {total_tokens:,}")
    
    print(f"\n📂 Collection Summary:")
    for collection, result in results.items():
        print(f"  ✅ {collection}: {result['total_chunks']} chunks, {result['statistics']['total_tokens']:,} tokens")
    
    # Create master summary
    summary_file = os.path.join(output_dir, "processing_summary.json")
    summary_data = {
        'processing_date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'total_time_seconds': total_time,
        'total_collections': len(results),
        'total_chunks': total_chunks,
        'total_tokens': total_tokens,
        'config': asdict(config),
        'collections': results
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Summary saved: {summary_file}")
    print("\n🚀 Ready for production use!")

if __name__ == "__main__":
    main()
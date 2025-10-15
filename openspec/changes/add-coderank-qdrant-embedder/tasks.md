# Implementation Tasks

## 1. Model Configuration
- [x] 1.1 Verify nomic-ai/nomic-embed-code is available on HuggingFace Hub
- [x] 1.2 Calculate optimal batch size for 15.83GB GPU VRAM (expect: 24 max)
- [x] 1.3 Validate batch size calculation: `(15.83 - 6.8 - 2.0) / 0.15 = 46 → cap at 24`
- [x] 1.4 Document model specs: 768-dim vectors, ~6.8GB VRAM, 2048 max tokens

## 2. Script Development
- [x] 2.1 Create `scripts/kaggle_embed_qdrant_ecosystem.py` based on `kaggle_embed_docling.py` template
- [x] 2.2 Implement subdirectory auto-detection for `output/qdrant_ecosystem/`
- [x] 2.3 Set EMBEDDING_MODEL = "nomic-ai/nomic-embed-code" (single model for all content)
- [x] 2.4 Add metadata enrichment with subdirectory tracking
- [x] 2.5 Implement data parallelism across 2 GPUs with memory-aware batching
- [x] 2.6 Implement unique ID generation: `qdrant_ecosystem:{subdir}:{filename}:chunk:{index}`
- [x] 2.7 Add model loading with error handling (no fallback logic needed)

## 3. Kaggle Optimization
- [x] 3.1 Add GPU detection and VRAM validation (verify 15.83GB per T4)
- [x] 3.2 Implement adaptive batch sizing based on available VRAM (2GB buffer, max 24)
- [x] 3.3 Add memory cleanup with `torch.cuda.empty_cache()` every 5 batches
- [x] 3.4 Add OOM error detection and automatic batch size reduction (50% decrease)
- [x] 3.5 Add progress reporting with ETA calculation and current GPU memory usage
- [x] 3.6 Handle Kaggle path conventions (`/kaggle/working/`, `/kaggle/input/`)
- [x] 3.7 Log batch size calculations and safety margins for debugging

## 4. Output & Validation
- [x] 4.1 Implement JSONL output format compatible with Qdrant upload scripts
- [x] 4.2 Add embedding summary JSON with stats per subdirectory
- [x] 4.3 Validate chunk IDs are unique across all subdirectories
- [x] 4.4 Add metadata validation (ensure all required fields present)

## 5. Testing & Documentation
- [x] 5.1 Test script locally with sample data (10 chunks per subdirectory)
- [ ] 5.2 Test on Kaggle with full dataset (dry run to estimate time/memory)
- [x] 5.3 Add docstring documentation with usage examples
- [x] 5.4 Create README section for Kaggle setup instructions
- [x] 5.5 Add error handling for common issues (missing input files, OOM errors)

## 6. Deployment
- [ ] 6.1 Run full pipeline on Kaggle and validate output
- [ ] 6.2 Verify embedding quality with sample searches (compare with existing embeddings)
- [ ] 6.3 Document expected processing time and resource usage
- [x] 6.4 Create example Kaggle notebook template

## 7. Future Enhancement: Reranking (Optional)
- [x] 7.1 Document reranking approach in README (CrossEncoder-based, 2-stage retrieval)
- [ ] 7.2 Create example reranking script (separate from embedding pipeline)
- [ ] 7.3 Test reranking with ms-marco-MiniLM-L-6-v2 model
- [ ] 7.4 Benchmark accuracy improvement: Qdrant-only vs Qdrant + reranking
- [ ] 7.5 Document when to use reranking (high-precision queries, top-10 results)

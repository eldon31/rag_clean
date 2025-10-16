from sentence_transformers import SparseEncoder

model = SparseEncoder("naver/splade-cocondenser-ensembledistil")
sentences = ["Natural language processing", "Machine learning algorithms"]
sparse_embeddings = model.encode(sentences)
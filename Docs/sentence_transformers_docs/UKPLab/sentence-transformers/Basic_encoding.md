model = SentenceTransformer("all-mpnet-base-v2")
embeddings = model.encode(["Hello world", "Another sentence"])
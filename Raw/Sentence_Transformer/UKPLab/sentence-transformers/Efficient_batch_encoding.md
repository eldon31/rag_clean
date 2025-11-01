query_embeddings = model.encode(queries, batch_size=32)
passage_embeddings = model.encode(passages, batch_size=32)
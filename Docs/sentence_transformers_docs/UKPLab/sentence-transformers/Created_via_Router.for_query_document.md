router = Router.for_query_document(
    query_modules=[SparseStaticEmbedding(...)],
    document_modules=[MLMTransformer(...), SpladePooling(...)]
)
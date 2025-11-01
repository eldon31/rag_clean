# Testing and Validation

- **Unit Tests:**
  - Cover `CrossEncoderBatchExecutor` batch sizing, leasing behavior, and telemetry emission.
  - Validate `SparseVectorGenerator` handles live inference and fallback paths.
- **Integration Tests:**
  - Run end-to-end embedder on small corpus with rerank/sparse enabled; verify export manifest, JSONL outputs, telemetry entries.
  - Stress test dynamic batch sizing by simulating low-memory conditions.
- **Performance Tests:**
  - Benchmark rerank latency with varying candidate counts/batch sizes to confirm adherence to 12 GB cap.
  - Measure sparse inference throughput vs metadata fallback to ensure acceptable overhead.

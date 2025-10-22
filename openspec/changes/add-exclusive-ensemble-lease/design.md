## Context
Sequential ensemble mode currently rotates models batch-by-batch but leaves each encoder resident on GPU memory until eviction, forcing conservative batch hints to avoid exceeding the 12 GB soft ceiling on Kaggle T4 GPUs. Operators want a deterministic, exclusive-pass workflow where each ensemble model leases both GPUs for the duration of its collection pass, allowing larger batches without concurrency-induced OOM risk and enabling per-model tuning of batch hints. The change spans the embedder core, batch runner orchestration, model lifecycle management, telemetry, and CLI/config surfaces, and must also account for temporary storage of per-model embeddings before aggregation.

## Goals / Non-Goals
- Goals: Provide an opt-in exclusive ensemble mode, centralise GPU leasing and telemetry, enable larger batch hints without OOM, keep reranker/companion models compliant with leases, update docs and summaries.
- Non-Goals: Overhaul non-ensemble execution, change existing adaptive batching heuristics outside exclusive mode, support heterogeneous GPU types beyond dual T4, or redesign run summary schemas beyond required telemetry additions.

## Decisions
- Decision: Introduce a GPU lease helper responsible for reserving both GPUs, evicting previous models, and emitting lease lifecycle telemetry including VRAM snapshots. This isolates concurrency policy from the batch runner and keeps model managers focused on hydration mechanics.
- Decision: Refactor the batch runner to loop over models first so each lease covers an entire collection pass before releasing devices. Adaptive controllers will reset per pass, progress telemetry gains model identifiers, and batch progress indexes switch to `(model_pass, batch_index)` to avoid double counting.
- Decision: Load ensemble models on CPU when exclusive mode is active, reconstructing DataParallel wrappers only inside an active lease. After each pass, unwrap and move models back to CPU to release VRAM and optionally persist per-model embeddings to disk when RAM is insufficient for whole-pass retention.
- Decision: Surface an explicit config/CLI flag defaulting to disabled to avoid surprising operators; documentation and embedding summaries will explain the trade-offs, telemetry expectations, and validation steps.

## Risks / Trade-offs
- Repeated model `.to(device)` transfers can add latency; we will support a sticky-primary option within the lease helper and capture telemetry (including VRAM usage deltas) to monitor warm-up overhead.
- DataParallel wrappers may leave hooks or buffers behind; defensive unwrap logic plus telemetry alerts will highlight residue requiring follow-up.
- Exclusive mode increases implementation complexity; keeping it opt-in and well-documented mitigates confusion.

## Migration Plan
1. Land GPU lease helper and supporting unit tests.
2. Update config/CLI surfaces and wire through batch runner/model manager changes behind the flag.
3. Implement per-model pass storage strategy (in-memory when feasible, disk-backed otherwise) and ensure matryoshka truncation paths remain deterministic across passes.
4. Adjust telemetry, summaries, and docs to describe exclusive mode, including VRAM metrics and progress indexing.
5. Run targeted integration tests plus manual dual-T4 validation to confirm enlarged batch hints, exclusive occupancy, and end-to-end aggregation parity before enabling in production workflows.

## Open Questions
- Should the lease helper support a configurable warm cache to keep one model resident between passes when memory allows?
- Do we need to expose telemetry for companion model CPU/GPU flips separately from main model leases?
- Where should we persist embeddings when collections exceed memory limits during exclusive passes (local disk vs streaming aggregator)?

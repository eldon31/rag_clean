# Introduction

This document outlines the architectural approach for enhancing `RAG_CLEAN` with a fully staffed CrossEncoder reranking stage inside the modular Ultimate Embedder. The goal is to merge dense embeddings, learned sparse vectors, and CrossEncoder reranking into a coordinated pipeline that respects the 12 GB-per-GPU ceiling while preserving the mature export and telemetry surfaces already in place.

**Relationship to existing architecture:** This plan extends the exclusive-ensemble embedder (GPU leasing, telemetry-backed batch runner, sparse helper scaffolding) by activating the dormant rerank and live sparse execution paths. Whenever new orchestration collides with the current flow, this document explains how to reconcile conflicts so consistency and backward compatibility are maintained.

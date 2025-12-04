# Phase 8 Benchmarking Checklist

This note explains how to run the new `benchmarks/phase8_benchmark_suite.py` harness and which
metrics we track for Phase 8.

## Goals
- Measure cold-start load time for representative physical/analytical models
- Capture peak memory usage (focus on coordinate deduplication)
- Time entity lookups + serialization as proxies for relationship/query workloads

## Running the Harness
```bash
# Synthetic model (default 250 beam/curve pairs, duplicated points to stress caching)
python benchmarks/phase8_benchmark_suite.py --iterations 8

# Use an existing payload
python benchmarks/phase8_benchmark_suite.py --payload tests/xmi/v2/test_inputs/complete_physical_model.json

# Generate a 1k-member payload and persist it for regression tracking
python benchmarks/phase8_benchmark_suite.py --members 1000 --export tmp/phase8_1k.json
```

Outputs show entity/relationship counts, average + p95 load times, peak MiB usage, lookup rates,
and serialization speed. Use the `--no-dup-points` flag to disable the coordinate deduplication
stress scenario when isolating other bottlenecks.

### Baseline Snapshot (dev laptop, Py3.12)
- Payload: synthetic, 5 beam/curve pairs (`--members 5 --iterations 1`)
- Load avg: ~2.2 ms
- Peak memory during load: ~0.04 MiB
- Entity lookup phase (5 IDs): <0.1 ms total
- Serialization loop: <0.1 ms total

These micro numbers simply validate the harness. Run with larger payloads (≥1k members) before
deciding on production targets.

### Large-Model Runs (Apr 2025 laptop)
| Members | Entities | Relationships | Load avg (p95) | Peak MiB | Lookup avg | Serialization avg | Notes |
|---------|----------|---------------|----------------|----------|------------|-------------------|-------|
| 1,000   | 4,000    | 1,000         | 0.480 s (0.486 s) | 6.35     | 0.145 s for 1k IDs | 8.4 ms | Linear `find_entity` scan dominates lookup cost. |
| 5,000   | 20,000   | 5,000         | 12.09 s (12.33 s) | 31.67    | 5.77 s for 5k IDs | 52 ms | Load time grows superlinearly due to repeated dictionary scans + coordinate deduplication hashing. |

**Observations**
- Model loading spends most of its time in `XmiModel.load_from_dict()` iterating `ENTITY_CLASS_MAPPING` and
  repeatedly calling `model.find_entity()` during relationship wiring. Profiling highlights the lack of an
  ID index—every lookup is O(n).
- Memory footprint is acceptable (≈6 MiB per 1k member pairs), which confirms point deduplication is keeping
  repeated nodes compact.
- Serialization remains cheap compared with other phases; no work needed there yet.

**Follow-ups**
1. Add an internal `Dict[str, XmiBaseEntity]` cache to `XmiModel` so `find_entity()` becomes O(1). That should
   cut the lookup benchmark from seconds to milliseconds for 5k IDs.
2. Investigate batching inside `load_from_dict()` (e.g., pre-group entities by `EntityType` to avoid repetitive
   string comparisons) once indexing is in place.
3. Record a CI baseline using the 1k-member payload so regressions are visible.

## Next Steps
- Record baseline numbers (store in repo or CI artifacts) for multiple payload sizes.
- Integrate the harness into CI (scheduled job) once acceptable thresholds are known.
- Extend coverage to relationship-heavy cases (e.g., thousands of nodes/segments) as we approach v1.0.

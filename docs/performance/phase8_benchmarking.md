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
- Load avg: ~2.2ms
- Peak memory during load: ~0.04 MiB
- Entity lookup phase (5 IDs): <0.1ms total
- Serialization loop: <0.1ms total

These micro numbers simply validate the harness. Run with larger payloads (≥1k members) before
deciding on production targets.

## Next Steps
- Record baseline numbers (store in repo or CI artifacts) for multiple payload sizes.
- Integrate the harness into CI (scheduled job) once acceptable thresholds are known.
- Extend coverage to relationship-heavy cases (e.g., thousands of nodes/segments) as we approach v1.0.

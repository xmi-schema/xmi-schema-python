"""Phase 8 benchmarking harness.

This script generates repeatable synthetic XMI payloads and captures coarse
metrics for model loading, relationship lookups, and serialization. It avoids
external dependencies so it can run anywhere the main library runs.
"""
from __future__ import annotations

import argparse
import json
import statistics
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from xmi.v2.models.xmi_model.xmi_model import XmiModel  # noqa: E402


@dataclass
class BenchmarkResult:
    label: str
    samples: List[float]

    @property
    def avg(self) -> float:
        return statistics.fmean(self.samples) if self.samples else 0.0

    @property
    def p95(self) -> float:
        if not self.samples:
            return 0.0
        ordered = sorted(self.samples)
        index = min(len(ordered) - 1, int(len(ordered) * 0.95))
        return ordered[index]

    @property
    def iterations(self) -> int:
        return len(self.samples)


def load_payload(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def synthesize_payload(member_count: int, duplicate_points: bool = True) -> Dict[str, Any]:
    """Create a synthetic payload with the requested number of beam/curve pairs."""
    entities: List[Dict[str, Any]] = []
    relationships: List[Dict[str, Any]] = []

    for idx in range(member_count):
        start_point_id = f"spc-{idx}-a"
        end_point_id = f"spc-{idx}-b"
        beam_id = f"beam-{idx}"
        curve_id = f"curve-{idx}"

        base_coord = idx if not duplicate_points else idx % 50
        entities.extend(
            [
                {
                    "ID": start_point_id,
                    "Name": f"Node {start_point_id}",
                    "EntityType": "XmiStructuralPointConnection",
                    "Point": {"X": float(base_coord), "Y": 0.0, "Z": 0.0},
                },
                {
                    "ID": end_point_id,
                    "Name": f"Node {end_point_id}",
                    "EntityType": "XmiStructuralPointConnection",
                    "Point": {"X": float(base_coord + 1), "Y": 0.0, "Z": 0.0},
                },
                {
                    "ID": curve_id,
                    "Name": f"Curve Member {idx}",
                    "EntityType": "XmiStructuralCurveMember",
                    "CurveMemberType": "Beam",
                    "SystemLine": "TopMiddle",
                    "Length": 6_000.0,
                    "LocalAxisX": "1,0,0",
                    "LocalAxisY": "0,1,0",
                    "LocalAxisZ": "0,0,1",
                    "BeginNodeXOffset": 0.0,
                    "EndNodeXOffset": 0.0,
                    "BeginNodeYOffset": 0.0,
                    "EndNodeYOffset": 0.0,
                    "BeginNodeZOffset": 0.0,
                    "EndNodeZOffset": 0.0,
                    "EndFixityStart": "FFFFFF",
                    "EndFixityEnd": "FFFFFF",
                },
                {
                    "ID": beam_id,
                    "Name": f"Physical Beam {idx}",
                    "EntityType": "XmiBeam",
                    "SystemLine": "TopMiddle",
                    "Length": 6_000.0,
                    "LocalAxisX": "1,0,0",
                    "LocalAxisY": "0,1,0",
                    "LocalAxisZ": "0,0,1",
                    "BeginNodeXOffset": 0.0,
                    "EndNodeXOffset": 0.0,
                    "BeginNodeYOffset": 0.0,
                    "EndNodeYOffset": 0.0,
                    "BeginNodeZOffset": 0.0,
                    "EndNodeZOffset": 0.0,
                },
            ]
        )

        relationships.append(
            {
                "ID": f"rel-{idx}",
                "Source": beam_id,
                "Target": curve_id,
                "EntityType": "XmiHasStructuralCurveMember",
                "Name": "BeamBridge",
                "Description": "Physical to analytical bridge",
                "UmlType": "Association",
            }
        )

    return {
        "Name": "SyntheticPerformanceModel",
        "Entities": entities,
        "Relationships": relationships,
        "Histories": [],
        "Errors": [],
    }


def benchmark_model_load(payload: Dict[str, Any], iterations: int) -> BenchmarkResult:
    samples: List[float] = []
    for _ in range(iterations):
        model = XmiModel()
        start = time.perf_counter()
        model.load_from_dict(payload)
        samples.append(time.perf_counter() - start)
    return BenchmarkResult(label="Model load", samples=samples)


def measure_memory(payload: Dict[str, Any]) -> float:
    tracemalloc.start()
    model = XmiModel()
    model.load_from_dict(payload)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / (1024 * 1024)


def benchmark_relationship_queries(model: XmiModel, ids: Sequence[str]) -> BenchmarkResult:
    samples: List[float] = []
    for _ in range(5):
        start = time.perf_counter()
        for entity_id in ids:
            model.find_entity(entity_id)
        samples.append(time.perf_counter() - start)
    return BenchmarkResult(label="Entity lookups", samples=samples)


def benchmark_serialization(model: XmiModel) -> BenchmarkResult:
    samples: List[float] = []
    for _ in range(5):
        start = time.perf_counter()
        model.model_dump()
        samples.append(time.perf_counter() - start)
    return BenchmarkResult(label="Serialization", samples=samples)


def run_suite(payload: Dict[str, Any], iterations: int) -> None:
    print(f"Entities: {len(payload.get('Entities', [])):,}")
    print(f"Relationships: {len(payload.get('Relationships', [])):,}")

    load_result = benchmark_model_load(payload, iterations)
    print(f"\nModel load → avg: {load_result.avg:.4f}s | p95: {load_result.p95:.4f}s | iters: {load_result.iterations}")

    peak_mb = measure_memory(payload)
    print(f"Peak memory (load): {peak_mb:.2f} MiB")

    model = XmiModel()
    model.load_from_dict(payload)
    beam_ids = [entity.id for entity in model.entities if getattr(entity, "entity_type", "") == "XmiBeam"]

    lookup_result = benchmark_relationship_queries(model, beam_ids)
    print(f"Entity lookups → avg: {lookup_result.avg:.4f}s for {len(beam_ids)} ids")

    serialization_result = benchmark_serialization(model)
    print(f"Serialization → avg: {serialization_result.avg:.4f}s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 8 benchmark harness")
    parser.add_argument("--payload", type=Path, help="Optional JSON payload to benchmark")
    parser.add_argument("--members", type=int, default=250, help="Synthetic member count (per physical/analytical pair)")
    parser.add_argument("--iterations", type=int, default=5, help="Iterations for the load benchmark")
    parser.add_argument("--export", type=Path, help="Optional path to export the synthetic payload")
    parser.add_argument("--no-dup-points", action="store_true", help="Disable coordinate deduplication stress test")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.payload:
        payload = load_payload(args.payload)
    else:
        payload = synthesize_payload(args.members, duplicate_points=not args.no_dup_points)
        if args.export:
            with args.export.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2)
            print(f"Synthetic payload written to {args.export}")

    run_suite(payload, args.iterations)


if __name__ == "__main__":
    main()

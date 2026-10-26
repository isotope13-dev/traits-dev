"""Defensive scanner finding models with prefixed class names.

Regression control for well-known/tool/detection/wpsecscan::finding-model:
a bare WPSecScan Finding constructor call belongs to WPSecScan, but
prefixed ``AdapterFinding`` / ``ScanFinding`` constructor calls are other
scanners' own finding models and must not attribute to WPSecScan.
"""
from dataclasses import dataclass


@dataclass
class AdapterFinding:
    """A single weight-statistics finding from a LoRA adapter scan."""

    severity: str
    code: str
    title: str
    detail: str = ""


@dataclass
class ScanFinding:
    """A single finding from a model file scan."""

    severity: str
    title: str
    path: str = ""


def collect():
    return [
        AdapterFinding(
            severity="high",
            code="WD-003",
            title="anomalous weight distribution",
            detail="excess kurtosis=21.4 (threshold 8.0)",
        ),
        ScanFinding(
            severity="medium",
            title="suspicious tensor name",
            path="adapter_model.bin",
        ),
    ]

#!/usr/bin/env python3
"""Power and sample-size planning utilities."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.stats.power import FTestAnovaPower, TTestIndPower, TTestPower


def sample_size(test: str, effect_size: float, target_power: float, alpha: float, groups: int) -> int:
    if test == "t_ind":
        return math.ceil(TTestIndPower().solve_power(effect_size=effect_size, alpha=alpha, power=target_power))
    if test in {"t_one", "t_paired"}:
        return math.ceil(TTestPower().solve_power(effect_size=effect_size, alpha=alpha, power=target_power))
    if test == "anova":
        return math.ceil(FTestAnovaPower().solve_power(effect_size=effect_size, alpha=alpha, power=target_power, k_groups=groups))
    raise ValueError(f"Unsupported test: {test}")


def achieved_power(test: str, effect_size: float, n: int, alpha: float, groups: int) -> float:
    if test == "t_ind":
        return float(TTestIndPower().power(effect_size=effect_size, nobs1=n, alpha=alpha))
    if test in {"t_one", "t_paired"}:
        return float(TTestPower().power(effect_size=effect_size, nobs=n, alpha=alpha))
    if test == "anova":
        return float(FTestAnovaPower().power(effect_size=effect_size, nobs=n, alpha=alpha, k_groups=groups))
    raise ValueError(f"Unsupported test: {test}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sample-size and power-curve outputs.")
    parser.add_argument("--test", choices=["t_ind", "t_one", "t_paired", "anova"], default="t_ind")
    parser.add_argument("--effect-size", type=float, required=True)
    parser.add_argument("--power", type=float, default=0.8)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--groups", type=int, default=3)
    parser.add_argument("--dropout", type=float, default=0.0, help="Expected dropout fraction, e.g. 0.2.")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/power"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    required_n = sample_size(args.test, args.effect_size, args.power, args.alpha, args.groups)
    enroll_n = math.ceil(required_n / (1 - args.dropout)) if args.dropout else required_n

    max_n = max(required_n * 2, 30)
    rows = [{"n": n, "power": achieved_power(args.test, args.effect_size, n, args.alpha, args.groups)} for n in range(5, max_n + 1)]
    curve = pd.DataFrame(rows)
    curve.to_csv(args.out_dir / "power_curve.csv", index=False)

    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(curve["n"], curve["power"], lw=2)
    ax.axhline(args.power, color="#d55e00", ls="--", lw=1)
    ax.axvline(required_n, color="0.35", ls=":", lw=1)
    ax.set_xlabel("n per group" if args.test == "t_ind" else "total n")
    ax.set_ylabel("Power")
    ax.set_ylim(0, 1.02)
    ax.set_title(f"Power curve: {args.test}, effect = {args.effect_size:g}")
    fig.tight_layout()
    fig.savefig(args.out_dir / "power_curve.png", dpi=200)
    plt.close(fig)

    lines = [
        "# Power Report",
        "",
        f"Test: `{args.test}`",
        f"Effect size: `{args.effect_size}`",
        f"Alpha: `{args.alpha}`",
        f"Target power: `{args.power}`",
        f"Required n: `{required_n}`" + (" per group" if args.test == "t_ind" else " total"),
    ]
    if args.dropout:
        lines.append(f"Dropout-adjusted enrollment n: `{enroll_n}` for dropout `{args.dropout:.0%}`")
    lines += [
        "",
        "Report a sensitivity range when the effect-size basis is uncertain.",
        "",
    ]
    (args.out_dir / "power_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(args.out_dir / "power_report.md")


if __name__ == "__main__":
    main()


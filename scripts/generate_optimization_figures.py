"""Rebuild the optimization figures used by the GitBook.

The schematic figures are generated from the equations described in the book.
The quantitative figures use COBRApy 0.30.0's ``textbook`` model and GLPK.
Run from the repository root with::

    python scripts/generate_optimization_figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#2563EB"
ORANGE = "#EA580C"
GREEN = "#059669"
PURPLE = "#7C3AED"
GRAY = "#64748B"
LIGHT_BLUE = "#DBEAFE"
LIGHT_ORANGE = "#FFEDD5"

plt.rcParams.update(
    {
        "figure.dpi": 140,
        "savefig.dpi": 180,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "legend.fontsize": 8,
        "svg.hashsalt": "gem-ebook-figures",
    }
)


def save(fig: plt.Figure, stem: str) -> None:
    """Save a transparent SVG and a white-background PNG."""
    svg_path = OUT / f"{stem}.svg"
    fig.savefig(
        svg_path,
        bbox_inches="tight",
        metadata={"Creator": "generate_optimization_figures.py", "Date": "2026-07-10"},
    )
    fig.savefig(OUT / f"{stem}.png", bbox_inches="tight", facecolor="white")
    # Matplotlib emits spaces at the ends of many SVG path lines. Normalize them
    # so regenerated assets remain clean under ``git diff --check``.
    svg_lines = svg_path.read_text(encoding="utf-8").splitlines()
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_lines) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def draw_lp_geometry() -> None:
    vertices = np.array([(0, 0), (6, 0), (6, 4), (2, 8), (0, 8)])
    xs = np.linspace(0, 7, 200)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True, sharey=True)

    for ax in axes:
        ax.add_patch(
            Polygon(vertices, closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, lw=2)
        )
        ax.scatter(vertices[:, 0], vertices[:, 1], color=BLUE, zorder=4)
        ax.plot(xs, 10 - xs, color=GRAY, ls="--", lw=1, label=r"$v_1+v_2=10$")
        ax.axvline(6, color=GRAY, ls=":", lw=1)
        ax.axhline(8, color=GRAY, ls=":", lw=1)
        ax.set(xlim=(-0.4, 7.1), ylim=(-0.4, 9.2), xlabel=r"$v_1$", ylabel=r"$v_2$")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=0.15)

    ax = axes[0]
    for z, alpha in [(3.0, 0.35), (5.0, 0.55), (7.4, 1.0)]:
        ax.plot(xs, (z - 0.5 * xs) / 0.8, color=ORANGE, alpha=alpha, lw=2)
    ax.scatter([2], [8], s=90, color=ORANGE, edgecolor="white", zorder=5)
    ax.annotate(
        r"unique optimum $(2,8)$",
        (2, 8),
        xytext=(3.0, 8.55),
        arrowprops={"arrowstyle": "->", "color": ORANGE},
        color=ORANGE,
    )
    ax.set_title(r"LP: move $0.5v_1+0.8v_2=Z$ outward")

    ax = axes[1]
    # The gray dashed line above shows the complete equality boundary. Emphasize
    # only its feasible segment so the orange encoding cannot be read as making
    # infeasible points part of the optimal set.
    ax.plot([2, 6], [8, 4], color=ORANGE, lw=4, solid_capstyle="round")
    ax.scatter([6, 2], [4, 8], s=80, color=ORANGE, edgecolor="white", zorder=5)
    ax.annotate(
        "every point on this edge is optimal",
        (4, 6),
        xytext=(0.6, 8.65),
        arrowprops={"arrowstyle": "->", "color": ORANGE},
        color=ORANGE,
    )
    ax.set_title(r"Alternate optima: $0.5v_1+0.5v_2=5$")

    fig.suptitle("Linear programming geometry: feasible polygon and objective lines", y=1.02)
    fig.tight_layout()
    save(fig, "lp-feasible-region")


def draw_norm_geometry() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 5.5))
    diamond = np.array([(1, 0), (0, 1), (-1, 0), (0, -1)])
    ax.add_patch(
        Polygon(diamond, closed=True, fill=False, edgecolor=ORANGE, lw=2.5, label=r"$L_1=1$")
    )
    ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor=BLUE, lw=2.5, label=r"$L_2=1$"))
    ax.scatter([0], [0], color="black", s=25)
    ax.annotate("axis-aligned corners\nencourage sparse changes", (1, 0), (1.15, 0.45),
                arrowprops={"arrowstyle": "->", "color": ORANGE}, color=ORANGE)
    ax.set(xlim=(-1.8, 2.25), ylim=(-1.55, 1.55), xlabel=r"change in $v_1$", ylabel=r"change in $v_2$")
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(0, color=GRAY, lw=0.8)
    ax.grid(alpha=0.15)
    ax.legend(loc="lower left")
    ax.set_title("The same radius looks different under L1 and L2 norms")
    fig.tight_layout()
    save(fig, "l1-l2-norm-geometry")


def draw_moma_projection() -> None:
    feasible = np.array([(0, 0), (6, 0), (6, 2), (2, 6), (0, 6)])
    wt = np.array([7.0, 7.0])
    moma = np.array([4.0, 4.0])
    fba = np.array([2.0, 6.0])

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.add_patch(Polygon(feasible, closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, lw=2))
    for radius in [np.sqrt(18), 5.0, 6.5]:
        ax.add_patch(Circle(wt, radius, fill=False, edgecolor=PURPLE, alpha=0.22, lw=1.5))
    ax.scatter(*wt, color=PURPLE, s=95, zorder=5, label="WT reference")
    ax.scatter(*moma, color=ORANGE, s=95, zorder=5, label="QP MOMA projection")
    ax.scatter(*fba, marker="*", color=GREEN, s=170, zorder=5, label="growth-optimal FBA vertex")
    ax.plot([wt[0], moma[0]], [wt[1], moma[1]], color=ORANGE, ls="--", lw=2)
    ax.annotate("shortest Euclidean distance", moma, (0.25, 7.6),
                arrowprops={"arrowstyle": "->", "color": ORANGE}, color=ORANGE)
    ax.text(0.35, 0.45, "mutant feasible polytope", color=BLUE)
    ax.set(xlim=(-0.4, 10), ylim=(-0.4, 10), xlabel=r"flux coordinate $v_1$", ylabel=r"flux coordinate $v_2$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.15)
    ax.legend(loc="upper right")
    ax.set_title("Quadratic MOMA is a projection onto the mutant feasible set")
    fig.tight_layout()
    save(fig, "qp-moma-projection")


def draw_room_tolerance() -> None:
    wt = np.array([2.0, 5.0, -3.0, 0.2])
    mutant = np.array([2.1, 8.0, -2.8, 1.5])
    half_width = np.array([0.45, 0.8, 0.55, 0.3])
    lo, hi = wt - half_width, wt + half_width
    changed = (mutant < lo) | (mutant > hi)
    y = np.arange(len(wt))[::-1]

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    for i, yi in enumerate(y):
        ax.plot([lo[i], hi[i]], [yi, yi], color=BLUE, lw=12, alpha=0.25, solid_capstyle="round")
        ax.scatter(wt[i], yi, color=BLUE, s=70, zorder=4)
        color = ORANGE if changed[i] else GREEN
        ax.scatter(mutant[i], yi, marker="D", color=color, s=70, zorder=5)
        ax.text(max(hi.max(), mutant.max()) + 0.45, yi, f"y{i + 1}={int(changed[i])}", va="center", color=color)
    ax.axvline(0, color=GRAY, lw=0.8)
    ax.set_yticks(y, [f"reaction {i + 1}" for i in range(len(wt))])
    ax.set_xlabel("flux")
    ax.set_title("ROOM MILP: a binary variable counts exits from each WT tolerance band")
    ax.scatter([], [], color=BLUE, label="WT flux / allowed band")
    ax.scatter([], [], marker="D", color=GREEN, label=r"mutant flux, $y_i=0$")
    ax.scatter([], [], marker="D", color=ORANGE, label=r"mutant flux, $y_i=1$")
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.15)
    fig.tight_layout()
    save(fig, "milp-room-tolerance")


def load_textbook():
    import cobra

    cobra.Configuration().processes = 1
    return cobra.io.load_model("textbook")


def draw_fva_intervals() -> None:
    from cobra.flux_analysis import flux_variability_analysis, pfba

    model = load_textbook()
    reaction_ids = ["PGI", "PFK", "PYK", "G6PDH2r", "EX_ac_e", "EX_etoh_e", "EX_for_e"]
    fva = flux_variability_analysis(
        model, reaction_list=reaction_ids, fraction_of_optimum=0.9, processes=1
    )
    representative = pfba(model).fluxes[reaction_ids]
    y = np.arange(len(reaction_ids))[::-1]

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for yi, rid in zip(y, reaction_ids):
        lo, hi = float(fva.loc[rid, "minimum"]), float(fva.loc[rid, "maximum"])
        ax.plot([lo, hi], [yi, yi], color=BLUE, lw=4, solid_capstyle="round")
        ax.scatter([lo, hi], [yi, yi], color=BLUE, s=28)
        ax.scatter(float(representative[rid]), yi, color=ORANGE, marker="D", s=42, zorder=4)
    ax.axvline(0, color=GRAY, lw=0.8)
    ax.set_yticks(y, reaction_ids)
    ax.set_xlabel(r"flux (mmol gDW$^{-1}$ h$^{-1}$)")
    ax.set_title("FVA intervals at least 90% of optimal growth")
    ax.scatter([], [], color=BLUE, label="FVA min–max")
    ax.scatter([], [], color=ORANGE, marker="D", label="one pFBA solution")
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.15)
    fig.tight_layout()
    save(fig, "fva-intervals")


def draw_robustness_curve() -> None:
    model = load_textbook()
    glucose = np.linspace(0.5, 20, 40)

    def scan(o2_limit: float):
        values = []
        for glc in glucose:
            with model:
                model.reactions.EX_glc__D_e.lower_bound = -float(glc)
                model.reactions.EX_o2_e.lower_bound = -float(o2_limit)
                value = model.slim_optimize(error_value=np.nan)
                values.append(value if np.isfinite(value) else np.nan)
        return np.asarray(values)

    oxygen_rich = scan(1000)
    oxygen_limited = scan(10)
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(glucose, oxygen_rich, color=BLUE, lw=2.5, label=r"O$_2$ uptake cap = 1000")
    ax.plot(glucose, oxygen_limited, color=ORANGE, lw=2.5, label=r"O$_2$ uptake cap = 10")
    ax.fill_between(glucose, oxygen_limited, oxygen_rich, color=LIGHT_ORANGE, alpha=0.7)
    ax.set(xlabel=r"glucose uptake cap (mmol gDW$^{-1}$ h$^{-1}$)", ylabel=r"max growth (h$^{-1}$)")
    ax.set_title("Robustness curves depend on the other active bounds")
    ax.grid(alpha=0.18)
    ax.legend()
    fig.tight_layout()
    save(fig, "glucose-robustness")


def draw_production_envelope() -> None:
    from cobra.flux_analysis import production_envelope

    model = load_textbook()
    envelope = production_envelope(
        model,
        reactions=[model.reactions.Biomass_Ecoli_core],
        objective="EX_ac_e",
        points=30,
    ).sort_values("Biomass_Ecoli_core")
    x = envelope["Biomass_Ecoli_core"].to_numpy(float)
    lo = envelope["flux_minimum"].to_numpy(float)
    hi = envelope["flux_maximum"].to_numpy(float)

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.fill_between(x, lo, hi, color=LIGHT_BLUE, alpha=0.9, label="feasible acetate range")
    ax.plot(x, hi, color=BLUE, lw=2.2, label="maximum")
    ax.plot(x, lo, color=GREEN, lw=2.2, ls="--", label="minimum")
    idx = int(np.argmax(x))
    ax.scatter(x[idx], lo[idx], color=ORANGE, s=70, zorder=5)
    ax.annotate("minimum = 0 at max growth\n(not growth-coupled)", (x[idx], lo[idx]),
                xytext=(0.45, 7.0), arrowprops={"arrowstyle": "->", "color": ORANGE}, color=ORANGE)
    ax.set(xlabel=r"biomass flux (h$^{-1}$)", ylabel=r"acetate secretion flux (mmol gDW$^{-1}$ h$^{-1}$)")
    ax.set_title("E. coli core acetate production envelope")
    ax.grid(alpha=0.18)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "acetate-production-envelope")


def main() -> None:
    draw_lp_geometry()
    draw_norm_geometry()
    draw_moma_projection()
    draw_room_tolerance()
    draw_fva_intervals()
    draw_robustness_curve()
    draw_production_envelope()
    print(f"Generated 7 figure pairs in {OUT}")


if __name__ == "__main__":
    main()

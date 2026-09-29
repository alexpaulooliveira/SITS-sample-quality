import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

# ==================== QUALIDADE EDITORIAL ====================

ARTWORK_DPI = 600

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

def save_png_svg_pdf_eps(fig, png_path):
    fig.patch.set_facecolor("white")

    base_path, _ = os.path.splitext(png_path)

    fig.savefig(
        png_path,
        bbox_inches="tight",
        dpi=ARTWORK_DPI,
        facecolor="white",
        edgecolor="none",
        format="png",
        metadata={"Software": "Matplotlib", "dpi": str(ARTWORK_DPI)},
        pil_kwargs={"dpi": (ARTWORK_DPI, ARTWORK_DPI), "compress_level": 1}
    )

    fig.savefig(base_path + ".svg", bbox_inches="tight", dpi=ARTWORK_DPI,
                facecolor="white", edgecolor="none", format="svg")

    fig.savefig(base_path + ".pdf", bbox_inches="tight", dpi=ARTWORK_DPI,
                facecolor="white", edgecolor="none", format="pdf")

    fig.savefig(base_path + ".eps", bbox_inches="tight", dpi=ARTWORK_DPI,
                facecolor="white", edgecolor="none", format="eps")


# ==================== GERAÇÃO DAS GRADES ====================

COLORS = {
    "brown":  "#8c564b",
    "cyan":   "#9edae5",
    "green":  "#7fc97f",
    "orange": "#ff7f00",
    "pink":   "#f781bf",
    "gray":   "#bdbdbd",
    "blue":   "#1f78b4",
    "olive":  "#cfcf7a",
}

def make_grid(seed, rows=15, cols=15):
    rng = np.random.default_rng(seed)
    grid = np.full((rows, cols), COLORS["green"], dtype=object)

    yy, xx = np.mgrid[0:rows, 0:cols]

    centers = [
        (2,  1,  COLORS["brown"],  2.2),
        (3,  5,  COLORS["cyan"],   3.0),
        (3, 12,  COLORS["green"],  2.8),
        (7, 13,  COLORS["orange"], 3.4),
        (11, 2,  COLORS["pink"],   3.2),
        (10, 6,  COLORS["gray"],   2.7),
        (1, 11,  COLORS["blue"],   2.2),
        (8, 7,   COLORS["olive"],  2.6),
    ]

    rng.shuffle(centers)

    for cy, cx, color, radius in centers:
        noise = rng.normal(0, 0.45, size=(rows, cols))
        dist = np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2)
        grid[dist + noise < radius] = color

    return grid

def draw_hex_grid(ax, grid):
    rows, cols = grid.shape

    r = 0.50
    dx = math.sqrt(3) * r
    dy = 1.5 * r

    for row in range(rows):
        for col in range(cols):
            x = col * dx + (row % 2) * dx / 2
            y = -row * dy

            hexagon = RegularPolygon(
                (x, y),
                numVertices=6,
                radius=r,
                orientation=math.radians(30),
                facecolor=grid[row, col],
                edgecolor="white",
                linewidth=0.55
            )
            ax.add_patch(hexagon)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.6, cols * dx + 0.6)
    ax.set_ylim(-rows * dy + 0.4, 0.8)

def generate_figure(output="Figure_4_cluster_grids.png"):
    fig, axes = plt.subplots(2, 2, figsize=(5.0, 5.0))

    seeds = [1, 7, 13, 21]

    for ax, seed in zip(axes.ravel(), seeds):
        grid = make_grid(seed)
        draw_hex_grid(ax, grid)

    plt.subplots_adjust(
        left=0.02,
        right=0.98,
        bottom=0.02,
        top=0.98,
        wspace=0.08,
        hspace=0.00
    )            

    save_png_svg_pdf_eps(fig, output)
    plt.close(fig)

if __name__ == "__main__":
    generate_figure("Figure_4_cluster_grids.png")
import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch
from matplotlib import patheffects as pe

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

    for ext in ["svg", "pdf", "eps"]:
        fig.savefig(
            base_path + f".{ext}",
            bbox_inches="tight",
            dpi=ARTWORK_DPI,
            facecolor="white",
            edgecolor="none",
            format=ext
        )


def shadowed_text(ax, x, y, text, size):
    ax.text(
        x, y, text,
        ha="center",
        va="center",
        fontsize=size,
        fontweight="bold",
        color="white",
        linespacing=0.90,
        path_effects=[pe.withStroke(linewidth=3.0, foreground="black")]
    )


def draw_panel(ax, x, y, w, h, color):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="none"))


def draw_noise(ax, x, y, w, h):
    draw_panel(ax, x, y, w, h, "#6a5517")

    ax.add_patch(Circle(
        (x+w/2, y+h*0.73),
        h*0.19,
        facecolor="#b9942a",
        edgecolor="#fff176",
        linewidth=3
    ))

    ax.add_patch(Circle(
        (x+w/2, y+h*0.73),
        h*0.145,
        facecolor="none",
        edgecolor="#fff176",
        linewidth=2
    ))

    funnel = Polygon([
        (x+w*0.38, y+h*0.80),
        (x+w*0.62, y+h*0.80),
        (x+w*0.54, y+h*0.69),
        (x+w*0.54, y+h*0.58),
        (x+w*0.46, y+h*0.58),
        (x+w*0.46, y+h*0.69),
    ], closed=True, facecolor="#fff176", edgecolor="white", linewidth=1.4)
    ax.add_patch(funnel)

    shadowed_text(ax, x+w/2, y+h*0.27, "AUTOMATIC\nNOISE\nREMOVAL", 17)


def draw_accuracy(ax, x, y, w, h):
    draw_panel(ax, x, y, w, h, "#0d344b")

    ax.plot(
        [x+w*0.16, x+w*0.16, x+w*0.52],
        [y+h*0.42, y+h*0.78, y+h*0.42],
        color="#50d6ff",
        linewidth=5,
        solid_capstyle="round"
    )

    for bx, bh in [(0.22, 0.16), (0.33, 0.25), (0.44, 0.35)]:
        ax.add_patch(Rectangle(
            (x+w*bx, y+h*0.42),
            w*0.07,
            h*bh,
            facecolor="#50d6ff",
            edgecolor="none"
        ))

    ax.plot(
        [x+w*0.22, x+w*0.34, x+w*0.47, x+w*0.61],
        [y+h*0.56, y+h*0.67, y+h*0.61, y+h*0.82],
        color="#50d6ff",
        linewidth=4
    )

    ax.arrow(
        x+w*0.58, y+h*0.78,
        w*0.08, h*0.08,
        head_width=w*0.08,
        head_length=w*0.07,
        color="#50d6ff"
    )

    ax.add_patch(Circle(
        (x+w*0.73, y+h*0.64),
        h*0.18,
        facecolor="#55d6ff",
        edgecolor="#0a2030",
        linewidth=3
    ))

    ax.plot(
        [x+w*0.65, x+w*0.71, x+w*0.81],
        [y+h*0.64, y+h*0.55, y+h*0.71],
        color="#0a2030",
        linewidth=5,
        solid_capstyle="round"
    )

    shadowed_text(ax, x+w/2, y+h*0.18, "IMPROVED\nACCURACY", 17)


def draw_reduced(ax, x, y, w, h):
    draw_panel(ax, x, y, w, h, "#355915")

    ax.add_patch(Circle(
        (x+w*0.34, y+h*0.84),
        h*0.075,
        facecolor="#efffd8",
        edgecolor="black",
        linewidth=1.5
    ))

    ax.plot(
        [x+w*0.34, x+w*0.34],
        [y+h*0.76, y+h*0.61],
        color="#efffd8",
        linewidth=8,
        solid_capstyle="round"
    )

    ax.plot(
        [x+w*0.22, x+w*0.46],
        [y+h*0.70, y+h*0.70],
        color="#efffd8",
        linewidth=8,
        solid_capstyle="round"
    )

    ax.plot(
        [x+w*0.30, x+w*0.30],
        [y+h*0.61, y+h*0.49],
        color="#efffd8",
        linewidth=7,
        solid_capstyle="round"
    )

    ax.plot(
        [x+w*0.38, x+w*0.38],
        [y+h*0.61, y+h*0.49],
        color="#efffd8",
        linewidth=7,
        solid_capstyle="round"
    )

    ax.add_patch(FancyArrowPatch(
        (x+w*0.56, y+h*0.86),
        (x+w*0.83, y+h*0.58),
        arrowstyle="-|>",
        mutation_scale=30,
        linewidth=6,
        color="#ffeb66"
    ))

    shadowed_text(ax, x+w/2, y+h*0.30, "REDUCED\nHUMAN\nSUPPORT", 17)


def create_step11_horizontal(output_path="step11.png"):
    fig, ax = plt.subplots(figsize=(8.4, 3.2))

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    border_color = "#556b2f"

    ax.add_patch(Rectangle(
        (0.30, 0.30),
        9.83,
        3.40,
        facecolor="white",
        edgecolor=border_color,
        linewidth=5
    ))

    w = 2.90
    h = 2.45
    y = 0.78

    draw_noise(ax, 0.55, y, w, h)
    draw_accuracy(ax, 3.75, y, w, h)
    draw_reduced(ax, 6.95, y, w, h)

    save_png_svg_pdf_eps(fig, output_path)
    plt.close(fig)


if __name__ == "__main__":
    create_step11_horizontal("step11.png")

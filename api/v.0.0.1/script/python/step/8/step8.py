import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle

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


# ==================== STEP 8: EXCLUSION MAP ====================

def generate_exclusion_map_icon(output_path="step_8_exclusion_map.png"):
    fig, ax = plt.subplots(figsize=(1.45, 2.25))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Moldura do arquivo CSV
    ax.add_patch(Rectangle(
        (0.8, 3.7), 8.2, 10.0,
        facecolor="white",
        edgecolor="#555555",
        linewidth=1.4
    ))



    # Cabeçalho da coluna
    ax.text(
        1.75, 12.75,
        "id",
        ha="left",
        va="center",
        fontsize=7.2,
        family="DejaVu Sans Mono",
        color="#444444"
    )

    # Linhas principais
    rows = [
        ("1", True),
        ("5", True),
        ("8", False),
    ]

    y_positions = [11.35, 9.75, 8.15]

    for (txt, highlight), y in zip(rows, y_positions):
        if highlight:
            ax.add_patch(FancyBboxPatch(
                (1.45, y - 0.55), 6.85, 1.05,
                boxstyle="round,pad=0.08,rounding_size=0.28",
                facecolor="white",
                edgecolor="red",
                linewidth=1.4
            ))

        ax.text(
            1.75, y,
            txt,
            ha="left",
            va="center",
            fontsize=8.4,
            color="#3767b1" if txt in ["1", "5"] else "#555555"
        )

    # Reticências verticais
    dot_x = 5.0
    for y in [6.2, 5.35, 4.5]:
        ax.add_patch(Circle(
            (dot_x, y),
            radius=0.22,
            facecolor="black",
            edgecolor="black",
            linewidth=0
        ))

    save_png_svg_pdf_eps(fig, output_path)
    plt.close(fig)


if __name__ == "__main__":
    generate_exclusion_map_icon("step_8_exclusion_map.png")
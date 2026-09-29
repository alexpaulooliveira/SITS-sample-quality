import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

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


# def create_step10_decision(output_path="step_10_decision.png"):
#     fig, ax = plt.subplots(figsize=(5.2, 2.6))
#     ax.set_xlim(0, 10)
#     ax.set_ylim(0, 5)
#     ax.axis("off")
#     fig.patch.set_facecolor("white")
    
#     # Dark green border around the entire figure content
#     ax.add_patch(Rectangle(
#         (0.15, 0.15),      # canto inferior esquerdo
#         9.70,              # largura
#         4.70,              # altura
#         fill=False,
#         edgecolor="#006400",   # verde escuro
#         linewidth=4.0,
#         zorder=0
#     ))    


#     # Decision text without black rectangle
#     ax.text(
#         5.0, 3.55,
#         r"SRSF > E_threshold ?",
#         ha="center",
#         va="center",
#         fontsize=22,
#         fontweight="bold",
#         color="black"
#     )

#     # STOP box
#     ax.add_patch(Rectangle(
#         (0.8, 0.75), 3.2, 1.25,
#         facecolor="white",
#         edgecolor="red",
#         linewidth=2.8
#     ))

#     ax.text(
#         2.4, 1.38,
#         "STOP",
#         ha="center",
#         va="center",
#         fontsize=22,
#         fontweight="bold",
#         color="red"
#     )

#     # STEP 5 box
#     ax.add_patch(Rectangle(
#         (6.0, 0.75), 3.2, 1.25,
#         facecolor="white",
#         edgecolor="blue",
#         linewidth=2.8
#     ))

#     ax.text(
#         7.6, 1.38,
#         "Step 5",
#         ha="center",
#         va="center",
#         fontsize=22,
#         fontweight="bold",
#         color="blue"
#     )

#     # YES arrow
#     ax.add_patch(FancyArrowPatch(
#         (4.1, 3.25), (2.55, 2.05),
#         arrowstyle="-|>",
#         mutation_scale=25,
#         linewidth=3.0,
#         color="red"
#     ))

#     ax.text(
#         2.35, 2.45,
#         "YES",
#         ha="right",
#         va="center",
#         fontsize=14,
#         fontweight="bold",
#         color="red"
#     )

#     # NO arrow
#     ax.add_patch(FancyArrowPatch(
#         (5.9, 3.25), (7.45, 2.05),
#         arrowstyle="-|>",
#         mutation_scale=25,
#         linewidth=3.0,
#         color="blue"
#     ))

#     ax.text(
#         7.65, 2.45,
#         "NO",
#         ha="left",
#         va="center",
#         fontsize=14,
#         fontweight="bold",
#         color="blue"
#     )

#     save_png_svg_pdf_eps(fig, output_path)
#     plt.close(fig)


def create_step10_decision(output_path="step_10_decision.png"):
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Dark green border around the entire figure content
    ax.add_patch(Rectangle(
        (0.15, 0.15),
        9.70,
        4.70,
        fill=False,
        edgecolor="#006400",
        linewidth=4.0,
        zorder=0
    ))

    # Decision text
    ax.text(
        5.0, 3.55,
        r"SRSF > E_threshold ?",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="black"
    )

    # STEP 5 box (agora à esquerda)
    ax.add_patch(Rectangle(
        (0.8, 0.75), 3.2, 1.25,
        facecolor="white",
        edgecolor="blue",
        linewidth=2.8
    ))

    ax.text(
        2.4, 1.38,
        "Step 5",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="blue"
    )

    # STOP box (agora à direita)
    ax.add_patch(Rectangle(
        (6.0, 0.75), 3.2, 1.25,
        facecolor="white",
        edgecolor="red",
        linewidth=2.8
    ))

    ax.text(
        7.6, 1.38,
        "STOP",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="red"
    )

    # NO arrow (agora à esquerda)
    ax.add_patch(FancyArrowPatch(
        (4.1, 3.25), (2.55, 2.05),
        arrowstyle="-|>",
        mutation_scale=25,
        linewidth=3.0,
        color="blue"
    ))

    ax.text(
        2.35, 2.45,
        "NO",
        ha="right",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="blue"
    )

    # YES arrow (agora à direita)
    ax.add_patch(FancyArrowPatch(
        (5.9, 3.25), (7.45, 2.05),
        arrowstyle="-|>",
        mutation_scale=25,
        linewidth=3.0,
        color="red"
    ))

    ax.text(
        7.65, 2.45,
        "YES",
        ha="left",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="red"
    )

    save_png_svg_pdf_eps(fig, output_path)
    plt.close(fig)


if __name__ == "__main__":
    create_step10_decision("step_10_decision.png")

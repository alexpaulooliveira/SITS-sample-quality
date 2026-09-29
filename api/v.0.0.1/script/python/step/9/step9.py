import os
import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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


def generate_evolved_satellite_texture(seed=7, size=420, altered_fraction=0.33):
    rng = np.random.default_rng(seed)

    img = np.zeros((size, size, 3), dtype=float)
    img[:] = np.array([35, 95, 38]) / 255

    green_palette = np.array([
        [18, 70, 30],
        [30, 105, 42],
        [70, 135, 55],
        [95, 145, 58],
        [125, 165, 55],
        [18, 55, 72],
        [35, 88, 120],
    ]) / 255

    altered_palette = np.array([
        [178, 145, 75],   # bege
        [195, 165, 95],   # amarelo-terra
        [150, 105, 55],   # marrom claro
        [118, 86, 45],    # marrom
        [210, 185, 110],  # amarelo seco
        [160, 125, 70],   # solo exposto
    ]) / 255

    blocks = []

    for _ in range(160):
        x0 = rng.integers(0, size - 40)
        y0 = rng.integers(0, size - 40)
        w = rng.integers(28, 95)
        h = rng.integers(28, 95)
        blocks.append((x0, y0, w, h))

    n_altered = int(len(blocks) * altered_fraction)
    altered_indices = set(rng.choice(len(blocks), size=n_altered, replace=False))

    for i, (x0, y0, w, h) in enumerate(blocks):
        if i in altered_indices:
            color = altered_palette[rng.integers(0, len(altered_palette))]
        else:
            color = green_palette[rng.integers(0, len(green_palette))]

        img[
            y0:min(size, y0 + h),
            x0:min(size, x0 + w)
        ] = color

    yy, xx = np.mgrid[0:size, 0:size]

    for cx, cy, rx, ry in [
        (150, 85, 33, 45),
        (220, 175, 38, 25),
        (75, 320, 36, 25),
    ]:
        mask = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1
        img[mask] = np.array([10, 58, 78]) / 255

    for _ in range(11):
        y = rng.integers(30, size - 30)
        slope = rng.uniform(-0.18, 0.18)
        x_start = rng.integers(0, 130)

        for x in range(x_start, size):
            yy_line = int(y + slope * (x - x_start))
            if 0 <= yy_line < size:
                img[
                    max(0, yy_line - 1):min(size, yy_line + 2),
                    x
                ] = np.array([210, 210, 185]) / 255

    img += rng.normal(0, 0.018, img.shape)

    return np.clip(img, 0, 1)


def create_evolved_satellite_image(output_path="evolved_satellite_image.png"):
    fig, ax = plt.subplots(figsize=(4.8, 4.3))

    ax.set_xlim(0, 5.6)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    texture = generate_evolved_satellite_texture(
        seed=7,
        size=420,
        altered_fraction=0.33
    )

    ax.imshow(
        texture,
        extent=(0.55, 5.0, 0.7, 4.7),
        interpolation="nearest",
        zorder=1
    )

    ax.add_patch(Rectangle(
        (0.55, 0.7),
        4.45,
        4.0,
        facecolor="none",
        edgecolor="black",
        linewidth=2.5,
        zorder=3
    ))

    save_png_svg_pdf_eps(fig, output_path)
    plt.close(fig)


if __name__ == "__main__":
    create_evolved_satellite_image("evolved_satellite_image.png")

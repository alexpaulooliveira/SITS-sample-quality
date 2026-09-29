import os
import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.transforms import Affine2D

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
        pad_inches=0.02,
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
            pad_inches=0.02,
            dpi=ARTWORK_DPI,
            facecolor="white",
            edgecolor="none",
            format=ext
        )


def generate_satellite_texture(seed=7, size=420):
    rng = np.random.default_rng(seed)

    img = np.zeros((size, size, 3), dtype=float)
    img[:] = np.array([35, 95, 38]) / 255

    palette = np.array([
        [18, 70, 30],
        [30, 105, 42],
        [70, 135, 55],
        [125, 165, 55],
        [178, 145, 75],
        [118, 86, 45],
        [18, 55, 72],
        [35, 88, 120],
    ]) / 255

    for _ in range(160):
        x0 = rng.integers(0, size - 40)
        y0 = rng.integers(0, size - 40)
        w = rng.integers(28, 95)
        h = rng.integers(28, 95)
        img[y0:min(size, y0 + h), x0:min(size, x0 + w)] = palette[rng.integers(0, len(palette))]

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
                img[max(0, yy_line - 1):min(size, yy_line + 2), x] = np.array([210, 210, 185]) / 255

    img += rng.normal(0, 0.018, img.shape)
    return np.clip(img, 0, 1)


def add_rotated_round_rect(
    ax,
    center,
    width,
    height,
    angle,
    facecolor,
    edgecolor="black",
    linewidth=2.5,
    radius=0.10,
    zorder=3
):
    cx, cy = center

    patch = FancyBboxPatch(
        (cx - width / 2, cy - height / 2),
        width,
        height,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=zorder
    )

    patch.set_transform(
        Affine2D().rotate_deg_around(cx, cy, angle) + ax.transData
    )

    ax.add_patch(patch)
    return patch


def draw_solar_panel(ax, center, width, height, angle):
    cx, cy = center

    add_rotated_round_rect(
        ax,
        center,
        width,
        height,
        angle,
        facecolor="#55dce8",
        edgecolor="black",
        linewidth=2.2,
        radius=0.10,
        zorder=4
    )

    tr = Affine2D().rotate_deg_around(cx, cy, angle) + ax.transData

    for k in [-1, 0, 1]:
        x = cx + k * width / 4
        ax.plot(
            [x, x],
            [cy - height / 2, cy + height / 2],
            color="black",
            linewidth=1.1,
            transform=tr,
            zorder=5
        )

    for k in [-1, 1]:
        y = cy + k * height / 6
        ax.plot(
            [cx - width / 2, cx + width / 2],
            [y, y],
            color="black",
            linewidth=1.1,
            transform=tr,
            zorder=5
        )


def draw_vertical_symmetric_satellite(ax):
    angle = 0

    cx, cy = 5.9, 2.5

    body_w = 0.85
    body_h = 0.85

    panel_w = 1.05
    panel_h = 1.05

    vertical_offset = 1.30
    connector_h = 0.48

    draw_solar_panel(
        ax,
        center=(cx, cy + vertical_offset),
        width=panel_w,
        height=panel_h,
        angle=angle
    )

    draw_solar_panel(
        ax,
        center=(cx, cy - vertical_offset),
        width=panel_w,
        height=panel_h,
        angle=angle
    )

    add_rotated_round_rect(
        ax,
        center=(cx, cy + 0.74),
        width=0.28,
        height=connector_h,
        angle=angle,
        facecolor="white",
        edgecolor="black",
        linewidth=2.0,
        radius=0.04,
        zorder=5
    )

    add_rotated_round_rect(
        ax,
        center=(cx, cy - 0.74),
        width=0.28,
        height=connector_h,
        angle=angle,
        facecolor="white",
        edgecolor="black",
        linewidth=2.0,
        radius=0.04,
        zorder=5
    )

    add_rotated_round_rect(
        ax,
        center=(cx, cy),
        width=body_w,
        height=body_h,
        angle=angle,
        facecolor="#9fb4c7",
        edgecolor="black",
        linewidth=2.4,
        radius=0.10,
        zorder=6
    )

    ax.plot(
        [cx, cx],
        [cy - body_h / 2, cy + body_h / 2],
        color="black",
        linewidth=1.2,
        zorder=7
    )

    ax.plot(
        [cx - body_w / 2, cx + body_w / 2],
        [cy, cy],
        color="black",
        linewidth=1.2,
        zorder=7
    )


def create_step1_satellite_to_dataset(output_path="step_1_satellite_dataset_vertical.png"):
    fig, ax = plt.subplots(figsize=(5.9, 4.1))

    ax.set_xlim(0.35, 6.65)
    ax.set_ylim(0.35, 4.65)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    texture = generate_satellite_texture()

    ax.imshow(
        texture,
        extent=(0.55, 3.95, 0.8, 4.2),
        interpolation="nearest",
        zorder=1
    )

    ax.add_patch(Rectangle(
        (0.55, 0.8),
        3.40,
        3.40,
        facecolor="none",
        edgecolor="black",
        linewidth=2.2,
        zorder=3
    ))

    draw_vertical_symmetric_satellite(ax)

    save_png_svg_pdf_eps(fig, output_path)
    plt.close(fig)


if __name__ == "__main__":
    create_step1_satellite_to_dataset("step_1_satellite_dataset_vertical.png")
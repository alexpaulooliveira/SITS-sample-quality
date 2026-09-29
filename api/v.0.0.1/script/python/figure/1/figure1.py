import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from pathlib import Path

out_pdf = Path("Figure_1_recreated_vector.pdf")
out_png = Path("Figure_1_recreated_1000dpi.png")

fig, ax = plt.subplots(figsize=(7.2, 4.0))

rows = 15
cols = 22
r = 0.43
dx = np.sqrt(3) * r
dy = 1.5 * r

colors = {
    "orange": "#ffa500",
    "yellow": "#ffff00",
    "cyan": "#00ffff",
    "pink": "#ffc0cb",
    "green": "#008000",
    "purple": "#800080",
    "blue": "#0000cc",
    "red": "#ff0000",
    "black": "#000000",
}

def region_color(row, col):
    if row < 5 and col < 7:
        return colors["orange"]
    if row < 6 and 7 <= col < 14:
        return colors["yellow"]
    if col >= 14:
        return colors["cyan"]
    if 5 <= row < 10 and 6 <= col < 14:
        return colors["pink"]
    if row >= 10 and 6 <= col < 14:
        return colors["green"]
    if row >= 10 and col >= 14:
        return colors["purple"]
    if row >= 10 and col < 6:
        return colors["orange"]
    return colors["yellow"]

def pos(row, col):
    return col * dx + (row % 2) * dx / 2, -row * dy

def add_hex(row, col, color, edge="#808080", lw=0.35):
    x, y = pos(row, col)
    hexagon = RegularPolygon(
        (x, y),
        numVertices=6,
        radius=r,
        orientation=np.radians(30),
        facecolor=color,
        edgecolor=edge,
        linewidth=lw
    )
    ax.add_patch(hexagon)

special_cells = {}

# Grupo central — já corrigido, não modificar
special_cells[(6, 11)] = colors["black"]
special_cells[(5, 10)] = colors["red"]
special_cells[(5, 11)] = colors["red"]
special_cells[(6, 10)] = colors["blue"]
special_cells[(6, 12)] = colors["blue"]
special_cells[(7, 10)] = colors["blue"]
special_cells[(7, 11)] = colors["blue"]

# Grupo superior direito — corrigido
# Como o centro está em uma linha ímpar, os vizinhos diagonais
# ficam deslocados uma coluna à direita.
special_cells[(3, 17)] = colors["black"]
special_cells[(2, 17)] = colors["blue"]
special_cells[(2, 18)] = colors["blue"]
special_cells[(3, 16)] = colors["blue"]
special_cells[(3, 18)] = colors["blue"]
special_cells[(4, 17)] = colors["blue"]
special_cells[(4, 18)] = colors["blue"]

for row in range(rows):
    for col in range(cols):
        color = special_cells.get((row, col), region_color(row, col))
        edge = color if (row, col) in special_cells else "#808080"
        lw = 0.4 if (row, col) in special_cells else 0.35
        add_hex(row, col, color, edge=edge, lw=lw)

legend_x = cols * dx + 1.5
legend_y = -2.0

legend_items = [
    (colors["black"], "With observations\nunder analysis"),
    (colors["blue"], "With observations\ninterpreted as neighbors"),
    (colors["red"], "With observations\ninterpreted as NOT neighbors"),
]

def add_legend_hex(x, y, color):
    hexagon = RegularPolygon(
        (x, y),
        numVertices=6,
        radius=0.35,
        orientation=np.radians(30),
        facecolor=color,
        edgecolor=color,
        linewidth=0.4
    )
    ax.add_patch(hexagon)

for i, (c, text) in enumerate(legend_items):
    y = legend_y - i * 3.2
    add_legend_hex(legend_x, y, c)
    ax.text(
        legend_x + 0.7,
        y,
        text,
        va="center",
        ha="left",
        fontsize=11,
        family="DejaVu Sans"
    )

ax.set_aspect("equal")
ax.axis("off")

ax.set_xlim(-0.8, legend_x + 5.8)
ax.set_ylim(-rows * dy - 0.2, 0.8)

plt.tight_layout(pad=0.05)

plt.savefig(out_pdf, bbox_inches="tight")
plt.savefig(out_png, dpi=1000, bbox_inches="tight")

print(f"PDF vetorial criado: {out_pdf}")
print(f"PNG 1000 dpi criado: {out_png}")


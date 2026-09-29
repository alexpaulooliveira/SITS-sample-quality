import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

# ==================== QUALIDADE EDITORIAL ====================

ARTWORK_DPI = 600

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def save_png_svg_pdf_eps(fig, png_path):
    import os

    fig.patch.set_facecolor('white')

    base_path, _ = os.path.splitext(png_path)
    svg_path = base_path + '.svg'
    pdf_path = base_path + '.pdf'
    eps_path = base_path + '.eps'

    fig.savefig(
        png_path,
        bbox_inches='tight',
        dpi=ARTWORK_DPI,
        facecolor='white',
        edgecolor='none',
        format='png',
        metadata={'Software': 'Matplotlib', 'dpi': str(ARTWORK_DPI)},
        pil_kwargs={"dpi": (ARTWORK_DPI, ARTWORK_DPI), "compress_level": 1}
    )

    fig.savefig(svg_path, bbox_inches='tight', dpi=ARTWORK_DPI,
                facecolor='white', edgecolor='none', format='svg')

    fig.savefig(pdf_path, bbox_inches='tight', dpi=ARTWORK_DPI,
                facecolor='white', edgecolor='none', format='pdf')

    fig.savefig(eps_path, bbox_inches='tight', dpi=ARTWORK_DPI,
                facecolor='white', edgecolor='none', format='eps')


# ==================== FIGURA STEP 3 ====================

def generate_step3_neural_grid(output_path="step3_neural_grid.png"):
    fig, ax = plt.subplots(figsize=(4.2, 4.0))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    rows = 10
    cols = 8
    radius = 0.42
    dx = math.sqrt(3) * radius
    dy = 1.5 * radius

    edge_main = "#6f6f6f"
    edge_faint = "#b8b8b8"

    # Área principal mais escura, simulando a malha neural destacada
    main_cells = set()    
    #######################################################
    # Estrutura principal da malha neural
    # Remove apenas a faixa central,
    # mantendo a conexão visual entre topo e base.
    
    for r in range(rows):
        for c in range(cols):
    
            # Corpo principal
            if 1 <= r <= 8 and 1 <= c <= 6:
                main_cells.add((r, c))
    
            # Laterais
            if 2 <= r <= 7 and c == 0:
                main_cells.add((r, c))
    
            if 2 <= r <= 7 and c == 7:
                main_cells.add((r, c))
    
            # Topo
            if r == 0 and 3 <= c <= 6:
                main_cells.add((r, c))
    
            # Base
            if r == 9 and 1 <= c <= 4:
                main_cells.add((r, c))
    
    # Remove apenas os hexágonos centrais
    gap_cells = {
        (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),
        (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7)
    }
    
    main_cells = main_cells - gap_cells
    #######################################################    


    def hex_center(r, c):
    
        # Compacta a malha removendo o vazio central
        if r >= 6:
            r = r - 2
    
        x = c * dx + (r % 2) * dx / 2
        y = -r * dy
    
        return x, y

    
    # Linhas tracejadas verticais superiores
    # Ajustado para remover as três linhas superiores esquerdas
    # que não tocam nenhum hexágono.
    for c in range(5, cols + 2):
        x, y_top = hex_center(0, c - 1)
        ax.plot(
            [x, x],
            [y_top + 0.35, y_top + 2.4],
            color=edge_faint,
            linewidth=1.1,
            linestyle=(0, (2, 3)),
            zorder=1
        )    

    # Linhas tracejadas diagonais à esquerda
    for r in range(3, rows + 2):
        x0, y0 = hex_center(r - 2, 0)
        ax.plot(
            [x0 - 2.8, x0 - 0.35],
            [y0 - 1.4, y0 - 0.15],
            color=edge_faint,
            linewidth=1.1,
            linestyle=(0, (2, 3)),
            zorder=1
        )

    # Pequenos hexágonos tracejados inferiores/esquerdos
    faint_cells = []
    for r in range(7, 10):
        for c in range(-2, 2):
            if r + c > 5:
                faint_cells.append((r, c))

    for r, c in faint_cells:
        x, y = hex_center(r, c)
        ax.add_patch(
            RegularPolygon(
                (x, y),
                numVertices=6,
                radius=radius,
                orientation=math.radians(30),
                facecolor="white",
                edgecolor=edge_faint,
                linewidth=1.0,
                linestyle=(0, (2, 2)),
                zorder=2
            )
        )

    # Malha principal
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in main_cells:
                continue

            x, y = hex_center(r, c)

            ax.add_patch(
                RegularPolygon(
                    (x, y),
                    numVertices=6,
                    radius=radius,
                    orientation=math.radians(30),
                    facecolor="white",
                    edgecolor=edge_main,
                    linewidth=1.45,
                    zorder=3
                )
            )

    # Alguns hexágonos tracejados no topo/direita, como na referência
    extra_top_right = [(0, 7), (0, 8), (1, 8), (2, 8)]
    for r, c in extra_top_right:
        x, y = hex_center(r, c)
        ax.add_patch(
            RegularPolygon(
                (x, y),
                numVertices=6,
                radius=radius,
                orientation=math.radians(30),
                facecolor="white",
                edgecolor=edge_faint,
                linewidth=1.0,
                linestyle=(0, (2, 2)),
                zorder=2
            )
        )

    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_xlim(-3.4, cols * dx + 1.5)
    ax.set_ylim(-rows * dy - 1.2, 2.8)

    save_png_svg_pdf_eps(fig, output_path)
    plt.close(fig)


generate_step3_neural_grid("step3_neural_grid.png")
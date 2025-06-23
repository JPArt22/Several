import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle, Patch
import datetime
import json
import os
import matplotlib.colors as mcolors

# --------------------------------------------------------
# CARGA DE DATOS DESDE JSON CON RUTA ROBUSTA
# --------------------------------------------------------

# Obtener ruta absoluta del script
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'weekly_data.json')

if not os.path.exists(json_path):
    raise FileNotFoundError(f"No se encuentra el archivo {json_path}")

with open(json_path, 'r') as f:
    data = json.load(f)

tasks = data['tasks']
days = data['days']
weekly_data = data['weekly_data']

# --------------------------------------------------------
# CONFIGURACIÓN DE FUENTE PERSONALIZADA
# --------------------------------------------------------

font_path = 'C:/Windows/Fonts/HPSimplified_Rg.ttf'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

# --------------------------------------------------------
# COLORES BASE (MASCULINOS, OSCUROS)
# --------------------------------------------------------

base_colors = [
    "#301A2A", "#003235", "#003C52", "#1C1C1C",
    "#2F4F4F", "#44301D", "#2E2E2E", "#0B2C0B",
    "#121239", "#441515"
]

colors_rgb = [mcolors.hex2color(c) for c in base_colors]

# --------------------------------------------------------
# CREACIÓN DEL GRÁFICO
# --------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7), facecolor='black')
ax.set_facecolor('black')

bottom = np.zeros(len(days))
bar_width = 0.5
x_positions = np.arange(len(days))

for i in range(len(tasks)):
    task_values = [day[i] for day in weekly_data]
    bars = ax.bar(x_positions, task_values, bottom=bottom, 
                  color=colors_rgb[i], edgecolor='#888888', linewidth=1.5, width=bar_width)

    for bar in bars:
        x, y = bar.get_x(), bar.get_y()
        w, h = bar.get_width(), bar.get_height()

        if h > 0:
            intensidad = 0.5  # Cuánto queremos que oscurezca (0 = sin degradado, 1 = todo negro abajo)
            for j in range(100):
                frac = j / 100
                # Degradado progresivo hacia negro
                new_color = np.array(colors_rgb[i]) * (1 - frac * intensidad)
                rect = Rectangle((x, y + h*frac), w, h/100, color=new_color, linewidth=0)
                ax.add_patch(rect)

    bottom += task_values

# --------------------------------------------------------
# LÍNEA DE TOTAL DIARIO
# --------------------------------------------------------

total_per_day = [sum(day) for day in weekly_data]
ax.plot(x_positions, total_per_day, color="#00FFE1", linestyle='-.', marker='o',
        linewidth=1.5, label='Total diario')

for i, total in enumerate(total_per_day):
    ax.text(i, total + 0.4, str(total), color='#DDDDDD', ha='center', fontsize=11)

# --------------------------------------------------------
# PROMEDIO SEMANAL
# --------------------------------------------------------

total_completed = sum(total_per_day)
average = total_completed / 7
props = dict(boxstyle='round', facecolor='black', alpha=0.95, edgecolor="#3AE8CB")
ax.text(0.70, 0.95, f'Weekly Avg: {average:.2f}', transform=ax.transAxes, fontsize=15, 
        verticalalignment='top', bbox=props, color="#3AE8CB")

# --------------------------------------------------------
# ESTÉTICA GENERAL
# --------------------------------------------------------

ax.set_ylim(0, 12)
ax.set_ylabel("Completed Tasks", color='#DDDDDD', fontsize=13)
ax.set_title("Weekly Task Performance", color='#DDDDDD', fontsize=20)
ax.set_xticks(x_positions)
ax.set_xticklabels(days, color='#DDDDDD', fontsize=12)
ax.tick_params(axis='y', colors='#DDDDDD')
plt.grid(axis='y', linestyle='--', alpha=0.3, color='#888888')

# --------------------------------------------------------
# LEYENDA
# --------------------------------------------------------

patches = [Patch(facecolor=colors_rgb[i], edgecolor='#888888', label=tasks[i]) for i in range(len(tasks))]
legend = ax.legend(handles=patches, loc='upper left', bbox_to_anchor=(1.02, 1),
                   facecolor='black', edgecolor='#888888', title='Tasks')
plt.setp(legend.get_title(), color='#DDDDDD')
for text in legend.get_texts():
    text.set_color('#DDDDDD')

plt.tight_layout()

# --------------------------------------------------------
# EXPORTACIÓN AUTOMÁTICA
# --------------------------------------------------------

fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
plt.savefig(f"Weekly_Tasks_{fecha_actual}.png", dpi=300, facecolor=fig.get_facecolor())

plt.show()

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
from matplotlib.patches import Patch
import datetime
import json

# --------------------------------------------------------
# CARGA AUTOMÁTICA DE DATOS DESDE ARCHIVO JSON
# --------------------------------------------------------

with open('weekly_data.json', 'r') as f:
    data = json.load(f)

tasks = data['tasks']
days = data['days']
weekly_data = data['weekly_data']

# --------------------------------------------------------
# CONFIGURACIÓN DE FUENTE PERSONALIZADA
# --------------------------------------------------------

font_path = 'C:/Windows/Fonts/HPSimplified_Rg.ttf'  # Ruta de la fuente
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

# --------------------------------------------------------
# CONFIGURACIÓN GENERAL DE COLORES
# --------------------------------------------------------

colors = [
    "#301A2A", "#003235", "#003C52", "#1C1C1C",
    "#2F4F4F", "#44301D", "#2E2E2E", "#0B2C0B",
    "#121239", "#441515"
]

# --------------------------------------------------------
# CREACIÓN DEL GRÁFICO
# --------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 8), facecolor='black')
ax.set_facecolor('black')

bottom = np.zeros(len(days))
bar_width = 0.6
x_positions = np.arange(len(days))

for i in range(len(tasks)):
    task_values = [day[i] for day in weekly_data]
    bars = ax.bar(x_positions, task_values, bottom=bottom, 
                  color=colors[i], edgecolor='#888888', linewidth=1.5, width=bar_width)
    for bar in bars:
        bar.set_linewidth(0.7)
        bar.set_edgecolor('#888888')
    bottom += task_values

# Línea de rendimiento total diario
total_per_day = [sum(day) for day in weekly_data]
ax.plot(x_positions, total_per_day, color="#00FFE1", linestyle='-.', marker='o',
        linewidth=1.5, label='Total diario')

for i, total in enumerate(total_per_day):
    ax.text(i, total + 0.4, str(total), color='#DDDDDD', ha='center', fontsize=11)

# Recuadro de promedio semanal (a la derecha)
total_completed = sum(total_per_day)
average = total_completed / 7
props = dict(boxstyle='round', facecolor='black', alpha=0.95, edgecolor='#888888')
ax.text(0.70, 0.95, f'Weekly Avg: {average:.2f}', transform=ax.transAxes, fontsize=15, 
        verticalalignment='top', bbox=props, color="#949494")

# Estética general
ax.set_ylim(0, 12)
ax.set_ylabel("Completed Tasks", color='#DDDDDD', fontsize=13)
ax.set_title("Weekly Task Performance", color='#DDDDDD', fontsize=20)
ax.set_xticks(x_positions)
ax.set_xticklabels(days, color='#DDDDDD', fontsize=12)
ax.tick_params(axis='y', colors='#DDDDDD')
plt.grid(axis='y', linestyle='--', alpha=0.3, color='#888888')

# Leyenda de tareas
patches = [Patch(facecolor=colors[i], edgecolor='#888888', label=tasks[i]) for i in range(len(tasks))]
legend = ax.legend(handles=patches, loc='upper left', bbox_to_anchor=(1.02, 1),
                   facecolor='black', edgecolor='#888888', title='Tasks')
plt.setp(legend.get_title(), color='#DDDDDD')
for text in legend.get_texts():
    text.set_color('#DDDDDD')

plt.tight_layout()

# Exportación automática con fecha
fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
plt.savefig(f"Weekly_Tasks_{fecha_actual}.png", dpi=300, facecolor=fig.get_facecolor())

plt.show()

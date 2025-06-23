import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sistema Centralizado", layout="wide")

# Simulación de login con roles (Requerimiento 3)
st.sidebar.title("Ingreso al Sistema")
usuario = st.sidebar.selectbox("Selecciona tu usuario", ["Admin", "Usuario"])
st.sidebar.success(f"Sesión iniciada como: {usuario}")

# Menú principal
menu = st.sidebar.radio("Menú Principal", [
    "Dashboard", 
    "Entradas / Formularios", 
    "Consultas", 
    "Flujos de Aprobación", 
    "Repositorio Documental", 
    "Gestión de Calidad", 
    "Reportes"
])

# 1. Dashboard general
if menu == "Dashboard":
    st.title("🔍 Panel de Actividad")
    st.write("Resumen de actividad reciente y entradas destacadas.")
    st.metric("Entradas nuevas", 12)
    st.metric("Pendientes por aprobar", 3)

# 2. Captura y consulta de formularios (Requerimiento 1)
elif menu == "Entradas / Formularios":
    st.title("📋 Nueva Entrada / Parte")
    tipo = st.selectbox("Tipo de Entrada", ["Inspección", "Revisión Técnica", "Reporte SISO"])
    titulo = st.text_input("Título de la Entrada")
    contenido = st.text_area("Contenido", height=200)
    archivo = st.file_uploader("Subir archivo relacionado")
    if st.button("Enviar"):
        st.success("Entrada registrada con éxito")
        # Aquí simularíamos guardar en base de datos

    st.subheader("📄 Entradas Registradas")
    # Simulación de registros existentes
    st.table([
        {"Fecha": "2024-06-01", "Título": "Inspección de Hormigón", "Estado": "Aprobado"},
        {"Fecha": "2024-06-10", "Título": "Reporte SISO semanal", "Estado": "Pendiente"},
    ])

# 3. Consultas avanzadas (consulta histórica)
elif menu == "Consultas":
    st.title("🔎 Buscador de Formularios")
    autor = st.text_input("Buscar por autor")
    fecha = st.date_input("Filtrar por fecha")
    if st.button("Buscar"):
        st.info("Mostrando resultados simulados...")

# 4. Flujos de aprobación digital (Requerimiento 2)
elif menu == "Flujos de Aprobación":
    st.title("✅ Flujos de Aprobación Digital")
    st.write("Simulación de flujo de órdenes de compra y solicitudes.")
    
    if usuario == "Admin":
        pendientes = [
            {"ID": "OC-001", "Solicitante": "Juan", "Monto": 1200, "Estado": "Pendiente"},
            {"ID": "OC-002", "Solicitante": "Ana", "Monto": 500, "Estado": "Pendiente"},
        ]
        for p in pendientes:
            st.write(f"Orden {p['ID']} - Solicitante: {p['Solicitante']} - Monto: ${p['Monto']}")
            if st.button(f"Aprobar {p['ID']}"):
                st.success(f"Orden {p['ID']} aprobada")
    else:
        st.info("No tiene permisos de aprobación.")

# 5. Repositorio documental (Requerimiento 4 mejorado)
elif menu == "Repositorio Documental":
    st.title("📂 Repositorio Documental con Historial de Versiones")
    st.write("Simulación de carga y control de versiones.")
    st.selectbox("Grupo", ["Obra 1", "Obra 2", "Administración"])
    st.write("Documentos:")
    st.markdown("- Informe técnico.pdf (v1.3, última modificación: 2024-06-15)")
    st.markdown("- Plano fundación.dwg (v2.1, última modificación: 2024-06-10)")

# 6. Gestión de Calidad
elif menu == "Gestión de Calidad":
    st.title("🛠 Módulo de Calidad")
    proceso = st.selectbox("Proceso", ["Fundición", "Acero", "Hormigón"])
    observacion = st.text_area("Observaciones de control")
    if st.button("Registrar evento"):
        st.success("Evento de calidad registrado")

# 7. Reportes y métricas (Requerimiento 5)
elif menu == "Reportes":
    st.title("📊 Reportes y Métricas")
    reporte = st.selectbox("Tipo de reporte", ["Calidad", "Progreso de Obra", "SISO"])
    if st.button("Generar reporte"):
        st.success("Reporte generado (simulado)")
        st.write("✅ Tiempos de aprobación promedio: 2 días")
        st.write("✅ Total de formularios registrados: 34")

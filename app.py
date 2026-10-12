import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de página con icono oficial e interfaz ancha
st.set_page_config(
    page_title="MTC | Control y Búsqueda de Concesiones Postales", 
    layout="wide", 
    page_icon="🏛️"
)

# ==============================================================================
# ESTILOS CSS AVANZADOS Y TIPOGRAFÍA MONTSERRAT
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, div {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Ocultar barra superior por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Banner Superior Institucional */
    .header-banner {
        background: #d40b33;
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(225, 37, 27, 0.2);
    }
    .header-title {
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.5px;
    }
    .header-sub {
        font-size: 0.95rem;
        color: #F8FAFC;
        margin-top: 6px;
        opacity: 0.95;
    }

    /* Tarjetas KPI Institucionales */
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #E1251B;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
    }
    .kpi-sub {
        font-size: 0.85rem;
        font-weight: 600;
        color: #E1251B;
    }

    /* Títulos de sección */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1E293B;
        margin-top: 20px;
        margin-bottom: 12px;
        border-left: 4px solid #E1251B;
        padding-left: 12px;
    }

    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-header {
        background-color: #E1251B;
        color: white;
        padding: 12px 15px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 15px;
        text-align: center;
    }

    /* 1. Fondo rojo MTC para la caja de selección */
    div[data-baseweb="select"] > div {
        background-color: #E1251B !important;
        border-color: #E1251B !important;
    }

    /* 2. Forzar texto blanco en absolutamente todos los elementos internos (p, span, div) */
    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* 3. Ajustar flecha desplegable para que se vea blanca y nítida */
    div[data-baseweb="select"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        width: 1.2rem !important;
        height: 1.2rem !important;
    }

    /* 4. Menú desplegable cuando se abre (fondo blanco con texto oscuro) */
    div[data-baseweb="popover"] ul {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="popover"] li {
        color: #1E293B !important;
    }

    div[data-baseweb="popover"] li:hover {
        background-color: #F1F5F9 !important;
        color: #E1251B !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# CONEXIÓN A DATOS EN VIVO (GOOGLE SHEETS)
# ==============================================================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RkLwQcmhck3r_jc_wj834AR9o2R7FU66koXTSEeh6lk/export?format=csv&gid=0"

def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    df.columns = [str(c).replace('"', '').strip() for c in df.columns]
    
    if 'FECHA DE INICIO DE CONCESION' in df.columns:
        df['FECHA DE INICIO DE CONCESION'] = pd.to_datetime(df['FECHA DE INICIO DE CONCESION'], format='%Y.%m.%d', errors='coerce')
    if 'FECHA DE VENCIMIENTO DE CONCESION' in df.columns:
        df['FECHA DE VENCIMIENTO DE CONCESION'] = pd.to_datetime(df['FECHA DE VENCIMIENTO DE CONCESION'], format='%Y.%m.%d', errors='coerce')
    return df

try:
    df = cargar_datos()
    conexion_ok = True
except Exception as e:
    conexion_ok = False
    st.error(f"⚠️ Error al conectar con Google Sheets: {e}")
    st.stop()

# ==============================================================================
# ENCABEZADO INSTITUCIONAL
# ==============================================================================
st.markdown("""
    <div class="header-banner">
        <div class="header-title">🏛️ MTC - Sistema de Control y Búsqueda de Concesiones Postales</div>
        <div class="header-sub">Ministerio de Transportes y Comunicaciones | Sincronizado en tiempo real</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# BARRA LATERAL - FILTROS
# ==============================================================================
st.sidebar.markdown('<div class="sidebar-header">🔍 Búsqueda y Filtros</div>', unsafe_allow_html=True)

busqueda = st.sidebar.text_input("Razón Social / Concesionario:", placeholder="Ej. DHL, OLVA, EXPRESS...")
ambito_filtro = st.sidebar.multiselect("Ámbito Geográfico:", options=sorted(df['AMBITO'].dropna().unique().tolist()) if 'AMBITO' in df.columns else [])
plazo_filtro = st.sidebar.multiselect("Plazo de Concesión (Años):", options=[5, 10, 15, 20])

# Aplicación de filtros
df_filtrado = df.copy()

if busqueda and 'CONCESIONARIO' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['CONCESIONARIO'].astype(str).str.contains(busqueda, case=False, na=False)]

if ambito_filtro and 'AMBITO' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['AMBITO'].isin(ambito_filtro)]

if plazo_filtro and 'PLAZO DE CONCESION' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['PLAZO DE CONCESION'].isin(plazo_filtro)]

# ==============================================================================
# TARJETAS DE MÉTRICAS (KPIs)
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Registro General</div>
            <div class="kpi-value">{len(df)}</div>
            <div style="font-size:0.75rem; color:#64748B; margin-top:2px;">Concesiones totales</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Resultados Filtrados</div>
            <div class="kpi-value" style="color:#E1251B;">{len(df_filtrado)}</div>
            <div style="font-size:0.75rem; color:#64748B; margin-top:2px;">Coincidencias activas</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Contacto / Alertas</div>
            <div class="kpi-sub" style="margin-top:8px;">falba@mtc.gob.pe</div>
            <div style="font-size:0.75rem; color:#64748B; margin-top:2px;">Notificaciones directas</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Estado Conexión</div>
            <div class="kpi-value" style="color:#16A34A; font-size:1.3rem; margin-top:5px;">🟢 En Vivo</div>
            <div style="font-size:0.75rem; color:#64748B; margin-top:2px;">Google Sheets vinculado</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN 1: FICHA DETALLADA Y QUINQUENIOS
# ==============================================================================
st.markdown('<div class="section-header">📋 Ficha Detallada de Concesión y Quinquenios</div>', unsafe_allow_html=True)

if 'CONCESIONARIO' in df_filtrado.columns:
    lista_empresas = df_filtrado['CONCESIONARIO'].dropna().tolist()
    if lista_empresas:
        empresa_sel = st.selectbox("Seleccione un Concesionario para evaluar:", options=lista_empresas)
        row = df[df['CONCESIONARIO'] == empresa_sel].iloc[0]
        
        with st.container():
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**Ámbito:**\n\n{row.get('AMBITO', 'N/A')}")
            c2.markdown(f"**Plazo Autorizado:**\n\n{row.get('PLAZO DE CONCESION', 'N/A')} Años")
            
            f_inicio = row.get('FECHA DE INICIO DE CONCESION')
            f_venc = row.get('FECHA DE VENCIMIENTO DE CONCESION')
            
            f_inicio_str = f_inicio.strftime('%d/%m/%Y') if pd.notnull(f_inicio) else 'N/A'
            f_venc_str = f_venc.strftime('%d/%m/%Y') if pd.notnull(f_venc) else 'N/A'
            
            c3.markdown(f"**Fecha Inicio:**\n\n{f_inicio_str}")
            c4.markdown(f"**Vencimiento Final:**\n\n{f_venc_str}")
            
            st.markdown("---")
            
            plazo = row.get('PLAZO DE CONCESION')
            hoy = datetime.now()
            
            if plazo == 5:
                st.info

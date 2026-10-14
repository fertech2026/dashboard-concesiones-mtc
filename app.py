import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuración de página con icono oficial e interfaz ancha
st.set_page_config(
    page_title="MTC | Control y Búsqueda de Concesiones Postales", 
    layout="wide", 
    page_icon="🏛️"
)

COLOR_ROJO_MTC = "#E1251B"

# ==============================================================================
# ESTILOS CSS UNIFICADOS (FIX TOTAL DE MULTISELECT, CHIPS Y SCROLLBARS)
# ==============================================================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    /* Tipografía General */
    html, body, [class*="css"], .stMarkdown, p, span, label {{
        font-family: 'Abadi', 'Montserrat', sans-serif !important;
        color: #0F172A;
    }}

    /* Ocultar elementos secundarios y texto de icono residual */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    [data-testid="stSidebarCollapseButton"] span {{
        display: none !important;
    }}

    /* Banner Superior Institucional en Rojo MTC exacto */
    .header-banner {{
        background: {COLOR_ROJO_MTC} !important;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(225, 37, 27, 0.25);
    }}
    .header-title {{
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.5px;
    }}
    .header-sub {{
        font-size: 0.95rem;
        color: #F8FAFC !important;
        margin-top: 6px;
        opacity: 0.95;
    }}

    /* Tarjetas KPI Institucionales */
    .kpi-card {{
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        border-top: 4px solid {COLOR_ROJO_MTC};
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
    }}
    .kpi-label {{
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A !important;
    }}
    .kpi-sub {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {COLOR_ROJO_MTC} !important;
    }}

    /* Títulos de sección */
    .section-header {{
        font-size: 1.25rem;
        font-weight: 700;
        color: #1E293B !important;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 4px solid {COLOR_ROJO_MTC};
        padding-left: 12px;
    }}

    /* Barra Lateral y su Encabezado */
    [data-testid="stSidebar"] {{
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }}
    .sidebar-header {{
        background-color: {COLOR_ROJO_MTC} !important;
        color: white !important;
        padding: 12px 15px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 15px;
        text-align: center;
    }}

    /* CAMPOS DE ENTRADA Y CAJAS DE MULTISELECT EN BARRA LATERAL */
    [data-testid="stSidebar"] input {{
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }}

    [data-testid="stSidebar"] input::placeholder {{
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
    }}

    [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
    }}

    /* ESTILO COMPLETO DE ETIQUETAS/CHIPS DEL MULTISELECT EN ROJO MTC */
    [data-testid="stSidebar"] [data-baseweb="tag"] {{
        background-color: {COLOR_ROJO_MTC} !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 4px 8px !important;
        margin: 2px !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="tag"] span {{
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
    }}

    /* BOTÓN 'X' DE ELIMINAR EN CHIPS DE MULTISELECT */
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {{
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        width: 14px !important;
        height: 14px !important;
    }}

    /* BARRA DESLIZANTE (SCROLLBAR) DENTRO DE LOS SELECTS / MULTISELECTS */
    [data-testid="stSidebar"] div[data-baseweb="select"] ::-webkit-scrollbar {{
        width: 6px !important;
        height: 6px !important;
    }}

    [data-testid="stSidebar"] div[data-baseweb="select"] ::-webkit-scrollbar-thumb {{
        background-color: #94A3B8 !important;
        border-radius: 4px !important;
    }}

    [data-testid="stSidebar"] div[data-baseweb="select"] ::-webkit-scrollbar-track {{
        background-color: #F1F5F9 !important;
    }}

    [data-testid="stSidebar"] div[data-baseweb="select"] svg {{
        fill: {COLOR_ROJO_MTC} !important;
        color: {COLOR_ROJO_MTC} !important;
    }}

    /* Selectbox Principal de Evaluación en Rojo MTC exacto */
    .stMainBlockContainer div[data-baseweb="select"] > div {{
        background-color: {COLOR_ROJO_MTC} !important;
        border: 2px solid {COLOR_ROJO_MTC} !important;
        border-radius: 8px !important;
    }}

    .stMainBlockContainer div[data-baseweb="select"] * {{
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 600 !important;
    }}

    .stMainBlockContainer div[data-baseweb="select"] svg {{
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }}

    /* Popover desplegable de opciones */
    div[data-baseweb="popover"] ul {{
        background-color: #FFFFFF !important;
    }}

    div[data-baseweb="popover"] li, div[data-baseweb="popover"] li * {{
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
    }}

    div[data-baseweb="popover"] li:hover {{
        background-color: #FEF2F2 !important;
    }}

    /* TABLA HTML ROJO MTC SÓLIDO (#E1251B) SIN OPACIDAD */
    .custom-table-container {{
        width: 100%;
        max-height: 480px;
        overflow-y: auto;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        background-color: #FFFFFF;
    }}

    .custom-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Abadi', 'Montserrat', sans-serif;
        font-size: 0.88rem;
    }}

    .custom-table th {{
        background-color: {COLOR_ROJO_MTC} !important;
        color: #FFFFFF !important;
        font-weight: 700;
        text-align: left;
        padding: 12px 14px;
        position: sticky;
        top: 0;
        z-index: 2;
        border-bottom: 2px solid #B91C1C;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }}

    .custom-table td {{
        padding: 10px 14px;
        color: #0F172A !important;
        border-bottom: 1px solid #F1F5F9;
    }}

    .custom-table tr:hover {{
        background-color: #FEF2F2;
    }}

    .custom-table tr:nth-child(even) {{
        background-color: #F8FAFC;
    }}
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
except Exception as e:
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
            <div style="font-size:0.75rem; color:#64748B;">Concesiones totales</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Resultados Filtrados</div>
            <div class="kpi-value" style="color:{COLOR_ROJO_MTC};">{len(df_filtrado)}</div>
            <div style="font-size:0.75rem; color:#64748B;">Coincidencias activas</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Contacto / Alertas</div>
            <div class="kpi-sub" style="margin-top:8px;">falba@mtc.gob.pe</div>
            <div style="font-size:0.75rem; color:#64748B;">Notificaciones directas</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Estado Conexión</div>
            <div class="kpi-value" style="color:#16A34A; font-size:1.3rem; margin-top:5px;">🟢 En Vivo</div>
            <div style="font-size:0.75rem; color:#64748B;">Google Sheets vinculado</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN 1: FICHA DETALLADA Y QUINQUENIOS
# ==============================================================================
st.markdown('<div class="section-header">📋 Ficha Detallada de Concesión y Quinquenios</div>', unsafe_allow_html=True)

if 'CONCESIONARIO' in df_filtrado.columns and not df_filtrado.empty:
    lista_empresas = df_filtrado['CONCESIONARIO'].dropna().tolist()
    empresa_sel = st.selectbox("Seleccione un Concesionario para evaluar:", options=lista_empresas)
    
    row = df_filtrado[df_filtrado['CONCESIONARIO'] == empresa_sel].iloc[0]
    
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
        st.info(f"ℹ️ **Concesión de 5 Años:** No requiere evaluaciones quinquenales intermedias. Vigencia directa hasta el **{f_venc_str}**.")
    elif plazo in [10, 15, 20] and pd.notnull(f_inicio):
        st.markdown("##### 🗓️ Evaluación Legal de Quinquenios")
        num_quinquenios = int(plazo / 5)
        quinquenio_encontrado = False
        
        for q in range(1, num_quinquenios):
            try:
                f_q = f_inicio.replace(year=f_inicio.year + (q * 5))
            except ValueError:
                f_q = f_inicio + timedelta(days=(q * 5 * 365))
            
            f_gracia = f_q + timedelta(days=30)
            
            if f_q >= hoy or (hoy <= f_gracia):
                f_q_str = f_q.strftime('%d/%m/%Y')
                f_gracia_str = f_gracia.strftime('%d/%m/%Y')
                st.write(f"• **{q}º Quinquenio Evaluado:** Vence el **{f_q_str}** | Límite periodo de gracia para pago de tasa: **{f_gracia_str}**")
                
                if hoy < f_q:
                    st.success(f"🟢 **ESTADO VIGENTE:** Faltan {(f_q - hoy).days} días para la siguiente evaluación quinquenal.")
                elif f_q <= hoy <= f_gracia:
                    st.warning(f"🟧 **PERIODO DE GRACIA:** Quedan {(f_gracia - hoy).days} días para efectuar el pago de la Tasa Quinquenal.")
                quinquenio_encontrado = True
                break
        
        if not quinquenio_encontrado:
            st.info(f"• **Tramo Final Cumplido:** Quinquenios intermedios completados satisfactoriamente. Vigencia supeditada a la **Fecha de Vencimiento Final ({f_venc_str})**.")

else:
    st.warning("⚠️ No se encontraron concesionarios con los filtros seleccionados.")

# ==============================================================================
# SECCIÓN 2: ANÁLISIS ESTADÍSTICO Y GRÁFICOS
# ==============================================================================
st.markdown('<div class="section-header">📈 Análisis Estadístico del Padrón</div>', unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)

with col_g1:
    if 'AMBITO' in df_filtrado.columns and not df_filtrado.empty:
        df_ambito = df_filtrado['AMBITO'].value_counts().reset_index()
        df_ambito.columns = ['Ámbito', 'Cantidad']
        
        fig_ambito = px.bar(
            df_ambito, 
            x='Ámbito', 
            y='Cantidad', 
            text='Cantidad',
            title="Concesiones por Ámbito Geográfico",
            color_discrete_sequence=[COLOR_ROJO_MTC]
        )
        fig_ambito.update_layout(
            template="plotly_white", 
            margin=dict(t=40, b=10, l=10, r=10),
            font=dict(color="#0F172A")
        )
        st.plotly_chart(fig_ambito, use_container_width=True)

with col_g2:
    if 'PLAZO DE CONCESION' in df_filtrado.columns and not df_filtrado.empty:
        df_plazo = df_filtrado['PLAZO DE CONCESION'].value_counts().reset_index()
        df_plazo.columns = ['Plazo (Años)', 'Cantidad']
        df_plazo['Plazo (Años)'] = df_plazo['Plazo (Años)'].astype(str) + " Años"
        
        fig_plazo = px.pie(
            df_plazo, 
            names='Plazo (Años)', 
            values='Cantidad', 
            title="Distribución por Plazo Autorizado",
            hole=0.4,
            color_discrete_sequence=[COLOR_ROJO_MTC, '#1E293B', '#64748B', '#94A3B8']
        )
        fig_plazo.update_layout(
            margin=dict(t=40, b=10, l=10, r=10),
            font=dict(color="#0F172A")
        )
        st.plotly_chart(fig_plazo, use_container_width=True)

# ==============================================================================
# SECCIÓN 3: TABLA GENERAL COMPLETA
# ==============================================================================
st.markdown('<div class="section-header">📊 Padrón General de Concesionarios</div>', unsafe_allow_html=True)

df_tabla = df_filtrado.copy()

if not df_tabla.empty:
    if 'FECHA DE INICIO DE CONCESION' in df_tabla.columns:
        df_tabla['FECHA DE INICIO DE CONCESION'] = df_tabla['FECHA DE INICIO DE CONCESION'].dt.strftime('%d/%m/%Y')
    if 'FECHA DE VENCIMIENTO DE CONCESION' in df_tabla.columns:
        df_tabla['FECHA DE VENCIMIENTO DE CONCESION'] = df_tabla['FECHA DE VENCIMIENTO DE CONCESION'].dt.strftime('%d/%m/%Y')

    df_tabla = df_tabla.fillna("-")

    headers_html = "".join([f"<th>{col}</th>" for col in df_tabla.columns])
    
    rows_html = ""
    for _, row in df_tabla.iterrows():
        cells = "".join([f"<td>{val}</td>" for val in row])
        rows_html += f"<tr>{cells}</tr>"

    table_html = f"""
    <div class="custom-table-container">
        <table class="custom-table">
            <thead>
                <tr>{headers_html}</tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.info("No hay registros disponibles para mostrar en la tabla.")

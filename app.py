import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="MTC - Dashboard Concesiones Postales", layout="wide", page_icon="🏛️")

# Estilos personalizados MTC
st.markdown("""
    <style>
    /* Color de encabezado principal */
    .mtc-title {
        color: #E1251B;
        font-weight: bold;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    /* Subtítulos */
    .mtc-subtitle {
        color: #1F2937;
        font-weight: 600;
        font-size: 1.3rem;
    }
    /* Tarjetas de métricas */
    div[data-testid="stMetricValue"] {
        color: #E1251B !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título con estilo MTC
st.markdown('<p class="mtc-title">🏛️ MTC - Sistema de Control y Búsqueda de Concesiones Postales</p>', unsafe_allow_html=True)
st.caption("Sincronizado en tiempo real | Notificaciones dirigidas a falba@mtc.gob.pe")

# ==============================================================================
# ENLACE DE GOOGLE SHEETS
# ==============================================================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RkLwQcmhck3r_jc_wj834AR9o2R7FU66koXTSEeh61k/export?format=csv&gid=0"

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
    st.success("🟢 Conectado en vivo con Google Sheets")
except Exception as e:
    st.error(f"⚠️ Error al conectar con Google Sheets: {e}")
    st.stop()

# Filtros laterales
st.sidebar.header("🔍 Buscador de Concesionarios")
busqueda = st.sidebar.text_input("Ingresar Razón Social / Nombre:", placeholder="Ej. DHL, OLVA, EXPRESS...")
ambito_filtro = st.sidebar.multiselect("Filtrar por Ámbito:", options=sorted(df['AMBITO'].dropna().unique().tolist()) if 'AMBITO' in df.columns else [])
plazo_filtro = st.sidebar.multiselect("Filtrar por Plazo (Años):", options=[5, 10, 15, 20])

df_filtrado = df.copy()

if busqueda and 'CONCESIONARIO' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['CONCESIONARIO'].astype(str).str.contains(busqueda, case=False, na=False)]

if ambito_filtro and 'AMBITO' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['AMBITO'].isin(ambito_filtro)]

if plazo_filtro and 'PLAZO DE CONCESION' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['PLAZO DE CONCESION'].isin(plazo_filtro)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Registro General", len(df))
col2.metric("Resultados Encontrados", len(df_filtrado))
col3.metric("Destinatario Alertas", "falba@mtc.gob.pe")
col4.metric("Dominio Institucional", "@mtc.gob.pe")

st.divider()

# Sección Ficha
st.markdown('<p class="mtc-subtitle">📌 Ficha Detallada y Estado Actual de Quinquenio</p>', unsafe_allow_html=True)
if 'CONCESIONARIO' in df_filtrado.columns:
    lista_empresas = df_filtrado['CONCESIONARIO'].dropna().tolist()
    if lista_empresas:
        empresa_sel = st.selectbox("Seleccione una empresa para consultar:", options=lista_empresas)
        row = df[df['CONCESIONARIO'] == empresa_sel].iloc[0]
        
        with st.expander(f"📋 Ficha Completa: {row['CONCESIONARIO']}", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.write(f"**Ámbito:** {row.get('AMBITO', 'N/A')}")
            c2.write(f"**Plazo Total:** {row.get('PLAZO DE CONCESION', 'N/A')} Años")
            
            f_inicio = row.get('FECHA DE INICIO DE CONCESION')
            f_venc = row.get('FECHA DE VENCIMIENTO DE CONCESION')
            
            f_inicio_str = f_inicio.strftime('%d/%m/%Y') if pd.notnull(f_inicio) else 'N/A'
            f_venc_str = f_venc.strftime('%d/%m/%Y') if pd.notnull(f_venc) else 'N/A'
            
            c3.write(f"**Fecha Inicio:** {f_inicio_str}")
            c4.write(f"**Vencimiento Final:** {f_venc_str}")
            
            plazo = row.get('PLAZO DE CONCESION')
            hoy = datetime.now()
            
            if plazo == 5:
                st.info(f"ℹ️ **Concesión de 5 Años:** No requiere evaluación de quinquenios intermedios. Vence definitivamente el **{f_venc_str}**.")
            elif plazo in [10, 15, 20] and pd.notnull(f_inicio):
                st.markdown("#### 🗓️ Evaluación de Quinquenios")
                num_quinquenios = int(plazo / 5)
                quinquenio_encontrado = False
                
                for q in range(1, num_quinquenios):
                    try:
                        f_q = f_inicio.replace(year=f_inicio.year + (q * 5))
                    except ValueError:
                        f_q = f_inicio + timedelta(days=(q * 5 * 365))
                    
                    f_gracia = f_q + timedelta(days=30)
                    
                    if f_q >= hoy or (hoy <= f_gracia):
                        st.write(f"- **{q}º Quinquenio (Siguiente Evaluado):** Vence el **{f_q.strftime('%d/%m/%Y')}** | Periodo de gracia para pago de

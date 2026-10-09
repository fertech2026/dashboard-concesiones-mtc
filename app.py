import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="MTC - Dashboard Concesiones Postales", layout="wide", page_icon="🏛️")
st.title("🏛️ MTC - Sistema de Control y Búsqueda de Concesiones Postales")
st.caption("Sincronizado en tiempo real | Notificaciones dirigidas a falba@mtc.gob.pe")

# ==============================================================================
# REEMPLAZA "TU_ID_DE_HOJA" CON EL ID REAL DE TU GOOGLE SHEETS
# ==============================================================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RkLwQcmhck3r_jc_wj834AR9o2R7FU66koXTSEeh6lk/export?format=csv&gid=0"

@st.cache_data(ttl=60)
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
    st.error("⚠️ Pendiente vincular ID de Google Sheets o el enlace no es público.")
    st.info("Para vincularlo, edita la variable `SHEET_URL` en `app.py` reemplazando `TU_ID_DE_HOJA` por tu ID de Google Sheets.")
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

# Análisis de Quinquenios Activos
st.subheader("📌 Ficha Detallada y Estado Actual de Quinquenio")
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
                        st.write(f"- **{q}º Quinquenio (Siguiente Evaluado):** Vence el **{f_q.strftime('%d/%m/%Y')}** | Periodo de gracia para pago de tasa hasta: **{f_gracia.strftime('%d/%m/%Y')}**")
                        
                        if hoy < f_q:
                            st.success("🟢 **Estado:** VIGENTE (Faltan " + str((f_q - hoy).days) + " días para el próximo vencimiento de quinquenio)")
                        elif f_q <= hoy <= f_gracia:
                            st.warning("🟧 **Estado:** EN PERIODO DE GRACIA (Quedan " + str((f_gracia - hoy).days) + " días para realizar el pago de la Tasa Quinquenal)")
                        quinquenio_encontrado = True
                        break
                
                if not quinquenio_encontrado:
                    st.write(f"- **Tramo Final:** La empresa ya cumplió sus quinquenios intermedios. Su vigencia se evalúa contra la **Fecha de Vencimiento Final ({f_venc_str})**.")

st.divider()

# Visor General
st.subheader("📋 Lista General de Concesiones Postales")
df_tabla = df_filtrado.copy()
if 'FECHA DE INICIO DE CONCESION' in df_tabla.columns:
    df_tabla['FECHA DE INICIO DE CONCESION'] = df_tabla['FECHA DE INICIO DE CONCESION'].dt.strftime('%Y-%m-%d')
if 'FECHA DE VENCIMIENTO DE CONCESION' in df_tabla.columns:
    df_tabla['FECHA DE VENCIMIENTO DE CONCESION'] = df_tabla['FECHA DE VENCIMIENTO DE CONCESION'].dt.strftime('%Y-%m-%d')

st.dataframe(df_tabla, use_container_width=True, height=400)

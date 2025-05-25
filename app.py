import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Béisbol", layout="wide")

# Leer CSV
df = pd.read_csv("archivo_completo.csv")

st.title("⚾ Dashboard de Béisbol - LAD y NYY")

# =======================
# 1. Gráfico de Pastel
# =======================
st.header("📊 Distribución de 'no_doubter_per'")

if 'no_doubter_per' in df.columns:
    fig1, ax1 = plt.subplots()
    df['no_doubter_per'].fillna('Desconocido', inplace=True)
    df['no_doubter_per'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)
    ax1.set_ylabel('')
    st.pyplot(fig1)
else:
    st.warning("La columna 'no_doubter_per' no está en el archivo.")

# =======================
# 2. HITTERS
# =======================
st.header("🎯 Hitters (position == 'hitter')")
hitters = df[df['position'] == 'hitter']

if not hitters.empty:
    # Dispersión
    st.subheader("Gráfica de Dispersión: barrel_batted_rate vs xwoba")
    if 'barrel_batted_rate' in hitters.columns and 'xwoba' in hitters.columns:
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=hitters, x='barrel_batted_rate', y='xwoba', ax=ax2)
        ax2.set_title("Hitters: Barrel Batted Rate vs xwOBA")
        st.pyplot(fig2)

    # Barra: HR Totales por jugador
    st.subheader("Gráfica de Barra: HR Totales por Jugador")
    if 'player_name' in hitters.columns and 'hr_total' in hitters.columns:
        top_hitters = hitters[['player_name', 'hr_total']].sort_values(by='hr_total', ascending=False).head(10)
        fig3, ax3 = plt.subplots()
        sns.barplot(data=top_hitters, x='hr_total', y='player_name', ax=ax3)
        ax3.set_title("Top 10 Hitters - HR Totales")
        st.pyplot(fig3)
else:
    st.info("No hay datos de hitters para mostrar.")

# =======================
# 3. PITCHERS
# =======================
st.header("🔥 Pitchers (position == 'pitcher')")
pitchers = df[df['position'] == 'pitcher']

if not pitchers.empty:
    # Dispersión
    st.subheader("Gráfica de Dispersión: release_speed vs release_spin_rate")
    if 'release_speed' in pitchers.columns and 'release_spin_rate' in pitchers.columns:
        fig4, ax4 = plt.subplots()
        sns.scatterplot(data=pitchers, x='release_speed', y='release_spin_rate', ax=ax4)
        ax4.set_title("Pitchers: Release Speed vs Spin Rate")
        st.pyplot(fig4)

    # Barra: K% por pitcher
    st.subheader("Gráfica de Barra: Strikeout % (K%) por Pitcher")
    if 'player_name' in pitchers.columns and 'k_percent' in pitchers.columns:
        top_pitchers = pitchers[['player_name', 'k_percent']].sort_values(by='k_percent', ascending=False).head(10)
        fig5, ax5 = plt.subplots()
        sns.barplot(data=top_pitchers, x='k_percent', y='player_name', ax=ax5)
        ax5.set_title("Top 10 Pitchers - K%")
        st.pyplot(fig5)
else:
    st.info("No hay datos de pitchers para mostrar.")

# =======================
# 4. Shohei Ohtani
# =======================
st.header("🌟 Shohei Ohtani - Análisis Especial")
shohei = df[df['player_name'].str.contains("Shohei Ohtani", case=False, na=False)]

if not shohei.empty:
    st.subheader("📋 Datos Generales")
    st.dataframe(shohei)

    st.subheader("📈 Métricas Numéricas")
    numeric_cols = shohei.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        fig6, ax6 = plt.subplots(figsize=(10, 4))
        shohei[numeric_cols].T.plot(kind='bar', legend=False, ax=ax6)
        ax6.set_title("Métricas numéricas de Shohei Ohtani")
        st.pyplot(fig6)
else:
    st.info("Shohei Ohtani no se encuentra en el archivo.")

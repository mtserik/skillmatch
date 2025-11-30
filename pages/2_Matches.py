# pages/2_Matches.py (versão com modos de visualização + labels de ajuda)
import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Matches", layout="centered")

CSV_PATH = "./data/inputs/data.csv"
FOTO_DIR = "./photos"

st.markdown("""
    <style>
        .card {
            background: #F2F3F4;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 12px;
        }
        .name {font-size: 1.1rem; font-weight: 700;}
        .role {font-size: 0.95rem; font-weight: 700; color: #2E86C1;}
        .role-helper {font-size: 0.95rem; font-weight: 700; color: #117A65;}
        .match {font-size: 1rem; color: #117A65; font-weight: 600;}
        .small {font-size: 0.9rem; color: #333;}
    </style>
""", unsafe_allow_html=True)

st.title("🔥 Matches em Tempo Real")

# --- Controles de atualização ---
col_a, col_b = st.columns([3,1])
with col_a:
    st.write("Atualização")
    auto_refresh = st.checkbox("Auto atualizar a cada 5s", value=True)
with col_b:
    if st.button("Atualizar agora"):
        st.rerun()

# --- lê CSV com segurança ---
if not os.path.exists(CSV_PATH):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("Nome,Area,Forte,Fraco\n")

try:
    df = pd.read_csv(CSV_PATH)
except Exception as e:
    st.error(f"Erro ao ler o CSV: {e}")
    st.stop()

if df.empty or len(df) < 1:
    st.info("Aguardando participantes preencherem…")
    st.stop()

df["Forte"] = df["Forte"].fillna("").astype(str)
df["Fraco"] = df["Fraco"].fillna("").astype(str)
df["Nome"] = df["Nome"].fillna("").astype(str)
df["Area"] = df["Area"].fillna("").astype(str)

participantes = (df['Nome'] + df['Area']).unique()
st.success(f"{len(participantes)} participantes registrados")

# --- calcular matches ---
matches = []
for i, row_i in df.iterrows():
    for j, row_j in df.iterrows():
        if i == j:
            continue
        if row_i["Fraco"].strip() != "" and row_i["Fraco"].strip() == row_j["Forte"].strip():
            matches.append((row_i, row_j, row_i["Fraco"].strip()))

# ================================================================
# Seletor de modo
# ================================================================
modo = st.radio(
    "Como deseja visualizar os matches?",
    ["Ver todos os matches", "Filtrar pelo nome do participante"],
    index=0
)

st.divider()

# ================================================================
# MODO 1 — VER TODOS OS MATCHES
# ================================================================
def render_match_card(needy, helper, ponto):
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])

        # -------------------------------------------
        # 🆘 LADO 1: QUEM PRECISA DE AJUDA
        # -------------------------------------------
        c1.markdown("<div class='role'>🆘 Precisa de ajuda</div>", unsafe_allow_html=True)

        foto1 = os.path.join(FOTO_DIR, f"{needy['Nome'].upper()}_{needy['Area'].upper()}.jpg")
        
        if helper['Nome'].upper() in ['JACKELINE', 'JACKE', 'JACK']:
            c2.image(os.path.join(FOTO_DIR, f"{helper['Nome'].upper()}.jpg"), width=100)
        elif os.path.exists(foto1):
            c1.image(foto1, width=100)
        else:
            c2.image(os.path.join(FOTO_DIR, "SEM_FOTO.jpg"), width=100)

        c1.markdown(f"<div class='name'>{needy['Nome']}</div>", unsafe_allow_html=True)
        c1.markdown(f"<div class='small'>Área: {needy['Area']}</div>", unsafe_allow_html=True)

        # -------------------------------------------
        # 🤝 LADO 2: QUEM PODE AJUDAR
        # -------------------------------------------
        c2.markdown("<div class='role-helper'>🤝 Pode ajudar</div>", unsafe_allow_html=True)

        foto2 = os.path.join(FOTO_DIR, f"{helper['Nome'].upper()}_{helper['Area'].upper()}.jpg")
        
        if helper['Nome'].upper() in ['JACKELINE', 'JACKE', 'JACK']:
            c2.image(os.path.join(FOTO_DIR, f"{helper['Nome'].upper()}.jpg"), width=100)
        elif os.path.exists(foto2):
            c2.image(foto2, width=100)
        else:
            c2.image(os.path.join(FOTO_DIR, "SEM_FOTO.jpg"), width=100)

        c2.markdown(f"<div class='name'>{helper['Nome']}</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='small'>Área: {helper['Area']}</div>", unsafe_allow_html=True)

        # Match
        st.markdown(f"<div class='match'>⭐ Match no ponto: {ponto}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # separador
        st.markdown("<hr style='border:0;border-top:1px solid #333;margin:18px 0;'>",
                    unsafe_allow_html=True)


if modo == "Ver todos os matches":

    if not matches:
        st.warning("Nenhum match encontrado ainda…")
    else:
        st.write(f"Encontrados {len(matches)} matches no total.")
        for needy, helper, ponto in matches:
            render_match_card(needy, helper, ponto)

# ================================================================
# MODO 2 — FILTRAR POR PARTICIPANTE
# ================================================================
else:
    st.subheader("Selecione seu nome:")

    nome_selecionado = st.selectbox(
        "Participante",
        sorted(df["Nome"].unique())
    )

    meus_matches = [
        (needy, helper, ponto)
        for (needy, helper, ponto) in matches
        if needy["Nome"] == nome_selecionado or helper["Nome"] == nome_selecionado
    ]

    if not meus_matches:
        st.warning("Nenhum match encontrado para esse participante ainda…")
    else:
        st.success(f"Foram encontrados {len(meus_matches)} matches para {nome_selecionado}:")
        for needy, helper, ponto in meus_matches:
            render_match_card(needy, helper, ponto)

# ------------------------------------
# Auto-refresh
# ------------------------------------
REFRESH_SECONDS = 5
if auto_refresh:
    time.sleep(REFRESH_SECONDS)
    st.rerun()

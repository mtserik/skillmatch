import streamlit as st
import csv
import os
import time

st.set_page_config(page_title="Formulário", layout="centered")

CSV_PATH = "./data/inputs/data.csv"

st.markdown("""
    <style>
        .title {text-align: center; font-size: 1.9rem; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📝 Preencha seu Perfil</div>", unsafe_allow_html=True)

# Perguntas
nome = st.text_input("Primeiro Nome")
area = st.selectbox("Área", ["Planning", "RTM", "Pricing", "Produtividade", "Novos Canais", "OOH_Exportação"])

fortes_lista = ["Liderança", "Comunicação", "Criatividade", "Tecnologia", "Organização"]
fracos_lista = ["Liderança", "Comunicação", "Criatividade", "Tecnologia", "Organização"]

forte = st.selectbox("Ponto Forte (escolha apenas 1)", fortes_lista)
fraco = st.selectbox("Ponto Fraco (escolha apenas 1)", fracos_lista)

if st.button("Enviar", use_container_width=True):
    if not nome or not area:
        st.error("Preencha todos os campos obrigatórios!")
    else:
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([nome, area, forte, fraco])
        
        st.success("Enviado com sucesso! 🎉")
        st.info("Redirecionando para a página de matches...")

        # pequena pausa para mostrar a mensagem
        time.sleep(1)

        # redirecionamento automático
        st.switch_page("pages/2_Matches.py")

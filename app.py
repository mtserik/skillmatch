import streamlit as st

st.set_page_config(page_title="Skill Match", layout="centered")

st.markdown("""
    <style>
        .main-title {text-align: center; font-size: 2.2rem; font-weight: 700; margin-top: 40px;}
        .btn {display: block; width: 100%; padding: 18px; 
              text-align: center; font-size: 1.2rem; margin-top: 20px;
              background: #2E86C1; color: white; border-radius: 10px; text-decoration: none;}
        .btn:hover {background: #1F618D;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🫱🏼‍🫲🏻 Skill Match</div>", unsafe_allow_html=True)

if st.button("👉 Preencher Formulário", use_container_width=True):
    st.switch_page("pages/1_Formulario.py")

if st.button("🔥 Ver Matches", use_container_width=True):
    st.switch_page("pages/2_Matches.py")

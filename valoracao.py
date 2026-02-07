# Importa bibliotecas necessárias
import streamlit as st
import pandas as pd
from formatadores import (
    moeda_para_int,
    int_para_moeda,
    texto_para_percentual,
    seguro_int,
    texto_para_float
)

# Configura a página do Streamlit
st.set_page_config(page_title="Valoração", layout="wide", page_icon="💸")

# Aplica estilo customizado se o arquivo existir
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Título da aplicação
st.title ('Valoração STI')

# Seleção do tipo de jornada
# As opções influenciam os campos exibidos e cálculos realizados
# Apenas para 'Cross-Sell' os campos são exibidos e cálculos feitos

tipo = st.sidebar.selectbox(options= ['Cross-Sell'],label='Opções')
periodicidade = st.sidebar.selectbox(options= ['Não','Sim'], label='Tem Periodicidade?')
if tipo == "Cross-Sell":
    # Entrada de dados pelo usuário
    acessos = st.text_input(
        "Quantidade de acessos únicos por mês",
        value="",
        placeholder="00.000.000",
        label_visibility="visible",
    )
    if periodicidade == 'Sim':
        periodicidade_f = st.text_input(
        "Quantidade de acessos no mês (periodicidade)",
        value="",
        placeholder="00,00",
        label_visibility="visible",
    )
    else:
        periodicidade_f = "0"
        pass
    elegibilidade = st.text_input(
        "Quantidade de elegiveis",
        value="",
        placeholder="00%",
        label_visibility="visible",
    )
    atratividade = st.text_input(
        "Qual a atratividade prevista pra jornada",
        value="",
        placeholder="00%",
        label_visibility="visible",
    )
    conversao = st.text_input(
        "Qual a conversão prevista pra jornada",
        value="",
        placeholder="00%",
        label_visibility="visible",
    )

    # Conversão dos valores de entrada para tipos numéricos
    numero = moeda_para_int(acessos)
    # Calcula elegíveis ANTES de dividir por periodicidade
    percent = texto_para_percentual(elegibilidade)
    topo_val = round(numero * percent)
    # Se periodicidade for 'Sim', divide o topo_val por periodicidade
    if periodicidade == 'Sim':
        periodicidade_int = texto_para_float(periodicidade_f)
        if periodicidade_int == 0:
            periodicidade_int = 1
        topo_val = seguro_int(topo_val / periodicidade_int)
    # Formata para exibição
    topo = int_para_moeda(topo_val)
    # Conversão da atratividade para percentual
    atratividade_pct = texto_para_percentual(atratividade)
    # Calcula o topo do funil considerando atratividade
    topo_funil_val = round(atratividade_pct * topo_val)
    topo_funil = int_para_moeda(topo_funil_val)
    # Conversão da conversão para percentual
    conversao_pct = texto_para_percentual(conversao)
    # Calcula o topo do funil considerando conversão
    topo_funil_conv_val = round(conversao_pct * topo_funil_val)
    topo_funil_conv = int_para_moeda(topo_funil_conv_val)

    col1, col2, col3 = st.columns(3)
    # Exibe os resultados
    col1.code("Clientes Elegíveis: " + topo)
    col2.code("Topo de Funil: " + topo_funil)
    col3.code("Contratações: " + topo_funil_conv)
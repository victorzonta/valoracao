# Importa bibliotecas necessárias
import streamlit as st
import pandas as pd
from formatadores import (
    moeda_para_int,
    int_para_moeda,
    texto_para_percentual,
    seguro_int,
    texto_para_float,
    calcular_premio_venda,
    preencher_tres_percentuais,
    gerar_tabela_resultados_cross_sell
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

tipo = st.sidebar.selectbox(options= ['','Cross-Sell', 'Orgânico', 'Embedded'],label='Opções')

if tipo == "Cross-Sell":
    periodicidade = st.sidebar.selectbox(options= ['Sim','Não'], label='Tem Periodicidade?')
    tipo_ticket = st.sidebar.selectbox(options= ['Menor Ticket','Medio Ticket', 'Maior Ticket', 'Randomico'],label='Opções')
    p1, p2, p3 = preencher_tres_percentuais()
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
        placeholder="00,00%",
        label_visibility="visible",
    )
    conversao = st.text_input(
        "Qual a conversão prevista pra jornada",
        value="",
        placeholder="00,00%",
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
    topo_funil_conv = int_para_moeda(round(topo_funil_conv_val))

    col1, col2, col3, col4 = st.columns(4)
    # Exibe os resultados
    col1.code("Clientes Elegíveis: " + topo)
    col2.code("Topo de Funil: " + topo_funil)
    col3.code("Contratações: " + topo_funil_conv)
    col4.code("Premio de Venda: R$" + int_para_moeda(calcular_premio_venda(topo_funil_conv_val,p1, p2, p3, 4, tipo_ticket)))
    col1,col2,col3,col4 = st.columns(4)
    col1.code("Premio de Venda IA: R$" + int_para_moeda(round(calcular_premio_venda(topo_funil_conv_val,p1, p2, p3, 1, tipo_ticket))))
    col2.code("Premio de Venda IU: R$" + int_para_moeda(round(calcular_premio_venda(topo_funil_conv_val,p1, p2, p3, 2, tipo_ticket))))
    col3.code("Premio de Venda IP: R$" + int_para_moeda(round(calcular_premio_venda(topo_funil_conv_val,p1, p2, p3, 3, tipo_ticket))))
    col4.code("Premio de Venda 1 ano: R$" + int_para_moeda(calcular_premio_venda(topo_funil_conv_val,p1, p2, p3, 4, tipo_ticket)*12))

    df = gerar_tabela_resultados_cross_sell(
        numero,
        periodicidade_int if periodicidade == 'Sim' else 'Não',
        percent,
        atratividade_pct,
        conversao_pct,
        p1, p2, p3,
        moeda_para_int(topo),
        moeda_para_int(topo_funil),
        moeda_para_int(topo_funil_conv),
        tipo_ticket
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.sidebar.download_button(
        label="📥 Baixar resultados (CSV)",
        data=csv,
        file_name="cross_sell.csv",
        mime="text/csv"
    )
if tipo == "Orgânico":
    tipo_ticket = st.sidebar.selectbox(options= ['Menor Ticket','Medio Ticket', 'Maior Ticket', 'Randomico'],label='Opções')
    p1, p2, p3 = preencher_tres_percentuais()
    acessos_organicos = st.text_input(
        "Topo de funil por mês",
        value="",
        placeholder="00.000.000",
        label_visibility="visible",
    )
    conversao_organica = st.text_input(
        "Qual a conversão prevista pra jornada",
        value="",
        placeholder="00,00%",
        label_visibility="visible",
    )
    # Cálculo das efetivações por mês
    acessos_organicos_int = moeda_para_int(acessos_organicos)
    conversao_organica_pct = texto_para_percentual(conversao_organica)
    efetivacoes_mes = round(acessos_organicos_int * conversao_organica_pct)
    efetivacoes_mes_fmt = int_para_moeda(efetivacoes_mes)
    
    #st.code("Premio de Venda: R$" + int_para_moeda(calcular_premio_venda(efetivacoes_mes,p1, p2, p3)))
    col1, col2, col3 = st.columns(3)
    col1.code(f"Efetivações por mês: {efetivacoes_mes_fmt}")
    col2.code("Premio de Venda: R$" + int_para_moeda(calcular_premio_venda(efetivacoes_mes,p1, p2, p3, 4,tipo_ticket)))
    col3.code("Premio de Venda 1 ano: R$" + int_para_moeda(calcular_premio_venda(efetivacoes_mes,p1, p2, p3, 4,tipo_ticket)*12))
    col1, col2, col3 = st.columns(3)
    col1.code("Premio de Venda IA: R$" + int_para_moeda(round(calcular_premio_venda(efetivacoes_mes,p1, p2, p3, 1,tipo_ticket))))
    col2.code("Premio de Venda IU: R$" + int_para_moeda(round(calcular_premio_venda(efetivacoes_mes,p1, p2, p3, 2,tipo_ticket))))
    col3.code("Premio de Venda IP: R$" + int_para_moeda(round(calcular_premio_venda(efetivacoes_mes,p1, p2, p3, 3,tipo_ticket))))
if tipo == "Embedded":
    tipo_ticket = st.sidebar.selectbox(options= ['Menor Ticket','Medio Ticket', 'Maior Ticket', 'Randomico'],label='Opções')
    total_usuarios = st.text_input(
        "Total de usuários",
        value="",
        placeholder="00.000.000",
        label_visibility="visible",
    )
    elegibilidade_emb_bool = st.sidebar.selectbox(options=['Sim','Não'], label='Tem Elegibilidade?')
    if elegibilidade_emb_bool == 'Sim':
        elegibilidade_emb = st.text_input(
            "Quantidade de elegíveis",
            value="",
            placeholder="00%",
            label_visibility="visible",
        )
        elegibilidade_pct = texto_para_percentual(elegibilidade_emb)
    else:
        elegibilidade_pct = 1.0
    conversao_emb = st.text_input(
        "Qual a conversão prevista para a jornada",
        value="",
        placeholder="00,00%",
        label_visibility="visible",
    )
    p1, p2, p3 = preencher_tres_percentuais()
    # Cálculos
    total_usuarios_int = moeda_para_int(total_usuarios)
    topo_emb = round(total_usuarios_int * elegibilidade_pct)
    conversao_pct = texto_para_percentual(conversao_emb)
    contratacoes_emb = round(topo_emb * conversao_pct)
    topo_emb_fmt = int_para_moeda(topo_emb)
    contratacoes_emb_fmt = int_para_moeda(contratacoes_emb)
    st.code(f"Topo de Funil: {topo_emb_fmt}")
    col1, col2, col3 = st.columns(3)
    col1.code(f"Contratações: {contratacoes_emb_fmt}")
    col2.code("Premio de Venda: R$" + int_para_moeda(calcular_premio_venda(contratacoes_emb,p1, p2, p3, 4,tipo_ticket)))
    col3.code("Premio de Venda 1 ano: R$" + int_para_moeda(calcular_premio_venda(contratacoes_emb,p1, p2, p3, 4,tipo_ticket)*12))
    col1, col2, col3 = st.columns(3)
    col1.code("Premio de Venda IA: R$" + int_para_moeda(round(calcular_premio_venda(contratacoes_emb,p1, p2, p3, 1,tipo_ticket))))
    col2.code("Premio de Venda IU: R$" + int_para_moeda(round(calcular_premio_venda(contratacoes_emb,p1, p2, p3, 2,tipo_ticket))))
    col3.code("Premio de Venda IP: R$" + int_para_moeda(round(calcular_premio_venda(contratacoes_emb,p1, p2, p3, 3,tipo_ticket))))
if tipo == '':
    st.markdown("""
    <div style="padding: 16px; border-radius: 8px; margin-top: 16px; color: #fcfbff;">
    <h4 style="text-align:center;font-size: 40px; color:#fcfbff;">Como preencher cada jornada:</h4>
    <ul style="font-size: 20px; color: #fcfbff;">
      <li><b>🟢 Cross-Sell:</b> <br>Informe <b>acessos únicos por mês</b>, <b>elegíveis</b>, <b>atratividade</b>, <b>conversão</b> e, se aplicável, a <b>periodicidade</b>.</li>
      <li><b>🔵 Orgânico:</b> <br>Informe o <b>topo de funil por mês</b> e a <b>conversão prevista</b> para a jornada.</li>
      <li><b>🟣 Embedded:</b> <br>Informe o <b>total de usuários</b>, <b>elegíveis</b> e a <b>conversão prevista</b> para a jornada.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
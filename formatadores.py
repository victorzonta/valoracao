# Funções utilitárias para conversão e formatação de valores

def moeda_para_int(valor: str) -> int:
    """
    Converte uma string representando um valor monetário (ex: 'R$ 1.000.000' ou '4,96')
    para um inteiro, removendo símbolos, pontos e espaços. Se houver vírgula, trata como decimal.
    Retorna 0 se o valor for vazio ou inválido.
    """
    if not valor:
        return 0
    valor = (
        valor.replace("R$", "")
             .replace(".", "")
             .replace(" ", "")
             .replace(",", ".")
    )
    try:
        return int(float(valor))
    except ValueError:
        return 0

def int_para_moeda(valor: int) -> str:
    """
    Formata um inteiro para string no padrão monetário brasileiro,
    usando pontos como separador de milhar.
    """
    return f"{valor:,}".replace(",", ".")

def texto_para_percentual(valor: str) -> float:
    """
    Converte uma string percentual (ex: '80%', '80,5%') para float.
    Retorna 0.0 se o valor for vazio.
    """
    if not valor:
        return 0.0

    valor = (
        valor.replace("%", "")
             .replace(",", ".")
             .strip()
    )
    return float(valor) / 100

def seguro_int(valor) -> int:
    """
    Tenta converter o valor para inteiro de forma segura.
    Se não for possível, retorna 0.
    """
    try:
        return int(float(valor))
    except (ValueError, TypeError):
        return 0
    
def texto_para_float(texto: str) -> float:
    if texto is None:
        return 0.0

    s = str(texto).strip().replace(" ", "")
    if s == "":
        return 0.0

    # pt-BR: "1.234,56" -> "1234.56"
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")

    try:
        return float(s)
    except ValueError:
        return 0.0

def calcular_premio_venda(contratacoes: float, p1: float, p2: float, p3: float, p4: int) -> float:
    """
    Calcula o prêmio de venda a partir do total de contratações e três percentuais,
    usando os valores fixos: 118,8, 178,8 e 300.
    Os percentuais devem ser passados já em formato decimal (ex: 0.75).
    p4 define o tipo de cálculo:
      1 = apenas IA
      2 = apenas IU
      3 = apenas IP
      4 = total (IA + IU + IP)
    """
    faixa1 = p1 * contratacoes * 118.8
    faixa2 = p2 * contratacoes * 178.8
    faixa3 = p3 * contratacoes * 300
    if p4 == 1:
        return round(faixa1)
    elif p4 == 2:
        return round(faixa2)
    elif p4 == 3:
        return round(faixa3)
    elif p4 == 4:
        return round(faixa1 + faixa2 + faixa3)
    else:
        return 0.0

def preencher_tres_percentuais():
    """
    Exibe três campos de input para porcentagens no formato Streamlit,
    retorna os valores convertidos para float.
    """
    import streamlit as st
    p1 = st.sidebar.text_input("Quanto o IA representa na Jornada", value="", placeholder="00%", label_visibility="visible")
    p2 = st.sidebar.text_input("Quanto o IU representa na Jornada", value="", placeholder="00%", label_visibility="visible")
    p3 = st.sidebar.text_input("Quanto o IP representa na Jornada", value="", placeholder="00%", label_visibility="visible")
    from formatadores import texto_para_percentual
    return texto_para_percentual(p1), texto_para_percentual(p2), texto_para_percentual(p3)

def gerar_tabela_resultados_cross_sell(
    total_cpfs_int,
    periodicidade_float,
    elegibilidade_pct,
    atratividade_pct,
    conversao_pct,
    p1, p2, p3,
    clientes_elegiveis_period,
    topo_funil,
    contratacoes
):
    import pandas as pd

    premio_ia = calcular_premio_venda(contratacoes, p1, p2, p3, 1)
    premio_iu = calcular_premio_venda(contratacoes, p1, p2, p3, 2)
    premio_ip = calcular_premio_venda(contratacoes, p1, p2, p3, 3)
    premio_total = calcular_premio_venda(contratacoes, p1, p2, p3, 4)

    def moeda_br(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    df = pd.DataFrame([
        {
            "Total de CPFs": int_para_moeda(total_cpfs_int),
            "Periodicidade": periodicidade_float,
            "Elegibilidade (%)": f"{elegibilidade_pct*100:.2f}%",
            "Clientes Elegíveis": int_para_moeda(clientes_elegiveis_period),
            "Atratividade (%)": f"{atratividade_pct*100:.2f}%",
            "Topo de Funil": int_para_moeda(topo_funil),
            "Conversão (%)": f"{conversao_pct*100:.2f}%",
            "Contratações": int_para_moeda(contratacoes),

            # 👇 agora com R$ na frente
            "Premio de Venda IA": moeda_br(premio_ia),
            "Premio de Venda IU": moeda_br(premio_iu),
            "Premio de Venda IP": moeda_br(premio_ip),
            "Premio de Venda Total": moeda_br(premio_total)
        }
    ])

    df = df.T.reset_index()
    df.columns = ["Etapas", "Valor"]
    return df

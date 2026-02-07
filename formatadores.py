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
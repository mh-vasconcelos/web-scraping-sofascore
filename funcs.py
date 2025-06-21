import re
class Pipeline2Processor:
    def __init__(self, data_dict):
        self.data = data_dict

    def conta_size(self):
        return [len(v) for v in self.data.values()]

    def todos_iguais(self, lista):
        return all(x == lista[0] for x in lista)

    def jogos_futuros(self):
        for k, v in self.data.items():
            while len(v) < self.max_len:
                v.append('Vazio')

    def ajusta_placar_vazio(self):
        while not self.todos_iguais(self.conta_size()):
            self.max_len = max(self.conta_size())
            self.jogos_futuros()
        return self.data

    @staticmethod
    def remover_padrao(texto):
        return re.sub(r'\n\d+', '', texto)

    @staticmethod
    def verifica_data(lista):
        padrao = re.compile(r'\b[0-3]\d/[0-1]\d/24\b')
        return any(padrao.search(item) for item in lista)

    @staticmethod
    def is_date(text):
        return bool(re.match(r'^\d{2}/\d{2}/\d{2}$', text))
    



# Ajuste refatorado

PATTERN_HORA   = re.compile(r'^\d{2}:\d{2}$')
PATTERN_DIGITO = re.compile(r'^\d')

def eh_hora(texto):
    """Retorna True se 'texto' for algo como '19:30'."""
    return bool(texto) and PATTERN_HORA.match(texto)

def comeca_com_digito(texto):
    """Retorna True se a primeira letra de 'texto' for dígito (usado para placar)."""
    return bool(texto) and PATTERN_DIGITO.match(texto)

def parsear_placar(lines, base_idx):
    """
    Tenta extrair placar_casa, placar_fora e resultado a partir de lines[base_idx:], 
    retornando (score_casa, score_fora, resultado, incremento).
    Se não encontrar placar válido, retorna (None, None, None, 0).
    """
    # ex.: base_idx é i+4 na chamada
    if base_idx >= len(lines):
        return None, None, None, 0

    linha = lines[base_idx]
    if not comeca_com_digito(linha):
        # não tem placar aí
        return None, None, None, 0

    # capturamos score_casa
    score_casa = linha.strip()[0]

    # Precisamos checar se existe duplicação de placar
    # Caso bom (sem duplicação):
    #    lines[i+5] é placar_fora, lines[i+6] é resultado
    #    incremento = 7 (data, status, home, away, sc_casa, sc_fora, resultado)
    #
    # Caso ruim (duplicação):
    #    lines[i+6] e lines[i+7] são dígitos (placar_casa e placar_fora)
    #    resultado em lines[i+8], incremento = 9
    idx_fora_candidato   = base_idx + 1  # seria i+5
    idx_possivel_dup1    = base_idx + 2  # seria i+6
    idx_possivel_dup2    = base_idx + 3  # seria i+7
    idx_resultado_dup    = base_idx + 4  # seria i+8

    # Cenário “bom”
    if (
        idx_fora_candidato < len(lines)
        and comeca_com_digito(lines[idx_fora_candidato])
        and not (
            idx_possivel_dup1 < len(lines)
            and idx_possivel_dup2 < len(lines)
            and comeca_com_digito(lines[idx_possivel_dup1])
            and comeca_com_digito(lines[idx_possivel_dup2])
        )
    ):
        score_fora = lines[idx_fora_candidato].strip()[0]
        resultado  = lines[idx_fora_candidato + 1] if (idx_fora_candidato + 1) < len(lines) else None
        incremento = 7
        return score_casa, score_fora, resultado, incremento

    # Cenário “ruim” (duplicação de placares)
    if (
        idx_possivel_dup1 < len(lines)
        and idx_possivel_dup2 < len(lines)
        and comeca_com_digito(lines[idx_possivel_dup1])
        and comeca_com_digito(lines[idx_possivel_dup2])
    ):
        score_fora = lines[idx_possivel_dup1].strip()[0]
        resultado  = lines[idx_resultado_dup] if idx_resultado_dup < len(lines) else None
        incremento = 9
        return score_casa, score_fora, resultado, incremento

    # Se entrou aqui, não conseguiu parsear placar corretamente
    return None, None, None, 0

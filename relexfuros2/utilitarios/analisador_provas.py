import os
from datetime import datetime

def guardar_em_ficheiro(texto, prefixo="prova"):
    pasta = "relexfuros2/registos"
    os.makedirs(pasta, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_ficheiro = os.path.join(pasta, f"{prefixo}_{timestamp}.txt")
    with open(nome_ficheiro, "w", encoding="utf-8") as f:
        f.write(texto)
    return f"🗂️ Documento guardado em: {nome_ficheiro}"

def analisar_texto_prova(pergunta):
    texto = (
        "📎 Prova registada.\n"
        f"Conteúdo: {pergunta.strip()}\n"
        "Esta informação será usada em futura denúncia ou carta."
    )
    return guardar_em_ficheiro(texto)

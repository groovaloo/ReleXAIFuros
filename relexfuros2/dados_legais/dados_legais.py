import os

PASTA_DADOS = os.path.dirname(__file__)

def extrair_texto_relevante(pergunta):
    resultados = []

    if not os.path.exists(PASTA_DADOS):
        return resultados

    for ficheiro in os.listdir(PASTA_DADOS):
        if ficheiro.endswith(".txt"):
            caminho = os.path.join(PASTA_DADOS, ficheiro)
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
                if pergunta.lower() in conteudo.lower():
                    resultados.append((ficheiro, conteudo.strip()))
                elif any(palavra in conteudo.lower() for palavra in pergunta.lower().split()):
                    excerto = conteudo[:600] + "..." if len(conteudo) > 600 else conteudo
                    resultados.append((ficheiro, excerto.strip()))

    return resultados

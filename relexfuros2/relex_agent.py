import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import glob
from datetime import datetime
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from docx import Document

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# --- IMPORTS RELATIVOS AO PROJETO ---
from relexfuros2.dados_legais.dados_legais import extrair_texto_relevante
from relexfuros2.utilitarios.gerador_documentos import guardar_carta_formatada
from relexfuros2.utilitarios.analisador_provas import analisar_texto_prova

# --- INICIALIZAÇÃO ---
load_dotenv()
llm = Ollama(model="llama2")
memoria = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🔇 Tavily desativado temporariamente
# from langchain_community.tools.tavily_search import TavilySearchResults
# api_key = os.getenv("TAVILY_API_KEY")
# search = TavilySearchResults(tavily_api_key=api_key)
# tools = [
#     Tool(
#         name="TavilySearch",
#         func=search.run,
#         description="Usa pesquisa online para encontrar informação legal ou técnica.",
#     ),
# ]
tools = []

agente = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memoria,
)

# --- FUNÇÕES AUXILIARES ---
def guardar_em_ficheiro(texto, prefixo="caso"):
    pasta = "relexfuros2/registos"
    os.makedirs(pasta, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    caminho = os.path.join(pasta, f"{prefixo}_{timestamp}.txt")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    return f"🗂️ Documento guardado em: {caminho}"

def gerar_carta_formal(pergunta, nome="Cooper", local="Lisboa"):
    corpo = (
        "Exmos. Senhores,\n\n"
        "Venho por este meio apresentar denúncia relativa à execução de um furo supostamente ilegal no meu terreno, "
        "sem a devida licença emitida pela Agência Portuguesa do Ambiente, ao abrigo do Decreto-Lei n.º 226-A/2007.\n\n"
        f"A entidade executora mencionada é 'Água Viva Perfurações'.\n\n"
        f"Descrição do caso:\n{pergunta.strip()}\n\n"
        "Solicito a análise da situação e eventual responsabilização da entidade executora.\n"
    )
    return guardar_carta_formatada(corpo, nome=nome, destino="Agência Portuguesa do Ambiente", local=local)

def gerar_denuncia(pergunta):
    texto = (
        "Exmos. Senhores,\n\n"
        "Venho por este meio apresentar denúncia relativa à execução de um furo aparentemente ilegal no meu terreno, "
        "sem a devida licença emitida pela Agência Portuguesa do Ambiente (DL 226-A/2007).\n\n"
        f"Entidade executora: Água Viva Perfurações\n\nDescrição:\n{pergunta}\n\n"
        "Com os melhores cumprimentos,\nCooper"
    )
    return guardar_em_ficheiro(texto, prefixo="denuncia")

def registar_prova(pergunta):
    texto = (
        "📎 Prova registada.\n"
        f"Conteúdo: {pergunta.strip()}\n"
        "Esta informação será usada em futura denúncia ou carta."
    )
    return guardar_em_ficheiro(texto, prefixo="prova")

def procurar_em_documentos(pergunta):
    pasta = "relexfuros2/dados_legais"
    if not os.path.exists(pasta):
        return None

    pergunta_lower = pergunta.lower()
    resultados = []

    for ficheiro in glob.glob(os.path.join(pasta, "*.txt")):
        with open(ficheiro, "r", encoding="utf-8") as f:
            conteudo = f.read().lower()
            palavras = pergunta_lower.split()
            coincidencias = sum(1 for p in palavras if p in conteudo)
            if pergunta_lower in conteudo or coincidencias >= 2:
                trechos = conteudo[:500].strip().replace("\n", " ")
                resultados.append(f"🔹 {os.path.basename(ficheiro)}: {trechos}...")

    if resultados:
        return "\n\n".join(resultados)
    return None

def gerar_email_denuncia(pergunta, nome="Cooper", email="cooper@email.com", destino="geral@apambiente.pt"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    anexo = f"carta_{timestamp}.docx"
    assunto = "Denúncia de perfuração ilegal – Água Viva Perfurações"
    corpo = (
        f"Assunto: {assunto}\nPara: {destino}\nDe: {email}\n\n"
        "Segue em anexo denúncia de furo ilegal pela 'Água Viva Perfurações' "
        "(DL 226-A/2007).\n\n"
        f"{pergunta.strip()}\n\nCom os melhores cumprimentos,\n{nome}\n\nAnexo: {anexo}"
    )
    return guardar_em_ficheiro(corpo, prefixo="email")

def tratar_categoria(categoria, pergunta):
    p = pergunta.lower()

    if categoria == "furos":
        if "carta" in p or "formal" in p:
            return gerar_carta_formal(pergunta)
        if "prova" in p or "anexar" in p or "foto" in p:
            return registar_prova(pergunta)
        if "denúncia" in p or "redigir" in p:
            return gerar_denuncia(pergunta)
        if "e-mail" in p or "email" in p:
            return gerar_email_denuncia(pergunta)

        return (
            "💧 Caso de furo detectado. O que pretende fazer?\n"
            "- 📄 Gerar carta formal\n"
            "- 📝 Redigir denúncia\n"
            "- 📧 Gerar e-mail automático\n"
            "- 📎 Anexar prova\n"
            "- ❌ Terminar"
        )

    return None

def correr_pergunta_relex(pergunta):
    p = pergunta.lower()

    if any(k in p for k in ["furo", "perfuração", "denúncia", "prova", "carta", "email"]):
        resposta = tratar_categoria("furos", pergunta)
        if resposta:
            return resposta

    if any(k in p for k in ["legislação", "licença", "apa", "diário da república", "zona protegida", "lagoa de óbidos", "captação"]):
        local = procurar_em_documentos(pergunta)
        if local:
            return f"📄 Info local encontrada:\n\n{local}\n\nO que faz a seguir?\n- 📄 Carta\n- 📧 Email\n- ❌ Terminar"

    print("🧠 Usando modelo Ollama...")
    return agente.run(pergunta)

# --- LOOP PRINCIPAL ---
if __name__ == "__main__":
    print("👋 ReLexFuros pronta para assistir com furos de água.\n")
    print("Exemplos:\n- 'Empresa fez um furo sem licença'\n- 'Quero redigir denúncia'\n- 'Preciso de licença?'\n")
    while True:
        q = input("Pergunta > ").strip()
        if q.lower() in ["sair", "exit", "q"]:
            print("👋 Até breve.")
            break
        resp = correr_pergunta_relex(q)
        print("\n🔸 Resposta:\n", resp, "\n" + "-" * 50 + "\n")
        if "❌ Terminar" in resp:
            print("👋 Até breve.")
            break

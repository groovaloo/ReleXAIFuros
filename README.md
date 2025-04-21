# ReleXAIFuros

**ReleXAIFuros** is an intelligent legal assistant designed to help users in Portugal deal with issues related to illegal water boreholes ("furos"). It allows users to generate formal complaints, attach evidence, and reference relevant local legislation automatically.

## 🧠 What It Does

- Detects and classifies water borehole cases
- Searches local legal documents for relevant info
- Generates formal letters, emails, and complaints
- Records and stores legal evidence
- Integrates with LLMs and optionally with Tavily for external legal verification

## 🗂️ Project Structure


relexfuros2/ │ ├── dados_legais/ # Legal data (laws, regulations, rulings) ├── registos/ # Generated files (complaints, emails, evidence) ├── utilitarios/ # Utility functions (document creation, file parsing) ├── relex_agent.py # Main script (core ReleX agent) ├── run.sh # Quick run script ├── run_debug.sh # Debug run script └── requirements.txt # Python dependencies

bash
Copiar
Editar



## 🚀 How to Run

Make sure you have Python 3.11+ installed and `ollama` running locally.

1. Clone the repository:
   ```bash
   git clone https://github.com/groovaloo/ReleXAIFuros.git
   cd ReleXAIFuros
Create a .env file (optional, for Tavily integration):

ini
Copiar
Editar
TAVILY_API_KEY=your_api_key_here
Install dependencies:

bash
Copiar
Editar
pip install -r requirements.txt
Run the assistant:

bash
Copiar
Editar
PYTHONPATH=. python relexfuros2/relex_agent.py
Or use:

bash
Copiar
Editar
./run.sh          # normal mode
./run_debug.sh    # verbose debug mode
📎 Features
📝 Draft legal complaints and formal documents

📎 Register and attach photo or text evidence

📧 Generate email-ready legal notices

📄 Search local legal files first (offline)

🌐 [Optional] Use Tavily to verify laws against official Portuguese government sources (*.gov.pt, dre.pt, etc.)

📌 Future Plans
Automated case validation

Agent chain with law-update verification

PDF parsing of official licenses

Integration with small claims submissions (Julgados de Paz)

💬 Example Prompts
text
Copiar
Editar
Empresa fez um furo sem licença
Quero redigir denúncia
Preciso de licença para captação subterrânea em zona protegida?
🛠️ Dev Notes
This project is in active development. For now, local legislation must be stored in relexfuros2/dados_legais/. External API access (e.g., Tavily) is optional and can be toggled via code comments.

Made with legal rage and righteous code.
— Cooper & Diane 💼💧


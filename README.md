# 🏛️ Painel do Eleitor - Portal de Notícias Legislativas

O **Painel do Eleitor** é uma plataforma web que transforma pautas legislativas complexas (PECs e PLs) em notícias acessíveis utilizando Inteligência Artificial. O sistema também permite que cidadãos acompanhem pautas específicas via WhatsApp.

## 🚀 Funcionalidades

- **Monitoramento Automático**: Captura dados reais da API da Câmara e do Senado.
- **IA Jornalística**: Utiliza o Google Gemini para reescrever eixos técnicos em artigos fáceis de ler.
- **Filtro Inteligente**: Busca por tema ou número da pauta com Scroll Infinito.
- **Captura de Leads**: Sistema de cadastro para acompanhamento via WhatsApp.
- **Painel Administrativo**: Gestão de contatos e interesses dos usuários.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11 + Flask
- **Banco de Dados**: SQLite3
- **Frontend**: Bootstrap 5, FontAwesome e JavaScript (Vanilla)
- **IA**: Google Gemini API (via Generative AI SDK)
- **Integração**: API de Dados Abertos da Câmara dos Deputados

## 📦 Como instalar

1. **Clonar o repositório**:

   ```bash
   git clone [https://github.com/seu-usuario/painel-eleitor.git](https://github.com/seu-usuario/painel-eleitor.git)

   ```

2. **Criar e ativar o ambiente virtual (Python 3.11)**:
   python -m venv venv
   source venv/scripts/activate # No Windows

3. **Instalar as dependências**:
   pip install -r requirements.txt

4. **Configurar a API Key**:
   Crie uma variável de ambiente ou edite o script de fetch com sua chave do Gemini.

5. **Instalar as dependências**:
   python database.py
   python fetch_data.py

6. **Rodar o projeto**:
   python app.py

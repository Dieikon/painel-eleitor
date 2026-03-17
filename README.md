#English
🏛️ Voter Panel - Legislative News Portal
Voter Panel (Painel do Eleitor) is a web platform that transforms complex legislative agendas (PECs and PLs) into accessible news using Artificial Intelligence. The system also allows citizens to follow specific topics via WhatsApp.

🚀 Features
**Automatic Monitoring**: Captures real-time data from the Chamber of Deputies and Senate APIs.
**Journalistic AI**: Uses Google Gemini to rewrite technical terms into easy-to-read articles.
**Smart Filter**: Search by theme or bill number with Infinite Scroll.
**Lead Capture**: Registration system for updates via WhatsApp.
**Admin Dashboard**: Management of contacts and user interests.

🛠️ Technologies Used

**Backend**: Python 3.11 + Flask
**Database**: SQLite3
**Frontend**: Bootstrap 5, FontAwesome, and JavaScript (Vanilla)
**AI**: Google Gemini API (via Generative AI SDK)
**Integration**: Brazilian Chamber of Deputies Open Data API


## 📸 System Demonstration

<p align="center">
<img width="1920" height="987" alt="Image" src="https://github.com/user-attachments/assets/ace23d1e-e9ef-4ae9-923f-fb5cf5564dad" />

<img width="1920" height="886" alt="Image" src="https://github.com/user-attachments/assets/00e0f5fa-50b5-4a96-868b-7984f426ee98" />

<img width="1920" height="884" alt="Image" src="https://github.com/user-attachments/assets/1c1f19c8-f370-4971-932b-0c3befb28eec" />

<img width="1920" height="884" alt="Image" src="https://github.com/user-attachments/assets/6fb7fbd6-6ac2-4bca-93d2-2d9c3c092267" />

<img width="1920" height="918" alt="Image" src="https://github.com/user-attachments/assets/c3179d26-b0c6-48d6-ba88-ea5c01cb1699" />
</p>

📦 Installation
Clone the repository:

Bash
git clone https://github.com/your-username/voter-panel.git
Create and activate the virtual environment (Python 3.11):

Bash
python -m venv venv
# On Windows:
source venv/Scripts/activate 
# On Linux/Mac:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure API Key:
Create an environment variable or edit the fetch script with your Gemini API key.

Initialize Database and Data:

Bash
python database.py
python fetch_data.py
Run the project:

Bash
python app.py


📦 Installation
Clone the repository:

Bash
git clone https://github.com/your-username/painel-eleitor.git
Create and activate the virtual environment (Python 3.11):

Bash
python -m venv venv
# On Windows:
source venv/Scripts/activate 
# On Linux/Mac:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure API Key:
Create an environment variable or edit the fetch script with your Gemini API key.

Initialize Database and Data:

Bash
python database.py
python fetch_data.py
Run the project:

Bash
python app.py

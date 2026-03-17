# 🏛️ Voter Panel (Painel do Eleitor)
> **Transforming complex legislative agendas into accessible news through AI.**

The **Voter Panel** is a web platform designed to bridge the gap between the legislative branch and the citizen. It converts technical and complex bills (PECs and PLs) into readable journalistic articles using Google Gemini AI. Additionally, it features a notification system for users to follow specific topics via WhatsApp.

---

## 🚀 Key Features

* **📡 Real-Time Monitoring**: Automated data ingestion from the Brazilian Chamber of Deputies and Senate APIs.
* **🤖 AI-Powered Journalism**: Leverages the **Google Gemini API** to translate "legalese" into clear, accessible language.
* **🔍 Smart Discovery**: Search for specific bills by theme or number with a seamless **Infinite Scroll** interface.
* **📱 WhatsApp Integration**: Lead capture system allowing citizens to subscribe to updates on specific legislative topics.
* **🛡️ Admin Dashboard**: Secure area for managing contacts, user interests, and system insights.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54) **Python 3.11** + Flask |
| **Database** | ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=flat&logo=sqlite&logoColor=white) **SQLite3** |
| **Frontend** | ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=flat&logo=bootstrap&logoColor=white) **Bootstrap 5**, FontAwesome, Vanilla JS |
| **Artificial Intelligence** | ![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=flat&logo=googlegemini&logoColor=white) **Google Gemini SDK** |
| **Data Source** | **Câmara dos Deputados** (Open Data API) |

---

## 📸 System Showcase

<p align="center">
  <img width="100%" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/ace23d1e-e9ef-4ae9-923f-fb5cf5564dad" />
</p>

<div align="center">
  <img width="49%" alt="Detail View 1" src="https://github.com/user-attachments/assets/00e0f5fa-50b5-4a96-868b-7984f426ee98" />
  <img width="49%" alt="Detail View 2" src="https://github.com/user-attachments/assets/1c1f19c8-f370-4971-932b-0c3befb28eec" />
</div>

<div align="center">
  <img width="49%" alt="Admin Panel" src="https://github.com/user-attachments/assets/6fb7fbd6-6ac2-4bca-93d2-2d9c3c092267" />
  <img width="49%" alt="Lead Capture" src="https://github.com/user-attachments/assets/c3179d26-b0c6-48d6-ba88-ea5c01cb1699" />
</div>

---

## 📦 Installation & Setup

Follow these steps to get the project running locally:

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/voter-panel.git](https://github.com/your-username/voter-panel.git)
cd voter-panel

2. Environment Setup
Create a virtual environment using Python 3.11:
python -m venv venv

# Activate on Windows:
source venv/Scripts/activate 

# Activate on Linux/Mac:
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure API Keys
Create a .env file or export your Gemini API key:
export GEMINI_API_KEY="your_api_key_here"

5. Initialize Database & Fetch Data
python database.py
python fetch_data.py

6. Launch Application
python app.py


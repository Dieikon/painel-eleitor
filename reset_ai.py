import sqlite3
from database import DB_NAME

def reset_ai_texts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Isso apaga APENAS o trabalho do Gemini, mantendo as pautas e fotos a salvo!
    cursor.execute('''
        UPDATE bills 
        SET ai_title = NULL, ai_summary = NULL, ai_article_html = NULL
    ''')
    
    conn.commit()
    conn.close()
    print("🧹 Banco limpo! Os textos da IA foram apagados, mas as fotos e pautas continuam lá.")
    print("👉 Agora você pode rodar 'python fetch_data.py' para a IA reescrever as matérias.")

if __name__ == '__main__':
    reset_ai_texts()
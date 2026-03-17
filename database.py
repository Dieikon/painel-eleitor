import sqlite3
import os

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela 1: Deputados (Fica vazia por enquanto, estamos usando a busca direta)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deputies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            party TEXT NOT NULL,
            state TEXT NOT NULL,
            photo_url TEXT
        )
    ''')

    # Tabela 2: Pautas (Bills)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY,           
            type_acronym TEXT NOT NULL,       
            number INTEGER NOT NULL,
            year INTEGER NOT NULL,
            summary TEXT NOT NULL,            
            author_name TEXT,                 
            author_photo_url TEXT,
            author_party TEXT,                
            url_inteiro_teor TEXT,            -- NOVO: Link do PDF Oficial para a IA ler
            ai_title TEXT,                    
            ai_summary TEXT,                  
            ai_article_html TEXT,             
            status TEXT,                      
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela 3: Leads (Contatos para WhatsApp) - NOVO!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            bill_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bill_id) REFERENCES bills (id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


if __name__ == '__main__':
    # Se rodar este arquivo direto, ele cria as tabelas
    init_db()
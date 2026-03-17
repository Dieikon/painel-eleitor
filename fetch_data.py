import requests
import sqlite3
import time
import json
import os
import re
import io
import PyPDF2
from google import genai
from dotenv import load_dotenv
from database import DB_NAME, get_db_connection

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("ERRO: A chave GEMINI_API_KEY não foi encontrada no arquivo .env!")

CHAMBER_API_URL = "https://dadosabertos.camara.leg.br/api/v2"

def get_senators_dict():
    print("Buscando dados do Senado...")
    senators_map = {}
    try:
        url = "https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            parlamentares = data.get('ListaParlamentarEmExercicio', {}).get('Parlamentares', {}).get('Parlamentar', [])
            for p in parlamentares:
                ident = p.get('IdentificacaoParlamentar', {})
                nome = ident.get('NomeParlamentar', '').upper()
                foto = ident.get('UrlFotoParlamentar', '')
                partido = ident.get('SiglaPartidoParlamentar', '')
                if nome and foto:
                    senators_map[nome] = {"foto": foto, "partido": partido}
    except Exception as e:
        print(f"Aviso: Não foi possível carregar Senadores ({e})")
    return senators_map

def extract_text_from_pdf(pdf_url):
    if not pdf_url:
        return ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(pdf_url, headers=headers, timeout=20, allow_redirects=True)
        
        if res.status_code == 200:
            if b'%PDF' in res.content[:5] or 'application/pdf' in res.headers.get('Content-Type', '').lower():
                reader = PyPDF2.PdfReader(io.BytesIO(res.content))
                text = ""
                for page in reader.pages[:15]:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                return text
    except Exception as e:
        pass
    return ""

def fetch_recent_bills():
    QTD_PECS_DESEJADAS = 2
    QTD_PLS_URGENTES_DESEJADOS = 2
    
    print(f"Iniciando sincronização (Alvos: {QTD_PECS_DESEJADAS} PEC e {QTD_PLS_URGENTES_DESEJADOS} PL Urgente)...")
    senators_map = get_senators_dict()
    
    buscas = [
        {
            "tipo": "PEC",
            "url": f"{CHAMBER_API_URL}/proposicoes?siglaTipo=PEC&ordem=DESC&ordenarPor=id&itens={QTD_PECS_DESEJADAS}",
            "alvo": QTD_PECS_DESEJADAS
        },
        {
            "tipo": "PL",
            "url": f"{CHAMBER_API_URL}/proposicoes?siglaTipo=PL&ordem=DESC&ordenarPor=id&itens=300",
            "alvo": QTD_PLS_URGENTES_DESEJADOS
        }
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    for busca in buscas:
        try:
            response = requests.get(busca["url"], timeout=15)
            response.raise_for_status()
            bills_data = response.json().get('dados', [])
        except Exception as e:
            print(f"Erro ao buscar pautas na URL: {e}")
            continue

        salvos_nesta_categoria = 0 
        print(f"Procurando por {busca['tipo']}...")

        for bill in bills_data:
            if salvos_nesta_categoria >= busca["alvo"]:
                break 

            bill_id = bill.get('id')
            sigla_tipo = bill.get('siglaTipo')
            numero = bill.get('numero')
            ano = bill.get('ano')
            
            author_name = "Autor Desconhecido"
            author_photo_url = "" 
            author_party = ""       
            status = "Em análise"   
            url_pdf = "" 
            
            try:
                detail_url = f"{CHAMBER_API_URL}/proposicoes/{bill_id}"
                detail_res = requests.get(detail_url, timeout=10)
                if detail_res.status_code == 200:
                    dados_detalhe = detail_res.json().get('dados', {})
                    status_data = dados_detalhe.get('statusProposicao', {})
                    status = status_data.get('descricaoTramitacao', 'Em tramitação')
                    regime = str(status_data.get('regime', ''))
                    url_pdf = dados_detalhe.get('urlInteiroTeor', '')

                    # REGRA DOS PLs: DESLIGADA PARA TESTE (Vai pegar qualquer PL)
                    # if sigla_tipo == 'PL' and 'Urgência' not in regime:
                    #     continue 
            except Exception:
                continue

            try:
                author_url = f"{CHAMBER_API_URL}/proposicoes/{bill_id}/autores"
                author_res = requests.get(author_url, timeout=10)
                if author_res.status_code == 200:
                    authors = author_res.json().get('dados', [])
                    if authors:
                        authors_sorted = sorted(authors, key=lambda x: x.get('ordemAssinatura', 999))
                        main_author = authors_sorted[0]
                        raw_name = main_author.get('nome', '')
                        author_uri = main_author.get('uri', '')
                        
                        # A LÓGICA DE FOTOS QUE EU TINHA APAGADO SEM QUERER VOLTOU AQUI!
                        if raw_name == 'Poder Executivo':
                            author_name = 'Presidência da República'
                            author_party = 'Governo Federal'
                            author_photo_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Luiz_In%C3%A1cio_Lula_da_Silva_%282023%29.jpg/600px-Luiz_In%C3%A1cio_Lula_da_Silva_%282023%29.jpg'
                        elif raw_name.startswith('Senado Federal'):
                            clean_name = raw_name.replace('Senado Federal -', '').replace('Senado Federal', '').replace('Senador', '').strip()
                            author_name = f"Senador {clean_name}"
                            author_party = "Senado"
                            for sen_name, sen_data in senators_map.items():
                                if clean_name.upper() in sen_name or sen_name in clean_name.upper():
                                    author_photo_url = sen_data["foto"]
                                    author_party = sen_data["partido"]
                                    break
                        else:
                            author_name = raw_name
                            if "deputados/" in author_uri:
                                author_id = author_uri.split("/")[-1]
                                author_photo_url = f"https://www.camara.leg.br/internet/deputado/bandep/{author_id}.jpg"
                                try:
                                    dep_res = requests.get(author_uri, timeout=5)
                                    if dep_res.status_code == 200:
                                        author_party = dep_res.json().get('dados', {}).get('ultimoStatus', {}).get('siglaPartido', '')
                                except:
                                    pass
            except Exception:
                pass 

            cursor.execute('''
                INSERT INTO bills (id, type_acronym, number, year, summary, author_name, author_photo_url, author_party, status, url_inteiro_teor)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    author_name = excluded.author_name,
                    author_photo_url = excluded.author_photo_url,
                    author_party = excluded.author_party,
                    status = excluded.status,
                    url_inteiro_teor = excluded.url_inteiro_teor
            ''', (bill_id, sigla_tipo, numero, ano, bill.get('ementa'), author_name, author_photo_url, author_party, status, url_pdf))
            
            if sigla_tipo == 'PL':
                print(f"  -> [BINGO!] PL encontrado e salvo: PL {numero}/{ano}")
            else:
                print(f"  -> PEC encontrada e salva: PEC {numero}/{ano}")

            salvos_nesta_categoria += 1

    conn.commit()
    conn.close()
    print("Pautas salvas com sucesso!")

def translate_bills_with_ai():
    print("Iniciando a Redação Jornalística com IA...")
    conn = get_db_connection()
    cursor = conn.cursor()

    bills_to_translate = cursor.execute('''
        SELECT id, summary, url_inteiro_teor, number, year FROM bills 
        WHERE ai_summary IS NULL OR ai_summary = ''
        ORDER BY year DESC, number DESC
    ''').fetchall()

    if not bills_to_translate:
        print("Todas as pautas já possuem matérias escritas.")
        conn.close()
        return

    client = genai.Client(api_key=GEMINI_API_KEY)

    for bill in bills_to_translate:
        bill_id = bill['id']
        official_summary = bill['summary']
        pdf_url = bill['url_inteiro_teor']
        pec_number = bill['number']
        pec_year = bill['year']
        
        full_text = ""
        if pdf_url:
            print(f"  -> Baixando Inteiro Teor para a redação: {pdf_url}")
            full_text = extract_text_from_pdf(pdf_url)
            
        if not full_text.strip():
            full_text = official_summary
        
        prompt = f"""
        Aja como um jornalista político sênior e analista legislativo de um grande portal de notícias brasileiro.
        Abaixo está o TEXTO INTEGRAL (incluindo a 'Justificação' do autor) de uma nova Proposta de Emenda à Constituição (PEC) ou Projeto de Lei (PL).
        
        Sua tarefa é ler esse documento original e escrever uma matéria jornalística profunda, verdadeira e com foco no interesse público.
        É estritamente proibido inventar regras. Baseie-se apenas no texto fornecido.
        
        ESTRUTURA OBRIGATÓRIA DA MATÉRIA EM HTML (Use a tag <h2> para estes 4 subtítulos abaixo):
        <h2>O que a proposta quer mudar</h2>
        (Explique de forma clara e objetiva o que a lei propõe).
        
        <h2>Como a lei é hoje e o que muda na prática</h2>
        (Contraste a regra atual com a nova regra proposta).
        
        <h2>Análise Editorial: O Lado do Cidadão</h2>
        (Faça uma análise jornalística crítica. Avalie a justificativa do deputado/senador e pondere se a medida realmente traz benefícios diretos e práticos para a população, ou se atende apenas a interesses corporativos/governamentais).
        
        <h2>Impacto real para a População</h2>
        (Explique de forma direta como isso afeta a vida, o bolso, os direitos do cidadão comum e os cofres do Estado).

        Sua tarefa é gerar um JSON VÁLIDO contendo:
        1. "titulo": Manchete forte e otimizada para SEO (máx 80 caracteres).
        2. "resumo": Resumo curto (máx 350 caracteres).
        3. "artigo_html": A matéria completa com a estrutura exigida acima, usando APENAS tags (<h2>, <p>, <ul>, <li>, <strong>). NUNCA use aspas duplas no HTML, use aspas simples.
        
        RETORNE APENAS O JSON VÁLIDO:
        {{
            "titulo": "...",
            "resumo": "...",
            "artigo_html": "..."
        }}
        
        TEXTO INTEGRAL DA LEI E JUSTIFICAÇÃO: 
        {full_text}
        """
        
        for attempt in range(3):
            try:
                print(f"\nEscrevendo matéria completa para a Pauta ID {bill_id} / {pec_number}/{pec_year}...")
                response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                ai_text = response.text.strip()
                
                match = re.search(r'\{.*\}', ai_text, re.DOTALL)
                if match:
                    json_str = match.group(0)
                else:
                    json_str = ai_text 
                    
                data = json.loads(json_str)
                ai_title = data.get("titulo", "Título indisponível")
                ai_summary = data.get("resumo", "Resumo indisponível")
                ai_article_html = data.get("artigo_html", "<p>Matéria em apuração pela nossa redação...</p>")
                    
                cursor.execute('UPDATE bills SET ai_title = ?, ai_summary = ?, ai_article_html = ? WHERE id = ?', 
                              (ai_title, ai_summary, ai_article_html, bill_id))
                conn.commit()
                print("  -> Matéria escrita com sucesso e pronta para SEO!")
                time.sleep(4) 
                break 
                
            except json.JSONDecodeError:
                print(f"  -> Erro de formatação JSON na tentativa {attempt + 1}. Tentando de novo...")
                time.sleep(2)
                continue
            except Exception as e:
                break
    conn.close()

if __name__ == '__main__':
    fetch_recent_bills()
    translate_bills_with_ai()
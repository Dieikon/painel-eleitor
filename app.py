from flask import Flask, render_template, request, jsonify
from database import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Abre a gaveta do banco de dados
    conn = get_db_connection()
    
    # 2. Puxa todas as pautas organizadas pelas mais recentes
    bills_db = conn.execute('SELECT * FROM bills ORDER BY year DESC, number DESC').fetchall()
    conn.close()

    # 3. Converte os dados do SQLite para Dicionários (para o JavaScript conseguir ler como JSON)
    bills_list = [dict(bill) for bill in bills_db]

    # 4. Entrega a página HTML passando a lista de pautas ('bills') junto!
    return render_template('index.html', bills=bills_list)

def get_bills():
    """
    Internal API endpoint for Infinite Scroll and Search.
    Returns JSON data in blocks of 13 bills.
    """
    # Get parameters from the frontend URL (e.g., ?q=imposto&page=2)
    search_query = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 13
    offset = (page - 1) * per_page

    conn = get_db_connection()
    
    if search_query:
        # Search in the summary OR search by PEC number
        sql = '''
            SELECT * FROM bills 
            WHERE summary LIKE ? OR number LIKE ? 
            ORDER BY year DESC, number DESC 
            LIMIT ? OFFSET ?
        '''
        search_term = f"%{search_query}%"
        bills = conn.execute(sql, (search_term, search_term, per_page, offset)).fetchall()
    else:
        # Default load if no search query is present
        sql = '''
            SELECT * FROM bills 
            ORDER BY year DESC, number DESC 
            LIMIT ? OFFSET ?
        '''
        bills = conn.execute(sql, (per_page, offset)).fetchall()
        
    conn.close()

    # Convert SQLite rows to a list of Python dictionaries
    bills_list = [dict(b) for b in bills]
    
    return jsonify(bills_list)


@app.route('/pauta/<int:bill_id>')
def bill_detail(bill_id):
    """
    Route to display the full details of a specific bill.
    Fetches data by ID from the local database.
    """
    conn = get_db_connection()
    bill = conn.execute('SELECT * FROM bills WHERE id = ?', (bill_id,)).fetchone()
    conn.close()

    # If someone types a wrong ID in the URL, show an error instead of crashing
    if bill is None:
        return "Pauta não encontrada na nossa base de dados.", 404

    return render_template('bill_detail.html', bill=bill)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    bill_id = data.get('bill_id')

    if not name or not phone or not bill_id:
        return jsonify({"success": False, "message": "Dados incompletos"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO leads (name, phone, bill_id) VALUES (?, ?, ?)',
            (name, phone, bill_id)
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Inscrição realizada com sucesso!"}), 201
    except Exception as e:
        print(f"Erro no banco: {e}") # Isso ajuda a ver o erro no terminal
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/admin/leads')
def view_leads():
    # Aqui você pode adicionar uma lógica de senha simples depois
    conn = get_db_connection()
    # Fazemos um JOIN para mostrar o nome da PEC junto com o contato
    leads = conn.execute('''
        SELECT l.*, b.type_acronym, b.number, b.year 
        FROM leads l
        JOIN bills b ON l.bill_id = b.id
        ORDER BY l.created_at DESC
    ''').fetchall()
    conn.close()
    return render_template('admin_leads.html', leads=leads)

if __name__ == '__main__':
    app.run(debug=True)
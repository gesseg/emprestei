import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Define o caminho absoluto para o banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), 'estoque.db')

# Conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabela de itens (executar uma vez)
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            item TEXT NOT NULL,  # Campo para múltiplos itens de empréstimo
            quantidade INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    

# Rota para listar os itens
@app.route('/')
def index():
    conn = get_db_connection()
    itens = conn.execute('SELECT * FROM itens').fetchall()
    conn.close()
    return render_template('index.html', itens=itens)

# Rota para adicionar um item
@app.route('/add', methods=('GET', 'POST'))
def add_item():
    if request.method == 'POST':
        nome = request.form['nome']
        itens_selecionados = request.form.getlist('item')  # Recebe os itens como lista
        item = ', '.join(itens_selecionados)  # Converte a lista para uma string separada por vírgulas
        quantidade = request.form['quantidade']

        conn = get_db_connection()
        conn.execute('INSERT INTO itens (nome, item, quantidade) VALUES (?, ?, ?)',
                     (nome, item, quantidade))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_item.html')

# Rota para editar um item
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM itens WHERE id = ?', (id,)).fetchone()

    if item is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form['nome']
        itens_selecionados = request.form.getlist('item')
        item_str = ', '.join(itens_selecionados)  # Converte a lista para uma string separada por vírgulas
        quantidade = request.form['quantidade']

        conn.execute('UPDATE itens SET nome = ?, item = ?, quantidade = ? WHERE id = ?',
                     (nome, item_str, quantidade, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_item.html', item=item)

# Rota para deletar um item
@app.route('/delete/<int:id>', methods=('POST',))
def delete_item(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM itens WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()  # Cria a tabela no início, se não existir
    app.run(debug=True)


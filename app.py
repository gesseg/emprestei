from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabela de itens (executar uma vez)
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
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
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        conn = get_db_connection()
        conn.execute('INSERT INTO itens (nome, quantidade, preco) VALUES (?, ?, ?)',
                     (nome, quantidade, preco))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_item.html')

# Rota para editar um item
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM itens WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        conn.execute('UPDATE itens SET nome = ?, quantidade = ?, preco = ? WHERE id = ?',
                     (nome, quantidade, preco, id))
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
    create_table()
    app.run(debug=True)
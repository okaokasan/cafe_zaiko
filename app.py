from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('cafe_management.db')  # 使用するデータベース名を指定
    conn.row_factory = sqlite3.Row
    return conn

# データベース初期化関数
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.close()

# 初期化を実行
init_db()

# ホームページルート
@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM inventory').fetchall()
    conn.close()
    return render_template('index.html', items=items)

# アイテム追加ルート
@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    quantity = request.form['quantity']

    if item_name and quantity.isdigit():
        conn = get_db_connection()
        conn.execute('INSERT INTO inventory (item_name, quantity) VALUES (?, ?)', (item_name, int(quantity)))
        conn.commit()
        conn.close()

    return redirect('/')

# アイテム削除ルート
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
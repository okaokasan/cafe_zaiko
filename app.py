from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 商品モデル
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# 商品一覧ページ
@app.route('/')
def index():
    items = Product.query.all()
    return render_template('index.html', items=items)

# 商品追加ページ
@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    new_product = Product(name=name, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('index'))

# 商品編集ページ
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = int(request.form['quantity'])
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_product.html', product=product)

# 数量変更ページ
@app.route('/quantity_change/<int:product_id>', methods=['GET', 'POST'])
def change_quantity(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.quantity = int(request.form['quantity'])
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('change_quantity.html', product=product)

# 商品削除
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

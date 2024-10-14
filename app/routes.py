from flask import Flask, request, jsonify, render_template
from app.models import db, Product
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/product/add', methods=['POST'])
def add_product():
    data = request.form
    picture = request.files.get('picture')

    if picture:
        filename = secure_filename(picture.filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        picture_url = os.path.join('static/uploads', filename)
    else:
        picture_url = None

    new_product = Product(
        name=data['name'],
        price=data['price'],
        classification=data['classification'],
        picture=picture_url
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully', 'product': data})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'classification': product.classification,
            'picture': product.picture
        }
        product_list.append(product_data)
    return jsonify(product_list)


@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'classification': product.classification,
        'picture': product.picture
    })


@app.route('/product/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.form
    product = Product.query.get_or_404(product_id)

    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'classification' in data:
        product.classification = data['classification']

    picture = request.files.get('picture')
    if picture:
        filename = secure_filename(picture.filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product.picture = os.path.join('static/uploads', filename)

    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})


@app.route('/product/delete/<int:product_id>', methods=['DELETE'])
def del_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

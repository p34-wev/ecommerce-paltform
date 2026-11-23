from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def get_db_connection():
    if DATABASE_URL and POSTGRES_AVAILABLE:
        # PostgreSQL for production
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    else:
        # SQLite for local development
        conn = sqlite3.connect('ecommerce.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    if DATABASE_URL and POSTGRES_AVAILABLE:
        # PostgreSQL syntax
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                category TEXT,
                stock INTEGER DEFAULT 0,
                rating REAL DEFAULT 0,
                reviews_count INTEGER DEFAULT 0,
                original_price REAL,
                discount INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                product_id INTEGER,
                user_name TEXT,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
    else:
        # SQLite syntax
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                category TEXT,
                stock INTEGER DEFAULT 0,
                rating REAL DEFAULT 0,
                reviews_count INTEGER DEFAULT 0,
                original_price REAL,
                discount INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                user_name TEXT,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

    conn.commit()
    conn.close()

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL and POSTGRES_AVAILABLE:
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
    else:
        products = conn.execute('SELECT * FROM products').fetchall()
    
    conn.close()
    
    result = []
    for product in products:
        result.append({
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'image_url': product['image_url'],
            'category': product['category'],
            'stock': product['stock'],
            'rating': product['rating'],
            'reviews_count': product['reviews_count'],
            'original_price': product['original_price'],
            'discount': product['discount']
        })
    
    return jsonify(result)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL and POSTGRES_AVAILABLE:
        cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        product = cursor.fetchone()
    else:
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    conn.close()
    
    if product:
        return jsonify({
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'image_url': product['image_url'],
            'category': product['category'],
            'stock': product['stock'],
            'rating': product['rating'],
            'reviews_count': product['reviews_count'],
            'original_price': product['original_price'],
            'discount': product['discount']
        })
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Name and price are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL and POSTGRES_AVAILABLE:
        # PostgreSQL
        cursor.execute('''
            INSERT INTO products (name, description, price, image_url, category, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['name'],
            data.get('description', ''),
            data['price'],
            data.get('image_url', ''),
            data.get('category', ''),
            data.get('stock', 0)
        ))
        product_id = cursor.fetchone()['id']
    else:
        # SQLite
        cursor.execute('''
            INSERT INTO products (name, description, price, image_url, category, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data.get('description', ''),
            data['price'],
            data.get('image_url', ''),
            data.get('category', ''),
            data.get('stock', 0)
        ))
        product_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': product_id, 'message': 'Product created successfully'}), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL and POSTGRES_AVAILABLE:
        cursor.execute('''
            UPDATE products
            SET name = %s, description = %s, price = %s, image_url = %s, category = %s, stock = %s
            WHERE id = %s
        ''', (
            data.get('name'),
            data.get('description'),
            data.get('price'),
            data.get('image_url'),
            data.get('category'),
            data.get('stock'),
            product_id
        ))
    else:
        cursor.execute('''
            UPDATE products
            SET name = ?, description = ?, price = ?, image_url = ?, category = ?, stock = ?
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('description'),
            data.get('price'),
            data.get('image_url'),
            data.get('category'),
            data.get('stock'),
            product_id
        ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Product updated successfully'})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL and POSTGRES_AVAILABLE:
        cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
    else:
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Product deleted successfully'})

@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL and POSTGRES_AVAILABLE:
        cursor.execute('SELECT * FROM reviews WHERE product_id = %s ORDER BY created_at DESC', (product_id,))
        reviews = cursor.fetchall()
    else:
        reviews = conn.execute('SELECT * FROM reviews WHERE product_id = ? ORDER BY created_at DESC', (product_id,)).fetchall()
    
    conn.close()
    
    result = []
    for review in reviews:
        result.append({
            'id': review['id'],
            'product_id': review['product_id'],
            'user_name': review['user_name'],
            'rating': review['rating'],
            'comment': review['comment'],
            'created_at': review['created_at']
        })
    
    return jsonify(result)

@app.route('/api/products/<int:product_id>/reviews', methods=['POST'])
def add_review(product_id):
    data = request.get_json()
    
    if not data or 'rating' not in data or 'user_name' not in data:
        return jsonify({'error': 'Rating and user name are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL and POSTGRES_AVAILABLE:
        cursor.execute('''
            INSERT INTO reviews (product_id, user_name, rating, comment)
            VALUES (%s, %s, %s, %s)
        ''', (
            product_id,
            data['user_name'],
            data['rating'],
            data.get('comment', '')
        ))

        # Update product rating
        cursor.execute('''
            UPDATE products
            SET rating = (
                SELECT AVG(rating) FROM reviews WHERE product_id = %s
            ),
            reviews_count = (
                SELECT COUNT(*) FROM reviews WHERE product_id = %s
            )
            WHERE id = %s
        ''', (product_id, product_id, product_id))
    else:
        cursor.execute('''
            INSERT INTO reviews (product_id, user_name, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (
            product_id,
            data['user_name'],
            data['rating'],
            data.get('comment', '')
        ))

        # Update product rating
        cursor.execute('''
            UPDATE products
            SET rating = (
                SELECT AVG(rating) FROM reviews WHERE product_id = ?
            ),
            reviews_count = (
                SELECT COUNT(*) FROM reviews WHERE product_id = ?
            )
            WHERE id = ?
        ''', (product_id, product_id, product_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Review added successfully'}), 201

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

import sqlite3

DATABASE = 'ecommerce.db'

def seed_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
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
    
    # Clear existing data
    cursor.execute('DELETE FROM products')
    cursor.execute('DELETE FROM reviews')
    
    # Sample products
    products = [
        {
            'name': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
            'price': 79.99,
            'original_price': 129.99,
            'discount': 38,
            'rating': 4.5,
            'reviews_count': 2341,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            'category': 'Electronics',
            'stock': 50
        },
        {
            'name': 'Smart Watch Series 5',
            'description': 'Advanced smartwatch with health tracking, GPS, and water resistance.',
            'price': 299.99,
            'original_price': 399.99,
            'discount': 25,
            'rating': 4.3,
            'reviews_count': 1892,
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
            'category': 'Electronics',
            'stock': 30
        },
        {
            'name': 'Classic Cotton T-Shirt',
            'description': 'Comfortable 100% cotton t-shirt available in multiple colors.',
            'price': 24.99,
            'original_price': 34.99,
            'discount': 29,
            'rating': 4.1,
            'reviews_count': 5678,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
            'category': 'Clothing',
            'stock': 100
        },
        {
            'name': 'Denim Jacket',
            'description': 'Stylish denim jacket with modern fit and premium quality.',
            'price': 89.99,
            'original_price': 149.99,
            'discount': 40,
            'rating': 4.6,
            'reviews_count': 1234,
            'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400',
            'category': 'Clothing',
            'stock': 25
        },
        {
            'name': 'Python Programming Book',
            'description': 'Comprehensive guide to Python programming for beginners and advanced users.',
            'price': 49.99,
            'original_price': 79.99,
            'discount': 37,
            'rating': 4.8,
            'reviews_count': 3456,
            'image_url': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400',
            'category': 'Books',
            'stock': 40
        },
        {
            'name': 'Modern Home Decor Set',
            'description': 'Elegant home decor set including vases, candles, and decorative items.',
            'price': 59.99,
            'original_price': 89.99,
            'discount': 33,
            'rating': 4.2,
            'reviews_count': 890,
            'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400',
            'category': 'Home',
            'stock': 15
        },
        {
            'name': 'Laptop Stand',
            'description': 'Ergonomic aluminum laptop stand for better posture and cooling.',
            'price': 39.99,
            'original_price': 59.99,
            'discount': 33,
            'rating': 4.4,
            'reviews_count': 2100,
            'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400',
            'category': 'Electronics',
            'stock': 60
        },
        {
            'name': 'Running Shoes',
            'description': 'Lightweight running shoes with advanced cushioning technology.',
            'price': 119.99,
            'original_price': 179.99,
            'discount': 33,
            'rating': 4.7,
            'reviews_count': 4567,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
            'category': 'Clothing',
            'stock': 35
        }
    ]
    
    # Insert products
    for product in products:
        cursor.execute('''
            INSERT INTO products (name, description, price, image_url, category, stock, rating, reviews_count, original_price, discount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['name'],
            product['description'],
            product['price'],
            product['image_url'],
            product['category'],
            product['stock'],
            product['rating'],
            product['reviews_count'],
            product['original_price'],
            product['discount']
        ))
    
    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(products)} products into the database!")

if __name__ == '__main__':
    seed_database()

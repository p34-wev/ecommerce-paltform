# Fashionkart - E-Commerce Platform

A full-stack e-commerce platform with product catalog management, built with Python (Flask) backend and HTML/CSS/JavaScript frontend.

## 🌐 Live Deployment

**View the live application:** https://playful-pie-376855.netlify.app

## Features

- Product catalog with grid view
- Add new products
- Edit existing products
- Delete products
- Filter products by category
- Search products by name or description
- Responsive design
- SQLite database for data persistence

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful API with CORS support
- **Hosting**: Netlify (Static Frontend)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. The database will be automatically created when you run the application for the first time.

## Running the Application

1. Start the Flask backend server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

2. Open `index.html` in your web browser
   - You can simply double-click the `index.html` file
   - Or use a local server like Live Server in VS Code

## API Endpoints

- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get a specific product
- `POST /api/products` - Create a new product
- `PUT /api/products/<id>` - Update a product
- `DELETE /api/products/<id>` - Delete a product

## Database Schema

The `products` table includes:
- `id` (integer, primary key, auto-increment)
- `name` (text, required)
- `description` (text)
- `price` (real, required)
- `image_url` (text)
- `category` (text)
- `stock` (integer, default 0)

## Usage

1. The home page displays all products in a grid layout
2. Click "Add Product" to add a new product
3. Use the filter dropdown to filter by category
4. Use the search box to search products
5. Click "Edit" on a product card to modify it
6. Click "Delete" to remove a product

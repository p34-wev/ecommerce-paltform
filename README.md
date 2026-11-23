# 🛍️ Fashionkart - E-Commerce Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.0+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

**A modern, full-stack e-commerce platform with seamless product management**

[🌐 View Live Demo](https://playful-pie-376855.netlify.app) • [📦 Installation](#-installation) • [🚀 Quick Start](#-quick-start) • [📖 API Docs](#-api-endpoints)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🛒 **Product Catalog** | Beautiful grid view with product cards |
| ➕ **Add Products** | Easy product creation with form validation |
| ✏️ **Edit Products** | Update product details in real-time |
| 🗑️ **Delete Products** | Remove products with confirmation |
| 🔍 **Search** | Find products by name or description |
| 🏷️ **Filter by Category** | Filter products by Electronics, Clothing, Books, etc. |
| 📱 **Responsive Design** | Works seamlessly on desktop, tablet, and mobile |
| 💾 **SQLite Database** | Lightweight, serverless data persistence |
| ⭐ **Reviews System** | Product ratings and customer reviews |
| 💰 **Discount Display** | Show original price and discount percentage |

---

## 🛠️ Tech Stack

<div align="center">

### Backend
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-lightgrey?style=flat-square&logo=sqlite)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript)

### Hosting
![Netlify](https://img.shields.io/badge/Netlify-00C7B7?style=flat-square&logo=netlify)

</div>

---

## 📸 Screenshots

### 🏠 Home Page
> Product catalog with grid layout and search functionality

### ➕ Add Product
> Form to add new products with image URL support

### 🏷️ Category Filter
> Filter products by different categories

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/p34-wev/ecommerce-paltform.git
cd ecommerce-paltform

# Install dependencies
pip install -r requirements.txt

# Seed the database with sample products
python seed.py
```

### Running the Application

```bash
# Start the Flask server
python app.py
```

The application will be available at `http://localhost:5000`

---

## 📖 API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products` | Get all products |
| `GET` | `/api/products/<id>` | Get a specific product by ID |
| `POST` | `/api/products` | Create a new product |
| `PUT` | `/api/products/<id>` | Update a product |
| `DELETE` | `/api/products/<id>` | Delete a product |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/<id>/reviews` | Get all reviews for a product |
| `POST` | `/api/products/<id>/reviews` | Add a review to a product |

### Example Request

```bash
# Get all products
curl http://localhost:5000/api/products

# Create a new product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "description": "High-quality wireless headphones",
    "price": 79.99,
    "category": "Electronics",
    "stock": 50
  }'
```

---

## 🗄️ Database Schema

### Products Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `name` | TEXT | Product name (required) |
| `description` | TEXT | Product description |
| `price` | REAL | Product price (required) |
| `image_url` | TEXT | URL to product image |
| `category` | TEXT | Product category |
| `stock` | INTEGER | Available stock (default: 0) |
| `rating` | REAL | Average rating (default: 0) |
| `reviews_count` | INTEGER | Number of reviews (default: 0) |
| `original_price` | REAL | Original price before discount |
| `discount` | INTEGER | Discount percentage |

### Reviews Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `product_id` | INTEGER | Foreign key to products |
| `user_name` | TEXT | Name of the reviewer |
| `rating` | INTEGER | Rating (1-5) |
| `comment` | TEXT | Review comment |
| `created_at` | TIMESTAMP | Review creation time |

---

## 🎯 Usage Guide

### 1️⃣ View Products
- Home page displays all products in a responsive grid
- Each product card shows image, name, price, rating, and discount

### 2️⃣ Add New Product
- Click the "Add Product" button
- Fill in the product details
- Submit to add to the catalog

### 3️⃣ Search Products
- Use the search bar to find products by name or description
- Results update in real-time

### 4️⃣ Filter by Category
- Select a category from the dropdown
- View only products in that category

### 5️⃣ Edit Product
- Click "Edit" on any product card
- Modify the details
- Save changes

### 6️⃣ Delete Product
- Click "Delete" on any product card
- Confirm deletion
- Product is removed from the database

---

## 🌐 Live Deployment

**View the live application:** https://playful-pie-376855.netlify.app

> The live deployment is hosted on Netlify for the frontend. For full functionality with backend API, run locally using the instructions above.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**p34-wev**

- GitHub: [@p34-wev](https://github.com/p34-wev)

---

<div align="center">

**⭐ If you like this project, please give it a star!**

Made with ❤️ using Python Flask

</div>

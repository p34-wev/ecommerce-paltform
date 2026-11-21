const API_URL = 'http://localhost:5000/api/products';

let products = [];
let filteredProducts = [];
let cart = [];
let wishlist = [];
let currentProduct = null;

// DOM Elements
const productGrid = document.getElementById('productGrid');
const dealsGrid = document.getElementById('dealsGrid');
const searchInput = document.getElementById('searchInput');
const cartSidebar = document.getElementById('cartSidebar');
const wishlistSidebar = document.getElementById('wishlistSidebar');
const productModal = document.getElementById('productModal');
const loginModal = document.getElementById('loginModal');
const overlay = document.getElementById('overlay');
const cartCount = document.getElementById('cartCount');
const wishlistCount = document.getElementById('wishlistCount');
const cartItems = document.getElementById('cartItems');
const wishlistItems = document.getElementById('wishlistItems');
const cartTotal = document.getElementById('cartTotal');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
    loadCart();
    loadWishlist();
    startTimer();
    setupCategoryFilters();
});

// Fetch Products
async function fetchProducts() {
    try {
        const response = await fetch(API_URL);
        products = await response.json();
        filteredProducts = [...products];
        renderProducts();
        renderDeals();
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Render Products
function renderProducts() {
    if (filteredProducts.length === 0) {
        productGrid.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-box-open"></i>
                <p>No products found</p>
            </div>
        `;
        return;
    }

    productGrid.innerHTML = filteredProducts.map(product => createProductCard(product)).join('');
}

function createProductCard(product) {
    const isInWishlist = wishlist.some(item => item.id === product.id);
    const discountBadge = product.discount ? `<span class="discount-badge">${product.discount}% off</span>` : '';
    const originalPrice = product.original_price ? `<span class="original-price">$${product.original_price.toFixed(2)}</span>` : '';
    const ratingBadge = product.rating ? `
        <div class="product-rating">
            <span class="rating-badge">${product.rating.toFixed(1)}</span>
            <i class="fas fa-star" style="color: #388e3c; font-size: 12px;"></i>
            <span class="rating-count">(${product.reviews_count || 0})</span>
        </div>
    ` : '';

    return `
        <div class="product-card" onclick="openProductModal(${product.id})">
            <img src="${product.image_url || 'https://via.placeholder.com/200'}" alt="${product.name}" class="product-image" onerror="this.src='https://via.placeholder.com/200'">
            <div class="product-info">
                <h3 class="product-title">${product.name}</h3>
                ${ratingBadge}
                <div class="product-price">
                    <span class="current-price">$${product.price.toFixed(2)}</span>
                    ${originalPrice}
                    ${discountBadge}
                </div>
                <div class="product-actions">
                    <button class="btn-add-cart-small" onclick="event.stopPropagation(); addToCart(${product.id})">
                        <i class="fas fa-shopping-cart"></i> Add
                    </button>
                    <button class="btn-wishlist-small ${isInWishlist ? 'active' : ''}" onclick="event.stopPropagation(); toggleWishlistItem(${product.id})">
                        <i class="fas fa-heart"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Render Deals
function renderDeals() {
    const deals = products.filter(p => p.discount && p.discount > 30).slice(0, 5);
    dealsGrid.innerHTML = deals.map(product => createProductCard(product)).join('');
}

// Category Filters
function setupCategoryFilters() {
    const categoryLinks = document.querySelectorAll('.category-link');
    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            categoryLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            const category = link.dataset.category;
            if (category) {
                filteredProducts = products.filter(p => p.category === category);
            } else {
                filteredProducts = [...products];
            }
            renderProducts();
        });
    });
}

// Search
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(searchTerm) ||
        (product.description && product.description.toLowerCase().includes(searchTerm))
    );
    renderProducts();
});

// Product Modal
async function openProductModal(productId) {
    try {
        const response = await fetch(`${API_URL}/${productId}`);
        currentProduct = await response.json();
        
        document.getElementById('modalImage').src = currentProduct.image_url || 'https://via.placeholder.com/400';
        document.getElementById('modalTitle').textContent = currentProduct.name;
        document.getElementById('modalRating').textContent = currentProduct.rating ? currentProduct.rating.toFixed(1) : '0';
        document.getElementById('modalReviews').textContent = `(${currentProduct.reviews_count || 0} reviews)`;
        document.getElementById('modalPrice').textContent = `$${currentProduct.price.toFixed(2)}`;
        document.getElementById('modalOriginalPrice').textContent = currentProduct.original_price ? `$${currentProduct.original_price.toFixed(2)}` : '';
        document.getElementById('modalDiscount').textContent = currentProduct.discount ? `${currentProduct.discount}% off` : '';
        
        const isInWishlist = wishlist.some(item => item.id === currentProduct.id);
        document.querySelector('.btn-wishlist').classList.toggle('active', isInWishlist);
        
        productModal.classList.remove('hidden');
        overlay.classList.remove('hidden');
        
        loadReviews(productId);
    } catch (error) {
        console.error('Error loading product:', error);
    }
}

function closeProductModal() {
    productModal.classList.add('hidden');
    overlay.classList.add('hidden');
    currentProduct = null;
}

// Cart Functions
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    
    saveCart();
    updateCartUI();
    showNotification('Added to cart!', 'success');
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartUI();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            saveCart();
            updateCartUI();
        }
    }
}

function toggleCart() {
    cartSidebar.classList.toggle('active');
    overlay.classList.toggle('hidden');
    wishlistSidebar.classList.remove('active');
}

function updateCartUI() {
    cartCount.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-shopping-cart"></i>
                <p>Your cart is empty</p>
            </div>
        `;
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <img src="${item.image_url || 'https://via.placeholder.com/80'}" alt="${item.name}" class="cart-item-image">
                <div class="cart-item-details">
                    <h4 class="cart-item-title">${item.name}</h4>
                    <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                    <div class="cart-item-quantity">
                        <button class="qty-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
                    </div>
                </div>
                <button onclick="removeFromCart(${item.id})" style="background:transparent; border:none; cursor:pointer; color:#ff6161;">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    cartTotal.textContent = `$${total.toFixed(2)}`;
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function loadCart() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartUI();
    }
}

function checkout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!', 'error');
        return;
    }
    showNotification('Proceeding to checkout...', 'success');
    // Add checkout logic here
}

// Wishlist Functions
function toggleWishlistItem(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const index = wishlist.findIndex(item => item.id === productId);
    if (index > -1) {
        wishlist.splice(index, 1);
        showNotification('Removed from wishlist', 'success');
    } else {
        wishlist.push(product);
        showNotification('Added to wishlist!', 'success');
    }
    
    saveWishlist();
    updateWishlistUI();
    renderProducts();
}

function toggleWishlist() {
    wishlistSidebar.classList.toggle('active');
    overlay.classList.toggle('hidden');
    cartSidebar.classList.remove('active');
}

function updateWishlistUI() {
    wishlistCount.textContent = wishlist.length;
    
    if (wishlist.length === 0) {
        wishlistItems.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-heart"></i>
                <p>Your wishlist is empty</p>
            </div>
        `;
    } else {
        wishlistItems.innerHTML = wishlist.map(item => `
            <div class="wishlist-item">
                <img src="${item.image_url || 'https://via.placeholder.com/80'}" alt="${item.name}" class="cart-item-image">
                <div class="cart-item-details">
                    <h4 class="cart-item-title">${item.name}</h4>
                    <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                </div>
                <div>
                    <button onclick="addToCart(${item.id}); toggleWishlistItem(${item.id});" style="background:#ff9f00; color:white; border:none; padding:8px 12px; cursor:pointer; border-radius:2px; margin-right:8px;">
                        <i class="fas fa-shopping-cart"></i>
                    </button>
                    <button onclick="toggleWishlistItem(${item.id})" style="background:transparent; border:none; cursor:pointer; color:#ff6161;">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
}

function saveWishlist() {
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
}

function loadWishlist() {
    const savedWishlist = localStorage.getItem('wishlist');
    if (savedWishlist) {
        wishlist = JSON.parse(savedWishlist);
        updateWishlistUI();
    }
}

function toggleWishlistFromModal() {
    if (currentProduct) {
        toggleWishlistItem(currentProduct.id);
        const isInWishlist = wishlist.some(item => item.id === currentProduct.id);
        document.querySelector('.btn-wishlist').classList.toggle('active', isInWishlist);
    }
}

function addToCartFromModal() {
    if (currentProduct) {
        addToCart(currentProduct.id);
    }
}

function buyNow() {
    if (currentProduct) {
        addToCart(currentProduct.id);
        closeProductModal();
        toggleCart();
    }
}

// Reviews
async function loadReviews(productId) {
    try {
        const response = await fetch(`${API_URL}/${productId}/reviews`);
        const reviews = await response.json();
        
        const reviewsList = document.getElementById('reviewsList');
        if (reviews.length === 0) {
            reviewsList.innerHTML = '<p style="color: #878787;">No reviews yet. Be the first to review!</p>';
        } else {
            reviewsList.innerHTML = reviews.map(review => `
                <div class="review-item">
                    <div class="review-header">
                        <span class="review-user">${review.user_name}</span>
                        <span class="review-date">${new Date(review.created_at).toLocaleDateString()}</span>
                    </div>
                    <div class="review-rating">
                        ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}
                    </div>
                    <p class="review-comment">${review.comment || 'No comment'}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

async function submitReview() {
    if (!currentProduct) return;
    
    const rating = document.getElementById('reviewRating').value;
    const userName = document.getElementById('reviewName').value;
    const comment = document.getElementById('reviewComment').value;
    
    if (!userName) {
        showNotification('Please enter your name', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${currentProduct.id}/reviews`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                rating: parseInt(rating),
                user_name: userName,
                comment: comment
            })
        });
        
        if (response.ok) {
            showNotification('Review submitted successfully!', 'success');
            document.getElementById('reviewName').value = '';
            document.getElementById('reviewComment').value = '';
            loadReviews(currentProduct.id);
            fetchProducts(); // Refresh to get updated rating
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        showNotification('Error submitting review', 'error');
    }
}

// Login Modal
function showLoginModal() {
    loginModal.classList.remove('hidden');
    overlay.classList.remove('hidden');
}

function closeLoginModal() {
    loginModal.classList.add('hidden');
    overlay.classList.add('hidden');
}

// Close All Modals
function closeAllModals() {
    productModal.classList.add('hidden');
    loginModal.classList.add('hidden');
    cartSidebar.classList.remove('active');
    wishlistSidebar.classList.remove('active');
    overlay.classList.add('hidden');
}

// Timer
function startTimer() {
    let hours = 12, minutes = 34, seconds = 56;
    
    setInterval(() => {
        seconds--;
        if (seconds < 0) {
            seconds = 59;
            minutes--;
            if (minutes < 0) {
                minutes = 59;
                hours--;
                if (hours < 0) {
                    hours = 23;
                }
            }
        }
        
        document.getElementById('hours').textContent = hours.toString().padStart(2, '0');
        document.getElementById('minutes').textContent = minutes.toString().padStart(2, '0');
        document.getElementById('seconds').textContent = seconds.toString().padStart(2, '0');
    }, 1000);
}

// Notification
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#388e3c' : '#ff6161'};
        color: white;
        border-radius: 4px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        font-weight: 500;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add keyframe animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(style);

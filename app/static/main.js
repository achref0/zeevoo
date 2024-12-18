document.addEventListener('DOMContentLoaded', () => {
    // Product modal
    const modal = document.getElementById('product-modal');
    const productCards = document.querySelectorAll('.product-card');
    const closeModal = document.querySelector('.close');

    productCards.forEach(card => {
        card.addEventListener('click', () => {
            const productId = card.dataset.productId;
            fetchProductDetails(productId).then(product => {
                populateModal(product);
                modal.style.display = 'block';
            });
        });
    });

    if (closeModal) {
        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();
            const productId = button.dataset.productId;
            addToCart(productId); // Send only productId
        });
    });

    // Flash message dismissal
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        message.addEventListener('click', () => {
            message.style.display = 'none';
        });
    });

    // Dashboard tabs
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;

            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
});

async function fetchProductDetails(productId) {
    const response = await fetch(`/api/product/${productId}`);
    return await response.json();
}

function populateModal(product) {
    const modalContent = document.querySelector('.modal-content');
    modalContent.innerHTML = `
        <span class="close">&times;</span>
        <h2>${product.name}</h2>
        <p class="product-price">$${product.price.toFixed(2)}</p>
        <div class="product-images">
            <img src="${product.image}" alt="${product.name}">
        </div>
        <p>${product.description}</p>
        <button class="add-to-cart" data-product-id="${product.id}">Add to Cart</button>
    `;
}

function addToCart(productId) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/api/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ productId: productId }), // Send only productId
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        showNotification('Item added to cart successfully!');
        updateCartIcon(data.cart_count);
    })
    .catch((error) => {
        console.error('Error:', error);
        showNotification('Error adding item to cart. Please try again.', 'error');
    });
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function updateCartIcon(count) {
    const cartIcon = document.querySelector('.cart-icon');
    if (cartIcon) {
        cartIcon.setAttribute('data-count', count);
    }
}

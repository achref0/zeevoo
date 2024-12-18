from app import create_app, db
from app.models import User, Product, Cart

app = create_app()

# Create the database and tables
with app.app_context():
    # Drop all tables first to avoid conflicts
    db.drop_all()
    
    # Create all tables
    db.create_all()
    
    # Create a sample admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        is_admin=True
    )
    admin.set_password('admin123')
    
    # Create a sample regular user
    user = User(
        username='user',
        email='user@example.com',
        is_admin=False
    )
    user.set_password('user123')
    
    # Add users to the session
    db.session.add(admin)
    db.session.add(user)
    
    # Create sample products
    products = [
        Product(
            name='Laptop',
            description='High-performance laptop with latest specifications',
            price=999.99,
            image='laptop.jpg',
            seller_id=1,
            is_approved=True,
            is_sold=False
        ),
        Product(
            name='Smartphone',
            description='Latest model smartphone with advanced features',
            price=699.99,
            image='smartphone.jpg',
            seller_id=1,
            is_approved=True,
            is_sold=False
        ),
        Product(
            name='Headphones',
            description='Wireless noise-canceling headphones',
            price=199.99,
            image='headphones.jpg',
            seller_id=2,
            is_approved=True,
            is_sold=False
        ),
        Product(
            name='Smartwatch',
            description='Fitness tracking smartwatch with heart rate monitor',
            price=299.99,
            image='smartwatch.jpg',
            seller_id=2,
            is_approved=True,
            is_sold=False
        )
    ]
    
    # Add products to the session
    for product in products:
        db.session.add(product)
    
    # Create empty carts for users
    admin_cart = Cart(user=admin)
    user_cart = Cart(user=user)
    db.session.add(admin_cart)
    db.session.add(user_cart)
    
    # Commit all changes
    db.session.commit()
    
    print("Database initialized successfully!")


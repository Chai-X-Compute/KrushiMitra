from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Test the database connection
        try:
            with db.engine.connect() as connection:
                print("\n✅ Database connection successful.\n")
        except Exception as e:
            print("\n" + "="*60)
            print("❌ AWS RDS DATABASE CONNECTION FAILED!")
            print(f"   Error: {e}")
            print("   Please check the following:")
            print("     1. The `DATABASE_URL` in your .env file is correct.")
            print("     2. The RDS instance is running and accessible.")
            print("     3. The security groups for your RDS instance allow connections from your IP.")
            print("="*60 + "\n")
        
        # Create tables
        db.create_all()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(200))
    language_preference = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resources = db.relationship('Resource', backref='owner', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Resource(db.Model):
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # tools, livestock, electronics, fertilizers, etc.
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    listing_type = db.Column(db.String(20), nullable=False)  # rent, borrow, sell
    condition = db.Column(db.String(20))  # new, good, fair, poor
    age_years = db.Column(db.Integer, default=0)
    quality = db.Column(db.Integer, default=5)  # 1-10 scale
    image_url = db.Column(db.String(500))
    location = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='resource', lazy=True)
    
    def __repr__(self):
        return f'<Resource {self.name}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # rent, borrow, buy
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    amount = db.Column(db.Float)
    rating = db.Column(db.Integer)  # 1-5 stars
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transaction {self.id}>'

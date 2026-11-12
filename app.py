from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite configuration – pizzeria.db file will be created automatically in the project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzeria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Models ---
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Topping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)


# --- Database Initialization & Initial Data ---
with app.app_context():
    db.create_all()
    if not Pizza.query.first():
        sample_pizzas = [
            Pizza(name="Margherita", description="Tomato sauce, mozzarella cheese, fresh basil", price=25.0),
            Pizza(name="Pepperoni", description="Tomato sauce, mozzarella cheese, spicy pepperoni salami", price=32.0),
            Pizza(name="Capricciosa", description="Tomato sauce, mozzarella cheese, mushrooms, ham", price=34.0),
            Pizza(name="Hawaiian", description="Tomato sauce, mozzarella cheese, ham, pineapple", price=30.0)
        ]
        sample_toppings = [
            Topping(name="Extra cheese", price=5.0),
            Topping(name="Garlic sauce", price=3.0),
            Topping(name="Jalapeno peppers", price=4.0),
            Topping(name="Mushrooms", price=4.0)
        ]
        db.session.add_all(sample_pizzas + sample_toppings)
        db.session.commit()


# --- Routes ---
@app.route('/')
def index():
    pizzas = Pizza.query.all()
    toppings = Topping.query.all()
    return render_template('index.html', pizzas=pizzas, toppings=toppings)

@app.route('/order', methods=['POST'])
def checkout():
    # Mock order handling for testing purposes
    return jsonify({"status": "success", "message": "Order placed successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
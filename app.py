from flask import Flask, render_template
from extensions import db
from routes.raw_ingredients import raw_ingredients_blueprint
from routes.in_house_ingredients import in_house_ingredients_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_cost.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(raw_ingredients_blueprint)
app.register_blueprint(in_house_ingredients_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

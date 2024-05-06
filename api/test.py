from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.name}-{self.description}'

  
drink = Drink(id=1, name ='grape',description = 'nice')
with app.app_context():
    db.session.add(drink)
    db.session.commit()
    
    
Drink.query.all()

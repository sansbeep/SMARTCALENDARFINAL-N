from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flaskwebgui import FlaskUI
import os

app = Flask(__name__)

# Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'calendar.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{'id': e.id, 'title': e.title, 'description': e.description, 'start': e.start} for e in events])

@app.route('/events', methods=['POST'])
def add_event():
    data = request.json
    new_event = Event(title=data['title'], description=data.get('description', ''), start=data['start'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'id': new_event.id})

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    # Launch as Desktop App
    FlaskUI(app=app, server="flask", width=1000, height=700).run()
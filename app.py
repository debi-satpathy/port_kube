from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        todo_data = {'id': todo.id, 'task': todo.task, 'done': todo.done}
        output.append(todo_data)
    return jsonify({'todos': output})

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    task = data.get('task', '')
    todo = Todo(task=task)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)

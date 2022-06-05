from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from sqlalchemy import false
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# ENV = 'prod'
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Sh268268@localhost/todoonline'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ursvjthysihsaa:e96740cfa41a8d19bec6ef774d4bc46d02dc29519d81b048e4a3c783ab806784@ec2-107-22-238-112.compute-1.amazonaws.com:5432/d4i36gndiupd5d'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Integer, default=0)
    utc_dt = datetime.now(timezone.utc)
    dt = utc_dt.astimezone()
    date_created = db.Column(db.DateTime, default=dt)
   
    def __repr__(self):      
        return '<Task %r>' % self.id
author = "Juliana 18281"

@app.route("/")
def index():   
    return render_template('index.html', author=author)

@app.route('/todo', methods=['POST', 'GET'])
def todo():
    if request.method == 'POST' :
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'     
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html', tasks=tasks, author=author)    
        
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task'
    else: 
        return render_template('update.html', task=task, author=author)

@app.route("/about")
def about():
    return render_template("about.html", author=author)

if __name__ == '__main__':
    app.run()
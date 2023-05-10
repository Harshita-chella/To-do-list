from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
with app.app_context():
    db=SQLAlchemy(app)

class To_do(db.Model):
    todo_no=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.todo_no} - {self.task}"
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        task=request.form['task']
        desc=request.form['desc']
        todo=To_do(task=task,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=To_do.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/products')
def products():
    allTodo=To_do.query.all()
    print(allTodo)
    return 'this is products page!'
@app.route('/update/<int:todo_no>',methods=['GET','POST'])
def update(todo_no):
    if request.method=='POST':
        task=request.form['task']
        desc=request.form['desc']
        todo=To_do.query.filter_by(todo_no=todo_no).first()
        todo.task= task
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=To_do.query.filter_by(todo_no=todo_no).first()
    return render_template('update.html',todo=todo)
@app.route('/delete/<int:todo_no>')
def delete(todo_no):
    todo=To_do.query.filter_by(todo_no=todo_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
if __name__=='__main__':
     app.run(debug=True,port=8000)
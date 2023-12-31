from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todist.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime,default= datetime.utcnow)
    def __repr__(self) -> str:
         return f"{self.sno}-{self.title}"




@app.route('/',methods=['GET',"POST"])
def hello_world():
        if request.method=="POST":
            title = request.form["title"]
            desc = request.form["desc"]
            todist = Todo(title=title,desc=desc)
            db.session.add(todist)
            db.session.commit()
        alltodo = Todo.query.all()
        return render_template('index.html',alltodo=alltodo)
@app.route('/About')
def About():
    return render_template("about.html")

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")
@app.route('/update/<int:sno>', methods=["POST",'GET'])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    alltodo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', alltodo=alltodo)

if __name__ == "__main__":
    app.run(debug=True,port=9000)
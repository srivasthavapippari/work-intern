from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from flask import render_template
from flask import redirect


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sri.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db=SQLAlchemy(app)


class Work(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.Text)
	date = db.Column(db.Text)

	def __init__(self, task,date):
		self.task = task
		self.date = date


db.create_all()


@app.route('/')
def tasks_list():
    values = Work.query.all()
    return render_template('wlist.html', values=values)

@app.route('/list', methods=['POST'])
def add_task():
    task = request.form['task']
    date = request.form['date']
    if not task:
        return 'Empty'
    fun = Work(task,date)
    db.session.add(fun)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Work.query.get(task_id)
    if not task:
        return redirect('/')
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

# This calls the flask object to run with address local host:50000
if __name__ == '__main__':
    app.run()



import os
from flask import Flask, render_template, request, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
app.config['SECRET_KEY'] = 'N\xee\xe9UQ\xc4\x945\xd6h\x868#i_X\x83\xe3dR'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DB_FILE
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# -------------- DB --------------- #

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Unicode)

# ----------- Initialize db ----------- #
if not os.path.exists(DB_FILE):
    db.create_all()
    db.session.add(Post(id=1, body='Blablabla'))
    db.session.add(Post(id=2, body='Post 2'))
    db.session.commit()

# -------------- Admin -------------- #
admin = Admin(app)
class MyModelView(ModelView):
    def is_accessible(self):
        return request.cookies.get('admin') == 'true'
admin.add_view(MyModelView(Post, db.session))

@app.route('/login-secret-url')
def login():
    resp = make_response('OK, you are logged in now')
    resp.set_cookie('admin', 'true')
    return resp

@app.route('/logout')
def logout():
    resp = make_response('OK, you are logged out')
    resp.set_cookie('admin', 'false')
    return resp

# -------------- Views ---------------- #
    
@app.route('/')
def index():
    return render_template('index.html', posts=Post.query.all())

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
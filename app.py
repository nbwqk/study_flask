from flask import Flask,make_response,json,jsonify,redirect,url_for,request,session,render_template,flash,abort
import click,os
from forms import LoginForm,NewNoteForm,EditNoteForm,DeleteNoteForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
app.secret_key='secret string'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
app.config.update(
    #MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_SERVER='smtp.163.com',
    MAIL_PORT='465',
    MAIL_USE_TLS=True,
    #MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_USERNAME='nbyzwqk@163.com',
    #MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_PASSWORD='CNEPQTZKJZBZPPZY',
    #MAIL_DEFAULT_SENDER=('Wqk',os.getenv('MAIL_USERNAME'))
    MAIL_DEFAULT_SENDER=('Wqk','nbyzwqk@163.com')
)
mail=Mail(app)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL','sqlite:///'+
    os.path.join(app.root_path,'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/hi')
@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

#@app.route('/greet',defaults={'name':'programmer'})
@app.route('/greet')
def say_hello():
    name=request.args.get('name')
    if name is None:
        name=request.cookies.get('name','Human')
        response='<h1>Hello,%s</h1>'%name
    #return '<h1>Hello,%s!</h1>' % name
    if 'logged_in' in session:
        response+='[Authenticated]'
    else:
        response+='[Not Authenticated]'
    return response

@app.cli.command()
def hello():
    '''Just say hello.'''
    click.echo('Hello,Human!')

@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!' % (2020-year)

@app.route('/foo')
def foo():
    data={
        'name':'wqk',
        'gender':'male'
    }
    response=make_response(json.dumps(data))
    response.mimetype='application/json'
    return response

@app.route('/j')
def f():
    return jsonify(name='zcy',age='25')

@app.route('/set/<name>')
def set_cookie(name):
    response=make_response(redirect(url_for('say_hello')))
    response.set_cookie('name',name)
    return response

@app.route('/login')
def login():
    session['logged_in']=True
    return redirect(url_for('say_hello'))

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('say_hello'))

@app.route('/fooo')
def fooo():
    return '<h1>Fooo page</h1><a href="%s">Do something</a>'% url_for('do_something')

@app.route('/bar')
def bar():
    return '<h1>Bar bage</h1><a href="%s">Do something</a>'% url_for('do_something')

@app.route('/do_something')
def do_something():
    return redirect(request.referrer or url_for('say_hello'))

@app.route('/watchlist')
def watchlist():
    user={'username':'wuqingke',
          'bio':'A boy who loves movies and music.',}
    movies=[
        {'name':'My Neighbor Totoro','year':'1988'},
        {'name':'Three Colours trilogy','year':'1993'},
        {'name':'Forrest Gump','year':'1994'},
        {'name':'Perfect Blue','year':'1997'},
    ]
    return render_template('watchlist.html', user=user, movies=movies)

from flask import Markup

@app.template_filter()  # 自定义过滤器
def musical(s):
    return s + Markup('&#9835;')

@app.template_global() # 自定义全局函数
def barr():
    return 'I am barr'

@app.template_test()  # 自定义测试器
def baz(n):
    if n=='baz':
        return True
    return False

@app.route('/index')
def index():
    a='wqk'
    notes=Note.query.all()
    form=DeleteNoteForm()
    return render_template('index.html',a=a,notes=notes,form=form)

@app.route('/flash')
def just_flash():
    flash('I am flash,who is looking for me?')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404

@app.route('/basic',methods=['GET','POST'])
def basic():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        flash('Welcome home,%s' % username)
        return redirect(url_for('index'))
    return render_template('basic.html',form=form)

@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database.')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Note=Note,Author=Author,Article=Article)

class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)

    def __repr__(self):
        return '<Note %r>' % self.body

class Author(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    phone=db.Column(db.String(20))
    articles=db.relationship('Article')

class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),index=True)
    body=db.Column(db.Text)
    author_id=db.Column(db.Integer,db.ForeignKey('author.id'))

@app.route('/new',methods=['GET','POST'])
def new_note():
    form=NewNoteForm()
    if form.validate_on_submit():
        body=form.body.data
        note=Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved.')
        return redirect(url_for('index'))
    return render_template('new_note.html',form=form)

@app.route('/edit/<int:note_id>',methods=['GET','POST'])
def edit_note(note_id):
    form=EditNoteForm()
    note=Note.query.get(note_id)
    if form.validate_on_submit():
       note.body=form.body.data
       db.session.commit()
       flash('Your note is updated.')
       return redirect(url_for('index'))
    form.body.data=note.body
    return render_template('edit_note.html',form=form)

@app.route('/delete/<int:note_id>',methods=['POST'])
def delete_note(note_id):
    form=DeleteNoteForm()
    if form.validate_on_submit():
        note=Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted.')
    else:
        abort(400)
    return redirect(url_for('index'))

association_table=db.Table('association',db.Column('student_id',db.Integer,
                           db.ForeignKey('student.id')),db.Column('teacher_id',
                           db.Integer,db.ForeignKey('teacher.id')))

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    grade=db.Column(db.String(20))
    teachers=db.relationship('Teacher',secondary=association_table,
                             back_populates='student')

class Teacher(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    office=db.Column(db.String(20))
    students=db.relationship('Student',secondary=association_table,
                             back_populates='teacher')

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),unique=True)
    body=db.Column(db.Text)
    comments=db.relationship('Comment',cascade='save-update,merge,delete',back_populates='post')

class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    post=db.relationship('Post',back_populates='comments')



@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Note=Note,Author=Author,Article=Article,Post=Post,Comment=Comment)

if __name__ == '__main__':
    app.run()

from flask import Flask,make_response,json,jsonify,redirect,url_for,request,session,render_template,flash
import click
from forms import LoginForm

app = Flask(__name__)
app.secret_key='secret string'

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
    return render_template('index.html',a=a)

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

if __name__ == '__main__':
    app.run()

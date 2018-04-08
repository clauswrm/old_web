from flask import render_template
from web import app


@app.route('/')
def hello_world():
    return 'hei'


@app.route('/user/<user>')
def default(user):
    return render_template('index.html', user=user)


@app.errorhandler(404)
def page_not_found(e):
    return '404 not found', 404

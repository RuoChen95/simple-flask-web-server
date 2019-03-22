from flask import \
    Flask, render_template, request, redirect, url_for, flash, jsonify, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

from flask import session as login_session

import random
import string

import json
from flask import make_response
import requests

from functools import wraps

client_id = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
client_secret = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_secret']

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/res/<int:id>/JSON')
@app.route('/res/<int:id>.JSON')
def resJSON(id):
    session = DBSession()
    res = session.query(Restaurant).filter_by(id=id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=res.id)
    return jsonify(MenuItems=[i.serialize for i in menu])


@app.route('/res/menu/<int:menu_id>/JSON')
@app.route('/res/menu/<int:menu_id>.JSON')
def resMenuJSON(menu_id):
    session = DBSession()
    menu = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menu.serialize)


@app.route('/login', methods=['GET'])
def login():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        code = request.data
        url = 'https://github.com/login/oauth/access_token?client_id='\
              + client_id\
              + '&client_secret=' + client_secret\
              + '&code=' + code
        access_token = requests.get(url).content.split('&')[0].split('=')[1]
        user_info = requests.get(
            'https://api.github.com/user?access_token=%s' % access_token)\
            .json()
        login_session['access_token'] = access_token
        login_session['username'] = user_info["login"]
        login_session['picture'] = user_info["avatar_url"]
        login_session['email'] = user_info["email"]
        login_session['bio'] = user_info["bio"]
        flash("You are now logged in as %s" % login_session['username'])
        return 'OK'


@app.route('/gdisconnect')
@app.route('/logout')
def gdisconnect():
    if login_session['access_token'] is None:
        print 'Access Token is None'
        response = make_response(json.dumps('User not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print 'In access token is %s', login_session['access_token']
        print 'User name is: '
        print login_session['username']
        # TODO: delete access_token in github
        del login_session['access_token']
        del login_session['username']
        del login_session['picture']
        del login_session['email']
        del login_session['bio']
        flash("You are now logout ")
        return redirect(url_for('all'))


@app.route('/')
@app.route('/res/')
def all():
    session = DBSession()
    res = session.query(Restaurant).all()
    menu = session.query(MenuItem)
    print menu
    return render_template(
        'res.html',
        res=res,
        menu=menu,
        login_session=login_session
    )


@app.route('/res/newRes/', methods=['GET', 'POST'])
@login_required
def addRes():
    session = DBSession()
    if request.method == 'GET':
        return render_template('newRes.html')
    if request.method == 'POST':
        newRes = Restaurant(name=request.form['name'])
        session.add(newRes)
        session.commit()
        flash('Add new restaurant success!')
        return redirect(url_for('all'))


@app.route('/res/editRes/<int:id>', methods=['GET', 'POST'])
@login_required
def editRes(id):
    session = DBSession()
    if request.method == 'GET':
        res = session.query(Restaurant).filter_by(id=id).one()
        return render_template('editRes.html', res=res)
    if request.method == 'POST':
        res = session.query(Restaurant).filter_by(id=id).one()
        res.name = request.form['name']
        session.commit()
        flash('edit res success')
        return redirect(url_for('all'))


@app.route('/res/deleteRes/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteRes(id):
    session = DBSession()
    if request.method == 'GET':
        res = session.query(Restaurant).filter_by(id=id).one()
        return render_template('deleteRes.html', res=res)
    if request.method == 'POST':
        # TODO: ON DELETE CASCADE functionality
        # Please consider to have the
        # ON DELETE CASCADE functionality implemented to
        # ensure database's integrity,
        # please look at the code review section
        # about how to do the implementation.
        #
        # It would be better for all the POST request,
        # you could include the csrf_token,
        # flask-seasurf provides you some simple way for this improvement.
        res = session.query(Restaurant).filter_by(id=id).one()
        session.delete(res)
        session.commit()
        flash('delete res success')
        return redirect(url_for('all'))


@app.route('/res/<int:id>/')
def restaurantMenu(id):
    session = DBSession()
    res = session.query(Restaurant).filter_by(id=id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=res.id)
    return render_template(
        'menu.html',
        res=res,
        menu=menu,
        login_session=login_session
    )


@app.route('/item/<int:id>/')
def item(id):
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=id).one()
    return render_template('item.html', item=item)


@app.route('/res/new/<int:res_id>/', methods=['GET', 'POST'])
@login_required
def add(res_id):
    session = DBSession()
    if request.method == 'GET':
        res = session.query(Restaurant).filter_by(id=res_id).one()
        return render_template('new.html', res=res)
    if request.method == 'POST':
        newM = MenuItem(name=request.form['name'], restaurant_id=res_id)
        session.add(newM)
        session.commit()
        flash('new menu item success')
        return redirect(url_for('restaurantMenu', id=res_id))


@app.route('/res/edit/<int:res_id>/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def edit(res_id, menu_id):
    session = DBSession()
    if request.method == 'GET':
        res = session.query(Restaurant).filter_by(id=res_id).one()
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('edit.html', res=res, menu=menu)
    if request.method == 'POST':
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        menu.name = request.form['name']
        menu.description = request.form['description']
        session.commit()
        flash('edit menu item success')
        return redirect(url_for('restaurantMenu', id=res_id))


@app.route('/res/delete/<int:res_id>/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def delete(res_id, menu_id):
    session = DBSession()
    if request.method == 'GET':
        res = session.query(Restaurant).filter_by(id=res_id).one()
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('delete.html', res=res, menu=menu)
    if request.method == 'POST':
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(menu)
        session.commit()
        flash('delete menu item success')
        return redirect(url_for('restaurantMenu', id=res_id))


if __name__ == '__main__':
    app.secret_key = 'secure key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

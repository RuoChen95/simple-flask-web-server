from flask import \
    Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@app.route('/res/<int:id>/JSON')
def resJSON(id):
    session = DBSession()
    res = session.query(Restaurant).filter_by(id=id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=res.id)
    return jsonify(MenuItems=[i.serialize for i in menu])


@app.route('/res/menu/<int:menu_id>/JSON')
def resMenuJSON(menu_id):
    session = DBSession()
    menu = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menu.serialize)


@app.route('/login', methods=['GET'])
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        access_token = request.data
        print access_token
    
        user_info = requests.get('https://api.github.com/user?access_token=%s' % access_token).json()

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
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print 'In gdisconnect access token is %s', login_session['access_token']
        print 'User name is: '
        print login_session['username']
        
        # TODO: delete access_token in github
        
        del login_session['access_token']
        del login_session['username']
        del login_session['picture']
        del login_session['email']
        del login_session['bio']

        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You are now logged out")
        return response
        

@app.route('/')
@app.route('/res/')
def all():
    session = DBSession()
    res = session.query(Restaurant).all()
    return render_template('res.html', res=res)


@app.route('/res/newRes/', methods=['GET', 'POST'])
def addRes():
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('newRes.html')
    if request.method == 'POST':
        newRes = Restaurant(name=request.form['name'])
        session.add(newRes)
        session.commit()
        flash('Add new restaurant success!')
        return redirect(url_for('all'))


@app.route('/res/editRes/<int:id>', methods=['GET', 'POST'])
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
def deleteRes(id):
    session = DBSession()
    if request.method == 'GET':
        res = session.query(Restaurant).filter_by(id=id).one()
        return render_template('deleteRes.html', res=res)
    if request.method == 'POST':
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
    return render_template('menu.html', res=res, menu=menu)


@app.route('/res/new/<int:res_id>/', methods=['GET', 'POST'])
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
def edit(res_id, menu_id):
    session = DBSession()
    if request.method == 'GET':
        res = session.query(Restaurant).filter_by(id=res_id).one()
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('edit.html', res=res, menu=menu)
    if request.method == 'POST':
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        menu.name = request.form['name']
        session.commit()
        flash('edit menu item success')
        return redirect(url_for('restaurantMenu', id=res_id))


@app.route('/res/delete/<int:res_id>/<int:menu_id>', methods=['GET', 'POST'])
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

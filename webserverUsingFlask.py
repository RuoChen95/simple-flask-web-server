from flask import \
    Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

from flask import session as login_session
import random
import string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


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


@app.route('/githubConnect', methods=['POST'])
def githubConnet():
    return


@app.route('/')
@app.route('/res/')
def all():
    session = DBSession()
    res = session.query(Restaurant).all()
    return render_template('res.html', res=res)


@app.route('/res/newRes/', methods=['GET', 'POST'])
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

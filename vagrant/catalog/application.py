from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from google.oauth2 import id_token
from google.auth.transport import requests
import random, string
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@app.route('/')
@app.route('/categories')
def categories():
    session = DBSession()
    categories = session.query(Category).all()
    new_items = session.query(Item).order_by(Item.timestamp.desc()).limit(5).all()
    return render_template('index.html', categories=categories, items=new_items)

@app.route('/categories/<int:category_id>/')
def category(category_id):
    session = DBSession()
    category = session.query(Category).get(category_id)
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category.html', category=category, items=items)

@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    session = DBSession()
    if request.method == 'GET':
        return render_template('new_category.html')
    else:
        newCategory = Category(name = request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("New Category created!")
        return redirect(url_for('category', category_id = newCategory.id))

@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    session = DBSession()
    category = session.query(Category).get(category_id)
    if request.method == 'GET':
        return render_template('edit_category.html', category=category)
    else:
        category.name = request.form['name']
        session.add(category)
        session.commit()
        flash("Category updated correctly!")
        return redirect(url_for('category', category_id = category_id))

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    session = DBSession()
    category = session.query(Category).get(category_id)
    if request.method == 'GET':
        return render_template('delete_category.html', category=category)
    else:
        session.delete(category)
        session.commit()
        flash("Category deleted correctly!")
        return redirect(url_for('categories'))




@app.route('/items/<int:item_id>/')
def item(item_id):
    session = DBSession()
    item = session.query(Item).get(item_id)
    return render_template('item.html', item=item)

@app.route('/items/new/', methods=['GET', 'POST'])
def newItem():
    if not login_session['sub']:
        abort(401)
    
    session = DBSession()
    categories = session.query(Category).all()
    if request.method == 'GET':
        return render_template('new_item.html', categories=categories)
    else:
        category_id = request.form['category']
        category = session.query(Category).get(category_id)
        newItem = Item(name = request.form['name'],
            description = request.form['description'],
            price = request.form['price'],
            image = request.form['image'],
            category = category,
            sub = login_session['sub'])
        session.add(newItem)
        session.commit()
        flash("New Item created!")
        return redirect(url_for('item', item_id = newItem.id))

@app.route('/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
    session = DBSession()
    categories = session.query(Category).all()
    item = session.query(Item).get(item_id)
    if item.sub != login_session['sub']:
        abort(401)

    if request.method == 'GET':
        return render_template('edit_item.html', categories=categories, item=item)
    else:
        category_id = request.form['category']
        category = session.query(Category).get(category_id)

        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.image = request.form['image']
        item.category = category
        session.add(item)
        session.commit()
        flash("Item updated correctly!")
        return redirect(url_for('item', item_id = item_id))

@app.route('/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    session = DBSession()
    item = session.query(Item).get(item_id)
    if item.sub != login_session['sub']:
        abort(401)

    category = session.query(Category).get(item.category_id)
    if request.method == 'GET':
        return render_template('delete_item.html', item=item)
    else:
        session.delete(item)
        session.commit()
        flash("Item deleted correctly!")
        return redirect(url_for('category', category_id=category.id))




@app.route('/api/categories/')
def categoriesJSON():
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


@app.route('/api/items/')
def itemsJSON():
    session = DBSession()
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    token = request.data
    
    CLIENT_ID = '156073641325-5rkho3i0a7li1peok2i7i6v2nrdn8h4p.apps.googleusercontent.com'
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        login_session['sub'] = idinfo['sub']
        login_session['name'] = idinfo['given_name']
        login_session['surname'] = idinfo['family_name']
        login_session['picture'] = idinfo['picture']

    except ValueError:
        # Invalid token
        pass

    return redirect(url_for('categories'))

@app.route('/logout')
def logout():
    login_session.pop('sub', None)
    login_session.pop('name', None)
    login_session.pop('surname', None)
    login_session.pop('picture', None)
    return redirect(url_for('categories'))


if __name__ == '__main__':
    app.secret_key = 'b4thHhB3bjoO0pdXTsQo3GGsJKKEQQ'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
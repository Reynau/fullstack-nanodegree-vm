from flask import *
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

import firebase_admin
from firebase_admin import credentials, auth

from flask_wtf.csrf import CSRFProtect, CSRFError

import random, string
import datetime

app = Flask(__name__)
csrf = CSRFProtect(app)

# Database initialization
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# Firebase initialization (Auth)
cred = credentials.Certificate("credentials/cred.json")
firebase_admin.initialize_app(cred)

@app.before_request
def do_something_whenever_a_request_comes_in():
    if not 'sub' in session:
        session_cookie = request.cookies.get('token')
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
            session['sub'] = decoded_claims['uid']
            session['name'] = decoded_claims['name']
            return
        except:
            return


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_cookie = request.cookies.get('token')
        # Verify the session cookie. In this case an additional check is added to detect
        # if the user's Firebase session was revoked, user deleted/disabled, etc.
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
            session['sub'] = decoded_claims['uid']
            session['name'] = decoded_claims['name']
            return f(*args, **kwargs)
        except ValueError as e:
            # Session cookie is unavailable or invalid. Force user to login.
            print(e)
            return redirect(url_for('login', mode="select", signInSuccessUrl=request.url))
        except auth.AuthError as e:
            # Session revoked. Force user to login.
            print(e)
            return redirect(url_for('login', mode="select", signInSuccessUrl=request.url))
    return decorated_function

@app.route('/categories')
@app.route('/')
def categories():
    db_session = DBSession()
    categories = db_session.query(Category).all()
    new_items = db_session.query(Item).order_by(Item.timestamp.desc()).limit(5).all()

    session_cookie = request.cookies.get('token')
    # Verify the session cookie. In this case an additional check is added to detect
    # if the user's Firebase session was revoked, user deleted/disabled, etc.
    try:
        auth.verify_session_cookie(session_cookie, check_revoked=True)
        return render_template('index.html', items=new_items, logged=True)
    except ValueError as e:
        # Session cookie is unavailable or invalid. Force user to login.
        print(e)
        return render_template('index.html', items=new_items, logged=False)
    except auth.AuthError as e:
        # Session revoked. Force user to login.
        print(e)
        return render_template('index.html', items=new_items, logged=False)
    

@app.route('/categories/<int:category_id>/')
def category(category_id):
    db_session = DBSession()
    category = db_session.query(Category).get(category_id)
    items = db_session.query(Item).filter_by(category_id=category.id).all()

    session_cookie = request.cookies.get('token')
    # Verify the session cookie. In this case an additional check is added to detect
    # if the user's Firebase session was revoked, user deleted/disabled, etc.
    try:
        auth.verify_session_cookie(session_cookie, check_revoked=True)
        return render_template('category.html', category=category, items=items, logged=True)
    except ValueError as e:
        # Session cookie is unavailable or invalid. Force user to login.
        print(e)
        return render_template('category.html', category=category, items=items, logged=False)
    except auth.AuthError as e:
        # Session revoked. Force user to login.
        print(e)
        return render_template('category.html', category=category, items=items, logged=False)

@app.route('/categories/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    if request.method == 'GET':
        return render_template('new_category.html', logged=True)
    else:
        newCategory = Category(name = request.form['name'])
        db_session = DBSession()
        db_session.add(newCategory)
        db_session.commit()
        flash("New Category created!")
        return redirect(url_for('category', category_id = newCategory.id))


@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    db_session = DBSession()
    category = db_session.query(Category).get(category_id)
    if request.method == 'GET':
        return render_template('edit_category.html', category=category, logged=True)
    else:
        category.name = request.form['name']
        db_session.add(category)
        db_session.commit()
        flash("Category updated correctly!")
        return redirect(url_for('category', category_id = category_id, logged=True))


@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):       
    db_session = DBSession()
    category = db_session.query(Category).get(category_id)
    if request.method == 'GET':
        return render_template('delete_category.html', category=category, logged=True)
    else:
        db_session.delete(category)
        db_session.commit()
        flash("Category deleted correctly!")
        return redirect(url_for('categories'))


@app.route('/items/<int:item_id>/')
def item(item_id):
    db_session = DBSession()
    item = db_session.query(Item).get(item_id)

    session_cookie = request.cookies.get('token')
    # Verify the session cookie. In this case an additional check is added to detect
    # if the user's Firebase session was revoked, user deleted/disabled, etc.
    try:
        decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
        return render_template('item.html', item=item, logged=True)
    except ValueError as e:
        # Session cookie is unavailable or invalid. Force user to login.
        print(e)
        return render_template('item.html', item=item, logged=False)
    except auth.AuthError as e:
        # Session revoked. Force user to login.
        print(e)
        return render_template('item.html', item=item, logged=False)


@app.route('/items/new/', methods=['GET', 'POST'])
def newItem():
    session_cookie = request.cookies.get('token')
    decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)

    db_session = DBSession()
    categories = db_session.query(Category).all()
    new_items = db_session.query(Item).order_by(Item.timestamp.desc()).limit(5).all()
    if request.method == 'GET':
        return render_template('new_item.html', items=new_items, logged=True)
    else:
        category_id = request.form['category']
        category = db_session.query(Category).get(category_id)
        newItem = Item(name = request.form['name'],
            description = request.form['description'],
            price = request.form['price'],
            image = request.form['image'],
            category = category,
            sub = decoded_claims['uid'])
        db_session.add(newItem)
        db_session.commit()
        flash("New Item created!")
        return redirect(url_for('item', item_id = newItem.id))


@app.route('/items/<int:item_id>/edit/', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    session_cookie = request.cookies.get('token')
    decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)

    db_session = DBSession()
    item = db_session.query(Item).get(item_id)
    if item.sub != decoded_claims['uid']:
        return abort(401, 'Insufficient permissions')

    categories = db_session.query(Category).all()
    if request.method == 'GET':
        return render_template('edit_item.html', categories=categories, item=item, logged=True)
    else:
        category_id = request.form['category']
        category = db_session.query(Category).get(category_id)

        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.image = request.form['image']
        item.category = category
        db_session.add(item)
        db_session.commit()
        flash("Item updated correctly!")
        return redirect(url_for('item', item_id = item_id))


@app.route('/items/<int:item_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteItem(item_id):
    session_cookie = request.cookies.get('token')
    decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
    
    db_session = DBSession()
    item = db_session.query(Item).get(item_id)
    if item.sub != decoded_claims['uid']:
        return abort(401, 'Insufficient permissions')

    category = db_session.query(Category).get(item.category_id)
    if request.method == 'GET':
        return render_template('delete_item.html', item=item, logged=True)
    else:
        db_session.delete(item)
        db_session.commit()
        flash("Item deleted correctly!")
        return redirect(url_for('category', category_id=category.id))




@app.route('/api/categories/')
def categoriesJSON():
    db_session = DBSession()
    categories = db_session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


@app.route('/api/items/')
def itemsJSON():
    db_session = DBSession()
    items = db_session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])




@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sessionLogin', methods=['POST'])
def sessionLogin():
    # Get the ID token sent by the client
    idToken = request.data
    # Set session expiration to 5 days.
    expires_in = datetime.timedelta(days=5)
    try:
        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(idToken, expires_in=expires_in)
        decoded_claims = auth.verify_session_cookie(session_cookie)
        session['sub'] = decoded_claims['uid']
        session['name'] = decoded_claims['name']
        response = jsonify({'status': 'success'})
        # Set cookie policy for session cookie.
        expires = datetime.datetime.now() + expires_in
        response.set_cookie(
            'token', session_cookie, expires=expires, httponly=True) # Should add secure=True if https is available
        return response
    except auth.AuthError:
        return abort(401, 'Failed to create a session cookie')

@app.route('/logout')
def logout():
    session.pop('sub', None)
    session.pop('name', None)
    response = make_response(redirect(request.referrer))
    response.set_cookie('token', expires=0)
    return response

@app.context_processor
def base_template_vars():
    db_session = DBSession()
    categories = db_session.query(Category).all()
    return dict(categories=categories)
    

if __name__ == '__main__':
    app.secret_key = 'b4thHhB3bjoO0pdXTsQo3GGsJKKEQQ'
    app.debug = True
    app.run(host = '0.0.0.0')
from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@app.route('/')
@app.route('/categories')
def categories():
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('index.html', categories=categories, items=items)

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
            category = category)
        session.add(newItem)
        session.commit()
        flash("New Item created!")
        return redirect(url_for('item', item_id = newItem.id))

@app.route('/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
    session = DBSession()
    categories = session.query(Category).all()
    item = session.query(Item).get(item_id)
    if request.method == 'GET':
        return render_template('edit_item.html', categories=categories, item=item)
    else:
        category_id = request.form['category']
        category = session.query(Category).get(category_id)

        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.category = category
        session.add(item)
        session.commit()
        flash("Item updated correctly!")
        return redirect(url_for('item', item_id = item_id))

@app.route('/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    session = DBSession()
    item = session.query(Item).get(item_id)
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



if __name__ == '__main__':
    app.secret_key = 'b4thHhB3bjoO0pdXTsQo3GGsJKKEQQ'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
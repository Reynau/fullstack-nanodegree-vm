from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories')
def home():
    categories = session.query(Category).all()
    return render_template('index.html', categories=categories)

@app.route('/categories/<int:category_id>/')
def category(category_id):
    category = session.query(Category).get(category_id)
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category.html', category=category, items=items)

@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'GET':
        return render_template('new_category.html')
    else:
        newCategory = Category(name = request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('category', category_id = newCategory.id))

@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    category = session.query(Category).get(category_id)
    if request.method == 'GET':
        return render_template('edit_category.html', category=category)
    else:
        category.name = request.form['name']
        session.add(category)
        session.commit()
        return redirect(url_for('category', category_id = category_id))

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    category = session.query(Category).get(category_id)
    if request.method == 'GET':
        return render_template('delete_category.html', category=category)
    else:
        session.delete(category)
        session.commit()
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
# Catalog application

Catalog application developed using [Flask](http://flask.pocoo.org/) that allows to create, read, update and delete items and categories. Allows registration and authentication using [Firebase Authentication](https://firebase.google.com/docs/auth/) service. 

## Features

- Create, Read, Update and Delete categories and items from a SQL database using [SQLAlchemy](https://www.sqlalchemy.org/)
- Create, Update and Delete operations are only alowed for authenticated users
- Update and Delete operations on items are only alowed for their authors.

## Design

All the server code is contained inside the application.py file, separated on different functional parts by visible code commentaries. Inside the templates folder you will find all the Jinja2 templates, and inside the static folder you will find all the scss and css generated styles.



## Requirements

- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)

## How to run it

Clone the repository and then execute the following command lines inside the repository directory:
```sh
$ cd vagrant
$ vagrant up
$ vagrant ssh
vagrant@vagrant$ cd /vagrant/catalog
vagrant@vagrant$ source /env/bin/activate
(env) vagrant@vagrant$ python database_setup.py
(env) vagrant@vagrant$ python application.py
```
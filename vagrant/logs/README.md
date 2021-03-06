# Python Reporting Tool

Reporting tool that prints out reports (in plain text) based on the data in a fictional news website
database created for the course.

The database contains three tables: articles, authors and log:

```
                                  Table "public.articles"
 Column |           Type           |                       Modifiers
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
```
```
                          Table "public.authors"
 Column |  Type   |                      Modifiers
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null default nextval('authors_id_seq'::regclass)
```
```
                                  Table "public.log"                                   
 Column |           Type           |                    Modifiers                      
--------+--------------------------+-------------------------------------------------- 
 path   | text                     |                                                   
 ip     | inet                     |                                                   
 method | text                     |                                                   
 status | text                     |                                                   
 time   | timestamp with time zone | default now()                                     
 id     | integer                  | not null default nextval('log_id_seq'::regclass)  
```

The questions that this python script answers are the following ones:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Design

The script has been designed to be simple and easy to understand. Each question is answered in a continuous block of code, identified by a comment, without being merged with other questions code, improving readability.  

A function named `printExerciceOutput` has been defined to facilitate the queries outputting and to remove code duplication.

## Requirements

- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)
- [Python 3](https://www.python.org/downloads/)
- [VM provided by the instructors](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
- [The database provided by the instructors](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

## How to run it

Extract your `newsdata.zip` file on your vagrant/logs directory and then run the following shell commands:
```sh
$ cd vagrant
$ vagrant up
$ vagrant ssh
vagrant@vagrant$ cd /vagrant/logs
vagrant@vagrant$ psql -d news -f newsdata.sql
vagrant@vagrant$ python logs.py
```
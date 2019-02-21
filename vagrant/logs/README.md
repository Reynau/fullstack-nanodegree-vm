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

## Requirements

- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)
- [Python 3](https://www.python.org/downloads/)
- [The database provided by the instructors](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

## How to run it

It requires Python and the VM with the postgresql database provided by the instructors.

Place the 'logs' folder inside the vagrant directory.

```sh
$ cd vagrant
$ vagrant up
$ vagrant ssh
vagrant@vagrant$ cd /vagrant/logs
vagrant@vagrant$ python logs.py
```
#!/usr/bin/env python3

"""Solves exercices of Logs deriverable for Full-Stack Web Developer Nanodegree."""


import psycopg2


def printExerciceOutput(title, result, extraOutput):
    """Print the result in clearly formatted plain tex."""
    print(title)
    for (p1, p2) in result:
        print('%s --- %s%s' % (p1, p2, extraOutput))
    print('\n')


db = psycopg2.connect("dbname=news")
c = db.cursor()

# Exercice 1
c.execute("""
    SELECT title, views
    FROM articles
    INNER JOIN (
        SELECT path, count(*) AS views
        FROM log
        GROUP BY path
    ) AS log 
    ON log.path = '/article/' || articles.slug
    ORDER BY views DESC 
    LIMIT 3;
""")
q1 = c.fetchall()
printExerciceOutput(
    '1. What are the most popular three articles of all time?', q1, 'views')

# Exercice 2
c.execute("""

    SELECT name, SUM(views) AS total
    FROM articles
    INNER JOIN authors ON articles.author = authors.id
    INNER JOIN (
        SELECT path, count(*) AS views
        FROM log
        GROUP BY path
    ) AS log 
    ON log.path = '/article/' || articles.slug
    GROUP BY name
    ORDER BY total DESC;
""")
q2 = c.fetchall()
printExerciceOutput(
    '2. Who are the most popular article authors of all time?', q2, 'views')

# Exercice 3
c.execute("""
    SELECT to_char(day, 'MON DD, YYYY'), percent FROM (
        SELECT date_trunc('day', time) AS day,
            ROUND(SUM(CASE WHEN status = '404 NOT FOUND'
            THEN 1 ELSE 0 END)::NUMERIC / count(*) * 100, 2) AS percent
        FROM log
        GROUP BY day) AS subq
    WHERE percent > 1
    ORDER BY percent DESC;
""")
q3 = c.fetchall()
printExerciceOutput(
    '3. On which days did more than 1% of requests lead to errors?',
    q3, '% errors')

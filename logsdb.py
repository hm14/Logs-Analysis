#!/usr/bin/env python

import psycopg2

DBNAME = "news"


# creates a report for the 3 required pieces of information
def create_report():
    headings = [[' * * * News Data Website Log Analysis * * *  \r\r'],
                ['Most Popular Articles', ' views'],
                ['Most Popular Authors', ' views'],
                ['Most Error Prone Days', ' %']]
    # creates a text file
    report = open("report.txt", "w+")
    report.write(headings[0][0])
    report.close()

    # each call writes a report requirement to text file
    write_report(headings[1][0], headings[1][1], get_top_articles())
    write_report(headings[2][0], headings[2][1], get_top_authors())
    write_error_report(headings[3][0], headings[3][1], get_top_error_days())


def write_report(heading, unit, raw_report):
    # opens text file
    report = open("report.txt", "a+")
    report.write(heading + '\r\r')
    for row in raw_report:
        # extracts data and concatenates strings to display desired format
        report.write('* ' + row[0] + ' - ' + str(row[1]) + unit + '\r')
    report.write('\r\r\r')
    report.close()


def write_error_report(heading, unit, raw_report):
    report = open("report.txt", "a+")
    report.write(heading + '\r\r')

    for row in raw_report:
        # changes datetime to str and desired format
        day = row[0].strftime('%m/%d/%y')
        # extracts data and concatenates strings to display desired format
        report.write('* ' + day + ' - ' + str(float(row[1])) + unit + '\r')
    report.close()


# runs query for 3 most viewed articles
def get_top_articles():
    # connect to db
    db = psycopg2.connect(database=DBNAME)
    # create cursor
    c = db.cursor()
    # run query
    c.execute("select articles.title, count(path) as views \
               from articles, log \
               where (articles.slug = split_part(path,'/article/',2)) \
               group by articles.title \
               order by count(path) DESC limit 3;")
    # store query result in variable report
    report = c.fetchall()
    # close db connection
    db.close()
    return report


# runs query for views of each author's articles
def get_top_authors():
    # connect to db
    db = psycopg2.connect(database=DBNAME)
    # create cursor
    c = db.cursor()
    # run query
    c.execute("select authors.name, count(path) as views \
               from authors, articles, log \
               where (articles.slug = split_part(path,'/article/',2)) \
               and authors.id = articles.author \
               group by authors.name \
               order by count(path) DESC;")
    # store query result in variable report
    report = c.fetchall()
    # close connection
    db.close()
    return report


# runs query for days when errors exceeded 1% of requests
def get_top_error_days():
    # connect to db
    db = psycopg2.connect(database=DBNAME)
    # create cursor
    c = db.cursor()
    # run query
    c.execute("select error_date as doomsday, \
               cast((100*errors/requests) as decimal(5,2)) as error_percent \
               from errors, requests \
               where error_date = request_date \
               and errors > requests/100.00;")
    # store qery result in variable report
    report = c.fetchall()
    # close connection
    db.close()
    return report

create_report()

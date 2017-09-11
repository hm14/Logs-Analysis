#News Data Log Analysis Project
A program to identify most viewed article and authors, and days when more than 1% of all received requests resulted in errors. The program is built using python and psql, and can be run using terminal. The program creates and writes output to report.txt.

##Installation
Install [Python](https://www.python.org/downloads/)

##Configuration
1) Make sure that the newsdata.sql database file is in the same directory as the one in which you run the logsdb.py python file.

2) Run the following commands to connect and load news database from newsdata.sql:
    psql -d news -f newsdata.sql
    psql -d news

3) Create the following views:

    i) create view requests as select time::timestamp::date as request_date, cast(count(status) as float) as requests from log group by request_date;

    ii) create view errors as select time::timestamp::date as error_date, cast(count(status) as float) as errors from log where status != '200 OK' group by error_date;

4) Run logsdb.py

##Output
The sample file sample.txt shows the format of output

##Code Layout

All code is in logsdb.py

The database newsdata.sql is not included

Be sure you have python and pip installed. Download it from their website:

https://python.org/

Be sure to install all requirements by calling the command

```
pip install -r requirements.txt
```

Once you have all the requirements installed, run the application by calling:

```
python run.py
```

The application will run on port 80.

Go to http://arboretum-backend.soe.ucsc.edu to see the website.

#Database Creation

SQLlite database for testing.

First, install SQLAlchemy.

pip install flask-sqlalchemy

In your python application, you need to import this:

from flask_sqlalchemy import SQLAlchemy.


In your application object, specify your database path in your 'SQLALCHEMY_DATABASE_URI' variable in your config class.

app.config['SQLALCHEMY_DATABASE_URI'] = ''# your path.

Then, in your __init__.py file, initialize your database, like this:

db = SQLAlchemy(app) # app the name of your application that you created in your __init__.py file, and db is the name of the database object you want to create.

now, in the python terminal, while located in the website directory:

Call this series of commands:

>>> from flask_greenhouse import db # flask_greenhouse is the name of your application.]
>>> db.create_all() # this creates your database if you haven't done so yet.

# this creates all your databases.

#testing commands:
>>> from flask_greenhouse import BMSDataentry # or whatever model you're using.
>>> json_received = {"language": "python", "framework": "flask"}
>>> entry_1 = BMSDataentry(json_content = json_received)
>>> db.session.add(entry_1)
>>> db.session.commit()

#to query the database from a fresh python terminal, run these commands:
>>> from flask_greenhouse import db
>>> from flask_greenhouse import BMSDataentry
>>> BMSDataentry.query.all() # or whatever query you want. read the flask docs for more information.
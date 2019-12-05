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

# Database Creation

Use a SQLlite database for testing.

First, install SQLAlchemy.
```
pip install flask-sqlalchemy
```
In your python application, you need to import this:
```python
from flask_sqlalchemy import SQLAlchemy.
```

In your application object, specify your database path in your 'SQLALCHEMY_DATABASE_URI' variable in your config class.

```python
app.config['SQLALCHEMY_DATABASE_URI'] = ''# your path.
```

Then, in your __init__.py file, initialize your database, like this:
```python
db = SQLAlchemy(app) # app the name of your application that you created in your __init__.py file, and db is the name of the database object you want to create.
```

now, in the python terminal, while located in the website directory:

Call this series of commands:
```python
>>> from flask_greenhouse import db # flask_greenhouse is the name of your application.]
>>> db.create_all() # this creates your database if you haven't done so yet.
```
This creates all your databases.

Testing Python database commands:
```python
>>> from flask_greenhouse.models import BMSDataentry # or whatever model you're using.
>>> json_received = {"language": "python", "framework": "flask"}
>>> entry_1 = BMSDataentry(json_content = json_received)
>>> db.session.add(entry_1)
>>> db.session.commit()
```

To query the database from a fresh python terminal, run these commands:
```python
>>> from flask_greenhouse import db
>>> from flask_greenhouse import BMSDataentry
>>> BMSDataentry.query.all() # or whatever query you want. read the flask docs for more information.
```
# Using Github (skip if you already know how)

Git is a Distriuted VCS. Every developer has a backup of the code.

Steps:

1.) 

install git.

command:

pip install git
	
2.) 
Set config values.
	
Command: 

git config --global user.name "William Kerr"
git config --global user.email "wkerr@ucsc.edu"

to see the configuration settings again, call:
	
git config --list

you can get help with any git verb by calling:

git config --help # config is the verb here. any verb will have the --help argument.

3a.) If there's an existing repository (with no .git 

Initialize your git repository.

command:

git init

To stop tracking a project with git, remove the .git directory.


3b.) If there's not an existing repository, create a folder, and then initialize your git repo.

4.) 
Before your first commit:

Add your files. 

see files added with git status. 

Command: 

git status

	
To ignore files, create a .gitignore file.

Linux Commands:

touch .gitignore

Windows Commands:

type nul > .gitignore

Things you may want to add in your .gitignore file in a Python project:

.DS_Store
.project
*.pyc

You do want to commit the .gitignore file, though.


5.)
Add files to staging area. 

Background:
There are 3 states: the working directory, the staging area, and the .git directory (repository)
Untracked files will stay in your working directory. 
Staging area is where we will organize what we want to be committed. We can pick and choose what we want committed.
.git directory is the place we actually store our repository.

To add files, use the git add command.

Commands: 

git add -A # this adds EVERYTHING that's not in the .gitignore file.
git status # this will tell you that now everything is in the staging area.

To remove something from the staging area, you can use git reset.

Commands:

git reset <filename>

6.) To Make a commit, use git commit.

git commit -m "Our first commit"

the -m argument passes in a message. If you don't do that, git will open your text editor and prompt you for a message.


7.) To Look at the commit log, use git log

git log 



8.) Cloning a remote repo;

Cloning means to copy a repository from another location.

Commands:

git clone <url> <where to clone>

9.) Viewing information about a remote repository:

To list information about the repositry

git remote -v

to list all branches in your repository, remotely and locally. 

git branch -a

To list the differences between the local files and the staging are files and the remote files:

Commands:

git diff

-	removed lines
+	added lines


10.) to add a remote origin:


git remote add origin


11.) To do a git pull: 

git pull. 

What it does: 
Pulls any changes that have been made by other developers since the last pull.

12.) To do a git push:

git push origin <branch> # usually pushing to master branch in single-developer situation.

what it does:

pushes your changes to the master.

13.) To change branches:

To one that exists:

git checkout <branch> 

To create one:

git branch <new branch name>

14.) To push a branch to our remote repository:

git push -u origin <branch> # we have pushed our new branch to our repository.
git branch -a # see all branches.

15.) To merge a branch to the master branch:

Commands:

git checkout master # switch to master branch. 
git pull origin master # update the local copy of the master branch.
git branch --merged # lists all the branches that have been merged with the current brangh. 
git merge <branch> # merge the changes in <branch> into the master branch
git branch --merged # see that the merge has worked.
git branch -d <branch> # delete that branch locally.
git push origin --delete <branch> delete that branch in the remote repository.


16.) fast example:

git branch subtract
git checkout subtract
git status # see that the working tree is clean.
git add -A
git commit -m <message>
git push -u origin subtract # push this new branch to the remote repo
git checkout master 
git pull origin master # pull all changes (if there are any). 
git merge subtract 
git push origin master # push changes 
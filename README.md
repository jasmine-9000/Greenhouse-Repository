Be sure you have python and pip installed. Download it from their website at:

https://python.org/

Be sure to install all requirements by calling this command


	pip install -r requirements.txt

Once you have all the requirements installed, run the application by calling:

    python run.py

    
The application will run on port 80.

Go to http://arboretum-backend.soe.ucsc.edu to see the website.

# Database Creation

Use a SQLlite database for testing.

First, install SQLAlchemy.


	pip install flask-sqlalchemy


In your python application, you need to import this:


	from flask_sqlalchemy import SQLAlchemy


In your application object, specify your database path in your 'SQLALCHEMY\_DATABASE\_URI' variable in your config class.


	app.config['SQLALCHEMY_DATABASE_URI'] = ''# your path.

Then, in your \__init__.py file, initialize your database.


	db = SQLAlchemy(app) 
	# app the name of your application that you created in your __init__.py file, and db is the name of the database object you want to create.


now, in the python terminal, while located in the website directory:

Call this series of commands:


	from flask_greenhouse import db # flask_greenhouse is the name of your application.  
	db.create_all() # this creates your database if you haven't done so yet.

This creates all your databases.

Testing Python database commands:

	
	>>> from flask_greenhouse.models import BMSDataentry # or whatever model you're using.
	>>> json_received = {"language": "python", "framework": "flask"}
	>>> entry_1 = BMSDataentry(json_content = json_received)
	>>> db.session.add(entry_1)
	>>> db.session.commit()

To query the database from a fresh python terminal, run these commands:

	>>> from flask_greenhouse import db
	>>> from flask_greenhouse import BMSDataentry
	>>> BMSDataentry.query.all() # or whatever query you want. read the flask docs for more information.

# Using Github 
##### (skip if you already know how to use git)

Git is a Distriuted Version Control System (VCS). When utilizing Git as the version control system, every developer has a backup of the code.

Steps:

## Install git.
	pip install git


## Set config values.

	git config --global user.name "William Kerr"
	git config --global user.email "wkerr@ucsc.edu"

to see the configuration settings again, call:

	git config --list

you can get help with any git verb by calling:

	git config --help # config is the verb here. any verb will have the --help argument.

## If there's an existing repository (with no .git file):
 
### Initialize your git repository.
	git init

To stop tracking a project with git, remove the .git directory.

##If there's not an existing repository:
create a folder, and then initialize your git repo.
	git init

## Before your first commit:

### Add your files. 
   see files added with git status. 
	git status
	
### To ignore files, create a .gitignore file.

1. Linux Commands:

	```touch .gitignore```
2. Windows Commands:

    ``` type nul > .gitignore```
3. Things you may want to add in your .gitignore file in a Python project:

	``` .DS_Store
	.project, *.pyc ```

 You do want to commit the .gitignore file, though.


## Add files to staging area. 

#### Background:

There are 3 states: the working directory, the staging area, and the .git directory (repository).

Untracked files will stay in your working directory. 

Staging area is where we will organize what we want to be committed. We can pick and choose what we want committed.

.git directory is the place we actually store our repository.

To add files, use the git add command.

  ```
  git add -A # this adds EVERYTHING that's not in the .gitignore file.
  git status # this will tell you that now everything is in the staging area.
  ```
To remove something from the staging area, you can use git reset.
```
git reset <filename>
```
## To Make a commit:
Use git commit.

	git commit -m "Our first commit"

the -m argument passes in a message. If you don't do that, git will open your text editor and prompt you for a message.


## To Look at the commit log:
Use git log

	git log 



## Cloning a remote repo

Cloning means to copy a repository from another location.

	git clone <url> <where to clone>

## Viewing information about a remote repository:

To list information about the repository:

	git remote -v

to list all branches in your repository, remotely and locally. 

	git branch -a

To list the differences between the local files and the staging are files and the remote files:

	git diff

Displays this result on the terminal:

	-	removed lines
	+	added lines


## Adding a remote origin

	git remote add origin


## Pulling changes 

Use git pull. 

	git pull

What it does: 
Pulls any changes that have been made by other developers since the last pull.

### To do a git push:

	git push origin <branch> 
	# usually pushing to master branch in single-developer situation.

what it does:

pushes your changes to the master.

## To change branches:

To one that exists:

	git checkout <branch> 

To create one:

	git branch <new branch name>

## To push a branch to our remote repository:

	git push -u origin <branch> # we have pushed our new branch to our repository.
	git branch -a # see all branches.	

## To merge a branch to the master branch:

	git checkout master # switch to master branch. 
	git pull origin master # update the local copy of the master branch.
	git branch --merged # lists all the branches that have been merged with the current brangh. 
	git merge <branch> # merge the changes in <branch> into the master branch
	git branch --merged # see that the merge has worked.
	git branch -d <branch> # delete that branch locally.
	git push origin --delete <branch> delete that branch in the remote repository.


## fast example:

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

# Sensor Routing

## Forms 

There are 3 forms: A User Registration Form, a User Login Form, a Sensor Data Request Form and a Sensor Registration Form.

### Sensor Registration Form
Options:

- sensor name
- units
- protocol
- type

Upon submission, a new sensor that's tied to the current user logged in will be added to our SQLite database.

### Sensor Data Request Form
Options:

- sensors owned 
	- a select field with all sensors owned
- start date: what time do you want to start requesting data
- end date: what time do you want to stop requesting data
- interval: an interval to query the database from. Must be a multiple of 10. 
- title: the title of the graph you want to plot
- x axis: what you want your x axis to be called
- y axis: what you want your y axis to be called

### User Login Form
Options:

- Username
- Password
- Remember Me

Upon submission, the database will lookup a user by username, and hash the provided password against the password stored in the database using a secret key.

This way, even if someone accesses the database directly, they won't know everyone's password unless they also know the secret key used for that password.

The Remember Me checkbox will tell the login manager to remember the user if the user closes the window or not by adding a cookie to the user's website.

### User Registration Form
Options:

- Username
- email (only for password resets)
- password
- confirm password

Upon submission, the web server will take the username, email, and password, create a new User instance with no sensors attached, and add it to the SQLite database.

## Models

### User Model

Login manager

Properties:

- username
- email
- password (stored in SHA-256 format)
- sensor list (we are backreferenced as 'master')

### Sensor Model

Properties:

- user id: the id of the user it belongs to.
- name: the name of the sensor
- type: what type of sensor it is
- units: what units it measures
- dataset: a list of Sensor Data Entries tied to it.

### Sensor Data Entry Model

Properties:

- date posted: what date was it posted. Default is time at creation.
- JSON content: a JSON Encoded dictionary class that converts itself back and forth from string as needed.
- sensor id: the id number of the sensor that produced this piece of data.


# Routes

## /sensors

Link:

http://arboretum-backend.soe.ucsc.edu/sensors

Requires you to be logged in. If not logged in, redirects you to the login page.

## /sensors/register

Link:

http://arboretum-backend.soe.ucsc.edu/sensors/register

Requires you to be logged in. Redirects you to login page if not logged in.

Allows you to register a new sensor, and start accepting data from it.

Unfortunately, it does not actually change the code on the Raspberry Pi itself.

## /sensors/users/register
Link:

http://arboretum-backend.soe.ucsc.edu/sensors/users/register

Allows a new user to register themselves into the database.

## /sensors/users/login
Link:

http://arboretum-backend.soe.ucsc.edu/sensors/users/login

Allows a user to login.

## /logout

Link:
http://arboretum-backend.soe.ucsc.edu/logout

Logs out a user upon visiting the URL.

This link will be displayed on the navigation bar.

# Post Route

Route:

http://arboretum-backend.soe.ucsc.edu/sensors/post-json/username/sensor_name

If a user by the name username exists and they have a sensor called sensor_name, then it will add the JSON content of your post request to a new Sensor Data Entry.

# Data Retrieval Routes 

## Multiple Data Point Route:
Link:

http://arboretum-backend.soe.ucsc.edu/sensors/get-sensor-json-data-range/sensor_id/start_date/end_date/interval

It's easier to search by sensor_id instead of sensor_name, and since the browser knows intrinsically what the sensor id is for each sensor, we can pass that instead of sensor name.

Returns a JSON file with all data points from start_date to end_date in interval minutes.


## Single data point route
Link:

http://arboretum-backend.soe.ucsc.edu/sensors/get-sensor-json-data-by-id/sensor_id/date

Returns a JSON file with a single data point.
If there's no data point: returns this:

	{
		data: {},
		date: <date>
	}


# BMS and Tristar Forms & Models

## Forms

### Date_Form

A front-end form used to request BMS data. 

Options:

- units
- start date
- end date
- interval
- title
- x axis
- y axis
- date format (python strftime behavior)
- style
- tight layout
- logarithmic scale
- marker

### Tristar Form
A front-end form used to request Tristar data.

Options:

- units
- start date
- end date
- interval
- title
- x axis
- y axis
- date format (python strftime behavior)
- style
- tight layout
- logarithmic scale
- marker

## Models
### JSONDataEntry
An inheritable class.

Properties

- date posted
- JSON content

Classes that inherit JSONDataEntry:

- BMSDataentry
- TristarDataEntry
- TristarDailyDataEntry

# Tristar and BMS routes

## BMS
### Routes
#### /BMS
	
Serves the BMS request graph

#### /BMS/server_side

Serves the server-side BMS request graph. Allows you to use matplotlib to do things.

#### /BMS/Instantaneous

Allows you to view the BMS data from the last known data point.

#### /BMS/Pins

Allows you to see the pins currently attached.

### POST routes
#### /BMS/post-json
Allows you to post BMS data.

### Data retrieval Routes
#### /BMS/api/single_point/date/parameter

Allows you to view a single data point at a specific date
#### /BMS/api/<string:start_date>/<string:end_date>/<int:interval>/<string:parameter>
Allows you to view multiple data points from start_date to end_date


## Tristar
### Routes
#### /Tristar
Serves the Tristar Request graph.
#### /Tristar/ChargeSettings
Allows you to view the current charge settings
#### /Tristar/DailyValues
Allows you to view last currently known Daily logger values.
### POST routes
#### /Tristar/post-json
Allows you to post instantaneous Tristar JSON data.
#### /Tristar/post-json/daily
Allows you to post daily Tristar JSON data.

### Data Retrieval routes
#### /Tristar/api/single_data_point/date/parameter

Allows you to view (in JSON format) a single Tristar data point with a certain parameter. 

#### /Tristar/api/start_date/end_date/interval/parameter

Allows you to view (in JSON format) Tristar data points within a range from start date to end date with an interval.

# JavaScript files

With my limited knowledge of jQuery and JavaScript, I wrote a few JavaScript files to retrieve data from the server using the data retrieval routes I wrote and described earlier, and graph them using Plotly.js.

View Tristar\_graph\_loader.js, BMS\_graph\_loader.js, and sensor\_graph\_loader.js for details, located in the static folder.

## Javascript Summary

The template API URLs are passed through my templating engine, Jinja2, and stored into the form itself by setting data-URL and data-MULTI\_URL to the API URLs.

Once the URLs have been passed the graph loaders when the form is submitted, the graph loaders turn the template API URLs into usable URLs that can request meaningful data using data from the form. 

The graph loader then sends an AJAX request with the API URL we built earlier, and upon success, stores all data  in a ```data{}``` dictionary.

```data{}``` and then is passed to a ```ChartIt()``` method that takes a ```data{}``` dictionary, and a div id to store the chart into.

Finally, this method is called:


	ChartIt(data, 'chart');

It takes a data dictionary containing x values (in our case, dates), y values (data points corresponding to those x_values), a graph title, x-axis title, y-axis title, etc., and plots it in the div id provided.

# Error Handling

This application handles errors using the functions in the errors/handlers.py file. This file is exported as a Flask blueprint, and applied to the main function by registering the blueprint in the __init__.py file.

It can handle these HTTP error codes:
 403,404,500,401,405,408,410,413,414,415,429,451,502,503,504.

When an error is thrown by the web server, the software will return an HTML template with information regarding the error.

## Example:

Not Found (404): The page you are looking for is not here.
Server Malfunction (500): Our server is experiencing technical difficulties.

# Deployment:

To deploy this website to a Linux Ubuntu web server properly, follow these steps:

## Update Linux
Call: 
	apt update && apt upgrade
## Set Hostname.
Call:
 
	hostnamectl set-hostname flask-greenhouse
	nano /etc/hosts

While in the nano editor, add a new line, and add this data:

	<hostname><tab>flask-greenhouse

```<hostname>``` is where the website is hosted.

```<tab>``` is a tab indent.

## Add limited user
Add a new user that can execute privileged commands. It’s safer than doing everything at root. Let’s not have hackers here.
Call: 

	adduser <username> #Then fill in all the information necessary.
	adduser <username> sudo
	# This gives <username> admin privileges.

If you’re going to do a GitHub transfer, skip the next two steps.
## Make a .ssh directory

Call 
	mkdir .ssh
## Upload your public key
On your local machine (on either Cygwin or on a Linux machine):
Call: 
	ssh-keygen -b 4096
	# generates a SSH key public-private key pair
	scp ~/.ssh/id_rsa.pub <username>@<hostname> ~/.ssh/authorized_keys
	# moves the public key to your server into the .ssh folder.

On your server:
Call:

	sudo chmod 700 ~/.ssh
	sudo chmod 600 ~/.ssh/*
	sudo nano /etc/ssh/sshd_config


Modify these parameters in the sshd_config file as necessary so these parameters have these values:

	PermitRootLogin no
	PasswordAuthentication no


For safety reasons, we cannot permit a root login, nor can we allow hackers to brute-force any user’s password. Since we have an SSH public key in our server now, we can disable password authentication, and disable root login.

## Setup firewall:

Call:

	sudo apt install ufw # this is an uncomplicated firewall. 
	sudo ufw default allow outgoing
	sudo ufw default deny incoming
	sudo ufw allow ssh
	sudo ufw allow <port number> 

This allows our port number to go through. For our test server, it will be 5000.

	sudo ufw enable # activae our firewall.
	sudo ufw status # see what we have allowed, and not allowed.
	
## Transfer Files.
You must get the source code of our website onto your server. You have several options to do this:

a.	git clone https://github.com/<repository_url>

b.	Execute an SSH file transfer of the website’s files using FileZilla or another FTP client. Ask someone who works in IT if you are unsure of how to do a SFTP over SSH. Ensure your private SSH key is applied to your transfer, and that you have uploaded your public key to the server properly.

## Install Packages
We need to install python3, pip, venv, our requirements from our requirements.txt file, and create our virtual environment.

Call: 

	sudo apt install python3-pip
	sudo apt install python3-venv
	python3 -m venv flask_greenhouse/venv 

This creates our virtual environment. if you accidentally created the venv folder in the wrong place, you can move it with the mv command. 

	source flask_greenhouse/venv/bin/activate # activates our virtual environment
	pip install -r requirements.txt

## Set Global Variables:
Instead of using environment variables, you should use a secure config.json file.
	
Call:
	sudo touch /etc/config.json
	sudo nano/etc/config.json

Your config.json file should contain:

	{
		‘SECRET_KEY’: “<secret key (sensitive)>”,
		‘SQLALCHEMY_DATABASE_URI’: “<SQLALCHEMY database URI (sensitive)”,
		‘MAIL_USERNAME’: “<username (sensitive)>”,
		‘MAIL_PASSWORD’: “<password (sensitive)>”,
	}

In your flask_greenhouse folder, there should be a config.py file. 

Have our config.py file load config.json instead of use environment variables.

## Running a Debug Server

To run a debug server, call:

	export FLASK_APP=run.py
	flask run –host-0.0.0.0

Your website should be running in debug mode.  When you navigate to your website, it should load properly. If there’s an error when loading your website, the console will display what type of error occurred. If you have set up error handling on your website (like I did), it should also work, too. My website should serve error templates back to the client in case of an error.

## Install nginx and gunicorn

These will be the two main engines that will serve our website for us while we are away. They are high performance engines, dedicated to serving websites.
Call these commands:

	cd ~/
	sudo apt install nginx
	pip install gunicorn  # ensure you’re still within your virtual environment.

Nginx will handle static files (CSS, JavaScript, Pictures).
Gunicorn will run the Python code.

## Update Nginx configuration files
Nginx does not come with our website enabled by default. To rectify that,
Call:

	sudo rm /etc/nginx/sites-enabled/default
	sudo nano /etc/nginx/sites-enabled/flask_greenhouse

The flask_greenhouse file will contain:

	server {
		listen 80;
		server_name <hostname>; # example: arboretum-backend.soe.ucsc.edu
		
		location /static {
			alias /home/<username>/greenhouse_website/flask_greenhouse/static;
		}
		location / {
			proxy_pass http://localhost:8000; #forwards all other traffic to port 8000
			include /etc/nginx/proxy_params;
			proxy_redirect off;
		}}


Call:

	sudo ufw allow http/tcp
	sudo ufw delete allow <port number> # where port number is your test port

## Create supervisor
Create your supervisor that handles traffic without your presence
Your website will run while you’re in an SSH session, but without a supervisor, once you close your SSH session, your website will shut down. To have your website be served while you’re not in an SSH session, install a supervisor to run your server without you.

Call:

	sudo apt install supervisor
	sudo nano /etc/supervisor/conf.d/flaskblog.conf

The file flaskblog.conf will contain:

	[program:flask_greenhouse]
	directory=/home/<username>/greenhouse_website
	command=/home/<username>/greenhouse_website/venv/bin/gunicorn -w 3 run:app
	user=<username>
	autostart=true
	autorestart=true
	stopasgroup=true
	killasgroup=true
	stderr_logfile=/var/log/greenhouse_website/greenhouse_website.err.log
	stdout_logfile=/var/log/greenhouse_website/greenhouse_website.out.log


Finally, call:

	sudo mkdir -p /var/log/greenhouse_website
	sudo touch /var/log/greenhouse_website/greenhouse_website.err.log
	sudo touch /var/log/greenhouse_website/greenhouse_website.out.log
	sudo supervisorctl reload
		# now, the supervisor should be restarted.

Your website should be up and running now.


# Raspberry Pi

## Introduction
This is the main Raspberry Pi code.

## run.py
This is the main loop of the Raspberry Pi. It initializes all of our stuff, and then does a forever loop, constantly reading data once per day, and once every chance it gets.

It wastes 2G data, but we've got plenty of that.

### Global Variables:

1. Private Server IP address: the IP address we want to send things to. Will be changed to arboretum-backend.soe.ucsc.edu later.
2. Destinations: what directories within the server do we want to send our files?
	1. BMS
	2. Tristar daily
	3. Tristar instantaneous 
	4. Faculty Sensors
	5. Student Sensors (n/a)
3. Bluetooth Addresses (TODO)

### Port Finding
Detect the operating system used.

If Linux, port numbers start with dev/ttyUSB*.

If Windows, port numbers start with COM*.

Create an array of ports.

Scan every port that the Raspberry Pi has connected. If it can find one that can connect to TSMPPT_1, TSMPPT_2 and BMS it will assign those ports to the respective reader classes created earlier.

The SixFab GSM/GPRS shield will always connect to dev/ttyS0, so there's no confusion on what port it will be connected to.

The initialization code will create TSMPPT, BMS, Faculty, and Sensor (light, water, and tempearture) reader classes. It will also create a sender class for the GSM shield.

At the start, the initialization code will also send a series of necessary initialization commands to the QualComm processor.


### Main Loop:
The code will then go into a forever looping code, executing these steps until shutdown:

1. Retrieve local time.
2. Construct local filenames for JSON files.
3. Create new files based on filenames.
4. If the local time is 23:58 PST: 
	1. Construct local filenames for daily Tristar Data
	2. Create new files
	3. Dump JSON data for daily monitoring data.
	4. Send JSON data to server at the post-json/daily address.
5. Dump JSON data for instantaneous monitoring data, BMS data, and Sensor data.
6. Close file pointesr.
7. Send all JSON data to their respective folders.

















#Summary
This website, as it pertains to my Senior thesis, is complete. I will add this README.md file to my Senior Thesis.


#Sources
https://docs.nginx.com/nginx/admin-guide/basic-functionality/runtime-control/

https://gunicorn.org/

https://ubuntu.com/download/server

https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

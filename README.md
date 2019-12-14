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

## Morningstar.py
### Introduction:

The TSMPPT has a Programmable Logic Controller (PLC) inside. The PLC can be reprogrammed to respond to different battery voltages. Example: when the battery goes to 3.7V, the battery goes to the equalize stage. To reprogram the Tristar MPPT, you must use a PC and a RS-232 to USB cable, and the program MSView, provided by Morningstar. 

Link: https://www.morningstarcorp.com/msview/. 

I also have a document called Viewing Data on Morningstar Devices that explains how to use the software.

However, the Tristar MPPT can be monitored by any device capable of serial monitoring, such asa a Raspberry Pi. Morningstar.py will contain the code necessary to monitor data from a Tristar Morningstar MPPT solar charge controller.

Morningstar has a MODBUS specification document for the Tristar Morningstar MPPT. It should be in my App Notes section. If not, here’s a link:

Link: https://www.stellavolta.com/content/MSCTSModbusCommunication.pdf

Morningstar.py contains a class that reads PLC data, denoted as Morningstar(). This class can monitor data by reading it and dumping the data to a JSON file. Details are in the upcoming sections.

### Dependencies:

#### modbus-tk:

The Tristar MPPT uses a royalty-free serial protocol called MODBUS. There exist many libraries to read it. The Python language has pymodbus, and modbus-tk.  Since pymodbus is not reliable (and I want reliable code), I will be using the modbus-tk library. It is distributed under the GNU-LGPL license (GNU Lesser General Public License) © 2009. Created by Luc Jean – luc.jean@gmail.com and Apidev – http://www.apidev.fr. No warranty of any kind.

#### json:
Comes with every distribution of python. Necessary to convert dictionaries into JSON format and dump it directly to an outfile.

#### serial:
This is a serial library for Python. It’s easy to use, and free. Provided as-is. Install with pip install pyserial. Use by calling “import serial”. ©2015 Chris Liechi clichi@gmx.net  All Rights Reserved. 

### Initialization

The Morningstar() class (like most other classes) has an __init__() function, that calls itself whenever a Morningstar() object is created. It requires port, baudrate, and the MODBUS slave number as arguments. When a Morningstar() object is created, it will initialize the serial connection to the PLC using this information. Then, it will create a MODBUS RtuMaster() class from the MODBUS-TK library.

After the MODBUS RtuMaster() class is initialized, it will call the internal function .scaling(). It will test what scaling factors are used.

Dictionaries in Python are everywhere in this code.

It will have methods to either dump data to the command line or dump data to an outfile. The outfile should be a .json file, since the contents will be written in JSON format.

### Classes:

#### Morningstar()

##### Description:
Reads data from the Tristar MPPT PLC. Takes PORT, BAUDRATE, and SLAVE_NUMBER upon initialization.

##### Variables:

- PORT: what port number are you using?
- BAUD: what baudrate are communicating at?
- SLAVE_NUMBER: what is the MODBUS slave number you’re reading from?
- serial\_connection: the serial connection from pyserial that actually communicates with the PLC.
- master: the class from modbus_tk that converts serial data into data we can read.


##### Methods:

- .scaling(): Sets the classes internal scaling properties (V_PU and I_PU). Also prints the current running version to the console. Runs every time an object of this class is created.

- .ADCdata(): Returns a dictionary containing ‘battery voltage’, ‘battery terminal voltage’, ‘battery sense voltage’, ‘array voltage’, ‘battery current’, ‘array current’, ‘12V supply’, ‘3V supply’, ‘meterbus voltrage’, ‘1.8V supply’, and ‘reference voltage’.

- .TemperatureData(): Returns a dictionary containing ‘heatsink temperature’, ‘RTS temperature’, and ‘battery regulation temperature’. All are in degrees Celsius.

- .StatusData(): Returns a dictionary containing ‘battery_voltage’, ‘charging_current’, ‘minimum battery voltage’, ‘maximum battery voltage’, ‘hour meter’, a list of faults, a list of alarms, the current state of the DIP switch, and the current state of the LED.


- .ChargerData(): Returns a dictionary containing ‘Charge State’, ‘target regulation voltage’, ‘Ah Charge Resettable’, ‘Ah Charge Total’, ‘kWhr Charge Resettable’, and ‘kWhr Charge Total’.

- .MPPTData(): Returns a dictionary containing: ‘output power’, ‘input power’, ‘max power of last sweep’, ‘Vmp of last sweep’, and ‘Voc of last sweep’.

- .Logger_TodaysValues(): Returns a dictionary containing: ‘Battery Voltage Minimum Daily’, ‘Battery Voltage Maximum Daily’, ‘Input Voltage Maximum Daily’, ‘Amp Hours Accumulated Daily’, ‘Watt hours accumulated daily’, ‘Maximum power output daily’, ‘Minimum temperature daily’, ‘Maximum Temperature Daily’, a list of daily faults, a list of daily alarms, ‘time_ab_daily’, ‘time_eq_daily’, and ‘time_fl_daily’.

- .ChargeSettings(): Returns a dictionary containing: 'EV_absorp', 'EV_float', 'Et_absorp', ‘Et_absorp_ext', 'EV_absorp_ext', 'EV_float_cancel', 'Et_float_exit_cum', 'EV_eq'], 'Et_eqcalendar', 'Et_eq_above', 'Et_eq_reg', 'Et_battery_service', 'EV_tempcomp', 'EV_hvd', 'EV_hvr', 'Evb_ref_lim', 'ETb_max', 'ETb_min', 'EV_soc_g_gy', 'EV_soc_gy_y', 'EV_soc_y_yr', 'EV_soc_yr_r', 'Elb_lim', 'EVa_ref_fixed_init', 'Eva_ref_fixed_pet_init'

- .DumpInstantenousDataToJSONFile(outfile): Calls all instantaneous data internal class methods (ADCdata(), TemperatureData(), StatusData(), ChargerData(), MPPTData()), and dumps them into an outfile using json.dumps(). Preferably, the file’s name will end in “.json” so the operating system can recognize that the file is in JSON format.

- .DumpDailyDataToJSONFile(outfile): Calls all daily data internal class methods (Logger_TodaysValues() and ChargeSettings()) and dumps them into an outfile using json.dumps(). Preferably, the file’s name will end in “.json” so the operating system can recognize that the file is in JSON format.


## BMS.py
### Introduction:
The Battery Management System (BMS) has a Programmable Logic Controller (PLC) in it. It can be used to monitor things such as charge dissipated, voltage levels of each individual cell, etc.
The internal PLC can be monitored using a USB interface. This is what the Raspberry Pi will do using the interpreted Python Language.
The Python language is dependent on classes to process data. So, I will be writing a Python class to ex-tract data from the BMS PLC.

### Dependencies:
#### pyserial: 
This is a serial library for Python. It’s easy to use, and free. Provided as-is. Install with pip install pyserial. Use by calling “import serial”. ©2015 Chris Liechi clichi@gmx.net  All Rights Reserved. 

Usage: https://pyserial.readthedocs.io/en/latest/pyserial.html

#### crc8_dallas: 
This is a CRC-8 library that uses the exact polynomial we need for this application: x^8 + x^2+x+1.  I had to modify the code to work with Python 3, since it was originally developed for Python 2.
#### sys: 
Comes with every distribution of python. Necessary to have a test bench.
Usage: https://docs.python.org/3/library/sys.html

#### json: 
Comes with every distribution of python. Necessary to convert dictionaries into JSON format and dump it directly to an outfile.
Usage: https://docs.python.org/3/library/json.html

### Initialization:
Create a BMS() object, passing in PORT and BAUDRATE. This will initialize the serial connection to the BMS PLC.
The BMS() object will destroy itself when python exits.
Classes:

#### BMSStatistic():
##### Description:
An internal class that contains a statistic from the sentence SS1(). Makes it easier to do mass data collec-tion from a series of sentences if a request for every statistic available is made.
##### Variables:

Every BMSStatistic object contains at least 4 variables:

-	statisticIdentifier: what is the ID of this statistic (i.e. what protocol to use to process it)
-	statisticValue: what is the value spat out (in decimal converted earlier from hexadecimal) from the BMS system?
-	statisticValueAdditionalInfo: any additional information spat out from the BMS system (e.g. Cell ID)?
-	timestamp: what time (in seconds since January 1, 1970 at 00:00 GMT) recorded. The BMS sys-tem records it in seconds since January 1, 2000 at 00:00 GMT).
Possible additional variables the class can have: 
-	Name: What is the real name of the statistic?
-	Unit: what unit is the value recorded in (e.g. V, mA, W)? If N/A, the value is simply how many times an event occurred.
-	Cell_ID: What is the ID of the cell the statistic came from?
Methods:
-	.dict(): converts this class into a dictionary with keys being the class variables it has, and their cor-responding values.
-	.string(): converts this class into a string in JSON format. 
-	.__init__(): initializes the object. Takes statisticIdentifi-er,statisticValue,statisticValueAdditionalInfo,timestamp. Upon creation, runs a specific protocol to process the data based on its statisticIdentifier.

### BMS():
#### Description:
A class that can read the BMS system. Call the .DumpToJSONFile() method to dump all data to an outfile. Details below.

#### Variables:

Every BMS() object contains at least 3 variables:

-	PORT: what port number is the Raspberry Pi reading from?
-	BAUDRATE: at what baudrate (in bits/second) is the Raspberry Pi reading at?
-	ser: the serial object (from the pyserial library) that sends and receives data from the BMS.
	
#### Methods:

-	.VR1(): returns a dictionary containing hardware type, serial number, and firmware version.
-	.BB1(): returns a dictionary containing number of cells, minimum balancing rate, and average cell balancing rate.
-	.BB2(): returns a dictionary containing cell string number, first cell number, size of group, and in-dividual cell module balancing rate of each cell group. 
-	.BC1(): returns a dictionary containing battery charge, battery capacity, and state of charge.
-	.BT1(): returns a dictionary containing the summary of cell module temperature values of the bat-tery pack.
-	.BT2(): This sentence contains individual cell module temperatures of a group of cells. Each group consists of 1 to 8 cells. This sentence is sent only after Control Unit receives a request sentence from external device, where the only data field is ‘?’ symbol. The normal response to BT2 request message, when battery pack is made up of two parallel cell strings:
-	.BT3(): This sentence contains the summary of cell temperature values of the battery pack. It is sent periodically with configurable time intervals for active and sleep states (Data Transmission to Display Period).	
-	.BT4(): This sentence contains individual cell temperatures of a group of cells. Each group con-sists of 1 to 8 cells.
-	.BV1(): Returns a dictionary containing a summary of cell voltages. contains number of cells, min-imum cell voltage, maximum cell voltage, average cell voltage, and total voltage.
-	.BV2(): This sentence contains individual voltages of a group of cells. Each group consists of 1 to 8 cells.
-	.CF2(parameterID): returns the parameter data of the parameter ID. Must be processed separately.
-	.CG1(): This sentence contains the statuses of Emus internal CAN peripherals. Can include CAN current sensor, and CAN cell group, along with the cell group number.
-	.CN1(): This sentence reports the CAN messages received on CAN bus by Emus BMS Control Unit, if “Send to RS232/USB” function is enabled.
-	.CN2(): This sentence reports the CAN messages sent on CAN bus if "Send to RS232/USB func-tion is enabled.
-	.CS1(): Returns a dictionary containing the parameters and status of the charger. Includes set volt-age, set current, actual voltage, actual current, number of connected charger, and CAN charger status.
-	.CV1(): Returns a dictionary containing the values of total voltage of battery pack, and current flowing through the battery pack.
-	.DT1(): This is a placeholder for an electric vehicle sentence. The code is being specifically programmed for a greenhouse, so this sentence will not be programmed and return an error.
-	.FD1(): This sentence resets the unit to factory defaults. Use at your own risk.
-	.IN1(): This sentence returns a dictionary containing the status of the input pins (AC sense, IGN In, FAST_CHG).
-	.LG1(clear): This sentence can either: retrieve events logged, or clear the event logger.
	- Retrieve Events Logged: pass in ‘N’ or a null value. 
		- Every event is recorded in a dictionary form like this: [“log event number 1”]: [“log event”: “No event”, “unix time stamp”: 1567014467
		- Possible events:
			-	No Event
			-	BMS started
			-	Lost communication to cells
			-	Established communication to cells
			-	Cells voltage critically low
			-	Critical low voltage recovered
			-	Cells voltage critically high
			-	Critical high voltage recovered
			-	Discharge current critically high
			-	Discharge critical high current recovered
			-	Charge current critically high
			-	Charge critical high current recovered
			-	Cell module temperature critically high
			-	Critical high cell module temperature recovered
			-	Leakage detected
			-	Leakage recovered
			-	Warning: low voltage – reducing power
			-	Power reduction due to low voltage recovered
			-	Warning: high current – reducing power
			-	Power reduction due to high current recovered
			-	Warning: High Cell module temperature – reducing power
			-	Power reduction due to high cell module temperature recovered.
			-	Charger connected 
			-	Charger disconnected
			-	Started pre-heating stage
			-	Started pre-charging stage
			-	Started main charging stage
			-	Started balancing stage
			-	Charging finished
			-	Charging error occurred
			-	Retrying charging
			-	Restarting charging
			-	Cell Temperature Critically high
			-	Critically high cell temperature recovered
			-	Warning: High cell temperature – reducing power
		-	Unix Timestamp: Time recorded in seconds since January 1, 1970 at 00:00 GMT.
		-	Log event number: what event number it 
	- Clear Event Logger: pass in the ascii value ‘C’ or ‘c’.
-	.OT1(): Returns a dictionary containing the status of output pins (Charger pin, heater, bat. low, buzzer, chg. ind.)
-	.PW1(request, password): Check the admin status with PW1(‘?’). Log into BMS system with PW1(‘P’, password). Logout with PW1().
-	.PW2(request, newPassword): Sets a new password, or clears a password. To set new password, call PW2('S',"mynewpassword"), and substitute “mynewpassword” with whatever password you want. To clear your password, call PW2('C'). Returns true if successful, false if not successful.
-	.RC1(): Resets the current sensor reading to zero. Used after current sensor is initially installed.
-	.RS1(): Resets the Emus BMS control unit entirely. Like a sudo reboot on a linux machine. Re-quires admin clearance.
-	.RS2(): This sentence is used to retrieve the reset source history log.
-	.SC1(percentage): This sentence sets the current state of the charge of the battery in %. Send in an integer from 0 to 100. This method will convert to hexadecimal format first. Returns False if not successful or invalid percentage is passed. Returns True if successful.
-	.SS1(request, statisticIdentifier): This sentence can either: Request All Statistics, Request a Specific Statistic (pass in a number), or Clear all unprotected statistics.
	- Request All Statistics: call SS1(‘?’). This will return all statistics the BMS currently has in the form of dictionaries converted from BMSstatistic classes.
	- Request a Specific Statistic: call SS1(‘N’, number), where number is a positive integer. Re-turns a dictionary containing a single statistic.
	- Clear all unprotected statistics: call SS1(‘c’). 
-	.ST1(): This sentence returns the status of the BMS in dictionary form. It contains these statistics:
	- Charging flags: charging stage, last charging error, last charging error parameter (for de-bugging purposes), stage duration, 
	- Status flags: Valid cell voltages, Valid balancing rates, valid number of live cells, battery charging finished, valid cell temperatures
	- Protection flags: undervoltage, overvoltage, discharge overcurrent, charge overcurrent, cell module overheat, leakage, no_cell_comm, cell_overheat
	- Power flags: warning: power reduction: low voltage, warning: power reduction: high cur-rent, warning: power reduction: high cell module temperature,  warning: power reduction: high cell temperature
	- Pin flags: ```no_function```, ```speed_sensor```, ```fast_charge_switch```, ```ign_key```, ```charger_mains_AC_sense```, ```heater_enable```, ```sound_buzzer```, ```battery_low```, ```charging_indication```, ```charger_enable_output```, ```state_of_charge```, ```battery_contactor```, ```battery_fan```, ```current_sensor```, ```leakage_sensor```, ```power_reduction```, ```charging_interlock```, ```analog_charger_control```, ```ZVU_boost_charge```, ```ZVU_slow_charge```, ```ZVU_buffer_mode```, ```BMS_failure```, ```equalization_enable```, ```DCDC_control```, ```ESM_rectifier_current_limit```, ```contactor_precharge```
-	.TD1(): Returns time and date according the BMS in dictionary form. Returns year, month, day, hour, minute, second, and the amount of uptime the unit has in seconds.
-	.TC2(): Used to calibrate cell temperature by a PC, not a microcontroller.
-	.DumpToJSONfile(outfile): Calls all data methods listed above, then dumps all data returned into an outfile in JSON format.
Note: Every data harvesting method returns “Cannot communicate to cells” if it fails.

### Private Methods:

#### bitAt(bitfield, position): 

##### Description:

Returns True if the bit is 1 at the position of the bitfield, False of 0. Used to analyze bitfields with fewer lines.














# Summary
This website, as it pertains to my Senior thesis, is complete. I will add this README.md file to my Senior Thesis.


# Sources
https://docs.nginx.com/nginx/admin-guide/basic-functionality/runtime-control/

https://gunicorn.org/

https://ubuntu.com/download/server

https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

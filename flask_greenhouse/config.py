# this is our secret configuration file. It's stored as a python class. 
class Config:	
	SECRET_KEY = 'e2a66d067f6ef25bda6011bd50d587ab' #os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' #os.environ.get('SQLALCHEMY_DATABASE_URI') # database path relative to flaskblog.py
#we need a mail server, a mail port, whether to use TLS, username and password for that server.
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
#MAIL_USE_SSL = True
#use environment variables to set username and password for personal email.
	MAIL_USERNAME = 'wrkerr9@gmail.com'#os.environ.get('EMAIL_USERNAME')
	MAIL_PASSWORD = 'integrals19'#os.environ.get('EMAIL_PASSWORD')
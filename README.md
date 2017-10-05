
# Introduction
This is a webapp powered by __flask__ & __bootstrap__,which is designed for:  
- **Collecting sharings shared by members in Wechat group, save them into database and show them on a webpage**
- **Q&A. Posting questions or views, other members can comment on it, a bit like Tieba**

# Config
to make WTForm work correctly, we need a secret key.The secret key is a random-like string.
to generate a random-like string:  
in bash:

    cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32
if with mac:

    cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-f0-9' | head -c 32  

if with window, you can use os module  
    `>>>import os`  
    `>>>os.urandom(24)`  


add the string into config.py: 

    class DevConfig(Config):
	    
	    SECRECT_KEY = ' '  #add here
	    SQLALCHEMY_TRACK_MODIFICATIONS = True
	    DEBUG = True
	    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')


# Installation
## Requirements
* python3 is required
* requirements.txt


###  to run the webapp:

create a virtual environment:  
`$pip3 install virtualenv`  

`$virtualenv my_env`

activate the virtual environment    
`$source app_env/bin/activate`  

install all independence in the virtual environment   
`(my_env)$ pip install -r requirements.txt`  

initiate databse:       
`(my_env)$ python manage.py setup_db`  

run the server:       
`(my_env)$ python manage.py gserver`  


__note__:
if with window, get into /my_env/Scripts/ , then run `activate` in the command line in this directory so as to activate the virtual environment

### to run the robot:
`$ python manage.py robot`   
A QR code will generate, you need to scan it and press confirm on your phone to log in your wechat account
then the robot(your wechat account)begin listening.Once somebody send sharing in Wechat group chatroom,
it can save the sharing info into database.

# Deploy
The most easiest way to deploy this webapp by using **gevent**, the related code was included in **manage.py**,
to run the gevent server:  
`$ python manage.py gserver`

# Tests
piece of  UI test provided, with Firefox and Firefox driver installed  
run:

`$ pip install selenium`  
`$ python ui_test.py`

# Todoist
- [ ] add unittest
- [ ] add cache
- [ ] construct restful API
- [ ] log in with wechat openid

# Introduction
This is a webapp powered by __flask__ & __bootstrap__,which is designed for:  
- **A very very friendly community for newbie**
- **Enhance communication. Posting questions or sharing views, other members can comment on it, a bit like Tieba**

# Config
To make WTForm work correctly, we need a SECRET KEY. The SECRET KEY is a random-like string.

Generate a random-like string in your Python 3 interpreter:

```python
import os, base64
n = 24
print(base64.b32encode(os.urandom(n)).decode('utf-8')[:n])
```


And please add the following string into the end of `webapp/config.py`: 

```python
class DevConfig(Config):
    
    SECRECT_KEY = os.environ.get('SECRECT_KEY', 'put your random key here') 
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')
```

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

#### test run:
initiate databse:       
`(my_env)$ python manage.py setup_db_test`

run the server:       
`(my_env)$ python manage.py gserver`  

#### real run:

initiate databse:

remove the existed database.db first

`(my_env)$ python manage.py setup_db_real`  


run the server:       
`(my_env)$ python manage.py gserver`  


__note__:
if with window, get into /my_env/Scripts/ , then run `activate` in the command line in this directory so as to activate the virtual environment.You can also add it to path.


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
- [ ] log in with  openid
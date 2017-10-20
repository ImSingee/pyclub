
## Introduction
This is a webapp powered by __flask__ & __bootstrap__,which is designed for:  
- **A very very friendly community for newbie**
- **Enhance communication. Posting questions or sharing views, other members can comment on it, a bit like Tieba**

## Pre-do

### Generate a SECRET_KEY

To make WTForm work correctly, we need a SECRET KEY. The SECRET KEY is a random-like string.

Generate a random-like string in your Python 3 interpreter:

```python
import os, base64
n = 24
print(base64.b32encode(os.urandom(n)).decode('utf-8')[:n])
```

### Environmental Configure

* Python 3
* Virtual environment
    * `$ pip install virtualenv`
    * `$ virtualenv my_env`
    * `$ source my_env/bin/activate`
* You should install the libraries used in the project
    * `$ pip intall -r requirements`
* Environmental variables
    * `WEBAPP_ENV`: `dev` for development or `product` for production environment
    * `ADMIN_USERNAME`: default admin username
    * `ADMIN_PASSWORD`: default admin password
    * `ADMIN_EMAIL`: default admin email
    * `SECRET_KEY`: the string you generated right now

## Run


Initiate database: `$ python manage.py setup_db`

Run the server: `$ python manage.py runserver`  



## Deploy
The most easiest way to deploy this webapp by using **gevent**, the related code was included in **manage.py**,
to run the gevent server:  

`$ python manage.py gserver`

## Tests
piece of  UI test provided, with Firefox and Firefox driver installed  
run:

```bash
pip install selenium
python tests/test_ui.py
```


## Todo
- [ ] Add unittest
- [ ] Add cache
- [ ] Construct restful API
- [ ] Log in with  openid
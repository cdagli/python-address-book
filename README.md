# python-address-book

[![Build Status](https://travis-ci.org/cdagli/python-address-book.svg?branch=master)](https://travis-ci.org/cdagli/python-address-book)

### Install
```
git clone https://github.com/cdagli/python-address-book
cd python-address-book
virtualenv venv 
source venv/bin/activate
pip install -r requirements.txt 
```

### Run 
```
python run.py 
```

### Tests 
```
nose2 
```

### Documentation

You can use the swagger.json to visualize the API documentation or a live swagger json will be available at **http://localhost:5000/api/v1.0/spec** when the script is started. You can use [this](https://chrome.google.com/webstore/detail/swagger-ui-console/ljlmonadebogfjabhkppkoohjkjclfai?hl=en) Chrome extension to visualize the documentation. 

![Swagger Screenshot](https://github.com/cdagli/python-address-book/blob/master/swagger.png)

### Notes 

Application uses the SQLite in memory database currently. If you'd like to change that please edit DevelopmentConfig class in the /api/utils/config.py

### Design-only question
Since SQLAlchemy is used on this project (or any other SQL would work, too) a substring could be searched like below; 

```
db.table.column.like('%comp%')
```

### Todo
    1. Better exception handling 
    2. Field validations
    3. Check existence of records and return messages e.g. "User does not exists, group does not exists" 
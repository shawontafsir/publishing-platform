# Simple Content Publishing Platform

## To Run The project:

### Back-end:
```
// go to the backend directory
$ cd backend

// create a python virtualenv
$ virtualenv venv

// activate the venv
$ source venv/bin/activate

// install dependencies
$ pip install -r requirements.txt

// run the project at port 8000
$ ./manage.py runserver 8000
```
Now, the **Backend** is ready to serve the **Rest API**.


### Front-end:
```
// go to the frontend directory
$ cd frontend

// install node dependencies locally
$ npm install

// run the parcel bundler
$ parcel index.html
```
Now, the **Frontend** is ready. Open the url built by the `parcel bundler` to the **browser**.
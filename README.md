# Fetch

How to run:
- This project is running on python version 3.8
- use pip to install the dependencies listed in requirements.txt
- follow the instructions on https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application to start the server
-- instead of hello.py, replace with main.py when setting the FLASK_APP environment variable
  
- use python -m flask run to run the server which will accept requests on http://127.0.0.1:5000

API Specifications
- there are 3 endpoints: /add_points [POST], /deduct_points[POST], and /balance [GET]
- /add_points takes in a json object like this: {
	"name": "UNILEVER",
	"amount": 200,
	"time": "2020-10-31 11"
}
  - the name must be a string, amount must be an int, and time must be a datetime in the format '%Y-%m-%d %H'.
    
- /deduct_points takes in a json object like this: {
	"amount": 5000
} where amount must be an int
  
- /balance is a get request and needs no parameters


# Instructions

1. Go to the server directory

```
cd server
```

2. Initialize your virtual environment

```
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:

```
.\venv\Scripts\activate
```

- On macOS and Linux:

```
source venv/bin/activate
```

4. Install the project dependencies:

```
pip install -r ../requirements.txt
```

5. Initialize the flask server

- On Windows:

```
set FLASK_APP=app.py
```

- On macOS and Linux:

```
export FLASK_APP=app.py
```

6. Start the server

```
flask run
```

7. Check out the following pages:

[Login](http://127.0.0.1:5000/login)

[User Dashboard](http://127.0.0.1:5000/)
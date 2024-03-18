from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
import sqlite_setup
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hurriscan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

sqlite_setup.main()
app = Flask(__name__)

@app.route('/data-visualization')
def data_visualization():
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('SELECT month, SUM(temp) as total_temp FROM Data GROUP BY month')
    data = cur.fetchall()

    conn.close()

    months = [row['month'] for row in data]
    temps = [row['total_temp'] for row in data]

    return render_template('data_visualization.html', months=months, temps=temps)

@app.route('/')
def home():
    return 'Welcome to the Home Page'

@app.route('/login')
def login():
    return render_template('login/login.html')

@app.route('/registration')
def registration():
    return render_template('registration/registration.html')

@app.route('/createAccount')
def createAcc():
    return render_template('registration/accountCreation.html')

@app.route('/alerts')
def alerts_page():
    return render_template('alerts.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin/admin-dashboard.html')

@app.route('/users')
def get_users():
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('SELECT * FROM User')
    rows = cur.fetchall()

    users = []
    for row in rows:
        user = {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'email': row[3],
            'phone': row[4],
            'alerts_email': row[5],
            'alerts_phone': row[6],
            'isAdmin': row[7]
        }
        users.append(user)

    conn.close()
    return jsonify(users)

@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    try:
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
        cur = conn.cursor()
        cur.execute('DELETE FROM User WHERE id = ?', (user_id,))
        conn.commit()
        
        conn.close()
        return redirect('/admin') # Doesn't do anything, but needed to return something ¯\_(ツ)_/¯

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/create-alert', methods=['POST'])
def create_alert():
    title = request.form['title']
    text = request.form['text']
    date = datetime.now().date()

    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    cur = conn.cursor()
    cur.execute('INSERT INTO Alert (title, text, date) VALUES (?, ?, ?)', (title, text, date))
    conn.commit()
    cur.execute('SELECT * FROM Alert')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

    return redirect('/alerts') # Wrong path but will change later!


if __name__ == '__main__':
    app.run(debug=True)


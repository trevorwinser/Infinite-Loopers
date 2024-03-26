from flask import Blueprint, render_template, jsonify, redirect, request
import os
import sqlite3
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder="../templates", static_folder="../static")

basedir = os.path.abspath(os.path.dirname(__file__))

@admin_bp.route('/admin')
def admin_dashboard():
    return render_template('admin-dashboard.html')

@admin_bp.route('/admin-navbar')
def admin_nav_bar():
    return render_template('admin-navbar.html')

@admin_bp.route('/users')
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

@admin_bp.route('/delete-user/<int:user_id>')
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
    
@admin_bp.route('/create-alert', methods=['POST'])
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

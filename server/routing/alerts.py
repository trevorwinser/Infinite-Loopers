from flask import Blueprint, render_template, redirect, request
import sqlite3

alerts_bp = Blueprint('alerts', __name__, template_folder="../templates", static_folder="../static")

@alerts_bp.route('/alerts', methods=['GET', 'POST'])
def alerts_page():
    if request.method == 'POST':
        phone = request.form.get('phone')
        email = request.form.get('email')
        east_coast = request.form.get('east-coast')
        west_coast = request.form.get('west-coast')

        if '@' not in email or len(phone) < 10:
            return "Invalid email or phone number"

        if east_coast and west_coast:
            zone = 'both'
        elif east_coast:
            zone = 'east'
        elif west_coast:
            zone = 'west'
        else:
            return "No zone selected"

        conn = sqlite3.connect('hurriscan.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE User
            SET phone = ?, email = ?, alerts_email = 1, alerts_phone = 1, zone = ?
            WHERE username = "User1";
        ''', (phone, email, zone))

        conn.commit()
        conn.close()

        return redirect('alerts_page')

    return render_template('alerts.html')
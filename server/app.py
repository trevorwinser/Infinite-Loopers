from routing import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)









# from flask import Blueprint, render_template
# import os
# from .. import sqlite_setup

# main_bp = Blueprint('main', __name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# sqlite_setup.main()

# @main_bp.route('/')
# def home():
#     return 'Welcome to the Home Page'

# @main_bp.route('/registration')
# def registration():
#     return render_template('registration/registration.html')

# @main_bp.route('/createAccount')
# def createAcc():
#     return render_template('registration/accountCreation.html')

# @main_bp.route('/user-dashboard')
# def user_dashboard():
#     return render_template('user-dashboard.html')



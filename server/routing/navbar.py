from flask import Blueprint, render_template, request
import os

navbar_bp = Blueprint('navbar', __name__, template_folder="../templates", static_folder="../static")

@navbar_bp.route('/navbar')
def navbar():
    return render_template('navbar.html')
from flask import Blueprint, render_template, request
import os
import sqlite3

mapfilter_bp = Blueprint('mapfilter', __name__, template_folder="../templates", static_folder="../static")

@mapfilter_bp.route('/map-filter')
def mapfilter():
    return render_template('mapfilter-temp/mapfilter.html')

@mapfilter_bp.route('/map-filter-data')
def mapfilterData():         
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
        
    try:
        sql = buildSQL()
        cursor.execute(sql)
        rows = cursor.fetchall()
        data = [{'latitude': row[0], 'longitude': row[1], 'humidity': row[2]} for row in rows]
        return data, 200

    except sqlite3.Error as e:
        return f"Error {e} fetching filtered data from database", 500
    except Exception as e:
        return f"Error {e} fetching filtered data from database", 500
    finally:
        conn.close()
    
def buildSQL():
    sql = "SELECT latitude, longitude, temp FROM Data"
    month = request.args.get('month')
    year = request.args.get('year')
    min_temperature = request.args.get('minTemperature')
    max_temperature = request.args.get('maxTemperature')
    if(month and year):
        sql += " WHERE month = " + month + " AND year = " + year
    if(min_temperature and max_temperature):
        if(month and year):
            sql += " AND "
        else:
            sql += " WHERE "
        sql += "temp BETWEEN " + min_temperature + " AND " + max_temperature
    return sql
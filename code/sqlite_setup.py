import sqlite3
import csv

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Data;")
    cursor.execute("DROP TABLE IF EXISTS Alerts;")
    cursor.execute("DROP TABLE IF EXISTS User;")
    cursor.execute("DROP TABLE IF EXISTS Account;")
    cursor.execute("DROP TABLE IF EXISTS user;")
    cursor.execute("DROP TABLE IF EXISTS new_table;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Data (
            obs INTEGER,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            date INTEGER,
            latitude REAL,
            longitude REAL,
            zon_winds REAL,
            mer_winds REAL,
            humidity REAL,
            air REAL,
            temp REAL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alert ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            date DATE NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            alerts TINYINT(1) NOT NULL,
            dateCreated DATE NOT NULL,
            isAdmin TINYINT(1) NOT NULL
        );
    ''')

    conn.commit()

def import_csv_to_table(conn, csv_file_path):
    cursor = conn.cursor()

    try:
        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # Skip the header row
            next(csv_reader, None)

            # Insert data into the table
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO Data
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                ''', row)
                
        conn.commit()
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"Error: {e}")
        
def create_users(conn):
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO User (username, password, email, alerts, dateCreated, isAdmin)
        VALUES ("Admin1", "Password1", "admin@gmail.com", 1, "2024-03-10", 1)
    ''')

    cursor.execute('''
        INSERT INTO User (username, password, email, alerts, dateCreated, isAdmin)
        VALUES ("User1", "Password1", "user@gmail.com", 1, "2024-03-10", 0)
    ''')

def main():

    conn = sqlite3.connect('hurriscan.db')

    csv_file_path = 'data/cleaned_data.csv'

    create_table(conn)

    import_csv_to_table(conn, csv_file_path)

    create_users(conn)

    cursor = conn.cursor()

    # print("Data in the database:")
    # cursor.execute("SELECT * FROM Data;")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

    print("\nTotal rows in the Data table:")
    cursor.execute("SELECT COUNT(*) FROM Data;")
    total_rows = cursor.fetchall()
    for row in total_rows:
        print(row[0])

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nTables:")
    for table in tables:
        print(table[0])

    print("\nUsers:")
    cursor.execute("SELECT username FROM User;")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])

    conn.close()

if __name__ == "__main__":
    main()
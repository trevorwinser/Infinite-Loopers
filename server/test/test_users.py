import unittest
from flask_testing import TestCase
from server.app import app 
import sqlite3
from sqlite_setup import create_table, create_users, main

class TestAlertsPage(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.conn = sqlite3.connect('hurriscan.db')
        create_table(self.conn)
        create_users(self.conn) 
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def testPost(self):
        response = self.client.post('/alerts', data={
            'phone': '0987654321',
            'email': 'user1@test.com',
            'east-coast': 'on',
            'west-coast': ''
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        self.cursor.execute('SELECT * FROM User WHERE username = "User1";')
        user = self.cursor.fetchone()

        self.assertEqual(user[4], '0987654321') 
        self.assertEqual(user[3], 'user1@test.com') 
        self.assertEqual(user[6], 1)  
        self.assertEqual(user[7], 1)  
        self.assertEqual(user[5], 'east')  

if __name__ == '__main__':
    unittest.main()
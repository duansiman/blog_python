#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

class DBManager:

    username = 'root'
    password = '123456'
    database = 'blog'
    host = 'localhost'

    def connect(self):
    	config = {
    		'user':DBManager.username,
    		'password':DBManager.password,
    		'host':DBManager.host,
            'database':DBManager.database
    	}

    	try:
    		cnx = mysql.connector.connect(**config)
    		return cnx
    	except mysql.connector.Error as err:
		if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
			print "The credentials you provided are not correct."
		elif (err.errno == errorcode.ER_BAD_DB_ERROR):
			print "The database you provided does not exist."
		else:
			print "Something went wrong: " , err
		return None

    def execute(self, sql, data):
        connection = self.connect()
        if not connection:
            return False

        cur = connection.cursor()
        try:
            cur.execute(sql, data)
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print ("An error occured: {}".format(err))
            return False

				
		
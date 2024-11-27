import psycopg2
import os
from kipeez.services.db.pool import pool
import pandas as pd
""" Return sql queries to setup the db"""


class Setup_Helper:
    @classmethod
    def get_file_content(cls, file_name):
        """ Read a file in the current dir"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, 'r') as file:
            sql_script = file.read()
        return sql_script

def setup_users():
    """ Returns the sql statement to setup the users table and the associated view"""
    query = Setup_Helper.get_file_content("definitions/users.sql") 
    query += f""";
    INSERT INTO users
        (email, first_name, last_name, hashed_password)
        VALUES
        ('hire@kipeez.com','Hire','Me','----');
    """
    return query


def setup_organisations():
    """ Returns the sql statement to setup the organisations table"""
    query = Setup_Helper.get_file_content("definitions/organisations.sql")
    return query



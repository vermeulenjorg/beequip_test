import psycopg2

from database import getconnection

def test_connection_class():
    """
    test to see the class type
    """
    assert type(getconnection()) ==  psycopg2.extensions.connection
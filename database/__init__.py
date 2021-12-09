import psycopg2

host = "beequipdatabase.postgres.database.azure.com"
dbname = "beequip_test"
user = "general_user"
password = "xBP<`gR/2TV2BF)*"
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

def getconnection():
    conn = psycopg2.connect(conn_string)
    return conn

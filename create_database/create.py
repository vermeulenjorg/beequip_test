from database import getconnection
import csv


def readfile(filename):
    """
    This function can read the given .CSV files and skips the first header which is added hard coded
    :param filename: The path and filename of the readable .csv file
    :return: A list of all rows in the csv file
    """
    with open(filename, newline='', ) as f:
        next(f)
        reader = csv.reader(f)
        data = list(reader)
    return data


def build_table(table, columns_to_create):
    """
    This function (re)creates a table in the connected database.
    :param table: The name of the table to be created
    :param columns_to_create: The columns of the to be created table
    """
    query_build_string = 'CREATE TABLE {0} ('.format(table)
    for key, value in columns_to_create.items():
        query_build_string = query_build_string + '{0} {1},'.format(key, value)
    query_build_string = query_build_string[:-1] + ');'
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS {0};'.format(table))
        print("Finished dropping table (if existed)")
        cursor.execute(query_build_string)
        print("Finished creating table")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


def load_data(table, data, columns):
    """
    This function loads data from a list to any given table using a specified column schema
    :param table: The tablename where data should be stored into
    :param data: The list of data to be stored
    :param columns: The predifined columns of the table
    """
    column_names = ''
    parameters = ''
    for i in range(len(columns)):
        if i == 0:
            parameters = parameters + '%s'
            column_names = str(list(columns.keys())[i])
        else:
            parameters = parameters + ',%s'
            column_names = column_names + ', ' + str(list(columns.keys())[i])
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO {0} ({1}) VALUES ({2});".format(table, column_names, parameters), data)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)



def create_customer():
    """
    This function reads customer data, (re)creates the needed table and stores this data in the table
    """
    table = 'Customer'
    file = '../data/customers.csv'
    data = readfile(file)
    columns_to_create = {'id': 'integer PRIMARY KEY', 'coc_number': 'integer', 'name': 'VARCHAR(255)'}
    build_table(table=table, columns_to_create=columns_to_create)
    load_data(table=table, data=data, columns=columns_to_create)


def create_lease():
    """
    This function reads lease data, (re)creates the needed table and stores this data in the table
    """
    table = 'Lease'
    file = '../data/leases.csv'
    data = readfile(file)
    columns_to_create = {'id': 'integer PRIMARY KEY', 'customer_id': 'integer', 'reference': 'VARCHAR(255)', 'installment_no': 'CHAR(8)', 'lane': 'VARCHAR(255)'
                         , 'team': 'VARCHAR(255)', 'object_brand': 'VARCHAR(255)', 'object_type': 'VARCHAR(255)'}
    build_table(table=table, columns_to_create=columns_to_create)
    load_data(table=table, data=data, columns=columns_to_create)


def create_installment():
    """
    This function reads installment data, (re)creates the needed table and stores this data in the table. It also creates a new unique identifier based on installment_no and t
    """
    table = 'Installment'
    file = '../data/installments.csv'
    data = readfile(file)
    for item in data:
        item.insert(0, str(item[0]) +  str(item[1]))
    columns_to_create = {'id': 'VARCHAR(255) PRIMARY KEY', 'installment_no': 'CHAR(8)', 't': 'integer', 'date': 'timestamp', 'installment': 'float', 'principal': 'float', 'interest': 'float', 'outstanding': 'float'}
    build_table(table=table, columns_to_create=columns_to_create)
    load_data(table=table, data=data, columns=columns_to_create)


if __name__ == "__main__":
    create_customer()
    create_lease()
    create_installment()
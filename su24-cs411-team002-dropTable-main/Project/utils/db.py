from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import os

def connect_db():
    try:
        ip_type = IPTypes.PUBLIC
        connector = Connector(ip_type)

        connection = connector.connect(
            'cs411-db-429518:us-central1:pt1',
            'pymysql',
            user='root',
            password='5GzZuBg^4P#D$5',
            database='processors',
        )

        print(f'Connection to database was successful! {connection}')

        return connection

    except Exception as e:
        print(f'Could not connect to database: {e}')

def execute_query(query, params=None):
    connection = connect_db()
    with connection.cursor() as cursor:
        if params is not None and not isinstance(params, (tuple, list)):
            params = (params,)
        cursor.execute(query, params)
        connection.commit()
        result = cursor.fetchall()
    connection.close()
    return result

def execute_query_file(filename, params=None):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'queries', filename + '.sql')
    with open(filename, 'r') as file:
        query = file.read()

    result = execute_query(query, params)
    return result

def check_credentials(username, password):
    query = "SELECT * FROM Person WHERE Username = %s AND Password = MD5(%s)"
    result = execute_query(query, (username, password))
    return len(result) > 0

def check_username(username):
    query = "SELECT * FROM Person WHERE Username = %s"
    result = execute_query(query, (username))
    return len(result) == 0

def get_budget(username):
    query = "SELECT ROUND(Budget, 2) FROM Person WHERE Username = %s"
    result = execute_query(query, (username))
    return result[0][0]

def register_user(username, budget, date, birthdate, password):
    query = "INSERT INTO Person VALUES(%s,%s,%s,%s,MD5(%s))"
    execute_query(query, (username, budget, date, birthdate, password))
    return 0

def create_new_cart(username, cart_name):
    query = "INSERT INTO Cart(GPUName, CPUName, Creator, Notes, CreationDate, LastModified, Title) VALUES (NULL, NULL, %s, NULL, CURDATE(), NOW(), %s)"
    execute_query(query, (username, cart_name))
    return 0

def get_cart_details(cart_id):
    query = "SELECT CartId, COALESCE(Title, 'Untitled Cart'), Creator, GPUName, CPUName, Notes, CreationDate, LastModified FROM Cart WHERE CartId = %s"
    result = execute_query(query, (cart_id))
    return result[0]

def update_cart_notes(cart_id, notes):
    query = "UPDATE Cart SET Notes = %s, LastModified = NOW() WHERE CartId = %s"
    result = execute_query(query, (notes, cart_id))
    return 0

def get_user_permission(cart_id, username):
    query = "SELECT Scope FROM Permission WHERE CartId = %s AND Username = %s ORDER BY TimeAdded DESC LIMIT 1"
    result = execute_query(query, (cart_id, username))
    return result[0][0]

def get_most_expensive_products():
    query = "SELECT p.ProductName, p.Brand, p.Cost, p.ReleaseYear FROM (SELECT ProductName, Brand, Cost, ReleaseYear FROM CPU UNION SELECT ProductName, Brand, Cost, ReleaseYear FROM GPU) AS p WHERE p.ReleaseYear >= 2023 ORDER BY p.Cost DESC LIMIT 15"
    result = execute_query(query)
    return 0

def get_cpus():
    query = "SELECT Brand, ProductName, ROUND(Cost, 2), ReleaseYear, BaseFreq_GHz, TurboFreq_GHz, Cores, Threads FROM CPU"
    result = execute_query(query)
    return result

def get_gpus():
    query = "SELECT Brand, ProductName, ROUND(Cost, 2), ReleaseYear, BaseFreq_MHz, MemorySize_GB, MemClock_MHz FROM GPU"
    result = execute_query(query)
    return result

def get_trending_cpus():
    query = "SELECT Brand, ProductName FROM TrendingCPUs"
    result = execute_query(query)
    return result

def get_trending_gpus():
    query = "SELECT Brand, ProductName FROM TrendingGPUs"
    result = execute_query(query)
    return result

def set_cpu(cart_id, cpu_name):
    query = "UPDATE Cart SET CPUName = %s, LastModified = NOW() WHERE CartId = %s"
    result = execute_query(query, (cpu_name, cart_id))
    return 0

def set_gpu(cart_id, gpu_name):
    query = "UPDATE Cart SET GPUName = %s, LastModified = NOW() WHERE CartId = %s"
    result = execute_query(query, (gpu_name, cart_id))
    return 0

def remove_cpu(cart_id):
    query = "UPDATE Cart SET CPUName = NULL, LastModified = NOW() WHERE CartId = %s"
    result = execute_query(query, (cart_id))
    return 0

def remove_gpu(cart_id):
    query = "UPDATE Cart SET GPUName = NULL, LastModified = NOW() WHERE CartId = %s"
    result = execute_query(query, (cart_id))
    return 0

def remove_cart(cart_id):
    query = "DELETE FROM Permission WHERE CartId = %s"
    result = execute_query(query, (cart_id))
    return 0

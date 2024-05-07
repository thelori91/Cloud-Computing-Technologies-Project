from flask import Flask, request, render_template
import psycopg2
import os
import ec2_metadata
application = Flask(__name__)

username = os.environ.get('RDS_USERNAME')
password = os.environ.get('RDS_PASSWORD')
host = os.environ.get('RDS_HOSTNAME')
port = os.environ.get('RDS_PORT')
database = os.environ.get('RDS_DB_NAME')
print(f"Current instance ID: {ec2_metadata.ec2_metadata.instance_id}")

print(f"Using environment variables: {username is not None and password is not None and host is not None and port is not None and database is not None}")

# Construct the connection string
conn_string = f"dbname={database} user={username} password={password} host={host} port={port}"

try:
    # Connect to the RDS instance
    conn = psycopg2.connect(conn_string)
    print("Connection established successfully!")

    # Create table 'numbers' if it doesn't exist (assuming table name)
    with conn.cursor() as cursor:
        sql = """CREATE TABLE IF NOT EXISTS numbers (
                id SERIAL PRIMARY KEY,
                number INTEGER NOT NULL
            );"""
        cursor.execute(sql)
    conn.commit()

    @application.route('/', methods=['GET', 'POST'])
    def index():        
        if request.method == 'POST':
            action = request.form['action']
            if action == 'insert':
                number = request.form['number']
                if number == 404:  # Simulate an error condition
                    raise SystemExit("Crashing to test instance restart!")
                insert_number(number)
            elif action == 'erase':
                erase_numbers()
            return render_template('index.html', numbers=None, show_numbers=False, instance_id=ec2_metadata.ec2_metadata.instance_id)
        elif request.method == 'GET':
            numbers = fetch_numbers()
            return render_template('index.html', numbers=numbers, show_numbers=True, instance_id=ec2_metadata.ec2_metadata.instance_id)
        else:
            return render_template('index.html', numbers=None, show_numbers=False,instance_id=ec2_metadata.ec2_metadata.instance_id)

    def insert_number(number):
        with conn.cursor() as cursor:
            sql = "INSERT INTO numbers (number) VALUES (%s)"
            cursor.execute(sql, (number,))
        conn.commit()

    def fetch_numbers():
        with conn.cursor() as cursor:
            sql = "SELECT * FROM numbers"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    def erase_numbers():
        with conn.cursor() as cursor:
            sql = "DELETE FROM numbers"
            cursor.execute(sql)
        conn.commit()

except Exception as e:
    print("Connection failed!")
    print(f"Error: {e}")

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)

# Fault tolerance
# Scalability and Realability
# Sicurezza
# Clustering
# Rilevamento dei guasti e ripristino automatico
 
# Amazon RDS: https://aws.amazon.com/rds/ per un database gestito altamente scalabile.
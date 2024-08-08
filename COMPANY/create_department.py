import os
import pandas as pd
import mysql.connector

# MySQL database configuration
db_config = {
    'user': 'cxm1569',
    'password': 'Samatha12345',
    'host': 'acadmysqldb001p.uta.edu',  # Update with the correct host
    'database': 'cxm1569'
}

# File names and corresponding table names
file_table_mapping = {
    'department': 'DEPARTMENT.csv',
    'dependent': 'DEPENDENT.csv',
    'dept_locations': 'DEPT_LOCATIONS.csv',
    'employee': 'EMPLOYEE.csv',
    'project': 'PROJECT.csv',
    'works_on': 'WORKS_ON.csv'
}


def insert_data_into_table(cursor, df, table_name):
    try:
        print(f'Table name: {table_name}')
        for index, row in df.iterrows():
            values = [str(col).replace("'", "").replace('"', '').strip() if type(col) == str else col for col in row]
            # Convert the date to the 'YYYY-MM-DD' format
            formatted_date = pd.to_datetime(values[3]).strftime('%Y-%m-%d')
            sql_query = f"INSERT INTO {table_name} (Dname, Dnumber, Mgr_ssn, Mgr_start_date) " \
                        f"VALUES ('{values[0]}', {int(values[1])}, '{values[2]}', '{formatted_date}');"
            try:
                cursor.execute(sql_query)
                print('Success:', sql_query)
            except Exception as insertion_error:
                print('Error:', str(insertion_error), 'for query:', sql_query)
        print(f'Data inserted successfully into {table_name}.\n')
    except Exception as e:
        print('Error:', e)




# Load department data from the CSV file
department_csv_path = file_table_mapping['department']
department_df = pd.read_csv(department_csv_path, header=None)

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    insert_data_into_table(cursor, department_df, 'department')

    connection.commit()
    print('Data insertion completed.')

except mysql.connector.Error as err:
    print('MySQL Error:', err)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print('Database connection closed.')

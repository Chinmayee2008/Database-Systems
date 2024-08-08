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

def insert_data_into_project(cursor, df, table_name):
    try:
        print(f'Table name: {table_name}')
        for index, row in df.iterrows():
            # Clean and process data
            values = [str(col).replace("'", "").replace('"', '').strip() if type(col) == str else col for col in row]
            
            # Modify this part based on the structure of the table
            pname = values[0]
            pnumber = int(values[1])
            plocation = values[2]
            dnum = int(values[3])

            # SQL query for PROJECT table
            sql_query = f"INSERT INTO {table_name} (Pname, Pnumber, Plocation, Dnum) " \
                        f"VALUES ('{pname}', {pnumber}, '{plocation}', {dnum});"

            try:
                cursor.execute(sql_query)
                print('Success:', sql_query)
            except Exception as insertion_error:
                print('Error:', str(insertion_error), 'for query:', sql_query)

        print(f'Data inserted successfully into {table_name}.\n')
    except Exception as e:
        print('Error:', e)


# Load project data from the CSV file
project_csv_path = file_table_mapping['project']
project_df = pd.read_csv(project_csv_path, header=None)

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Call the function to insert data into PROJECT table
    insert_data_into_project(cursor, project_df, 'PROJECT')

    connection.commit()
    print('Data insertion completed.')

except mysql.connector.Error as err:
    print('MySQL Error:', err)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print('Database connection closed.')

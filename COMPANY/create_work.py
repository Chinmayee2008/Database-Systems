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

def insert_data_into_works_on(cursor, df, table_name):
    try:
        print(f'Table name: {table_name}')
        for index, row in df.iterrows():
            # Clean and process data
            values = [str(col).replace("'", "").replace('"', '').strip() if type(col) == str else col for col in row]
            
            # Modify this part based on the structure of the table
            essn = values[0]
            pno = int(values[1])
            hours = float(values[2])

            # SQL query for WORKS_ON table
            sql_query = f"INSERT INTO {table_name} (Essn, Pno, Hours) " \
                        f"VALUES ('{essn}', {pno}, {hours});"

            try:
                cursor.execute(sql_query)
                print('Success:', sql_query)
            except Exception as insertion_error:
                print('Error:', str(insertion_error), 'for query:', sql_query)

        print(f'Data inserted successfully into {table_name}.\n')
    except Exception as e:
        print('Error:', e)


# Load works_on data from the CSV file
works_on_csv_path = file_table_mapping['works_on']
works_on_df = pd.read_csv(works_on_csv_path, header=None)

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Call the function to insert data into WORKS_ON table
    insert_data_into_works_on(cursor, works_on_df, 'WORKS_ON')

    connection.commit()
    print('Data insertion completed.')

except mysql.connector.Error as err:
    print('MySQL Error:', err)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print('Database connection closed.')

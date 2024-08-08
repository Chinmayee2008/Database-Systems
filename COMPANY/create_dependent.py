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

def insert_data_into_dependent(cursor, df, table_name):
    try:
        print(f'Table name: {table_name}')
        for index, row in df.iterrows():
            # Clean and process data
            values = [str(col).replace("'", "").replace('"', '').strip() if type(col) == str else col for col in row]
            
            # Modify this part based on the structure of the table
            essn = values[0]
            dependent_name = values[1]
            sex = values[2]
            bdate = values[3]
            relationship = values[4]

            # Update the STR_TO_DATE format to match your date format in the CSV
            sql_query = f"INSERT INTO {table_name} (Essn, Dependent_name, Sex, Bdate, Relationship) " \
                        f"VALUES ('{essn}', '{dependent_name}', '{sex}', STR_TO_DATE('{bdate}', '%d-%b-%Y'), '{relationship}');"

            try:
                cursor.execute(sql_query)
                print('Success:', sql_query)
            except Exception as insertion_error:
                print('Error:', str(insertion_error), 'for query:', sql_query)

        print(f'Data inserted successfully into {table_name}.\n')
    except Exception as e:
        print('Error:', e)



# Load dependent data from the CSV file
dependent_csv_path = file_table_mapping['dependent']
dependent_df = pd.read_csv(dependent_csv_path, header=None)

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Call the function to insert data into DEPENDENT table
    insert_data_into_dependent(cursor, dependent_df, 'DEPENDENT')

    connection.commit()
    print('Data insertion completed.')

except mysql.connector.Error as err:
    print('MySQL Error:', err)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print('Database connection closed.')

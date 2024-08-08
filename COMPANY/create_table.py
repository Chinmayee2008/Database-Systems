import os
import pandas as pd
import mysql.connector

# MySQL database configuration
db_config = {
    'user': 'cxm1569',
    'password': 'Samatha12345',
    'host': 'acadmysqldb001p.uta.edu',
    'database': 'cxm1569'
}

# File names and corresponding table names
file_table_mapping = {
    'department': 'DEPARTMENT.csv',  # Corrected file name for department
    'dependent': 'DEPENDENT.csv',
    'dept_locations': 'DEPT_LOCATIONS.csv',
    'employee': 'EMPLOYEE.csv',
    'project': 'PROJECT.csv',
    'works_on': 'WORKS_ON.csv'
}

# Function to clean and insert data from DataFrame into the employee table
def insert_data_into_employee(cursor, df):
    try:
        print('Table name: employee')
        for index, row in df.iterrows():
            values = [str(col).replace("'", "").replace('"', '').strip() if type(col) == str else col for col in row]
            # Address is a concatenation of columns 5, 6, and 7
            address = f"{values[5]} {values[6]} {values[7]}"
            values[5] = address
            values[6] = None  # Set to None as it's not used
            values[7] = None  # Set to None as it's not used
            sql_query = f"INSERT INTO employee (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno) " \
                        f"VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', STR_TO_DATE('{values[4]}', '%d-%b-%Y'), '{values[5]}', '{values[8]}', {values[9]}, {values[10]}, {values[11]});"
            try:
                cursor.execute(sql_query)
                print('Success:', sql_query)
            except Exception as insertion_error:
                print('Error:', str(insertion_error), 'for query:', sql_query)
        print('Data inserted successfully into employee.\n')
    except Exception as e:
        print('Error:', e)

# Load employee data from the CSV file
employee_csv_path = file_table_mapping['employee']
employee_df = pd.read_csv(employee_csv_path, header=None)

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Call the function to insert data into the EMPLOYEE table
    insert_data_into_employee(cursor, employee_df)

    connection.commit()
    print('Data insertion completed.')

except mysql.connector.Error as err:
    print('MySQL Error:', err)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print('Database connection closed.')

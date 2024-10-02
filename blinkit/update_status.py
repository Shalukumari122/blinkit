import mysql.connector
from mysql.connector import Error

def update_status_in_mysql(old_status, new_status):
    connection = None  # Initialize connection to None
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',  # e.g., 'localhost' or your DB server
            database='zepto',  # Name of your database
            user='root',  # Your MySQL username
            password='actowiz'  # Your MySQL password
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Define the SQL query to update the status
            sql_update_query = """UPDATE blinkit_lat_long_roshi SET Status = %s WHERE Status = %s"""

            # Execute the query with the provided data
            cursor.execute(sql_update_query, (new_status, old_status))

            # Commit the transaction to the database
            connection.commit()

            print(f"Records with status '{old_status}' successfully updated to '{new_status}'.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        # Close the database connection if it was established
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

# Example usage:
old_status = 'Done'
new_status = 'pending'
update_status_in_mysql(old_status, new_status)

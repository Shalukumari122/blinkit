import os
from datetime import datetime, timedelta

import pandas as pd
import pymysql

# Connect to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='actowiz',
    database='zepto'
)
# query ='select `id`,`pincode`,`lat`,`long`,`serviceable` from blinkit_lat_long_comp'
query ='select `url`,`brand` from blinkit_link_pids_comp'
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

output_file_path = fr'C:\\Users\\shalu.kumari\\PycharmProjects\\pythonProject\\blinkit\\input\\blinkit_link_pids_comp.xlsx'

# Create the directory if it does not exist
df.to_excel(output_file_path, index=False)
print(f"Data has been exported to {output_file_path}")



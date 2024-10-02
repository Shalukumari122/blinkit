import pandas as pd
import sqlalchemy
import pymysql

file_name = r"C:\Users\shalu.kumari\Desktop\blinkit_roshi_pincode.xlsx"
df = pd.read_excel(file_name)
mydb = pymysql.connect(host="localhost", user="root", password="actowiz", database="blinkit_db")
cur = mydb.cursor()
table_name = "blinkit_links_pids_comp"
db_conn = sqlalchemy.create_engine("mysql+pymysql://root:actowiz@localhost/blinkit_db")
df.to_sql(table_name, con=db_conn, if_exists='replace', index=False)
mydb.commit()
print("file inserted to data base")



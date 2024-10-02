import pandas as pd
from sqlalchemy import create_engine

# Load data from both Excel files
df1 = pd.read_excel('blinkit_link_pids_roshi.xlsx')  # First file with pincode, area, city, store_id
df2 = pd.read_excel('blinkit_lat_long_roshi.xlsx')  # Second file with Id, brand_name, sku_name, product_name, etc.

# Clean up column names by stripping spaces and converting to lowercase
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Preview the column names and data to ensure they match
print("Columns in df1:", df1.columns)
print("Columns in df2:", df2.columns)
print(df1.head())  # Check first few rows of df1
print(df2.head())  # Check first few rows of df2

# Initialize an empty DataFrame for the master table
blinkit_links_roshi = pd.DataFrame()

# Iterate through each row of the first DataFrame
for index, row in df2.iterrows():
    # Extract relevant data from the first file (df1)

    pincode = row.get('pincode', 'NA')
    lat = row.get('lat', 'NA')
    long = row.get('long', 'NA') # Use 'NA' if the column is missing
    serviceable = row.get('serviceable', 'NA')
    # Check if pincode, area, city, and store_id are being accessed correctly
    print(f"Processing row {index} from df1: {pincode}, {lat}, {long}, {serviceable}")

    # Iterate through the second DataFrame
    for i, product_row in df1.iterrows():
        # Combine the current row from df1 and df2
        combined_data = {
            'pincode': pincode,
            'lat':lat,
            'long':long,
            'serviceable':serviceable,
            'Roshi Wellness SKUs - as Named in Blinkit':product_row.get('Roshi Wellness SKUs - as Named in Blinkit','NA'),
            'url': product_row.get('url', 'NA')

        }

        # Check the combined row before adding it
        print(f"Combined data row {i}: {combined_data}")

        # Convert the dictionary to a DataFrame and concatenate with the master table
        blinkit_links_roshi = pd.concat([blinkit_links_roshi, pd.DataFrame([combined_data])], ignore_index=True)

# SQL database connection setup
engine = create_engine('mysql+pymysql://root:actowiz@localhost/blinkit_db')

# Store the master table into SQL
blinkit_links_roshi.to_sql('blinkit_links_roshi', con=engine, if_exists='replace', index=False)

print("Data successfully inserted into SQL!")

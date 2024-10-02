import os
from datetime import datetime, date


# Function to check if today is Sunday
def is_sunday():
    return datetime.today().weekday() == 6 # Sunday is represented by 6

# Function to create a directory if it's Sunday
def create_directory_if_sunday(directory_name):
    if is_sunday():
        # Check if the directory already exists
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            print(f"Directory '{directory_name}' created.")
        else:
            print(f"Directory '{directory_name}' already exists.")
    else:
        print("Today is not Sunday. No directory created.")

# Set the directory name
today_date = str(date.today()).replace('-', '_')
folder_loc = f'C:/paga_save/live_project/blinkit_weekly/roshi/{today_date}'

directory_name = folder_loc

# Run the function
create_directory_if_sunday(directory_name)




from sqlalchemy import create_engine, inspect
import os

# Create an engine (connect to your SQLite database)
# You can replace the database URL with your environment variable or path to the database
DATABASE_URL = 'sqlite:///instance/app.db'
  # Replace with actual URL if necessary
engine = create_engine(DATABASE_URL)


# Create an inspector to inspect the database
inspector = inspect(engine)

# Get the list of tables in the database
tables = inspector.get_table_names()

# Print the tables in the database
print("Tables in the database:", tables)

# Check if the 'users' table exists
if 'users' in tables:
    print("The 'users' table exists.")
else:
    print("The 'users' table does not exist.")

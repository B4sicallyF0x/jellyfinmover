import sqlite3

# load database
db_file = 'library.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# define paths to replace
path_replacements = {
    'Z:\\Anime\\': 'D:\\Media\\Anime\\',
    'Z:\\Movies\\': 'D:\\Media\\Movies\\',
    'Z:\\TV_Shows\\': 'D:\\Media\\TV_Shows\\'
}

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    for column in columns:
        column_name = column[1]
        
        cursor.execute(f"SELECT {column_name} FROM {table_name};")
        rows = cursor.fetchall()
        
        for row in rows:
            value = row[0]
            if value:
                # ensure the value is a string
                if isinstance(value, bytes):
                    value = value.decode('utf-8', errors='ignore')  

                if isinstance(value, str): 
                    # replace paths
                    new_value = value
                    for old_path, new_path in path_replacements.items():
                        new_value = new_value.replace(old_path, new_path)
                    
                    # if the value was modified, update the database
                    if new_value != value:
                        cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {column_name} = ?",
                                       (new_value, value))
                        print(f"Replaced in {table_name}, column {column_name}: {value} -> {new_value}")
                else:
                    print(f"Value is not a string in {table_name}, column {column_name}: {value}")

# commit changes and close the connection
conn.commit()
conn.close()

# 1. read the migration files in src/migrations
# 2. run the migrations using shell command

import os
import sys

# read the files in the migrations folder
files = os.listdir("src/migrations")

# read command line up or down
if len(sys.argv) > 1 and sys.argv[1] == "up":
    # run the migrations in ascending order
    files.sort()
    for file in files:
        if file != "migration_utils.py":  # don't run the migration_utils.py file
            print(file)
            # run the migration
            os.system(f"python src/migrations/{file} up")
elif len(sys.argv) > 1 and sys.argv[1] == "down":
    # run the migrations in descending order
    files.sort(reverse=True)
    for file in files:
        if file != "migration_utils.py":  # don't run the migration_utils.py file
            print(file)
            # run the migration
            os.system(f"python src/migrations/{file} down")
else:
    print("Invalid command line argument.")
    exit(1)

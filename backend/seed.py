# purpose of this file is to seed the database with dummy data
# basically to run all the fules in the database_seeder folder

import os


base_path = "database_seeder"

for i in os.listdir(base_path):
    if i == "seedAuthority.py" or i == "seedPosts.py":
        continue
    command = f"python {base_path}/{i}"
    print(f"executing {command}")
    os.system(command)

# seed authority AFTER user

command = f"python {base_path}/seedAuthority.py"
print(f"executing {command}")
os.system(command)

command = f"python {base_path}/seedPosts.py"
print(f"executing {command}")
os.system(command)

print("done seeding")

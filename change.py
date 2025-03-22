import sqlite3

conn = sqlite3.connect("instance/db.sqlite3")
cursor = conn.cursor()

# Update all users with role_id = 2 (customer) to role_id = 3 (employee)
cursor.execute("UPDATE user SET role_id = 3 WHERE role_id = 2;")

conn.commit()
print("All customers have been updated to employees.")
conn.close()

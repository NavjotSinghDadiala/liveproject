from sqlalchemy.sql import text
from app import db, app  # Ensure correct import of Flask app and db

with app.app_context():  # Ensures execution inside Flask context
    sql_query = text("""
        UPDATE hired 
        SET employee_email = 'dadialanavjotsingh@gmail.com' 
        WHERE employee_email = 'employee@example.com';
    """)

    db.session.execute(sql_query)  # Execute the query
    db.session.commit()  # Commit the changes

print("Hired table updated successfully!")

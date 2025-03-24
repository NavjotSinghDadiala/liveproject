from sqlalchemy.sql import text
from app import db, app  

with app.app_context():  # Ensures execution inside Flask context
    sql_queries = [
    text("ALTER TABLE applicants ADD COLUMN linkedin TEXT;"),
    text("ALTER TABLE applicants ADD COLUMN github_profile TEXT;"),
    text("ALTER TABLE applicants ADD COLUMN projects TEXT;"),

    text("ALTER TABLE user ADD COLUMN phone_number TEXT;"),
    text("ALTER TABLE user ADD COLUMN address TEXT;"),

    text("ALTER TABLE job ADD COLUMN salary INTEGER;"),
    text("ALTER TABLE job ADD COLUMN job_type TEXT;"),
    
    text("ALTER TABLE application ADD COLUMN interview_scheduled BOOLEAN;"),
    
    text("ALTER TABLE hired ADD COLUMN hire_date TEXT;")
]

# Execute each query
with db.engine.connect() as connection:
    for query in sql_queries:
        try:
            connection.execute(query)
            print(f"Executed: {query}")
        except Exception as e:
            print(f"Error executing {query}: {e}")

print("Columns added successfully.")
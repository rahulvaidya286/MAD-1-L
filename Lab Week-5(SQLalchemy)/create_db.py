from app import app, db, Course  # Import 'app', 'db', and 'Course' from app.py

# Create an application context
with app.app_context():
    # Initialize the database and create tables
    db.create_all()

    # Prepopulate the course table with the provided data
    courses = [
        Course(course_code="CSE01", course_name="MAD I", course_description="Modern Application Development - I"),
        Course(course_code="CSE02", course_name="DBMS", course_description="Database management Systems"),
        Course(course_code="CSE03", course_name="PDSA", course_description="Programming, Data Structures and Algorithms using Python"),
        Course(course_code="BST13", course_name="BDM", course_description="Business Data Management")
    ]

    # Add courses to the session and commit
    db.session.bulk_save_objects(courses)
    db.session.commit()

    print("Database created with tables and course data populated.")

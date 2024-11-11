from app import app, db, Course, Student, Enrollment  # Import 'app', 'db', 'Course', 'Student', and 'Enrollment' from app.py

# Create an application context
with app.app_context():
    # Initialize the database and create tables
    db.create_all()

    # Prepopulate the course table with the provided data
    course1 = Course(course_name="Introduction to Programming", course_code="CS101", course_description="Learn the basics of programming.")
    course2 = Course(course_name="Data Structures", course_code="CS102", course_description="Learn about data structures.")
    
    # Prepopulate the student table with the provided data
    student1 = Student(roll_number="S001", first_name="John", last_name="Doe")
    student2 = Student(roll_number="S002", first_name="Jane", last_name="Smith")
    
    # Prepopulate the enrollment table with the provided data
    enrollment1 = Enrollment(student_id=1, course_id=1)
    enrollment2 = Enrollment(student_id=2, course_id=2)

    # Add courses, students, and enrollments to the session
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(student1)
    db.session.add(student2)
    db.session.add(enrollment1)
    db.session.add(enrollment2)

    # Commit the session
    db.session.commit()

    print("Database created with tables and course data populated.")

from app import db, Student, Course, Enrollments, app

def init_db():
    # Drop existing tables and create new ones
    db.drop_all()
    db.create_all()
    
    # Create sample students
    students = [
        Student(roll_number="21F1001", first_name="Luke", last_name="Skywalker"),
        Student(roll_number="21F1002", first_name="Leia", last_name="Organa"),
        Student(roll_number="21F1003", first_name="Han", last_name="Solo"),
        Student(roll_number="21F1004", first_name="Padmé", last_name="Amidala"),
        Student(roll_number="21F1005", first_name="Obi-Wan", last_name="Kenobi")
    ]
    
    # Create sample courses
    courses = [
        Course(course_code="CS101", course_name="Introduction to Programming", 
               course_description="Basic programming concepts using Python"),
        Course(course_code="CS102", course_name="Data Structures", 
               course_description="Fundamental data structures and algorithms"),
        Course(course_code="CS201", course_name="Database Systems", 
               course_description="Introduction to database management systems"),
        Course(course_code="CS202", course_name="Web Development", 
               course_description="Web application development using Flask"),
        Course(course_code="CS301", course_name="Machine Learning", 
               course_description="Basic concepts of machine learning")
    ]
    
    # Add all students and courses to the session
    db.session.add_all(students)
    db.session.add_all(courses)
    db.session.commit()
    
    # Create some sample enrollments
    enrollments = [
        Enrollments(estudent_id=1, ecourse_id=1),  # CS101
        Enrollments(estudent_id=1, ecourse_id=2),  # CS102
        
        Enrollments(estudent_id=2, ecourse_id=1),  # CS101
        Enrollments(estudent_id=2, ecourse_id=3),  # CS201
        
        Enrollments(estudent_id=3, ecourse_id=2),  # CS102
        Enrollments(estudent_id=3, ecourse_id=4),  # CS202
        
        Enrollments(estudent_id=4, ecourse_id=3),  # CS201
        Enrollments(estudent_id=4, ecourse_id=5),  # CS301
        
        Enrollments(estudent_id=5, ecourse_id=1),  # CS101
        Enrollments(estudent_id=5, ecourse_id=5)   # CS301
    ]
    
    # Add all enrollments to the session
    db.session.add_all(enrollments)
    db.session.commit()
    
    print("Database initialized with sample data!")
    
    # Print summary of created data
    print("\nCreated Students:")
    for student in Student.query.all():
        print(f"- {student.roll_number}: {student.first_name} {student.last_name}")
    
    print("\nCreated Courses:")
    for course in Course.query.all():
        print(f"- {course.course_code}: {course.course_name}")
    
    print("\nCreated Enrollments:")
    for enrollment in Enrollments.query.all():
        student = Student.query.get(enrollment.estudent_id)
        course = Course.query.get(enrollment.ecourse_id)
        print(f"- {student.roll_number} enrolled in {course.course_code}")

if __name__ == "__main__":
    with app.app_context():
        init_db()
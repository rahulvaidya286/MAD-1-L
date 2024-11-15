from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week7_database.sqlite3's
app.secret_key = 'secret-key'
db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

# Course model
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

# Enrollments model
class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

# Home Page: Display students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Create student
@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form['roll']
        f_name = request.form['f_name']
        l_name = request.form['l_name']

        # Check if roll number already exists
        existing_student = Student.query.filter_by(roll_number=roll).first()
        if existing_student:
            flash('Student with this roll number already exists!')
            return redirect(url_for('index'))

        new_student = Student(roll_number=roll, first_name=f_name, last_name=l_name)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create_student.html')

# Update student
@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_student.html', student=student)

# Delete student
@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# View student details
@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get(student_id)
    enrollments = Enrollments.query.filter_by(estudent_id=student_id).all()
    return render_template('student_details.html', student=student, enrollments=enrollments)

# Courses
@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

# Create course
@app.route('/course/create', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['c_name']
        desc = request.form['desc']

        new_course = Course(course_code=code, course_name=name, course_description=desc)
        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('courses'))
    return render_template('create_course.html')

# Update course
@app.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
def update_course(course_id):
    course = Course.query.get(course_id)
    if request.method == 'POST':
        course.course_name = request.form['c_name']
        course.course_description = request.form['desc']
        db.session.commit()
        return redirect(url_for('courses'))
    return render_template('update_course.html', course=course)

# Delete course
@app.route('/course/<int:course_id>/delete')
def delete_course(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('courses'))

# Main block to run the app
if __name__ == '__main__':
    app.run(debug=True)

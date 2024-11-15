from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week7_database.sqlite3'
db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    enrollments = db.relationship('Enrollments', backref='student', lazy=True, 
                                cascade="all, delete-orphan")

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)
    enrollments = db.relationship('Enrollments', backref='course', lazy=True, 
                                cascade="all, delete-orphan")

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

# Routes for Student CRUD Operations
@app.route('/')
def index():
    students = Student.query.order_by(Student.roll_number).all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form['roll']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        
        # Check if student already exists
        existing_student = Student.query.filter_by(roll_number=roll).first()
        if existing_student:
            return render_template('student_exists.html', roll_number=roll)
        
        new_student = Student(roll_number=roll, first_name=f_name, last_name=l_name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('create_student.html')

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    courses = Course.query.all()
    
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        
        # Handle new enrollment
        course_id = request.form['course']
        if course_id:
            new_enrollment = Enrollments(estudent_id=student_id, ecourse_id=course_id)
            db.session.add(new_enrollment)
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('update_student.html', student=student, courses=courses)

@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_detail.html', student=student)

@app.route('/student/<int:student_id>/withdraw/<int:course_id>')
def withdraw_course(student_id, course_id):
    enrollment = Enrollments.query.filter_by(estudent_id=student_id, ecourse_id=course_id).first()
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
    return redirect(url_for('index'))

# Routes for Course CRUD Operations
@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/course/create', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        code = request.form['code']
        c_name = request.form['c_name']
        desc = request.form['desc']
        
        # Check if course already exists
        existing_course = Course.query.filter_by(course_code=code).first()
        if existing_course:
            return render_template('course_exists.html', course_code=code)
        
        new_course = Course(course_code=code, course_name=c_name, course_description=desc)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('courses'))
    
    return render_template('create_course.html')

@app.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        course.course_name = request.form['c_name']
        course.course_description = request.form['desc']
        db.session.commit()
        return redirect(url_for('courses'))
    
    return render_template('update_course.html', course=course)

@app.route('/course/<int:course_id>/delete')
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('courses'))

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
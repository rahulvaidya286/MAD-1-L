from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

# Routes
@app.route('/', methods=['GET'])
def home():
    students = Student.query.all()
    if students:
        return render_template('index.html', students=students)
    else:
        return render_template('index_alt.html')

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        roll_number = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        courses = request.form.getlist('courses')
        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student:
            return render_template('exists.html', roll_number=roll_number)
        else:
            new_student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
            db.session.add(new_student)
            db.session.commit()
            for course_code in courses:
                course = Course.query.filter_by(course_code=course_code).first()
                if course:
                    enrollment = Enrollment(estudent_id=new_student.student_id, ecourse_id=course.course_id)
                    db.session.add(enrollment)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        return render_template('error.html')
    
@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    if request.method == 'GET':
        student = Student.query.filter_by(student_id=student_id).first()
        return render_template('update.html', student=student)
    elif request.method == 'POST':
        student = Student.query.filter_by(student_id=student_id).first()
        if student:
            student.first_name = request.form['f_name']
            student.last_name = request.form['l_name']
            courses = request.form.getlist('courses')
            
            # Clear existing enrollments
            Enrollment.query.filter_by(estudent_id=student_id).delete()
            
            # Add new enrollments
            for course_code in courses:
                course = Course.query.filter_by(course_code=course_code).first()
                if course:
                    enrollment = Enrollment(estudent_id=student.student_id, ecourse_id=course.course_id)
                    db.session.add(enrollment)
            
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('error.html')

@app.route('/student/<int:student_id>/delete', methods=['GET'])
def delete_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('error.html')
    
if __name__ == '__main__':
    app.run(debug=True)

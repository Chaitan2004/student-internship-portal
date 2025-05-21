from flask import Flask, render_template, request, redirect, url_for, session, send_file,jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from datetime import datetime, date
import os
from io import BytesIO
from flask_cors import CORS
import time
import random
import webbrowser
from threading import Timer
import pandas as pd
from flask import send_file
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/studentinternportal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)  # Enable CORS for all routes



db = SQLAlchemy(app)


class StudentData(db.Model):
    __tablename__ = 'student_data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    course = db.Column(db.String(255), nullable=True)
    branch = db.Column(db.String(255), nullable=True)
    institute_name = db.Column(db.String(255), nullable=True)
    project_domain = db.Column(db.String(255), nullable=True)
    project_title = db.Column(db.String(255), nullable=True)
    date_mentacc = db.Column(db.Date, nullable=True)
    dob = db.Column(db.Date, nullable=True)
    guardian_name = db.Column(db.String(255), nullable=True)
    guardian_designation = db.Column(db.String(255), nullable=True)
    guardian_phn_no = db.Column(db.String(25), nullable=True)
    employee_code_no = db.Column(db.String(50), nullable=True)
    year_of_study = db.Column(db.String(20), nullable=True)
    institute_address = db.Column(db.String(255), nullable=True)
    permanent_address = db.Column(db.String(255), nullable=True)
    local_address = db.Column(db.String(255), nullable=True)
    phn_no = db.Column(db.String(30), nullable=True)
    alternate_phn_no = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    alternate_email = db.Column(db.String(255), nullable=True)
    project_group = db.Column(db.String(255), nullable=True)
    training_from_date = db.Column(db.Date, nullable=True)
    training_to_date = db.Column(db.Date, nullable=True)
    bank_name = db.Column(db.String(255), nullable=True)
    dd_no = db.Column(db.String(255), nullable=True)
    date_of_dd = db.Column(db.Date, nullable=True)
    date_of_dd2 = db.Column(db.Date, nullable=True)
    amount = db.Column(db.String(255), nullable=True)
    designation_english = db.Column(db.String(255), nullable=True)
    designation_hindi = db.Column(db.String(255), nullable=True)
    incharge_english = db.Column(db.String(255), nullable=True)
    incharge_hindi = db.Column(db.String(255), nullable=True)
    conduct = db.Column(db.String(255), nullable=True)
    ref_no = db.Column(db.String(100), nullable=True)
    file_data = db.Column(db.LargeBinary, nullable=True)
    certificate = db.Column(db.String(255), nullable=True)
    guide_name = db.Column(db.String(255), nullable=True)
    submission_id = db.Column(db.String(36), nullable=False)
    joiningfile = db.Column(db.LargeBinary, nullable=True)
    dateofjoining= db.Column(db.Date, nullable=True)
    nodues_file= db.Column(db.LargeBinary, nullable=True)
    attendance=db.Column(db.String(255), nullable=True)
    projectdetails = db.Column(db.String(1000), nullable=True)
    idc=db.Column(db.String(255), nullable=True)
    gender=db.Column(db.String(100), nullable=True)
    mark=db.Column(db.String(100), nullable=True)
    photo = db.Column(db.LargeBinary)  # Store image binary data
    certificatecollectiondate = db.Column(db.Date)







class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)

@app.route('/')
def index():
    error = request.args.get('error')

    return render_template('loginsignup.html', error= error)


@app.route('/changedetails')
def change_details():
    return render_template('changedetails.html')


@app.route('/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return render_template('password_change_response.html', error='User not logged in'), 401

    current_password = request.form['current-password']
    new_password = request.form['new-password']

    user = Users.query.get(session['user_id'])

    if user.password != current_password:
        return render_template('password_change_response.html', error='Current password is incorrect'), 400

    user.password = new_password
    db.session.commit()

    return render_template('password_change_response.html', message='Password changed successfully')


@app.route('/changedetails2')
def change_details2():
    return render_template('changedetails2.html')


@app.route('/change-password2', methods=['POST'])
def change_password2():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))

    current_password = request.form['current-password']
    new_password = request.form['new-password']

    user = Users.query.get(session['user_id'])

    if user.password != current_password:
        return render_template('password_change_response2.html', error='Current password is incorrect'), 400

    user.password = new_password
    db.session.commit()

    return render_template('password_change_response2.html', message='Password changed successfully')



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = Users.query.filter_by(username=username, password=password).first()

    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        session['type'] = user.type
        if user.type == 'operator':
            return redirect(url_for('ophome'))
        elif user.type == 'admin':
            return redirect(url_for('adminhome'))
    else:
        return "Invalid credentials", 401


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/ophome')
def ophome():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    message = request.args.get('message')
    msg_type = request.args.get('msg_type')
    return render_template('ophome.html', message=message, msg_type=msg_type, type=session.get('type'), id= session.get('username') )


@app.route('/homestu')
def homestu():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    return render_template('homestu.html')


@app.route('/homestu2')
def homestu2():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    return render_template('homestu2.html')


@app.route('/mentor-acceptance-form')
def mentor_acceptance_form():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    return render_template('mentor_acceptance_form.html')


@app.route('/joining-form')
def joining_form():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    return render_template('joining_form.html')


@app.route('/no-dues-form')
def no_dues_form():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    return render_template('no_dues_form.html')


@app.route('/generate-certificate')
def generate_certificate():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    return render_template('generate_certificate.html')


@app.route('/adminhome')
def adminhome():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))

    message = request.args.get('message')
    msg_type = request.args.get('msg_type')
    return render_template('adminhome.html', message=message, msg_type=msg_type ,type=session.get('type'), id= session.get('username'))



@app.route('/print-empty-form')
def print_empty_form():
    return render_template('print_empty_form.html')


@app.route('/createuserdisplay')
def createuserdisplay():
    return render_template('createuser.html')

@app.route('/download-pdf/<int:id>')
def download_pdf(id):
    student = StudentData.query.get(id)
    if student and student.mentoracceptance:
        return send_file(BytesIO(student.mentoracceptance),
                         attachment_filename=f'{student.name}_form.pdf',
                         as_attachment=True)
    return "PDF not found", 404

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    course_details = request.form['course_details']
    branch = request.form['branch']
    institute_name = request.form['institute_name']
    project_domain = request.form['project_domain']
    project_topic = request.form['project_topic']

    new_data = StudentData(
        name=name,
        course_details=course_details,
        branch=branch,
        institute_name=institute_name,
        project_domain=project_domain,
        project_topic=project_topic
    )
    db.session.add(new_data)
    db.session.commit()
    return "Form submitted successfully"


@app.route('/createuser', methods=['GET', 'POST'])
def create_user():


    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))

    else:
        success_message = None
        error_message = None

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user_type = request.form['role']
            phone = request.form['phone']
            email = request.form['email']

            # Check if a user with the same username already exists
            existing_user = Users.query.filter_by(username=username).first()

            if existing_user:
                error_message = "This username is taken."
            else:
                # Create a new user instance
                new_user = Users(username=username, password=password, type=user_type, phone_no=phone, email=email)

                # Add the new user to the database
                db.session.add(new_user)
                db.session.commit()
                success_message = "USER SUCCESSFULLY CREATED."

        return redirect(url_for('adminhome', message=success_message or error_message, msg_type='success' if success_message else 'error'))




@app.route('/operator-details')
def operator_details():
    if 'user_id' not in session:
        return redirect(url_for('index', error="SESSION TIMED OUT"))

    operators = Users.query.filter_by(type='operator').all()
    return render_template('operator_details.html', operators=operators)

@app.route('/submitmen', methods=['POST'])
def submitmen():

    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    else:
        name = request.form.get('name')
        course = request.form.get('course')
        branch = request.form.get('branch')
        institute_name = request.form.get('institute_name')
        project_domain = request.form.get('project_domain')
        project_title = request.form.get('project_title')
        guide_name = request.form.get('guide_name')
        datetoday = date.today().strftime('%Y-%m-%d')
        file = request.files.get('fileUpload')
        phn_no= request.form.get('phone')

        print(phn_no)

        names = [n.strip() for n in name.split(',')]
        courses = [c.strip() for c in course.split(',')]
        domains = [d.strip() for d in project_domain.split(',')]
        titles = [t.strip() for t in project_title.split(',')]
        phn_nos=[p.strip() for p in phn_no.split(',')]


        if not (len(names) == len(courses) == len(domains) == len(titles) == len(phn_nos)):
            error_message = "The number of entries for each field must be equal."
            return redirect(url_for('ophome', message=error_message, msg_type='error'))

        # Generate a unique submission ID for this submission
        def generate_submission_id():
            timestamp = int(time.time() * 1000)  # Current time in milliseconds
            random_number = random.randint(1000, 9999)  # Random number between 1000 and 9999
            return f"{timestamp}-{random_number}"

        submission_id = generate_submission_id()  # Generate submission ID here

        for i in range(len(names)):
            print("entered")
            student = StudentData.query.filter_by(name=names[i], phn_no= phn_nos[i]).first()
            if student:
                print("done")
                # Update existing student record
                student.course = courses[i] if courses[i] else student.course
                student.branch = branch if branch else student.branch
                student.institute_name = institute_name if institute_name else student.institute_name
                student.project_domain = domains[i] if domains[i] else student.project_domain
                student.project_title = titles[i] if titles[i] else student.project_title
                student.guide_name = guide_name if guide_name else student.guide_name
                if file and file.filename.endswith('.pdf'):
                    student.file_data = file.read()
            else:
                print("error")
                # Create a new student record
                new_student = StudentData(
                    name=names[i],
                    course=courses[i],
                    branch=branch,
                    institute_name=institute_name,
                    project_domain=domains[i],
                    project_title=titles[i],
                    guide_name=guide_name,
                    date_mentacc=datetoday,
                    file_data=file.read() if file and file.filename.endswith('.pdf') else None,
                    submission_id=submission_id,  # Assign the common submission_id
                    phn_no= phn_nos[i]
                )
                db.session.add(new_student)

        db.session.commit()
        success_message = "Student details submitted successfully."
        return redirect(url_for('ophome', message=success_message, msg_type='success'))


@app.route('/mentoraccprint')
def mentoraccprint():
    return render_template('mentoraccprint.html')


@app.route('/view', methods=['POST'])
def get_student_details():
    print("Starting get_student_details")
    student_id = request.form.get('student_id')
    submission_date = request.form.get('date')
    phoneno= request.form.get('phn')

    session['student_id'] = student_id

    session['phoneno'] = phoneno

    query = StudentData.query.filter(
        StudentData.name == student_id,
        StudentData.phn_no == phoneno
    )

    if submission_date:  # check if submission_date is not None or not empty
        query = query.filter(StudentData.date_mentacc == submission_date)

    student = query.first()

    if student:
        print(f"Student found: {student.name}")

        # Get the submission ID
        submission_id = student.submission_id
        print(f"Submission ID for {student.name}: {submission_id}")
        all_students = StudentData.query.all()
        same_submission_students = [s for s in all_students if s.submission_id == student.submission_id]
        print(f"Found {len(all_students)}")

        print(f"SQL Query Executed: {same_submission_students}")

        if same_submission_students:
            print(f"Found {len(same_submission_students)} students with the same submission ID.")
            for s in same_submission_students:
                print(f"Student: {s.name}")
        else:
            print("No other students found with the same submission ID.")

        return render_template('view.html', student_details=same_submission_students,
                               submission_date=student.date_mentacc)

    else:
        print("No student found with the provided ID and date.")
        return render_template('view.html', student_details=[], submission_date=submission_date)


@app.route('/viewinfo')
def viewinfo():
    return render_template('viewinfo.html')
@app.route('/save-student', methods=['POST'])
def save_student():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))

    else:
        name = request.form.get('name')
        course = request.form.get('course')
        branch = request.form.get('branch')
        institute_name = request.form.get('institute_name')
        project_domain = request.form.get('project_domain')
        project_title = request.form.get('project_title')
        dob = request.form.get('dob')
        guardian_name = request.form.get('guardian_name')
        guardian_designation = request.form.get('guardian_designation')
        guardian_phn_no = request.form.get('guardian_phn_no')
        year_of_study = request.form.get('year_of_study')
        institute_address = request.form.get('institute_address')
        permanent_address = request.form.get('permanent_address')
        local_address = request.form.get('local_address')
        phn_no = request.form.get('phn_no')
        alternate_phn_no = request.form.get('alternate_phn_no')
        email = request.form.get('email')
        alternate_email = request.form.get('alternate_email')
        project_group = request.form.get('project_group')
        training_from_date = request.form.get('training_from_date')
        training_to_date = request.form.get('training_to_date')
        bank_name = request.form.get('bank_name')
        dd_no = request.form.get('dd_no')
        date_of_dd = request.form.get('date_of_dd')
        date_of_dd2 = request.form.get('date_of_dd2')
        amount = request.form.get('amount')
        designation_english = request.form.get('designation_english')
        designation_hindi = request.form.get('designation_hindi')
        incharge_english = request.form.get('incharge_english')
        incharge_hindi = request.form.get('incharge_hindi')
        file = request.files.get('joining_file')
        employee_code_no=request.files.get('employee_code_no')
        gender= request.form.get('gender')
        joiningdate = request.form.get('joiningdate')



        student_record = StudentData.query.filter_by(name=name, phn_no=phn_no).first()

        if student_record:
            # Update existing record
            student_record.phn_no = phn_no or student_record.phn_no
            student_record.course = course or student_record.course
            student_record.branch = branch or student_record.branch
            student_record.institute_name = institute_name or student_record.institute_name
            student_record.project_domain = project_domain or student_record.project_domain
            student_record.project_title = project_title or student_record.project_title
            student_record.dob = datetime.strptime(dob, '%Y-%m-%d') if dob else student_record.dob
            student_record.guardian_name = guardian_name or student_record.guardian_name
            student_record.guardian_designation = guardian_designation or student_record.guardian_designation
            student_record.guardian_phn_no = guardian_phn_no or student_record.guardian_phn_no
            student_record.year_of_study = year_of_study or student_record.year_of_study
            student_record.institute_address = institute_address or student_record.institute_address
            student_record.permanent_address = permanent_address or student_record.permanent_address
            student_record.local_address = local_address or student_record.local_address
            student_record.alternate_phn_no = alternate_phn_no or student_record.alternate_phn_no
            student_record.email = email or student_record.email
            student_record.alternate_email = alternate_email or student_record.alternate_email
            student_record.project_group = project_group or student_record.project_group
            student_record.training_from_date = datetime.strptime(training_from_date, '%Y-%m-%d') if training_from_date else student_record.training_from_date
            student_record.training_to_date = datetime.strptime(training_to_date, '%Y-%m-%d') if training_to_date else student_record.training_to_date
            student_record.bank_name = bank_name or student_record.bank_name
            student_record.dd_no = dd_no or student_record.dd_no
            student_record.date_of_dd = datetime.strptime(date_of_dd, '%Y-%m-%d') if date_of_dd else student_record.date_of_dd
            student_record.date_of_dd2 = datetime.strptime(date_of_dd2, '%Y-%m-%d') if date_of_dd2 else student_record.date_of_dd2
            student_record.amount = amount or student_record.amount
            student_record.designation_english = designation_english or student_record.designation_english
            student_record.designation_hindi = designation_hindi or student_record.designation_hindi
            student_record.incharge_english = incharge_english or student_record.incharge_english
            student_record.incharge_hindi = incharge_hindi or student_record.incharge_hindi
            student_record.dateofjoining = joiningdate or student_record.dateofjoining
            student_record.employee_code_no = employee_code_no or student_record.employee_code_no
            student_record.gender= gender or student_record.gender





            if file:
                student_record.joiningfile = file.read()
        else:
            # Add new record
            student_record = StudentData(
                name=name,
                course=course,
                branch=branch,
                institute_name=institute_name,
                project_domain=project_domain,
                project_title=project_title,
                dob=datetime.strptime(dob, '%Y-%m-%d') if dob else None,
                guardian_name=guardian_name,
                guardian_designation=guardian_designation,
                guardian_phn_no=guardian_phn_no,
                year_of_study=year_of_study,
                institute_address=institute_address,
                permanent_address=permanent_address,
                local_address=local_address,
                phn_no=phn_no,
                alternate_phn_no=alternate_phn_no,
                email=email,
                alternate_email=alternate_email,
                project_group=project_group,
                training_from_date=datetime.strptime(training_from_date, '%Y-%m-%d') if training_from_date else None,
                training_to_date=datetime.strptime(training_to_date, '%Y-%m-%d') if training_to_date else None,
                bank_name=bank_name,
                dd_no=dd_no,
                date_of_dd=datetime.strptime(date_of_dd, '%Y-%m-%d') if date_of_dd else None,
                date_of_dd2=datetime.strptime(date_of_dd2, '%Y-%m-%d') if date_of_dd2 else None,
                amount=amount,
                designation_english=designation_english,
                designation_hindi=designation_hindi,
                incharge_english=incharge_english,
                incharge_hindi=incharge_hindi,
                joiningfile=file.read() if file else None,
                dateofjoining=joiningdate,
                employee_code_no= employee_code_no,
                gender= gender

            )
            db.session.add(student_record)

        db.session.commit()

        success_message = "Student details submitted successfully."
        return redirect(url_for('ophome', message=success_message, msg_type='success'))

@app.route('/joinprint')
def joinprint():
    return render_template('joinprint.html')


@app.route('/viewinfojoin', methods=['GET', 'POST'])
def viewinfojoin():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))

    elif request.method == 'POST':
        name = request.form.get('name')
        phn_no = request.form.get('phn_no')

        session['student_name'] = name
        session['phone'] = phn_no

        student_record = StudentData.query.filter_by(name=name, phn_no=phn_no).first()

        if student_record:
            print("okkk")
            return render_template('viewjoin.html', student=student_record)
        else:
            return redirect(url_for('ophome', message="student not found", msg_type='success'))

    return render_template('viewinfojoin.html')

@app.route('/viewcertificate', methods=['POST'])
def view_certificate():
    name = request.form.get('name')
    phone_no = request.form.get('phn_no')

    session['certificate_name'] = name



    # Query the database for the student details
    student = StudentData.query.filter_by(name=name, phn_no=phone_no).first()

    if student:
        # Extract details from the student record
        return render_template('certificate.html',
                               student_name=student.name,
                               guardian_name=student.guardian_name,
                               college_name=student.institute_name,
                               course=student.course,
                               start_date=student.training_from_date,
                               end_date=student.training_to_date,
                               title=student.project_title,
                               division=student.project_group,
                               today_date=date.today().strftime('%B %d, %Y'),
                               ref_no= student.ref_no,
                               branch= student.branch,
                               gender= student.gender)  # Adjust based on your data
    else:
        error = "Student not found. Please check the details."
        return render_template('generate_certificate.html', error=error)


@app.route('/joiningform')
def joiningform():
    return render_template('joiningform.html')


@app.route('/save-student2', methods=['POST'])
def save_student2():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    else:
        name = request.form.get('name')
        course = request.form.get('course')
        branch = request.form.get('branch')
        institute_name = request.form.get('institute_name')
        project_domain = request.form.get('project_domain')
        project_title = request.form.get('project_title')
        dob = request.form.get('dob')
        guardian_name = request.form.get('guardian_name')
        guardian_designation = request.form.get('guardian_designation')
        guardian_phn_no = request.form.get('guardian_phn_no')
        year_of_study = request.form.get('year_of_study')
        institute_address = request.form.get('institute_address')
        permanent_address = request.form.get('permanent_address')
        local_address = request.form.get('local_address')
        phn_no = request.form.get('phn_no')
        alternate_phn_no = request.form.get('alternate_phn_no')
        email = request.form.get('email')
        alternate_email = request.form.get('alternate_email')
        project_group = request.form.get('project_group')
        training_from_date = request.form.get('training_from_date')
        training_to_date = request.form.get('training_to_date')
        bank_name = request.form.get('bank_name')
        dd_no = request.form.get('dd_no')
        date_of_dd = request.form.get('date_of_dd')
        date_of_dd2 = request.form.get('date_of_dd2')
        amount = request.form.get('amount')
        designation_english = request.form.get('designation_english')
        designation_hindi = request.form.get('designation_hindi')
        incharge_english = request.form.get('incharge_english')
        incharge_hindi = request.form.get('incharge_hindi')
        file = request.files.get('joining_file')
        employee_code_no=request.files.get('employee_code_no')
        phone = session.get('phone', '')
        student_name = session.get('student_name', '')

        gender= request.form.get('gender')

        student_record = StudentData.query.filter_by(name=student_name, phn_no=phone).first()

        if student_record:
            # Update existing record
            student_record.name = name or student_record.name
            student_record.phn_no = phn_no or student_record.phn_no
            student_record.course = course or student_record.course
            student_record.branch = branch or student_record.branch
            student_record.institute_name = institute_name or student_record.institute_name
            student_record.project_domain = project_domain or student_record.project_domain
            student_record.project_title = project_title or student_record.project_title
            student_record.dob = datetime.strptime(dob, '%Y-%m-%d') if dob else student_record.dob
            student_record.guardian_name = guardian_name or student_record.guardian_name
            student_record.guardian_designation = guardian_designation or student_record.guardian_designation
            student_record.guardian_phn_no = guardian_phn_no or student_record.guardian_phn_no
            student_record.year_of_study = year_of_study or student_record.year_of_study
            student_record.institute_address = institute_address or student_record.institute_address
            student_record.permanent_address = permanent_address or student_record.permanent_address
            student_record.local_address = local_address or student_record.local_address
            student_record.alternate_phn_no = alternate_phn_no or student_record.alternate_phn_no
            student_record.email = email or student_record.email
            student_record.alternate_email = alternate_email or student_record.alternate_email
            student_record.project_group = project_group or student_record.project_group
            student_record.training_from_date = datetime.strptime(training_from_date, '%Y-%m-%d') if training_from_date else student_record.training_from_date
            student_record.training_to_date = datetime.strptime(training_to_date, '%Y-%m-%d') if training_to_date else student_record.training_to_date
            student_record.bank_name = bank_name or student_record.bank_name
            student_record.dd_no = dd_no or student_record.dd_no
            student_record.date_of_dd = datetime.strptime(date_of_dd, '%Y-%m-%d') if date_of_dd else student_record.date_of_dd
            student_record.date_of_dd2 = datetime.strptime(date_of_dd2, '%Y-%m-%d') if date_of_dd2 else student_record.date_of_dd2
            student_record.amount = amount or student_record.amount
            student_record.designation_english = designation_english or student_record.designation_english
            student_record.designation_hindi = designation_hindi or student_record.designation_hindi
            student_record.incharge_english = incharge_english or student_record.incharge_english
            student_record.incharge_hindi = incharge_hindi or student_record.incharge_hindi
            student_record.dateofjoining = datetime.now().strftime("%d-%m-%Y")
            student_record.employee_code_no = employee_code_no or student_record.employee_code_no
            student_record.gender= gender or student_record.gender



            if file:
                student_record.joiningfile = file.read()
        else:
            error= "no student found"
            return redirect(url_for('ophome', message=error, msg_type='error'))

            db.session.add(student_record)

        db.session.commit()

        success_message = "Student details changed successfully."
        return redirect(url_for('ophome', message=success_message, msg_type='success'))

@app.route('/mentoredit')
def mentoredit():
    return render_template('mentoredit.html')

@app.route('/submitmen2', methods=['POST'])
def submitmen2():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    else:
        # Retrieve form data
        name = request.form.get('name')
        course = request.form.get('course')
        branch = request.form.get('branch')
        institute_name = request.form.get('institute_name')
        project_domain = request.form.get('project_domain')
        project_title = request.form.get('project_title')
        guide_name = request.form.get('guide_name')
        date = request.form.get('date')
        file = request.files.get('fileUpload')
        phn_no= request.form.get('phone')

        # Retrieve student ID from session
        student_id = session.get('student_id')
        phoneno=session.get('phoneno')

        if not student_id:
            error_message = "No student ID found in session."
            return redirect(url_for('ophome', message=error_message, msg_type='error'))

        # Check if student exists in database
        student = StudentData.query.filter_by(name=student_id, phn_no= phoneno).first()

        if student:
            # Update student details based on form data
            student.name = name if name else student.name
            student.course = course if course else student.course
            student.branch = branch if branch else student.branch
            student.institute_name = institute_name if institute_name else student.institute_name
            student.project_domain = project_domain if project_domain else student.project_domain
            student.project_title = project_title if project_title else student.project_title
            student.guide_name = guide_name if guide_name else student.guide_name
            student.phn_no = phn_no if phn_no else student.phn_no


            if file and file.filename.endswith('.pdf'):
                student.file_data = file.read()

            db.session.commit()
            success_message = "Student details updated successfully."
            return redirect(url_for('ophome', message=success_message, msg_type='success'))
        else:
            error_message = f"No student found with Name: {student_id}"
            return redirect(url_for('ophome', message=error_message, msg_type='error'))


@app.route('/submit_nodues', methods=['POST'])
def submit_nodues():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))

    else:
        ref_no = request.form.get('reg_number')
        trainee_name = request.form.get('trainee_name')
        conduct = request.form.get('conduct')
        attendance = request.form.get('attendance')
        file = request.files.get('fileUpload')
        project_details = request.form.get('project_details')
        idc = request.form.get('idc')
        phone2= request.form.get('phone')

        session['trainee_name'] = trainee_name
        session['phone2'] = phone2


        if conduct == 'satisfactory':
            conduct = 'Satisfactory'
        elif conduct == 'not_satisfactory':
            conduct = 'Not Satisfactory'

            print(conduct)

        # Fetch the newly added student's details from the database
        student = StudentData.query.filter_by(name=trainee_name, phn_no= phone2).first()

        # Assuming `project_details` and `idc` are form fields, not files
        if student:
            print("found")

            # Save uploaded PDF file if it exists
            if file and file.filename.endswith('.pdf'):
                file_data = file.read()
            else:
                file_data = None

            # Update student data
            student.ref_no = ref_no
            student.conduct = conduct
            student.attendance = attendance
            student.projectdetails = project_details
            student.idc = idc
            student.nodues_file = file_data

            # Commit changes to the database
            db.session.commit()

            # Render the template with the student's details
            return render_template('viewnodues.html', student=student)
        else:
            error_message = "Student not found"
            return redirect(url_for('ophome', message=error_message, msg_type='error'))

@app.route('/editnodues')
def editnodues():
    return render_template('editnodues.html')

@app.route('/submit_nodues2', methods=['POST'])
def submit_nodues2():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    else:
        ref_no = request.form.get('reg_number')
        conduct = request.form.get('conduct')
        attendance = request.form.get('attendance')
        file = request.files.get('fileUpload')
        project_details = request.form.get('project_details')
        idc = request.form.get('idc')
        trainee_name = session.get('trainee_name')
        phone3= session.get('phone2')

        if conduct == 'satisfactory':
            conduct = 'Satisfactory'
        elif conduct == 'not_satisfactory':
            conduct = 'Not Satisfactory'

        # Fetch the newly added student's details from the database
        student = StudentData.query.filter_by(name=trainee_name, phn_no= phone3).first()

        if student:
            # Save uploaded PDF file if it exists
            if file and file.filename.endswith('.pdf'):
                file_data = file.read()
            else:
                file_data = None

            # Update the student's details with fallback to current values if no new input
            student.ref_no = ref_no if ref_no else student.ref_no
            student.conduct = conduct if conduct else student.conduct
            student.attendance = attendance if attendance else student.attendance
            student.projectdetails = project_details if project_details else student.projectdetails
            student.idc = idc if idc else student.idc
            student.nodues_file = file_data if file_data else student.nodues_file

            # Commit changes to the database
            db.session.commit()

            # Return a response or render a template
            return render_template('viewnodues.html', student=student)
        else:
            error_message = "Student not found"
            return redirect(url_for('ophome', message=error_message, msg_type='error'))


@app.route('/fetchmentoracc', methods=['GET', 'POST'])
def fetchmentoracc():
    selected_date = None
    data = None
    error = None
    message = None

    if request.method == 'POST':
        selected_date = request.form.get('selectedDate')
        if not selected_date:
            error = 'Please select a date'
        else:
            data = StudentData.query.filter_by(date_mentacc=selected_date).all()
            if not data:
                message = 'No data found for the selected date'

    return render_template('fetchmentoracc.html', selected_date=selected_date, data=data, error=error, message=message)

@app.route('/fetchmentoracc2', methods=['GET', 'POST'])
def fetch_mentor_acc():
    data = []
    error = None
    message = None

    if request.method == 'POST':
        selected_date = request.form.get('selectedDate')
        student_name = request.form.get('studentName')

        # Case 1: Filter by date
        if selected_date:
            data = StudentData.query.filter_by(date_mentacc=selected_date).all()
            if not data:
                message = 'No data found for the selected date'

        # Case 2: Filter by partial student name
        elif student_name:
            data = StudentData.query.filter(StudentData.name.ilike(f"%{student_name}%")).all()
            if not data:
                message = 'No student found with the given name'

        else:
            error = 'Please enter a name or select a date.'

    return render_template('fetchmentoracc2.html', data=data, error=error, message=message)

@app.route('/download/<int:student_id>', methods=['GET'])
def download_file(student_id):
    student = StudentData.query.get(student_id)
    if student and student.file_data:
        return send_file(
            BytesIO(student.file_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='mentor_acceptance.pdf'  # Updated argument
        )
    else:
        abort(404, description="File not found")


@app.route('/update_collected_status', methods=['POST'])
def update_collected_status():
    if 'user_id' not in session:
        return redirect(url_for('index', error= "SESSION TIMED OUT"))
    else:
        collected = request.form.get('collected', 'no')
        name =session.get('certificate_name')
     # Assuming you have some way to identify which record to update

        # Update the database with the collected status
        student = StudentData.query.filter_by(name= name).first()
        if student:
            student.mark = collected
            student.certificatecollectiondate = date.today()
            db.session.commit()
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Record not found"}), 404

@app.route('/certificatesnotcollected')
def certificates_not_collected():
    students = StudentData.query.filter_by(mark='no').all()
    return render_template('certificatesnotcollected.html', students=students)
from flask import session

@app.route('/student_data', methods=['GET', 'POST'])
def student_data():
    students = []

    from_date = request.form.get('studentFromDate')
    to_date = request.form.get('studentToDate')
    student_name = request.form.get('studentName')

    # Only refetch if not exporting
    if request.method == 'POST' and 'export' not in request.form:
        ids = []

        if from_date and to_date:
            filtered_by_date = StudentData.query.filter(
                StudentData.training_from_date >= from_date,
                StudentData.training_to_date <= to_date
            ).all()
            for s in filtered_by_date:
                students.append(s)
                ids.append(s.id)

        if student_name:
            filtered_by_name = StudentData.query.filter(
                StudentData.name.ilike(f'%{student_name}%')
            ).all()
            for s in filtered_by_name:
                students.append(s)
                ids.append(s.id)

        session['student_ids'] = ids  # Save to session

    elif request.method == 'POST' and 'export' in request.form:
        ids = session.get('student_ids', [])
        students = StudentData.query.filter(StudentData.id.in_(ids)).all()

    # Add duration
    for student in students:
        if student.training_from_date and student.training_to_date:
            duration = (student.training_to_date - student.training_from_date).days // 7
            student.duration_weeks = duration

    # Export logic
    if request.method == 'POST' and 'export' in request.form:
        data = [{
            'Name': student.name,
            'Phone Number': student.phn_no,
            'Guide Name': student.guide_name,
            'Project Title': student.project_title,
            'Training Period': f"{student.training_from_date} to {student.training_to_date}",
        } for student in students]

        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Student Data')
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="student_data.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    return render_template('stuinterndetails.html', students=students)

@app.route('/stu2')
def stu2():
    return render_template('stu2.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    students = None
    if request.method == 'POST':
        ref_no = request.form.get('ref_no')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')

        query = db.session.query(StudentData)

        if ref_no:
            query = query.filter(StudentData.ref_no == ref_no)
        if name:
            query = query.filter(StudentData.name.ilike(f'%{name}%'))
        if phone_number:
            query = query.filter(StudentData.phn_no == phone_number)

        students = query.all()

    return render_template('viewverification.html', students=students)


@app.route('/verification', methods=['GET', 'POST'])
def verification():

    return render_template('verficationsoughtlanding.html')

@app.route('/certificate2/<int:student_id>')
def certificate2(student_id):

    student = StudentData.query.get(student_id)
    if student:
        if student.photo:
            encoded_photo = base64.b64encode(student.photo).decode('utf-8')
            photo_data_url = f"data:image/jpeg;base64,{encoded_photo}"  # or image/png if it's PNG

            # Logic to generate and display the certificate
            return render_template('certificate2.html',student_name=student.name,
                                   guardian_name=student.guardian_name,
                                   college_name=student.institute_name,
                                   course=student.course,
                                   start_date=student.training_from_date,
                                   end_date=student.training_to_date,
                                   title=student.project_title,
                                   division=student.project_group,
                                   today_date=student.certificatecollectiondate,
                                   ref_no= student.ref_no,
                                   branch= student.branch,
                                   photo= photo_data_url,
                                   gender= student.gender)
        else:
            return render_template('certificate2.html', student_name=student.name,
                                   guardian_name=student.guardian_name,
                                   college_name=student.institute_name,
                                   course=student.course,
                                   start_date=student.training_from_date,
                                   end_date=student.training_to_date,
                                   title=student.project_title,
                                   division=student.project_group,
                                   today_date=student.certificatecollectiondate,
                                   ref_no=student.ref_no,
                                   branch=student.branch,
                                   photo=None,
                                   gender=student.gender)
    else:
        return "Student not found", 404

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

@app.route('/export_all_students', methods=['GET'])
def export_all_students():
    students = StudentData.query.all()

    # Get all column names dynamically
    columns = [c.key for c in inspect(StudentData).mapper.column_attrs]

    # Convert to list of dicts
    data = []
    for student in students:
        row = {}
        for col in columns:
            val = getattr(student, col)
            row[col] = str(val) if val is not None else ''
        data.append(row)

    # Create Excel file in memory
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='All Students')
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="all_student_data.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    # Get the student's name from the session
    name = session.get('certificate_name')

    if not name:
        return 'Student name not found in session', 400  # If the name is not in the session

    # Ensure that a photo is uploaded
    if 'photo' not in request.files:
        return 'No photo uploaded', 400

    file = request.files['photo']

    if file:
        # Optional: Validate file type if needed
        if file and file.filename.split('.')[-1].lower() not in ['png', 'jpeg', 'jpg']:
            return 'Invalid file type. Please upload a PNG or JPEG image.', 400

        # Find the student by name from the session
        student = StudentData.query.filter_by(name=name).first()  # Use the session name to find the student

        if student:
            # Save the photo as binary in the database
            student.photo = file.read()  # Store the image data in the 'photo' column (make sure it's defined in your model)
            db.session.commit()  # Save the changes to the database
            return 'Photo saved successfully', 200
        else:
            return 'Student not found', 404
    return 'Upload failed', 400

@app.route('/search2', methods=['GET', 'POST'])
def search2():
    students = None
    if request.method == 'POST':
        ref_no = request.form.get('ref_no')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')

        query = db.session.query(StudentData)

        if ref_no:
            query = query.filter(StudentData.ref_no == ref_no)
        if name:
            query = query.filter(StudentData.name.ilike(f'%{name}%'))
        if phone_number:
            query = query.filter(StudentData.phn_no == phone_number)

        students = query.all()

    return render_template('viewverification2.html', students=students)


if __name__ == '__main__':
    # Open the browser in a separate thread after 1 second
    Timer(1, open_browser).start()
    app.run(debug=True)
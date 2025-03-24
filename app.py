from flask import Flask, render_template, request, flash, session, redirect, url_for , jsonify 
import io , os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from models import *  
from models import User, Applicants 
import re
import sqlite3
from flask import send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder='static', template_folder='static/templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Admin Role')
        db.session.add(admin_role)

    employee_role = Role.query.filter_by(name='employee').first()
    if not employee_role:
        employee_role = Role(name='employee', description='Employee Role')
        db.session.add(employee_role)

    applicant_role = Role.query.filter_by(name='applicant').first()
    if not applicant_role:
        applicant_role = Role(name='applicant', description='Applicant Role')
        db.session.add(applicant_role)

    db.session.commit()


    admin = User.query.filter_by(email='admin@gmail.com').first()
    if not admin:
        admin = User(
            name='Admin User',
            email='admin@gmail.com',
            password='admin',
            role_id=admin_role.id 
        )
        db.session.add(admin)
        db.session.commit()

    employees = User.query.all()
    for emp in employees:
        print(f"ID: {emp.id}, Name: {emp.name}, Email: {emp.email}, Role ID: {emp.role_id}")
    print([hired.employee_email for hired in Hired.query.all()])


#--------------------------------------------------------------------------------------------------------------------------------
# ROUTERS 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Invalid credentials', 'danger')
        return render_template('login.html')

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        session.pop('_flashes', None)
        session['user_email'] = user.email
        session['role'] = user.role.name

        flash("Login successful!", "success")

        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['role'] == 'employee':
            return redirect(url_for('employee_dashboard'))
        else:
            session.clear()
            flash("Invalid user/role. Please contact admin.", "danger")
            return redirect(url_for('login'))

    applicant = Applicants.query.filter_by(email=email).first()

    if applicant and applicant.password == password:
        session.pop('_flashes', None)
        session['user_email'] = applicant.email
        session['role'] = 'applicant'

        flash("Login successful!", "success")
        return redirect(url_for('profile_dashboard'))

    flash('Invalid credentials', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  

        if not is_valid_email(email):
            flash("Invalid email format.", "danger")
            return redirect('/register')

        existing_user = User.query.filter_by(email=email).first()
        existing_applicant = Applicants.query.filter_by(email=email).first()
        
        if existing_user or existing_applicant:
            flash("Email already exists. Try logging in.", "danger")
            return redirect('/register')

        if role == "applicant":
            new_applicant = Applicants(
                name=username,
                email=email,
                password=password,
                approval=False
            )
            db.session.add(new_applicant)
        else:
            role_id = 1 if role == "admin" else 2  
            new_user = User(
                name=username,
                email=email,
                password=password,
                role_id=role_id
            )
            db.session.add(new_user)

        db.session.commit()
        flash("Registration Successful! You can now log in.", "success")
        return redirect('/login')

    return render_template('register.html')

# DASHBOARDS -----------------------------------------------------------------------------------------------------------------

@app.route('/admin_dashboard')
def admin_dashboard():
    print("Session Data in Admin Dashboard:", session) 
    
    if 'user_email' not in session or session.get('role') != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    user = User.query.all()
    applicants = Applicants.query.all()
    jobs = Job.query.all()
    hired_count = Hired.query.all()

    return render_template('admin_dashboard.html', user=user, applicants=applicants, jobs=jobs, hired_count=hired_count)

@app.route('/chart.png')
def get_chart_data():
    applicants_count = Applicants.query.count()  
    employees_count = User.query.filter_by(role_id=2).count()  

    return jsonify({
        "labels": ["Applicants", "Employees"],
        "data": [applicants_count, employees_count]
    })


@app.route('/employee_dashboard')
def employee_dashboard():
    print("Session Data in Employee Dashboard:", session) 
    
    if 'user_email' not in session:
        flash('Please log in first!', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['user_email']).first()
    applicants = Applicants.query.all() 
    jobs = Job.query.all()
    
    hired_count = Hired.query.filter_by(employee_email=user.email).count()

    return render_template('employee_dashboard.html', user=user, applicants=applicants, jobs=jobs, hired_count=hired_count)



@app.route('/profile_dashboard')
def profile_dashboard():
    if 'user_email' not in session or session['role'] != 'applicant':
        flash('Access Denied!', 'danger')
        return redirect(url_for('login'))

    applicant = Applicants.query.filter_by(email=session['user_email']).first()

    if not applicant:
        flash('Applicant not found!', 'danger')
        return redirect(url_for('login'))

    jobs = Job.query.all()

    return render_template('profile_dashboard.html', user=applicant, jobs=jobs)
#------------------------------------------------------------------------------------------------------------------------------------

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER       
def allowed_file(filename):
    """Check if the file is allowed by extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#-----------------------------------------------------------------------------------------------------------------------------------

@app.route('/resume/<resume_filename>')
def view_resume(resume_filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], resume_filename)

@app.route('/upload_resume', methods=["GET", "POST"])       #ERROR
def upload_resume():
    if 'user_email' not in session or session['role'] != 'applicant':
        flash('Access Denied! Please log in as an applicant.', 'danger')
        return redirect(url_for('login'))

    applicant = Applicants.query.filter_by(email=session['user_email']).first()

    if not applicant:
        flash('Applicant not found!', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        resume = request.files.get('resume')

        if not resume or not allowed_file(resume.filename):
            flash("Invalid resume format. Please upload a PDF, DOC, or DOCX file.", "danger")
            return redirect('/upload_resume')

        resume_filename = secure_filename(resume.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        resume.save(resume_path)

        applicant.resume = resume_filename
        db.session.commit()

        flash("Resume uploaded successfully!", "success")
        return redirect(url_for('profile_dashboard'))

    return render_template('upload_resume.html')


@app.route('/edit_profile/<field>', methods=['GET', 'POST'])
def edit_profile(field):
    if 'user_email' not in session:
        flash('Please log in first!', 'danger')
        return redirect(url_for('login'))

    if session['role'] == 'applicant':
        user = Applicants.query.filter_by(email=session['user_email']).first()
    else:
        user = User.query.filter_by(email=session['user_email']).first()

    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_value = request.form.get('value')

        if not new_value:
            flash(f"The {field} field cannot be empty!", 'danger')
            return redirect(url_for('edit_profile', field=field))

        setattr(user, field, new_value)
        
        db.session.commit()
        flash(f"Your {field} has been updated!", 'success')
        return redirect(url_for('profile_dashboard'))

    return render_template('edit_profile.html', user=user, field=field)



@app.route('/applicants')
def applicants():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    applicants = Applicants.query.all()
    
    return render_template('applicants.html', applicants=applicants)

@app.route('/job_detail/<int:job_id>')
def job_detail(job_id):
    if 'user_email' not in session:
        flash('Please log in to view job details!', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['user_email']).first()
    job = Job.query.get(job_id)

    if not job:
        flash('Job not found!', 'danger')
        return redirect(url_for('career'))

    return render_template('job_detail.html', user=user, job=job)


@app.route('/approve_applicant/<applicant_email>', methods=['POST'])
def approve_applicant(applicant_email):
    if 'role' not in session or session['role'] != 'employee':
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    applicant = Applicants.query.filter_by(email=applicant_email).first()
    if not applicant:
        flash("Applicant not found.", "danger")
        return redirect(url_for('employee_dashboard'))

    employee = User.query.filter_by(email=session['user_email']).first()
    if not employee:
        flash("Employee not found!", "danger")
        return redirect(url_for('employee_dashboard'))

    employee_role = Role.query.filter_by(name='employee').first()
    if not employee_role:
        flash("Employee role not found. Please contact admin.", "danger")
        return redirect(url_for('employee_dashboard'))

    new_employee = User(
        name=applicant.name,
        email=applicant.email,
        password=applicant.password,  
        role_id=employee_role.id
    )

    db.session.add(new_employee)

    hired_entry = Hired(employee_email=employee.email, applicant_email=applicant.email)
    db.session.add(hired_entry)
    db.session.delete(applicant)
    db.session.commit()
    flash(f"{applicant.email} is now an employee!", "success")
    return redirect(url_for('employee_dashboard'))
@app.route('/career')
def career():
    if 'user_email' not in session:
        flash('Please log in to view job listings!', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['user_email']).first()

    if session['role'] != 'applicant':
        flash("Only applicants can view job listings!", "danger")
        return redirect(url_for('employee_dashboard'))

    jobs = Job.query.all()
    return render_template('career.html', user=user, jobs=jobs)

@app.route('/reject_applicant/<applicant_email>', methods=['POST'])
def reject_applicant(applicant_email):
    if 'role' not in session or session['role'] != 'employee':
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    applicant = Applicants.query.filter_by(email=applicant_email).first()
    if not applicant:
        flash("Applicant not found.", "danger")
        return redirect(url_for('employee_dashboard'))

    db.session.delete(applicant)
    db.session.commit()

    flash(f"Applicant {applicant.email} has been rejected!", "warning")
    return redirect(url_for('employee_dashboard'))


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if 'user_email' not in session or session['role'] != 'employee':
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        vacancies = request.form['vacancies']
        employee_email = session['user_email']  

        if not title or not description or not vacancies:
            flash("All fields are required!", "danger")
            return redirect(url_for('add_job'))

        new_job = Job(
            title=title,
            description=description,
            vacancies=int(vacancies),
            employee_email=employee_email
        )

        db.session.add(new_job)
        db.session.commit()
        flash("Job posted successfully!", "success")
        return redirect(url_for('employee_dashboard'))

    return render_template('add_job.html')

@app.route('/apply_job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'user_email' not in session or session['role'] != 'applicant':
        flash('Only applicants can apply for jobs!', 'danger')
        return redirect(url_for('career'))

    applicant = Applicants.query.filter_by(email=session['user_email']).first()

    if not applicant:
        flash("Applicant profile not found!", "danger")
        return redirect(url_for('career'))

    existing_application = Application.query.filter_by(applicant_id=applicant.id, job_id=job_id).first()
    if existing_application:
        flash("You have already applied for this job!", "warning")
        return redirect(url_for('career'))

    new_application = Application(applicant_id=applicant.id, job_id=job_id, status="Pending Review")
    db.session.add(new_application)
    db.session.commit()

    flash("Application submitted successfully!", "success")
    return redirect(url_for('career'))

@app.route('/view_applications')
def view_applications():
    if 'role' not in session or session['role'] != 'employee':
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    job_applications = db.session.query(Application, Applicants, Job)\
        .join(Applicants, Application.applicant_id == Applicants.id)\
        .join(Job, Application.job_id == Job.id)\
        .filter(Application.status == "Pending Review")\
        .all()

    application_history = ApplicationHistory.query.order_by(ApplicationHistory.updated_on.desc()).all()

    return render_template('view_applications.html', job_applications=job_applications, application_history=application_history)




@app.route('/update_application/<int:app_id>', methods=['POST'])
def update_application(app_id):
    if 'role' not in session or session['role'] != 'employee':
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    application = Application.query.get(app_id)
    if not application:
        flash("Application not found!", "danger")
        return redirect(url_for('view_applications'))

    status = request.form.get('status')  # "Approved" or "Rejected"
    applicant = Applicants.query.get(application.applicant_id)
    if not applicant:
        flash("Applicant not found!", "danger")
        return redirect(url_for('view_applications'))

    history_entry = ApplicationHistory(
        application_id=application.id,
        applicant_id=application.applicant_id,
        job_id=application.job_id,
        status=status,
        updated_by=session['user_email'] 
    )
    db.session.add(history_entry)

    if status == "Approved":
        employee_role = Role.query.filter_by(name='employee').first()
        if not employee_role:
            flash("Employee role not found. Please contact admin.", "danger")
            return redirect(url_for('view_applications'))

        new_employee = User(
            name=applicant.name,
            email=applicant.email,
            password=applicant.password, 
            role_id=employee_role.id
        )
        db.session.add(new_employee)

        hired_entry = Hired(employee_email=session['user_email'], applicant_email=applicant.email)
        db.session.add(hired_entry)

        db.session.delete(applicant)

        flash(f"{applicant.name} has been approved and is now an employee!", "success")

    elif status == "Rejected":
        flash(f"{applicant.name}'s application has been rejected.", "danger")

    application.status = status
    db.session.commit()

    return redirect(url_for('view_applications'))





@app.route('/my_jobs')
def my_jobs():
    if 'role' not in session or session['role'] != 'employee':
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    jobs = Job.query.all()
    return render_template('my_jobs.html', jobs=jobs)

@app.route('/view_jobs')
def view_jobs():
    if 'role' not in session or session['role'] not in ['employee', 'admin']:
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    jobs = Job.query.all()  
    return render_template('view_jobs.html', jobs=jobs)

@app.route('/view_applicants')
def view_applicants():
    if 'role' not in session or session['role'] not in ['employee', 'admin']:
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    applicants = Applicants.query.all()

    return render_template('view_applicants.html', applicants=applicants)

@app.route('/view_team_members')
def view_team_members():
    if 'role' not in session or session['role'] not in ['employee', 'admin']:
        flash("Access Denied!", "danger")
        return redirect(url_for('employee_dashboard'))

    user = User.query.filter_by(email=session['user_email']).first()
    team_members = User.query.all()

    team_stats = {}
    for member in team_members:
        jobs_count = Job.query.filter_by(employee_email=member.email).count()
        hired_count = Hired.query.filter_by(employee_email=member.email).count()

        team_stats[member.email] = {
            'jobs_count': jobs_count,
            'hired_count': hired_count
        }

    return render_template('view_team_members.html', team_members=team_members, team_stats=team_stats)
















#--------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)

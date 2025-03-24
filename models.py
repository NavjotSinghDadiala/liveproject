from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False) 
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=2)
    flag = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resume = db.Column(LargeBinary, nullable=True) 

    role = db.relationship('Role', backref=db.backref('users', lazy=True))  

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False) 
    resume = db.Column(db.String(255), nullable=False , default= "No resume uploaded")  
    approval = db.Column(db.Boolean, default=False)
    experience = db.Column(db.String(100), nullable=True , default= "No experience")
    degree = db.Column(db.String(100), nullable=True , default= "No degree")
    skills = db.Column(db.String(500), nullable=True , default= "No skills")
    portfolio = db.Column(db.String(100), nullable=True , default= "No portfolio")

    def __repr__(self):
        return f"<Applicant {self.id} - {self.name}>" 

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    vacancies = db.Column(db.Integer, nullable=False, default=1)
    employee_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False) 

    employee = db.relationship('User', backref='posted_jobs')
    applications = db.relationship('Application', backref='job_applications', lazy=True)  

    def __repr__(self):
        return f"<Job {self.title}>"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(50), default="Applied")
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    job = db.relationship('Job', backref='job_applications')
    applicant = db.relationship('Applicants', backref='applicant_applications')

    def __repr__(self):
        return f"<Application {self.id} - Applicant {self.applicant_id} - Job {self.job_id}>"

class ApplicationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  
    updated_by = db.Column(db.String(100), nullable=False) 
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    application = db.relationship('Application', backref='history_entries')
    applicant = db.relationship('Applicants', backref='history_records')
    job = db.relationship('Job', backref='history_records')

    def __repr__(self):
        return f"<History {self.id} - App {self.application_id} - {self.status}>"


class Hired(db.Model):
    employee_email = db.Column(db.String(120), db.ForeignKey('user.email'), primary_key=True)
    applicant_email = db.Column(db.String(120), db.ForeignKey('applicants.email'), primary_key=True)
    hired_on = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('User', foreign_keys=[employee_email])
    applicant = db.relationship('Applicants', foreign_keys=[applicant_email])

    def __repr__(self):
        return f"<Hired Employee {self.employee_email} -> Applicant {self.applicant_email}>"

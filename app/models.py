from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Doctor(UserMixin, db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(50), unique=True) 
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False) 
    phone = db.Column(db.String(20), index=True)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    
    # New Patient History Sections
    past_history = db.Column(db.Text)
    family_history = db.Column(db.Text)
    personal_history = db.Column(db.Text)
    mental_general = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.now) # Fixed Timezone

    visits = db.relationship("Visit", backref="patient", lazy=True, cascade="all, delete-orphan")

class Visit(db.Model):
    __tablename__ = "visits"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    visit_date = db.Column(db.DateTime, default=datetime.now, index=True) # Fixed Timezone
    
    # Clinical Data
    symptoms = db.Column(db.Text)
    medicines_given = db.Column(db.Text)
    notes = db.Column(db.Text)
    photo_path = db.Column(db.String(255))
    is_followup = db.Column(db.Boolean, default=False)
    
    # Physical Generals
    appetite = db.Column(db.String(100))
    thirst = db.Column(db.String(100))
    tongue = db.Column(db.String(100))
    salivation = db.Column(db.String(100))
    taste = db.Column(db.String(100))
    desire = db.Column(db.String(100))
    aversion = db.Column(db.String(100))
    intolerance = db.Column(db.String(100))
    stool = db.Column(db.String(100))
    urine = db.Column(db.String(100))
    perspiration = db.Column(db.String(100))
    discharge = db.Column(db.String(100))
    thermal = db.Column(db.String(100))
    
    # Menstruation
    m_cycle = db.Column(db.String(100))
    m_flow = db.Column(db.String(100))
    m_color = db.Column(db.String(100))
    m_timing = db.Column(db.String(100)) 
    leucorrhoea = db.Column(db.String(100))
    
    # General Modalities
    fear = db.Column(db.String(100))
    air_pref = db.Column(db.String(100))

class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.now, index=True)
    category = db.Column(db.String(50))
    transaction_type = db.Column(db.String(10), default="Expense")
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))

class Notice(db.Model):
    __tablename__ = "notices"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="General") # e.g., Festival, Holiday, News
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
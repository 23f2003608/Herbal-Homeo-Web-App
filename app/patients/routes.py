# app/patients/routes.py (complete replacement)
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from sqlalchemy import or_, func, and_
from ..models import db, Patient, Visit
from flask import render_template, make_response
from io import BytesIO
import pdfkit

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")

def generate_patient_id():
    last_patient = Patient.query.order_by(Patient.id.desc()).first()
    if not last_patient:
        return "HH-01"
    last_id_num = int(last_patient.card_id.split('-')[1])
    return f"HH-{last_id_num + 1:02d}"

@patients_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_appointment():
    # Automated ID Logic
    last_patient = Patient.query.order_by(Patient.id.desc()).first()
    next_id = "HH-01"
    if last_patient and last_patient.card_id.startswith("HH-"):
        try:
            last_num = int(last_patient.card_id.split("-")[1])
            next_id = f"HH-{last_num + 1:02d}"
        except: pass

    if request.method == "POST":
        # 1. Create Patient with new History Fields
        patient = Patient(
            card_id=next_id,
            name=request.form.get("name"),
            age=request.form.get("age"), # Required
            phone=request.form.get("phone"),
            gender=request.form.get("gender"),
            address=request.form.get("address"),
            past_history=request.form.get("past_history"),
            family_history=request.form.get("family_history"),
            personal_history=request.form.get("personal_history"),
            mental_general=request.form.get("mental_general")
        )
        db.session.add(patient)
        db.session.flush()

        # 2. Handle Photo (Existing logic)
        photo_file = request.files.get("photo")
        photo_path = None
        if photo_file and photo_file.filename:
            filename = secure_filename(photo_file.filename)
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{datetime.now().timestamp()}_{filename}")
            photo_file.save(file_path)
            photo_path = file_path.split("app/static/")[-1]

        # 3. Create Visit with Physical Generals
        visit = Visit(
            patient=patient,
            visit_date=datetime.now(), # Local Time Fix
            symptoms=request.form.get("symptoms"),
            medicines_given=request.form.get("medicines"),
            notes=request.form.get("notes"),
            photo_path=photo_path,
            is_followup=False,
            # Physical Generals mapping
            appetite=request.form.get("appetite"),
            thirst=request.form.get("thirst"),
            tongue=request.form.get("tongue"),
            salivation=request.form.get("salivation"),
            taste=request.form.get("taste"),
            desire=request.form.get("desire"),
            aversion=request.form.get("aversion"),
            intolerance=request.form.get("intolerance"),
            stool=request.form.get("stool"),
            urine=request.form.get("urine"),
            perspiration=request.form.get("perspiration"),
            discharge=request.form.get("discharge"),
            thermal=request.form.get("thermal"),
            m_cycle=request.form.get("m_cycle"),
            m_flow=request.form.get("m_flow"),
            m_color=request.form.get("m_color"),
            m_timing=request.form.get("m_timing"),
            leucorrhoea=request.form.get("leucorrhoea"),
            fear=request.form.get("fear"),
            air_pref=request.form.get("air_pref")
        )
        db.session.add(visit)
        db.session.commit()
        flash(f"New Patient {next_id} registered successfully.", "success")
        return redirect(url_for("patients.patients_list"))
    return render_template("patients/appointment_form.html", next_id=next_id)

@patients_bp.route("/", methods=["GET", "POST"])
@login_required
def patients_list():
    """Main patients page with search + default listing"""
    page = request.args.get('page', 1, type=int)
    per_page = 15
    
    # Search parameters
    search_card_id = request.form.get("card_id") if request.method == "POST" else request.args.get("card_id")
    search_phone = request.form.get("phone") if request.method == "POST" else request.args.get("phone")
    search_name = request.form.get("name") if request.method == "POST" else request.args.get("name")
    search_date = request.form.get("date") if request.method == "POST" else request.args.get("date")
    
    query = db.session.query(Patient).join(Visit).group_by(Patient.id)
    
    if search_card_id:
        query = query.filter(Patient.card_id.ilike(f"%{search_card_id}%"))
    if search_phone:
        query = query.filter(Patient.phone.ilike(f"%{search_phone}%"))
    if search_name:
        query = query.filter(Patient.name.ilike(f"%{search_name}%"))
    if search_date:
        query = query.filter(func.date(Visit.visit_date) == search_date)
    
    patients = query.order_by(Patient.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template("patients/patients.html", patients=patients, 
                         search_params={
                             'card_id': search_card_id,
                             'phone': search_phone,
                             'name': search_name,
                             'date': search_date
                         })

@patients_bp.route("/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    """Edit patient details"""
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == "POST":
        patient.name = request.form.get("name", patient.name)
        patient.phone = request.form.get("phone", patient.phone)
        patient.gender = request.form.get("gender", patient.gender)
        patient.address = request.form.get("address", patient.address)
        patient.card_id = request.form.get("card_id", patient.card_id)
        db.session.commit()
        flash("Patient details updated.", "success")
        return redirect(url_for("patients.patients_list"))
    
    return render_template("patients/edit_patient.html", patient=patient)

@patients_bp.route("/<int:patient_id>/history")
@login_required
def patient_history(patient_id):
    """Patient history with images"""
    patient = Patient.query.get_or_404(patient_id)
    visits = Visit.query.filter_by(patient_id=patient_id).order_by(Visit.visit_date.desc()).all()
    return render_template("patients/patient_history.html", patient=patient, visits=visits)

@patients_bp.route("/<int:patient_id>/delete")
@login_required
def delete_patient(patient_id):
    """Delete patient and all visits"""
    patient = Patient.query.get_or_404(patient_id)
    patient_name = patient.name
    db.session.delete(patient)
    db.session.commit()
    flash(f"Patient {patient_name} and all records deleted.", "warning")
    return redirect(url_for("patients.patients_list"))

@patients_bp.route("/<int:patient_id>/followup", methods=["GET", "POST"])
@login_required
def new_followup(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        # Follow-up logic is now clean and separate
        photo_file = request.files.get("photo")
        photo_path = None
        if photo_file and photo_file.filename:
            filename = secure_filename(photo_file.filename)
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{datetime.now().timestamp()}_{filename}")
            photo_file.save(file_path)
            photo_path = file_path.split("app/static/")[-1]

        visit = Visit(
            patient_id=patient.id,
            visit_date=datetime.now(),
            symptoms=request.form.get("symptoms"),
            medicines_given=request.form.get("medicines"),
            notes=request.form.get("notes"),
            photo_path=photo_path,
            is_followup=True
        )
        db.session.add(visit)
        db.session.commit()
        flash("Follow-up visit recorded.", "success")
        return redirect(url_for('patients.patient_history', patient_id=patient.id))
    
    return render_template("patients/followup_form.html", patient=patient, current_date=datetime.now().strftime('%d %b %Y'))
#!/usr/bin/env python3
"""
Seed script to create a test doctor account
"""
from app import create_app, db
from app.models import Doctor

app = create_app()

with app.app_context():
    # Check if doctor already exists
    doctor = Doctor.query.filter_by(username="dr_shikhar").first()
    
    if not doctor:
        # Create new doctor
        doctor = Doctor(
            username="dr_shikhar",
            full_name="Dr. Shikhar Sharma"
        )
        doctor.set_password("password123")
        db.session.add(doctor)
        db.session.commit()
        print("✅ Doctor account created successfully!")
    else:
        print("✅ Doctor account already exists!")
    
    print("\n--- Login Credentials ---")
    print(f"Username: dr_shikhar")
    print(f"Password: password123")
    print(f"PIN: 2023")
    print("------------------------\n")

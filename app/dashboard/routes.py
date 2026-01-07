from flask import Blueprint, render_template, request
from flask_login import login_required
from ..models import Visit, Expense, Patient 
from .. import db 
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@login_required
def doctor_dashboard():
    now = datetime.now()
    # Get filters from URL, default to current month/year
    selected_month = request.args.get('month', now.month, type=int)
    selected_year = request.args.get('year', now.year, type=int)
    
    # 1. KPI CALCULATIONS
    # Today's footfall (real-time)
    today_footfall = Visit.query.filter(func.date(Visit.visit_date) == now.date()).count()

    # Monthly Revenue (Income transactions from Expense table)
    month_income = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == 'Income',
        func.extract("month", Expense.date) == selected_month,
        func.extract("year", Expense.date) == selected_year
    ).scalar()

    # Monthly Expenses
    month_expense = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == 'Expense',
        func.extract("month", Expense.date) == selected_month,
        func.extract("year", Expense.date) == selected_year
    ).scalar()

    net_profit = month_income - month_expense

    # Patient Stats for specific month
    month_query = Visit.query.filter(
        func.extract("month", Visit.visit_date) == selected_month,
        func.extract("year", Visit.visit_date) == selected_year
    )
    month_footfall = month_query.count()
    followups = month_query.filter(Visit.is_followup == True).count()
    new_patients = month_footfall - followups

    # 2. TREND DATA (Last 6 Months relative to selection)
    finance_labels, income_trend, expense_trend = [], [], []
    for i in range(5, -1, -1):
        # Calculate target months
        target_date = datetime(selected_year, selected_month, 1) - timedelta(days=i*30)
        m, y = target_date.month, target_date.year
        finance_labels.append(target_date.strftime("%b %y"))
        
        inc = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            Expense.transaction_type == 'Income',
            func.extract("month", Expense.date) == m, 
            func.extract("year", Expense.date) == y).scalar()
            
        exp = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            Expense.transaction_type == 'Expense',
            func.extract("month", Expense.date) == m, 
            func.extract("year", Expense.date) == y).scalar()
        
        income_trend.append(float(inc))
        expense_trend.append(float(exp))

    # 3. DEMOGRAPHICS (General lifetime stats)
    male_count = Patient.query.filter(func.lower(Patient.gender) == 'male').count()
    female_count = Patient.query.filter(func.lower(Patient.gender) == 'female').count()
    total_patients = Patient.query.count()
    other_count = total_patients - (male_count + female_count)
    
    # 4. RECENT TRANSACTIONS (Filtered by month)
    recent_transactions = Expense.query.filter(
        func.extract("month", Expense.date) == selected_month,
        func.extract("year", Expense.date) == selected_year
    ).order_by(Expense.date.desc()).limit(8).all()

    return render_template(
        "dashboard/doctor_dashboard.html",
        selected_month=selected_month,
        selected_year=selected_year,
        today_footfall=today_footfall,
        month_footfall=month_footfall,
        month_income=float(month_income),
        month_expense=float(month_expense),
        net_profit=float(net_profit),
        finance_labels=finance_labels,
        income_trend=income_trend,
        expense_trend=expense_trend,
        new_patients=new_patients,
        other_count=other_count,
        followups=followups,
        male_count=male_count,
        female_count=female_count,
        recent_transactions=recent_transactions,
        datetime=datetime
    )
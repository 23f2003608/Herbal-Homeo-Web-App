# app/expenses/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from sqlalchemy import func
from ..models import db, Expense

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@expenses_bp.route("/", methods=["GET", "POST"])
@login_required
def manage_expenses():
    # Get Month/Year from URL for filtering (defaults to current month)
    selected_month = request.args.get('month', datetime.today().month, type=int)
    selected_year = request.args.get('year', datetime.today().year, type=int)

    if request.method == "POST":
        date_str = request.form.get("date")
        t_type = request.form.get("transaction_type") 
        category = request.form.get("category")
        amount = request.form.get("amount")
        description = request.form.get("description")

        e = Expense(
            date=datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.today().date(),
            transaction_type=t_type,
            category=category,
            amount=amount,
            description=description
        )
        db.session.add(e)
        db.session.commit()
        flash(f"{t_type} added successfully.", "success")
        return redirect(url_for("expenses.manage_expenses", month=selected_month, year=selected_year))

    # Recent transactions for the table (Filtered by selected month/year)
    # Note: Using strftime for SQLite compatibility
    recent = Expense.query.filter(
        func.strftime('%m', Expense.date) == f"{selected_month:02d}",
        func.strftime('%Y', Expense.date) == str(selected_year)
    ).order_by(Expense.date.desc()).all()

    # Grouping Income by Category for Chart 1
    income_data = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter(
            Expense.transaction_type == 'Income', 
            func.strftime('%m', Expense.date) == f"{selected_month:02d}",
            func.strftime('%Y', Expense.date) == str(selected_year)
        )
        .group_by(Expense.category).all()
    )

    # Grouping Expenses by Category for Chart 2
    expense_data = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter(
            Expense.transaction_type == 'Expense',
            func.strftime('%m', Expense.date) == f"{selected_month:02d}",
            func.strftime('%Y', Expense.date) == str(selected_year)
        )
        .group_by(Expense.category).all()
    )

    return render_template(
        "expenses/expenses.html",
        expenses=recent,
        income_labels=[c[0] for c in income_data],
        income_values=[float(c[1]) for c in income_data],
        expense_labels=[c[0] for c in expense_data],
        expense_values=[float(c[1]) for c in expense_data],
        selected_month=selected_month,
        selected_year=selected_year,
        datetime=datetime
    )
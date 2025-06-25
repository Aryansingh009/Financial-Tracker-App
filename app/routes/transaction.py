# 🔌 Import required modules and objects
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app import db
from app.models import Transaction
from app.routes.forms import TransactionForm, DeleteTransactionForm
from flask_wtf.csrf import generate_csrf

# 🧩 Define a Blueprint for transaction-related routes
transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/add', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()  # Instantiate the form
    if form.validate_on_submit():  # If form is submitted and valid
        transaction = Transaction(
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data,
            date=form.date.data,
            user_id=session.get('user_id')  # Associate transaction with logged-in user
        )
        db.session.add(transaction)  # Add transaction to the session
        db.session.commit()  # Save it to the database
        return redirect(url_for('transaction_bp.dashboard'))  # Redirect to dashboard after saving
    return render_template('add.html', form=form)  # Show the form on GET or if invalid

@transaction_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))  # Redirect to login if user is not authenticated

    # Get all transactions for the logged-in user
    transactions = Transaction.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', transactions=transactions)  # Render dashboard with user's data

@transaction_bp.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth_bp.login'))  # Ensure user is logged in

    transaction = Transaction.query.get_or_404(transaction_id)  # Get transaction or return 404

    # 🚫 Ensure the user is only deleting their own transaction
    if transaction.user_id != session['user_id']:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('transaction_bp.dashboard'))

    db.session.delete(transaction)  # Delete the transaction
    db.session.commit()  # Save changes
    flash("Transaction deleted successfully.", "success")
    return redirect(url_for('transaction_bp.dashboard'))  # Return to dashboard

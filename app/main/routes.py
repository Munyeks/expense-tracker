from flask import Blueprint, Response, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import date
import io
import csv
from app import db
from app.models import Category, Transaction
from app.main.forms import CategoryForm, TransactionForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)

    income = db.session.query(func.sum(Transaction.amount)).join(Category).filter(
        Transaction.user_id == current_user.id, 
        Category.type == 'income',
        Transaction.date >= first_day_of_month
    ).scalar() or 0
    
    expense = db.session.query(func.sum(Transaction.amount)).join(Category).filter(
        Transaction.user_id == current_user.id, 
        Category.type == 'expense',
        Transaction.date >= first_day_of_month
    ).scalar() or 0
    
    balance = income - expense
    
    recent_transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= first_day_of_month
    ).order_by(Transaction.date.desc()).limit(5).all()

    # LOGIKA GRAFIK: Mengelompokkan pengeluaran berdasarkan kategori bulan ini
    expense_data = db.session.query(Category.name, func.sum(Transaction.amount)).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Category.type == 'expense',
        Transaction.date >= first_day_of_month
    ).group_by(Category.name).all()
    
    # Memisahkan label dan data untuk dikirim ke Chart.js
    chart_labels = [row[0] for row in expense_data]
    chart_values = [float(row[1]) for row in expense_data]

    return render_template('main/dashboard.html', 
                           title='Dashboard', 
                           income=income, 
                           expense=expense, 
                           balance=balance,
                           transactions=recent_transactions,
                           chart_labels=chart_labels,
                           chart_values=chart_values)

# RUTE BARU: Export transaksi ke format CSV
@main.route('/export')
@login_required
def export_csv():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    # Membuat file CSV di dalam memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header kolom
    writer.writerow(['Tanggal', 'Kategori', 'Tipe', 'Catatan', 'Nominal (Rp)'])
    
    for t in transactions:
        writer.writerow([
            t.date.strftime('%Y-%m-%d'),
            t.category.name,
            'Pemasukan' if t.category.type == 'income' else 'Pengeluaran',
            t.note or '',
            t.amount
        ])
        
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=riwayat_transaksi.csv"}
    )

@main.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = CategoryForm()
    
    # Menangani penambahan kategori baru
    if form.validate_on_submit():
        category = Category(name=form.name.data, type=form.type.data, owner=current_user)
        db.session.add(category)
        db.session.commit()
        flash('Kategori berhasil ditambahkan!', 'success')
        return redirect(url_for('main.categories'))
        
    # Mengambil semua kategori milik user yang sedang login
    user_categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    
    return render_template('main/categories.html', 
                           title='Kelola Kategori', 
                           form=form, 
                           categories=user_categories)

@main.route('/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.type = form.type.data
        db.session.commit()
        flash('Kategori berhasil diperbarui.', 'success')
        return redirect(url_for('main.categories'))
        
    return render_template('main/edit_category.html', title='Edit Kategori', form=form, category=category)

@main.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    form = TransactionForm()
    
    user_categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in user_categories]
    
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            category_id=form.category_id.data,
            note=form.note.data,
            date=form.date.data,
            owner=current_user
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaksi berhasil dicatat!', 'success')
        return redirect(url_for('main.transactions'))
        
    # LOGIKA PAGINATION & PENCARIAN
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()
    
    # Mulai dengan query dasar: transaksi milik user saat ini
    base_query = Transaction.query.filter_by(user_id=current_user.id).join(Category)
    
    # Jika ada kata kunci pencarian, tambahkan filter ilike (PostgreSQL style)
    if search_query:
        base_query = base_query.filter(
            db.or_(
                Transaction.note.ilike(f'%{search_query}%'),
                Category.name.ilike(f'%{search_query}%')
            )
        )
    
    pagination = base_query.order_by(Transaction.date.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('main/transactions.html', 
                           title='Kelola Transaksi', 
                           form=form, 
                           pagination=pagination,
                           search_query=search_query, # Kirim query kembali ke form HTML
                           categories_exist=len(user_categories) > 0)

@main.route('/transaction/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = TransactionForm(obj=transaction)
    
    user_categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in user_categories]
    
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.category_id = form.category_id.data
        transaction.date = form.date.data
        transaction.note = form.note.data
        db.session.commit()
        flash('Transaksi berhasil diperbarui.', 'success')
        return redirect(url_for('main.transactions'))
        
    return render_template('main/edit_transaction.html', title='Edit Transaksi', form=form, transaction=transaction)

@main.route('/transaction/<int:id>/delete', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaksi berhasil dihapus.', 'success')
    return redirect(url_for('main.transactions'))
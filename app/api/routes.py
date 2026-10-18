from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import Category, Transaction

api = Blueprint('api', __name__)

@api.route('/transactions')
@login_required
def get_transactions():
    # Mengambil 20 transaksi terakhir user
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(20).all()
    
    # Memformat data SQLAlchemy menjadi list of dictionaries (standar JSON)
    data = []
    for t in transactions:
        data.append({
            'id': t.id,
            'amount': float(t.amount),
            'date': t.date.strftime('%Y-%m-%d'),
            'category': t.category.name,
            'type': t.category.type,
            'note': t.note or ''
        })
        
    return jsonify({
        'status': 'success',
        'message': 'Data transaksi berhasil diambil',
        'count': len(data),
        'data': data
    })
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class CategoryForm(FlaskForm):
    name = StringField('Nama Kategori', validators=[DataRequired(), Length(max=50)])
    type = SelectField('Tipe', choices=[('expense', 'Pengeluaran'), ('income', 'Pemasukan')], validators=[DataRequired()])
    submit = SubmitField('Simpan Kategori')

class TransactionForm(FlaskForm):
    amount = DecimalField('Nominal', validators=[DataRequired()])
    # Pilihan category_id akan diisi secara dinamis di routes berdasarkan data user
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    note = StringField('Catatan', validators=[Length(max=200)])
    date = DateField('Tanggal', validators=[DataRequired()])
    submit = SubmitField('Simpan Transaksi')
# run.py
from app import create_app, db
from app.models import User, Category, Transaction

app = create_app()

# Fitur tambahan: Mendaftarkan context processor untuk shell CLI
# Ini sangat berguna untuk debugging via terminal (flask shell)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Category': Category, 'Transaction': Transaction}

if __name__ == '__main__':
    app.run(debug=True)
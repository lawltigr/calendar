import sys
from app import create_app
from extensions import db
from models import User

if len(sys.argv) != 2:
    print("Usage: python make_admin.py <username>")
    sys.exit(1)
username = sys.argv[1]

app = create_app()
with app.app_context():
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User '{username}' not found.")
        sys.exit(1)
    user.is_admin = True
    db.session.commit()
    print(f"User '{username}' is now an admin.")
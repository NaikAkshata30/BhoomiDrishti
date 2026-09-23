import secrets
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models import User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

OFFICIAL_ACCOUNTS = [
    ('umang.gov@officials.in', 'Official@123'),
    ('admin.gov@officials.in', 'Admin@123'),
    ('officer.gov@officials.in', 'Officer@123'),
    ('director.gov@officials.in', 'Director@123'),
]


def seed_official_accounts():
    for email, password in OFFICIAL_ACCOUNTS:
        if not User.query.filter_by(email=email).first():
            db.session.add(User(
                email=email,
                password_hash=generate_password_hash(password),
                role='official',
                full_name=email.split('.')[0].title(),
            ))
    db.session.commit()


@bp.route('/signup', methods=['POST'])
def signup():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get('email', '')).strip().lower()
    password = str(payload.get('password', ''))
    full_name = str(payload.get('full_name', '')).strip()

    if not email or not password or not full_name:
        return jsonify({'success': False, 'error': 'Full name, email, and password are required.'}), 400
    if len(password) < 8:
        return jsonify({'success': False, 'error': 'Password must contain at least 8 characters.'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'error': 'This email is already registered. Please sign in.'}), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role='civilian',
        full_name=full_name,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Account created. Please sign in.'}), 201


@bp.route('/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get('email', '')).strip().lower()
    password = str(payload.get('password', ''))
    role = str(payload.get('role', 'civilian')).lower()
    user = User.query.filter_by(email=email, role=role).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'success': False, 'error': 'Invalid email or password. Civilian users must sign up first.'}), 401

    return jsonify({
        'success': True,
        'token': secrets.token_urlsafe(32),
        'user': {'email': user.email, 'role': user.role, 'full_name': user.full_name},
    }), 200

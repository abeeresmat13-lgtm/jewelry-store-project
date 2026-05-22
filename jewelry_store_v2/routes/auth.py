from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User

auth = Blueprint('auth', __name__)


# ── ROUTE 1: REGISTER ─────────────────────────────────────────
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # redirect if already logged in
    if session.get('user_id'):
        return redirect(url_for('shop.home'))

    error = None

    if request.method == 'POST':
        username  = request.form.get('username', '').strip()
        email     = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password  = request.form.get('password', '')
        phone     = request.form.get('phone', '').strip()

        # manual validation
        if not username or not email or not full_name or not password:
            error = 'All fields are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif User.query.filter_by(username=username).first():
            error = 'Username already taken.'
        elif User.query.filter_by(email=email).first():
            error = 'Email already registered.'
        else:
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                role='customer'
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', error=error)


# ── ROUTE 2: LOGIN ────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('shop.home'))

    error = None

    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            error = 'Email and password are required.'
        else:
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password) and user.is_active:
                # store user info in session manually
                session['user_id']   = user.id
                session['user_name'] = user.full_name
                session['user_role'] = user.role
                flash(f'Welcome back, {user.full_name}!', 'success')

                if user.is_admin():
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('shop.home'))
            else:
                error = 'Invalid email or password.'

    return render_template('login.html', error=error)


# ── ROUTE 3: LOGOUT ───────────────────────────────────────────
@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('shop.home'))

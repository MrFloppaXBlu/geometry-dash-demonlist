from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Challenge, Submission
from config import config
import os

app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Display the main demonlist"""
    page = request.args.get('page', 1, type=int)
    challenges = Challenge.query.order_by(Challenge.placement).paginate(page=page, per_page=20)
    return render_template('index.html', challenges=challenges)

@app.route('/challenge/<int:challenge_id>')
def view_challenge(challenge_id):
    """View details of a specific challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    submissions = Submission.query.filter_by(challenge_id=challenge_id, status='approved').all()
    return render_template('challenge.html', challenge=challenge, submissions=submissions)

# ==================== AUTH ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new mod/admin"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login for mods/admins"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('mod_dashboard'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout current user"""
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# ==================== MOD PANEL ROUTES ====================

@app.route('/mod/dashboard')
@login_required
def mod_dashboard():
    """Mod dashboard overview"""
    if not current_user.is_mod and not current_user.is_admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('index'))
    
    challenges = Challenge.query.order_by(Challenge.placement).all()
    pending_submissions = Submission.query.filter_by(status='pending').count()
    
    return render_template('mod/dashboard.html', challenges=challenges, pending_submissions=pending_submissions)

@app.route('/mod/add-challenge', methods=['GET', 'POST'])
@login_required
def add_challenge():
    """Add a new challenge to the demonlist"""
    if not current_user.is_mod and not current_user.is_admin:
        flash('You do not have permission to perform this action', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        placement = request.form.get('placement', type=int)
        name = request.form.get('name')
        difficulty = request.form.get('difficulty')
        points = request.form.get('points', type=int)
        description = request.form.get('description')
        video_url = request.form.get('video_url')
        
        # Check if placement already exists
        if Challenge.query.filter_by(placement=placement).first():
            flash('A challenge at this placement already exists', 'error')
            return redirect(url_for('add_challenge'))
        
        challenge = Challenge(
            placement=placement,
            name=name,
            difficulty=difficulty,
            points=points,
            creator_id=current_user.id,
            description=description,
            video_url=video_url
        )
        db.session.add(challenge)
        db.session.commit()
        
        flash(f'Challenge "{name}" added successfully!', 'success')
        return redirect(url_for('mod_dashboard'))
    
    return render_template('mod/add_challenge.html')

@app.route('/mod/edit-challenge/<int:challenge_id>', methods=['GET', 'POST'])
@login_required
def edit_challenge(challenge_id):
    """Edit an existing challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    
    if not current_user.is_admin and current_user.id != challenge.creator_id:
        flash('You do not have permission to edit this challenge', 'error')
        return redirect(url_for('mod_dashboard'))
    
    if request.method == 'POST':
        challenge.placement = request.form.get('placement', type=int)
        challenge.name = request.form.get('name')
        challenge.difficulty = request.form.get('difficulty')
        challenge.points = request.form.get('points', type=int)
        challenge.description = request.form.get('description')
        challenge.video_url = request.form.get('video_url')
        
        db.session.commit()
        flash('Challenge updated successfully!', 'success')
        return redirect(url_for('mod_dashboard'))
    
    return render_template('mod/edit_challenge.html', challenge=challenge)

@app.route('/mod/delete-challenge/<int:challenge_id>', methods=['POST'])
@login_required
def delete_challenge(challenge_id):
    """Delete a challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    
    if not current_user.is_admin and current_user.id != challenge.creator_id:
        flash('You do not have permission to delete this challenge', 'error')
        return redirect(url_for('mod_dashboard'))
    
    challenge_name = challenge.name
    db.session.delete(challenge)
    db.session.commit()
    
    flash(f'Challenge "{challenge_name}" deleted successfully!', 'success')
    return redirect(url_for('mod_dashboard'))

@app.route('/mod/submissions')
@login_required
def view_submissions():
    """View and manage pending submissions"""
    if not current_user.is_mod and not current_user.is_admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    submissions = Submission.query.filter_by(status='pending').paginate(page=page, per_page=20)
    
    return render_template('mod/submissions.html', submissions=submissions)

@app.route('/mod/approve-submission/<int:submission_id>', methods=['POST'])
@login_required
def approve_submission(submission_id):
    """Approve a player submission"""
    if not current_user.is_mod and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    submission = Submission.query.get_or_404(submission_id)
    submission.status = 'approved'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Submission approved'})

@app.route('/mod/reject-submission/<int:submission_id>', methods=['POST'])
@login_required
def reject_submission(submission_id):
    """Reject a player submission"""
    if not current_user.is_mod and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    submission = Submission.query.get_or_404(submission_id)
    submission.status = 'rejected'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Submission rejected'})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ==================== CLI COMMANDS ====================

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Challenge': Challenge, 'Submission': Submission}

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def create_admin():
    """Create an admin user"""
    username = input('Username: ')
    email = input('Email: ')
    password = input('Password: ')
    
    if User.query.filter_by(username=username).first():
        print('Username already exists!')
        return
    
    user = User(username=username, email=email, is_admin=True, is_mod=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f'Admin user "{username}" created successfully!')

if __name__ == '__main__':
    app.run(debug=True)

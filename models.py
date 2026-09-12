from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Mod/Admin user model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_mod = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    challenges = db.relationship('Challenge', backref='creator', lazy=True, foreign_keys='Challenge.creator_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Challenge(db.Model):
    """Demonlist challenge model"""
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    placement = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)  # e.g., "Easy Demon", "Medium Demon", "Hard Demon", "Insane Demon", "Extreme Demon"
    points = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    submissions = db.relationship('Submission', backref='challenge', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Challenge {self.placement}. {self.name}>'


class Submission(db.Model):
    """Player submission model"""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    player_name = db.Column(db.String(120), nullable=False)
    video_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Submission {self.player_name} - {self.challenge.name}>'

# Geometry Dash Demonlist 🎮

A web-based Pointercrate-inspired demonlist for Geometry Dash with mod management capabilities. Mods can add, edit, and remove challenges, as well as manage player submissions.

## Features ✨

### Public Features
- **Browse Demonlist**: View all ranked challenges with difficulty tiers and points
- **Challenge Details**: Click any challenge to see full information, verification video, and verified completions
- **Responsive Design**: Beautiful gradient UI inspired by Pointercrate

### Mod Powers 🔧
- **Add Challenges**: Upload new demons to the list with placement, name, difficulty, points, and description
- **Edit Challenges**: Modify existing challenge details
- **Delete Challenges**: Remove challenges from the demonlist
- **Manage Submissions**: Review and approve/reject player completion submissions
- **Mod Dashboard**: Overview of all challenges and pending submissions

## Tech Stack 🛠️

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS/JavaScript (Jinja2 templates)
- **Authentication**: Flask-Login with password hashing

## Installation 📦

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/MrFloppaXBlu/geometry-dash-demonlist.git
   cd geometry-dash-demonlist
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your settings:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://user:password@localhost:5432/demonlist_db
   SECRET_KEY=your-secret-key-here
   ```

5. **Initialize database**
   ```bash
   flask init-db
   ```

6. **Create admin user**
   ```bash
   flask create-admin
   ```
   Follow the prompts to create your first admin account.

7. **Run the application**
   ```bash
   flask run
   ```
   The app will be available at `http://localhost:5000`

## Usage 🎯

### For Users
1. Visit the homepage to browse the demonlist
2. Click on any challenge to see details and verified completions
3. Submit your own completion (feature for future versions)

### For Mods
1. Register or login with your mod account
2. Access the **Mod Panel** from the navigation menu
3. **Add Challenge**: Click "Add New Challenge" button and fill in:
   - Placement number
   - Challenge name
   - Difficulty tier
   - Point value
   - Description (optional)
   - Verification video URL (optional)
4. **Manage Submissions**: Click "Review Submissions" to approve/reject player submissions
5. **Edit/Delete**: Use the edit/delete buttons on the dashboard to modify challenges

## Project Structure 📁

```
.
├── app.py                 # Main Flask application with all routes
├── models.py              # Database models (User, Challenge, Submission)
├── config.py              # Configuration for different environments
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── templates/             # HTML templates
    ├── base.html          # Base template with navigation
    ├── index.html         # Main demonlist page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── challenge.html     # Individual challenge view
    ├── 404.html           # 404 error page
    ├── 500.html           # 500 error page
    └── mod/               # Mod panel templates
        ├── dashboard.html     # Mod dashboard overview
        ├── add_challenge.html # Add new challenge form
        ├── edit_challenge.html# Edit challenge form
        └── submissions.html   # Manage submissions
```

## Database Schema 💾

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Hashed password
- `is_mod`: Boolean flag for mod status
- `is_admin`: Boolean flag for admin status
- `created_at`: Account creation timestamp

### Challenges Table
- `id`: Primary key
- `placement`: Unique placement number
- `name`: Challenge name
- `difficulty`: Difficulty tier
- `points`: Point value
- `creator_id`: Foreign key to Users
- `description`: Challenge description
- `video_url`: Verification video URL
- `created_at`: Challenge creation timestamp
- `updated_at`: Last update timestamp

### Submissions Table
- `id`: Primary key
- `challenge_id`: Foreign key to Challenges
- `player_name`: Player's name
- `video_url`: Completion video URL
- `status`: Status (pending, approved, rejected)
- `created_at`: Submission timestamp

## API Endpoints 🔌

### Public Routes
- `GET /` - Home page with demonlist
- `GET /challenge/<id>` - View challenge details
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Registration page
- `POST /register` - Process registration
- `GET /logout` - Logout user

### Mod Routes (Requires Authentication)
- `GET /mod/dashboard` - Mod dashboard
- `GET /mod/add-challenge` - Add challenge form
- `POST /mod/add-challenge` - Create new challenge
- `GET /mod/edit-challenge/<id>` - Edit challenge form
- `POST /mod/edit-challenge/<id>` - Update challenge
- `POST /mod/delete-challenge/<id>` - Delete challenge
- `GET /mod/submissions` - View pending submissions
- `POST /mod/approve-submission/<id>` - Approve submission
- `POST /mod/reject-submission/<id>` - Reject submission

## Future Features 🚀

- [ ] Player submission system for completions
- [ ] Leaderboard for players
- [ ] User profiles and statistics
- [ ] Comments/discussion on challenges
- [ ] Mobile app
- [ ] Difficulty voting system
- [ ] Integration with actual Geometry Dash stats
- [ ] API for external integrations

## Contributing 🤝

To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📜

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the maintainers

## Acknowledgments 🙏

- Inspired by [Pointercrate](https://pointercrate.com/) - The official Geometry Dash demonlist
- Built with Flask and modern web technologies

---

**Made with ❤️ for the Geometry Dash community**
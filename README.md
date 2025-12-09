# PlayTested ⚡️

**Game reviewing platform**

This platform creates a social space for those who care about games to discuss their favorites, and their least favorites. The platform is designed for avid gamers.

## Features

- Write and publish reviews
- Rate reviews on whether you agree or disagree with them
- Add friends and view their profiles

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 5.2.6 |
| Database | SQLite3 |
| Frontend | HTML, CSS (custom styling) |
| API Integration | IGDB (Twitch) API |
| Authentication | Django Auth |
| Image Handling | Pillow |

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/bipgoppa/game_review_platform.git
   cd game_review_platform
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create an `env` file in the `game_review_platform` directory with IGDB API credentials.
   
   To get IGDB API credentials:
   - Register at [Twitch Developers](https://dev.twitch.tv/)
   - Create an application
   - Use the Client ID and Client Secret

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
game_review_platform/
│
├── IGDReviews/              # Reviews app - game search and reviews
│   ├── forms.py             # Review and search forms
│   ├── models.py            # Review and Vote models
│   ├── views.py             # Review CRUD operations
│   ├── igdb_api.py          # IGDB API integration
│   └── urls.py              # Review-related URLs
│
├── feed/                    # Main feed app
│   ├── views.py             # Feed display logic
│   ├── static/feed/css/     # Main stylesheet
│   └── templates/feed/      # Feed templates
│
├── profiles/                # User profiles and social features
│   ├── models.py            # Profile and Friendship models
│   ├── views.py             # Profile management
│   ├── forms.py             # Profile forms
│   └── signals.py           # Auto-create profiles
│
├── login/                   # Authentication app
│   ├── views.py             # Login/logout functionality
│   └── forms.py             # Login forms
│
├── create_account/          # User registration
│
├── templates/               # Shared templates
│   ├── reviews/             # Review templates
│   └── profiles/            # Profile templates
│
├── media/avatars/           # User-uploaded avatars
│
├── game_review_platform/    # Project settings
│   ├── settings.py          # Django settings
│   └── urls.py              # Main URL routing
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── env                      # Environment variables (DO NOT COMMIT)
└── .gitignore               # Git ignore rules
```

### Key Directories Explained

- **IGDBReviews/** - Review functionality including game search using IGDB API, creating/editing/deleting reviews, and the voting system
- **feed/** - Displays user reviews, friend reviews, and highest rated reviews. Also includes all CSS styling
- **profiles/** - Manages user profiles, avatars, bios, and the ability to send/accept friend requests
- **login/** & **create_account/** - Handles user authentication, registration, and session management
- **templates/** - Shared HTML templates organized by feature. Uses Django template inheritance

## Usage

### Creating an Account

1. Go to the Home page
2. Click "Don't have an account? Create one"
3. Fill in your desired username, email, and password
4. Log in with your new credentials

### Writing a Review

1. Log in to your account
2. Use search bar to find a game
3. Click "Write a review" on game card
4. Fill in the review:
   - Playtime (hours)
   - Review title
   - Message/description of review
   - Star rating (1-5)
5. Submit your review

### Adding Friends

1. Go to the "Friends" page
2. Enter a username in the "Send a Friend Request" section
3. The other user will receive the request
4. Once accepted, you'll see each other's reviews in the friend's feed

### Voting on Reviews

- Click the ▲ button to upvote a review
- Click the ▼ button to downvote a review
- Click again to remove your vote

### Filtering by Genre

1. On the feed page, use the "Filter by Genre" dropdown
2. Select a genre to see only reviews for games in that category
3. Click "Clear filter" to return all reviews

## Security Notes

- Keep your IGDB credentials secure
- Never commit your `env` file to version control

## Future Enhancements

- Advanced search filters
- User statistics dashboard
- Comment system on reviews

## Acknowledgements

- Game data provided by [IGDB API](https://www.igdb.com/api)
- Built with [Django](https://www.djangoproject.com/)
- Styling inspired by modern gaming platforms

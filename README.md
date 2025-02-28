# Sino: AI IELTS Tutor App

## Overview

Sino is an AI-powered IELTS tutor application designed to help users prepare for the IELTS exam through personalized practice sessions and feedback. The app features virtual coaches, practice tests, and performance analytics.

## Features

- User registration and authentication with mother tongue selection
- Multiple virtual coaches with unique personalities
- IELTS practice tests with reading passages and various question types
- Real-time test timer and question navigation
- Automatic test scoring and performance feedback
- User statistics tracking (average IELTS score, practice count, rating)

## Technology Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default)
- **Forms**: django-crispy-forms with crispy-bootstrap5
- **Media Handling**: Pillow

## Project Structure

```
sino/
├── accounts/             # User authentication and profiles
├── core/                 # Homepage and navigation components
├── practice/             # Practice test functionality
├── sino/                 # Main project settings
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded content
│   └── coach_images/     # Coach profile images
├── templates/            # HTML templates
├── initial_data.py       # Initial data loading script
├── deploy.sh             # Deployment script
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd sino
```

### Step 2: Set Up Virtual Environment

```bash
python -m venv sino_env
```

Activate the virtual environment:

- On Windows:
  ```bash
  sino_env\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source sino_env/bin/activate
  ```

### Step
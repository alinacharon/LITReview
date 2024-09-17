# LITReview - Book Review Platform

LITReview is a Django-based web application that allows users to request and publish book reviews. Users can follow each other, create tickets for book review requests, and write reviews for books.

## Features

- User authentication (signup, login, logout)
- Follow/unfollow other users
- Create tickets (book review requests)
- Write reviews for books (with or without an existing ticket)
- View a personalized feed of tickets and reviews from followed users
- Edit and delete your own tickets and reviews

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/alinacharon/LITReview.git
   cd litreview
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Apply database migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser (admin) account:
   ```
   python manage.py createsuperuser
   ```

## Running the Application

1. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. Open a web browser and go to `http://127.0.0.1:8000/` to access the application.

## Usage

- Register a new account or log in with existing credentials.
- Use the navigation menu to access different features:
  - Create a ticket to request a book review
  - Write a review for a book
  - View your feed to see posts from users you follow
  - Manage your follows/followers
  - View and manage your own posts

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` using the superuser credentials you created earlier. Here you can manage users, tickets, and reviews.

## Configuration

- The main configuration file is `base/settings.py`.
- To change the language or time zone, modify the `LANGUAGE_CODE` and `TIME_ZONE` settings.



# Nazbeen_Online_PlatForm

# E-Learning Platform

This project is a comprehensive e-learning platform built with Django, offering features for course management, user enrollment, lesson organization, and interactive quizzes. It allows instructors to create and manage courses, students to enroll, and facilitates learning through a structured model.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Models Overview](#models-overview)
- [Credits](#credits)

---

## Features

- **Course Creation and Management:** Instructors can create and manage courses with associated modules, lessons, and quizzes.
- **User Enrollment and Tracking:** Students can enroll in courses, and their enrollment status is tracked.
- **Content Organization:** Courses are categorized by subject and can include various modules and lessons.
- **Media Integration:** Supports Cloudinary for storing images, videos, and PDFs.
- **Interactive Quizzes:** Courses can include quizzes with various question types.
- **User Notifications:** Instructors receive notifications when students enroll or interact with courses.
- **Customizable Access Levels:** Courses can be made public, email-restricted, or free.

---

## Requirements

- **Python 3.12**
- **Django** (latest stable version)
- **Cloudinary** (for image and video storage)
- **Django REST Framework** (optional, for API endpoints)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/e-learning-platform.git
   cd e-learning-platform
   ```

2. **Install Dependencies:**

   Use `pip` to install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Cloudinary:**

   Ensure you have a Cloudinary account and set your Cloudinary environment variables. You can initialize it in `helpers.py`:

   ```python
   import cloudinary
   cloudinary.config(
       cloud_name="your-cloud-name",
       api_key="your-api-key",
       api_secret="your-api-secret"
   )
   ```

4. **Run Migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

---

## Configuration

### Cloudinary

This platform uses Cloudinary to handle images, videos, and other media files. Make sure to set up your Cloudinary configuration in the `helpers.py` file as described above.

### Course Access Levels

Courses can be configured to restrict access based on the following levels:
- **Anyone** - Public access to anyone.
- **Email Required** - Requires an email to access.

---

## Usage

1. **Create Categories and Subjects:**

   Log in as a superuser and create course categories and subjects through the admin panel.

2. **Add Courses:**

   Courses can be added with details such as the instructor, access level, price, and status (draft, published, coming soon).

3. **Organize Content:**

   - **Modules and Lessons:** Organize course content by adding modules and lessons to each course.
   - **Quizzes:** Attach quizzes to modules with different types of questions to assess learning.

4. **User Enrollment:**

   Users can enroll in courses and track their progress.

5. **Interactive Features:**

   Users can interact with courses through likes, comments, and by viewing notifications of updates or new content.

---

## Models Overview

### Core Models

- **Category:** Represents the category under which courses are grouped.
- **Subject:** Each course is related to a specific subject.
- **Course:** The main model representing courses. Includes fields for instructor, students, access level, and media resources (image, video, PDF).

### Supporting Models

- **Module:** Organizes lessons within a course.
- **Lesson:** Represents individual lessons within modules.
- **LessonVideo:** Stores video content related to lessons.
- **Quiz:** Allows quizzes to be attached to courses with various question types.

### User Models

- **Student:** Extends the user model to include courses they are enrolled in.
- **Enrollment:** Tracks the enrollment of a student in a course with status options.
- **Likes:** Represents likes by users for specific courses.

### Interaction Models

- **Question:** Represents a question in a quiz, with options for multiple-choice or true/false formats.
- **Answer:** Stores answer choices for each question.
- **Notification:** Used to notify instructors about course interactions.

---

## Credits

This project is built with Django and relies on Cloudinary for media storage. Contributions from the open-source community have helped shape various aspects of this platform.

---


# CareerBridge — Django Job Board Platform

**A full-stack job board and recruitment management platform built with Django and Django REST Framework.**

CareerBridge connects job seekers with employers through a modern web interface and a role-based recruitment system. Candidates can explore jobs, upload resumes, submit applications, and track their progress. Employers can manage job listings, review applications, and update candidate statuses.

Developed as part of the **CodeAlpha Backend Development Internship — October 2026**.

---

## Project Overview

CareerBridge demonstrates backend development through authentication, database management, RESTful APIs, secure file handling, application tracking, and role-based permissions.

The project combines a responsive frontend with a Django backend to simulate a realistic recruitment workflow.

## Key Features

### Candidate Features

- Browse available job opportunities.
- Search and filter jobs by keyword, location, and employment type.
- View detailed job descriptions.
- Upload PDF resumes.
- Apply for jobs with an uploaded resume and optional cover letter.
- Prevent duplicate applications for the same job.
- Track application statuses through a personal dashboard.
- Download uploaded resumes securely.

### Employer Features

- Create and manage job postings.
- View job listings associated with the employer.
- Review applications received for posted jobs.
- Update application statuses, including Pending, Reviewed, and Shortlisted.
- View recruitment statistics through an employer dashboard.
- Access candidate resumes through protected endpoints.

### Security Features

- User authentication and session management.
- Role-based permissions for candidates and employers.
- Ownership checks for employer job management.
- Protection against duplicate applications.
- Restricted resume access.
- File upload validation.
- CSRF protection for authenticated web requests.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Backend programming |
| Django 6.1.2 | Web framework |
| Django REST Framework 3.18.3 | RESTful API development |
| SQLite | Relational database |
| HTML5 | Page structure |
| CSS3 | Responsive frontend styling |
| JavaScript | Interactive functionality |
| Pillow | Image-processing dependency |
| Git and GitHub | Version control and project hosting |

## Project Structure

The repository contains the following principal directories and files:

- `careerbridge/` — Django configuration, URL routing, and website views.
- `jobs/` — Models, serializers, API views, permissions, migrations, and tests.
- `templates/` — Website pages and dashboard templates.
- `static/` — Stylesheets, JavaScript, and static assets.
- `screenshots/` — Project demonstration screenshots.
- `manage.py` — Django management utility.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Excluded local and private files.

## Installation and Setup

### 1. Clone the repository

Clone the CareerBridge repository from GitHub and navigate into its directory.

### 2. Create a virtual environment

On Windows:

`python -m venv .venv`

Activate the environment:

`.venv\Scripts\activate`

### 3. Install dependencies

`pip install -r requirements.txt`

### 4. Apply database migrations

`python manage.py migrate`

### 5. Create an administrator account

`python manage.py createsuperuser`

### 6. Start the development server

`python manage.py runserver`

Open the website at:

`http://127.0.0.1:8000/`

**Note:** The project uses locally configured settings and a development database. Ensure required Django settings and environment variables are configured before running it outside the original development environment.

## Application Pages

| Page | Local URL |
|---|---|
| Homepage | `/` |
| Browse Jobs | `/jobs/` |
| Job Details | `/jobs/<job_id>/` |
| Apply for a Job | `/jobs/<job_id>/apply/` |
| Candidate Dashboard | `/dashboard/candidate/` |
| Employer Dashboard | `/dashboard/employer/` |
| Django Administration | `/admin/` |

## REST API

CareerBridge uses Django REST Framework to support recruitment operations.

Example endpoints include:

| Endpoint | Purpose |
|---|---|
| `/api/candidate/resumes/` | Candidate resume upload |
| `/api/employer/jobs/` | Employer job creation |
| `/api/employer/applications/` | View applications received by an employer |

Additional endpoints support job management, candidate applications, application-status updates, and protected resume downloads.

API access is governed by authentication, user roles, and ownership permissions.

## Automated Testing

The project includes Django automated tests covering backend functionality and access control.

Run Django's system checks:

`python manage.py check`

Run the automated tests:

`python manage.py test -v 2`

**Verified test result: 8 tests passed, 0 failures.**

Test coverage includes:

- Duplicate job application prevention.
- Candidate restrictions on employer-only operations.
- Employer job ownership enforcement.
- Application-status update permissions.
- Candidate resume ownership.
- Authorized employer resume access.
- Protection against unrelated employers accessing private resumes.

## Project Screenshots

The `screenshots/` directory contains evidence of the completed application.

| Screenshot | Description |
|---|---|
| `01_homepage` | CareerBridge landing page |
| `02_job_listings` | Job search and listings |
| `03_job_details` | Detailed job information |
| `04_application_form` | Candidate application form |
| `05_already_applied.png` | Duplicate application protection |
| `06_candidate_dashboard` | Candidate application dashboard |
| `07_employer_dashboard` | Employer recruitment dashboard |
| `08_employer_applications` | Received applications |
| `09_application_success.png` | Successful application submission |
| `10_status_updated.png` | Employer application-status update |
| `11_tests_passed.png` | Automated Django test results |

Screenshots document the major user workflows and backend testing outcomes.

## Example Workflow

**Candidate journey**

Browse jobs → View job details → Upload resume → Apply for job → Track application status.

**Employer journey**

Sign in → Manage job listings → Review candidate applications → Update application status.

These workflows demonstrate how the frontend, backend, database, and permission system work together.

## Privacy and Repository Safety

The Git repository excludes local development files, including:

- Python virtual environments.
- SQLite development databases.
- Uploaded resumes and media files.
- Local test documents.
- Environment files containing secrets.
- Python cache and temporary files.

The repository contains source code and demonstration screenshots rather than private candidate documents.

## Future Improvements

Potential improvements include email notifications, enhanced employer recruitment tools, pagination, automated deployment, additional automated tests, and production database support.

## Project Status

**Functional local development project.**

Core candidate and employer workflows have been demonstrated, and all eight existing automated Django tests have passed.

The application has not been represented as a production-deployed service.

## Internship

**Program:** CodeAlpha Backend Development Internship

**Project:** CareerBridge — Job Board Platform

**Period:** October 2026

**Focus:** Django backend development, REST APIs, database integration, authentication, authorization, file handling, and automated testing.

---
## Author

**Kaunain Gul Khalid**
Backend Development Intern | CodeAlpha — October 2026

Passionate about Python, Django, backend development, RESTful APIs, and building practical software applications.

**GitHub:** [https://github.com/Kaunaingul-ai]

**LinkedIn:** [https://www.linkedin.com/in/kaunain-gul-khalid-283949427/]


*CareerBridge — Connecting talent with opportunity.*

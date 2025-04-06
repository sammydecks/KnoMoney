omg hi guys <3 - Sammy

Hi yall :D - Mimi

# Project Overview

KnoMoney is a platform where students can know their money before they have no money.

KnoMoney empowers college students to take control of their finances by understanding and minimizing their student loan debt for a more secure financial future.

# Features

📊 **Accrued Interest Calculator:** Calculate the total interest that have accrued on federal unsubsidized loans.

📰 **FAQ:** Understand terms related to student loans and the calculator.

# Tech Stack

- **Backend:** Django
- **Frontend:** Bootstrap
- **Database:** PostgreSQL & Amazon AWS
- **APIs:** N/A

# Installation & Setup

## Clone Repository

```
git clone https://github.com/sammydecks/KnoMoney.git
cd project-name
```

## Database Setup

Resources:

- https://www.youtube.com/watch?v=z_FN0Zu-Z3Q

1. Install `pip install psycopg2-binary` and `postgresql` in virtual environment
2. Create AWS database and update settings.py (Following already done!)
3. Edit inbound rules to connect django application to postgreSQL application
4. Migrate database files to postgreSQL with `python3 manage.py makemigrations` and `python3 manage.py migrate`
5. Can add superuser with `python3 manage.py createsuperuser` (already created below to use!)

**Admin Account**

1. Start local host: `python3 manage.py runserver`
2. Write 'admin' in url name: `http://127.0.0.1:8000/admin`
3. Log in with credentials (Username: admin | Password: same as knoyourmoney@gmail.com)

Debugging Issues: If there is a `CSRF verification failed`, turn on all browser cookies in web browser.

### Amazon AWS Information

- DB Instance Identifier: knomoney-database
- Credentials - Master Username: knomoney_team
- Database Name: knomoney_database

### Dbeaver Connection to Amazon RDS Instance

- https://www.youtube.com/watch?v=_Yzr7yBGWQI

1. Create RDS instance and copy endpoint
2. Add in username and password and connect

- https://www.youtube.com/watch?v=RDH5yZHNYdI

Test: `python3 manage.py dbshell`

### Local database setup for development

1. Install PostgreSQL (MacOS)
   `brew update`
   `brew install postgresql`
   `brew services start postgresql`

2. Create local user and database
   `psql postgres`
   `CREATE USER knomoney_dev WITH PASSWORD 'password';`
   `CREATE DATABASE knomoney_local OWNER knomoney_dev;`

3. Run database migrations
   `python3 manage.py migrate`

4. Create superuser to log into admin interface
   `python3 manage.py createsuperuser`

### CRUD Operations

- https://docs.djangoproject.com/en/5.1/topics/db/models/

## Install Dependencies

```
pip install -r requirements.txt  # For Django
```

For MacOS:

1. Create virtual environment: `python3 -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install any dependencies: ex. `pip3 install django`
4. Exit virtual environment: `deactivate`

## Run the Server

```
python manage.py runserver  # For Django
```

# Version Control

## General Process

1. `cd` into correct directory
2. Pull from main branch `git pull origin main`
3. Create new branch `git branch [branchname]`
4. Change to branch `git checkout [branchname]`
5. Make changes to code
6. Add changed code into local repo `git add .`
7. Commit changed code `git commit -m [comment]`
8. Push branch to remote repo `git push`
9. Create PR in GitHub

# User Guide

1. User starts on the Landing Page
2. User clicks on the "Save Now" button
3. User is redirected to the calculator page
4. User fills in loan information including the following fields:
   - Graduation Date
   - Loan Amount
   - Interest Rate
   - Loan Type (subsidized, unsubsidized)
   - Date Received
5. User clicks the "Add Loan" button to fill in all their loans
6. User clicks "Calculate" button
7. Results and recommendations generate below the calculator inputs

# Roadmap & Next Steps

1. Deploy website
2. Beta user feedback & iterations
3. Launch

# Team and Contributions

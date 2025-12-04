🕒 TimeClock Backend API

The TimeClock Backend API is a Django + Django REST Framework project designed to manage employee attendance, clock-in/clock-out tracking, and working hours calculations.
It provides secure RESTful endpoints to handle authentication, store attendance data, and deliver real-time reporting for HR and management dashboards.

🚀 Features
1. Authentication & Security

🔐 JWT-based authentication (access & refresh tokens)

Role-based access (e.g., Admin, Employee, Manager)

Token auto-refresh using DRF SimpleJWT

2. Clock-In / Clock-Out Management

Employees can clock in and clock out via API

Tracks:

Time-in & time-out

Date of attendance

Geolocation support (optional)

Descriptions for time-in/out remarks

3. Attendance Overview

Fetch all attendance records per user

Get attendance summary by date, week, month, or year

Handle late logins and early logouts

4. Reporting & Analytics

Calculate total worked hours per day, week, and month

Generate reports filtered by user, department, or date

Export-ready JSON response for integration with dashboards

🔗 API Endpoints
Authentication
Method	Endpoint	Description
POST	/api/auth/login/	Login & get tokens
POST	/api/auth/refresh/	Refresh access token
POST	/api/auth/register/	Register new user
Attendance
Method	Endpoint	Description
GET	/api/timeclock/<user_id>/	Get user’s attendance
POST	/api/timeclock/clock-in/	Clock in
POST	/api/timeclock/clock-out/	Clock out
GET	/api/timeclock/summary/	Get attendance summary
⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/timeclock-backend.git
cd timeclock-backend

2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables

Create a .env file:

SECRET_KEY=your_django_secret
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/timeclock

5. Run migrations
python manage.py migrate

6. Start the server
python manage.py runserver

📌 Example API Usage

Clock In Example

POST /api/timeclock/clock-in/
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>

{
  "userId": "a12b34c5-d678-90ef-gh12-ijk345lmn678",
  "timeIn": "08:45:00",
  "timeInDescription": "Arrived early",
  "timeInLocation": "HQ Office",
  "date": "2025-08-20"
}


Successful Response

{
  "status": "success",
  "message": "Clock-in recorded successfully",
  "data": {
    "userId": "a12b34c5-d678-90ef-gh12-ijk345lmn678",
    "timeIn": "08:45:00",
    "timeInDescription": "Arrived early",
    "timeInLocation": "HQ Office",
    "date": "2025-08-20"
  }
}

🧩 Future Improvements

⏱ Real-time tracking using WebSockets

📊 Advanced analytics dashboards

🌎 Multi-branch geolocation tracking

📥 CSV/Excel export for attendance reports

🧑‍💻 Author

TimeClock Development Team
📧 support@timeclock.com
🔗 GitHub
# Django-Attendance

### College-ERP Project

Welcome to the College-ERP Project! This project is a comprehensive web-based application built using Flask and PyMongo. It aims to streamline and manage various aspects of a college's operations, including student management, staff management, attendance tracking, and department management. The application includes secure authentication mechanisms and is designed to be easily extensible.

---

## Features

### 1. **User Authentication and Authorization**
   - **JWT Authentication:** Secure access to resources using JSON Web Tokens (JWT).
   - **Role-based Access Control:** Permissions are assigned based on user roles (e.g., Admin, Staff, Student).
   - **Token Management:** Expired and revoked tokens are handled securely.

### 2. **Student Management**
   - Register and manage student details such as name, email, phone, department, batch, semester, etc.
   - Update student information with strict validation and secure password handling.
   - Fetch details of specific students or a list of all students.

### 3. **Staff Management**
   - Register staff members with specific roles (e.g., Admin, Staff).
   - Secure login for staff members with appropriate role-based permissions.
   - Admins have the ability to manage staff details.

### 4. **Attendance Tracking**
   - Record and retrieve attendance data for students.
   - Manage attendance records efficiently.

### 5. **Department Management**
   - Add and manage different departments within the college.
   - Assign staff and students to respective departments.

### 6. **Comprehensive API Documentation**
   - **Swagger UI**: Interactive API documentation using Swagger UI, making it easy to test and explore the API.

---

## Project Structure

```plaintext
College-ERP/
│
├── routes/
│   ├── staff.py                # Routes for staff management
│   ├── student.py              # Routes for student management
│   ├── user.py                 # Routes for user authentication (login/logout)
│   ├── attendance.py           # Routes for attendance management
│   └── department.py           # Routes for department management
│
├── models/
│   └── schema.py               # Database schemas and data validation using Marshmallow
│
├── helper/
│   └── authorize.py            # Authorization utilities for role-based access control
│
├── log_services/
│   └── logger.py               # Logging configuration and utilities
│
├── db/
│   └── mongo.py                # MongoDB setup and initialization
│
├── blocklist.py                # Blocklist for managing revoked JWTs
├── app.py                      # Main application entry point
├── .env                        # Environment variables for configuration
└── README.md                   # Project documentation (this file)
```

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/college-erp.git
   cd college-erp
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Create a `.env` file in the root directory and add the following variables:
     ```plaintext
     MONGO_URL=your_mongo_uri
     JWT_KEY=your_jwt_secret_key
     ```

5. **Run the Application:**
   ```bash
   flask run
   ```

6. **Access the API Documentation:**
   - Open your browser and navigate to `http://localhost:5000/swagger-ui/` to explore the API documentation.

---

## Usage

### **Student Management**

- **Register a Student:**
  - Endpoint: `POST /register/student`
  - Payload:
    ```json
    {
      "name": "John Doe",
      "email": "john@student.com",
      "phone": 1234567890,
      "dept": "Computer Science",
      "batch": 2022,
      "sem": 4,
      "password": "password123"
    }
    ```

- **Get All Students:**
  - Endpoint: `GET /student`

- **Update Student Details:**
  - Endpoint: `PUT /student/<student_id>`
  - Payload: Include only the fields you want to update.

- **Delete a Student:**
  - Endpoint: `DELETE /student/<student_id>`

### **Staff Management**

- **Register a Staff Member:**
  - Endpoint: `POST /register/staff`
  - Payload: Similar to student registration but with a staff email pattern.

- **Get All Staff Members:**
  - Endpoint: `GET /staff`

### **Attendance Management**

- **Record Attendance:**
  - Endpoint: `POST /attendance`
  - Payload:
    ```json
    {
      "student_id": "student_id",
      "date": "YYYY-MM-DD",
      "present": true
    }
    ```

### **Department Management**

- **Add a Department:**
  - Endpoint: `POST /department`
  - Payload:
    ```json
    {
      "name": "Computer Science"
    }
    ```

---

## Logging

- The application uses a customizable logging setup that records activities, errors, and other key events. Logging is configured to handle different environments, including development and production.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For any inquiries or support, please contact [your-email@example.com].

---

Thank you for using the College-ERP Project! We hope it helps streamline your college operations effectively.
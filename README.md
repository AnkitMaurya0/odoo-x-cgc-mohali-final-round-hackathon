# RoadGuard - Roadside Assistance Management System

A comprehensive Flask web application designed for managing roadside assistance services, connecting customers with mechanics and workers for efficient service delivery.

## 🚗 Project Overview

RoadGuard is a multi-role platform that streamlines the roadside assistance process by connecting:
- **Customers** seeking roadside assistance
- **Mechanics** managing shops and service requests  
- **Workers** executing assigned tasks in the field

## 🏆 Odoo Hackathon Submission

This project is developed for the Odoo Hackathon, demonstrating modern web application architecture with role-based access control, geolocation services, and real-time task management.

## ✨ Key Features

### For Customers
- **Location-based Shop Discovery**: Find nearby mechanics using Haversine distance calculation
- **Service Request Management**: Submit detailed service requests with GPS coordinates
- **Real-time Status Tracking**: Monitor request progress from submission to completion
- **Service History**: View past service requests and their outcomes

### For Mechanics
- **Shop Management**: Manage shop details, services, and location
- **Employee Management**: Add, edit, and manage worker accounts with secure authentication
- **Request Processing**: View and process incoming service requests
- **Task Assignment**: Assign specific requests to available workers
- **Work Monitoring**: Track progress of all assigned tasks in real-time

### For Workers
- **Task Dashboard**: View assigned tasks with customer and location details
- **Status Updates**: Update task progress (Assigned → In Progress → Completed)
- **Location Integration**: Access customer location coordinates for navigation
- **Mobile-friendly Interface**: Optimized for field work

## 🔧 Technical Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with proper relational design
- **Security**: Werkzeug password hashing
- **Frontend**: HTML/CSS/JavaScript with responsive design
- **Geolocation**: Haversine formula for distance calculations
- **Session Management**: Flask sessions for user authentication

## 📊 Database Schema

```sql
- customers (id, name, email, password)
- mechanics (id, name, email, password)  
- mechanic_shops (id, mechanic_id, shop_name, address, phone, services, lat, lon)
- employees (id, mechanic_id, name, email, password, role)
- service_requests (id, customer_id, shop_id, service_type, location, status, created_at)
- assigned_tasks (id, request_id, employee_id, status)
- feedback (id, employee_id, rating, comment)
```

## 🚀 Installation & Setup

### Prerequisites
```bash
Python 3.7+
Flask
SQLite3
```

### Installation Steps

1. **Clone the Repository**
```bash
git clone <repository-url>
cd roadguard
```

2. **Install Dependencies**
```bash
pip install flask werkzeug
```

3. **Database Setup**
```bash
# Create SQLite database with required tables
python setup_database.py  # (create this script based on schema)
```

4. **Run the Application**
```bash
python app.py
```

5. **Access the Application**
```
http://localhost:5000
```

## 📱 Usage Guide

### Getting Started

1. **Registration**
   - Customers: Sign up with basic details
   - Mechanics: Register with shop information and location
   - Workers: Added by mechanics through employee management

2. **Customer Workflow**
   ```
   Login → Find Shops → Request Service → Track Status
   ```

3. **Mechanic Workflow**
   ```
   Login → View Requests → Assign to Workers → Monitor Progress
   ```

4. **Worker Workflow**
   ```
   Login → View Tasks → Update Status → Complete Service
   ```

## 🔒 Security Features

- **Password Security**: Werkzeug-based password hashing with salt
- **Session Management**: Secure user sessions with role-based access
- **Input Validation**: Protection against SQL injection
- **Role-based Authorization**: Different access levels for each user type

## 🌍 Geolocation Features

- **Distance Calculation**: Haversine formula for accurate distance measurement
- **Shop Filtering**: Filter mechanics by distance radius
- **Location Storage**: GPS coordinates stored for service requests
- **Navigation Support**: Location data available for worker navigation

## 📈 System Architecture

```
User Interface Layer
    ↓
Flask Application Layer (Routes & Business Logic)
    ↓
Database Layer (SQLite with proper relationships)
    ↓
Security Layer (Password hashing & Session management)
```

## 🔧 Configuration

### Environment Variables
```python
SECRET_KEY = "your_secret_key"  # Change in production
DEBUG = True  # Set to False in production
```

### Database Configuration
- Database: `RoadGuard.db` (SQLite)
- Connection pooling handled by Flask
- Row factory set for dict-like access

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📋 API Endpoints

### Authentication
- `GET/POST /login` - User authentication
- `GET /logout` - User logout
- `GET/POST /signup/customer` - Customer registration
- `GET/POST /signup/mechanic` - Mechanic registration

### Customer Routes
- `GET /customer/dashboard` - Customer dashboard
- `GET /view_shops` - View nearby shops
- `GET/POST /request_service` - Service request form
- `GET /my_request` - View request history

### Mechanic Routes
- `GET /mechanic/dashboard` - Mechanic dashboard
- `GET/POST /add_employee` - Employee management
- `GET /employee_list` - View all employees
- `GET/POST /assign_work/<id>` - Task assignment
- `GET /work_status` - Monitor all tasks

### Worker Routes
- `GET /worker_dashboard` - Worker task dashboard
- `POST /update_work_status/<id>` - Update task status

## 🐛 Known Issues & Limitations

- Location services require browser permission
- Real-time notifications not implemented
- Payment integration pending
- Mobile app not available (web-responsive only)

## 🚀 Future Enhancements

- Real-time WebSocket notifications
- Payment gateway integration
- Mobile application development
- Advanced analytics dashboard
- Multi-language support
- Integration with mapping services

## 📞 Support

For technical support or queries regarding this Odoo Hackathon submission:
- Create an issue in the repository
- Contact the development team

## 📄 License

This project is developed for the Odoo Hackathon. License terms to be determined.

---

**Built with ❤️ for Odoo Hackathon**

*Connecting customers with reliable roadside assistance through technology*

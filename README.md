# RoadGuard - Roadside Assistance Management System

**Team Name:** Smart Coder  
**Team Leader:** Ankit Kumar</br>
**Team No:** 52</br>
**Submission Video:** [Watch Demo](https://drive.google.com/file/d/1Lf7G4UnggtF5H3Yxc_nixUv6DAJeOiB_/view?usp=sharing)

---

## Project Overview

RoadGuard is a comprehensive Flask web application designed for managing roadside assistance services, connecting customers with mechanics and workers for efficient service delivery. This multi-role platform streamlines the roadside assistance process through intelligent geolocation, task management, and real-time status tracking.

## Odoo Hackathon Submission

This project represents Team Smart Coder's innovative solution for the Odoo Hackathon, demonstrating modern web application architecture with role-based access control, geolocation services, and comprehensive task management capabilities.

## Problem Statement

Traditional roadside assistance faces several challenges:
- Difficulty finding nearby service providers
- Lack of real-time communication between customers and mechanics
- Inefficient task assignment and tracking
- Poor coordination between mechanics and field workers
- Limited visibility into service request status

## Solution Architecture

RoadGuard addresses these challenges through:
- **Location-based Service Discovery** using Haversine distance calculations
- **Multi-role Dashboard System** for customers, mechanics, and workers
- **Real-time Task Management** with status tracking
- **Secure Authentication System** with password hashing
- **Responsive Design** optimized for both desktop and mobile use

## Key Features & Functionality

### Customer Portal
- **Smart Shop Discovery**: Find nearby mechanics using GPS coordinates and distance filtering
- **Detailed Service Requests**: Submit requests with location, issue description, and service type
- **Real-time Tracking**: Monitor request status from submission to completion
- **Service History**: Access complete history of past service requests
- **Distance-based Filtering**: Filter mechanics by proximity (1km, 5km, 10km+ options)

### Mechanic Management System
- **Comprehensive Shop Management**: Manage shop details, services offered, and operating hours
- **Employee Administration**: Add, edit, and manage worker accounts with role-based permissions
- **Request Processing Hub**: View and process incoming customer service requests
- **Intelligent Task Assignment**: Assign specific requests to available workers based on skills and location
- **Performance Monitoring**: Track completion rates and worker performance metrics
- **Multi-shop Support**: Manage multiple service locations from single dashboard

### Worker Mobile Interface
- **Task Dashboard**: View assigned tasks with customer contact and location details
- **Progress Tracking**: Update task status through intuitive interface (Assigned → In Progress → Completed)
- **Location Integration**: Access customer GPS coordinates for navigation
- **Communication Tools**: Direct contact information for customer coordination
- **Work History**: Track completed assignments and performance

## Technical Implementation

### Technology Stack
- **Backend Framework**: Flask (Python 3.7+)
- **Database**: SQLite with optimized relational design
- **Security**: Werkzeug security for password hashing with salt
- **Frontend**: Responsive HTML5/CSS3/JavaScript
- **Geolocation**: Custom Haversine formula implementation
- **Session Management**: Flask secure session handling

### Database Architecture
```sql
customers table: User authentication and profile data
mechanics table: Mechanic owner information and credentials
mechanic_shops table: Shop details, services, and geolocation
employees table: Worker accounts with role-based access
service_requests table: Customer requests with full tracking
assigned_tasks table: Task assignments and status management
feedback table: Service rating and review system
```

### Security Implementation
- **Password Protection**: Werkzeug generate_password_hash() with automatic salting
- **Session Security**: Secure session management with role validation
- **SQL Injection Prevention**: Parameterized queries throughout application
- **Access Control**: Role-based route protection and authorization
- **Input Validation**: Server-side validation for all user inputs

## Installation & Setup Guide

### Prerequisites
```bash
Python 3.7 or higher
pip package manager
Web browser with location services
```

### Quick Start Installation
```bash
# Clone repository
git clone <repository-url>
cd roadguard

# Install required dependencies
pip install flask
pip install werkzeug

# Initialize database
python setup_database.py

# Start application
python app.py

# Access application
http://localhost:5000
```

### Database Setup
Create SQLite database with the following structure:
```sql
-- Execute these commands to set up the database
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT);
CREATE TABLE mechanics (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT);
CREATE TABLE mechanic_shops (id INTEGER PRIMARY KEY, mechanic_id INTEGER, shop_name TEXT, shop_address TEXT, phone TEXT, service_provided TEXT, latitude REAL, longitude REAL);
CREATE TABLE employees (id INTEGER PRIMARY KEY, mechanic_id INTEGER, name TEXT, email TEXT UNIQUE, password TEXT, role TEXT, phone TEXT);
CREATE TABLE service_requests (id INTEGER PRIMARY KEY, customer_id INTEGER, shop_id INTEGER, name TEXT, phone TEXT, issue TEXT, service_type TEXT, location TEXT, status TEXT, created_at DATETIME);
CREATE TABLE assigned_tasks (id INTEGER PRIMARY KEY, request_id INTEGER, employee_id INTEGER, status TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE feedback (id INTEGER PRIMARY KEY, employee_id INTEGER, rating INTEGER, comment TEXT);
```

## User Journey & Workflows

### Customer Experience
1. **Registration**: Sign up with email and secure password
2. **Location Discovery**: Allow GPS access for accurate shop finding
3. **Service Selection**: Choose from available mechanics and services
4. **Request Submission**: Provide detailed problem description and contact info
5. **Real-time Updates**: Receive status updates as work progresses
6. **Service Completion**: Rate and review the service experience

### Mechanic Operations
1. **Shop Setup**: Register business with location and services offered
2. **Team Management**: Add workers with specific roles and permissions
3. **Request Monitoring**: View incoming customer requests in real-time
4. **Task Distribution**: Assign work based on worker availability and expertise
5. **Progress Tracking**: Monitor all active jobs and completion status
6. **Performance Analysis**: Review completion metrics and customer feedback

### Worker Field Operations
1. **Daily Dashboard**: Check assigned tasks and priorities
2. **Customer Contact**: Access contact information and job details
3. **Navigation**: Use provided GPS coordinates for routing
4. **Status Updates**: Report progress at each phase of work
5. **Job Completion**: Mark tasks complete with final status

## API Endpoints & Routes

### Authentication Routes
- `GET/POST /login` - Multi-role user authentication with password verification
- `GET /logout` - Secure session termination
- `GET/POST /signup/customer` - Customer account creation
- `GET/POST /signup/mechanic` - Mechanic registration with shop setup

### Customer Management Routes
- `GET /customer/dashboard` - Customer portal with recent requests and nearby shops
- `GET /view_shops` - Location-based shop discovery with distance filtering
- `GET/POST /request_service` - Service request submission form
- `GET /my_request` - Customer request history and status tracking

### Mechanic Management Routes
- `GET /mechanic/dashboard` - Mechanic control panel with active requests
- `GET/POST /add_employee` - Worker account creation and management
- `GET /employee_list` - Team overview with edit/delete capabilities
- `GET/POST /assign_work/<request_id>` - Task assignment interface
- `GET /work_status` - Real-time monitoring of all assigned tasks
- `POST /update_task_status/<task_id>` - Task status modification

### Worker Interface Routes
- `GET /worker_dashboard` - Worker task overview with location data
- `POST /update_work_status/<task_id>` - Progress reporting interface

## Advanced Features

### Geolocation Services
- **Haversine Distance Calculation**: Accurate distance measurement between coordinates
- **Automatic Location Detection**: Browser-based GPS coordinate acquisition
- **Distance Filtering**: Customizable radius-based shop filtering (1km, 5km, 10km+)
- **Location Storage**: GPS coordinates saved with each service request
- **Navigation Integration**: Coordinate data formatted for map applications

### Real-time Management
- **Live Status Updates**: Task progress reflected across all dashboards
- **Instant Notifications**: Status changes visible immediately to relevant users
- **Dynamic Task Assignment**: Real-time assignment capabilities
- **Progress Monitoring**: Live tracking of work completion across teams

### Performance Optimization
- **Database Indexing**: Optimized queries for fast response times
- **Session Caching**: Efficient user data management
- **Responsive Design**: Mobile-optimized interface for field workers
- **Minimal Load Times**: Streamlined frontend with essential features

## Testing & Quality Assurance

### Security Testing
- Password hashing verification with multiple test cases
- Session security validation across different user roles
- SQL injection prevention testing with malicious inputs
- Access control verification for unauthorized route access

### Functionality Testing
- Multi-role authentication flow validation
- Geolocation accuracy testing with known coordinates
- Task assignment and status update workflow verification
- Database relationship integrity testing

## Deployment Considerations

### Production Setup
```python
# Configuration for production deployment
app.config['SECRET_KEY'] = 'secure-production-key'
app.config['DEBUG'] = False
app.config['DATABASE_URL'] = 'production-database-url'
```

### Scalability Features
- Database connection pooling for concurrent users
- Modular code structure for easy feature additions
- RESTful API design for potential mobile app integration
- Optimized queries for handling large datasets

## Future Development Roadmap

### Phase 1 Enhancements
- Real-time WebSocket notifications for instant updates
- Advanced search and filtering options for shops
- Customer feedback and rating system expansion
- Mobile application development for iOS and Android

### Phase 2 Integrations
- Payment gateway integration for seamless transactions
- Third-party mapping service integration (Google Maps, MapBox)
- SMS and email notification system
- Advanced analytics dashboard with business intelligence

### Phase 3 Scalability
- Multi-tenant architecture for franchise operations
- API development for third-party integrations
- Machine learning for predictive maintenance suggestions
- IoT integration for vehicle diagnostics

## Business Impact & Benefits

### For Customers
- Reduced wait times through efficient shop discovery
- Transparent pricing and service tracking
- 24/7 access to roadside assistance network
- Quality assurance through rating and feedback systems

### For Mechanics
- Increased visibility and customer reach
- Efficient workforce management and task distribution
- Performance analytics for business optimization
- Streamlined operations with digital workflows

### For Workers
- Clear task assignments with all necessary information
- Mobile-friendly interface for field operations
- Performance tracking and career development insights
- Efficient communication with customers and management

## Project Statistics

- **Total Routes**: 25+ API endpoints
- **Database Tables**: 7 optimized relational tables
- **User Roles**: 3 distinct user types with specific permissions
- **Security Features**: 5+ implemented security measures
- **Responsive Design**: Mobile-optimized interface
- **Geolocation**: Accurate distance calculations using Haversine formula

## Support & Documentation

### Technical Support
- Comprehensive inline code documentation
- Error handling with user-friendly messages
- Debug mode for development troubleshooting
- Structured logging for production monitoring

### User Documentation
- Role-specific user guides
- Video demonstration available at submission link
- FAQ section for common issues
- Contact information for technical assistance

## Team Smart Coder

**Team Leader**: Ankit Kumar  
**Project**: RoadGuard - Roadside Assistance Management System  
**Hackathon**: Odoo Hackathon Submission  
**Demo Video**: [View Complete Demonstration](https://drive.google.com/file/d/1Lf7G4UnggtF5H3Yxc_nixUv6DAJeOiB_/view?usp=sharing)

---

## License & Usage

This project is developed specifically for the Odoo Hackathon competition. All rights reserved by Team Smart Coder.

**Built with innovation and dedication for the Odoo Hackathon**

*Revolutionizing roadside assistance through intelligent technology solutions*

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Mechanics table (for shop owners login)
CREATE TABLE IF NOT EXISTS mechanics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Mechanic shops table
CREATE TABLE IF NOT EXISTS mechanic_shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mechanic_id INTEGER NOT NULL,
    shop_name TEXT NOT NULL,
    shop_address TEXT NOT NULL,
    phone TEXT NOT NULL,
    service_provided TEXT,
    latitude REAL,
    longitude REAL,
    FOREIGN KEY (mechanic_id) REFERENCES mechanics (id)
);

-- Employees table
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mechanic_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'worker',
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (mechanic_id) REFERENCES mechanics (id)
);

-- Service requests table
CREATE TABLE IF NOT EXISTS service_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    shop_id INTEGER,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    issue TEXT NOT NULL,
    service_type TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Assigned tasks table
CREATE TABLE IF NOT EXISTS assigned_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    status TEXT DEFAULT 'Assigned',
    FOREIGN KEY (request_id) REFERENCES service_requests (id),
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker_id INTEGER NOT NULL,
    worker_name TEXT,
    comment TEXT,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (worker_id) REFERENCES employees (id)
);

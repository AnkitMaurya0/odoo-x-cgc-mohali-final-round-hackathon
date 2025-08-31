from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import math
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "your_secret_key"   # session ke liye zaroori

# ---------- DB Connection ----------
def get_db_connection():
    conn = sqlite3.connect("RoadGuard.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Home Route ----------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


# ---------- Signup - Customer ----------
@app.route("/signup/customer", methods=["GET", "POST"])
def signup_customer():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO customers (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup_customer.html")


# ---------- Signup - Mechanic ----------
@app.route("/signup/mechanic", methods=["GET", "POST"])
def signup_mechanic():
    if request.method == "POST":
        owner_name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        shop_name = request.form["shop_name"]
        shop_address = request.form["shop_address"]
        services = request.form["services"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        password = request.form["password"]
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        # Step 1: Insert into mechanics (owner details)
        cur.execute(
            "INSERT INTO mechanics (name, email, password) VALUES (?, ?, ?)",
            (owner_name, email, hashed_password)
        )
        mechanic_id = cur.lastrowid  # get new mechanic's id

        # Step 2: Insert into mechanic_shops (shop details)
        cur.execute("""
            INSERT INTO mechanic_shops 
                (mechanic_id, shop_name, shop_address, phone, service_provided, latitude, longitude) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (mechanic_id, shop_name, shop_address, phone, services, latitude, longitude))

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup_mechanic_shop.html")


# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        # 1. Check Customer
        cur.execute("SELECT * FROM customers WHERE email=?", (email,))
        customer = cur.fetchone()
        if customer and check_password_hash(customer["password"], password):
            session["user"] = customer["email"]
            session["name"] = customer["name"]
            session["role"] = "customer"
            session["customer_id"] = customer["id"]
            conn.close()
            return redirect(url_for("customer_dashboard"))

        # 2. Check Mechanic
        cur.execute("SELECT * FROM mechanics WHERE email=?", (email,))
        mechanic = cur.fetchone()
        if mechanic and check_password_hash(mechanic["password"], password):
            session["user"] = mechanic["email"]
            session["name"] = mechanic["name"]
            session["role"] = "mechanic"
            session["mechanic_id"] = mechanic["id"]
            conn.close()
            return redirect(url_for("mechanic_dashboard"))

        # 3. Check Employee (Worker)
        cur.execute("SELECT * FROM employees WHERE email=?", (email,))
        worker = cur.fetchone()
        if worker and check_password_hash(worker["password"], password):
            session["user"] = worker["email"]
            session["name"] = worker["name"]
            session["role"] = "worker"
            session["worker_id"] = worker["id"]   # yaha worker id store ho rahi hai
            session["mechanic_id"] = worker["mechanic_id"]  # worker ka master mechanic
            conn.close()
            return redirect(url_for("worker_dashboard"))  # fixed (function name)

        conn.close()
        return "Invalid credentials!"

    return render_template("login.html")




# ---------- Dashboards ----------
@app.route("/customer/dashboard")
def customer_dashboard():
    if "role" in session and session["role"] == "customer":
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM customers WHERE id=?", (session["customer_id"],))
        customer = cur.fetchone()

        cur.execute("""SELECT * FROM service_requests 
                       WHERE customer_id=? 
                       ORDER BY created_at DESC LIMIT 3""",
                       (session["customer_id"],))
        recent_requests = cur.fetchall()

        cur.execute("SELECT * FROM mechanic_shops")
        shops = [dict(row) for row in cur.fetchall()]

        conn.close()
        return render_template("customer_dashboard.html",
                               customer=customer,
                               recent_requests=recent_requests,
                               shops=shops)
    return redirect(url_for("login"))


@app.route("/mechanic/dashboard")
def mechanic_dashboard():
    if "role" in session and session["role"] == "mechanic":
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch mechanic shop details
        cur.execute("SELECT * FROM mechanic_shops WHERE mechanic_id=?", (session["mechanic_id"],))
        shop = cur.fetchone()

        requests = []
        if shop:  
            
            cur.execute("""
                SELECT sr.id, sr.service_type, sr.status, c.name AS customer_name
                FROM service_requests sr
                JOIN customers c ON sr.customer_id = c.id
                WHERE sr.shop_id = ?
            """, (shop["id"],))
            requests = cur.fetchall()

        conn.close()

        return render_template(
            "mechanic_dashboard.html",
            user=session["user"],
            shop=shop,
            requests=requests
        )
    return redirect(url_for("login"))

@app.route("/worker_dashboard")
def worker_dashboard():
    
    if "role" not in session or session["role"] != "worker":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()

    
    cur.execute("""
        SELECT at.id, c.name AS customer_name, sr.service_type, at.status, sr.location
        FROM assigned_tasks at
        JOIN service_requests sr ON at.request_id = sr.id
        JOIN customers c ON sr.customer_id = c.id
        WHERE at.employee_id = ?
    """, (session["worker_id"],))   

    rows = cur.fetchall()
    conn.close()

    # tasks list
    tasks = []
    for r in rows:
        lat, lon = None, None
        if r["location"]:
            try:
                parts = r["location"].replace("Lat:", "").replace("Lon:", "").split(",")
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
            except Exception as e:
                print("Location parse error:", e)

        tasks.append({
            "id": r["id"],
            "customer": r["customer_name"],
            "service": r["service_type"],
            "status": r["status"],
            "lat": lat,
            "lon": lon
        })

    return render_template("worker_dashboard.html", tasks=tasks, name=session.get("name"))






# ---------- Request Service ----------
@app.route("/request_service", methods=["GET", "POST"])
def request_service():
    if "role" not in session or session["role"] != "customer":
        return redirect(url_for("login"))

    shop_id = request.args.get("shop_id")   # URL se shop_id le raha hai (GET request se)

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        issue = request.form["issue"]
        service_type = request.form["service_type"]
        location = request.form["location"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""INSERT INTO service_requests 
                       (customer_id, shop_id, name, phone, issue, service_type, location, status, created_at) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (session["customer_id"], shop_id, name, phone, issue, service_type, location, "Pending", datetime.now()))
        conn.commit()
        conn.close()

        return redirect(url_for("my_request"))

    # GET request → form open karo
    return render_template("request_form.html", shop_id=shop_id)


# ---------- View Shops ----------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route("/view_shops")
def view_shops():
    # Get query params from JS
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    distance_filter = request.args.get("distance", type=int)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mechanic_shops")
    shops = cur.fetchall()
    conn.close()

    shop_list = []
    for shop in shops:
        shop_dict = dict(shop)

        # If coordinates exist, calculate distance
        if lat and lon and shop_dict.get("latitude") and shop_dict.get("longitude"):
            shop_distance = haversine(
                lat, lon, float(shop_dict["latitude"]), float(shop_dict["longitude"])
            )
            shop_dict["distance"] = round(shop_distance, 2)

            # Apply distance filter
            if distance_filter and shop_distance > distance_filter:
                continue
        else:
            shop_dict["distance"] = "N/A"

        shop_list.append(shop_dict)

    return render_template("view_shop.html", shops=shop_list)

# ---------- My Requests ----------
@app.route("/my_request")
def my_request():
    if "customer_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sr.id,
               ms.shop_name,
               sr.service_type AS service_requested,
               sr.created_at AS request_date,
               sr.status
        FROM service_requests sr
        JOIN mechanic_shops ms ON sr.shop_id = ms.id
        WHERE sr.customer_id = ?
        ORDER BY sr.created_at DESC
    """, (session["customer_id"],))
    
    requests = cur.fetchall()
    conn.close()
    return render_template("my_request.html", requests=requests)



# ---------- Employee Management ----------
@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        mechanic_id = session.get("mechanic_id")  # assuming logged-in mechanic
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        #  Check if email already exists
        cur.execute("SELECT * FROM employees WHERE email = ?", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            conn.close()
            flash(" Email already exists. Please choose another one.", "danger")
            return redirect(url_for("add_employee"))

        # Insert new employee
        cur.execute(
            "INSERT INTO employees (mechanic_id, name, email, password, role) VALUES (?, ?, ?, ?, ?)",
            (mechanic_id, name, email, hashed_password, role)
        )
        conn.commit()
        conn.close()

        flash(" Employee added successfully!", "success")
        return redirect(url_for("employee_list"))

    return render_template("add_employee.html")


@app.route("/employee_list")
def employee_list():
    if "role" not in session or session["role"] != "mechanic":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE mechanic_id=?", (session["mechanic_id"],))
    employees = cur.fetchall()
    conn.close()

    return render_template("employee_list.html", employees=employees)

@app.route("/assign_work/<int:request_id>", methods=["GET", "POST"])
def assign_work(request_id):
    
    if "role" not in session or session["role"] != "mechanic":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()

    
    cur.execute("SELECT * FROM service_requests WHERE id=?", (request_id,))
    svc_req = cur.fetchone()
    if not svc_req:
        conn.close()
        return "Service request not found", 404

    
    cur.execute("SELECT * FROM employees WHERE mechanic_id=?", (session["mechanic_id"],))
    employees = cur.fetchall()

    
    if request.method == "POST":
        employee_id = request.form["employee_id"]

        
        cur.execute("""
            INSERT INTO assigned_tasks (request_id, employee_id, status)
            VALUES (?, ?, ?)
        """, (
            request_id,
            employee_id,
            "Assigned"
        ))

        # service request status update 
        cur.execute("UPDATE service_requests SET status=? WHERE id=?", ("Assigned", request_id))

        conn.commit()
        conn.close()

        return redirect(url_for("work_status"))

    conn.close()
    return render_template("assign_work.html", svc_req=svc_req, employees=employees)



@app.route("/work_status")
def work_status():
    if "role" not in session or session["role"] != "mechanic":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            at.id, 
            e.name AS employee_name, 
            c.name AS customer_name,        -- customers table se naam
            sr.service_type AS description, -- service_requests se service type
            at.status
        FROM assigned_tasks at
        JOIN employees e ON at.employee_id = e.id
        JOIN service_requests sr ON at.request_id = sr.id
        JOIN customers c ON sr.customer_id = c.id   -- join with customers
        WHERE e.mechanic_id = ?
    """, (session["mechanic_id"],))

    tasks = cur.fetchall()
    conn.close()

    return render_template("work_status.html", tasks=tasks)


@app.route("/update_work_status/<int:task_id>", methods=["POST"])
def update_work_status(task_id):
    if "role" not in session or session["role"] != "worker":
        return redirect(url_for("login"))

    status = request.form.get("status")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE assigned_tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

    flash(" Task status updated successfully!", "success")
    return redirect(url_for("worker_dashboard"))


@app.route("/update_task_status/<int:task_id>", methods=["POST"])
def update_task_status(task_id):
    if "role" not in session or session["role"] != "mechanic":
        return redirect(url_for("login"))

    new_status = request.form["status"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE assigned_tasks SET status=? WHERE id=?", (new_status, task_id))
    conn.commit()
    conn.close()

    # Redirect back to mechanic dashboard instead of login
    return redirect(url_for("mechanic_dashboard"))






@app.route("/feedback_list")
def feedback_list():
    if "role" not in session or session["role"] != "mechanic":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT f.id, e.name as employee_name, f.comment, f.rating
                   FROM feedback f
                   JOIN employees e ON f.employee_id = e.id
                   WHERE e.mechanic_id=?""", (session["mechanic_id"],))
    feedbacks = cur.fetchall()
    conn.close()
    return render_template("feedback_list.html", feedbacks=feedbacks)

@app.route("/edit_employee/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
    employee = cur.fetchone()

    if not employee:
        conn.close()
        return "Employee not found!", 404

    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        phone = request.form["phone"]
        cur.execute("UPDATE employees SET name=?, role=?, phone=? WHERE id=?",
                    (name, role, phone, employee_id))
        conn.commit()
        conn.close()
        # flash("Employee updated successfully!", "success")  # Remove flash, not imported
        return redirect(url_for("employee_list"))

    conn.close()
    return render_template("edit_employee.html", employee=employee)

@app.route("/delete_employee/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Delete employee by id
    cur.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
    conn.close()
    
    flash(" Employee deleted successfully!", "success")
    return redirect(url_for("employee_list"))


@app.route("/assign_work", methods=["GET", "POST"])
def assign_task():
    if "role" not in session or session["role"] != "mechanic":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch all employees under this mechanic
    cur.execute("SELECT * FROM employees WHERE mechanic_id=?", (session["mechanic_id"],))
    employees = cur.fetchall()

    # Fetch all pending service requests for this mechanic's shop
    cur.execute("""
        SELECT sr.id, sr.problem_description, sr.customer_id
        FROM service_requests sr
        JOIN mechanic_shops ms ON sr.shop_id = ms.id
        WHERE ms.mechanic_id=? AND sr.status='Pending'
    """, (session["mechanic_id"],))
    requests = cur.fetchall()

    if request.method == "POST":
        request_id = request.form["request_id"]
        employee_id = request.form["employee_id"]

        # Insert into assigned_tasks
        cur.execute("""
            INSERT INTO assigned_tasks (request_id, employee_id, status)
            VALUES (?, ?, ?)
        """, (request_id, employee_id, "Assigned"))

        # Update request status also
        cur.execute("UPDATE service_requests SET status=? WHERE id=?", ("Assigned", request_id))

        conn.commit()
        conn.close()
        return redirect(url_for("work_status"))

    conn.close()
    return render_template("assign_work.html", employees=employees, requests=requests)



# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

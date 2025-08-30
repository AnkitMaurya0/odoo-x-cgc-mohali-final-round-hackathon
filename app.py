from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

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

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO cutomers (name, email, password) VALUES (?, ?, ?)",
                    (name, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup_customer.html")

# ---------- Signup - Mechanic ----------
@app.route("/signup/mechanic", methods=["GET", "POST"])
def signup_mechanic():
    if request.method == "POST":
        name = request.form["name"]              # owner ka naam
        email = request.form["email"]
        phone = request.form["phone"]
        shop_name = request.form["shop_name"]
        shop_address = request.form["shop_address"]
        services = request.form["services"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""INSERT INTO mechanic_shops 
                    (user_id, shop_name, shop_address, phone, service_provided, latitude, longitude) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (email, shop_name, shop_address, phone, services, latitude, longitude))

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

        # Check customer table
        cur.execute("SELECT * FROM cutomers WHERE email=? AND password=?", (email, password))
        customer = cur.fetchone()

        if customer:
            session["user"] = customer["email"]
            session["role"] = "customer"
            return redirect(url_for("customer_dashboard"))

        # Check mechanic table (user_id = email use kiya hai)
        cur.execute("SELECT * FROM mechanic_shops WHERE user_id=? ", (email,))
        mechanic = cur.fetchone()

        if mechanic:
            session["user"] = mechanic["user_id"]
            session["role"] = "mechanic"
            return redirect(url_for("mechanic_dashboard"))

        conn.close()
        return "Invalid credentials!"

    return render_template("login.html")

# ---------- Dashboards ----------
@app.route("/customer/dashboard")
def customer_dashboard():
    if "role" in session and session["role"] == "customer":
        return render_template("customer_dashboard.html", user=session["user"])
    return redirect(url_for("login"))

@app.route("/mechanic/dashboard")
def mechanic_dashboard():
    if "role" in session and session["role"] == "mechanic":
        return render_template("mechanic_dashboard.html", user=session["user"])
    return redirect(url_for("login"))

# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

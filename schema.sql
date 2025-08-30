CREATE TABLE IF NOT EXISTS cutomers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
);

CREATE TABLE IF NOT EXISTS mechanic_shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    shop_name TEXT,
    shop_address TEXT,
    phone TEXT,
    service_provided TEXT,
    latitude TEXT,
    longitude TEXT
);

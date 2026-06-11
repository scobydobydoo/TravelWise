
import sqlite3
import os


DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "travelwise.db"
)


# ───────────────── DATABASE CONNECTION ─────────────────

def get_db():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ───────────────── INITIALIZE DATABASE ─────────────────

def init_db():

    conn = get_db()

    cur = conn.cursor()

    # ───────────────── USERS ─────────────────

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ───────────────── BUDGET TIERS ─────────────────

    cur.execute("""
    CREATE TABLE IF NOT EXISTS budget_tiers (

        id INTEGER PRIMARY KEY,

        label TEXT NOT NULL,

        budget_per_day INTEGER NOT NULL
    )
    """)

    # ───────────────── HOTELS ─────────────────

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hotels (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tier_id INTEGER NOT NULL,

        name TEXT NOT NULL,

        price INTEGER NOT NULL,

        rating REAL NOT NULL,

        FOREIGN KEY (tier_id)
        REFERENCES budget_tiers(id)
    )
    """)

    # ───────────────── RESTAURANTS ─────────────────

    cur.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tier_id INTEGER NOT NULL,

        name TEXT NOT NULL,

        price INTEGER NOT NULL,

        rating REAL NOT NULL,

        FOREIGN KEY (tier_id)
        REFERENCES budget_tiers(id)
    )
    """)

    # ───────────────── ACTIVITIES ─────────────────
    # Used by:
    # - planner_service.py
    # - recomm.py

    cur.execute("""
    CREATE TABLE IF NOT EXISTS activities (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        type TEXT NOT NULL
        CHECK(type IN (
            'Adventure',
            'Spiritual',
            'Nature',
            'Food'
        )),

        cost INTEGER NOT NULL DEFAULT 0,

        rating REAL NOT NULL,

        safety REAL NOT NULL DEFAULT 4.0,

        popularity REAL NOT NULL DEFAULT 4.0
    )
    """)

    # ───────────────── PRICE SCAM CATEGORIES ─────────────────

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scam_categories (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        key TEXT UNIQUE NOT NULL,

        description TEXT NOT NULL,

        base_price INTEGER NOT NULL,

        weight_q INTEGER NOT NULL,

        weight_l INTEGER NOT NULL,

        weight_s INTEGER NOT NULL,

        tips TEXT NOT NULL
    )
    """)

    conn.commit()

    # ───────────────── SEED DATABASE ─────────────────

    if cur.execute(
        "SELECT COUNT(*) FROM budget_tiers"
    ).fetchone()[0] == 0:

        seed_database(cur)

        conn.commit()

    conn.close()

    print("[DB] Initialized:", DB_PATH)


# ───────────────── SEED DATA ─────────────────

def seed_database(cur):

    # ───────────────── BUDGET TIERS ─────────────────

    tiers = [

        (1, "Backpacker", 1200),

        (2, "Budget", 2500),

        (3, "Mid-Range", 4500),

        (4, "Premium", 8000),

        (5, "Luxury", 15000)
    ]

    cur.executemany(
        "INSERT INTO budget_tiers VALUES (?,?,?)",
        tiers
    )


    # ───────────────── HOTELS ─────────────────

    hotels = [

        (1, "Zostel Rishikesh", 400, 4.2),

        (1, "GoStops", 350, 4.0),

        (1, "Shantiyoga Ashram", 500, 4.3),

        (2, "Moustache", 800, 4.1),

        (2, "Hotel Yog Vashishth", 1200, 3.8),

        (2, "Divine Resort", 1500, 4.0),

        (3, "Hotel Ganga Kinara", 2800, 4.2),

        (3, "Sterling Palm Bliss", 3000, 4.3),

        (3, "The Forest Resort", 3500, 4.4),

        (4, "Aloha on Ganges", 7000, 4.6),

        (4, "Ganga Beach Resort", 6500, 4.5),

        (5, "Ananda Himalayas", 25000, 4.9)
    ]

    cur.executemany(
        """
        INSERT INTO hotels
        (tier_id, name, price, rating)

        VALUES (?,?,?,?)
        """,
        hotels
    )


    # ───────────────── RESTAURANTS ─────────────────

    restaurants = [

        (1, "Little Buddha Cafe", 250, 4.5),

        (1, "Freedom Cafe", 200, 4.3),

        (1, "Street Food", 80, 4.0),

        (2, "Pure Soul Cafe", 350, 4.6),

        (2, "The 60's Cafe", 400, 4.4),

        (2, "Bhandari Swiss Cottage", 300, 4.2),

        (3, "Chotiwala", 450, 4.5),

        (3, "Green Italian Cafe", 600, 4.7),

        (3, "Pumpernickel German", 500, 4.6),

        (4, "Achanta's Restaurant", 800, 4.7),

        (4, "Sanskriti Cafe", 700, 4.6),

        (5, "Ananda Spa Restaurant", 2000, 4.9)
    ]

    cur.executemany(
        """
        INSERT INTO restaurants
        (tier_id, name, price, rating)

        VALUES (?,?,?,?)
        """,
        restaurants
    )


    # ───────────────── ACTIVITIES ─────────────────

    activities = [

        ("Ganga Aarti", "Spiritual", 0, 4.9, 5.0, 4.8),

        ("Temple Tour", "Spiritual", 0, 4.7, 4.8, 4.5),

        ("Triveni Ghat", "Spiritual", 0, 4.7, 4.9, 4.7),

        ("Sunset Point", "Nature", 0, 4.6, 4.7, 4.3),

        ("River Rafting 16km", "Adventure", 1200, 4.8, 4.4, 5.0),

        ("Yoga Class", "Spiritual", 400, 4.8, 5.0, 4.6),

        ("Beatles Ashram", "Spiritual", 100, 4.8, 4.7, 4.9),

        ("Neer Waterfall Trek", "Nature", 200, 4.5, 4.2, 4.4),

        ("Mountain Biking", "Adventure", 1500, 4.4, 4.0, 4.3),

        ("Flying Fox", "Adventure", 2000, 4.5, 4.3, 4.7),

        ("Bungee Jumping", "Adventure", 3500, 4.6, 4.1, 5.0),

        ("River Rafting 36km", "Adventure", 2500, 4.7, 4.3, 4.9),

        ("Meditation Camp", "Spiritual", 800, 4.6, 4.9, 4.2),

        ("Kunjapuri Temple Trek", "Nature", 300, 4.4, 4.1, 4.3),

        ("Chotiwala Restaurant", "Food", 400, 4.5, 4.5, 4.8),

        ("Little Buddha Cafe", "Food", 350, 4.6, 4.7, 4.7)
    ]

    cur.executemany(
        """
        INSERT INTO activities
        (name, type, cost, rating, safety, popularity)

        VALUES (?,?,?,?,?,?)
        """,
        activities
    )


    # ───────────────── SCAM CATEGORIES ─────────────────

    scam_data = [

    (
        "rafting_16km",
        "River Rafting - 16 km",
        450,
        80,
        60,
        120,
        "Always insist on BIS-certified life jackets."
    ),

    (
        "rafting_36km",
        "River Rafting - 36 km",
        1200,
        120,
        100,
        180,
        "Long routes become expensive during peak season."
    ),

    (
        "bungee_jumping",
        "Bungee Jumping",
        2500,
        300,
        200,
        350,
        "Check for certified bungee operators only."
    ),

    (
        "flying_fox",
        "Flying Fox",
        1800,
        200,
        120,
        250,
        "Combo packages are usually cheaper."
    ),

    (
        "giant_swing",
        "Giant Swing",
        2200,
        250,
        180,
        300,
        "Verify GST inclusion before payment."
    ),

    (
        "yoga_class",
        "Yoga Class",
        200,
        150,
        100,
        180,
        "Ashram packages are cheaper long-term."
    ),

    (
        "meditation_retreat",
        "Meditation Retreat",
        1500,
        250,
        120,
        200,
        "Ask if accommodation is included."
    ),

    (
        "bike_rental",
        "Scooty/Bike Rental",
        500,
        100,
        80,
        120,
        "Record fuel level before renting."
    ),

    (
        "camping",
        "Riverside Camping",
        1800,
        220,
        160,
        280,
        "Avoid unregistered camps in monsoon season."
    ),

    (
        "ayurveda_massage",
        "Ayurveda Massage",
        1000,
        180,
        100,
        150,
        "Verify therapist certification."
    ),

    (
        "tattoo",
        "Tattoo Studio",
        2000,
        250,
        180,
        220,
        "Ensure sealed needles are used."
    ),

    (
        "boat_ride",
        "Boat Ride",
        300,
        60,
        40,
        80,
        "Agree on price before boarding."
    ),

    (
        "photography",
        "Tourist Photography",
        800,
        100,
        90,
        140,
        "Clarify edited photo charges."
    ),

    (
        "tour_guide",
        "Private Tour Guide",
        1500,
        200,
        140,
        220,
        "Ask for full itinerary beforehand."
    )
    ]


    cur.executemany(
        """
        INSERT INTO scam_categories
        (
            key,
            description,
            base_price,
            weight_q,
            weight_l,
            weight_s,
            tips
        )

        VALUES (?,?,?,?,?,?,?)
        """,
        scam_data
    )


    # ───────────────── INDEXES ─────────────────

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_activity_type
    ON activities(type)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_activity_cost
    ON activities(cost)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_activity_rating
    ON activities(rating)
    """)


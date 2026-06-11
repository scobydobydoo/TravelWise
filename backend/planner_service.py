from db import get_db


def generate_plan(tier: int, days: int, prefs: list[str]) -> dict:
    conn = get_db()
    cur = conn.cursor()

    row = cur.execute(
        "SELECT label, budget_per_day FROM budget_tiers WHERE id=?", (tier,)
    ).fetchone()
    if not row:
        raise ValueError(f"Invalid tier: {tier}")

    tier_label   = row["label"]
    budget_total = row["budget_per_day"] * days
    hotel_budget = int(budget_total * 0.40)
    food_budget  = int(budget_total * 0.25)
    transport_budget = int(budget_total * 0.10)
    activity_budget  = budget_total - hotel_budget - food_budget - transport_budget

    hotel = None
    for t in range(tier, 0, -1):
        row = cur.execute("""
            SELECT name, price, rating FROM hotels
            WHERE tier_id=? AND price * ? <= ?
            ORDER BY rating DESC LIMIT 1
        """, (t, days, hotel_budget)).fetchone()
        if row:
            hotel = dict(row)
            break
    if not hotel:
        hotel = cur.execute(
            "SELECT name, price, rating FROM hotels ORDER BY price ASC LIMIT 1"
        ).fetchone()
        hotel = dict(hotel)

    hotel_cost = hotel["price"] * days

    food_per_meal = food_budget // (2 * days)
    restaurant = None
    for t in range(tier, 0, -1):
        row = cur.execute("""
            SELECT name, price, rating FROM restaurants
            WHERE tier_id=? AND price <= ?
            ORDER BY rating DESC LIMIT 1
        """, (t, food_per_meal)).fetchone()
        if row:
            restaurant = dict(row)
            break
    if not restaurant:
        restaurant = cur.execute(
            "SELECT name, price, rating FROM restaurants ORDER BY price ASC LIMIT 1"
        ).fetchone()
        restaurant = dict(restaurant)

    food_cost = min(restaurant["price"] * 2 * days, food_budget)
    transport_cost = transport_budget


    if prefs:
        placeholders = ",".join("?" * len(prefs))
        activity_rows = cur.execute(
            f"SELECT name, type, cost, rating FROM activities WHERE type IN ({placeholders}) ORDER BY CASE WHEN cost=0 THEN 999 ELSE rating*1.0/cost END DESC",
            prefs
        ).fetchall()
    else:
        activity_rows = cur.execute(
            "SELECT name, type, cost, rating FROM activities ORDER BY CASE WHEN cost=0 THEN 999 ELSE rating*1.0/cost END DESC"
        ).fetchall()

    conn.close()

    selected_activities = []
    activity_total = 0
    for act in activity_rows:
        act = dict(act)
        if activity_total + act["cost"] <= activity_budget:
            selected_activities.append(act)
            activity_total += act["cost"]

    total_spent = hotel_cost + food_cost + transport_cost + activity_total

    return {
        "tier":  tier_label,
        "days":  days,
        "prefs": prefs if prefs else ["All"],

        "budget": {
            "total":     budget_total,
            "hotel":     hotel_budget,
            "food":      food_budget,
            "transport": transport_budget,
            "activities":activity_budget,
        },

        "hotel": {
            "name":   hotel["name"],
            "rating": hotel["rating"],
            "price_per_night": hotel["price"],
            "total_cost": hotel_cost,
        },

        "restaurant": {
            "name":   restaurant["name"],
            "rating": restaurant["rating"],
            "price_per_meal": restaurant["price"],
            "total_cost": food_cost,
        },

        "transport_cost": transport_cost,

        "activities": [
            {
                "name":   a["name"],
                "type":   a["type"],
                "cost":   a["cost"],
                "rating": a["rating"],
                "free":   a["cost"] == 0,
            }
            for a in selected_activities
        ],

        "summary": {
            "hotel":      hotel_cost,
            "food":       food_cost,
            "transport":  transport_cost,
            "activities": activity_total,
            "total_spent":total_spent,
            "remaining":  budget_total - total_spent,
            "over_budget": total_spent > budget_total,
        }
    }
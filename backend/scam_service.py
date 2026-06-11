"""
Linear regression model: price = base + w_q*quality + w_l*location + w_s*season
"""

from db import get_db


def get_catalogue() -> list[dict]:
    """Return all scam categories for frontend dropdown."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, key, description, base_price FROM scam_categories ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def detect_scam(
    category_id: int,
    quality: int,
    location: int,
    season: int,
    offered_price: float
) -> dict:
    conn = get_db()
    item = conn.execute(
        "SELECT * FROM scam_categories WHERE id=?", (category_id,)
    ).fetchone()
    conn.close()

    if not item:
        raise ValueError(f"Category id {category_id} not found")

    item = dict(item)

    fair_price = (
        item["base_price"]
        + item["weight_q"] * quality
        + item["weight_l"] * location
        + item["weight_s"] * season
    )

    deviation = ((offered_price - fair_price) / fair_price) * 100

    if deviation > 20:
        verdict = "SCAM"
        verdict_color = "red"
        message = (
            f"WARNING — Overcharged by {deviation:.1f}%. "
            "Likely causes: tourist zone premium, peak season surge, or vendor targeting first-time visitors."
        )
    elif deviation < -20:
        verdict = "SUSPICIOUS"
        verdict_color = "orange"
        message = (
            f"Price is {abs(deviation):.1f}% BELOW fair value. "
            "Likely causes: fake/poor quality product, bait-and-switch, or hidden charges added later."
        )
    elif deviation > 10:
        verdict = "SLIGHTLY HIGH"
        verdict_color = "yellow"
        message = (
            f"Slightly overpriced by {deviation:.1f}%. Negotiable. "
            "Compare with 2-3 nearby vendors before buying."
        )
    elif deviation < -10:
        verdict = "GOOD DEAL"
        verdict_color = "green"
        message = (
            f"Good deal — {abs(deviation):.1f}% below fair market value. "
            "Verify quality/authenticity before purchasing."
        )
    else:
        verdict = "FAIR"
        verdict_color = "green"
        message = "Fair price. Within ±10% of market estimate. Proceed with confidence."

    # ── Top price driver ───────────────────────────────────────────────────
    contrib = {
        "Quality level":    item["weight_q"] * quality,
        "Location premium": item["weight_l"] * location,
        "Season demand":    item["weight_s"] * season,
    }
    top_driver = max(contrib, key=contrib.get)
    top_pct    = round((contrib[top_driver] / fair_price) * 100, 1) if fair_price else 0

    driver_notes = {
        "Quality level":    "Certified staff, premium gear, or branded service inflates cost.",
        "Location premium": "Prime tourist zones (Tapovan / Laxman Jhula) carry a location surcharge.",
        "Season demand":    "Peak season (Oct-Nov / Yoga Festival) drives demand-based price spikes.",
    }

    return {
        "item": item["description"],
        "fair_price":   round(fair_price, 2),
        "offered_price": offered_price,
        "acceptable_range": {
            "low":  round(fair_price * 0.80, 2),
            "high": round(fair_price * 1.20, 2),
        },
        "deviation_pct": round(deviation, 2),
        "verdict":       verdict,
        "verdict_color": verdict_color,
        "message":       message,
        "insight": f"Top price driver: {top_driver} (~{top_pct}% of fair price). {driver_notes[top_driver]}",
        "local_tip": item["tips"],
        "contributions": {
            "quality":  contrib["Quality level"],
            "location": contrib["Location premium"],
            "season":   contrib["Season demand"],
        }
    }
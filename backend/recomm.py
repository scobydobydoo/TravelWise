from db import get_db


def get_activity_types():

    conn = get_db()

    rows = conn.execute("""
        SELECT DISTINCT type
        FROM activities
        ORDER BY type
    """).fetchall()

    conn.close()

    return [r["type"] for r in rows]


def recommend_activities(
    activity_type,
    budget,
    min_rating=0
):

    conn = get_db()

    rows = conn.execute("""
        SELECT *
        FROM activities
        WHERE type = ?
        AND cost <= ?
        ORDER BY rating DESC
    """, (activity_type, budget)).fetchall()

    conn.close()

    if not rows:

        return {
            "type": activity_type,
            "budget": {
                "total": budget,
                "spent": 0,
                "remaining": budget
            },
            "activities": [],
            "message": "No activities found"
        }

    activities = [dict(r) for r in rows]


    for act in activities:

        affordability = (
            (budget - act["cost"]) / budget
        )

        score = (
            act["rating"] * 0.4
            + act["safety"] * 0.3
            + act["popularity"] * 0.2
            + affordability * 5 * 0.1
        )

        act["recommendation_score"] = round(score, 2)


    activities.sort(
        key=lambda x: x["recommendation_score"],
        reverse=True
    )


    selected = []

    spent = 0

    for act in activities:

        if act["rating"] < min_rating:
            continue

        if spent + act["cost"] <= budget:

            selected.append(act)

            spent += act["cost"]

    remaining = budget - spent


    insight = ""

    if selected:

        best = selected[0]

        insight = (
            f"Top recommendation is "
            f"{best['name']} with score "
            f"{best['recommendation_score']}"
        )

    return {

        "type": activity_type,

        "budget": {
            "total": budget,
            "spent": spent,
            "remaining": remaining
        },

        "activities": [
            {
                "name": a["name"],
                "type": a["type"],
                "cost": a["cost"],
                "rating": a["rating"],
                "safety": a["safety"],
                "popularity": a["popularity"],
                "recommendation_score":
                    a["recommendation_score"],
                "free": a["cost"] == 0
            }
            for a in selected
        ],

        "summary": {
            "total_selected": len(selected),
            "remaining_budget": remaining
        },

        "insight": insight
    }


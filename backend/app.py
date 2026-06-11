from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

from db import get_db, init_db
from planner_service import generate_plan
from scam_service import detect_scam, get_catalogue
from recomm import recommend_activities, get_activity_types
from risk_service import analyse_risk

app = Flask(__name__)
CORS(app)

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
CPP_DIR      = os.path.join(BASE_DIR, "CPP")
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

@app.route('/signup', methods=['POST'])
def signup():
    data     = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"status": "fail", "message": "Fill all fields"})
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"status": "success", "message": "Signup successful"})
    except Exception:
        return jsonify({"status": "fail", "message": "Username already exists"})
    finally:
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data     = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone(); conn.close()
    if user:
        return jsonify({"status": "success", "user_id": user["id"]})
    return jsonify({"status": "fail", "message": "Invalid credentials"})


# ───────────────────────── BUDGET PLANNER ───────────────────────────────────

@app.route('/plan', methods=['POST'])
def plan():
    data = request.json
    try:
        result = generate_plan(int(data.get("tier",1)), int(data.get("days",1)), data.get("prefs",[]))
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})


# ───────────────────────── SCAM DETECTOR ────────────────────────────────────

@app.route('/scam/categories', methods=['GET'])
def scam_categories():
    try:
        return jsonify({"status": "success", "categories": get_catalogue()})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})


@app.route('/scam/detect', methods=['POST'])
def scam_detect():
    data = request.json
    try:
        result = detect_scam(int(data.get("category_id",0)), int(data.get("quality",3)),
                             int(data.get("location",3)), int(data.get("season",3)),
                             float(data.get("offered_price",0)))
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})


# ───────────────────────── RECOMMENDATION ───────────────────────────────────

@app.route('/recommend/types', methods=['GET'])
def recommend_types():
    try:
        return jsonify({"status": "success", "types": get_activity_types()})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})


@app.route('/recommend', methods=['POST'])
def recommend():
    data          = request.json
    activity_type = data.get("type", "").strip()
    budget        = int(data.get("budget", 0))
    min_rating    = float(data.get("min_rating", 0))
    if not activity_type:
        return jsonify({"status": "fail", "message": "Activity type required"})
    if budget <= 0:
        return jsonify({"status": "fail", "message": "Budget must be positive"})
    try:
        result = recommend_activities(activity_type=activity_type, budget=budget, min_rating=min_rating)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})


# ───────────────────────── ROUTE PLANNER ────────────────────────────────────

@app.route('/route', methods=['POST'])
def route_plan():
    data        = request.json
    source      = data.get("source", "").strip()
    destination = data.get("destination", "").strip()
    vehicle     = data.get("vehicle", "rickshaw").strip()

    if not source or not destination:
        return jsonify({"status": "fail", "message": "Source and destination required"})

    try:
        fetch = subprocess.run(
            ["python", os.path.join(CPP_DIR, "fetch_graph.py"), source, destination],
            capture_output=True, text=True, timeout=120, cwd=CPP_DIR
        )
        app.logger.info("fetch_graph stdout: " + fetch.stdout.strip())
        app.logger.info("fetch_graph stderr: " + fetch.stderr.strip())
        if fetch.returncode != 0:
            err = fetch.stderr.strip() or fetch.stdout.strip() or "fetch_graph.py failed"
            return jsonify({"status": "fail", "message": "Graph error: " + err})

        binary = os.path.join(CPP_DIR, "planner.exe")
        if not os.path.exists(binary):
            binary = os.path.join(CPP_DIR, "planner")
        if not os.path.exists(binary):
            return jsonify({"status": "fail", "message": "planner binary not found — compile main.cpp first"})

        cpp = subprocess.run(
            [binary],
            input=source + "\n" + destination + "\n" + vehicle + "\n",
            capture_output=True, text=True, timeout=60,
            cwd=CPP_DIR, encoding="utf-8", errors="replace"
        )
        app.logger.info("planner stdout: " + cpp.stdout.strip())
        app.logger.info("planner stderr: " + cpp.stderr.strip())

        info = _parse_cpp_output(cpp.stdout)
        app.logger.info("parsed: " + str(info))

        if info.get("status") == "no_route":
            return jsonify({"status": "fail", "message": "No route found between '" + source + "' and '" + destination + "'"})

        old_mtime    = os.path.getmtime(os.path.join(CPP_DIR, "map.html")) if os.path.exists(os.path.join(CPP_DIR, "map.html")) else 0
        map_run      = subprocess.run(
            ["python", os.path.join(CPP_DIR, "show_map.py")],
            capture_output=True, text=True, timeout=30, cwd=CPP_DIR
        )
        app.logger.info("show_map stderr: " + map_run.stderr.strip())

        map_html      = ""
        map_html_path = os.path.join(CPP_DIR, "map.html")
        if os.path.exists(map_html_path):
            if os.path.getmtime(map_html_path) > old_mtime:
                with open(map_html_path, "r", encoding="utf-8") as f:
                    map_html = f.read()
            else:
                app.logger.warning("map.html not updated by show_map.py")
                app.logger.warning("show_map stdout: " + map_run.stdout)
                app.logger.warning("show_map stderr: " + map_run.stderr)

        return jsonify({
            "status": "success",
            "data": {
                **info,
                "source":      source,
                "destination": destination,
                "vehicle":     vehicle,
                "map_html":    map_html
            }
        })

    except subprocess.TimeoutExpired:
        return jsonify({"status": "fail", "message": "Timed out"})
    except Exception as e:
        app.logger.exception("route error")
        return jsonify({"status": "fail", "message": str(e)})


def _parse_cpp_output(output):
    result = {"status": "unknown", "distance_km": None, "eta_min": None, "fare": None, "raw": output}
    for line in output.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip().upper()
        val = val.strip()
        if   key == "STATUS":      result["status"] = val.lower()
        elif key == "DISTANCE_KM":
            try: result["distance_km"] = float(val)
            except: pass
        elif key == "ETA_MIN":
            try: result["eta_min"] = float(val)
            except: pass
        elif key == "FARE":
            try: result["fare"] = float(val)
            except: pass
    return result


# ───────────────────────── RISK ANALYSIS ────────────────────────────────────

@app.route("/risk", methods=["POST"])
def risk_analysis():
    data  = request.json
    place = data.get("place", "").strip()
    if not place:
        return jsonify({"status": "fail", "message": "Place name required"})
    try:
        result = analyse_risk(place)
        return jsonify({"status": "success", "data": result})
    except ValueError as e:
        return jsonify({"status": "fail", "message": str(e)})
    except Exception as e:
        app.logger.exception("Risk analysis error")
        return jsonify({"status": "fail", "message": str(e)})


# ───────────────────────── HEALTH ───────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "TravelWise API v2.0"})



@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
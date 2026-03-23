// =============================================================
//  TravelWise — Transport & Routing Module (OSM Update)
//  PART 1/4 — Data Structures + JSON Map Loader
// =============================================================

#include <bits/stdc++.h>
#include <fstream>
using namespace std;

// ─────────────────────────────────────────────
//  UPDATED EDGE & NODE (OSM-compatible)
// ─────────────────────────────────────────────

struct Edge {
    int     to;
    double  distance;   // from OSM "length" field (meters → km)
    double  cost;       // estimated: distance * rate
    double  time;       // from OSM "maxspeed" or estimated
    double  safety;     // derived from OSM road "highway" tag
    string  roadName;   // from OSM "name" tag
};

struct Node {
    int     id;
    string  name;       // from OSM "name" tag (if available)
    double  lat;        // OSM "y"
    double  lon;        // OSM "x"
};

// ─────────────────────────────────────────────
//  SAFETY SCORE FROM OSM HIGHWAY TAG
// ─────────────────────────────────────────────
//  OSM tags roads by type — we map these to safety scores

double safetyFromHighway(const string& highway) {
    if (highway == "primary")       return 0.90;
    if (highway == "secondary")     return 0.80;
    if (highway == "tertiary")      return 0.70;
    if (highway == "residential")   return 0.75;
    if (highway == "unclassified")  return 0.60;
    if (highway == "track")         return 0.40;
    if (highway == "footway")       return 0.85;
    return 0.65; // default
}

// ─────────────────────────────────────────────
//  SIMPLE JSON PARSER (No external library)
//  Reads the transport_network.json exported
//  from Python OSMnx script
// ─────────────────────────────────────────────

// Extract string value for a key from a JSON line
// e.g. line: "lat": 28.6139  →  returns "28.6139"
string extractValue(const string& line, const string& key) {
    size_t pos = line.find("\"" + key + "\"");
    if (pos == string::npos) return "";
    pos = line.find(":", pos) + 1;
    while (pos < line.size() && (line[pos] == ' ' || line[pos] == '"')) pos++;
    size_t end = line.find_first_of(",}\n\"", pos);
    return line.substr(pos, end - pos);
}

// ─────────────────────────────────────────────
//  LOAD GRAPH FROM JSON FILE
// ─────────────────────────────────────────────

void loadFromJSON(const string& filepath,
                  vector<Node>& nodes,
                  vector<vector<Edge>>& adj,
                  int& n)
{
    ifstream file(filepath);
    if (!file.is_open()) {
        cerr << "ERROR: Cannot open " << filepath << "\n";
        return;
    }

    string line;
    string section = "";     // "nodes" or "edges"
    Node   currNode;
    int    eu = -1, ev = -1;
    double elen = 0, espeed = 60.0;
    string ehighway = "unclassified";
    string ename    = "";

    // Cost rate: 10 units per km (tune as needed)
    const double COST_PER_KM = 10.0;

    while (getline(file, line)) {

        // Detect section
        if (line.find("\"nodes\"") != string::npos) { section = "nodes"; continue; }
        if (line.find("\"edges\"") != string::npos) { section = "edges"; continue; }

        if (section == "nodes") {
            string sid  = extractValue(line, "id");
            string slat = extractValue(line, "lat");
            string slon = extractValue(line, "lon");
            string snam = extractValue(line, "name");

            if (!sid.empty())  currNode.id   = stoi(sid);
            if (!slat.empty()) currNode.lat  = stod(slat);
            if (!slon.empty()) currNode.lon  = stod(slon);
            if (!snam.empty()) currNode.name = snam;

            // When a node object closes
            if (line.find("}") != string::npos && currNode.id >= 0) {
                if (currNode.name.empty())
                    currNode.name = "Node_" + to_string(currNode.id);
                int idx = currNode.id;
                if (idx >= n) {
                    n = idx + 1;
                    nodes.resize(n);
                    adj.resize(n);
                }
                nodes[idx] = currNode;
                currNode   = {};
            }
        }

        if (section == "edges") {
            string su  = extractValue(line, "u");
            string sv  = extractValue(line, "v");
            string sel = extractValue(line, "distance");
            string shw = extractValue(line, "highway");
            string spd = extractValue(line, "maxspeed");
            string snm = extractValue(line, "name");

            if (!su.empty())  eu       = stoi(su);
            if (!sv.empty())  ev       = stoi(sv);
            if (!sel.empty()) elen     = stod(sel) / 1000.0; // m → km
            if (!shw.empty()) ehighway = shw;
            if (!spd.empty()) espeed   = stod(spd);
            if (!snm.empty()) ename    = snm;

            // When an edge object closes
            if (line.find("}") != string::npos && eu >= 0 && ev >= 0) {
                double safety = safetyFromHighway(ehighway);
                double time   = (espeed > 0) ? (elen / espeed) * 60.0 : elen * 3.0;
                double cost   = elen * COST_PER_KM;

                if (eu < n && ev < n) {
                    adj[eu].push_back({ev, elen, cost, time, safety, ename});
                    adj[ev].push_back({eu, elen, cost, time, safety, ename}); // undirected
                }
                eu = ev = -1; elen = 0;
                ehighway = "unclassified"; ename = ""; espeed = 60.0;
            }
        }
    }

    cout << "✓ Loaded " << n << " nodes from " << filepath << "\n";
}
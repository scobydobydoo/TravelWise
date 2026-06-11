/*
 * TravelWise — Route Planner (C++ Dijkstra Engine)
 * Compatible with GCC versions that don't support C++17 structured bindings.
 */

#include <bits/stdc++.h>
#include "json.hpp"

using namespace std;
using json = nlohmann::json;

typedef pair<double, long long> pdi;

// adjacency list: node -> [(to, travel_time_sec, length_m)]
unordered_map<long long, vector<tuple<long long, double, double>>> adj;

// ── Fare calculation ──────────────────────────────────────────────────────────
double calculateFare(const string& vehicle, double distance_km) {
    if (vehicle == "rickshaw") return 20.0 + distance_km * 10.0;
    if (vehicle == "vikram")   return 10.0 + distance_km *  8.0;
    if (vehicle == "magic")    return 15.0 + distance_km *  9.0;
    if (vehicle == "bus")      return         distance_km *  5.0;
    return distance_km * 12.0;
}

// ── Dijkstra ──────────────────────────────────────────────────────────────────
vector<long long> dijkstra(long long src, long long dest,
                            unordered_map<long long, double>& dist) {

    unordered_map<long long, long long> parent;
    priority_queue<pdi, vector<pdi>, greater<pdi>> pq;

    dist[src] = 0.0;
    pq.push(make_pair(0.0, src));

    while (!pq.empty()) {
        double d    = pq.top().first;
        long long u = pq.top().second;
        pq.pop();

        if (u == dest) break;
        if (d > dist[u]) continue;

        for (size_t i = 0; i < adj[u].size(); i++) {
            long long v  = get<0>(adj[u][i]);
            double    t  = get<1>(adj[u][i]);
            double    nd = d + t;

            if (!dist.count(v) || dist[v] > nd) {
                dist[v]   = nd;
                parent[v] = u;
                pq.push(make_pair(nd, v));
            }
        }
    }

    if (!dist.count(dest)) return vector<long long>();

    vector<long long> path;
    long long cur = dest;
    while (cur != src) {
        path.push_back(cur);
        if (!parent.count(cur)) return vector<long long>();
        cur = parent[cur];
    }
    path.push_back(src);
    reverse(path.begin(), path.end());
    return path;
}

static string quoteArg(const string& arg) {
    string result = "\"";
    for (char c : arg) {
        if (c == '\\') result += "\\\\";
        else if (c == '"') result += "\\\"";
        else result += c;
    }
    result += "\"";
    return result;
}

static int runPythonScript(const string& script, const vector<string>& args) {
    string cmd = "python ";
    cmd += quoteArg(script);
    for (const auto& arg : args) {
        cmd += " ";
        cmd += quoteArg(arg);
    }

    cerr << "INFO running: " << cmd << "\n";
    int status = std::system(cmd.c_str());
    if (status == -1) return -1;

    #ifdef _WIN32
    return status;
    #else
    return WEXITSTATUS(status);
    #endif
}

// ── Main ──────────────────────────────────────────────────────────────────────
int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    // 1. Read inputs from stdin
    string source, destination, vehicle;
    if (!getline(cin, source))      { cerr << "ERR: no source\n";      return 1; }
    if (!getline(cin, destination)) { cerr << "ERR: no destination\n"; return 1; }
    if (!getline(cin, vehicle))     { cerr << "ERR: no vehicle\n";     return 1; }

    // Trim \r and spaces (Windows line endings)
    while (!source.empty()      && (source.back()      == '\r' || source.back()      == ' ')) source.erase(source.size()-1);
    while (!destination.empty() && (destination.back() == '\r' || destination.back() == ' ')) destination.erase(destination.size()-1);
    while (!vehicle.empty()     && (vehicle.back()     == '\r' || vehicle.back()     == ' ')) vehicle.erase(vehicle.size()-1);

    if (vehicle.empty()) vehicle = "rickshaw";

    cerr << "INFO source=" << source << " dest=" << destination << " vehicle=" << vehicle << "\n";

    // 2. Fetch graph.json from Python helper
    if (runPythonScript("fetch_graph.py", {source, destination}) != 0) {
        cerr << "ERR: fetch_graph.py failed\n";
        return 1;
    }

    // 3. Load graph.json (written by fetch_graph.py)
    ifstream file("graph.json");
    if (!file.is_open()) {
        cerr << "ERR: graph.json not found\n";
        return 1;
    }

    json data;
    try {
        file >> data;
    } catch (const exception& e) {
        cerr << "ERR: graph.json parse error: " << e.what() << "\n";
        return 1;
    }

    long long source_node      = data["source_node"];
    long long destination_node = data["destination_node"];

    for (size_t i = 0; i < data["edges"].size(); i++) {
        json& edge  = data["edges"][i];
        long long u = edge["from"];
        long long v = edge["to"];
        double    t = edge["weight"];
        double  len = edge["length"];
        adj[u].push_back(make_tuple(v, t, len));
    }

    cerr << "INFO graph loaded: " << adj.size() << " nodes\n";

    // 3. Run Dijkstra
    unordered_map<long long, double> dist;
    vector<long long> path = dijkstra(source_node, destination_node, dist);

    if (path.empty()) {
        cout << "STATUS:no_route\n";
        cerr << "ERR: no route found\n";
        return 0;
    }

    // 4. Accumulate total distance along path
    double total_distance_m = 0.0;
    for (size_t i = 0; i + 1 < path.size(); i++) {
        long long u = path[i];
        long long v = path[i + 1];
        for (size_t j = 0; j < adj[u].size(); j++) {
            if (get<0>(adj[u][j]) == v) {
                total_distance_m += get<2>(adj[u][j]);
                break;
            }
        }
    }

    double distance_km = total_distance_m / 1000.0;
    double time_min    = dist[destination_node] / 60.0;
    double fare        = calculateFare(vehicle, distance_km);

    // 5. Write route.txt for show_map.py
    ofstream out("route.txt");
    if (!out.is_open()) {
        cerr << "ERR: cannot write route.txt\n";
        return 1;
    }
    for (size_t i = 0; i < path.size(); i++) out << path[i] << " ";
    out.close();

    // 7. Generate HTML map using Python helper
    if (runPythonScript("show_map.py", {}) != 0) {
        cerr << "ERR: show_map.py failed\n";
        return 1;
    }

    // 8. Print machine-readable output to stdout (Flask parses these)
    cout << "STATUS:success\n";
    cout << fixed << setprecision(4);
    cout << "DISTANCE_KM:" << distance_km << "\n";
    cout << "ETA_MIN:"     << time_min    << "\n";
    cout << "FARE:"        << fare        << "\n";
    cout << "VEHICLE:"     << vehicle     << "\n";
    cout << "NODES:"       << path.size() << "\n";

    cerr << "INFO distance=" << distance_km << "km eta=" << time_min << "min fare=" << fare << "\n";

    return 0;
}
#include <bits/stdc++.h>
#include "json.hpp"

using namespace std;
using json = nlohmann::json;

typedef pair<double, long long> pii;

unordered_map<long long, vector<tuple<long long, double, double>>> adj;

vector<long long> dijkstra(long long src, long long dest, unordered_map<long long, double> &dist) {
    unordered_map<long long, long long> parent;
    priority_queue<pii, vector<pii>, greater<pii>> pq;

    pq.push({0, src});
    dist[src] = 0;

    while (!pq.empty()) {
        auto temp = pq.top();
        pq.pop();

        double d = temp.first;
        long long u = temp.second;

        if (u == dest) break;

        for (auto &edge : adj[u]) {
            long long v = get<0>(edge);
            double time = get<1>(edge);

            if (!dist.count(v) || dist[v] > d + time) {
                dist[v] = d + time;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }

    vector<long long> path;
    long long cur = dest;

    while (cur != src) {
        path.push_back(cur);
        if (!parent.count(cur)) return {};
        cur = parent[cur];
    }
    path.push_back(src);
    reverse(path.begin(), path.end());

    return path;
}

int main() {

    string source, destination;

    cout << "Enter Source: ";
    getline(cin, source);

    cout << "Enter Destination: ";
    getline(cin, destination);

    string command = "python fetch_graph.py \"" + source + "\" \"" + destination + "\"";
    if (system(command.c_str()) != 0) {
        cout << "Python script failed!\n";
        return 1;
    }

    ifstream file("graph.json");

    if (!file.is_open() || file.peek() == ifstream::traits_type::eof()) {
        cout << "Error: graph.json is empty!\n";
        return 1;
    }

    json data;
    file >> data;

    long long source_node = data["source_node"];
    long long destination_node = data["destination_node"];

    for (auto &edge : data["edges"]) {
        long long u = edge["from"];
        long long v = edge["to"];
        double time = edge["weight"];
        double distance = edge["length"];

        adj[u].push_back({v, time, distance});
    }

    cout << "\nComputing fastest route...\n";

    unordered_map<long long, double> dist;
    vector<long long> path = dijkstra(source_node, destination_node, dist);

    if (path.empty()) {
        cout << "No route found!\n";
        return 0;
    }

    cout << "\nRoute Found:\n";
    for (auto node : path) cout << node << " ";
    cout << "\n";

    double total_distance = 0;

    for (int i = 0; i < path.size() - 1; i++) {
        long long u = path[i];
        long long v = path[i + 1];

        for (auto &edge : adj[u]) {
            if (get<0>(edge) == v) {
                total_distance += get<2>(edge);
                break;
            }
        }
    }

    double total_time = dist[destination_node];

    cout << "\nTotal Distance: " << total_distance / 1000.0 << " km\n";
    cout << "Estimated Time: " << total_time / 60.0 << " minutes\n";

    ofstream out("route.txt");
    for (auto node : path) out << node << " ";
    out.close();

    system("python show_map.py");

    cout << "\nMap generated\n";
    system("start map.html");

    return 0;
}
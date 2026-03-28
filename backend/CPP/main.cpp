#include <bits/stdc++.h>
#include "json.hpp"

using namespace std;
using json = nlohmann::json;

typedef pair<double, long long> pii;

unordered_map<long long, vector<pair<long long, double>>> adj;

vector<long long> dijkstra(long long src, long long dest) {
    unordered_map<long long, double> dist;
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
            long long v = edge.first;
            double w = edge.second;

            if (!dist.count(v) || dist[v] > d + w) {
                dist[v] = d + w;
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
    int result = system(command.c_str());

    if (result != 0) {
        cout << "Python script failed!\n";
        return 1;
    }

    ifstream file("graph.json");

    if (!file.is_open() || file.peek() == ifstream::traits_type::eof()) {
        cout << "Error: graph.json is empty or not created!\n";
        return 1;
    }

    json data;
    file >> data;

    long long source_node = data["source_node"];
    long long destination_node = data["destination_node"];

    for (auto &edge : data["edges"]) {
        long long u = edge["from"];
        long long v = edge["to"];
        double w = edge["weight"];

        adj[u].push_back({v, w});
    }

    cout << "\nComputing Route...\n";

    vector<long long> path = dijkstra(source_node, destination_node);

    if (path.empty()) {
        cout << "No route found!\n";
        return 0;
    }

    cout << "\nRoute Found:\n";
    for (auto node : path) cout << node << " ";
    cout << "\n";

    ofstream out("route.txt");
    for (auto node : path) {
        out << node << " ";
    }
    out.close();

    cout << "\nGenerating map...\n";

    int map_result = system("python show_map.py");

    if (map_result != 0) {
        cout << "Failed to generate map!\n";
        return 1;
    }

    cout << "\nMap generated\n";
    system("start map.html");

    return 0;
}
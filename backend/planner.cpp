#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
using namespace std;

struct Activity {
    string name, category, location;
    int cost;
    float hours, rating;
};

struct Accommodation {
    string name, location;
    int cost;
    float rating;
};

struct FoodPlace {
    string name, cuisine;
    int cost;
    float rating;
};

struct Transport {
    string mode;
    int cost;
};

class RishikeshPlanner {
    map<int, int> dailyBudget = {{1,1200},{2,2500},{3,4500},{4,8000},{5,15000}};
    
    vector<Accommodation> stays[6];
    vector<FoodPlace> foods[6];
    vector<Activity> activities;
    Transport trans[6];
    
public:
    RishikeshPlanner() {
       
        stays[1] = {{"Zostel Rishikesh","Tapovan",400,4.2},{"GoStops","Laxman Jhula",350,4.0},{"Shantiyoga Ashram","Ram Jhula",500,4.3}};
        stays[2] = {{"Moustache","Tapovan",800,4.1},{"Hotel Yog Vashishth","Tapovan",1200,3.8},{"Divine Resort","Laxman Jhula",1500,4.0}};
        stays[3] = {{"Hotel Ganga Kinara","Laxman Jhula",2800,4.2},{"Sterling Palm Bliss","Swargashram",3000,4.3},{"The Forest Resort","Tapovan",3500,4.4}};
        stays[4] = {{"Aloha on Ganges","Laxman Jhula",7000,4.6},{"Ganga Beach Resort","Tapovan",6500,4.5}};
        stays[5] = {{"Ananda Himalayas","Narendra Nagar",25000,4.9}};
        
        
        foods[1] = {{"Little Buddha Cafe","Continental",250,4.5},{"Freedom Cafe","Multicuisine",200,4.3},{"Street Food","Indian",80,4.0}};
        foods[2] = {{"Pure Soul Cafe","Healthy",350,4.6},{"The 60's Cafe","Continental",400,4.4},{"Bhandari Swiss Cottage","Indian",300,4.2}};
        foods[3] = {{"Chotiwala","Indian",450,4.5},{"Green Italian Cafe","Italian",600,4.7},{"Pumpernickel German","German",500,4.6}};
        foods[4] = {{"Achanta's Restaurant","Multi",800,4.7},{"Sanskriti Cafe","Fine Dining",700,4.6}};
        foods[5] = {{"Ananda Spa Restaurant","Gourmet",2000,4.9},{"The Sitting Elephant","Fine Dining",1500,4.8}};
        
        
        trans[1] = {"Walking + Local Bus",50};
        trans[2] = {"Shared Auto + Bus",150};
        trans[3] = {"Shared Auto + Taxi",300};
        trans[4] = {"Private Taxi",600};
        trans[5] = {"Private Car with Driver",1500};
        
        
        activities = {
            {"Ganga Aarti","Spiritual","Parmarth Niketan",0,1.0,4.9},
            {"River Rafting 16km","Adventure","Shivpuri",1200,3.0,4.8},
            {"River Rafting 36km","Adventure","Kaudiyala",2500,6.0,4.7},
            {"Yoga Class","Spiritual","Tapovan",400,1.0,4.8},
            {"Bungee Jumping","Adventure","Mohanchatti",3500,1.0,4.6},
            {"Flying Fox","Adventure","Mohanchatti",2000,1.0,4.5},
            {"Mountain Biking","Adventure","Tapovan",1500,3.0,4.4},
            {"Temple Tour","Spiritual","All Areas",0,2.0,4.7},
            {"Meditation Camp","Spiritual","Tapovan",800,2.0,4.6},
            {"Neer Waterfall Trek","Nature","Neer Village",200,4.0,4.5},
            {"Sunset Point","Nature","Tapovan",0,1.5,4.6},
            {"Cafe Hopping","Food","Laxman Jhula",500,2.0,4.5},
            {"Triveni Ghat","Spiritual","Triveni",0,1.0,4.7},
            {"Kunjapuri Temple Trek","Nature","Kunjapuri",300,3.0,4.4},
            {"Beatles Ashram","Spiritual","Tapovan",100,2.0,4.8},
            {"Ayurvedic Massage","Wellness","Tapovan",800,1.5,4.5}
        };
    }
    
    void plan(int tier, int days, vector<string>& prefs) {
        int totalBudget = dailyBudget[tier] * days;
        
        
        sort(stays[tier].begin(), stays[tier].end(), [](auto &a, auto &b){return a.rating>b.rating;});
        sort(foods[tier].begin(), foods[tier].end(), [](auto &a, auto &b){return a.rating>b.rating;});
        
        
        Accommodation selectedStay;
        int stayCost;
        for(auto &stay : stays[tier]) {
            stayCost = stay.cost * days;
            int foodCost = foods[tier][0].cost * 2 * days;
            int transportCost = trans[tier].cost * days;
            int essentials = stayCost + foodCost + transportCost;
            
            if(essentials <= totalBudget) {
                selectedStay = stay;
                break;
            }
        }
        
        if(selectedStay.name.empty()) {
            selectedStay = stays[tier].back();
            stayCost = selectedStay.cost * days;
        }
        
        
        int foodCost = foods[tier][0].cost * 2 * days;
        int transportCost = trans[tier].cost * days;
        int essentialsTotal = stayCost + foodCost + transportCost;
        int activityBudget = totalBudget - essentialsTotal;
        
        
        vector<Activity> validActivities;
        for(auto &act : activities) {
            if(!prefs.empty()) {
                for(auto &p : prefs) {
                    if(act.category == p) {
                        validActivities.push_back(act);
                        break;
                    }
                }
            } else {
                validActivities.push_back(act);
            }
        }
        
        
        sort(validActivities.begin(), validActivities.end(), [](auto &a, auto &b){
            float ratioA = a.cost == 0 ? 999 : a.rating / a.cost;
            float ratioB = b.cost == 0 ? 999 : b.rating / b.cost;
            return ratioA > ratioB;
        });
        
        
        vector<Activity> finalActs;
        int actCost = 0;
        for(auto &act : validActivities) {
            if(actCost + act.cost <= activityBudget) {
                finalActs.push_back(act);
                actCost += act.cost;
            }
        }
        
        
        cout << "\n============================================================\n";
        cout << "     RISHIKESH BUDGET PLANNER - YOUR ITINERARY\n";
        cout << "============================================================\n\n";
        
        cout << "BUDGET SUMMARY\n";
        string tierName[] = {"","Backpacker","Budget","Mid-Range","Premium","Luxury"};
        cout << "   Tier: " << tierName[tier] << "\n";
        cout << "   Days: " << days << "  |  Total Budget: Rs." << totalBudget << "\n\n";
        
        cout << "ACCOMMODATION\n";
        cout << "   " << selectedStay.name << " [Rating: " << selectedStay.rating << "/5]\n";
        cout << "   Location: " << selectedStay.location << "  |  Rs." << selectedStay.cost << "/night\n";
        cout << "   Total: Rs." << stayCost << "\n\n";
        
        cout << "FOOD RECOMMENDATIONS\n";
        for(int i=0; i<min(3,(int)foods[tier].size()); i++) {
            cout << "   " << foods[tier][i].name << " [Rating: " << foods[tier][i].rating << "/5]\n";
            cout << "      Cuisine: " << foods[tier][i].cuisine << "  |  Rs." << foods[tier][i].cost << "/meal\n";
        }
        cout << "   Estimated food cost: Rs." << foodCost << "\n\n";
        
        cout << "TRANSPORT\n";
        cout << "   " << trans[tier].mode << "  |  Rs." << trans[tier].cost << "/day\n";
        cout << "   Total: Rs." << transportCost << "\n\n";
        
        cout << "ACTIVITIES (Budget: Rs." << activityBudget << ")\n";
        if(finalActs.empty()) {
            cout << "   No activities within remaining budget\n";
            if(activityBudget > 0) cout << "   Try selecting cheaper accommodation or reducing days\n";
        } else {
            for(auto &act : finalActs) {
                cout << "   " << act.name << " [" << act.category << "] [Rating: " << act.rating << "/5]\n";
                cout << "      Location: " << act.location << "  |  Rs." << act.cost;
                if(act.cost == 0) cout << " (FREE)";
                cout << "  |  " << act.hours << "hrs\n";
            }
        }
        
        int totalSpent = stayCost + foodCost + transportCost + actCost;
        cout << "\nCOST BREAKDOWN\n";
        cout << "   Accommodation: Rs." << stayCost << "\n";
        cout << "   Food:          Rs." << foodCost << "\n";
        cout << "   Transport:     Rs." << transportCost << "\n";
        cout << "   Activities:    Rs." << actCost << "\n";
        cout << "   --------------------\n";
        cout << "   TOTAL:         Rs." << totalSpent << "\n";
        cout << "   Remaining:     Rs." << (totalBudget - totalSpent) << "\n\n";
        
        cout << "EXPERT TIPS\n";
        if(tier==1) cout << "   * Visit during monsoon (July-Aug) for 30%% off on rafting\n";
        if(tier<=2) cout << "   * Free Ganga Aarti at Parmarth Niketan (6 PM daily)\n";
        if(tier==3) cout << "   * Book combo packages for adventure activities\n";
        if(tier>=4) cout << "   * Try private sunset boat ride on Ganges\n";
        cout << "   * Best time for rafting: September-March\n";
        cout << "   * Book accommodations at least 1 week in advance\n";
        
        if(activityBudget < 0) {
            cout << "\nIMPORTANT: Your essentials cost exceeds budget!\n";
            cout << "   * Consider reducing number of days\n";
            cout << "   * Or choose a lower budget tier\n";
            cout << "   * Or select cheaper accommodation\n";
        } else if(activityBudget < 1000 && days > 3) {
            cout << "\nTIP: Low activity budget. Consider:\n";
            cout << "   * Reducing number of days\n";
            cout << "   * Choosing cheaper accommodation\n";
            cout << "   * Focusing on free activities\n";
        }
        
        cout << "\n============================================================\n";
        cout << "     HAVE A WONDERFUL TRIP TO RISHIKESH!\n";
        cout << "============================================================\n";
    }
};

int main() {
    RishikeshPlanner planner;
    int tier, days, choice;
    vector<string> prefs;
    
    cout << "WELCOME TO PROJECTWISE - RISHIKESH TRAVEL PLANNER\n\n";
    cout << "Budget Tiers:\n";
    cout << "1. Backpacker  (Rs.1200/day) - Hostels, street food\n";
    cout << "2. Budget      (Rs.2500/day) - Basic comfort\n";
    cout << "3. Mid-Range   (Rs.4500/day) - Good hotels\n";
    cout << "4. Premium     (Rs.8000/day) - Premium stays\n";
    cout << "5. Luxury      (Rs.15000/day) - Luxury resorts\n";
    cout << "Select tier (1-5): ";
    cin >> tier;
    
    cout << "Number of days: ";
    cin >> days;
    
    cout << "\nPreferences :\n";
    cout << "1. Adventure   2. Spiritual   3. Food   4. Nature\n";
    cout << "Your choices (press 0 for all): ";
    
    prefs.clear();
    while(cin >> choice) {
        if(choice == 0) {
            prefs.clear();
            break;
        }
        if(choice==1) prefs.push_back("Adventure");
        else if(choice==2) prefs.push_back("Spiritual");
        else if(choice==3) prefs.push_back("Food");
        else if(choice==4) prefs.push_back("Nature");
        if(cin.get()=='\n') break;
    }
    
    planner.plan(tier, days, prefs);
    return 0;
}
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

struct Hotel {
    string name;
    int price;
    float rating;
};

struct Restaurant {
    string name;
    int price;
    float rating;
};

struct Activity {
    string name;
    string type;      
    int cost;
    float rating;
};


class RishikeshPlanner {
private:
    int budgetPerDay[6];
    Hotel hotels[6][3];
    Restaurant restaurants[6][3];
    Activity allActivities[20];
    int activityCount;
    
public:

    RishikeshPlanner() {
        
        budgetPerDay[1] = 1200;   budgetPerDay[2] = 2500;
        budgetPerDay[3] = 4500;   budgetPerDay[4] = 8000;
        budgetPerDay[5] = 15000;
        
        hotels[1][0] = {"Zostel Rishikesh", 400, 4.2};
        hotels[1][1] = {"GoStops", 350, 4.0};
        hotels[1][2] = {"Shantiyoga Ashram", 500, 4.3};
        
        hotels[2][0] = {"Moustache", 800, 4.1};
        hotels[2][1] = {"Hotel Yog Vashishth", 1200, 3.8};
        hotels[2][2] = {"Divine Resort", 1500, 4.0};
        
        hotels[3][0] = {"Hotel Ganga Kinara", 2800, 4.2};
        hotels[3][1] = {"Sterling Palm Bliss", 3000, 4.3};
        hotels[3][2] = {"The Forest Resort", 3500, 4.4};
        
        hotels[4][0] = {"Aloha on Ganges", 7000, 4.6};
        hotels[4][1] = {"Ganga Beach Resort", 6500, 4.5};
        
        hotels[5][0] = {"Ananda Himalayas", 25000, 4.9};
        
        restaurants[1][0] = {"Little Buddha Cafe", 250, 4.5};
        restaurants[1][1] = {"Freedom Cafe", 200, 4.3};
        restaurants[1][2] = {"Street Food", 80, 4.0};
        
        restaurants[2][0] = {"Pure Soul Cafe", 350, 4.6};
        restaurants[2][1] = {"The 60's Cafe", 400, 4.4};
        restaurants[2][2] = {"Bhandari Swiss Cottage", 300, 4.2};
        
        restaurants[3][0] = {"Chotiwala", 450, 4.5};
        restaurants[3][1] = {"Green Italian Cafe", 600, 4.7};
        restaurants[3][2] = {"Pumpernickel German", 500, 4.6};
        
        restaurants[4][0] = {"Achanta's Restaurant", 800, 4.7};
        restaurants[4][1] = {"Sanskriti Cafe", 700, 4.6};
        
        restaurants[5][0] = {"Ananda Spa Restaurant", 2000, 4.9};
        
        
        activityCount = 0;
        allActivities[activityCount++] = {"Ganga Aarti", "Spiritual", 0, 4.9};
        allActivities[activityCount++] = {"Temple Tour", "Spiritual", 0, 4.7};
        allActivities[activityCount++] = {"Triveni Ghat", "Spiritual", 0, 4.7};
        allActivities[activityCount++] = {"Sunset Point", "Nature", 0, 4.6};
        allActivities[activityCount++] = {"River Rafting 16km", "Adventure", 1200, 4.8};
        allActivities[activityCount++] = {"Yoga Class", "Spiritual", 400, 4.8};
        allActivities[activityCount++] = {"Beatles Ashram", "Spiritual", 100, 4.8};
        allActivities[activityCount++] = {"Neer Waterfall Trek", "Nature", 200, 4.5};
        allActivities[activityCount++] = {"Mountain Biking", "Adventure", 1500, 4.4};
        allActivities[activityCount++] = {"Flying Fox", "Adventure", 2000, 4.5};
        allActivities[activityCount++] = {"Bungee Jumping", "Adventure", 3500, 4.6};
        allActivities[activityCount++] = {"River Rafting 36km", "Adventure", 2500, 4.7};
        allActivities[activityCount++] = {"Meditation Camp", "Spiritual", 800, 4.6};
        allActivities[activityCount++] = {"Kunjapuri Temple Trek", "Nature", 300, 4.4};
    }
    
    int partitionHotels(Hotel arr[], int low, int high) {
        float pivot = arr[high].rating;
        int i = low - 1;
        for(int j = low; j < high; j++)
            if(arr[j].rating >= pivot) swap(arr[++i], arr[j]);
        swap(arr[i+1], arr[high]);
        return i+1;
    }
    
    void quickSortHotels(Hotel arr[], int low, int high) {
        if(low < high) {
            int pi = partitionHotels(arr, low, high);
            quickSortHotels(arr, low, pi-1);
            quickSortHotels(arr, pi+1, high);
        }
    }
    
    void sortHotels(Hotel arr[], int n) {
        if(n > 1) quickSortHotels(arr, 0, n-1);
    }
    
    int partitionRestaurants(Restaurant arr[], int low, int high) {
        float pivot = arr[high].rating;
        int i = low - 1;
        for(int j = low; j < high; j++)
            if(arr[j].rating >= pivot) swap(arr[++i], arr[j]);
        swap(arr[i+1], arr[high]);
        return i+1;
    }
    
    void quickSortRestaurants(Restaurant arr[], int low, int high) {
        if(low < high) {
            int pi = partitionRestaurants(arr, low, high);
            quickSortRestaurants(arr, low, pi-1);
            quickSortRestaurants(arr, pi+1, high);
        }
    }
    
    void sortRestaurants(Restaurant arr[], int n) {
        if(n > 1) quickSortRestaurants(arr, 0, n-1);
    }
    
    float activityValue(Activity a) {
        if(a.cost == 0) return 999;
        return a.rating / a.cost;
    }
    
    int partitionActivities(Activity arr[], int low, int high) {
        float pivot = activityValue(arr[high]);
        int i = low - 1;
        for(int j = low; j < high; j++)
            if(activityValue(arr[j]) >= pivot) swap(arr[++i], arr[j]);
        swap(arr[i+1], arr[high]);
        return i+1;
    }
    
    void quickSortActivities(Activity arr[], int low, int high) {
        if(low < high) {
            int pi = partitionActivities(arr, low, high);
            quickSortActivities(arr, low, pi-1);
            quickSortActivities(arr, pi+1, high);
        }
    }
    
    void sortActivities(Activity arr[], int n) {
        if(n > 1) quickSortActivities(arr, 0, n-1);
    }
    

    int filterByPref(Activity src[], int srcCount, Activity dest[], vector<string>& prefs) {
        int cnt = 0;
        for(int i = 0; i < srcCount; i++) {
            if(prefs.empty()) {
                dest[cnt++] = src[i];
            } else {
                for(string p : prefs) {
                    if(src[i].type == p) {
                        dest[cnt++] = src[i];
                        break;
                    }
                }
            }
        }
        return cnt;
    }
    
    Hotel selectHotel(int tier, int days, int hotelBudget) {
        for(int t = tier; t >= 1; t--) {
            int cnt = 0;
            while(cnt < 3 && hotels[t][cnt].name != "") cnt++;
            sortHotels(hotels[t], cnt);
            for(int i = 0; i < cnt; i++) {
                if(hotels[t][i].price * days <= hotelBudget)
                    return hotels[t][i];
            }
        }
        return hotels[1][0];
    }

    Restaurant selectRestaurant(int tier, int foodBudgetPerMeal) {
        for(int t = tier; t >= 1; t--) {
            int cnt = 0;
            while(cnt < 3 && restaurants[t][cnt].name != "") cnt++;
            sortRestaurants(restaurants[t], cnt);
            for(int i = 0; i < cnt; i++) {
                if(restaurants[t][i].price <= foodBudgetPerMeal)
                    return restaurants[t][i];
            }
        }
        return restaurants[1][2];
    }
    
    int selectActivities(Activity avail[], int n, Activity selected[], int budget) {
        sortActivities(avail, n);
        int spent = 0, cnt = 0;
        for(int i = 0; i < n; i++) {
            if(spent + avail[i].cost <= budget) {
                selected[cnt++] = avail[i];
                spent += avail[i].cost;
            }
        }
        return cnt;
    }
    

    void plan(int tier, int days, vector<string>& prefs) {
        int total = budgetPerDay[tier] * days;
        
        int hotelBudget     = (int)(total * 0.40);
        int foodBudget      = (int)(total * 0.25);
        int transportBudget = (int)(total * 0.10);
        int activityBudget  = total - hotelBudget - foodBudget - transportBudget;

        Hotel hotel = selectHotel(tier, days, hotelBudget);
        int hotelCost = hotel.price * days;

        int foodBudgetPerMeal = foodBudget / (2 * days);
        Restaurant rest = selectRestaurant(tier, foodBudgetPerMeal);

        int foodCost = min(rest.price * 2 * days, foodBudget);

        int transportCost = transportBudget;

        Activity filtered[20], selected[20];
        int filteredCount = filterByPref(allActivities, activityCount, filtered, prefs);
        int selectedCount = selectActivities(filtered, filteredCount, selected, activityBudget);
      
        int activityTotal = 0;
        for(int i = 0; i < selectedCount; i++) activityTotal += selected[i].cost;
        int totalSpent = hotelCost + foodCost + transportCost + activityTotal;
        
        cout << "\n========================================\n";
        cout << "       RISHIKESH TRIP PLANNER\n";
        cout << "========================================\n\n";
        
        string tiers[] = {"", "Backpacker", "Budget", "Mid-Range", "Premium", "Luxury"};
        cout << "BUDGET: " << tiers[tier] << " | " << days << " days | Rs." << total << "\n\n";
        
        cout << "PREFERENCES: ";
        if(prefs.empty()) cout << "All";
        else for(string p : prefs) cout << p << " ";
        cout << "\n\n";

        cout << "BUDGET ALLOCATION:\n";
        cout << "   Hotel:      Rs." << hotelBudget     << " (40%)\n";
        cout << "   Food:       Rs." << foodBudget      << " (25%)\n";
        cout << "   Transport:  Rs." << transportBudget << " (10%)\n";
        cout << "   Activities: Rs." << activityBudget  << " (25%)\n\n";
        
        cout << "HOTEL: " << hotel.name << " (" << hotel.rating << "/5)\n";
        cout << "       Rs." << hotel.price << "/night | Total: Rs." << hotelCost << "\n\n";
        
        cout << "FOOD: " << rest.name << " (" << rest.rating << "/5)\n";
        cout << "      Rs." << rest.price << "/meal | Total: Rs." << foodCost << "\n\n";
        
        cout << "TRANSPORT: Rs." << transportCost << "\n\n";
        
        cout << "ACTIVITIES (Budget: Rs." << activityBudget << ")\n";
        if(selectedCount == 0) {
            cout << "   None within budget\n";
        } else {
            for(int i = 0; i < selectedCount; i++) {
                cout << "   " << (i+1) << ". " << selected[i].name 
                     << " [" << selected[i].type << "]\n";
                cout << "      Rs." << selected[i].cost 
                     << (selected[i].cost == 0 ? " (FREE)" : "") 
                     << " | Rating: " << selected[i].rating << "/5\n";
            }
        }
        
        cout << "\nCOST BREAKDOWN:\n";
        cout << "   Hotel:      Rs." << hotelCost << "\n";
        cout << "   Food:       Rs." << foodCost << "\n";
        cout << "   Transport:  Rs." << transportCost << "\n";
        cout << "   Activities: Rs." << activityTotal << "\n";
        cout << "   -------------------------\n";
        cout << "   TOTAL:      Rs." << totalSpent << "\n";
        cout << "   Remaining:  Rs." << (total - totalSpent) << "\n";
        
        if(totalSpent > total) {
            cout << "\n  WARNING: Budget too low! Reduce days or choose lower tier.\n";
        }
        
        cout << "\n========================================\n";
        cout << "         HAVE A GREAT TRIP!\n";
        cout << "========================================\n";
    }
};

int main() {
    RishikeshPlanner planner;
    int tier, days, choice;
    vector<string> prefs;
    
    cout << "WELCOME TO RISHIKESH TRAVEL PLANNER\n\n";
    cout << "Budget Tiers:\n";
    cout << "1. Backpacker  (Rs.1200/day)\n";
    cout << "2. Budget      (Rs.2500/day)\n";
    cout << "3. Mid-Range   (Rs.4500/day)\n";
    cout << "4. Premium     (Rs.8000/day)\n";
    cout << "5. Luxury      (Rs.15000/day)\n";
    cout << "Select tier: ";
    cin >> tier;
    
    cout << "Number of days: ";
    cin >> days;
    
    cout << "\nPreferences (1.Adventure 2.Spiritual 3.Nature, 0 to finish):\n";
    while(true) {
        cout << "Choice: ";
        cin >> choice;
        if(choice == 0) break;
        else if(choice == 1) prefs.push_back("Adventure"), cout << "   + Adventure\n";
        else if(choice == 2) prefs.push_back("Spiritual"), cout << "   + Spiritual\n";
        else if(choice == 3) prefs.push_back("Nature"), cout << "   + Nature\n";
        else if(choice == 4) { prefs.clear(); cout << "   All activities\n"; break; }
    }
    
    planner.plan(tier, days, prefs);
    return 0;
}

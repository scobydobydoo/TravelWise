import os
#   base_price  – INR floor price at quality=1, location=1, season=1
#   weight_q    – Rs added per quality point (reflects certification premium)
#   weight_l    – Rs added per location point (tourist-zone surcharge)
#   weight_s    – Rs added per season point (demand-driven spike)
#   description – readable label for display
#   tips        – real consumer advice shown after prediction

CATALOGUE = {
    "rafting_16km": {
        "description": "River Rafting - 16 km (Shivpuri to Rishikesh)",
        "base_price": 450,
        "weight_q": 80,   
        "weight_l": 60,   
        "weight_s": 120,  
        "tips": "Always insist on BIS-certified life jackets. Avoid touts near Ram Jhula bridge."
    },
    "rafting_36km": {
        "description": "River Rafting - 36 km (Marine Drive to Rishikesh)",
        "base_price": 900,
        "weight_q": 150,
        "weight_l": 80,
        "weight_s": 200,
        "tips": "Book via registered GMVN or certified operators. Groups of 6+ typically get 20% off."
    },
    "bungee_jumping": {
        "description": "Bungee Jumping (Jumpin Heights, Mohan Chatti - 83m)",
        "base_price": 2500,
        "weight_q": 300,  
        "weight_l": 200,
        "weight_s": 350,
        "tips": "Only ONE certified bungee site exists near Rishikesh (Jumpin Heights). Beware all other 'bungee' offers."
    },
    "flying_fox": {
        "description": "Flying Fox / Zipline",
        "base_price": 800,
        "weight_q": 120,
        "weight_l": 100,
        "weight_s": 150,
        "tips": "Combo packages (bungee + flying fox + giant swing) offer 20-30% better value than single bookings."
    },
    "yoga_class": {
        "description": "Yoga Class (1 session, ~90 min)",
        "base_price": 200,
        "weight_q": 150,  # certified Iyengar/Sivananda teacher vs random
        "weight_l": 100,
        "weight_s": 180,  # International Yoga Festival (March) = 3x spike
        "tips": "Yoga Festival (March) prices spike 3x. Monthly ashram packages are 60% cheaper per session."
    },
    "meditation_retreat": {
        "description": "Meditation / Retreat Session (half-day)",
        "base_price": 400,
        "weight_q": 200,
        "weight_l": 120,
        "weight_s": 150,
        "tips": "Parmarth Niketan offers FREE evening Ganga Aarti and meditation. Do not pay touts for this."
    },
    "ayurvedic_massage": {
        "description": "Ayurvedic Massage / Spa (60 min full body)",
        "base_price": 600,
        "weight_q": 200,  
        "weight_l": 150,
        "weight_s": 100,
        "tips": "Ask for a BAMS-qualified Ayurvedic therapist certificate. Avoid ghat-side massage offers from strangers."
    },
    "rudraksha_beads": {
        "description": "Rudraksha Mala / Beads (108-bead standard)",
        "base_price": 80,
        "weight_q": 250,  
        "weight_l": 60,
        "weight_s": 40,
        "tips": "5-mukhi rudraksha is common and genuine. 1- mukhi sold cheaply is almost certainly fake."
    },
    "brass_idol": {
        "description": "Brass / Copper Religious Idol",
        "base_price": 150,
        "weight_q": 180,
        "weight_l": 70,
        "weight_s": 30,
        "tips": "First quoted price near Ram Jhula market is typically 3x fair price. Bargain firmly and walk away once."
    },
    "hippie_clothes": {
        "description": "Hippie / Bohemian Wear (kurta, harem pants)",
        "base_price": 120,
        "weight_q": 100,
        "weight_l": 80,
        "weight_s": 50,
        "tips": "Tapovan boutiques charge 2x for the same stock found at Laxman Jhula side-lane shops."
    },
    "cotton_clothes": {
        "description": "Plain Cotton Clothes (local weave, t-shirt / shirt)",
        "base_price": 100,
        "weight_q": 80,
        "weight_l": 60,
        "weight_s": 30,
        "tips": "Verify hand-woven labels - machine-print fabric is routinely sold as hand-block-printed cloth."
    },

    "german_bakery": {
        "description": "German Bakery Style Cafe (meal + drink)",
        "base_price": 180,
        "weight_q": 120,
        "weight_l": 150,  
        "weight_s": 80,
        "tips": "Little Buddha Cafe is iconic but overpriced. Equally good meals 200m off the main lane at half the cost."
    },
    "israeli_food": {
        "description": "Israeli / Continental Restaurant (per person)",
        "base_price": 200,
        "weight_q": 130,
        "weight_l": 160,
        "weight_s": 90,
        "tips": "Many Israeli cafes cluster near Laxman Jhula. Shakshouka and hummus quality varies - read recent reviews."
    },
    "local_thali": {
        "description": "Local Vegetarian Thali (full meal)",
        "base_price": 60,
        "weight_q": 50,
        "weight_l": 80,   
        "weight_s": 30,
        "tips": "Rs 80-120 thali near Triveni Ghat is wholesome and filling. Same dish costs Rs 250+ near bungee camps."
    },
    "taxi_local": {
        "description": "Taxi / Cab (local, up to 10 km within Rishikesh)",
        "base_price": 150,
        "weight_q": 60,   
        "weight_l": 80,
        "weight_s": 100,
        "tips": "Use Ola / Uber where available. For single passengers, autorickshaws are significantly cheaper."
    },
    "bike_rental": {
        "description": "Bike / Scooter Rental (per day)",
        "base_price": 300,
        "weight_q": 150,  
        "weight_l": 100,
        "weight_s": 120,
        "tips": "Photograph the entire bike BEFORE riding off. Document all scratches - renters are often wrongly charged for existing damage."
    },
}


# SECTION 2 : LINEAR REGRESSION PRICE PREDICTOR


def predict_fair_price(category_key, quality, location, season):
    """
    price = base + w_q*quality + w_l*location + w_s*season
    """
    item = CATALOGUE[category_key]
    predicted = (
        item["base_price"]
        + item["weight_q"] * quality
        + item["weight_l"] * location
        + item["weight_s"] * season
    )
    return round(predicted, 2)


def evaluate_offer(offered_price, fair_price):
    """
    Thresholds:
      > +20%  : SCAM         
      +10-20% : SLIGHTLY HIGH 
      +-10%   : FAIR          
      -10-20% : GOOD DEAL     
      < -20%  : SUSPICIOUS    
    """
    deviation = ((offered_price - fair_price) / fair_price) * 100

    if deviation > 20:
        status = "SCAM"
        msg = (
            "WARNING - SCAM ALERT! Overcharged by {:.1f}%.\n"
            "   Likely causes: Tourist zone premium, peak season surge,\n"
            "   or vendor targeting first-time visitors."
        ).format(deviation)
    elif deviation < -20:
        status = "SUSPICIOUS"
        msg = (
            "SUSPICIOUS PRICE! {:.1f}% BELOW fair value.\n"
            "   Likely causes: Fake/poor quality product, bait-and-switch,\n"
            "   or hidden charges will be added later."
        ).format(abs(deviation))
    elif deviation > 10:
        status = "SLIGHTLY HIGH"
        msg = (
            "Slightly overpriced by {:.1f}%. Negotiable.\n"
            "   Compare with 2-3 nearby vendors before buying."
        ).format(deviation)
    elif deviation < -10:
        status = "GOOD DEAL"
        msg = (
            "GOOD DEAL! {:.1f}% below fair market value.\n"
            "   Verify quality/authenticity before purchasing."
        ).format(abs(deviation))
    else:
        status = "FAIR"
        msg = (
            "FAIR PRICE. Within +-10% of market estimate.\n"
            "   Proceed with confidence."
        )

    return status, deviation, msg


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3 : PRICE DRIVER EXPLANATION (Bonus feature)
# Identifies which of the three factors contributes most to the price
# and returns a human-readable explanation sentence.
# ──────────────────────────────────────────────────────────────────────────────

def price_explanation(quality, location, season, fair_price, category_key):
    """
    Determine the biggest price driver and explain it in plain language.
    Compares three contribution amounts: quality, location, season.
    """
    item = CATALOGUE[category_key]
    contrib_q = item["weight_q"] * quality
    contrib_l = item["weight_l"] * location
    contrib_s = item["weight_s"] * season

    drivers = {
        "Quality level":    contrib_q,
        "Location premium": contrib_l,
        "Season demand":    contrib_s,
    }
    top_driver = max(drivers, key=drivers.get)
    top_val = drivers[top_driver]
    pct = round((top_val / fair_price) * 100, 1) if fair_price else 0

    notes = {
        "Quality level":    "Certified staff, premium gear, or branded service inflates cost.",
        "Location premium": "Prime tourist zones (Tapovan / Laxman Jhula) carry a location surcharge.",
        "Season demand":    "Peak season (Oct-Nov / Yoga Festival) drives demand-based price spikes.",
    }
    return "Top price driver: {} (~{}% of fair price). {}".format(
        top_driver, pct, notes[top_driver]
    )


WIDTH = 66  # console width for borders

def clear():
    """Clear terminal screen cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")

def hr(char="="):
    print(char * WIDTH)

def header():
    hr()
    print("  MARKET SCAM DETECTOR ".center(WIDTH))
    print("  Fair Price Estimator for Tourists & Travellers".center(WIDTH))
    hr()

def print_categories():
    print()
    hr("-")
    print("  {:<4} {:<44} {}".format("No.", "Category / Service", "Base Rs"))
    hr("-")
    for idx, (key, val) in enumerate(CATALOGUE.items(), 1):
        desc = val["description"]
        if len(desc) > 44:
            desc = desc[:41] + "..."
        print("  {:<4} {:<44} Rs{}".format(idx, desc, val["base_price"]))
    hr("-")

def get_int_input(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt).strip())
            if lo <= val <= hi:
                return val
            print("  >> Please enter a number between {} and {}.".format(lo, hi))
        except ValueError:
            print("  >> Invalid input. Please enter a whole number.")

def get_float_input(prompt):
    while True:
        try:
            val = float(input(prompt).strip())
            if val > 0:
                return val
            print("  >> Price must be a positive number.")
        except ValueError:
            print("  >> Invalid input. Please enter a numeric price.")

def explain_factors():
    print()
    hr("-")
    print("  FACTOR RATING GUIDE  (1 = lowest  |  5 = highest)")
    hr("-")
    print()
    print("  QUALITY (1-5)")
    print("    1  Very basic - uncertified, poor gear, no training")
    print("    2  Below average")
    print("    3  Average / decent condition")
    print("    4  Good / well-maintained")
    print("    5  Premium - certified, brand-new, expert staff")
    print()
    print("  LOCATION (1-5)")
    print("    1  Remote / local market (bypass roads, Muni-ki-Reti)")
    print("    2  Rishikesh main town (Triveni Ghat area)")
    print("    3  Ram Jhula / Sivananda Ashram zone")
    print("    4  Laxman Jhula main lane")
    print("    5  Tapovan (premium international tourist hub)")
    print()
    print("  SEASON (1-5)")
    print("    1  Monsoon off-season (Jul-Aug - many closures)")
    print("    2  Early summer (Jun)")
    print("    3  Shoulder season (Feb, Dec)")
    print("    4  High season (Mar-May, International Yoga Festival)")
    print("    5  Peak season (Oct-Nov, post-monsoon white water rafting)")
    print()
    hr("-")

def show_result(item_name, fair_price, offered, status, deviation, msg, tips, explanation):
    """Render the complete analysis card to the console."""
    low  = round(fair_price * 0.80, 2)
    high = round(fair_price * 1.20, 2)

    print()
    hr()
    print("  PRICE ANALYSIS RESULT".center(WIDTH))
    hr()
    print("  Item            : {}".format(item_name))
    print("  Predicted Fair  : Rs {:,.0f}".format(fair_price))
    print("  Acceptable Range: Rs {:,.0f}  to  Rs {:,.0f}  (+-20%)".format(low, high))
    print("  Vendor Price    : Rs {:,.0f}".format(offered))
    print("  Deviation       : {:+.1f}%".format(deviation))
    hr("-")
    print("  VERDICT         : [ {} ]".format(status))
    hr("-")
    for line in msg.split("\n"):
        print("  {}".format(line))
    hr("-")
    print("  INSIGHT:")
    # Word-wrap the explanation
    _wrap_print(explanation, indent="    ")
    hr("-")
    print("  LOCAL TIP:")
    _wrap_print(tips, indent="    ")
    hr()

def _wrap_print(text, indent="  "):
    """Wrap and print text within console WIDTH."""
    words = text.split()
    line = indent
    for w in words:
        if len(line) + len(w) + 1 > WIDTH - 2:
            print(line)
            line = indent + w + " "
        else:
            line += w + " "
    if line.strip():
        print(line)


def main():
    clear()
    header()

    keys = list(CATALOGUE.keys())  

    while True:
        print()
        print("  MAIN MENU")
        print("  [1]  Check if a vendor price is fair")
        print("  [2]  View factor rating guide")
        print("  [3]  Browse all {} categories".format(len(keys)))
        print("  [0]  Exit")
        print()
        choice = input("  Your choice: ").strip()

        if choice == "0":
            print()
            print("  Have a nice day!!!")
            print()
            break

        elif choice == "2":
            explain_factors()
            input("\n  Press Enter to return to menu...")
            clear()
            header()

        elif choice == "3":
            print_categories()
            input("\n  Press Enter to return to menu...")
            clear()
            header()

        elif choice == "1":
            clear()
            header()
            print_categories()
            print()

            cat_num = get_int_input(
                "  Select category number (1-{}): ".format(len(keys)), 1, len(keys)
            )
            cat_key = keys[cat_num - 1]
            item = CATALOGUE[cat_key]
            print("\n  Selected : {}".format(item["description"]))

            print()
            print("  Rate the following (1 = lowest, 5 = highest).")
            print("  Use option [2] in the main menu for the detailed guide.")
            print()
            quality  = get_int_input("  Quality Level    (1=basic   ... 5=premium) : ", 1, 5)
            location = get_int_input("  Location Factor  (1=remote  ... 5=Tapovan) : ", 1, 5)
            season   = get_int_input("  Season Factor    (1=offseason .. 5=peak)   : ", 1, 5)

            offered = get_float_input("\n  Vendor asking price (in Rs): ")

            fair_price = predict_fair_price(cat_key, quality, location, season)

            status, deviation, msg = evaluate_offer(offered, fair_price)

            explanation = price_explanation(quality, location, season, fair_price, cat_key)

            show_result(
                item_name=item["description"],
                fair_price=fair_price,
                offered=offered,
                status=status,
                deviation=deviation,
                msg=msg,
                tips=item["tips"],
                explanation=explanation
            )

            input("\n  Press Enter to return to menu...")
            clear()
            header()

        else:
            print("  >> Invalid choice. Enter 0, 1, 2, or 3.")


if __name__ == "__main__":
    main()
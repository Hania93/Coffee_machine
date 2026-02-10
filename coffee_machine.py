from coffee_machine_data import drinks, express_resources as DEFAULT_RESOURCES, express_coins as DEFAULT_COINS, INIT_EKSPRESS_RESOURCES
import os, json, copy
from colorama import init, Fore, Style

init(autoreset=True) 

# ---------------------- CONSTANTS ----------------------
YES = "yes"
NO = "no"
STATE_FILE = "machine_state.json"

# ---------------------- UTILS ----------------------
def save_state(resources, coins):
    """
    Saves the current state of the machine (resources and coins) to a JSON file.
    This allows the machine to persist its state across runs, so that resources and coin inventory are maintained even after the program is closed and reopened.        
    
    :param resources: Dictionary with keys: coffee_g, water_ml, milk_ml representing current machine resources
    :param coins: Dictionary with keys: coin_value_cents, value_count representing current coin inventory
    :return: True if the state was successfully saved, False otherwise
    """
    state = {
        "resources": resources,
        "coins": coins
    }
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)
        print("\n💾 Machine state saved.")
        return True
    return False

def load_state(default_resources, default_coins):
    """
    Loads the saved state of the machine (resources and coins) from a JSON file.
    If no saved state exists, it returns the default resources and coins.
    
    :param default_resources: Default resources dictionary with keys: coffee_g, water_ml, milk_ml representing initial machine resources        
    :param default_coins: Default coins dictionary with keys: coin_value_cents, value_count representing initial coin inventory
    :return: Tuple of (resources, coins) where resources is a dictionary with keys: coffee_g, water_ml, milk_ml and coins is a dictionary with keys: coin_value_cents, value_count
    """
    if not os.path.exists(STATE_FILE):
        print("No saved state found. Starting with initial resources and coins.")
        return copy.deepcopy(default_resources), copy.deepcopy(default_coins)

    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print("⚠ Error reading state file. Resetting to defaults.")
        print(f"Reason: {e}")
        return copy.deepcopy(default_resources), copy.deepcopy(default_coins)

    if not isinstance(state, dict):
        print("⚠ Invalid state format. Resetting to defaults.")
        return copy.deepcopy(default_resources), copy.deepcopy(default_coins)

    if "resources" not in state or "coins" not in state:
        print("⚠ Missing keys in state file. Resetting to defaults.")
        return copy.deepcopy(default_resources), copy.deepcopy(default_coins)

    resources = state["resources"]
    coins_raw = state["coins"]

    required_resources_keys = {"coffee_g", "water_ml", "milk_ml"}
    if not isinstance(resources, dict) or not required_resources_keys.issubset(resources.keys()):
        print("⚠ Invalid resources data. Resetting to defaults.")
        return copy.deepcopy(default_resources), copy.deepcopy(default_coins)

    for key in required_resources_keys:
        if not isinstance(resources.get(key), int) or resources[key] < 0:
            print(f"⚠ Invalid resource value for '{key}'. Resetting to defaults.")
            return copy.deepcopy(default_resources), copy.deepcopy(default_coins)
        
    if not isinstance(coins_raw, dict):
        print("⚠ Invalid coins data. Resetting to defaults.")
        return copy.deepcopy(default_resources), copy.deepcopy(default_coins)

    coins = {}
    for k, v in coins_raw.items():
        try:
            k_int = int(k)
            if not isinstance(v, int) or v < 0:
                raise ValueError
            coins[k_int] = v
        except ValueError:
            print(f"⚠ Invalid coin entry: {k}:{v}. Resetting to defaults.")
            return copy.deepcopy(default_resources), copy.deepcopy(default_coins)

    print("💾 Machine state loaded (validated).")
    return resources, coins

def clear_console():
    """
    Clears the console screen. Works on both Windows and Unix-based systems.
        
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def show_resources(resources):
    """
    Displays the current resources of the machine in a user-friendly format.
    
    :param resources: Dictionary with keys: coffee_g, water_ml, milk_ml representing current machine resources
    """   
    print(f"\n[Machine Resources]")
    print(f"Coffee: {Fore.GREEN}{resources['coffee_g']}g{Fore.RESET} | Water: {Fore.GREEN}{resources['water_ml']}ml{Fore.RESET} | Milk: {Fore.GREEN}{resources['milk_ml']}ml{Fore.RESET}\n")

def format_money(amount_cents):
    """
    Formats an amount in cents to a string in dollars with 2 decimal places.
    
    :param amount_cents: Amount in cents to be formatted
    :return: Formatted string in dollars with 2 decimal places
    :rtype: str
    """
    return f"${amount_cents/100:.2f}"

# ---------------------- DRINK SELECTION ----------------------
def select_drink(drinks_list):
    """
    Displays the menu and allows the user to select a drink.
    Validates the correctness of the choice.
    
    :param drinks_list: List of drink dictionaries with keys: name, coffee_g, water_ml, milk_ml, price_cents
    :return: The selected drink dictionary
    """
    clear_console()
    print(f"☕{Fore.LIGHTBLUE_EX} Welcome to the Coffee Machine ☕{Fore.RESET}\n")
    print(f"Please select a drink:\n")

    for i, drink in enumerate(drinks_list, start=1):
        print(f"{Fore.LIGHTCYAN_EX} [{i}] {drink['name']:10} - {format_money(drink['price_cents'])}{Fore.RESET}")

    while True:
        try:
            choice = int(input("\nEnter the drink number: "))
            if not 1 <= choice <= len(drinks_list):
                raise ValueError
            selected = drinks_list[choice-1]
            print(f"\nYou selected: {Fore.GREEN}{selected['name']} - {format_money(selected['price_cents'])}{Fore.RESET}")
            return selected
        except ValueError:
            print(f"Invalid input! Choose a number from 1 to {len(drinks_list)}.")

# ---------------------- RESOURCE MANAGEMENT ----------------------
def can_make_drink(drink, resources):
    """
    Checks if the machine has enough resources to make the selected drink.
    
    :param drink: Drink dictionary with keys: name, coffee_g, water_ml, milk_ml, price_cents
    :param resources: Dictionary with keys: coffee_g, water_ml, milk_ml representing current machine resources
    :return: True if the drink can be made, False otherwise
    """
    return (drink['coffee_g'] <= resources['coffee_g'] and
            drink['water_ml'] <= resources['water_ml'] and
            drink['milk_ml'] <= resources['milk_ml'])

def check_what_missing(drink, resources):
    """
    Checks which specific resources are insufficient to make the selected drink.
    
    :param drink: Drink dictionary with keys: name, coffee_g, water_ml, milk_ml, price_cents
    :param resources: Dictionary with keys: coffee_g, water_ml, milk_ml representing current machine resources
    :return: List of resource names that are insufficient (e.g., ['coffee', 'milk'])
    """
    missing = []
    if drink['coffee_g'] > resources['coffee_g']:
        missing.append('coffee')
    if drink['water_ml'] > resources['water_ml']:
        missing.append('water')
    if drink['milk_ml'] > resources['milk_ml']:
        missing.append('milk')
    for r in missing:
        print(f"⚠ Not enough {r}!")
    return missing

def refill_resource(resource, resources):
    """
    Refills the specified resource to its initial level.
    
    :param resource: String name of the resource to refill ('coffee', 'water', or 'milk')
    :param resources: Dictionary with keys: coffee_g, water_ml, milk_ml representing current machine resources
    """
    mapping = {'coffee':'coffee_g', 'water':'water_ml', 'milk':'milk_ml'}
    resources[mapping[resource]] = INIT_EKSPRESS_RESOURCES[mapping[resource]]
    print(f"{resource.capitalize()} refilled!")

# ---------------------- PAYMENT ----------------------    
def pay_for_drink_ui(drink, express_coins):
    """
    Handles user interaction for inserting coins and making payment.
    
    :param drink: Drink dictionary with 'name' and 'price_cents'
    :param express_coins: Machine coin inventory {coin_cents: count}
    :return: True if payment succeeded, False otherwise
    """
    price_cents = drink['price_cents']
    print(f"\n💰 Please insert {Fore.GREEN}{format_money(price_cents)}{Fore.RESET}")
    

    available_coins = sorted([c for c, count in express_coins.items() if count > 0], reverse=True)
    if not available_coins:
        print(f"{Fore.RED}❌ Machine has no coins available. Cannot accept payment.{Fore.RESET}")
        return False

    print(f"Accepted coins: {Fore.GREEN}{', '.join([format_money(c) for c in available_coins])}{Fore.RESET}")
    inserted_cents = []
    total_inserted = 0

    while total_inserted < price_cents:
        print(f"Paid: {Fore.GREEN}{format_money(total_inserted)}{Fore.RESET} | Remaining: {Fore.LIGHTYELLOW_EX}{format_money(price_cents - total_inserted)}{Fore.RESET}")
        try:
            coin = float(input(f"Insert coin ({Fore.RED}0 to cancel{Fore.RESET}) "))
            coin_cents = int(round(coin * 100))
            
            if coin_cents == 0:
                print(Fore.RED + "Payment cancelled.")
                if inserted_cents:
                    print(f"💸 Refunding: {Fore.YELLOW}{format_money(sum(inserted_cents))}{Fore.RESET} -> {[c/100 for c in inserted_cents]}")
                return False

            if coin_cents not in available_coins:
                print(f"{Fore.RED}Invalid coin!{Fore.RESET}")
                continue

            inserted_cents.append(coin_cents)
            total_inserted += coin_cents

        except ValueError:
            print(f"{Fore.RED}Invalid input!{Fore.RESET}")

    # Payment done, try to process
    try:
        change = process_payment(price_cents, inserted_cents, express_coins)
        if change:
            print(f"💸 Change returned: {Fore.YELLOW}{format_money(sum(change))}{Fore.RESET} -> {[c/100 for c in change]}")
        else:
            print("💸 No change needed.")
        return True
    except ValueError as e:
        print(e)
        print("💸 Refunding inserted coins.")
        return False
    
def process_payment(price_cents, inserted_cents, express_coins):
    """
    Processes the payment logic for a given price.
    Updates express_coins and returns the change if payment is sufficient.

    :param price_cents: Price of the drink in cents
    :param inserted_cents: List of inserted coins in cents
    :param express_coins: Dictionary {coin_cents: count} representing machine coins
    :return: List of change coins in cents
    :raises ValueError: if not enough money or cannot return exact change
    """
    temp_coins = express_coins.copy()
    
    # Add inserted coins to temp inventory
    for c in inserted_cents:
        temp_coins[c] = temp_coins.get(c, 0) + 1

    total_inserted = sum(inserted_cents)
    if total_inserted < price_cents:
        raise ValueError("Not enough money inserted.")

    change_cents = total_inserted - price_cents
    change_list = []

    if change_cents == 0:
        # Exact payment, no change
        express_coins.clear()
        express_coins.update(temp_coins)
        return []

    # Calculate change using greedy algorithm
    denominations = sorted(temp_coins.keys(), reverse=True)
    for denom in denominations:
        while change_cents >= denom and temp_coins[denom] > 0:
            temp_coins[denom] -= 1
            change_cents -= denom
            change_list.append(denom)

    if change_cents != 0:
        raise ValueError("Cannot return exact change with available coins!")

    # Update machine coins
    express_coins.clear()
    express_coins.update(temp_coins)
    return change_list


# ---------------------- MAKE DRINK ----------------------
def make_drink(drink, resources):
    """
    Deducts the required resources from the machine to make the selected drink.
    Displays a message to the user and shows the remaining resources.
    
    :param drink: Drink dictionary with keys: name, coffee_g, water_ml, milk_ml, price_cents
    :param resources: Dictionary with keys: coffee_g, water_ml, milk_ml representing current machine resources
    """
    resources['coffee_g'] -= drink['coffee_g']
    resources['water_ml'] -= drink['water_ml']
    resources['milk_ml'] -= drink['milk_ml']
    print(f"\n☕{Fore.MAGENTA} Enjoy your {drink['name']}! {Fore.RESET}\n")
    show_resources(resources)

# ---------------------- MAIN LOOP ----------------------
def main():
    """
    Main function that runs the coffee machine program.
    Handles the main loop of the program, including drink selection, resource checking, payment processing, and state saving/loading.
    """
    express_resources, express_coins = load_state(DEFAULT_RESOURCES, DEFAULT_COINS)

    want_coffee = True

    while want_coffee:
        drink = select_drink(drinks)

        if can_make_drink(drink, express_resources):
            if pay_for_drink_ui(drink, express_coins):
                make_drink(drink, express_resources)
        else:
            missing = check_what_missing(drink, express_resources)
            for r in missing:
                resp = ""
                while resp not in [YES, NO]:
                    resp = input(f"Do you want to refill {r}? ({Fore.GREEN}{YES}{Fore.RESET}/{Fore.RED}{NO}{Fore.RESET}): ").lower()
                if resp == YES:
                    refill_resource(r, express_resources)
                    show_resources(express_resources)

            if can_make_drink(drink, express_resources):
                if pay_for_drink_ui(drink, express_coins):
                    make_drink(drink, express_resources)

        resp = ""
        while resp not in [YES, NO]:
            resp = input(f"Do you want to make another drink? ({Fore.GREEN}{YES}{Fore.RESET}/{Fore.RED}{NO}{Fore.RESET}): ").lower()
        want_coffee = resp == YES

    save_state(express_resources, express_coins)
    print("\n👋 Thank you! See you next time!")

# ---------------------- START ----------------------
main()

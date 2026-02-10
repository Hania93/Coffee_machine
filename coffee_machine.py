from coffee_machine_data import drinks, express_resources, express_coins, INIT_EKSPRESS_RESOURCES
import os, json, copy

YES = "yes"
NO = "no"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_resources(resources):   
    print("\n[Machine Resources]")
    print(f"Coffee: {resources['coffee_g']}g | Water: {resources['water_ml']}ml | Milk: {resources['milk_ml']}ml\n")

def format_money(amount_cents):
    return f"${amount_cents/100:.2f}"

def select_drink(drinks_list):
    clear_console()
    print("☕ Welcome to the Coffee Machine ☕\n")
    print("Please select a drink:\n")

    for i, drink in enumerate(drinks_list, start=1):
        print(f" [{i}] {drink['name']:10} - {format_money(drink['price_cents'])}")

    while True:
        try:
            choice = int(input("\nEnter the drink number: "))
            if not 1 <= choice <= len(drinks_list):
                raise ValueError
            selected = drinks_list[choice-1]
            print(f"\nYou selected: {selected['name']} - {format_money(selected['price_cents'])}")
            return selected
        except ValueError:
            print(f"Invalid input! Choose a number from 1 to {len(drinks_list)}.")

def can_make_drink(drink, resources):
    return (drink['coffee_g'] <= resources['coffee_g'] and
            drink['water_ml'] <= resources['water_ml'] and
            drink['milk_ml'] <= resources['milk_ml'])

def check_what_missing(drink, resources):
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
    mapping = {'coffee':'coffee_g', 'water':'water_ml', 'milk':'milk_ml'}
    resources[mapping[resource]] = INIT_EKSPRESS_RESOURCES[mapping[resource]]
    print(f"{resource.capitalize()} refilled!")

def pay_for_drink(drink, express_coins):
    price_cents = drink['price_cents']

    print(f"\n💰 Please insert {format_money(price_cents)}")

    denominations_cents = sorted(
        [c for c, count in express_coins.items() if count > 0],
        reverse=True
    )
    
    if not denominations_cents:
        print("❌ Machine has no coins available. Cannot accept payment.")
        return False

    print("Accepted coins:", ", ".join([format_money(c) for c in denominations_cents]))

    inserted_cents = []
    total_cents = 0

    while total_cents < price_cents:
        print(f"Paid: {format_money(total_cents)} | Remaining: {format_money(price_cents - total_cents)}")
        try:
            coin = float(input("Insert coin (or 0 to cancel): "))
            coin_cents = int(round(coin * 100))

            if coin_cents == 0:
                print("Payment cancelled.")
                if inserted_cents:
                    print(f"💸 Refunding: {format_money(sum(inserted_cents))} -> {[c/100 for c in inserted_cents]}")
                return False

            if coin_cents not in denominations_cents:
                print("Invalid coin!")
                continue

            inserted_cents.append(coin_cents)
            total_cents += coin_cents

        except ValueError:
            print("Invalid input!")

    print(f"✅ Total paid: {format_money(total_cents)}")

    try:
        change_cents = calculate_change(price_cents, inserted_cents, express_coins)
        if change_cents:
            print(f"💸 Change returned: {format_money(sum(change_cents))} -> {[c/100 for c in change_cents]}")
        else:
            print("💸 No change needed.")
        return True
    except ValueError as e:
        print(e)
        print("💸 Refunding inserted coins.")
        return False

def calculate_change(price_cents, inserted_cents, express_coins):
    temp_coins = copy.deepcopy(express_coins)

    for c in inserted_cents:
        temp_coins[c] += 1

    change_cents = sum(inserted_cents) - price_cents
    change_list = []

    if change_cents == 0:
        return []

    denominations = sorted(temp_coins.keys(), reverse=True)

    for denom in denominations:
        while change_cents >= denom and temp_coins[denom] > 0:
            temp_coins[denom] -= 1
            change_cents -= denom
            change_list.append(denom)

    if change_cents != 0:
        raise ValueError("❌ Cannot return exact change!")

    express_coins.clear()
    express_coins.update(temp_coins)
    return change_list

def make_drink(drink, resources):
    resources['coffee_g'] -= drink['coffee_g']
    resources['water_ml'] -= drink['water_ml']
    resources['milk_ml'] -= drink['milk_ml']
    print(f"\n☕ Enjoy your {drink['name']}!\n")
    show_resources(resources)

def main():
    want_coffee = True
    while want_coffee:
        drink = select_drink(drinks)

        if can_make_drink(drink, express_resources):
            if pay_for_drink(drink, express_coins):
                make_drink(drink, express_resources)
        else:
            missing = check_what_missing(drink, express_resources)
            for r in missing:
                resp = ""
                while resp not in [YES, NO]:
                    resp = input(f"Do you want to refill {r}? ({YES}/{NO}): ").lower()
                if resp == YES:
                    refill_resource(r, express_resources)
                    show_resources(express_resources)

            if can_make_drink(drink, express_resources):
                if pay_for_drink(drink, express_coins):
                    make_drink(drink, express_resources)

        resp = ""
        while resp not in [YES, NO]:
            resp = input(f"Do you want another drink? ({YES}/{NO}): ").lower()
        want_coffee = resp == YES

    print("\n👋 Thank you! See you next time!")

# ---------------------- START ----------------------
main()

from coffee_machine_data import drinks, express_resources, express_coins, INIT_EKSPRESS_RESOURCES

YES = "yes"
NO = "no"

def select_drink(drinks_list):
    print("\n========== Available drinks ==========")
    for i, drink in enumerate(drinks_list, start=1):
        print(f"{i}. {drink['name']} - ${drink['price']:.2f}")
    print("=====================================")

    while True:
        try:
            drink_idx = int(input("Select a drink by number: "))
            if not 1 <= drink_idx <= len(drinks_list):
                raise ValueError
            drink = drinks_list[drink_idx - 1]
            print(f"You selected: {drink['name']} - ${drink['price']:.2f}")
            return drink
        except ValueError:
            print(f"Invalid input! Enter a number from 1 to {len(drinks_list)}")

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
        print(f"Not enough {r}!")
    return missing

def refill_resource(missing_resource, express_resources):
    express_resources[{'coffee':'coffee_g', 'water':'water_ml', 'milk':'milk_ml'}[missing_resource]] = INIT_EKSPRESS_RESOURCES[{'coffee':'coffee_g', 'water':'water_ml', 'milk':'milk_ml'}[missing_resource]]
    print(f"{missing_resource.capitalize()} refilled!")

def format_money(amount):
    return f"${amount:.2f}"

def coins_to_decimal(coins):
    decimal_coins = []
    for coin in coins.keys():
        if '$' in coin:
            decimal_coins.append(float(coin.replace("$","")))
        elif 'cent' in coin:
            decimal_coins.append(float(coin.replace("cent",""))/100)
    decimal_coins.sort(reverse=True)
    return decimal_coins

def pay_for_drink(drink, express_coins):
    accepted_coins = ', '.join([f"${c:.2f}" for c in coins_to_decimal(express_coins)])
    print(f"Please insert {format_money(drink['price'])} in coins. Accepted: {accepted_coins}")

    denominations = coins_to_decimal(express_coins)
    inserted_coins = []
    sum_inserted_coins = 0

    while sum_inserted_coins < drink['price']:
        print(f"Paid: {format_money(sum_inserted_coins)}, remaining: {format_money(drink['price'] - sum_inserted_coins)}")
        try:
            coin = float(input("Insert coin (or 0 to cancel): "))
            coin_cents = int(coin * 100)
            valid_cents = [int(d*100) for d in denominations]
            if coin == 0:
                print("Payment cancelled.")
                return False
            elif coin_cents not in valid_cents:
                print("Invalid coin. Try again.")
            else:
                inserted_coins.append(coin)
                sum_inserted_coins += coin
        except ValueError:
            print("Invalid input. Enter a number.")

    print(f"Total paid: {format_money(sum_inserted_coins)}")

    try:
        change = calculate_change(drink['price'], inserted_coins, express_coins)
        if change:
            print(f"Change returned: {format_money(sum(change))} -> {change}")
        else:
            print("No change.")
        return True
    except ValueError as e:
        print(e)
        return False

def calculate_change(price, inserted_coins, express_coins):
    price_cents = int(price*100)
    inserted_cents = [int(c*100) for c in inserted_coins]
    temp_coins = express_coins.copy()

    for c in inserted_cents:
        key = f"${c//100}" if c>=100 else f"{c}cent"
        temp_coins[key] += 1

    change = sum(inserted_cents) - price_cents
    change_list = []

    if change == 0:
        return []

    denominations = sorted([int(d*100) for d in coins_to_decimal(temp_coins)], reverse=True)

    for denom in denominations:
        while change >= denom:
            key = f"${denom//100}" if denom>=100 else f"{denom}cent"
            if temp_coins.get(key,0) == 0:
                break
            temp_coins[key] -= 1
            change -= denom
            change_list.append(denom/100)

    if change != 0:
        raise ValueError("Cannot return exact change!")
    express_coins.clear()
    express_coins.update(temp_coins)
    return change_list

def make_drink(drink, resources):
    resources['coffee_g'] -= drink['coffee_g']
    resources['water_ml'] -= drink['water_ml']
    resources['milk_ml'] -= drink['milk_ml']

def show_resources(resources):
    print("\n--- Machine resources ---")
    print(f"Coffee: {resources['coffee_g']}g, Water: {resources['water_ml']}ml, Milk: {resources['milk_ml']}ml")
    print("-------------------------\n")

def main():
    print("Welcome to the Premium Coffee Machine!")
    want_coffee = True

    while want_coffee:
        drink = select_drink(drinks)

        if can_make_drink(drink, express_resources):
            if pay_for_drink(drink, express_coins):
                make_drink(drink, express_resources)
                print(f"Enjoy your {drink['name']}!")
                show_resources(express_resources)
        else:
            missing = check_what_missing(drink, express_resources)
            for r in missing:
                response = ""
                while response not in [YES, NO]:
                    response = input(f"Do you want to refill {r}? Type {YES}/{NO}: ").lower()
                if response == YES:
                    refill_resource(r, express_resources)
                    show_resources(express_resources)

        response = ""
        while response not in [YES, NO]:
            response = input(f"Do you want another drink? Type {YES}/{NO}: ").lower()
        want_coffee = response == YES

    print("Thank you! See you next time!")
# start app
main()

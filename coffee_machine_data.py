INIT_EKSPRESS_RESOURCES = {
    'coffee_g': 500,
    'water_ml': 1000,
    'milk_ml': 500
}

drinks = [
    {
        "name": "Espresso",
        "coffee_g": 9,
        "water_ml": 30,
        "milk_ml": 0,
        "price": 2.5
    },
    {
        "name": "Double Espresso",
        "coffee_g": 18,
        "water_ml": 60,
        "milk_ml": 0,
        "price": 4
    },
    {
        "name": "Lungo",
        "coffee_g": 10,
        "water_ml": 100,
        "milk_ml": 0,
        "price": 4
    },
    {
        "name": "Americana",
        "coffee_g": 10,
        "water_ml": 100,
        "milk_ml": 0,
        "price": 5
    },
    {
        "name": "Cappuccino",
        "coffee_g": 9,
        "water_ml": 30,
        "milk_ml": 120,
        "price": 4
    },
    {
        "name": "Latte",
        "coffee_g": 9,
        "water_ml": 30,
        "milk_ml": 200,
        "price": 3.5
    },
    {
        "name": "Flat White",
        "coffee_g": 18,
        "water_ml": 60,
        "milk_ml": 120,
        "price": 4.5
    }
]

express_resources = {
    "water_ml": INIT_EKSPRESS_RESOURCES["water_ml"],
    "coffee_g": INIT_EKSPRESS_RESOURCES["coffee_g"],
    "milk_ml": INIT_EKSPRESS_RESOURCES["milk_ml"]
}

express_coins = {
    "$1": 20,
    "$5": 20,    
    "25cent": 20,
    "50cent": 20,    
    "10cent": 20
}


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
        "price_cents": 250
    },
    {
        "name": "Double Espresso",
        "coffee_g": 18,
        "water_ml": 60,
        "milk_ml": 0,
        "price_cents": 400
    },
    {
        "name": "Lungo",
        "coffee_g": 10,
        "water_ml": 100,
        "milk_ml": 0,
        "price_cents": 400
    },
    {
        "name": "Americana",
        "coffee_g": 10,
        "water_ml": 100,
        "milk_ml": 0,
        "price_cents": 500
    },
    {
        "name": "Cappuccino",
        "coffee_g": 9,
        "water_ml": 30,
        "milk_ml": 120,
        "price_cents": 400
    },
    {
        "name": "Latte",
        "coffee_g": 9,
        "water_ml": 30,
        "milk_ml": 200,
        "price_cents": 350
    },
    {
        "name": "Flat White",
        "coffee_g": 18,
        "water_ml": 60,
        "milk_ml": 120,
        "price_cents": 450
    }
]

express_resources = {
    "water_ml": INIT_EKSPRESS_RESOURCES["water_ml"],
    "coffee_g": INIT_EKSPRESS_RESOURCES["coffee_g"],
    "milk_ml": INIT_EKSPRESS_RESOURCES["milk_ml"]
}

express_coins = {
    100: 20,
    500: 20,    
    25: 20,
    50: 20,    
    10: 20
}


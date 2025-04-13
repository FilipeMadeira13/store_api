def product_data():
    return {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 7500, "status": True}


# Cria função com dados inválidos
def invalid_product_data():
    return {"name": 10, "quantity": "Zero", "price": "Oito Mil", "status": True}


def products_data():
    return [
        {"name": "Iphone 11 Pro Max", "quantity": 4, "price": 5800, "status": True},
        {"name": "Iphone 12 Pro Max", "quantity": 6, "price": 6000, "status": True},
        {"name": "Iphone 13 Pro Max", "quantity": 9, "price": 5500, "status": True},
        {"name": "Iphone 15 Pro Max", "quantity": 5, "price": 6500, "status": False},
    ]

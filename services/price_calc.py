PRICE_PER_PAGE = 0.20  # можно сделать динамическим позже

def calculate_price(page_count: int) -> float:
    return round(page_count * PRICE_PER_PAGE, 2)

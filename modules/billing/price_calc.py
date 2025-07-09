from config import PRICE_PER_PAGE

def calculate_price(page_count: int) -> float:
    return round(page_count * PRICE_PER_PAGE, 2)

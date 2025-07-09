import re

import re

def validate_page_range_str(input_str, max_pages=None, offset=0):
    input_str = input_str.replace(" ", "")
    if not input_str:
        raise ValueError("Пустой ввод")

    parts = input_str.split(',')
    for part in parts:
        if re.fullmatch(r"\d+", part):
            page = int(part) - offset
            if page < 1 or (max_pages and page > max_pages):
                raise ValueError(f"Неверный номер страницы: {part}")
        elif re.fullmatch(r"\d+-\d+", part):
            start, end = map(int, part.split('-'))
            start -= offset
            end -= offset
            if start > end:
                raise ValueError(f"Неверный диапазон: {part}")
            if max_pages and (start < 1 or end > max_pages):
                raise ValueError(f"Диапазон вне допустимого диапазона: {part}")
        else:
            raise ValueError(f"Неправильный формат: {part}")

    return input_str  # возвращаем строку, пригодную для lp
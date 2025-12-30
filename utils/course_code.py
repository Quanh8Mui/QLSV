def generate_course_code(start_year: int) -> str:
    """
    2025 -> K25
    2021 -> K21
    """
    year_suffix = str(start_year)[-2:]
    return f"K{year_suffix}"

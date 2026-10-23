import datetime as dt
import random
import re

COUNTRY_CODE = "+38"
WEEKEND_DAYS = (5, 6)
UPCOMING_DAYS = 7


def get_days_from_today(date: str) -> int | None:
    """Return the number of days from the given date to today.

    The result is negative if the date is in the future. Only calendar days
    are taken into account, time of day is ignored.

    Args:
        date: Date string in the 'YYYY-MM-DD' format.

    Returns:
        Whole number of days, or None if the date has an invalid format.
    """
    target_date = parse_date(date)
    if target_date is None:
        return None
    today = dt.date.today()
    return get_days_between_dates(today, target_date)


def get_days_between_dates(date_a: dt.date, date_b: dt.date) -> int:
    """Return the number of days from date_b to date_a (negative if date_b is later)."""
    return (date_a - date_b).days


def parse_date(date: str, separator: str = "-") -> dt.date | None:
    """Parse a 'YYYY<sep>MM<sep>DD' string into a date.

    Args:
        date: Date string to parse.
        separator: Separator between date parts, "-" by default.

    Returns:
        The parsed date, or None if the input is not a valid date string.
    """
    try:
        return dt.datetime.strptime(date, f"%Y{separator}%m{separator}%d").date()
    except (ValueError, TypeError):
        return None


def _is_int(value) -> bool:
    """Return True for real integers, excluding bool."""
    return isinstance(value, int) and not isinstance(value, bool)


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    """Generate a sorted list of unique random numbers for a lottery ticket.

    Args:
        min: Lowest possible number, at least 1.
        max: Highest possible number, at most 1000.
        quantity: How many numbers to pick, from 1 to the size of the range.

    Returns:
        Sorted list of unique numbers, or an empty list if the parameters
        are not integers or violate the constraints.
    """
    if not all(_is_int(value) for value in (min, max, quantity)):
        return []
    if not 1 <= min <= max <= 1000:
        return []
    if not 1 <= quantity <= max - min + 1:
        return []
    return sorted(random.sample(range(min, max + 1), quantity))


def normalize_phone(phone_number: str) -> str | None:
    """Normalize a phone number to the '+<digits>' format for SMS delivery.

    All characters except digits and a leading '+' are removed. A number that
    already has a '+' keeps its country code, one starting with '380' gets only
    the '+', any other number gets the default '+38' prefix.

    Args:
        phone_number: Phone number in an arbitrary format.

    Returns:
        Normalized number, or None if the input is not a string or has no digits.
    """
    if not isinstance(phone_number, str):
        return None
    digits = re.sub(r"\D", "", phone_number)
    if not digits:
        return None
    if re.match(r"\s*\+", phone_number):
        return f"+{digits}"
    if digits.startswith(COUNTRY_CODE.lstrip("+") + "0"):
        return f"+{digits}"
    return f"{COUNTRY_CODE}{digits}"


def _birthday_in_year(birth_date: dt.date, year: int) -> dt.date:
    """Return the birthday in the given year, moving Feb 29 to Mar 1 in non-leap years."""
    try:
        return birth_date.replace(year=year)
    except ValueError:
        return dt.date(year, 3, 1)


def get_upcoming_birthdays(users: list[dict]) -> list[dict]:
    """Return users whose birthday falls within the next 7 days, including today.

    A congratulation date that falls on a weekend is moved to the next Monday.
    Users with an invalid birthday are skipped.

    Args:
        users: List of dicts with `name` and `birthday` ('YYYY.MM.DD') keys.

    Returns:
        List of dicts with `name` and `congratulation_date` ('YYYY.MM.DD') keys.
    """
    today = dt.date.today()
    result = []
    for user in users:
        birth_date = parse_date(user.get("birthday"), separator=".")
        if birth_date is None:
            continue

        next_birthday = _birthday_in_year(birth_date, today.year)
        if next_birthday < today:
            # Already passed this year, so the next one is in the following year
            next_birthday = _birthday_in_year(birth_date, today.year + 1)

        if get_days_between_dates(next_birthday, today) >= UPCOMING_DAYS:
            continue

        congratulation_date = next_birthday
        if congratulation_date.weekday() in WEEKEND_DAYS:
            # Shift the congratulation to the next Monday
            congratulation_date += dt.timedelta(days=7 - congratulation_date.weekday())
        result.append({
            "name": user["name"],
            "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
        })
    return result


def start():
    date_str = '2026-10-09'
    days = get_days_from_today(date_str)
    print(f'days from {date_str} to today: {days}')
    print(f'invalid date: {get_days_from_today("09.10.2026")}')

    print(f'numbers: {get_numbers_ticket(1, 49, 6)}')
    print(f'min == max: {get_numbers_ticket(5, 5, 1)}')
    print(f'invalid range: {get_numbers_ticket(1, -2, 10)}')
    print(f'too many numbers: {get_numbers_ticket(10, 12, 5)}')

    raw_numbers = [
        "067\\t123 4567",
        "(095) 234-5678\\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
        "+49 151 2345 6789",
        "dsgdsgfdsg"
    ]
    sanitized_numbers = []
    for num in raw_numbers:
        sanitized_number = normalize_phone(num)
        if sanitized_number is not None:
            sanitized_numbers.append(sanitized_number)
    print("Phone numbers for SMS:", sanitized_numbers)

    today = dt.date.today()
    users = [
        {"name": "Today", "birthday": today.replace(year=1990).strftime("%Y.%m.%d")},
        {"name": "In 6 days", "birthday": (today + dt.timedelta(days=6)).replace(year=1985).strftime("%Y.%m.%d")},
        {"name": "In 7 days", "birthday": (today + dt.timedelta(days=7)).replace(year=1985).strftime("%Y.%m.%d")},
        {"name": "Yesterday", "birthday": (today - dt.timedelta(days=1)).replace(year=1992).strftime("%Y.%m.%d")},
        {"name": "Invalid", "birthday": "not a date"},
    ]
    print("Birthdays next 7 days:", get_upcoming_birthdays(users))


if __name__ == '__main__':
    start()

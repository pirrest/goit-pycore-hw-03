import datetime as dt
import random


# returns number of days from today
# if given date is in the future, returns negative number
# date should be in YYYY-MM-DD format
# returns None if date is not in the correct format
def get_days_from_today(date: str) -> int | None:
    target_date = parse_date(date)
    if target_date is None:
        return None
    today = dt.date.today()
    return get_days_between_dates(today, target_date)

# returns number of days from today
# if given date is in the future, returns negative number
def get_days_between_dates(date_a: dt.date, date_b: dt.date) -> int:
    return (date_a - date_b).days

# parses date in YYYY-MM-DD format
# separator in the format can be set via the parameter, by default "-"
def parse_date(date: str, separator="-") -> dt.date | None:
    try:
        return dt.datetime.strptime(date, f"%Y{separator}%m{separator}%d").date()
    except (ValueError, TypeError):
        return None

# returns list of random numbers from min to max
# quantity parameter specifies quantity of numbers
# max should be less than 1000
def get_numbers_ticket(min:int, max:int, quantity:int) -> list[int]:
    if not (0 < min < max < 1000 and max > 0) or not (min < quantity < max):
        return []
    all_numbers = [min + i for i in range(max)]
    selected_numbers = []
    while quantity > 0:
        quantity -= 1
        if len(all_numbers) == 0:
            break
        number = random.choice(all_numbers)
        all_numbers.remove(number)
        selected_numbers.append(number)
    return sorted(selected_numbers)

# formats phone_number to the country_code + digits
# if phone_number starts with country_code, it will be ignored
def normalize_phone(phone_number:str, country_code:str = '+380') -> str | None:
    assert isinstance(phone_number, str), "phone_number must be a string"
    assert isinstance(country_code, str), "country_code must be a string"
    phone_number = ''.join(filter(str.isdigit, phone_number))
    if len(phone_number) == 0:
        return None
    for char in country_code:
        if phone_number.startswith(char):
            phone_number = phone_number[1:]
    return f'{country_code}{phone_number}'

# returns list of users whose birthday is in the next 7 days
# each user should have `name` field and `birthday` field in format yyyy.mm.dd
# returns list of maps with `name` and `congratulation_date` fields in the same format
def get_upcoming_birthdays(users):
    result = []
    for user in users:
        user_birth_date = parse_date(user["birthday"], separator=".")
        today = dt.date.today()
        try:
            birthday_this_year = user_birth_date.replace(year=today.year)
        except ValueError:
            # Shifts Feb 29 to Mar 1 in non-leap years
            birthday_this_year = user_birth_date.replace(year=today.year, month=3, day=1)

        days_delta = get_days_between_dates(today, birthday_this_year)
        print(days_delta)
        if 0 >= days_delta >= -7:
            congratulation_date = birthday_this_year
            if birthday_this_year.weekday() in (5, 6):
                # Shift congratulation date to the next Monday if birthday falls on a weekend
                congratulation_date += dt.timedelta(days=(7 - birthday_this_year.weekday()))
            result.append({"name": user["name"], "congratulation_date": congratulation_date.strftime("%Y.%m.%d")})
    return result

def start():
    date_str = '2026-10-09'
    days = get_days_from_today(date_str)
    print(f'days from {date_str} to today: {days}')
    numbers = get_numbers_ticket(1, 100, 10)
    print(f'numbers: {numbers}')
    numbers2 = get_numbers_ticket(1, -2, 10)
    print(f'numbers2: {numbers2}')

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
        "dsgdsgfdsg"
    ]
    sanitized_numbers = []
    for num in raw_numbers:
        sanitized_number = normalize_phone(num)
        if sanitized_number is not None:
            sanitized_numbers.append(sanitized_number)
    print("Phone numbers for SMS:", sanitized_numbers)

    users = [
        {"name": "John Doe", "birthday": "1985.10.21"},
        {"name": "Jane Smith", "birthday": "1990.10.23"},
        {"name": "Jane Smith 2", "birthday": "1990.01.23"},
        {"name": "Jane Smith 3", "birthday": "1990.10.24"}
    ]
    upcoming_birthdays = get_upcoming_birthdays(users)
    print("Birthdays next 7 days:", upcoming_birthdays)

if __name__ == '__main__':
    start()

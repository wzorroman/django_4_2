import datetime
import calendar

DAY_WEEK = {
    0: "Monday",
    1: "Tuesday",
    2: "wednesday",
    3: "Thurday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}
DAY_WEEK_SPA = {
    0: "Lunes",
    1: "Martes",
    2: "Miercoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sabado",
    6: "Domingo"
}


def count_days_in_month(year: int, month: int) -> dict:
    # Validate if the year is a leap year (bisiesto)
    is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    # Get the number of days in the month
    num_days = calendar.monthrange(year, month)[1]

    # Count Saturdays and Sundays in the given month
    saturdays = 0
    sundays = 0

    for dia in range(1, num_days + 1):
        num_day_week = calendar.weekday(year, month, dia)
        if num_day_week == 5:  # SATURDAY
            saturdays += 1
        elif num_day_week == 6:  # SUNDAY
            sundays += 1

    data = {
        'total_days': num_days,
        'saturdays': saturdays,
        'sundays': sundays,
        'is_leap_year': is_leap_year
    }
    return data


def calculate_date_info(start_date: str, end_date: str):
    """
    Calculate the difference in days, number of complete months,
    and number of Saturdays and Sundays between two given dates.

    Args:
        start_date (str): Format 'YYYY-MM-DD'.
        end_date (str): Format 'YYYY-MM-DD'.

    Returns:
        dict:
              {
                  'total_days': int,
                  'full_months': int,
                  'saturdays': int,
                  'sundays': int,
                  'range_days': {
                    "date" : str,
                    "day_number": int,
                    "day_of_week": str
                    }
              }
              Retorna None si hay un error en el formato de las fechas.
    """

    try:
        start_day = datetime.datetime.strptime(f"{start_date} 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_day = datetime.datetime.strptime(f"{end_date} 23:59:59", '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print("\nError: Incorrect date format. Use YYYY-MM-DD.")
        return None

    if start_day > end_day:
        print("\nError: The start date must be before the end date.")
        return None

    # 1. Calculate the difference in days
    end_day += datetime.timedelta(seconds=1)
    day_difference = (end_day - start_day).days

    # 2. Calculate the number of complete months
    full_months = 0
    start_year = start_day.year
    start_month = start_day.month
    end_year = end_day.year
    end_month = end_day.month
    num_days = calendar.monthrange(start_year, start_month)[1]
    if day_difference >= num_days:
        full_months = ((end_year - start_year) * 12) + (end_month - start_month)

    # 3. Count Saturdays and Sundays
    range_days = {}
    saturdays = 0
    sundays = 0
    # print(f"\n *** {start_day} - {end_day} => Dif: ({day_difference})")
    for i in range(day_difference):
        current_day = start_day + datetime.timedelta(days=i)
        current_day_str = current_day.strftime("%d-%m-%Y")
        current_month_desc = current_day.strftime("%B")
        num_day_in_week = current_day.weekday()

        # icon_day = "*" if num_day_in_week in [5, 6] else ""
        # print(f" {i}: {current_day_str} || ({num_day_in_week}) {DAY_WEEK.get(num_day_in_week)} {icon_day}")
        if current_day.weekday() == 5:  # 5 saturday
            saturdays += 1
        elif current_day.weekday() == 6:  # 6 Sunday
            sundays += 1
        range_days[i] = {
            "date": current_day_str,
            "day_number": num_day_in_week,
            "day_of_week": DAY_WEEK.get(num_day_in_week),
            "day_of_week_spa": DAY_WEEK_SPA.get(num_day_in_week),
            "month_desc": current_month_desc
        }
    # print(f" full_months: {full_months} -- SA: {saturdays} | DO: {sundays} \n  ------||------")

    return {
        'total_days': day_difference,
        'full_months': full_months,
        'saturdays': saturdays,
        'sundays': sundays,
        'range_days': range_days
    }

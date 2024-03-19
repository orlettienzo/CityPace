import datetime

from decimal import Decimal
from enum import Enum

class MoonPhase(Enum):
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7

def age(date_target: datetime.date) -> Decimal:
    """Calculate the age of the moon at the given date."""
    # calculate days since 11 August 1999
    number_of_days = (date_target - datetime.date(1999, 8, 11)).days
    # reducing this modulo 29.53059 days
    phase_moon = number_of_days % 29.53059
    return phase_moon

def phase(age_temp: Decimal) -> MoonPhase:
    """Return the moon phase at the given age."""
    if 0 <= age_temp < 1.84566:
        return MoonPhase.NEW_MOON
    elif 1.84566 <= age_temp < 5.53699:
        return MoonPhase.WAXING_CRESCENT
    elif 5.53699 <= age_temp < 9.22831:
        return MoonPhase.FIRST_QUARTER
    elif 9.22831 <= age_temp < 12.91963:
        return MoonPhase.WAXING_GIBBOUS
    elif 12.91963 <= age_temp < 16.61096:
        return MoonPhase.FULL_MOON
    elif 16.61096 <= age_temp < 20.30228:
        return MoonPhase.WANING_GIBBOUS
    elif 20.30228 <= age_temp < 23.99361:
        return MoonPhase.LAST_QUARTER
    elif 23.99361 <= age_temp < 27.68493:
        return MoonPhase.WANING_CRESCENT
    else:
        return MoonPhase.NEW_MOON

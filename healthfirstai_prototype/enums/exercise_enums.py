"""Exercise enums

This file contains enums for exercise types, body parts, and equipment.

"""

from enum import Enum

import datetime


class DaysOfTheWeek(str, Enum):
    """
    Enum for days of the week
    """

    today = datetime.datetime.now().strftime("%A")
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"

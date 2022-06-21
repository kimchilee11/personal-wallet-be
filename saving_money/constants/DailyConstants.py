from enum import Enum


class DailyStatus(Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)




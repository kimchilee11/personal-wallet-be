from enum import Enum


class TransStatus(Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class ValueCurrency(Enum):
    VND = "VND"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)



from datetime import datetime
from stockobjectsexceptions import QuoteAlreadyExists

# class QuoteCodeAlreadySet(Exception):
#    def __init__(self, new_code):
#        super().__init__(
#            self,
#            f"Unable to set code to {new_code}: Quote object already has a code set",
#        )


class BaseQuote:
    _date: datetime
    _open: float
    _high: float
    _low: float
    _close: float
    _volume: int

    def __init__(
        self,
        parent,
        date: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
    ):
        self._parent = parent,
        self._date = date
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume


    @property
    def name(self) -> str:
        return self._parent.name

    @property
    def code(self) -> str:
        return self._parent.code

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def open(self) -> float:
        return self._open

    @property
    def high(self) -> float:
        return self._high

    @property
    def low(self) -> float:
        return self._low

    @property
    def close(self) -> float:
        return self._close

    @property
    def volume(self) -> int:
        return self._volume
from stockobjects.basequote import BaseQuote
from datetime import datetime


class CompanyQuote(BaseQuote):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    # company_name:str
    # company_code:str
    # name:str
    # code:str

    def __init__(
        self,
        company_object,
        date: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
    ):
        self._parent = company_object
        super().__init__(
            parent=company_object,
            date=date,
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume,
        )

    def get_quote(self):
        return {
            "company_name": self._parent.name,
            "company_code": self._parent.code,
            "date": self._date,
            "open": self._open,
            "high": self._high,
            "low": self._low,
            "close": self._close,
            "volume": self._volume,
        }

    @property
    def company_name(self) -> str:
        print(self._parent.name)
        return self._parent.name

    @property
    def company_code(self) -> str:
        return self._parent.code

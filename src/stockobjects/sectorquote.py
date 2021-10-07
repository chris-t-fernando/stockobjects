from stockobjects.basequote import BaseQuote
from datetime import datetime


class SectorQuote(BaseQuote):
    def __init__(
        self,
        sector_object,
        date: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
    ):
        super().__init__(
            parent=sector_object,
            date=date,
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume,
        )

    def get_quote(self):
        return {
            "sector_name": self._parent.name,
            "sector_code": self._parent.code,
            "date": self._date,
            "open": self._open,
            "high": self._high,
            "low": self._low,
            "close": self._close,
            "volume": self._volume,
        }

    @property
    def sector_name(self) -> str:
        return self._parent.name

    @property
    def sector_code(self) -> str:
        return self._parent.code

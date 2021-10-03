from basequote import BaseQuote
from stockobjectsexceptions import QuoteAlreadyExists


class QuoteCollection:
    _quotes: dict
    _name: str
    _code: str

    def __init__(self, parent):
        self._parent = parent
        self._name = parent.name
        self._code = parent.code

    @property
    def code(self) -> str:
        return self._code

    @property
    def sector(self) -> str:
        return self._sector

    def add_quote(self, new_quote: BaseQuote) -> bool:
        if new_quote.date in self.quotes:
            raise QuoteAlreadyExists(code=self._code, date=new_quote)

        self._quotes[new_quote.date] = new_quote
        return True

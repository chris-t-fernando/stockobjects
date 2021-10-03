from datetime import datetime
from companyquote import CompanyQuote
from stockobjectsexceptions import QuoteAlreadyExists
from typing import Dict
from parsing import DateParser


class Company:
    _company_name: str
    _company_code: str
    _quotes: Dict[datetime, CompanyQuote]

    def __init__(self, company_name, company_code, sector_object):
        self._company_name = company_name
        self._company_code = company_code
        self._sector_object = sector_object
        self._quotes = {}

    @property
    def company_code(self) -> str:
        return self._company_code

    @property
    def company_name(self) -> str:
        return self._company_name

    @property
    def code(self) -> str:
        return self._company_code

    @property
    def name(self) -> str:
        return self._company_name

    @property
    def length(self):
        return len(self._quotes)

    def add_quote(
        self,
        date: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
    ) -> bool:
        # self._quotes[date] = CompanyQuote
        # try to turn the incoming parameters into a CompanyQuote
        try:
            new_quote = CompanyQuote(
                self,
                date=date,
                open=open,
                high=high,
                low=low,
                close=close,
                volume=volume,
            )
        except Exception as e:
            raise

        # and then use the add_quote_object method to add it - avoids duplicating code
        # try except will catch if there's already a duplicate quote
        try:
            add_quote_result = self.add_quote_object(new_quote)
        except Exception as e:
            raise

        return add_quote_result

    def add_quote_object(self, new_quote: CompanyQuote) -> bool:
        if new_quote.date in self._quotes:
            raise QuoteAlreadyExists(code=self._company_code, date=new_quote)

        self._quotes[new_quote.date] = new_quote
        return True

    def get_company_quote_length(self):
        return self.length

    def get_quote(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
    ) -> Dict[datetime, CompanyQuote]:
        try:
            dates = DateParser(date_from=date_from, date_to=date_to, date=date)
        except Exception as e:
            raise

        print(f"Going to do some stuff with {dates.date_from} and {dates.date_to}")

        matched_quotes = {}

        for quote_date in self._quotes:
            if dates.date_from <= quote_date and dates.date_to >= quote_date:
                matched_quotes[quote_date] = self._quotes[quote_date]

        # not checking for zero returns since zero is a valid response, doesn't mean exception/error
        return matched_quotes
        

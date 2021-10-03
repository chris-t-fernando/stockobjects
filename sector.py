from datetime import datetime

# from quotecollection import QuoteCollection
from stockobjectsexceptions import CompanyAlreadyExists, QuoteAlreadyExists
from sectorquote import SectorQuote
from company import Company
from typing import Dict


class Sector:
    _sector_name: str
    _sector_code: str
    # _quotes: QuoteCollection
    _quotes: Dict[datetime, SectorQuote]
    _companies: Dict[str, Company]

    def __init__(self, sector_name: str, sector_code: str):
        self._sector_name = sector_name
        self._sector_code = sector_code
        self._quotes = {}
        self._companies = {}

    @property
    def sector_code(self) -> str:
        return self._sector_code

    @property
    def sector_name(self) -> str:
        return self._sector_name

    @property
    def code(self) -> str:
        return self._sector_code

    @property
    def name(self) -> str:
        return self._sector_name

    def add_company(self, new_company: Company):
        if new_company in self._companies.keys():
            raise CompanyAlreadyExists(company_code=new_company.company_code)

        self._companies[new_company.company_code] = new_company
        return True

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
            new_quote = SectorQuote(
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

    def add_quote_object(self, new_quote: SectorQuote) -> bool:
        if new_quote.date in self._quotes:
            raise QuoteAlreadyExists(code=self._sector_code, date=new_quote)

        self._quotes[new_quote.date] = new_quote
        return True

    def get_company_by_code(self, company_code: str) -> Company:
        # iterate through sectors, looking for the company
        if company_code in self._companies:
            return self._companies[company_code]

        # didn't find it.  Not really an exception
        return False

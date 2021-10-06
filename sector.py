from datetime import datetime

# from quotecollection import QuoteCollection
from stockobjectsexceptions import (
    CompanyAlreadyExists,
    QuoteAlreadyExists,
    CompanyDoesNotExist,
)
from sectorquote import SectorQuote
from companyquote import CompanyQuote
from company import Company
from typing import Dict
from parsing import DateParser

# DONE
# Sector(sector_name Str, sector_code Str)
# Sector->add_sector_quote(all the things) -> bool
# Sector->add_sector_quote_object(quote SectorQuote) -> bool
# Sector->add_company(company Company) -> bool
# Sector->get_company(company_code Str) -> Company
# Sector->get_sector_quote(date datetime=None) -> QuoteCollection
# Sector->get_company_quote(company_code Str=None) -> QuoteCollection
# Sector->sector_quote_length() -> int
# Sector->add_company_quote(all the things) -> bool
# Sector->add_company_quote_object(quote CompanyQuote) -> bool
# Sector->company_length() -> int
# Sector->company_quote_length() -> int


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

    def add_sector_quote(
        self,
        date: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
    ) -> bool:
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
            add_quote_result = self.add_sector_quote_object(new_quote)
        except Exception as e:
            raise

        return add_quote_result

    def add_sector_quote_object(self, new_quote: SectorQuote) -> bool:
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

    def get_sector_quote(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
    ) -> Dict[datetime, SectorQuote]:
        return self._get_quote(
            date_from=date_from, date_to=date_to, date=date, company_code=None
        )

    def get_company_quote(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
        company_code: str = None,
    ) -> Dict[datetime, CompanyQuote]:
        # there will be multiple companies in the sector, so need to loop through them all
        results = {}
        for company in self._companies:
            results[company] = self._get_quote(
                date_from=date_from,
                date_to=date_to,
                date=date,
                company_code=company_code,
            )

        # i wonder - if there are no quotes for the company, should I even return it?
        return results

    def _get_quote(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
        company_code: str = None,
    ):
        try:
            dates = DateParser(date_from=date_from, date_to=date_to, date=date)
        except Exception as e:
            raise

        if company_code != None and company_code not in self._companies:
            raise CompanyDoesNotExist(company_code=company_code)

        matched_quotes = {}

        for quote_date in self._quotes:
            company_match = False
            date_match = False
            if (
                dates.date_from <= quote_date.date()
                and dates.date_to >= quote_date.date()
            ):
                date_match = True

            if company_code != None:
                # this is super shonky - could be company_code that is the same as sector_code
                if self._quotes[quote_date].code == company_code:
                    company_match = True
            else:
                company_match = True

            if company_match and date_match:
                matched_quotes[quote_date] = self._quotes[quote_date]

        # not checking for zero returns since zero is a valid response, doesn't mean exception/error
        return matched_quotes

    def add_company_quote(
        self,
        company_object: Company,
        date: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
    ) -> bool:
        # look up whether we have this company
        if company_object.company_code not in self._companies.keys():
            raise CompanyDoesNotExist(company_code=company_object.company_code)

        # don't need to worry about checking if its a duplicate quote - that's the responsibility of Company
        # then add it
        self._companies[company_object.company_code].add_quote(
            date=date, open=open, high=high, low=low, close=close, volume=volume
        )

        # either raise an Exception or return True
        return True

    def add_company_quote_object(
        self, company_object: Company, new_quote: CompanyQuote
    ) -> bool:
        # look up whether we have this company
        if company_object.company_code not in self._companies.keys():
            raise CompanyDoesNotExist(company_code=company_object.company_code)

        # don't need to worry about checking if its a duplicate quote - that's the responsibility of Company
        # then add it
        self._companies[company_object.company_code].add_quote_object(
            new_quote=new_quote
        )

        # either raise an Exception or return True
        return True

    @property
    def sector_quote_length(self) -> int:
        return len(self._quotes)

    @property
    def company_length(self) -> int:
        return len(self._companies)

    @property
    def company_quote_length(self) -> int:
        collected_quotes = 0
        # loop through companies to get quote length
        for company in self._companies:
            collected_quotes += len(self._companies[company]._quotes)

        return collected_quotes

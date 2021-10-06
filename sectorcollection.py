from sector import Sector
from company import Company
from sectorquote import SectorQuote
from companyquote import CompanyQuote
from stockobjectsexceptions import (
    SectorAlreadyExists,
    SectorDoesNotExist,
    CompanyDoesNotExist,
)
from company import Company
from typing import Dict, List
from datetime import datetime
from parsing import DateParser


class SectorCollection:
    # dict with sector_code as key, Sector object as value
    # _companies: Dict[str, Company]
    _sectors: Dict[str, Sector]
    _quotes: Dict[datetime, SectorQuote]
    _name: str

    def __init__(self, name: str):
        self._name = name
        self._sectors = {}
        self._quotes = {}

    def add_sector(self, new_sector: Sector) -> bool:
        if new_sector.sector_code in self._sectors:
            raise SectorAlreadyExists(new_sector.sector_code)

        self._sectors[new_sector.sector_code] = new_sector
        return True

    def get_sector_by_code(self, sector_code: str) -> Sector:
        if sector_code not in self._sectors:
            raise SectorDoesNotExist(sector_code)

        return self._sectors[sector_code]

    def get_company_by_code(self, company_code: str) -> Company:
        # iterate through sectors, looking for the company
        for this_sector in self._sectors:
            if company_code in self._sectors[this_sector]._companies:
                return self._sectors[this_sector]._companies[company_code]

        # didn't find it. not really an exception though
        return False

    @property
    def length(self) -> int:
        return len(self._sectors)

    @property
    def name(self) -> str:
        return self._name

    def get_sector_quote(
        self,
        search_sectors: List[str] = None,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
    ) -> Dict[datetime, SectorQuote]:
        try:
            dates = DateParser(date_from=date_from, date_to=date_to, date=date)
        except Exception as e:
            raise

        matched_quotes = {}
        for sector in self._sectors:
            # if I want all sectors
            if search_sectors == None:
                matched_quotes[sector] = self._sectors[sector].get_sector_quote(
                    date_from=date_from, date_to=date_to, date=date
                )

            # if I only want the sectors in the search_sectors List
            elif sector in search_sectors:
                matched_quotes[sector] = self._sectors[sector].get_sector_quote(
                    date_from=date_from, date_to=date_to, date=date
                )

        # not checking for zero returns since zero is a valid response, doesn't mean exception/error
        return matched_quotes

    def get_company_quote(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
        company_code: List[str] = None,
    ) -> Dict[datetime, CompanyQuote]:

        try:
            dates = DateParser(date_from=date_from, date_to=date_to, date=date)
        except Exception as e:
            raise

        matched_quotes = {}
        for sector in self._sectors:
            sector_query = self._sectors[sector].get_company_quote(
                date_from=date_from,
                date_to=date_to,
                date=date,
                company_code=company_code,
            )

            ### THIS IS ALL BUSTED KIND OF
            # need to update the Sector->get_company_quote so that it takes a List of companies we care about
            # then this method will need to loop through Sector._companies to get a subset of company_codes that belongs to that sector
            # then we can query that sector for those company codes
            # then we can combine it all together here
            for company in sector_query:
                matched_quotes[company] = sector_query[company]

        return matched_quotes

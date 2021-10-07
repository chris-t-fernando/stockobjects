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
        if not isinstance(new_sector, Sector):
            raise TypeError("new_sector must be of type Sector")

        if new_sector.sector_code in self._sectors:
            raise SectorAlreadyExists(new_sector.sector_code)

        self._sectors[new_sector.sector_code] = new_sector
        return True

    def get_sector(self, sector_code: str) -> Sector:
        if not isinstance(sector_code, str):
            raise TypeError("sector_code must be of type string")

        if sector_code not in self._sectors:
            raise SectorDoesNotExist(sector_code)

        return self._sectors[sector_code]

    def get_company(self, company_code: str) -> Company:
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
        sector_codes: List[str] = None,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
    ) -> Dict[datetime, SectorQuote]:
        try:
            dates = DateParser(date_from=date_from, date_to=date_to, date=date)
        except Exception as e:
            raise

        # if a sector is specified, make sure it exists
        if sector_codes != None:
            for sector in sector_codes:
                if sector not in self._sectors:
                    raise SectorDoesNotExist(sector)

        matched_quotes = {}
        for sector in self._sectors:
            # if I want all sectors
            if sector_codes == None:
                matched_quotes[sector] = self._sectors[sector].get_sector_quote(
                    date_from=date_from, date_to=date_to, date=date
                )

            # if I only want the sectors in the sector_codes List
            elif sector in sector_codes:
                matched_quotes[sector] = self._sectors[sector].get_sector_quote(
                    date_from=date_from, date_to=date_to, date=date
                )

        # not checking for zero returns since zero is a valid response, doesn't mean exception/error
        return matched_quotes

    def get_company_quote(
        self,
        company_codes: List[str] = None,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
    ) -> Dict[datetime, CompanyQuote]:

        try:
            dates = DateParser(date_from=date_from, date_to=date_to, date=date)
        except Exception as e:
            raise

        # validate that the company codes is a list
        # todo: be clever and allow a string?
        if company_codes != None:
            if not isinstance(company_codes, list):
                raise TypeError(
                    f"company_codes must be either None or List[str], instead of {type(company_codes)}"
                )

        matched_quotes = {}
        found_company_codes = []

        # loop through all sectors
        for sector in self._sectors:
            # either get all companies
            if company_codes == None:
                this_sector_company_quotes = None
            # or just the companies that belong to this specific sector
            else:
                this_sector_company_quotes = list(
                    set(self._sectors[sector]._companies) & set(company_codes)
                )

            # get the companies we care about
            this_sector_matches = self._sectors[sector].get_company_quote(
                company_codes=this_sector_company_quotes,
                date_from=date_from,
                date_to=date_to,
                date=date,
            )

            # merge the existing matches with the new matches
            matched_quotes = {**matched_quotes, **this_sector_matches}

            # keep record of the company codes we found
            found_company_codes = found_company_codes + list(this_sector_matches.keys())

        # before returning matched_quotes, we need to see if we weren't able to find any company codes
        if company_codes != None:
            # diff the codes we were asked to search for vs the ones we actually found
            invalid_company_codes = list(set(company_codes) - set(found_company_codes))

            # if there are any invalid quotes
            if len(invalid_company_codes) > 0:
                # raise an exception
                raise CompanyDoesNotExist(invalid_company_codes)

        # otherwise return what we found
        return matched_quotes

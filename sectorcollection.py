from sector import Sector

# from companycollection import CompanyCollection
# from quotecollection import QuoteCollection
from sectorquote import SectorQuote
from stockobjectsexceptions import SectorAlreadyExists, SectorDoesNotExist
from company import Company
from typing import Dict
from datetime import datetime


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

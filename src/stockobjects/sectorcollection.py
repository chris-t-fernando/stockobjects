from typing import Dict, List
from datetime import datetime

from stockobjects.sector import Sector
from stockobjects.company import Company
from stockobjects.sectorquote import SectorQuote
from stockobjects.companyquote import CompanyQuote
from stockobjects.stockobjectsexceptions import (
    SectorAlreadyExists,
    SectorDoesNotExist,
    CompanyDoesNotExist,
)
from stockobjects.company import Company
from stockobjects.parsing import DateParser
import json


class SectorCollection:
    # dict with sector_code as key, Sector object as value
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

        raise CompanyDoesNotExist(company_code=company_code)

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

    def _validate_sqs(self, payload: dict) -> bool:
        if not "Records" in payload.keys():
            raise Exception("No Records key in event.  Failing")

        # for each recrord
        for record in payload["Records"]:
            try:
                # does this key exist?
                messageType = record["messageAttributes"]["QuoteType"]["stringValue"]
            except Exception as e:
                raise Exception("Unable to find quoteType in message.  Failing")

            # and if it does, is it a valid value?
            if messageType != "stock" and messageType != "sector":
                raise Exception(
                    f"quoteType is invalid.  Expected either 'sector' or 'stock', instead found {messageType}.  Failing"
                )

            # is it valid json?
            try:
                listOfQuotes = json.loads(record["body"])
            except:
                raise

            # and if it is, is there a key for quoteObject?
            if not "quoteObject" in listOfQuotes.keys():
                raise Exception("Unable to find quoteObject in payload")

            # and are there any quotes?
            if not isinstance(listOfQuotes["quoteObject"], list):
                raise Exception("No quotes in quoteObject")

            if len(listOfQuotes["quoteObject"]) == 0:
                raise Exception("No quotes in quoteObject")

        # got here without raising an Exception so the input is good
        return True

    def load_sqs(self, payload: str) -> bool:
        # validate the payload per my custom formatting
        try:
            self._validate_sqs(payload=payload)
        except:
            raise

        # todo hacky
        boilerplate_sector = Sector("Boilerplate", "Boilerplate")
        self.add_sector(new_sector=boilerplate_sector)

        # okay so its valid. now you need to loop through
        for record in payload["Records"]:
            # hold on to the message type
            messageType = record["messageAttributes"]["QuoteType"]["stringValue"]

            # read the embedded json in the body key
            this_quote_collection = json.loads(record["body"])

            if messageType == "sector":
                # there can be more than one quote object per record
                for this_quote in this_quote_collection["quoteObject"]:
                    # do we already have this sector?
                    try:
                        this_sector = self.get_sector(sector_code=this_quote["sector_code"])
                    except:
                        # new sector, so instantiate it as an object and add it to the collection
                        this_sector = Sector(
                            "boilerplate sector name", this_quote["sector_code"]
                        )
                        self.add_sector(new_sector=this_sector)

                    # create a quote object
                    try:
                        date = this_quote["quote_date"]
                        open = this_quote["open"]
                        high = this_quote["high"]
                        low = this_quote["low"]
                        close = this_quote["close"]
                        volume = this_quote["volume"]

                        new_quote = SectorQuote(
                            sector_object=this_sector,
                            date=date,
                            open=open,
                            high=high,
                            low=low,
                            close=close,
                            volume=volume,
                        )
                    except:
                        # new sector quote is bad - barf? log? not sure what I want to do with this. json.loads barfs so I guess I should too?
                        raise

                    try:
                        self.get_sector(
                            sector_code=this_quote["sector_code"]
                        ).add_sector_quote_object(new_quote=new_quote)
                    except:
                        # barfed because there was already a quote for this date?  bad types?
                        raise

            # company - stock is an old name I used at the beginning of this whole palava
            elif messageType == "stock":
                # there can be more than one quote object per record
                for this_quote in this_quote_collection["quoteObject"]:
                    # do we already have this company?
                    try:
                        this_company = self.get_company(
                            company_code=this_quote["stock_code"]
                        )
                    except CompanyDoesNotExist:
                        # new sector, so instantiate it as an object and add it to the collection
                        this_company = Company(
                            company_name="boilerplate company name",
                            company_code=this_quote["stock_code"],
                        )

                        # hacky - company quotes don't specify the sector they belong to, so orphan them
                        self.get_sector(
                            sector_code=boilerplate_sector.sector_code
                        ).add_company(new_company=this_company)
                    except:
                        raise

                    # create a quote object
                    try:
                        date = this_quote["quote_date"]
                        open = this_quote["open"]
                        high = this_quote["high"]
                        low = this_quote["low"]
                        close = this_quote["close"]
                        volume = this_quote["volume"]

                        new_quote = CompanyQuote(
                            company_object=this_company,
                            date=date,
                            open=open,
                            high=high,
                            low=low,
                            close=close,
                            volume=volume,
                        )

                    except:
                        # new sector quote is bad - barf? log? not sure what I want to do with this. json.loads barfs so I guess I should too?
                        raise

                    try:
                        self.get_company(
                            company_code=this_quote["stock_code"]
                        ).add_quote_object(new_quote=new_quote)
                    except:
                        # barfed because there was already a quote for this date?  bad types?
                        raise
                    
        # if we got here, it was successful
        return True

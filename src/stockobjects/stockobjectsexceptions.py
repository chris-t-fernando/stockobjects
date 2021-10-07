from datetime import datetime


class QuoteAlreadyExists(Exception):
    def __init__(self, code: str, date: datetime):
        super().__init__(
            self,
            f"Code {code} already has a quote for {date}",
        )


class SectorAlreadyExists(Exception):
    def __init__(self, sector_code: str):
        super().__init__(
            self,
            f"SectorCollection already has a quote for {sector_code}",
        )


class CompanyAlreadyExists(Exception):
    def __init__(self, company_code: str):
        super().__init__(
            self,
            f"Sector already has a company object for {company_code}",
        )


class CompanyDoesNotExist(Exception):
    def __init__(self, company_code: str):
        super().__init__(
            self,
            f"Sector does not have a Company with the code {company_code}",
        )


class SectorDoesNotExist(Exception):
    def __init__(self, sector_code: str):
        super().__init__(
            self,
            f"SectorCollection does not have a Sector with the code {sector_code}",
        )


class InvalidDateOptions(Exception):
    def __init__(self):
        super().__init__(
            self,
            f"Invalid combination of parameters.  Either set date_from and/or date_to, OR set date",
        )

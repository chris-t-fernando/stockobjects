import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from stockobjectsexceptions import QuoteAlreadyExists
from company import Company
from sector import Sector
from companyquote import CompanyQuote
from sectorquote import SectorQuote
from sectorcollection import SectorCollection

# company, SectorQuote, companyQuote
from datetime import datetime
import string
import random

# todo: for when I'm randomly generating entire structures.  If I was clever I'd probably use a test fixture
CONST_TEST_SECTOR_COUNT = 2
CONST_TEST_COMPANY_COUNT = 3
CONST_TEST_SECTOR_QUOTES = 5
CONST_TEST_COMPANY_QUOTES = 5
CONST_QUOTES_START_DAY = 1

# for when I'm unit testing individual sectors/companies/quotes
CONST_SECTOR1_NAME = "Cutlery"
CONST_SECTOR1_CODE = "xcj"

CONST_COMPANY1_COMPANY_NAME = "Knives Inc"
CONST_COMPANY1_COMPANY_CODE = "kni"

CONST_COMPANY2_COMPANY_NAME = "Spoons r us"
CONST_COMPANY2_COMPANY_CODE = "spo"

CONST_QUOTE1_DATE = datetime.strptime("18/09/19 01:55:19", "%d/%m/%y %H:%M:%S")

CONST_QUOTE2_DATE = datetime.strptime("18/09/19 01:55:19", "%d/%m/%y %H:%M:%S")

CONST_QUOTE3_DATE = datetime.strptime("19/10/20 01:55:19", "%d/%m/%y %H:%M:%S")


def generate_sector():
    name = "sectorname-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
    code = "sectorcode-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=3)
    )
    return Sector(sector_name=name, sector_code=code)


def generate_company(sector):
    name = "companyname-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
    code = "companycode-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=3)
    )

    return Company(company_name=name, company_code=code, sector_object=sector)


def generate_sector_collection(
    sector_count, company_count, sector_quotes, company_quotes
):
    this_collection = SectorCollection(
        name="collectionname-".join(
            random.choices(string.ascii_uppercase + string.digits, k=4)
        )
    )

    sectors_generated = 0
    while sectors_generated < sector_count:
        generated_sector = generate_sector()
        this_collection.add_sector(generated_sector)

        sector_quotes_generated = 0
        day = CONST_QUOTES_START_DAY
        while sector_quotes_generated < sector_quotes:
            this_collection.get_sector_by_code(generated_sector.sector_code).add_quote(
                date=datetime.strptime(f"{day}/10/20 01:55:19", "%d/%m/%y %H:%M:%S"),
                open=2,
                high=2,
                low=2,
                close=2,
                volume=2000,
            )
            day += 1
            sector_quotes_generated += 1

        # generate companies in this sector
        companies_generated = 0
        day = CONST_QUOTES_START_DAY
        while companies_generated < company_count:
            generated_company = generate_company(generated_sector)

            this_collection.get_sector_by_code(
                generated_sector.sector_code
            ).add_company(generated_company)

            # generate quotes for  this company
            company_quotes_generated = 0
            while company_quotes_generated < company_quotes:
                this_collection.get_company_by_code(
                    generated_company.company_code
                ).add_quote(
                    date=datetime.strptime(
                        f"{day}/10/20 01:55:19", "%d/%m/%y %H:%M:%S"
                    ),
                    open=1,
                    high=1,
                    low=1,
                    close=1,
                    volume=1000,
                )
                day += 1
                company_quotes_generated += 1

            companies_generated += 1

        sectors_generated += 1

    return this_collection


class TestSector(unittest.TestCase):
    def test_sector_name(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        result = test_sector.sector_name
        self.assertEqual(CONST_SECTOR1_NAME, result)

    def test_sector_code(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        result = test_sector.sector_code
        self.assertEqual(CONST_SECTOR1_CODE, result)


class TestCompany(unittest.TestCase):
    def test_attr_name(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )

        test_company = Company(
            company_name=CONST_COMPANY1_COMPANY_NAME,
            company_code=CONST_COMPANY1_COMPANY_NAME,
            sector_object=test_sector,
        )

        result = test_company.name
        self.assertEqual(CONST_COMPANY1_COMPANY_NAME, result)

    def test_attr_company_code(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )

        test_company = Company(
            company_name=CONST_COMPANY1_COMPANY_NAME,
            company_code=CONST_COMPANY1_COMPANY_NAME,
            sector_object=test_sector,
        )

        result = test_company.code
        self.assertEqual(CONST_COMPANY1_COMPANY_NAME, result)

    # todo: patch sector so that this is a unit test instead of integration test
    def test_attr_company_name(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )

        test_company = Company(
            company_name=CONST_COMPANY1_COMPANY_NAME,
            company_code=CONST_COMPANY1_COMPANY_NAME,
            sector_object=test_sector,
        )

        result = test_company.company_name
        self.assertEqual(CONST_COMPANY1_COMPANY_NAME, result)

    def test_attr_company_code(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        test_company = Company(
            company_name=CONST_COMPANY1_COMPANY_NAME,
            company_code=CONST_COMPANY1_COMPANY_NAME,
            sector_object=test_sector,
        )
        result = test_company.company_code
        self.assertEqual(CONST_COMPANY1_COMPANY_NAME, result)

    def test_add_quote_object(self):
        test_company = generate_company(sector=generate_sector())
        test_quote_object = CompanyQuote(
            company_object=test_company,
            date=CONST_QUOTE2_DATE,
            open=10,
            high=12,
            low=8,
            close=11,
            volume=2000,
        )
        test_company.add_quote_object(test_quote_object)

        self.assertEquals(test_company._quotes[CONST_QUOTE2_DATE], test_quote_object)

    def test_add_quote(self):
        different_test_company = generate_company(sector=generate_sector())
        different_test_company.add_quote(
            date=CONST_QUOTE1_DATE,
            open=10,
            high=12,
            low=8,
            close=11,
            volume=2000,
        )

        self.assertEquals(
            different_test_company._quotes[CONST_QUOTE1_DATE].date, CONST_QUOTE1_DATE
        )
        self.assertEquals(different_test_company._quotes[CONST_QUOTE1_DATE].open, 10)
        self.assertEquals(different_test_company._quotes[CONST_QUOTE1_DATE].high, 12)
        self.assertEquals(different_test_company._quotes[CONST_QUOTE1_DATE].low, 8)
        self.assertEquals(different_test_company._quotes[CONST_QUOTE1_DATE].close, 11)
        self.assertEquals(
            different_test_company._quotes[CONST_QUOTE1_DATE].volume, 2000
        )

    def test_get_company_quote_length(self):
        test_company = generate_company(sector=generate_sector())

        quotes_added = 0
        quotes_to_add = 5

        start_length = test_company.get_company_quote_length()
        today = datetime.now()

        while quotes_added < quotes_to_add:
            days_ago = timedelta(days=quotes_added)
            this_quote_date = today - days_ago
            test_quote_object = CompanyQuote(
                company_object=test_company,
                date=this_quote_date,
                open=10,
                high=12,
                low=8,
                close=11,
                volume=2000,
            )
            test_company.add_quote_object(test_quote_object)
            quotes_added += 1

        end_length = test_company.get_company_quote_length()

        self.assertEquals(start_length, 0)
        self.assertEquals(end_length, 5)

    def test_attr_length(self):
        test_company = generate_company(sector=generate_sector())

        quotes_added = 0
        quotes_to_add = 5

        start_length = test_company.length

        start_length = test_company.get_company_quote_length()
        today = datetime.now()

        while quotes_added < quotes_to_add:
            days_ago = timedelta(days=quotes_added)
            this_quote_date = today - days_ago
            test_quote_object = CompanyQuote(
                company_object=test_company,
                date=this_quote_date,
                open=10,
                high=12,
                low=8,
                close=11,
                volume=2000,
            )
            test_company.add_quote_object(test_quote_object)
            quotes_added += 1

        end_length = test_company.length

        self.assertEquals(start_length, 0)
        self.assertEquals(end_length, 5)

    def test_get_quote_no_filter(self):
        test_collection = generate_sector_collection(
            sector_count=CONST_TEST_SECTOR_COUNT,
            company_count=CONST_TEST_COMPANY_COUNT,
            sector_quotes=CONST_TEST_SECTOR_QUOTES,
            company_quotes=CONST_TEST_COMPANY_QUOTES,
        )

        # todo make this much better - test fixture or something
        # this is so dodgey. because i'm randomly generating the sector names and company names
        # and because i know that all sector quotes and company quotes are the same length
        # basically just get the first company from the first sector and use it as the thing we test
        quotes_collected = 0
        for s in test_collection._sectors:
            for c in test_collection._sectors[s]._companies:
                test_company = test_collection._sectors[s]._companies[c].code
                quote_result = test_collection.get_company_by_code(
                    test_company
                ).get_quote()
                self.assertEqual(len(quote_result), CONST_TEST_COMPANY_QUOTES)
                quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_COMPANY_QUOTES
            * CONST_TEST_SECTOR_COUNT
            * CONST_TEST_COMPANY_COUNT,
        )

    def test_get_quotes_filtered_by_date(self):
        self.assertEqual(True, False)
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        # company 1 and 2 are different companys but will have quotes on the same date
        # company 2 will have two quotes each on a different date
        test_company_1 = Company(
            company_name=CONST_COMPANY1_COMPANY_NAME,
            company_code=CONST_COMPANY1_COMPANY_NAME,
            sector_object=test_sector,
        )
        test_company_2 = Company(
            company_name=CONST_COMPANY2_COMPANY_NAME,
            company_code=CONST_COMPANY2_COMPANY_NAME,
            sector_object=test_sector,
        )

        test_company_quote1 = CompanyQuote(
            company_object=test_company_1,
            date=CONST_QUOTE1_DATE,
            open=10,
            high=12,
            low=8,
            close=11,
            volume=2000,
        )

        test_company_quote2 = CompanyQuote(
            company_object=test_company_1,
            date=CONST_QUOTE2_DATE,
            open=10,
            high=12,
            low=8,
            close=11,
            volume=2000,
        )

        test_company_quote3 = CompanyQuote(
            company_object=test_company_1,
            date=CONST_QUOTE1_DATE,
            open=10,
            high=12,
            low=8,
            close=11,
            volume=2000,
        )

        # result = test_company.get_quotes().filter(date=CONST_QUOTE1_DATE)
        # self.assertEqual(CONST_company, result[0].company_code)
        # self.assertEqual(CONST_Q1_QUOTE_DATE, result[0].date)
        # self.assertEqual(10, result[0].open)

    def test_get_quotes_filtered_by_company_code(self):
        self.assertEqual(True, False)

    def test_get_quotes_filtered_by_company_code_filtered_by_date(self):
        self.assertEqual(True, False)

    def test_diff(self):
        self.assertEqual(True, False)


class TestSectorCollection(unittest.TestCase):
    def test_property_length(self):
        test_sector_collection = generate_sector_collection(
            sector_count=CONST_TEST_SECTOR_COUNT,
            company_count=CONST_TEST_COMPANY_COUNT,
            sector_quotes=CONST_TEST_SECTOR_QUOTES,
            company_quotes=CONST_TEST_COMPANY_QUOTES,
        )

        self.assertEqual(test_sector_collection.length, CONST_TEST_SECTOR_COUNT)

    def test_property_name(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector_collection.add_sector(
            Sector(sector_name="my mining company", sector_code="min")
        )

        self.assertEqual(test_sector_collection.name, "asx test")

    def test_add_sector(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector_collection.add_sector(
            Sector(sector_name="my mining company", sector_code="min")
        )

        self.assertEqual(test_sector_collection.length, 1)
        self.assertEqual(
            test_sector_collection._sectors["min"].sector_name, "my mining company"
        )
        self.assertEqual(test_sector_collection._sectors["min"].sector_code, "min")

    def test_get_sector_by_code(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector = Sector(sector_name="my mining company", sector_code="min")
        test_sector_collection.add_sector(test_sector)

        self.assertEqual(test_sector_collection.get_sector_by_code("min"), test_sector)

    def test_get_quotes(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector = Sector(sector_name="my mining company", sector_code="min")
        test_sector_collection.add_sector(test_sector)

        result = test_sector_collection.get_quotes()

        self.assertEqual(
            result,
        )

    def test_filter(self):
        ...


class TestCompanyCollection(unittest.TestCase):
    def test_add_Company(self):
        ...

    def test_get_company_by_code(self):
        ...

    def test_get_quotes(self):
        ...

    def test_filter(self):
        ...


class TestQuoteCollection(unittest.TestCase):
    def test_add_quote(self):
        ...

    def test_filter_by_date(self):
        ...

    def test_filter_by_sector_code(self):
        ...

    def test_get_quotes(self):
        ...


class TestSectorQuote(unittest.TestCase):
    def test_get_open():
        assert (True, False)

    def test_get_high():
        assert (True, False)

    def test_get_low():
        assert (True, False)

    def test_get_close():
        assert (True, False)

    def test_get_volume():
        assert (True, False)


class TestCompanyQuote(unittest.TestCase):
    def test_get_open():
        assert (True, False)

    def test_get_high():
        assert (True, False)

    def test_get_low():
        assert (True, False)

    def test_get_close():
        assert (True, False)

    def test_get_volume():
        assert (True, False)


# companys.get_quotes()
#                    .filter(date=)
#                    .filter(company_code=)
#

# yfinance gives me a list of quotes
# convert them in to company objects
# sql gives me a list of quotes
# convert them in to company objects
# diff()

# deprecated - probably won't use collections - collapse them in to companys/sectors
# class TestSectorCollection(unittest.TestCase):
#    def test_init(self):
#        test_sector = quote.Sector(CONST_SECTOR1_NAME, CONST_SECTOR1_CODE)
#        test_sectorcollection = quote.SectorCollection()
#        self.assertEqual(0, test_sectorcollection.count())
#
#    def test_add(self):
#        test_sector = quote.Sector(CONST_SECTOR1_NAME, CONST_SECTOR1_CODE)
#        test_sectorcollection = quote.SectorCollection()
#        test_sectorcollection.add(test_sector)
#        self.assertEqual(1, test_sectorcollection.count())
#        test_sectorcollection.add(test_sector)
#        self.assertEqual(2, test_sectorcollection.count())

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
CONST_TEST_SECTOR_COUNT = 5
CONST_TEST_COMPANY_COUNT = 11
CONST_TEST_SECTOR_QUOTES = 13
CONST_TEST_COMPANY_QUOTES = 17
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
        day = 1
        day = CONST_QUOTES_START_DAY
        while sector_quotes_generated < sector_quotes:
            this_collection.get_sector_by_code(
                generated_sector.sector_code
            ).add_sector_quote(
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
            day = 1
            while company_quotes_generated < company_quotes:
                this_collection.get_company_by_code(
                    company_code=generated_company.company_code
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


class TestTestSetup(unittest.TestCase):
    def test_generate_sector(self):
        test_sector = generate_sector()
        self.assertEqual(isinstance(test_sector, Sector), True)

    def test_generate_company(self):
        test_company = generate_company(generate_sector())
        self.assertEqual(isinstance(test_company, Company), True)

    def test_generate_sector_collection(self):
        test_collection = generate_sector_collection(
            sector_count=CONST_TEST_SECTOR_COUNT,
            company_count=CONST_TEST_COMPANY_COUNT,
            sector_quotes=CONST_TEST_SECTOR_QUOTES,
            company_quotes=CONST_TEST_COMPANY_QUOTES,
        )

        self.assertEqual(isinstance(test_collection, SectorCollection), True)
        self.assertEqual(len(test_collection._sectors), CONST_TEST_SECTOR_COUNT)
        for sector in test_collection._sectors:
            self.assertEqual(isinstance(test_collection._sectors[sector], Sector), True)

            self.assertEqual(
                len(test_collection._sectors[sector]._quotes), CONST_TEST_SECTOR_QUOTES
            )
            for sector_quote in test_collection._sectors[sector]._quotes:
                self.assertEqual(
                    isinstance(
                        test_collection._sectors[sector]._quotes[sector_quote],
                        SectorQuote,
                    ),
                    True,
                )

            self.assertEqual(
                len(test_collection._sectors[sector]._companies),
                CONST_TEST_COMPANY_COUNT,
            )
            for company in test_collection._sectors[sector]._companies:
                self.assertEqual(
                    isinstance(
                        test_collection._sectors[sector]._companies[company], Company
                    ),
                    True,
                )
                self.assertEqual(
                    len(test_collection._sectors[sector]._companies[company]._quotes),
                    CONST_TEST_COMPANY_QUOTES,
                )

                for company_quote in (
                    test_collection._sectors[sector]._companies[company]._quotes
                ):
                    self.assertEqual(
                        isinstance(
                            test_collection._sectors[sector]
                            ._companies[company]
                            ._quotes[company_quote],
                            CompanyQuote,
                        ),
                        True,
                    )


class TestCompany(unittest.TestCase):  # done
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
                    company_code=test_company
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
                    company_code=test_company
                ).get_quote(
                    date=datetime.strptime(f"01/10/20", "%d/%m/%y"),
                )
                self.assertEqual(len(quote_result), 1)
                quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT,
        )

    def test_get_quotes_filtered_by_date_start(self):
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
                    company_code=test_company
                ).get_quote(date_from=datetime.strptime(f"03/10/20", "%d/%m/%y"))
                self.assertEqual(len(quote_result), 3)
                quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected, CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT * 3
        )

    def test_get_quotes_filtered_by_date_end(self):
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
                    company_code=test_company
                ).get_quote(date_to=datetime.strptime(f"02/10/20", "%d/%m/%y"))
                self.assertEqual(len(quote_result), 2)
                quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected, CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT * 2
        )

    def test_get_quotes_filtered_by_date_start_and_date_end(self):
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
                    company_code=test_company
                ).get_quote(
                    date_from=datetime.strptime(f"01/10/20", "%d/%m/%y"),
                    date_to=datetime.strptime(f"05/10/20", "%d/%m/%y"),
                )
                self.assertEqual(len(quote_result), 5)
                quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT * 5,
        )


class TestCompanyQuote(unittest.TestCase):  # done
    def test_attr_name(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.name
        self.assertEqual(result, "A company name")

    def test_attr_code(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.code
        self.assertEqual(result, "xyz")

    def test_attr_company_name(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.company_name
        self.assertEqual(result, "A company name")

    def test_attr_company_code(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.company_code
        self.assertEqual(result, "xyz")

    def test_get_open(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.open
        self.assertEqual(result, 8.2)

    def test_get_high(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.high
        self.assertEqual(result, 10.3)

    def test_get_low(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.low
        self.assertEqual(result, 5.6)

    def test_get_close(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.close
        self.assertEqual(result, 6.8)

    def test_get_volume(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.volume
        self.assertEqual(result, 21000000)

    def test_get_quote(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_company = Company("A company name", "xyz", sector_object=test_sector)
        test_date = datetime.now()
        test_company_quote = CompanyQuote(
            company_object=test_company,
            date=test_date,
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_company_quote.get_quote()
        self.assertEqual(result["company_name"], "A company name")
        self.assertEqual(result["company_code"], "xyz")
        self.assertEqual(result["date"], test_date)
        self.assertEqual(result["open"], 8.2)
        self.assertEqual(result["high"], 10.3)
        self.assertEqual(result["low"], 5.6)
        self.assertEqual(result["close"], 6.8)
        self.assertEqual(result["volume"], 21000000)


class TestQuoteCollection(unittest.TestCase):
    def test_add_quote(self):
        self.assertEqual(True, False)

    def test_filter_by_date(self):
        self.assertEqual(True, False)

    def test_filter_by_sector_code(self):
        self.assertEqual(True, False)

    def test_get_quotes(self):
        self.assertEqual(True, False)


class TestSector(unittest.TestCase):
    def test_attr_sector_name(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        result = test_sector.sector_name
        self.assertEqual(CONST_SECTOR1_NAME, result)

    def test_attr_sector_code(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        result = test_sector.sector_code
        self.assertEqual(CONST_SECTOR1_CODE, result)

    def test_attr_name(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        result = test_sector.name
        self.assertEqual(CONST_SECTOR1_NAME, result)

    def test_attr_code(self):
        test_sector = Sector(
            sector_name=CONST_SECTOR1_NAME, sector_code=CONST_SECTOR1_CODE
        )
        result = test_sector.code
        self.assertEqual(CONST_SECTOR1_CODE, result)

    def test_attr_sector_quote_length(self):
        test_collection = generate_sector_collection(
            sector_count=CONST_TEST_SECTOR_COUNT,
            company_count=CONST_TEST_COMPANY_COUNT,
            sector_quotes=CONST_TEST_SECTOR_QUOTES,
            company_quotes=CONST_TEST_COMPANY_QUOTES,
        )

        for sector in test_collection._sectors:
            self.assertEqual(
                test_collection._sectors[sector].sector_quote_length,
                CONST_TEST_SECTOR_QUOTES,
            )

    def test_attr_company_length(self):
        test_collection = generate_sector_collection(
            sector_count=CONST_TEST_SECTOR_COUNT,
            company_count=CONST_TEST_COMPANY_COUNT,
            sector_quotes=CONST_TEST_SECTOR_QUOTES,
            company_quotes=CONST_TEST_COMPANY_QUOTES,
        )

        for sector in test_collection._sectors:
            self.assertEqual(
                test_collection._sectors[sector].company_length,
                CONST_TEST_COMPANY_COUNT,
            )

    def test_attr_company_quote_length(self):
        test_collection = generate_sector_collection(
            sector_count=CONST_TEST_SECTOR_COUNT,
            company_count=CONST_TEST_COMPANY_COUNT,
            sector_quotes=CONST_TEST_SECTOR_QUOTES,
            company_quotes=CONST_TEST_COMPANY_QUOTES,
        )

        for sector in test_collection._sectors:
            for company in test_collection._sectors[sector]._companies:
                self.assertEqual(
                    test_collection._sectors[sector].company_quote_length,
                    CONST_TEST_COMPANY_QUOTES * CONST_TEST_COMPANY_COUNT,
                )

    def test_get_sector_quote_no_filter(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_sector_quote()
            self.assertEqual(len(quote_result), CONST_TEST_SECTOR_QUOTES)
            quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * CONST_TEST_SECTOR_QUOTES,
        )

    def test_get_sector_quote_filtered_by_date(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_sector_quote(date=datetime.strptime(f"03/10/20", "%d/%m/%y"))
            self.assertEqual(len(quote_result), 1)
            quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT,
        )

    def test_get_sector_quote_filtered_by_date_start(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_sector_quote(date_from=datetime.strptime(f"03/10/20", "%d/%m/%y"))
            self.assertEqual(len(quote_result), 3)
            quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * 3,
        )

    def test_get_sector_quote_filtered_by_date_end(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_sector_quote(date_to=datetime.strptime(f"02/10/20", "%d/%m/%y"))
            self.assertEqual(len(quote_result), 2)
            quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * 2,
        )

    def test_get_sector_quote_filtered_by_date_start_and_date_end(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_sector_quote(
                date_from=datetime.strptime(f"02/10/20", "%d/%m/%y"),
                date_to=datetime.strptime(f"04/10/20", "%d/%m/%y"),
            )
            self.assertEqual(len(quote_result), 3)
            quotes_collected += len(quote_result)

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * 3,
        )

    def test_get_company_quote_no_filter(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_company_quote()

            # returns multidimensional array: [company_code][some date]
            self.assertEqual(len(quote_result), CONST_TEST_COMPANY_COUNT)
            for company in quote_result:
                self.assertEqual(len(quote_result[company]), CONST_TEST_COMPANY_QUOTES)
                quotes_collected += len(quote_result[company])

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT
            * CONST_TEST_COMPANY_COUNT
            * CONST_TEST_COMPANY_QUOTES,
        )

    def test_get_company_quote_filtered_by_date(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_company_quote(date=datetime.strptime(f"03/10/20", "%d/%m/%y"))

            # returns multidimensional array: [company_code][some date]
            self.assertEqual(len(quote_result), CONST_TEST_COMPANY_COUNT)
            for company in quote_result:
                self.assertEqual(len(quote_result[company]), 1)
                quotes_collected += len(quote_result[company])

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT,
        )

    def test_get_company_quote_filtered_by_date_start(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_company_quote(date_from=datetime.strptime(f"03/10/20", "%d/%m/%y"))

            # returns multidimensional array: [company_code][some date]
            self.assertEqual(len(quote_result), CONST_TEST_COMPANY_COUNT)
            for company in quote_result:
                self.assertEqual(len(quote_result[company]), 3)
                quotes_collected += len(quote_result[company])

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT * 3,
        )

    def test_get_company_quote_filtered_by_date_end(self):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_company_quote(date_to=datetime.strptime(f"02/10/20", "%d/%m/%y"))

            # returns multidimensional array: [company_code][some date]
            self.assertEqual(len(quote_result), CONST_TEST_COMPANY_COUNT)
            for company in quote_result:
                self.assertEqual(len(quote_result[company]), 2)
                quotes_collected += len(quote_result[company])

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT * 2,
        )

    def test_get_company_quote_filtered_by_date_start_and_date_end(
        self,
    ):
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
            quote_result = test_collection.get_sector_by_code(
                sector_code=s
            ).get_company_quote(
                date_from=datetime.strptime(f"02/10/20", "%d/%m/%y"),
                date_to=datetime.strptime(f"04/10/20", "%d/%m/%y"),
            )

            # returns multidimensional array: [company_code][some date]
            self.assertEqual(len(quote_result), CONST_TEST_COMPANY_COUNT)
            for company in quote_result:
                self.assertEqual(len(quote_result[company]), 3)
                quotes_collected += len(quote_result[company])

        self.assertEqual(
            quotes_collected,
            CONST_TEST_SECTOR_COUNT * CONST_TEST_COMPANY_COUNT * 3,
        )


class TestSectorCollection(unittest.TestCase):
    def test_attr_length(self):
        test_sector_collection = generate_sector_collection(
            sector_count=CONST_TEST_SECTOR_COUNT,
            company_count=CONST_TEST_COMPANY_COUNT,
            sector_quotes=CONST_TEST_SECTOR_QUOTES,
            company_quotes=CONST_TEST_COMPANY_QUOTES,
        )

        self.assertEqual(test_sector_collection.length, CONST_TEST_SECTOR_COUNT)

    def test_attr_name(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector_collection.add_sector(
            Sector(sector_name="my mining sector", sector_code="min")
        )

        self.assertEqual(test_sector_collection.name, "asx test")

    def test_add_sector(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector_collection.add_sector(
            Sector(sector_name="my mining sector", sector_code="min")
        )

        self.assertEqual(test_sector_collection.length, 1)
        self.assertEqual(
            test_sector_collection._sectors["min"].sector_name, "my mining sector"
        )
        self.assertEqual(test_sector_collection._sectors["min"].sector_code, "min")

    def test_get_sector_by_code(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_collection.add_sector(test_sector)

        self.assertEqual(test_sector_collection.get_sector_by_code("min"), test_sector)

    def test_get_quotes(self):
        test_sector_collection = SectorCollection("asx test")
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_collection.add_sector(test_sector)

        result = test_sector_collection.get_quotes()

        self.assertEqual(result, False)

    def test_filter(self):
        self.assertEqual(True, False)


class TestSectorQuote(unittest.TestCase):  # done
    def test_attr_name(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.name
        self.assertEqual(result, "my mining sector")

    def test_attr_code(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.code
        self.assertEqual(result, "min")

    def test_attr_company_name(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.sector_name
        self.assertEqual(result, "my mining sector")

    def test_attr_company_code(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.sector_code
        self.assertEqual(result, "min")

    def test_get_open(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.open
        self.assertEqual(result, 8.2)

    def test_get_high(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.high
        self.assertEqual(result, 10.3)

    def test_get_low(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.low
        self.assertEqual(result, 5.6)

    def test_get_close(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.close
        self.assertEqual(result, 6.8)

    def test_get_volume(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=datetime.now(),
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.volume
        self.assertEqual(result, 21000000)

    def test_get_quote(self):
        test_sector = Sector(sector_name="my mining sector", sector_code="min")
        test_date = datetime.now()
        test_sector_quote = SectorQuote(
            sector_object=test_sector,
            date=test_date,
            open=8.2,
            high=10.3,
            low=5.6,
            close=6.8,
            volume=21000000,
        )
        result = test_sector_quote.volume
        self.assertEqual(result, 21000000)

        result = test_sector_quote.get_quote()
        self.assertEqual(result["sector_name"], "my mining sector")
        self.assertEqual(result["sector_code"], "min")
        self.assertEqual(result["date"], test_date)
        self.assertEqual(result["open"], 8.2)
        self.assertEqual(result["high"], 10.3)
        self.assertEqual(result["low"], 5.6)
        self.assertEqual(result["close"], 6.8)
        self.assertEqual(result["volume"], 21000000)

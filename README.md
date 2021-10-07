# stockobjects
A simple set of objects for representing stock and sector objects in Python.

## Learning intention
1. Packaging my own reusable modules
1. Working towards mastery of OO in Python - more advance scoping, testing, inversion of control, dunder methods
1. More advanced testing approaches

## todo
1. More testing
1. Use mocking
1. Additional validation for dates and checking that exceptions are raised in all edge cases
1. Moving from dict to custom objects for quote collections so that I can use built-in methods via dunders and type hinting for how to interact (dicts provide no hints)

# Usage
## Data structure
SectorCollection object contains 0:m Sector objects
Sector object contains 0:m SectorQuote objects
Sector object contains 0:m Company objects
Company object contains 0:m CompanyQuote objects

## Examples
Instantiate the SectorCollection.  A better name (todo!) would be Market instead of SectorCollection
<br>
<code>my_collection = SectorCollection(name="My first collection")</code>

Instantiate a sector to add to the SectorCollection
<br>
<code>my_sector = Sector(sector_name="Fruit sector", sector_code="xbf")
my_collection.add_sector(my_sector)</code>

Instantiate a company and add it to the sector
<br>
<code>my_company = Company(company_name="Banana company", company_code="ban", sector_object=my_sector)
my_collection.get_sector(my_sector.sector_code).add_company(my_company)</code>

From here, instantiate SectorQuotes and Company quotes
And then start querying them

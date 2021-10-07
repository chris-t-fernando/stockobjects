from datetime import datetime
from stockobjectsexceptions import InvalidDateOptions


class DateParser:
    date_from: datetime
    date_to: datetime

    def __init__(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        date: datetime = None,
    ):
        # date_from = None      date_to = None      date = None             Return all
        # date_from = set       date_to = None      date = None             Return all since
        # date_from = set       date_to = set       date = None             Return all between
        # date_from = set       date_to = set       date = set              Exception
        # date_from = None      date_to = set       date = set              Exception
        # date_from = set       date_to = None      date = set              Exception
        # date_from = None      date_to = None      date = set              Return one

        # permutations first
        if date_from == None and date_to == None and date == None:
            # return all
            picked_from = datetime.strptime("01-01-1970", "%d-%m-%Y")
            picked_to = datetime.now()
        elif date_from != None and date_to == None and date == None:
            # return all since
            picked_from = date_from
            picked_to = datetime.now()
        elif date_from != None and date_to != None and date == None:
            # return all between
            picked_from = date_from
            picked_to = date_to
        elif date_from != None and date_to != None and date != None:
            raise InvalidDateOptions
        elif date_from != None and date_to == None and date != None:
            raise InvalidDateOptions
        elif date_from == None and date_to != None and date != None:
            raise InvalidDateOptions
        elif date_from == None and date_to != None and date == None:
            picked_from = datetime.strptime("01-01-1970", "%d-%m-%Y")
            picked_to = date_to
        elif date_from == None and date_to == None and date != None:
            picked_from = date
            picked_to = date

        # now I know what I'm comparing, make sure they're the right types
        if (
            isinstance(picked_from, datetime) == False
            or isinstance(picked_to, datetime) == False
        ):
            raise TypeError("Parameters must be of type datetime")

        # trim out the time
        picked_from = picked_from.date()
        picked_to = picked_to.date()

        # now we've picked the dates we're going to use, check if they make sense: picked_from is earlier than picked_to
        if picked_from > picked_to:
            # bad - to is before from
            raise ValueError(f"Date_from must be before date_to.")

        # good
        self.date_from = picked_from
        self.date_to = picked_to

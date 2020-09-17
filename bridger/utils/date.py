from datetime import date, datetime, timedelta
from django.conf import settings
from django.utils.timezone import localdate
from dateutil import rrule
from django.utils.dateparse import parse_date
from collections import defaultdict

def get_date_interval_from_get(request):
    """
    Parses a request and returns the start and end date from it.

    Parameters
    ----------
    request: The GET Request Object

    Returns
    -------
    Return a tuple in the form of (start_date, end_date). If either the start date or the end date is not present in the request None is returned in the tuple
    """
    start_identifier = getattr(settings, "BRIDGER_START_IDENTIFIERS", ["start", "start_date", "from", "date_gte"],)
    end_identifier = getattr(settings, "BRIDGER_END_IDENTIFIERS", ["end", "end_date", "to", "date_lte"])
    date_format = getattr(settings, "BRIDGER_DATE_FORMAT", "%Y-%m-%d")

    assert isinstance(start_identifier, list)
    assert isinstance(end_identifier, list)
    assert isinstance(date_format, str)

    start = next((identifier for identifier in start_identifier if identifier in request.GET), None,)
    end = next((identifier for identifier in end_identifier if identifier in request.GET), None)

    if start:
        try:
            start = datetime.strptime(request.GET.get(start), date_format).date()
        except ValueError:
            start = None
    if end:
        try:
            end = datetime.strptime(request.GET.get(end), date_format).date()
        except ValueError:
            end = None

    return start, end


def get_quarter_from_date(d):
    return ((d.month - 1) // 3) + 1


def get_start_date_from_date(d):
    quarter = get_quarter_from_date(d)
    return date(d.year, quarter * 3 - 2, 1)


def get_end_date_from_date(d):
    quarter = get_quarter_from_date(d)
    return date(d.year + ((quarter * 3 + 1) // 12), (quarter * 3 + 1) % 12, 1) - timedelta(days=1)


def get_start_and_end_date_from_date(d):
    return get_start_date_from_date(d), get_end_date_from_date(d)


def current_quarter_date_start(field=None, request=None, view=None):
     return get_start_date_from_date(localdate())

def current_quarter_date_end(field=None, request=None, view=None):
     return get_end_date_from_date(localdate())

def current_quarter_date_interval(field, request, view):
    return (
        current_quarter_date_start(field, request, view),
        current_quarter_date_end(field, request, view),
    )

def current_year_date_start(field, request, view):
    d = localdate()
    return date(d.year,1,1)

def current_year_date_end(field, request, view):
    d = localdate()
    return date(d.year + 1,1,1) - timedelta(days=1)

def current_year_date_interval(field, request, view):
    return (
        current_year_date_start(field, request, view),
        current_year_date_end(field, request, view),
    )

def current_month_date_start(field, request, view):
    d = localdate()
    return date(d.year,d.month,1)

def current_month_date_end(field=None, request=None, view=None):
    d = localdate()
    if d.month == 12:
        return date(d.year, 12, 31)
    return date(d.year, d.month + 1, 1) - timedelta(days=1)

def current_month_date_interval(field, request, view):
    return (
        current_month_date_start(field, request, view),
        current_month_date_end(field, request, view),
    )

    
def get_date_interval_from_request(request, request_type="GET"):
    """
    Parses a request and returns the start and end date from it.

    Parameters
    ----------
    request: The GET Request Object

    Returns
    -------
    Return a tuple in the form of (start_date, end_date). If either the start date or the end date is not present in the request None is returned in the tuple
    """

    start_identifier = ["start", "start_date", "from", "date_gte"]
    end_identifier = ["end", "end_date", "to", "date_lte"]
    params = request.GET if request_type == "GET" else request.POST
    start = None
    end = None
    if "date" in params:
        if len(params.get("date").split(",")) == 2:
            start, end = params.get("date").split(",")
    else:
        start = next(
            (params.get(identifier) for identifier in start_identifier if identifier in params),
            None,
        )
        end = next(
            (params.get(identifier) for identifier in end_identifier if identifier in params), None
        )

    if start:
        start = parse_date(start)
    if end:
        end = parse_date(end)

    return start, end




def get_number_of_hours_between_dates(
    d1, d2, skip_weekends=True, list_public_holidays=False, hours_range=range(0,23), granularity=12
):
    def convert_days_from_hours(hours, granularity, hours_per_day):
        return int(hours/granularity)*granularity/hours_per_day
    rules = rrule.rruleset()
    
    byweekday_list = [rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR]
    if not skip_weekends:
        byweekday_list.extend([rrule.SA, rrule.SU])
    
    rules.rrule(
        rrule.rrule(
            freq=rrule.HOURLY,
            byweekday=byweekday_list,
            byhour=hours_range,
            dtstart=d1,
            until=d2,
        )
    )
    if list_public_holidays:
        for holiday in list_public_holidays:
            s1 = datetime(holiday.year, holiday.month, holiday.day, 0, 0, 0)
            s2 = datetime(holiday.year, holiday.month, holiday.day, 23, 59, 59)
            rules.exrule(
                rrule.rrule(
                    rrule.HOURLY,
                    dtstart=s1,
                    until=s2
                )
            )
    dates = defaultdict(int)
    for r in list(rules):
        dates[r.date()] += 1
    return {k: convert_days_from_hours(v, granularity, len(hours_range)) for k, v in dates.items()}



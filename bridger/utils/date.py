from datetime import datetime

from django.conf import settings


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
    print(request)
    start_identifier = getattr(
        settings,
        "BRIDGER_START_IDENTIFIERS",
        ["start", "start_date", "from", "date_gte"],
    )
    end_identifier = getattr(
        settings, "BRIDGER_END_IDENTIFIERS", ["end", "end_date", "to", "date_lte"]
    )
    date_format = getattr(settings, "BRIDGER_DATE_FORMAT", "%Y-%m-%d")

    assert isinstance(start_identifier, list)
    assert isinstance(end_identifier, list)
    assert isinstance(date_format, str)

    start = next(
        (identifier for identifier in start_identifier if identifier in request.GET),
        None,
    )
    end = next(
        (identifier for identifier in end_identifier if identifier in request.GET), None
    )

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

from calendar import monthrange
from datetime import date

from django.utils.timezone import localdate

from bridger.utils.date import get_end_date_from_date, get_start_date_from_date


def current_quarter_date_start(field, request, view):
    return get_start_date_from_date(localdate())


def current_quarter_date_end(field, request, view):
    return get_end_date_from_date(localdate())


def current_month_date_start(field, request, view):
    today = date.today()
    return date(today.year, today.month, 1)


def current_month_date_end(field, request, view):
    today = date.today()
    return date(today.year, today.month, monthrange(today.year, today.month)[1])


def current_quarter_date_interval(field, request, view):
    return (
        current_quarter_date_start(field, request, view),
        current_quarter_date_end(field, request, view),
    )

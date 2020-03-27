from django.utils.timezone import localdate

from bridger.utils.date import get_start_date_from_date, get_end_date_from_date


def current_quarter_date_start(field, request):
     return get_start_date_from_date(localdate())


def current_quarter_date_end(field, request):
     return get_end_date_from_date(localdate())
from prettytable import PrettyTable
from decimal import Decimal


def prettytable_from_querydict(values, float_format=False):
    ptable = PrettyTable()
    keys = [key for key in values[0].keys()]
    
    ptable.field_names = list(keys)

    if float_format:
        for _values in values:
            formatted_values = list()
            for v in _values.values():
                if type(v) in [float, int, Decimal]:
                    v = f"{v:,.2f}"
                formatted_values.append(v)
            ptable.add_row(formatted_values)
    else:
        for _values in values:
            ptable.add_row(_values.values())

    print(ptable)


def prettytable_from_list(headers, values):
    ptable = PrettyTable()
    
    ptable.field_names = list(headers)

    for _values in values:
        ptable.add_row(_values.values())

    print(ptable)
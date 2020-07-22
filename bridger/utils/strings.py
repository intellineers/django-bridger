
def enumerated_string_join(l):
    ''' Generates a human readable string out of a list '''

    if len(l) > 0:
        l = [str(i) for i in l]
        return ' and '.join([', '.join(l[:-1]), l[-1]]) if len(l) > 1 else l[0]
    return ''

def format_number(number, is_pourcent=False, decimal=2):
    number = number if number else 0
    return f'{number:,.{decimal}{"%" if is_pourcent else "f"}}'
    
class ReferenceIDMixin:
    @property
    def reference_id(self):
        return f"{self.id:06}"
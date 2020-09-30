
from inscriptis import get_text
import re

def convert_html2text(html):
    mail_text = get_text(html)
    return re.sub('[\n]+', '\n', mail_text).strip()

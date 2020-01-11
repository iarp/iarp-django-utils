from bs4 import BeautifulSoup
from django.template.defaulttags import register


@register.filter
def startswith(text, value):
    return text.startswith(value)


@register.filter
def endswith(text, value):
    return text.endswith(value)


@register.filter
def truncatesentences(value, arg):
    """
    Truncate HTML after `arg` number of words.
    Preserve newlines in the HTML.
    """
    try:
        length = int(arg)
    except ValueError:  # invalid literal for int()
        return value  # Fail silently.
    soup = BeautifulSoup(value, 'html.parser')
    lines = []
    for index, line in enumerate(value.split('\n')):
        if index >= length:
            break
        if not line:
            length += 1
        lines.append(line)
    return '\n'.join(lines)

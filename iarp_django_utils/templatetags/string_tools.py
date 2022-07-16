from django.template.defaulttags import register


@register.filter
def startswith(text, value):
    return text.startswith(value)


@register.filter
def endswith(text, value):
    return text.endswith(value)


@register.filter
def truncatesentences(value, arg):
    """Splits on newline characters and returns however many sentences you wish.

    Examples:

        {{ myvar|truncatesentences:3 }}

    Args:
        value: the value to work on
        arg: how many sentences to return
    """
    try:
        length = int(arg)
    except ValueError:  # invalid literal for int()
        return value  # Fail silently.
    lines = []
    for index, line in enumerate(value.split('\n')):
        if index >= length:
            break

        # If the line is blank, do not count it as a sentence
        if not line:
            length += 1

        lines.append(line)
    return '\n'.join(lines)


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)

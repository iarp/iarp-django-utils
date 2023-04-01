from django import template


register = template.Library()


@register.filter()
def smooth_timedelta(timedeltaobj):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()

    is_negative = secs < 0
    if is_negative:
        secs = secs * -1

    timetot = ""
    if secs > 86400:  # 60sec * 60min * 24hrs
        days = secs // 86400
        timetot += "{} day{}".format(int(days), 's' if int(days) != 1 else '')
        secs = secs - days * 86400

    if secs > 3600:
        hrs = secs // 3600
        timetot += " {} hour{}".format(int(hrs), 's' if int(hrs) != 1 else '')
        secs = secs - hrs * 3600

    if secs > 60:
        mins = secs // 60
        timetot += " {} minute{}".format(int(mins), 's' if int(mins) != 1 else '')
        secs = secs - mins * 60

    if secs > 0:
        timetot += " {} second{}".format(int(secs), 's' if int(secs) != 1 else '')

    # if is_negative:
    #     timetot += " ago"

    return timetot.strip()

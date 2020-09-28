from django.template.defaulttags import register

from iarp_utils.strings import slugify


@register.filter
def slug_word(word):
    return slugify(value=word)

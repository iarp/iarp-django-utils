from django import template
from django.contrib.auth.context_processors import auth
from django.template import Context, Template
from django.utils.safestring import mark_safe

from iarp_django_utils.models import get_pagecontents_model


register = template.Library()


@register.simple_tag(takes_context=True)
def page_contents(context, app, location, show_blank=True):

    pc, _ = get_pagecontents_model().objects.get_or_create(app=app, location=location)

    if "request" in context:
        auth_data = auth(context["request"])
        auth_data["request"] = context["request"]
    else:
        auth_data = {}

    context_ctx = Context(auth_data)
    formatted_contents = Template(pc.contents).render(context=context_ctx)

    if not show_blank and not formatted_contents:
        return ""

    return mark_safe(
        """
        <div class="page-contents-wrapper {location}" data-page-contents-id="{id}">
            <div class="page-contents-contents">
                {contents}
            </div>
        </div>""".format(
            id=pc.pk, location=location, contents=formatted_contents
        )
    )

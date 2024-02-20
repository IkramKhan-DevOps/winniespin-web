from django import template

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def image_or_placeholder(image, extras='100'):
    if image:
        return image.url
    return f"https://placeholder.co/{extras}"


@register.filter
def check_null(value):
    if value:
        return value
    return ""
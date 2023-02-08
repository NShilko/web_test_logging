from django import template


register = template.Library()


@register.filter()
def date_converter(date):
    new_date = date.strftime("%d.%m.%Y %H:%M:%S")
    return f'{new_date}'

@register.filter()
def censor(txt):
    spam_list = ['редиска', 'тревога']
    new_text = txt
    for spam in spam_list:
        new_text = new_text.lower().replace(spam, spam[:1] + '*' * (len(spam) - 1))
    return f'{new_text}'

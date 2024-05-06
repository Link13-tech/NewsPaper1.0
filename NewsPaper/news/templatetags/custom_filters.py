from django import template


register = template.Library()


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError("Этот фильтр может быть применен только к тексту")

    censored_words = ["ржавчина", "место", "гость", "котором", "дверь", "напротив", "витрины", "перчатки"]

    censored_text = []
    for word in text.split():
        if word.lower() in censored_words:
            censored_text.append(word[0] + '*' * (len(word) - 1))
        else:
            censored_text.append(word)

    return ' '.join(censored_text)

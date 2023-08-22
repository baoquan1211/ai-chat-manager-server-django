from words_filter.models import WordsFilter


def message_filter(message):
    words = WordsFilter.objects.get()
    print(words)

from string import punctuation
from typing import List


def gen_stop_word(file_input, searches: List[str], stops: List[str]):
    searches_vocab = set(word.lower() for word in searches)
    stops_vocab = set(word.lower() for word in stops)

    if isinstance(file_input, str):
        file = open(file_input, 'r', encoding='utf-8')
    else:
        file = file_input

    for line in file:
        string = set(line.translate(str.maketrans('', '', punctuation)).strip().lower().split())

        if stops_vocab & string:
            continue

        if searches_vocab & string:
            yield line

    file.close()


for i in gen_stop_word('lermontov.txt', searches=['голубом', 'скрыпит'], stops=['']):
    print(i)

print('-' * 100)

with open('lermontov.txt', 'r', encoding='utf-8') as f:
    for i in gen_stop_word(f, ['покой', 'парус', 'увы'], ['ветер']):
        print(i)
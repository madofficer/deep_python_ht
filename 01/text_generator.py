from string import punctuation
from io import StringIO


def gen_stop_word(file_input, searches=None, stops=None):
    if stops is None:
        stops = [""]
    if searches is None:
        searches = [""]

    def parse_lines(f):
        searches_vocab = set(word.lower() for word in searches)
        stops_vocab = set(word.lower() for word in stops)
        for line in f:
            string = set(
                line.translate(str.maketrans("", "", punctuation))
                .strip()
                .lower()
                .split()
            )

            if stops_vocab & string:
                continue

            if searches_vocab & string:
                yield line

    if isinstance(file_input, str):
        with open(file_input, "r", encoding="utf-8") as file:
            yield from parse_lines(file)
    else:
        yield from parse_lines(file_input)


# if __name__ == "__main__":
#
#     for i in gen_stop_word("lermontov.txt", searches=["голубом", "скрыпит"]):
#         print(i)
#
#     print("-" * 100)
#
#     with open("lermontov.txt", "r", encoding="utf-8") as lermont:
#         for i in gen_stop_word(lermont, ["покой", "парус", "увы"], ["ветер"]):
#             print(i)
#
#     text = "\nа Роза упала на лапу Азора\nSATOR AREPO TENET OPERA ROTAS"
#     print(text)
#     file = StringIO(text)
#
#     print('-' * 100)
#     gen = gen_stop_word('rofl', ['SATOR'], ["а Роза упала на лапу Азора"])
#     words = list(gen)
    # words = [word.strip() for word in words]
    # print(words)

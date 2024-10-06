import json
from string import punctuation
from collections.abc import Callable


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | str = str,
) -> None:

    if (required_keys is None or len(required_keys) == 0) or (tokens is None or len(tokens) == 0):
        print('nothing to say..')
        return

    if callback is None:
        callback = lambda k, t:  f"I found for you key: {k} and value: {t}"

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as error:
        print(f"json parsing error {error}")
        return

    required_keys = set(required_keys)
    tokens = set(token.lower() for token in tokens)
    for key, value in data.items():
        if key in required_keys:
            value_to_process = (
                value.translate(str.maketrans("", "", punctuation))
                .strip()
                .lower()
                .split()
            )
            for tok in value_to_process:
                if tok in tokens:
                    print(callback(key, tok))


if __name__ == "__main__":
    with open("poets.txt", "r", encoding="utf-8") as f:
        json_string = " ".join(line.strip() for line in f.readlines())

    keys_arg = ["Anton_Chekhov", "Lev_Tolstoy", "Alexander_Pushkin"]
    tokens_arg = ["СЕРДЦЕ", "жизнь", "мЫ"]
    process_json(
        json_string,
        keys_arg,
        tokens_arg,
        lambda author, his_word: f"{author=}, {his_word=}",
    )
    print('---')
    process_json(json_string, None, None, lambda author, his_word: f"{author=}, {his_word=}")
    print('---')
    process_json(json_string, keys_arg, tokens_arg, None)
    print('---')
    process_json(json_string, None, None, None)

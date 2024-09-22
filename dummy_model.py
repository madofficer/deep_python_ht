class DummyModel:
    def predict(self, message: str) -> float:
        raise NotImplementedError


def predict_message_mood(
    message: str, bad_thresholds: float = 0.3, good_thresholds: float = 0.8
) -> str:
    if not isinstance(message, str):
        raise TypeError(
            f"Argument 'message' must be str," f" not {type(message).__name__}"
        )
    if not isinstance(bad_thresholds, float):
        raise TypeError(
            f"Argument 'bad_thresholds' must be float,"
            f" not {type(bad_thresholds).__name__}"
        )
    if not isinstance(good_thresholds, float):
        raise TypeError(
            f"Argument 'good_thresholds' must be float,"
            f" not {type(good_thresholds).__name__}"
        )

    if not (0 < bad_thresholds < 1):
        raise ValueError(
            f"Argument 'bad_thresholds' must be between 0 and 1,"
            f" got {bad_thresholds}"
        )
    if good_thresholds <= bad_thresholds:
        raise ValueError(
            f"Argument 'good_thresholds' must be greater than"
            f" 'bad_thresholds', got 'bad_thresholds'={bad_thresholds},"
            f"'good_thresholds'={good_thresholds}"
        )
    if not (0 < good_thresholds < 1):
        raise ValueError(
            f"Argument 'good_thresholds' must be between 0 and 1,"
            f" got {good_thresholds}"
        )

    model = DummyModel()
    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    elif prediction > good_thresholds:
        return "отл"
    else:
        return "норм"

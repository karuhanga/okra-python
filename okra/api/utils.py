class OptionalDict(dict):
    def __init__(self, **kwargs):
        final_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        super().__init__(**final_kwargs)

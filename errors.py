class ApiRateLimitError(BaseException):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"You have reached the maximum number of calls per day for the {self.name} API."
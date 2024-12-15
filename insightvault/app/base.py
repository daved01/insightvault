from ..utils.logging import get_logger


class BaseApp:
    def __init__(self, name: str = "insightvault") -> None:
        self.name = name
        self.logger = get_logger(self.name)

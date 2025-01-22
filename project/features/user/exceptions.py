class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)

class UserDeleteError(Exception):
    def __init__(self, message: str = "User delete error"):
        self.message = message
        super().__init__(self.message)

class UserExistsError(Exception):
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)
class EntityNotFoundException(Exception):
    def __init__(self, repository, **kwargs):
        message = f"Entity not found for {kwargs}"
        super().__init__(message)
        self.repository = repository
        self.kwargs = kwargs


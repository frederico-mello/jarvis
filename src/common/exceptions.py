class ICTGraphRAGError(Exception):
    pass


class ConfigurationError(ICTGraphRAGError):
    pass


class SourceIngestionError(ICTGraphRAGError):
    pass


class RetrievalError(ICTGraphRAGError):
    pass


class AuthenticationError(ICTGraphRAGError):
    pass


class AuthorizationError(ICTGraphRAGError):
    pass


class ValidationError(ICTGraphRAGError):
    pass


class RateLimitError(ICTGraphRAGError):
    pass

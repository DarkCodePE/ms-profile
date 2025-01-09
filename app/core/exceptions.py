# app/core/exceptions.py
class ProfilerException(Exception):
    """Base exception for scraper errors."""
    pass


class KafkaError(ProfilerException):
    """Raised when there's an error with Kafka operations."""
    pass

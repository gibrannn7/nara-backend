class NaraBaseException(Exception):
    """Base exception for all application-level errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InfrastructureException(NaraBaseException):
    """Raised when third-party services (GCP, Mixpanel, etc.) fail."""
    def __init__(self, message: str = "Infrastructure dependency failed", status_code: int = 503):
        super().__init__(message, status_code)

class ResourceNotFoundException(NaraBaseException):
    """Raised when a Firestore document is not found."""
    def __init__(self, resource_name: str, resource_id: str):
        super().__init__(f"{resource_name} with ID {resource_id} not found", 404)
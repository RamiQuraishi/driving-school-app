"""Custom exceptions for the Ontario Driving School Manager."""

class ODSMError(Exception):
    """Base exception for all ODSM errors."""
    
    def __init__(self, message: str, code: str = None):
        """Initialize ODSM error.
        
        Args:
            message: Error message
            code: Error code
        """
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationError(ODSMError):
    """Exception for validation errors."""
    
    def __init__(self, message: str, field: str = None, value: any = None):
        """Initialize validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
            value: Invalid value
        """
        self.field = field
        self.value = value
        super().__init__(message, "VALIDATION_ERROR")

class DatabaseError(ODSMError):
    """Exception for database errors."""
    
    def __init__(self, message: str, operation: str = None):
        """Initialize database error.
        
        Args:
            message: Error message
            operation: Database operation that failed
        """
        self.operation = operation
        super().__init__(message, "DATABASE_ERROR")

class MTOComplianceError(ODSMError):
    """Exception for MTO compliance violations."""
    
    def __init__(
        self,
        message: str,
        requirement: str = None,
        entity_type: str = None,
        entity_id: str = None
    ):
        """Initialize MTO compliance error.
        
        Args:
            message: Error message
            requirement: MTO requirement that was violated
            entity_type: Type of entity (instructor, vehicle, etc.)
            entity_id: ID of the entity
        """
        self.requirement = requirement
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(message, "MTO_COMPLIANCE_ERROR")

class BusinessRuleError(ODSMError):
    """Exception for business rule violations."""
    
    def __init__(
        self,
        message: str,
        rule: str = None,
        context: dict = None
    ):
        """Initialize business rule error.
        
        Args:
            message: Error message
            rule: Business rule that was violated
            context: Additional context about the violation
        """
        self.rule = rule
        self.context = context or {}
        super().__init__(message, "BUSINESS_RULE_ERROR")

class VersionConflictError(ODSMError):
    """Exception for version conflicts."""
    
    def __init__(
        self,
        message: str,
        current_version: int = None,
        new_version: int = None,
        entity_type: str = None,
        entity_id: str = None
    ):
        """Initialize version conflict error.
        
        Args:
            message: Error message
            current_version: Current version number
            new_version: New version number
            entity_type: Type of entity
            entity_id: ID of the entity
        """
        self.current_version = current_version
        self.new_version = new_version
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(message, "VERSION_CONFLICT_ERROR")

class EventError(ODSMError):
    """Exception for event handling errors."""
    
    def __init__(
        self,
        message: str,
        event_type: str = None,
        handler: str = None
    ):
        """Initialize event error.
        
        Args:
            message: Error message
            event_type: Type of event that failed
            handler: Handler that failed
        """
        self.event_type = event_type
        self.handler = handler
        super().__init__(message, "EVENT_ERROR")

class ConfigurationError(ODSMError):
    """Exception for configuration errors."""
    
    def __init__(
        self,
        message: str,
        config_key: str = None,
        config_value: any = None
    ):
        """Initialize configuration error.
        
        Args:
            message: Error message
            config_key: Configuration key that caused the error
            config_value: Invalid configuration value
        """
        self.config_key = config_key
        self.config_value = config_value
        super().__init__(message, "CONFIGURATION_ERROR") 
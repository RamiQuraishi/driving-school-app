# Shared Code Guidelines

## Overview
This document outlines the guidelines for sharing code between the Electron frontend and FastAPI backend in the Ontario Driving School Manager application.

## Directory Structure

### Shared Code Location
```
src/
  shared/
    constants/     # Shared constants
    types/         # Shared type definitions
    validation/    # Shared validation rules
    utils/         # Shared utility functions
```

## Type Definitions

### Python Types
```python
# src/shared/types/models.py
from pydantic import BaseModel
from typing import Optional, List

class Student(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    courses: List[str]
```

### TypeScript Types
```typescript
// src/shared/types/models.ts
export interface Student {
  id: number;
  name: string;
  email: string;
  phone?: string;
  courses: string[];
}
```

## Constants

### Python Constants
```python
# src/shared/constants/status.py
from enum import Enum

class StudentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
```

### TypeScript Constants
```typescript
// src/shared/constants/status.ts
export enum StudentStatus {
  ACTIVE = "active",
  INACTIVE = "inactive",
  PENDING = "pending"
}
```

## Validation Rules

### Python Validation
```python
# src/shared/validation/student.py
from pydantic import BaseModel, validator
import re

class StudentValidator(BaseModel):
    @validator("email")
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v
```

### TypeScript Validation
```typescript
// src/shared/validation/student.ts
import { z } from "zod";

export const studentSchema = z.object({
  email: z.string().email("Invalid email format")
});
```

## Utility Functions

### Python Utilities
```python
# src/shared/utils/formatting.py
from datetime import datetime
from typing import Optional

def format_date(date: Optional[datetime]) -> str:
    if not date:
        return ""
    return date.strftime("%Y-%m-%d")
```

### TypeScript Utilities
```typescript
// src/shared/utils/formatting.ts
import { format } from "date-fns";

export const formatDate = (date?: Date): string => {
  if (!date) return "";
  return format(date, "yyyy-MM-dd");
};
```

## Best Practices

### Type Safety
- Use strong typing in both languages
- Keep type definitions in sync
- Use type checking tools
- Document type changes

### Code Organization
- Keep shared code modular
- Use clear naming conventions
- Maintain consistent structure
- Document shared components

### Version Control
- Track changes to shared code
- Update both implementations
- Test changes in both environments
- Document breaking changes

### Testing
- Test shared code in both environments
- Maintain test coverage
- Use similar test patterns
- Share test utilities

## Implementation Guidelines

### Python Backend
- Use Pydantic for validation
- Implement type hints
- Follow PEP 8
- Use async/await

### TypeScript Frontend
- Use Zod for validation
- Implement interfaces
- Follow ESLint rules
- Use React patterns

## Error Handling

### Python
```python
# src/shared/errors.py
from typing import Optional

class SharedError(Exception):
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(message)
```

### TypeScript
```typescript
// src/shared/errors.ts
export class SharedError extends Error {
  constructor(
    message: string,
    public code?: string
  ) {
    super(message);
    this.name = "SharedError";
  }
}
```

## Data Transformation

### Python
```python
# src/shared/transformers.py
from typing import Dict, Any

def to_api_format(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": data["id"],
        "name": data["name"].title(),
        "email": data["email"].lower()
    }
```

### TypeScript
```typescript
// src/shared/transformers.ts
interface Data {
  id: number;
  name: string;
  email: string;
}

export const toApiFormat = (data: Data) => ({
  id: data.id,
  name: data.name.charAt(0).toUpperCase() + data.name.slice(1),
  email: data.email.toLowerCase()
});
```

## Documentation

### Code Comments
- Document shared interfaces
- Explain complex logic
- Note platform differences
- Update when changed

### API Documentation
- Document shared endpoints
- Include examples
- Note limitations
- Keep up to date

## Maintenance

### Regular Tasks
- Update dependencies
- Check type compatibility
- Review shared code
- Update documentation

### Best Practices
- Keep code DRY
- Maintain consistency
- Test thoroughly
- Document changes 
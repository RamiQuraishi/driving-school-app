"""
Telemetry Service

This module implements anonymous telemetry collection for the Ontario Driving School Manager.
It collects usage data while maintaining user privacy.

Author: Rami Drive School
Date: 2024
"""

import json
import platform
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class TelemetryData:
    """Telemetry data."""
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    session_id: str
    device_id: str
    app_version: str
    os_info: Dict[str, str]

class TelemetryService:
    """Telemetry service implementation."""
    
    def __init__(
        self,
        app_version: str,
        storage_path: str,
        enabled: bool = True
    ):
        """Initialize telemetry service.
        
        Args:
            app_version: Application version
            storage_path: Path to store telemetry data
            enabled: Whether telemetry is enabled
        """
        self.app_version = app_version
        self.storage_path = storage_path
        self.enabled = enabled
        self.device_id = self._get_or_create_device_id()
        self.session_id = str(uuid.uuid4())
    
    def track_event(
        self,
        event_type: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Track telemetry event.
        
        Args:
            event_type: Event type
            data: Event data
        """
        if not self.enabled:
            return
            
        # Create telemetry data
        telemetry = TelemetryData(
            event_type=event_type,
            timestamp=datetime.utcnow(),
            data=data or {},
            session_id=self.session_id,
            device_id=self.device_id,
            app_version=self.app_version,
            os_info=self._get_os_info()
        )
        
        # Save telemetry data
        self._save_telemetry(telemetry)
    
    def _get_or_create_device_id(self) -> str:
        """Get or create device ID.
        
        Returns:
            str: Device ID
        """
        try:
            with open(self.storage_path + '.device_id', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            device_id = str(uuid.uuid4())
            with open(self.storage_path + '.device_id', 'w') as f:
                f.write(device_id)
            return device_id
    
    def _get_os_info(self) -> Dict[str, str]:
        """Get OS information.
        
        Returns:
            Dict[str, str]: OS information
        """
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    def _save_telemetry(self, telemetry: TelemetryData) -> None:
        """Save telemetry data.
        
        Args:
            telemetry: Telemetry data
        """
        # Convert telemetry to dict
        telemetry_dict = {
            'event_type': telemetry.event_type,
            'timestamp': telemetry.timestamp.isoformat(),
            'data': telemetry.data,
            'session_id': telemetry.session_id,
            'device_id': telemetry.device_id,
            'app_version': telemetry.app_version,
            'os_info': telemetry.os_info
        }
        
        # Save to file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(telemetry_dict) + '\n')
    
    def start_new_session(self) -> None:
        """Start new telemetry session."""
        self.session_id = str(uuid.uuid4())
    
    def enable(self) -> None:
        """Enable telemetry collection."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable telemetry collection."""
        self.enabled = False 
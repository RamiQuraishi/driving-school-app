"""
Anonymous telemetry service.
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from ..config.telemetry import telemetry_config

logger = logging.getLogger(__name__)

class TelemetryService:
    """Anonymous telemetry service."""
    
    def __init__(self):
        """Initialize the telemetry service."""
        self.config = telemetry_config
        self._session: Optional[aiohttp.ClientSession] = None
        self._queue: asyncio.Queue = asyncio.Queue()
        self._running = False
    
    async def start(self) -> None:
        """Start the telemetry service."""
        if not self.config.enabled:
            return
            
        self._running = True
        self._session = aiohttp.ClientSession()
        asyncio.create_task(self._process_queue())
    
    async def stop(self) -> None:
        """Stop the telemetry service."""
        self._running = False
        if self._session:
            await self._session.close()
    
    async def track_metric(self, name: str, value: Any, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Track a telemetry metric.
        
        Args:
            name: Metric name
            value: Metric value
            tags: Optional metric tags
        """
        if not self.config.enabled:
            return
            
        try:
            await self._queue.put({
                'name': name,
                'value': value,
                'tags': tags or {},
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.error(f"Error queueing metric {name}: {str(e)}")
    
    async def _process_queue(self) -> None:
        """Process the telemetry queue."""
        batch = []
        
        while self._running:
            try:
                # Collect metrics until batch size or timeout
                while len(batch) < self.config.batch_size:
                    try:
                        metric = await asyncio.wait_for(
                            self._queue.get(),
                            timeout=self.config.collection_interval
                        )
                        batch.append(metric)
                    except asyncio.TimeoutError:
                        break
                
                if batch:
                    await self._send_metrics(batch)
                    batch = []
                    
            except Exception as e:
                logger.error(f"Error processing telemetry queue: {str(e)}")
                await asyncio.sleep(5)  # Back off on error
    
    async def _send_metrics(self, metrics: list) -> None:
        """
        Send metrics to telemetry endpoint.
        
        Args:
            metrics: List of metrics to send
        """
        if not self._session:
            return
            
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.config.api_key or ''
        }
        
        data = {
            'metrics': metrics,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '0.1.0'
        }
        
        for attempt in range(self.config.max_retries):
            try:
                async with self._session.post(
                    self.config.endpoint,
                    json=data,
                    headers=headers,
                    timeout=self.config.timeout
                ) as response:
                    if response.status == 200:
                        return
                    logger.warning(f"Telemetry request failed: {response.status}")
            except Exception as e:
                logger.error(f"Error sending telemetry: {str(e)}")
            
            await asyncio.sleep(2 ** attempt)  # Exponential backoff 
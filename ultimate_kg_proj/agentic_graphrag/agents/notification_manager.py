"""
Notification Management System for Agentic GraphRAG

This module implements a comprehensive notification system with multiple channels
for alerting users about interesting connections and system events.
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, Protocol
from datetime import datetime
from pathlib import Path
import aiofiles
import httpx
from abc import ABC, abstractmethod

from .schemas import NotificationEvent, DetectedConnection
from ..config import config

# Configure logging
logger = logging.getLogger(__name__)

class NotificationChannel(ABC):
    """Abstract base class for notification channels"""
    
    @abstractmethod
    async def send_notification(self, event: NotificationEvent) -> bool:
        """Send a notification through this channel"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test if the channel is properly configured and reachable"""
        pass
    
    @property
    @abstractmethod
    def channel_name(self) -> str:
        """Get the name of this notification channel"""
        pass

class ConsoleNotificationChannel(NotificationChannel):
    """Console-based notification channel that prints to stdout"""
    
    def __init__(self, colored: bool = True):
        self.colored = colored
        self.colors = {
            "info": "\033[94m",      # Blue
            "warning": "\033[93m",   # Yellow
            "error": "\033[91m",     # Red
            "critical": "\033[95m",  # Magenta
            "reset": "\033[0m"       # Reset
        }
    
    @property
    def channel_name(self) -> str:
        return "console"
    
    async def send_notification(self, event: NotificationEvent) -> bool:
        """Send notification to console"""
        try:
            timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            if self.colored:
                color = self.colors.get(event.severity, "")
                reset = self.colors["reset"]
                print(f"{color}[{timestamp}] {event.severity.upper()}: {event.message}{reset}")
            else:
                print(f"[{timestamp}] {event.severity.upper()}: {event.message}")
            
            # Print additional data if present
            if event.data:
                formatted_data = json.dumps(event.data, indent=2)
                print(f"  Data: {formatted_data}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to print console notification: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test console output"""
        try:
            print("Console notification channel test - OK")
            return True
        except Exception:
            return False

class FileNotificationChannel(NotificationChannel):
    """File-based notification channel that writes to log files"""
    
    def __init__(self, file_path: str = "notifications.log", max_size_mb: int = 10):
        self.file_path = Path(file_path)
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
        
        # Ensure directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    @property
    def channel_name(self) -> str:
        return "file"
    
    async def send_notification(self, event: NotificationEvent) -> bool:
        """Send notification to file"""
        try:
            # Check file size and rotate if needed
            await self._rotate_if_needed()
            
            # Format notification
            timestamp = event.timestamp.isoformat()
            notification_data = {
                "timestamp": timestamp,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "severity": event.severity,
                "message": event.message,
                "data": event.data
            }
            
            # Write to file
            async with aiofiles.open(self.file_path, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(notification_data) + "\n")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to write file notification: {e}")
            return False
    
    async def _rotate_if_needed(self):
        """Rotate log file if it exceeds maximum size"""
        try:
            if self.file_path.exists() and self.file_path.stat().st_size > self.max_size_bytes:
                # Rotate file
                backup_path = self.file_path.with_suffix(f".{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
                self.file_path.rename(backup_path)
                logger.info(f"Rotated notification log to {backup_path}")
        except Exception as e:
            logger.error(f"Failed to rotate log file: {e}")
    
    async def test_connection(self) -> bool:
        """Test file write access"""
        try:
            test_event = NotificationEvent(
                event_id="test",
                event_type="test",
                message="File notification channel test",
                severity="info"
            )
            return await self.send_notification(test_event)
        except Exception:
            return False

class WebhookNotificationChannel(NotificationChannel):
    """Webhook-based notification channel that sends HTTP POST requests"""
    
    def __init__(self, webhook_url: str, timeout: int = 30, retries: int = 3):
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.retries = retries
        self.client = httpx.AsyncClient(timeout=timeout)
    
    @property
    def channel_name(self) -> str:
        return "webhook"
    
    async def send_notification(self, event: NotificationEvent) -> bool:
        """Send notification via webhook"""
        try:
            # Prepare webhook payload
            payload = {
                "timestamp": event.timestamp.isoformat(),
                "event_id": event.event_id,
                "event_type": event.event_type,
                "severity": event.severity,
                "message": event.message,
                "data": event.data,
                "source": "agentic_graphrag"
            }
            
            # Send with retries
            for attempt in range(self.retries):
                try:
                    response = await self.client.post(
                        self.webhook_url,
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code in [200, 201, 202]:
                        return True
                    else:
                        logger.warning(f"Webhook returned status {response.status_code}: {response.text}")
                        
                except httpx.RequestError as e:
                    logger.warning(f"Webhook attempt {attempt + 1} failed: {e}")
                    if attempt == self.retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test webhook connectivity"""
        try:
            test_payload = {
                "message": "Webhook notification channel test",
                "test": True,
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.client.post(
                self.webhook_url,
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
            
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            logger.error(f"Webhook test failed: {e}")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

class NotificationManager:
    """
    Main notification manager that coordinates multiple notification channels
    and handles user preferences, filtering, and delivery.
    """
    
    def __init__(self, threshold: float = None):
        self.threshold = threshold or config.notifications.threshold
        self.channels: Dict[str, NotificationChannel] = {}
        self.enabled_channels = set(config.notifications.channels)
        self.user_preferences = {}
        self.notification_history = []
        self.stats = {
            "notifications_sent": 0,
            "notifications_failed": 0,
            "channels_active": 0,
            "last_notification": None
        }
        
        # Initialize default channels
        self._initialize_default_channels()
    
    def _initialize_default_channels(self):
        """Initialize default notification channels"""
        # Console channel
        if "console" in self.enabled_channels:
            self.channels["console"] = ConsoleNotificationChannel()
        
        # File channel
        if "file" in self.enabled_channels:
            self.channels["file"] = FileNotificationChannel("logs/notifications.log")
        
        # Webhook channel
        if "webhook" in self.enabled_channels and config.notifications.webhook_url:
            self.channels["webhook"] = WebhookNotificationChannel(config.notifications.webhook_url)
    
    async def process_connections(self, connections: List[DetectedConnection]) -> Dict[str, Any]:
        """
        Process detected connections and trigger notifications for high-relevance ones.
        
        Args:
            connections: List of detected connections
            
        Returns:
            Processing results with notification statistics
        """
        try:
            # Filter high relevance connections
            high_relevance = [
                conn for conn in connections 
                if conn.score.score >= self.threshold
            ]
            
            if not high_relevance:
                return {
                    "status": "no_notifications",
                    "connections_processed": len(connections),
                    "notifications_sent": 0,
                    "threshold": self.threshold
                }
            
            # Create notification events for high relevance connections
            notifications_sent = 0
            
            for connection in high_relevance:
                event = self._create_connection_event(connection)
                success = await self.send_notification(event)
                if success:
                    notifications_sent += 1
            
            return {
                "status": "notifications_sent",
                "connections_processed": len(connections),
                "high_relevance_connections": len(high_relevance),
                "notifications_sent": notifications_sent,
                "threshold": self.threshold
            }
            
        except Exception as e:
            logger.error(f"Error processing connections for notifications: {e}")
            return {
                "status": "error",
                "error": str(e),
                "connections_processed": len(connections),
                "notifications_sent": 0
            }
    
    def _create_connection_event(self, connection: DetectedConnection) -> NotificationEvent:
        """Create a notification event from a detected connection"""
        severity = "info"
        if connection.score.score >= 0.9:
            severity = "critical"
        elif connection.score.score >= 0.8:
            severity = "warning"
        
        return NotificationEvent(
            event_id=f"conn_{hash(connection.source_fact + connection.target_fact)}",
            event_type="high_relevance_connection",
            message=f"High relevance connection detected (score: {connection.score.score:.2f}): {connection.relationship}",
            severity=severity,
            data={
                "source_fact": connection.source_fact,
                "target_fact": connection.target_fact,
                "relationship": connection.relationship,
                "score": connection.score.score,
                "confidence": connection.score.confidence,
                "connection_type": connection.score.connection_type,
                "evidence": connection.evidence,
                "metadata": connection.metadata
            }
        )
    
    async def send_notification(self, event: NotificationEvent) -> bool:
        """
        Send a notification through all enabled channels.
        
        Args:
            event: NotificationEvent to send
            
        Returns:
            True if sent successfully through at least one channel
        """
        if not self.channels:
            logger.warning("No notification channels configured")
            return False
        
        success_count = 0
        total_channels = len(self.channels)
        
        # Send through all channels
        for channel_name, channel in self.channels.items():
            try:
                success = await channel.send_notification(event)
                if success:
                    success_count += 1
                    logger.debug(f"Notification sent successfully via {channel_name}")
                else:
                    logger.warning(f"Failed to send notification via {channel_name}")
                    
            except Exception as e:
                logger.error(f"Error sending notification via {channel_name}: {e}")
        
        # Update statistics
        if success_count > 0:
            self.stats["notifications_sent"] += 1
            self.stats["last_notification"] = datetime.now().isoformat()
            
            # Add to history (keep last 100)
            self.notification_history.append({
                "timestamp": event.timestamp.isoformat(),
                "event_type": event.event_type,
                "message": event.message,
                "channels_sent": success_count,
                "total_channels": total_channels
            })
            if len(self.notification_history) > 100:
                self.notification_history.pop(0)
        else:
            self.stats["notifications_failed"] += 1
        
        return success_count > 0
    
    async def test_all_channels(self) -> Dict[str, bool]:
        """Test all configured notification channels"""
        results = {}
        
        for channel_name, channel in self.channels.items():
            try:
                success = await channel.test_connection()
                results[channel_name] = success
                logger.info(f"Channel {channel_name} test: {'PASS' if success else 'FAIL'}")
            except Exception as e:
                results[channel_name] = False
                logger.error(f"Channel {channel_name} test failed: {e}")
        
        return results
    
    def add_channel(self, name: str, channel: NotificationChannel):
        """Add a custom notification channel"""
        self.channels[name] = channel
        logger.info(f"Added notification channel: {name}")
    
    def remove_channel(self, name: str):
        """Remove a notification channel"""
        if name in self.channels:
            del self.channels[name]
            logger.info(f"Removed notification channel: {name}")
    
    def set_threshold(self, threshold: float):
        """Set the notification threshold"""
        if 0.0 <= threshold <= 1.0:
            self.threshold = threshold
            logger.info(f"Notification threshold set to {threshold}")
        else:
            raise ValueError("Threshold must be between 0.0 and 1.0")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get notification statistics"""
        return {
            **self.stats,
            "channels_configured": len(self.channels),
            "enabled_channels": list(self.enabled_channels),
            "current_threshold": self.threshold,
            "recent_notifications": self.notification_history[-10:]  # Last 10
        }
    
    def get_notification_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent notification history"""
        return self.notification_history[-limit:]
    
    async def cleanup(self):
        """Clean up resources"""
        for channel in self.channels.values():
            if hasattr(channel, 'close'):
                try:
                    await channel.close()
                except Exception as e:
                    logger.error(f"Error closing channel: {e}")

# Global notification manager instance
notification_manager = NotificationManager()
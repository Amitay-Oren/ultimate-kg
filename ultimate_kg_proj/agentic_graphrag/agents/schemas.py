"""
Pydantic schemas for structured agent outputs in the Agentic GraphRAG system.

These schemas define the structure for fact extraction, connection detection,
and other structured outputs from the multi-agent pipeline.
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

class DataFormat(str, Enum):
    """Supported data formats for processing"""
    TEXT = "text"
    JSON = "json"
    PDF = "pdf"
    CSV = "csv"
    HTML = "html"
    MARKDOWN = "md"
    XML = "xml"

class ProcessingStatus(str, Enum):
    """Processing status values"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

class FactType(str, Enum):
    """Types of facts that can be extracted"""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    EVENT = "event"
    CONCEPT = "concept"
    RELATIONSHIP = "relationship"
    TEMPORAL = "temporal"
    NUMERIC = "numeric"
    OTHER = "other"

class ExtractedFact(BaseModel):
    """Schema for individual extracted facts"""
    fact: str = Field(description="The extracted fact as a clear statement")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score for the fact")
    fact_type: FactType = Field(description="Type/category of the fact")
    entities: List[str] = Field(default_factory=list, description="Key entities mentioned in the fact")
    source_context: Optional[str] = Field(None, description="Original context where fact was found")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class FactExtractionOutput(BaseModel):
    """Schema for fact extraction results"""
    facts: List[ExtractedFact] = Field(description="List of extracted facts")
    total_facts: int = Field(description="Total number of facts extracted")
    processing_time: float = Field(description="Time taken for extraction in seconds")
    data_format: DataFormat = Field(description="Format of the processed data")
    extraction_method: str = Field(description="Method used for extraction")
    status: ProcessingStatus = Field(description="Processing status")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    
    @validator('total_facts')
    def validate_total_facts(cls, v, values):
        if 'facts' in values and v != len(values['facts']):
            raise ValueError('total_facts must match the length of facts list')
        return v

class ConnectionScore(BaseModel):
    """Schema for connection relevance scoring"""
    score: float = Field(ge=0.0, le=1.0, description="Relevance score between 0 and 1")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the score")
    reasoning: str = Field(description="Explanation for the score")
    connection_type: str = Field(description="Type of connection (semantic, factual, temporal, etc.)")

class DetectedConnection(BaseModel):
    """Schema for detected connections between knowledge elements"""
    source_fact: str = Field(description="Source fact or knowledge element")
    target_fact: str = Field(description="Target fact or knowledge element")
    relationship: str = Field(description="Description of the relationship")
    score: ConnectionScore = Field(description="Relevance scoring details")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence for the connection")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional connection metadata")

class ConnectionDetectionOutput(BaseModel):
    """Schema for connection detection results"""
    connections: List[DetectedConnection] = Field(description="List of detected connections")
    total_connections: int = Field(description="Total number of connections found")
    high_relevance_connections: List[DetectedConnection] = Field(
        default_factory=list, 
        description="Connections above relevance threshold"
    )
    threshold_used: float = Field(description="Relevance threshold applied")
    processing_time: float = Field(description="Time taken for detection in seconds")
    status: ProcessingStatus = Field(description="Processing status")
    
    @validator('total_connections')
    def validate_total_connections(cls, v, values):
        if 'connections' in values and v != len(values['connections']):
            raise ValueError('total_connections must match the length of connections list')
        return v

class SearchResult(BaseModel):
    """Schema for knowledge search results"""
    content: str = Field(description="The content/text of the result")
    score: float = Field(ge=0.0, le=1.0, description="Relevance score for the result")
    source: str = Field(description="Source of the result (database, document, etc.)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional result metadata")
    snippet: Optional[str] = Field(None, description="Highlighted snippet from the content")
    entities: List[str] = Field(default_factory=list, description="Key entities in the result")

class SearchOutput(BaseModel):
    """Schema for search operation results"""
    results: List[SearchResult] = Field(description="List of search results")
    total_count: int = Field(description="Total number of results found")
    search_time: float = Field(description="Time taken for search in seconds")
    search_type: str = Field(description="Type of search performed")
    query: str = Field(description="Original search query")
    related_concepts: List[str] = Field(default_factory=list, description="Related concepts found")
    status: ProcessingStatus = Field(description="Search status")

class ProcessingRequest(BaseModel):
    """Schema for data processing requests"""
    data: str = Field(description="Data to be processed")
    format: DataFormat = Field(description="Format of the data")
    options: Dict[str, Any] = Field(default_factory=dict, description="Processing options")
    extract_facts: bool = Field(default=True, description="Whether to extract facts")
    detect_connections: bool = Field(default=True, description="Whether to detect connections")
    notify_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Notification threshold")

class ProcessingResponse(BaseModel):
    """Schema for data processing responses"""
    status: ProcessingStatus = Field(description="Overall processing status")
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    facts_extracted: int = Field(default=0, description="Number of facts extracted")
    connections_found: int = Field(default=0, description="Number of connections detected")
    notifications_sent: int = Field(default=0, description="Number of notifications triggered")
    processing_time: float = Field(description="Total processing time in seconds")
    processed_at: datetime = Field(default_factory=datetime.now, description="When processing completed")
    
    fact_extraction: Optional[FactExtractionOutput] = Field(None, description="Detailed fact extraction results")
    connection_detection: Optional[ConnectionDetectionOutput] = Field(None, description="Detailed connection detection results")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    warnings: List[str] = Field(default_factory=list, description="Any warnings generated")

class AgentStatus(BaseModel):
    """Schema for agent status information"""
    name: str = Field(description="Agent name")
    initialized: bool = Field(description="Whether agent is initialized")
    active: bool = Field(description="Whether agent is currently active")
    requests_processed: int = Field(default=0, description="Number of requests processed")
    last_activity: Optional[datetime] = Field(None, description="Timestamp of last activity")
    errors: int = Field(default=0, description="Number of errors encountered")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")

class SystemStatus(BaseModel):
    """Schema for overall system status"""
    status: str = Field(description="Overall system status")
    uptime: float = Field(description="System uptime in seconds")
    version: str = Field(description="System version")
    agents: List[AgentStatus] = Field(default_factory=list, description="Status of all agents")
    database_status: Dict[str, str] = Field(default_factory=dict, description="Database connection status")
    mcp_server_status: str = Field(description="MCP server connection status")
    a2a_server_status: str = Field(description="A2A server status")
    requests_processed: int = Field(default=0, description="Total requests processed")
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")

class NotificationEvent(BaseModel):
    """Schema for notification events"""
    event_id: str = Field(description="Unique event identifier")
    event_type: str = Field(description="Type of notification event")
    message: str = Field(description="Notification message")
    severity: str = Field(description="Severity level (info, warning, error, critical)")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    timestamp: datetime = Field(default_factory=datetime.now, description="When event occurred")
    channels: List[str] = Field(default_factory=list, description="Channels to notify")
    sent: bool = Field(default=False, description="Whether notification was sent")

# Utility schemas for pipeline coordination
class PipelineStage(BaseModel):
    """Schema for pipeline stage information"""
    stage_name: str = Field(description="Name of the pipeline stage")
    status: ProcessingStatus = Field(description="Status of this stage")
    start_time: Optional[datetime] = Field(None, description="When stage started")
    end_time: Optional[datetime] = Field(None, description="When stage completed")
    output: Optional[Dict[str, Any]] = Field(None, description="Stage output data")
    errors: List[str] = Field(default_factory=list, description="Stage errors")

class PipelineExecution(BaseModel):
    """Schema for complete pipeline execution tracking"""
    pipeline_id: str = Field(description="Unique pipeline execution ID")
    stages: List[PipelineStage] = Field(description="All pipeline stages")
    overall_status: ProcessingStatus = Field(description="Overall pipeline status")
    start_time: datetime = Field(default_factory=datetime.now, description="Pipeline start time")
    end_time: Optional[datetime] = Field(None, description="Pipeline end time")
    total_time: Optional[float] = Field(None, description="Total execution time")
    final_output: Optional[ProcessingResponse] = Field(None, description="Final pipeline output")
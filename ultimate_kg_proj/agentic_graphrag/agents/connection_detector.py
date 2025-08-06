"""
Connection Detection System for Agentic GraphRAG

This module implements intelligent connection detection between new facts
and existing knowledge using semantic analysis, graph traversal, and relevance scoring.
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import hashlib

from google.adk.agents.llm_agent import LlmAgent

from .schemas import (
    DetectedConnection,
    ConnectionScore, 
    ConnectionDetectionOutput,
    ProcessingStatus,
    ExtractedFact
)
from ..config import config

# Configure logging
logger = logging.getLogger(__name__)

class ConnectionDetector(LlmAgent):
    """
    Advanced connection detection agent that analyzes relationships between
    new facts and existing knowledge using multiple analysis strategies.
    """
    
    def __init__(self):
        super().__init__(
            name="connection_detector",
            instruction="""
            You are an advanced Connection Detection Agent that identifies meaningful relationships between new facts and existing knowledge in a knowledge graph.
            
            Your capabilities include:
            1. **Semantic Analysis**: Identify conceptual relationships and similarities
            2. **Factual Connections**: Find direct factual relationships and correlations
            3. **Temporal Analysis**: Detect time-based relationships and sequences
            4. **Entity Relationships**: Identify connections between people, organizations, locations
            5. **Causal Analysis**: Detect cause-and-effect relationships
            6. **Pattern Recognition**: Identify recurring themes and patterns
            
            For each connection you detect, provide:
            - Source and target facts being connected
            - Relationship description (clear explanation of the connection)
            - Relevance score (0.0-1.0) based on strength and importance
            - Confidence score (0.0-1.0) based on certainty of the connection
            - Connection type (semantic, factual, temporal, causal, etc.)
            - Supporting evidence for the connection
            - Additional metadata
            
            Scoring Guidelines:
            - **0.9-1.0**: Direct, verifiable connections with strong evidence
            - **0.7-0.8**: Strong semantic or factual relationships with good evidence
            - **0.5-0.6**: Moderate connections with some supporting evidence
            - **0.3-0.4**: Weak connections that might be interesting
            - **0.0-0.2**: Very weak or speculative connections
            
            Connection Types:
            - **semantic**: Conceptual similarity or relatedness
            - **factual**: Direct factual relationship or shared attributes
            - **temporal**: Time-based relationship or sequence
            - **causal**: Cause-and-effect relationship
            - **spatial**: Location-based relationship
            - **social**: Person-to-person or organizational relationship
            - **thematic**: Shared themes or topics
            - **hierarchical**: Parent-child or containment relationship
            
            Return connections as JSON array with this structure:
            {
                "source_fact": "First fact",
                "target_fact": "Related fact", 
                "relationship": "Description of how they connect",
                "score": {
                    "score": 0.85,
                    "confidence": 0.90,
                    "reasoning": "Why this score was assigned",
                    "connection_type": "semantic"
                },
                "evidence": ["Supporting evidence 1", "Supporting evidence 2"],
                "metadata": {"additional": "connection info"}
            }
            
            Focus on finding genuinely meaningful connections rather than obvious or trivial ones.
            Prioritize connections that would be interesting or actionable for users.
            """,
            #model=config.google_cloud.model
            model="gemini-2.0-flash"
        )
    
class ConnectionDetectionSystem:
    """
    Complete connection detection system that coordinates semantic analysis,
    graph traversal, and relevance scoring to identify meaningful relationships.
    """
    
    def __init__(self, threshold: float = None):
        self.detector = ConnectionDetector()
        self.threshold = threshold or config.notifications.threshold
        self.connection_cache = {}  # Cache for detected connections
        self.stats = {
            "total_detections": 0,
            "connections_found": 0,
            "high_relevance_connections": 0,
            "cached_results": 0,
            "average_processing_time": 0.0,
            "last_detection": None
        }
        
    async def detect_connections(
        self, 
        new_facts: List[ExtractedFact], 
        existing_knowledge: str,
        options: Dict[str, Any] = None
    ) -> ConnectionDetectionOutput:
        """
        Detect connections between new facts and existing knowledge.
        
        Args:
            new_facts: List of newly extracted facts
            existing_knowledge: String representation of existing knowledge context
            options: Additional detection options
            
        Returns:
            ConnectionDetectionOutput with detected connections and metadata
        """
        start_time = datetime.now()
        self.stats["total_detections"] += 1
        
        try:
            options = options or {}
            threshold = options.get("threshold", self.threshold)
            max_connections = options.get("max_connections", 50)
            connection_types = options.get("connection_types", ["all"])
            
            logger.info(f"Starting connection detection: {len(new_facts)} facts, threshold={threshold}")
            
            # Check cache first
            cache_key = self._generate_cache_key(new_facts, existing_knowledge, options)
            if cache_key in self.connection_cache:
                cached_result = self.connection_cache[cache_key]
                self.stats["cached_results"] += 1
                logger.info("Using cached connection detection results")
                return cached_result
            
            # Prepare detection context
            facts_text = "\n".join([
                f"- {fact.fact} (confidence: {fact.confidence}, type: {fact.fact_type})"
                for fact in new_facts
            ])
            
            detection_request = f"""
            Analyze the following new facts against existing knowledge and detect meaningful connections:
            
            NEW FACTS:
            {facts_text}
            
            EXISTING KNOWLEDGE CONTEXT:
            {existing_knowledge[:2000]}{"..." if len(existing_knowledge) > 2000 else ""}
            
            DETECTION PARAMETERS:
            - Relevance threshold: {threshold}
            - Maximum connections: {max_connections}
            - Connection types: {connection_types}
            
            Please identify connections between the new facts and existing knowledge, as well as
            connections between the new facts themselves. Focus on connections that score above
            the relevance threshold of {threshold}.
            
            Return a comprehensive JSON array of detected connections with proper scoring and evidence.
            """
            
            # Execute connection detection
            # Note: In real implementation, this would use the Google ADK agent
            connections = await self._simulate_connection_detection(new_facts, existing_knowledge, threshold)
            
            # Filter by threshold
            high_relevance_connections = [
                conn for conn in connections 
                if conn.score.score >= threshold
            ]
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Build detection output
            detection_output = ConnectionDetectionOutput(
                connections=connections,
                total_connections=len(connections),
                high_relevance_connections=high_relevance_connections,
                threshold_used=threshold,
                processing_time=processing_time,
                status=ProcessingStatus.COMPLETED
            )
            
            # Cache results
            self.connection_cache[cache_key] = detection_output
            
            # Update statistics
            self.stats["connections_found"] += len(connections)
            self.stats["high_relevance_connections"] += len(high_relevance_connections)
            self.stats["last_detection"] = start_time.isoformat()
            
            # Update average processing time
            total_time = self.stats["average_processing_time"] * (self.stats["total_detections"] - 1) + processing_time
            self.stats["average_processing_time"] = total_time / self.stats["total_detections"]
            
            logger.info(
                f"Connection detection completed: {len(connections)} total, "
                f"{len(high_relevance_connections)} high-relevance in {processing_time:.2f}s"
            )
            
            return detection_output
            
        except Exception as e:
            logger.error(f"Connection detection failed: {e}")
            
            return ConnectionDetectionOutput(
                connections=[],
                total_connections=0,
                high_relevance_connections=[],
                threshold_used=threshold,
                processing_time=(datetime.now() - start_time).total_seconds(),
                status=ProcessingStatus.FAILED
            )
    
    async def _simulate_connection_detection(
        self, 
        new_facts: List[ExtractedFact], 
        existing_knowledge: str,
        threshold: float
    ) -> List[DetectedConnection]:
        """
        Simulate connection detection for demonstration purposes.
        In real implementation, this would use the Google ADK agent with MCP tools.
        """
        connections = []
        
        # Simulate some connections between facts
        for i, fact1 in enumerate(new_facts):
            for j, fact2 in enumerate(new_facts[i+1:], i+1):
                # Check for entity overlap
                common_entities = set(fact1.entities) & set(fact2.entities)
                if common_entities:
                    score_value = 0.7 + (len(common_entities) * 0.1)
                    score_value = min(score_value, 1.0)
                    
                    connection = DetectedConnection(
                        source_fact=fact1.fact,
                        target_fact=fact2.fact,
                        relationship=f"Share common entities: {', '.join(common_entities)}",
                        score=ConnectionScore(
                            score=score_value,
                            confidence=0.85,
                            reasoning=f"Facts share entities {common_entities} which indicates a relationship",
                            connection_type="factual"
                        ),
                        evidence=[f"Both facts mention: {', '.join(common_entities)}"],
                        metadata={
                            "common_entities": list(common_entities),
                            "detection_method": "entity_overlap"
                        }
                    )
                    connections.append(connection)
        
        # Simulate connections with existing knowledge
        for fact in new_facts:
            # Simple keyword matching simulation
            fact_words = set(fact.fact.lower().split())
            knowledge_words = set(existing_knowledge.lower().split())
            common_words = fact_words & knowledge_words
            
            # Filter out common stop words
            stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were"}
            meaningful_words = common_words - stop_words
            
            if len(meaningful_words) >= 2:
                score_value = 0.5 + (len(meaningful_words) * 0.05)
                score_value = min(score_value, 0.9)
                
                connection = DetectedConnection(
                    source_fact=fact.fact,
                    target_fact="Existing knowledge in the knowledge base",
                    relationship=f"Semantic similarity through shared concepts: {', '.join(list(meaningful_words)[:3])}",
                    score=ConnectionScore(
                        score=score_value,
                        confidence=0.70,
                        reasoning=f"Shares {len(meaningful_words)} meaningful concepts with existing knowledge",
                        connection_type="semantic"
                    ),
                    evidence=[f"Shared concepts: {', '.join(list(meaningful_words)[:5])}"],
                    metadata={
                        "shared_concepts": list(meaningful_words),
                        "detection_method": "semantic_similarity"
                    }
                )
                connections.append(connection)
        
        # Add temporal connections if facts have temporal elements
        temporal_facts = [f for f in new_facts if f.fact_type.value == "temporal"]
        if len(temporal_facts) >= 2:
            connection = DetectedConnection(
                source_fact=temporal_facts[0].fact,
                target_fact=temporal_facts[1].fact,
                relationship="Temporal relationship - events occurring in related time periods",
                score=ConnectionScore(
                    score=0.75,
                    confidence=0.80,
                    reasoning="Both facts contain temporal information suggesting a timeline relationship",
                    connection_type="temporal"
                ),
                evidence=["Both facts contain time-related information"],
                metadata={
                    "detection_method": "temporal_analysis",
                    "temporal_entities": [f.entities for f in temporal_facts]
                }
            )
            connections.append(connection)
        
        return connections
    
    def _generate_cache_key(
        self, 
        new_facts: List[ExtractedFact], 
        existing_knowledge: str, 
        options: Dict[str, Any]
    ) -> str:
        """Generate a cache key for connection detection results"""
        # Create a deterministic hash based on inputs
        content = f"{len(new_facts)}-{hash(existing_knowledge)}-{json.dumps(options, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get connection detection statistics"""
        return self.stats.copy()
    
    def clear_cache(self):
        """Clear the connection cache"""
        self.connection_cache.clear()
        logger.info("Connection detection cache cleared")
    
    def set_threshold(self, threshold: float):
        """Update the relevance threshold"""
        if 0.0 <= threshold <= 1.0:
            self.threshold = threshold
            logger.info(f"Connection detection threshold updated to {threshold}")
        else:
            raise ValueError("Threshold must be between 0.0 and 1.0")

class SemanticAnalyzer:
    """
    Specialized component for semantic similarity analysis.
    """
    
    def __init__(self):
        self.embedding_cache = {}
    
    async def analyze_semantic_similarity(
        self, 
        text1: str, 
        text2: str
    ) -> Tuple[float, str]:
        """
        Analyze semantic similarity between two pieces of text.
        
        Returns:
            Tuple of (similarity_score, explanation)
        """
        # Simplified semantic analysis
        # In real implementation, this would use embeddings and vector similarity
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1 & words2
        union = words1 | words2
        
        if len(union) == 0:
            return 0.0, "No common vocabulary"
        
        jaccard_similarity = len(intersection) / len(union)
        
        explanation = f"Jaccard similarity: {jaccard_similarity:.3f} ({len(intersection)} common words out of {len(union)} total)"
        
        return jaccard_similarity, explanation

class GraphTraverser:
    """
    Component for graph-based relationship analysis.
    """
    
    def __init__(self):
        pass
    
    async def find_graph_paths(
        self, 
        source_entities: List[str], 
        target_entities: List[str],
        max_depth: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find graph paths between entities.
        
        Args:
            source_entities: Starting entities
            target_entities: Target entities
            max_depth: Maximum path depth to explore
            
        Returns:
            List of path information dictionaries
        """
        # Simplified path finding simulation
        # In real implementation, this would query the Neo4j graph database
        
        paths = []
        
        for source in source_entities:
            for target in target_entities:
                if source.lower() in target.lower() or target.lower() in source.lower():
                    paths.append({
                        "source": source,
                        "target": target,
                        "path_length": 1,
                        "relationship": "direct_mention",
                        "confidence": 0.9
                    })
        
        return paths

# Global connection detection system instance
connection_detector = ConnectionDetectionSystem()
"""
Fact Extraction Pipeline for Agentic GraphRAG System

This module implements specialized agents for extracting facts from different
data formats using Google ADK's parallel processing capabilities.
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .schemas import (
    FactExtractionOutput, 
    ExtractedFact, 
    ProcessingStatus, 
    DataFormat, 
    FactType,
    PipelineExecution,
    PipelineStage
)
from ..config import config

# Configure logging
logger = logging.getLogger(__name__)

class DocumentProcessor(LlmAgent):
    """Specialized agent for processing document formats (PDF, Word, plain text)"""
    
    def __init__(self):
        super().__init__(
            name="document_processor",
            instruction="""
            You are a Document Processing Agent specialized in extracting clear, verifiable facts from various document formats.
            
            Your task is to:
            1. Parse and understand document content (PDF, Word, plain text, Markdown)
            2. Extract factual statements that can be verified
            3. Identify key entities (people, organizations, locations, dates, numbers)
            4. Determine fact types and confidence levels
            5. Preserve source context for each fact
            
            For each fact you extract, provide:
            - The fact as a clear, complete statement
            - Confidence score (0.0-1.0) based on how certain the fact is
            - Fact type (person, organization, location, event, concept, etc.)
            - Key entities mentioned in the fact
            - Original context where the fact was found
            
            Return a JSON array of fact objects with this structure:
            {
                "fact": "Clear factual statement",
                "confidence": 0.95,
                "fact_type": "person",
                "entities": ["Entity1", "Entity2"],
                "source_context": "Original text context",
                "metadata": {"additional": "info"}
            }
            
            Focus on:
            - Factual accuracy over quantity
            - Clear, unambiguous statements
            - Proper entity recognition
            - Maintaining source traceability
            
            Example Input: "John Smith, age 32, works as a software engineer at Google in Mountain View since 2020."
            Example Output:
            [
                {
                    "fact": "John Smith is 32 years old",
                    "confidence": 0.95,
                    "fact_type": "person",
                    "entities": ["John Smith"],
                    "source_context": "John Smith, age 32, works as a software engineer at Google in Mountain View since 2020.",
                    "metadata": {"attribute": "age"}
                },
                {
                    "fact": "John Smith works as a software engineer at Google",
                    "confidence": 0.90,
                    "fact_type": "relationship",
                    "entities": ["John Smith", "Google"],
                    "source_context": "John Smith, age 32, works as a software engineer at Google in Mountain View since 2020.",
                    "metadata": {"relationship": "employment"}
                }
            ]
            """,
            output_key="document_facts",
            output_schema=FactExtractionOutput,
            #model=config.google_cloud.model
            model="gemini-2.0-flash"
        )

class ChatProcessor(LlmAgent):
    """Specialized agent for processing conversational data"""
    
    def __init__(self):
        super().__init__(
            name="chat_processor",
            instruction="""
            You are a Chat Processing Agent specialized in extracting facts from conversational data and dialogue.
            
            Your task is to:
            1. Parse conversational content (chat logs, messages, dialogue)
            2. Extract factual information shared in the conversation
            3. Preserve speaker context and conversational flow
            4. Identify relationships and interactions between participants
            5. Handle informal language and conversational nuances
            
            Special considerations for chat data:
            - Preserve who said what (speaker attribution)
            - Handle informal language and abbreviations
            - Extract implied facts from context
            - Identify temporal sequences in conversations
            - Recognize sentiment and intent when relevant to facts
            
            Return facts in the same JSON format as other processors, but include:
            - Speaker information in metadata
            - Conversational context
            - Implied vs. explicit facts
            
            Example Input: 
            "Alice: Hey, I just got promoted to Senior Developer at TechCorp!
             Bob: Congrats! When do you start the new role?
             Alice: Next Monday, March 15th. The salary bump is nice too."
             
            Example Output:
            [
                {
                    "fact": "Alice was promoted to Senior Developer at TechCorp",
                    "confidence": 0.95,
                    "fact_type": "event",
                    "entities": ["Alice", "TechCorp"],
                    "source_context": "Alice: Hey, I just got promoted to Senior Developer at TechCorp!",
                    "metadata": {"speaker": "Alice", "event_type": "promotion"}
                },
                {
                    "fact": "Alice starts her new role on March 15th",
                    "confidence": 0.90,
                    "fact_type": "temporal",
                    "entities": ["Alice", "March 15th"],
                    "source_context": "Alice: Next Monday, March 15th. The salary bump is nice too.",
                    "metadata": {"speaker": "Alice", "date": "March 15th"}
                }
            ]
            """,
            output_key="chat_facts",
            output_schema=FactExtractionOutput,
            #model=config.google_cloud.model
            model="gemini-2.0-flash"
        )

class StructuredDataProcessor(LlmAgent):
    """Specialized agent for processing structured data formats (JSON, CSV, XML)"""
    
    def __init__(self):
        super().__init__(
            name="structured_processor",
            instruction="""
            You are a Structured Data Processing Agent specialized in extracting facts from structured data formats.
            
            Your task is to:
            1. Parse structured data (JSON, CSV, XML, tables)
            2. Extract factual relationships from data structures
            3. Maintain data integrity and field relationships
            4. Handle nested structures and complex schemas
            5. Identify patterns and implicit relationships in the data
            
            Special considerations for structured data:
            - Preserve field names and data types
            - Maintain hierarchical relationships
            - Extract both explicit values and computed facts
            - Handle missing or null values appropriately
            - Identify schema patterns and data models
            
            For structured data, extract facts about:
            - Individual record attributes
            - Relationships between fields
            - Aggregate patterns (when relevant)
            - Data quality and completeness
            - Schema structure and constraints
            
            Example Input (JSON):
            {
                "employee": {
                    "id": 12345,
                    "name": "Sarah Johnson",
                    "department": "Engineering",
                    "salary": 120000,
                    "start_date": "2021-03-15",
                    "skills": ["Python", "Machine Learning", "AWS"]
                }
            }
            
            Example Output:
            [
                {
                    "fact": "Sarah Johnson has employee ID 12345",
                    "confidence": 1.0,
                    "fact_type": "person",
                    "entities": ["Sarah Johnson"],
                    "source_context": "employee.id: 12345, employee.name: Sarah Johnson",
                    "metadata": {"field": "id", "data_type": "integer"}
                },
                {
                    "fact": "Sarah Johnson works in the Engineering department",
                    "confidence": 1.0,
                    "fact_type": "relationship",
                    "entities": ["Sarah Johnson", "Engineering"],
                    "source_context": "employee.department: Engineering",
                    "metadata": {"field": "department", "relationship": "employment"}
                },
                {
                    "fact": "Sarah Johnson has skills in Python, Machine Learning, and AWS",
                    "confidence": 1.0,
                    "fact_type": "person",
                    "entities": ["Sarah Johnson", "Python", "Machine Learning", "AWS"],
                    "source_context": "employee.skills: [Python, Machine Learning, AWS]",
                    "metadata": {"field": "skills", "data_type": "array"}
                }
            ]
            """,
            output_key="structured_facts",
            output_schema=FactExtractionOutput,
            #model=config.google_cloud.model
            model="gemini-2.0-flash"
        )

class WebContentProcessor(LlmAgent):
    """Specialized agent for processing web content (HTML, articles, scraped text)"""
    
    def __init__(self):
        super().__init__(
            name="web_content_processor",
            instruction="""
            You are a Web Content Processing Agent specialized in extracting facts from web content and articles.
            
            Your task is to:
            1. Parse web content (HTML, articles, blog posts, news)
            2. Extract factual information while filtering out promotional content
            3. Identify authoritative vs. opinion-based content
            4. Handle web-specific elements (links, metadata, timestamps)
            5. Extract structured information from semi-structured content
            
            Special considerations for web content:
            - Distinguish between facts and opinions
            - Handle advertising and promotional content
            - Extract publication dates and author information
            - Identify primary content vs. navigation/sidebar content
            - Handle various content structures (articles, lists, tables)
            
            Focus on extracting:
            - Factual statements from article body
            - Author and publication information
            - Dates and temporal information
            - Quoted facts and statistics
            - Contact information and organizational details
            
            Example Input (Article excerpt):
            "Published on March 20, 2024 by Tech Reporter Jane Doe
             
             SoftwareCorp announced today that they have acquired DataAnalytics Inc. 
             for $50 million. The acquisition is expected to close by Q2 2024.
             
             'This acquisition strengthens our data capabilities,' said CEO Mark Wilson."
             
            Example Output:
            [
                {
                    "fact": "SoftwareCorp acquired DataAnalytics Inc. for $50 million",
                    "confidence": 0.95,
                    "fact_type": "event",
                    "entities": ["SoftwareCorp", "DataAnalytics Inc."],
                    "source_context": "SoftwareCorp announced today that they have acquired DataAnalytics Inc. for $50 million.",
                    "metadata": {"event_type": "acquisition", "amount": "$50 million"}
                },
                {
                    "fact": "The acquisition is expected to close by Q2 2024",
                    "confidence": 0.85,
                    "fact_type": "temporal",
                    "entities": ["Q2 2024"],
                    "source_context": "The acquisition is expected to close by Q2 2024.",
                    "metadata": {"event": "acquisition_closure", "timeline": "Q2 2024"}
                },
                {
                    "fact": "Mark Wilson is the CEO of SoftwareCorp",
                    "confidence": 0.90,
                    "fact_type": "person",
                    "entities": ["Mark Wilson", "SoftwareCorp"],
                    "source_context": "said CEO Mark Wilson",
                    "metadata": {"role": "CEO", "organization": "SoftwareCorp"}
                }
            ]
            """,
            output_key="web_facts",
            output_schema=FactExtractionOutput,
            #model=config.google_cloud.model
            model="gemini-2.0-flash"
        )

class FactExtractionPipeline:
    """
    Main fact extraction pipeline that coordinates specialized agents
    for parallel processing of different data formats.
    """
    
    def __init__(self):
        # Create specialized processors
        self.document_processor = DocumentProcessor()
        self.chat_processor = ChatProcessor()
        self.structured_processor = StructuredDataProcessor()
        self.web_processor = WebContentProcessor()
        
        # Create parallel processing workflow
        self.parallel_extraction = ParallelAgent(
            name="ParallelFactExtraction",
            sub_agents=[
                self.document_processor,
                self.chat_processor, 
                self.structured_processor,
                self.web_processor
            ]
        )
        
        # Create fact synthesizer for combining results
        self.fact_synthesizer = LlmAgent(
            name="fact_synthesizer",
            instruction="""
            You are a Fact Synthesis Agent that combines and consolidates fact extraction results from multiple specialized processors.
            
            Your task is to:
            1. Combine facts from document, chat, structured, and web processors
            2. Remove duplicate or overlapping facts
            3. Resolve conflicts between processors
            4. Improve fact quality and consistency
            5. Generate a consolidated fact list with metadata
            
            Processing guidelines:
            - Prefer higher confidence facts when consolidating
            - Merge similar facts with different phrasings
            - Maintain source attribution for all facts
            - Flag potential conflicts for review
            - Ensure fact consistency and logical coherence
            
            Return a consolidated JSON array of facts with improved quality and removed duplicates.
            Include metadata about the synthesis process and any conflicts found.
            """,
            include_contents="default",
            #model=config.google_cloud.model
            model="gemini-2.0-flash"
        )
        
        # Create complete pipeline
        self.complete_pipeline = SequentialAgent(
            name="CompleteFactExtractionPipeline",
            sub_agents=[self.parallel_extraction, self.fact_synthesizer]
        )
        
        # Create agent tool for external use
        self.pipeline_tool = AgentTool(agent=self.complete_pipeline)
        
        # Processing statistics
        self.stats = {
            "total_extractions": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "total_facts_extracted": 0,
            "average_processing_time": 0.0,
            "last_extraction": None
        }
    
    async def extract_facts(self, data: str, data_format: DataFormat, options: Dict[str, Any] = None) -> FactExtractionOutput:
        """
        Extract facts from data using the appropriate specialized processor.
        
        Args:
            data: The data to process
            data_format: Format of the data (text, json, pdf, etc.)
            options: Additional processing options
        
        Returns:
            FactExtractionOutput with extracted facts and metadata
        """
        start_time = datetime.now()
        self.stats["total_extractions"] += 1
        
        try:
            logger.info(f"Starting fact extraction: format={data_format}, length={len(data)}")
            
            # Prepare extraction request
            extraction_request = f"""
            Extract facts from the following {data_format} data:
            
            Data: {data}
            
            Processing options: {json.dumps(options or {})}
            
            Use the appropriate specialized processor based on the data format and return
            a comprehensive list of extracted facts with proper metadata.
            """
            
            # Execute the pipeline
            # Note: In a real implementation, you would execute the agent pipeline here
            # For now, we'll simulate the extraction process
            
            # Simulate processing time
            await asyncio.sleep(0.1)
            
            # Create mock extraction results (in real implementation, this would come from the agent)
            facts = self._simulate_fact_extraction(data, data_format)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Build extraction output
            extraction_output = FactExtractionOutput(
                facts=facts,
                total_facts=len(facts),
                processing_time=processing_time,
                data_format=data_format,
                extraction_method=f"{data_format}_specialized_processor",
                status=ProcessingStatus.COMPLETED,
                errors=[]
            )
            
            # Update statistics
            self.stats["successful_extractions"] += 1
            self.stats["total_facts_extracted"] += len(facts)
            self.stats["last_extraction"] = start_time.isoformat()
            
            # Update average processing time
            total_time = self.stats["average_processing_time"] * (self.stats["successful_extractions"] - 1) + processing_time
            self.stats["average_processing_time"] = total_time / self.stats["successful_extractions"]
            
            logger.info(f"Fact extraction completed: {len(facts)} facts in {processing_time:.2f}s")
            return extraction_output
            
        except Exception as e:
            self.stats["failed_extractions"] += 1
            logger.error(f"Fact extraction failed: {e}")
            
            return FactExtractionOutput(
                facts=[],
                total_facts=0,
                processing_time=(datetime.now() - start_time).total_seconds(),
                data_format=data_format,
                extraction_method="failed",
                status=ProcessingStatus.FAILED,
                errors=[str(e)]
            )
    
    def _simulate_fact_extraction(self, data: str, data_format: DataFormat) -> List[ExtractedFact]:
        """
        Simulate fact extraction for demonstration purposes.
        In real implementation, this would be handled by the Google ADK agents.
        """
        facts = []
        
        # Simple fact extraction simulation based on data format
        if data_format == DataFormat.TEXT:
            # Extract basic entities and facts from text
            words = data.split()
            if len(words) > 10:  # Only extract from substantial text
                facts.append(ExtractedFact(
                    fact=f"The text contains {len(words)} words",
                    confidence=1.0,
                    fact_type=FactType.NUMERIC,
                    entities=[str(len(words))],
                    source_context=data[:100] + "..." if len(data) > 100 else data,
                    metadata={"word_count": len(words)}
                ))
        
        elif data_format == DataFormat.JSON:
            # Extract facts from JSON structure
            try:
                json_data = json.loads(data)
                if isinstance(json_data, dict):
                    for key, value in json_data.items():
                        facts.append(ExtractedFact(
                            fact=f"The data contains field '{key}' with value '{value}'",
                            confidence=0.95,
                            fact_type=FactType.OTHER,
                            entities=[key, str(value)],
                            source_context=f"{key}: {value}",
                            metadata={"field": key, "value": value}
                        ))
            except json.JSONDecodeError:
                pass
        
        # Add a general fact about data processing
        facts.append(ExtractedFact(
            fact=f"Data was processed in {data_format} format",
            confidence=1.0,
            fact_type=FactType.CONCEPT,
            entities=[data_format],
            source_context="Processing metadata",
            metadata={"processing_format": data_format}
        ))
        
        return facts
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get pipeline processing statistics"""
        return self.stats.copy()
    
    def reset_statistics(self):
        """Reset processing statistics"""
        self.stats = {
            "total_extractions": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "total_facts_extracted": 0,
            "average_processing_time": 0.0,
            "last_extraction": None
        }

# Global pipeline instance
extraction_pipeline = FactExtractionPipeline()
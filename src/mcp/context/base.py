from __future__ import annotations
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class ContextMetadata(BaseModel):
    """
    Represents metadata for a context object in the Model Context Protocol.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    source: Optional[str] = None
    version: str = "1.0.0"
    tags: Dict[str, Any] = Field(default_factory=dict)

class ContextObject(BaseModel):
    """
    Base class for context objects in the Model Context Protocol.
    """
    metadata: ContextMetadata = Field(default_factory=ContextMetadata)
    content: Dict[str, Any]

    def validate(self) -> bool:
        """
        Validate the context object's integrity and structure.
        
        Returns:
            bool: Whether the context object is valid
        """
        # Basic validation logic
        return bool(self.content)

    def merge(self, other: ContextObject) -> ContextObject:
        """
        Merge two context objects.
        
        Args:
            other (ContextObject): Another context object to merge
        
        Returns:
            ContextObject: Merged context object
        """
        merged_content = {**self.content, **other.content}
        merged_tags = {**self.metadata.tags, **other.metadata.tags}
        
        return ContextObject(
            content=merged_content,
            metadata=ContextMetadata(
                source=f"{self.metadata.source},{other.metadata.source}",
                tags=merged_tags
            )
        )

class ContextProvider:
    """
    Base class for context providers in the Model Context Protocol.
    """
    def get_context(self, context_type: str, **kwargs) -> Optional[ContextObject]:
        """
        Retrieve a context object.
        
        Args:
            context_type (str): Type of context to retrieve
            **kwargs: Additional retrieval parameters
        
        Returns:
            Optional[ContextObject]: Retrieved context object or None
        """
        raise NotImplementedError("Subclasses must implement get_context method")

    def store_context(self, context: ContextObject) -> bool:
        """
        Store a context object.
        
        Args:
            context (ContextObject): Context object to store
        
        Returns:
            bool: Whether storage was successful
        """
        raise NotImplementedError("Subclasses must implement store_context method")

def create_context_object(
    content: Dict[str, Any], 
    source: Optional[str] = None, 
    tags: Optional[Dict[str, Any]] = None
) -> ContextObject:
    """
    Factory method to create a context object.
    
    Args:
        content (Dict[str, Any]): Content of the context object
        source (Optional[str]): Source of the context
        tags (Optional[Dict[str, Any]]): Tags for the context
    
    Returns:
        ContextObject: Created context object
    """
    metadata = ContextMetadata(
        source=source,
        tags=tags or {}
    )
    return ContextObject(content=content, metadata=metadata)

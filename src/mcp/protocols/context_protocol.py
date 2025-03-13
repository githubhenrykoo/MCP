from __future__ import annotations
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum, auto
import json
import hashlib

class ContextProtocolVersion(Enum):
    V1_0 = auto()
    V1_1 = auto()

class ContextRequest(BaseModel):
    """
    Represents a context retrieval request in the Model Context Protocol.
    """
    request_id: str = Field(default_factory=lambda: hashlib.md5(json.dumps(self).encode()).hexdigest())
    context_type: str
    parameters: Dict[str, Any] = {}
    protocol_version: ContextProtocolVersion = ContextProtocolVersion.V1_0
    
    def validate(self) -> bool:
        """
        Validate the context request.
        
        Returns:
            bool: Whether the request is valid
        """
        return bool(self.context_type)

class ContextResponse(BaseModel):
    """
    Represents a context response in the Model Context Protocol.
    """
    request_id: str
    status: str
    context_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = {}

    @classmethod
    def success(
        cls, 
        request_id: str, 
        context_data: Dict[str, Any], 
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextResponse:
        """
        Create a successful context response.
        
        Args:
            request_id (str): Original request ID
            context_data (Dict[str, Any]): Retrieved context data
            metadata (Optional[Dict[str, Any]]): Additional metadata
        
        Returns:
            ContextResponse: Successful response object
        """
        return cls(
            request_id=request_id,
            status="SUCCESS",
            context_data=context_data,
            metadata=metadata or {}
        )

    @classmethod
    def error(
        cls, 
        request_id: str, 
        error_message: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextResponse:
        """
        Create an error context response.
        
        Args:
            request_id (str): Original request ID
            error_message (str): Description of the error
            metadata (Optional[Dict[str, Any]]): Additional metadata
        
        Returns:
            ContextResponse: Error response object
        """
        return cls(
            request_id=request_id,
            status="ERROR",
            error_message=error_message,
            metadata=metadata or {}
        )

class ContextNegotiationProtocol:
    """
    Manages context negotiation and retrieval in the Model Context Protocol.
    """
    def __init__(self, providers: List[Any] = None):
        """
        Initialize the context negotiation protocol.
        
        Args:
            providers (Optional[List[Any]]): List of context providers
        """
        self.providers = providers or []

    def negotiate_context(self, request: ContextRequest) -> ContextResponse:
        """
        Negotiate and retrieve context based on the request.
        
        Args:
            request (ContextRequest): Context retrieval request
        
        Returns:
            ContextResponse: Context retrieval response
        """
        try:
            # Validate request
            if not request.validate():
                return ContextResponse.error(
                    request_id=request.request_id,
                    error_message="Invalid context request"
                )

            # Attempt to retrieve context from providers
            for provider in self.providers:
                context = provider.get_context(
                    context_type=request.context_type,
                    **request.parameters
                )
                
                if context:
                    return ContextResponse.success(
                        request_id=request.request_id,
                        context_data=context.content,
                        metadata={
                            "provider": provider.__class__.__name__,
                            "context_id": context.metadata.id
                        }
                    )

            # No context found
            return ContextResponse.error(
                request_id=request.request_id,
                error_message="No context found for the given request"
            )

        except Exception as e:
            # Handle unexpected errors
            return ContextResponse.error(
                request_id=request.request_id,
                error_message=f"Unexpected error: {str(e)}"
            )

def create_context_request(
    context_type: str, 
    parameters: Optional[Dict[str, Any]] = None
) -> ContextRequest:
    """
    Factory method to create a context request.
    
    Args:
        context_type (str): Type of context to request
        parameters (Optional[Dict[str, Any]]): Request parameters
    
    Returns:
        ContextRequest: Created context request
    """
    return ContextRequest(
        context_type=context_type,
        parameters=parameters or {}
    )

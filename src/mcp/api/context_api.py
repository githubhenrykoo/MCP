from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from ..protocols.context_protocol import (
    ContextRequest, 
    ContextResponse, 
    ContextNegotiationProtocol
)
from ..context.providers.base_provider import (
    FileSystemContextProvider, 
    InMemoryContextProvider
)
from ..context.base import create_context_object

class ContextRequestModel(BaseModel):
    """
    Pydantic model for context request validation.
    """
    context_type: str
    parameters: Dict[str, Any] = {}

class ContextAPIServer:
    """
    FastAPI-based context management server for Model Context Protocol.
    """
    def __init__(self):
        """
        Initialize the context API server with default providers.
        """
        self.app = FastAPI(
            title="Model Context Protocol API",
            description="API for managing and retrieving contextual information",
            version="1.0.0"
        )
        
        # Initialize context providers
        self.file_provider = FileSystemContextProvider()
        self.memory_provider = InMemoryContextProvider()
        
        # Create context negotiation protocol
        self.negotiation_protocol = ContextNegotiationProtocol([
            self.file_provider, 
            self.memory_provider
        ])
        
        # Setup API routes
        self._setup_routes()

    def _setup_routes(self):
        """
        Configure API routes for context management.
        """
        @self.app.post("/context/negotiate", response_model=Dict[str, Any])
        async def negotiate_context(request: ContextRequestModel):
            """
            Negotiate and retrieve context based on the request.
            
            Args:
                request (ContextRequestModel): Context retrieval request
            
            Returns:
                Dict[str, Any]: Context negotiation response
            """
            # Create context request
            context_request = ContextRequest(
                context_type=request.context_type,
                parameters=request.parameters
            )
            
            # Negotiate context
            response = self.negotiation_protocol.negotiate_context(context_request)
            
            # Handle response
            if response.status == "SUCCESS":
                return {
                    "status": "success",
                    "context": response.context_data,
                    "metadata": response.metadata
                }
            else:
                raise HTTPException(
                    status_code=404, 
                    detail=response.error_message or "Context not found"
                )

        @self.app.post("/context/store", response_model=Dict[str, Any])
        async def store_context(context_data: Dict[str, Any]):
            """
            Store a context object.
            
            Args:
                context_data (Dict[str, Any]): Context data to store
            
            Returns:
                Dict[str, Any]: Storage result
            """
            try:
                # Create context object
                context = create_context_object(
                    content=context_data,
                    source="api_upload",
                    tags={"origin": "api_store"}
                )
                
                # Store in both providers
                file_result = self.file_provider.store_context(context)
                memory_result = self.memory_provider.store_context(context)
                
                return {
                    "status": "success" if file_result and memory_result else "partial",
                    "context_id": context.metadata.id
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Error storing context: {str(e)}"
                )

    def get_app(self):
        """
        Get the FastAPI application instance.
        
        Returns:
            FastAPI: Configured FastAPI application
        """
        return self.app

# Create API server instance
context_api_server = ContextAPIServer()
app = context_api_server.get_app()

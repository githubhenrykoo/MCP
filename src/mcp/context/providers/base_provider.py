from __future__ import annotations
from typing import Dict, Any, Optional
import os
import json

from ..base import ContextObject, ContextProvider, create_context_object

class FileSystemContextProvider(ContextProvider):
    """
    A context provider that retrieves and stores context from the local file system.
    """
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the file system context provider.
        
        Args:
            base_path (Optional[str]): Base directory for storing context files
        """
        self.base_path = base_path or os.path.join(os.getcwd(), 'mcp_contexts')
        os.makedirs(self.base_path, exist_ok=True)

    def get_context(self, context_type: str, **kwargs) -> Optional[ContextObject]:
        """
        Retrieve a context object from the file system.
        
        Args:
            context_type (str): Type of context to retrieve
            **kwargs: Additional retrieval parameters
        
        Returns:
            Optional[ContextObject]: Retrieved context object or None
        """
        filename = kwargs.get('filename', f'{context_type}.json')
        filepath = os.path.join(self.base_path, filename)
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    content = json.load(f)
                
                return create_context_object(
                    content=content,
                    source=f'file://{filepath}',
                    tags={'context_type': context_type}
                )
        except Exception as e:
            print(f"Error retrieving context: {e}")
        
        return None

    def store_context(self, context: ContextObject) -> bool:
        """
        Store a context object to the file system.
        
        Args:
            context (ContextObject): Context object to store
        
        Returns:
            bool: Whether storage was successful
        """
        try:
            # Use context type or a default filename
            context_type = context.metadata.tags.get('context_type', 'default')
            filename = f'{context_type}.json'
            filepath = os.path.join(self.base_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(context.content, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error storing context: {e}")
            return False

class InMemoryContextProvider(ContextProvider):
    """
    A context provider that stores and retrieves context in memory.
    """
    def __init__(self):
        """
        Initialize the in-memory context provider.
        """
        self._contexts: Dict[str, ContextObject] = {}

    def get_context(self, context_type: str, **kwargs) -> Optional[ContextObject]:
        """
        Retrieve a context object from memory.
        
        Args:
            context_type (str): Type of context to retrieve
            **kwargs: Additional retrieval parameters
        
        Returns:
            Optional[ContextObject]: Retrieved context object or None
        """
        key = kwargs.get('key', context_type)
        return self._contexts.get(key)

    def store_context(self, context: ContextObject) -> bool:
        """
        Store a context object in memory.
        
        Args:
            context (ContextObject): Context object to store
        
        Returns:
            bool: Whether storage was successful
        """
        try:
            # Use context type or a generated key
            key = context.metadata.tags.get('key', context.metadata.id)
            self._contexts[key] = context
            return True
        except Exception as e:
            print(f"Error storing context: {e}")
            return False

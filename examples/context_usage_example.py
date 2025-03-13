#!/usr/bin/env python3
"""
Example script demonstrating the usage of the Model Context Protocol (MCP)
"""

from mcp.context.base import create_context_object
from mcp.protocols.context_protocol import create_context_request, ContextNegotiationProtocol
from mcp.context.providers.base_provider import FileSystemContextProvider, InMemoryContextProvider

def main():
    """
    Demonstrate basic Model Context Protocol usage
    """
    # Create context providers
    file_provider = FileSystemContextProvider()
    memory_provider = InMemoryContextProvider()

    # Create a context negotiation protocol
    negotiation_protocol = ContextNegotiationProtocol([
        file_provider, 
        memory_provider
    ])

    # Example: Create and store a model training context
    model_context = create_context_object(
        content={
            "model_name": "example_classifier",
            "training_dataset": "cifar10",
            "hyperparameters": {
                "learning_rate": 0.001,
                "batch_size": 32,
                "epochs": 50
            },
            "performance_metrics": {
                "accuracy": 0.92,
                "f1_score": 0.91
            }
        },
        source="training_run",
        tags={
            "context_type": "model_training",
            "version": "1.0"
        }
    )

    # Store the context
    file_provider.store_context(model_context)
    memory_provider.store_context(model_context)

    # Create a context request
    context_request = create_context_request(
        context_type="model_training",
        parameters={"model_name": "example_classifier"}
    )

    # Negotiate and retrieve context
    response = negotiation_protocol.negotiate_context(context_request)

    # Print context details
    if response.status == "SUCCESS":
        print("Context Retrieved Successfully:")
        print("Context Data:", response.context_data)
        print("Metadata:", response.metadata)
    else:
        print("Context Retrieval Failed:", response.error_message)

if __name__ == "__main__":
    main()

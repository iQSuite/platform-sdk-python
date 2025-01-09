# iQSuite Python SDK

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

iQ Suite Platform is a powerful Retrieval Augmented Generation as a service (RAGAAS) and Hybrid Search that allows you to:

- Create **semantically** and **keyword-based** searchable indices from unstructured sources such as PDF, Microsoft Word, PowerPoint and raw text chunks
- Quickly perform vector-based semantic retrieval augmented generation with precision and persistent performance
- Chat with your documents using natural language
- Instantly extract insights from raw unstructured text chunks, emails, domain-specific text data code
- Build production-ready document Q&A systems, natural-language-based analytics, key-value pair extractions, classifications, and etc.


> The platform handles all the complexity of document processing, embedding generation, contextualized chunking, reranking and vector search, allowing you to focus on building your application.

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Authentication](#get-current-user)
  - [Document-based RAG](#document-based-rag)
      - [Create Index](#create-index)
      - [Create Index With Polling](#create-index-with-polling)
      - [Add Document To Index](#add-document-to-index)
      - [Add Document With Polling](#add-document-with-polling)
      - [List Indices](#list-indices)
      - [List Documents](#list-documents)
      - [Delete Document](#delete-document)
      - [Chat](#chat)
      - [Search](#search)
      - [Task Status](#task-status)
  - [Instant RAG](#instant-rag)
      - [Create Instant RAG](#create-instant-rag)
      - [Query Instant RAG](#query-instant-rag)
  - [Webhooks](#webhooks)
      - [Create Webhook](#create-webhook)
      - [List Webhooks](#list-webhooks)
      - [Update Webhook](#update-webhook)
      - [Delete Webhook](#delete-webhook)
- [Supported Documents](#supported-documents)
- [Error Handling](#error-handling)
- [Support](#support)

## Installation

```bash
pip install iqsuite
```

## Features

- 📄 Multi-format document support (PDF, Word, PowerPoint)
- 🔍 Hybrid semantic search
- 💬 Natural language chat with documents
- 🚀 Instant RAG capabilities
- 🔄 Asynchronous processing with webhook support
- ⚡ Real-time notifications
- 🔒 Secure API authentication

## Quick Start

### Get API Key

> [!CAUTION]
> Never share your API key or commit it to version control. Always use environment variables or secure key management systems.

1. Visit [iQ Suite Platform](https://iqsuite.ai)
2. Sign up with your email or GitHub to create an account.
3. Once logged in, click on the "API Keys" from the left sidebar, fill in API key name and click `Create API Key` to create a new key.
4. Copy the key and store it somewhere safe as **it'll not be shown again**.

### Use the API Key

```python
import os
from iqsuite import IQSuiteClient
from iqsuite.exceptions import APIError, AuthenticationError

client = IQSuiteClient(os.getenv("IQSUITE_API_KEY"))
```

## Usage Examples

### Get Current User

Retrieve information about the authenticated user. This is to ensure that you're successfully authenticated with iQ.

```python
try:
    user = client.get_user()
    print(f"User ID: {user.id}")
    print(f"Email: {user.email}")
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(f"API Error: {e}")
```


### Document-based RAG

#### Create Index

> [!NOTE]
> Creating an index is an asynchronous operation. You'll receive a task ID that you can use to track the progress.

```python
# Create a new index from a document
with open('document.pdf', 'rb') as f:
    response = client.create_index(document=f,filename='document.pdf')
    print(f"Task ID: {response.task_id}")
```

#### Create Index With Polling

> [!TIP]
> Use this method when you need to wait for the index creation to complete before proceeding.

```python
# Create index and wait for completion
response = client.create_index_and_poll(
    document='document.pdf',
    polling_interval=20,      # Seconds between polling attempts
    max_retries=2             # Maximum number of polling attempts
)
print(f"Index ID: {response.index_id}")
```

#### Add Document To Index

> [!NOTE]
> Adding documents to an existing index is also asynchronous. Make sure you already have an existing index ready and available to use.

```python
# Add a new document to an existing index
with open('new_document.docx', 'rb') as f:
    response = client.add_document(
        index_id='idx_abc123',
        document=f,
        filename='new_document.docx'
    )
    print(f"Task ID: {response.task_id}")
```

#### Add Document With Polling

```python
# Add document and wait for completion
response = client.add_document_and_poll(
    index_id='idx_abc123',
    document='new_document.docx',
    polling_interval=20,      # Seconds between polling attempts
    max_retries=2             # Maximum number of polling attempts
)
print(f"Document ID: {response.document_id}")
```

#### List Indices

```python
# Get all your indices
indices = client.list_indices()

for index in indices.data:
    print(f"Index ID: {index.id}")
```

#### List Documents

```python
# Get all documents in an index
documents = client.get_documents('your_index_id')

for doc in documents.data:
    print(f"Document ID: {doc.id}")
```

#### Delete Document

> [!CAUTION]
> Document deletion is permanent and cannot be undone.

```python
try:
    result = client.delete_document(
        index_id='your-index-id',
        document_id='document-id-to-delete')
    print("Document deleted successfully")
except APIError as e:
    print(f"Error: {e}")
```

#### Chat

> [!TIP]
> For best results, make your questions clear and specific.

```python
try:
    response = client.chat(
        index_id='your-index-id',
        query="What are the main points discussed?"
    )
    print(f"Response: {response}")
except APIError as e:
    print(f"Error: {e}")
```

#### Search

```python
try:
    results = client.search(
        index_id='your-index-id',
        query="neural networks"
    )
    print(f"Search results: {results}")
except APIError as e:
    print(f"Error: {e}")
```

#### Task Status

> [!TIP]
> Use this to check the progress of any asynchronous operation.

```python
try:
    status = client.get_task_status('your-task-id')
    print(f"Status: {status.status}")
except APIError as e:
    print(f"Error: {e}")


# Using polling to check task status (Optional)
while True:
    status = client.get_task_status('your-task-id')
    print(f"Status: {status.status}")
    if status.status == 'completed':
        break
    elif status.status == 'failed':
        raise Exception("Index creation failed")
    time.sleep(5)  # Wait 5 seconds before checking again
```

### Instant RAG

> [!IMPORTANT]
> Instant RAG is perfect for quick, one-time analysis of text content without the need to create persistent indices.

#### Create Instant RAG

```python
# Create an instant RAG session
context = """Your text content here. This can be a long piece of text 
that you want to analyze or query immediately."""

response = client.create_instant_rag(context=context)

```

#### Query Instant RAG

```python
# Query your instant RAG
response = client.query_instant_rag(
    rag_id="irag_abc123",
    query="What are the key points in this text?",
)

```

### Webhooks

> [!TIP]
> Webhooks are the recommended way to handle asynchronous operations in production environments. If your application requires to be notified for an event, using webkooks is the recommeneded way rahter than using polling method. You can create and manage webhooks from the iQ Suite Platform Application or using the below function.

#### Create Webhook

```python
# Set up a new webhook
webhook = client.create_webhook(
    url="https://your-domain.com/webhook",
    name="Processing Events",
    enabled=True,
    secret="your-webhook-secret"  # Optional: for security
)
```

#### List Webhooks

```python
# Get all your webhooks
webhooks = client.list_webhooks()
```

#### Update Webhook

```python
# Modify an existing webhook
updated_webhook = client.update_webhook(
    webhook_id="whk_abc123",
    url="https://your-domain.com/new-endpoint",
    name="Updated Webhook Name",
    enabled=True
)
```

#### Delete Webhook

> [!CAUTION]
> Deleting a webhook will immediately stop all notifications to the specified endpoint.

```python
# Remove a webhook
response = client.delete_webhook(webhook_id="whk_abc123")
```

#### Webhook Events

When an event occurs, your webhook endpoint will receive a POST request with a JSON payload:

```json
{
    "event": "index.created",
    "task_id": "task_abc123",
    "status": "completed",
    "data": {
        "index_id": "idx_xyz789",
        "document_count": 1
    },
    "timestamp": "2025-01-09T09:10:27.000000Z"
}
```

> [!IMPORTANT]
> Always verify webhook signatures in production environments to ensure the request came from iQ Suite.

## Supported Documents

> [!NOTE]
> All documents are automatically processed with OCR (Optical Character Recognition) when applicable.

The iQ Suite platform supports the following document types:

- PDF Files (.pdf)
  - Text-based PDFs
  - Scanned PDFs with OCR support
  - Password-protected PDFs (require password during upload)
- Microsoft Word Documents
  - Modern format (.docx)
  - Legacy format (.doc)
- Microsoft PowerPoint Presentations
  - Modern format (.pptx)
  - Legacy format (.ppt)

> [!TIP]
> For best results, ensure your documents are properly formatted and text is clear and legible.

## Error Handling

> [!IMPORTANT]
> Implement proper error handling in your application to ensure robustness and good user experience.

The SDK uses several exception types to handle different error scenarios:

```python
try:
    result = client.create_index(document='file.pdf')
except AuthenticationError as e:
    # Handle invalid or expired API keys
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    # Handle rate limit exceeding
    print(f"Rate limit exceeded. Reset at: {e.reset_at}")
except ValidationError as e:
    # Handle invalid input parameters
    print(f"Invalid input: {e.errors}")
except APIError as e:
    # Handle general API errors
    print(f"API error: {e.message}, Status: {e.status_code}")
except NetworkError as e:
    # Handle connectivity issues
    print(f"Network error: {e}")
```

Common error status codes:
- `400`: Bad Request - Check your input parameters
- `401`: Unauthorized - Invalid API key
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource doesn't exist
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Server Error - Contact support

> [!WARNING]
> Never ignore errors in production. Always implement proper error handling and retry mechanisms for transient failures.

## Support

We're here to help you succeed with the iQ Suite platform:

### Documentation
- 📚 [Full API Documentation](https://docs.iqsuite.ai/)
- 🔧 [SDK Reference](https://docs.iqsuite.ai/sdk/python)
- 📖 [Tutorials & Guides](https://docs.iqsuite.ai/tutorials)

### Getting Help
- 📧 [Email Support](mailto:support@iqsuite.ai)
- 💬 [Discord Community](https://discord.gg/iqsuite)
- 🐛 [GitHub Issues](https://github.com/iqsuite/iqsuite-python/issues)

### Best Practices
- ✅ Keep your SDK version updated
- 📝 Enable logging in development
- 🔄 Implement retry mechanisms for production use
- 🔒 Follow security best practices


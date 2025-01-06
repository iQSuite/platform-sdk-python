# IQSuite Python SDK

A Python SDK for interacting with the IQSuite API. This library provides a simple and intuitive way to use IQSuite's document indexing and search capabilities.

## Installation

You can install the package in several ways:

### From PyPI
```bash
pip install iqsuite
```

### From GitHub
```bash
pip install git+https://github.com/blue-hex/iqsuite-platform-py-sdk.git
```

Or add to your requirements.txt:
```
git+https://github.com/blue-hex/iqsuite-platform-py-sdk.git
```

### Local Development Installation
```bash
git clone https://github.com/blue-hex/iqsuite-platform-py-sdk.git
cd iqsuite-platform-py-sdk
pip install -e .
```

## Quick Start

```python
from iqsuite import IQSuiteClient

# Initialize the client
client = IQSuiteClient('your-api-key')

# Get user information
user = client.get_user()
print(f"Logged in as: {user.email}")

# List all indexes
indexes = client.list_indexes()
for index in indexes:
    print(f"Index: {index.id}, Documents: {index.document_count}")

# Create a new index
with open('document.pdf', 'rb') as f:
    task = client.create_index(f, 'document.pdf')
print(f"Index creation task ID: {task.id}")

# Check task status
status = client.get_task_status(task.id)
print(f"Task status: {status.status}")

# Add document to existing index
index_id = "your-index-id"
with open('another_document.pdf', 'rb') as f:
    task = client.add_document(index_id, f, 'another_document.pdf')

# Chat with index
response = client.chat(index_id, "What is OpenVINO?")
print(response)

# Search in index
results = client.search(index_id, "insurance")
print(results)
```

## Features

- User management
- Index creation and management
- Document uploading and indexing
- Document search and retrieval
- Chat interface with indexed documents
- Asynchronous task status tracking
- Error handling and retries

## Error Handling

The SDK provides custom exceptions for better error handling:

```python
from iqsuite import IQSuiteException, AuthenticationError, APIError

try:
    client = IQSuiteClient('invalid-api-key')
    user = client.get_user()
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(f"API error: {str(e)}, Status code: {e.status_code}")
except IQSuiteException as e:
    print(f"Something went wrong: {str(e)}")
```

## API Reference

### IQSuiteClient

The main client class for interacting with the IQSuite API.

```python
client = IQSuiteClient(api_key: str, base_url: str = "https://iqsuite.test/api/v1")
```

#### Methods

- `get_user()` - Get current user information
- `list_indexes()` - List all available indexes
- `get_documents(index_id: str)` - Get all documents from an index
- `create_index(document: BinaryIO, filename: str)` - Create a new index with an initial document
- `add_document(index_id: str, document: BinaryIO, filename: str)` - Add a document to an existing index
- `get_task_status(task_id: str)` - Check the status of a task
- `chat(index_id: str, query: str)` - Chat with an index
- `search(index_id: str, query: str)` - Perform hybrid search on an index
- `delete_document(index_id: str, document_id: str)` - Delete a document from an index

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/blue-hex/iqsuite-platform-py-sdk.git
cd iqsuite-platform-py-sdk
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## Building and Publishing

1. Build the package:
```bash
python -m build
```

2. Upload to PyPI:
```bash
python -m twine upload dist/*
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


## Support

If you encounter any problems or have any questions, please:

1. Check the [GitHub Issues](https://github.com/blue-hex/iqsuite-platform-py-sdk/issues) for existing problems and solutions
2. Create a new issue if your problem is not already reported
3. Contact [support](mailto:support@example.com) for additional help
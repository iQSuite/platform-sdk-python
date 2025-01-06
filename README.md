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

## Quick Start

```python
from iqsuite import IQSuiteClient

# Initialize the client
client = IQSuiteClient('your-api-key')

# For development/testing with self-signed certificates
client = IQSuiteClient(
    api_key='your-api-key',
    verify_ssl=False,  # Only use in development
    verbose=True       # Optional: to show warnings (defaults to False)
)
```

### Basic Operations

```python
# Get user information
user = client.get_user()
print(f"Logged in as: {user.email}")

# List all indexes
indexes = client.list_indexes()
for index in indexes:
    print(f"Index: {index.id}")
```

### Creating a New Index

```python
# Create a new index with initial document
with open('document.pdf', 'rb') as f:
    task = client.create_index(f, 'document.pdf')
    print(f"Task ID: {task.task_id}")
    print(f"Message: {task.message}")
    print(f"Status URL: {task.check_status}")

    # Check task status
    status = client.get_task_status(task.task_id)
    print(f"Task status: {status.status}")
```

### Adding Documents to an Index

```python
# Add document to existing index
index_id = "your-index-id"  # Get this from list_indexes() or create_index()
with open('new_document.pdf', 'rb') as f:
    task = client.add_document(index_id, f, 'new_document.pdf')
    print(f"Task ID: {task.task_id}")
    print(f"Message: {task.message}")
    print(f"Status check URL: {task.check_status}")

    # Check task status
    status = client.get_task_status(task.task_id)
    print(f"Task status: {status.status}")
```

### Complete Example with Error Handling

```python
from iqsuite import IQSuiteClient, AuthenticationError, APIError

# Initialize client
client = IQSuiteClient('your-api-key', verify_ssl=False, suppress_warnings=True)

try:
    # List available indexes
    indexes = client.list_indexes()
    if indexes:
        # Get the first index ID
        index_id = indexes[0].id
        print(f"Found index: {index_id}")

        # Add new document to this index
        with open('document.pdf', 'rb') as f:
            task = client.add_document(index_id, f, 'document.pdf')
            print(f"Task ID: {task.task_id}")
            print(f"Message: {task.message}")

            # Check task status
            status = client.get_task_status(task.task_id)
            print(f"Task status: {status.status}")

        # Chat with index
        response = client.chat(index_id, "What is OpenVINO?")
        print(f"Chat response: {response}")

        # Search in index
        results = client.search(index_id, "insurance")
        print(f"Search results: {results}")

except AuthenticationError as e:
    print(f"Authentication error: {e}")
except APIError as e:
    print(f"API error: {e}")
    if hasattr(e, 'status_code'):
        print(f"Status code: {e.status_code}")
```


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

## Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


## Support

If you encounter any problems or have any questions, please:

1. Check the [GitHub Issues](https://github.com/blue-hex/iqsuite-platform-py-sdk/issues) for existing problems and solutions
2. Create a new issue if your problem is not already reported
3. Contact support for additional help
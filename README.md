# DevKB-Snippets - Code Snippet Manager

A focused code snippet storage and retrieval system with tagging and search.

## Features

- Store and organize code snippets
- Tag-based organization
- Language detection
- Full-text search
- Export/Import functionality
- Lightweight SQLite storage

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Add a snippet
```bash
python -m snippets add --code "print('Hello')" --language python --tags "example,hello"
```

### Search by tag
```bash
python -m snippets tag python
```

### List all
```bash
python -m snippets list
```

## Configuration

```bash
cp .env.example .env
```

## License

MIT

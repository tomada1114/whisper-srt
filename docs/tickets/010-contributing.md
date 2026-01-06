# Ticket #10: Create CONTRIBUTING.md

## Overview
Create a contributing guide for developers who want to contribute to the project.

## Acceptance Criteria
- [ ] CONTRIBUTING.md created in English
- [ ] Development setup instructions
- [ ] Code style guidelines
- [ ] Testing instructions
- [ ] Pull request process

## CONTRIBUTING.md Content

```markdown
# Contributing to whisper-srt

Thank you for your interest in contributing to whisper-srt!

## Development Setup

### Prerequisites
- Python 3.9+
- Git

### Clone and Install
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/whisper-srt-from-mp3.git
cd whisper-srt-from-mp3

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
\`\`\`

### Verify Setup
\`\`\`bash
make ci  # Run linting, type checking, and tests
\`\`\`

## Development Commands

\`\`\`bash
# Run all checks (lint + type-check + test)
make ci

# Individual commands
make lint       # Run ruff linter
make format     # Format code with ruff
make type-check # Run mypy
make test       # Run pytest
make test-cov   # Run pytest with coverage

# Run specific test
pytest tests/unit/domain/test_vocabulary.py -v
\`\`\`

## Code Style

- Use [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- Follow [PEP 8](https://pep8.org/) conventions
- Add type hints to all functions
- Write docstrings in English

### Pre-commit Check
Before committing, ensure all checks pass:
\`\`\`bash
make ci
\`\`\`

## Testing

### Test Structure
\`\`\`
tests/
└── unit/
    ├── domain/
    ├── application/
    ├── infrastructure/
    └── interface/
\`\`\`

### Writing Tests
- Use pytest fixtures for common setup
- Mock external APIs (OpenAI)
- Cover happy path, sad path, and edge cases

### Example Test
\`\`\`python
def test_something(tmp_path):
    # Arrange
    input_file = tmp_path / "test.txt"
    input_file.write_text("content")

    # Act
    result = some_function(input_file)

    # Assert
    assert result == expected
\`\`\`

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Ensure tests pass: `make ci`
5. Commit with clear message: `git commit -m "feat: add new feature"`
6. Push to your fork: `git push origin feature/your-feature`
7. Open a Pull Request

### Commit Message Format
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `chore:` Maintenance

## Questions?

Open an issue for questions or discussions.
```

## Files to Create
- `CONTRIBUTING.md` - New file in repository root

## Dependencies
- None (can be created independently)

# Coverage Reporting Guide

This document explains how code coverage works in the xmi-schema-python project.

## Overview

We use **local coverage reporting** without any cloud services. All coverage processing happens either on your local machine or in GitHub Actions.

## Tools Used

- **coverage.py**: Core coverage measurement tool
- **pytest-cov**: Pytest plugin for coverage
- **GitHub Actions**: Automated coverage in CI/CD
- **GitHub Script**: Posts coverage comments on PRs

## Local Coverage

### Running Tests with Coverage

```bash
# Basic coverage report in terminal
poetry run pytest --cov=src/xmi

# Generate HTML report
poetry run pytest --cov=src/xmi --cov-report=html

# Generate XML report (for CI)
poetry run pytest --cov=src/xmi --cov-report=xml

# All formats at once
poetry run pytest --cov=src/xmi --cov-report=html --cov-report=xml --cov-report=term
```

### Viewing HTML Reports

After generating HTML reports, open them in your browser:

```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

The HTML report shows:
- Overall coverage percentage
- Coverage by file
- Line-by-line coverage (green = covered, red = not covered)
- Branch coverage details

### Coverage Configuration

Coverage settings are in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src/xmi"]
omit = [
    "*/tests/*",
    "*/test_*",
]

[tool.coverage.report]
precision = 1
show_missing = true
skip_covered = false
```

## CI/CD Coverage

### PR Validation Workflow

When you create a pull request, the workflow automatically:

1. **Runs tests with coverage** on Python 3.12
2. **Calculates coverage percentage**
3. **Generates badge color**:
   - 🟢 Green (>=75%): Good coverage
   - 🟡 Yellow (60-75%): Acceptable
   - 🔴 Red (<60%): Needs improvement
4. **Posts comment on PR** with:
   - Coverage badge
   - Line coverage percentage
   - Branch coverage percentage
   - Link to download full report
5. **Uploads artifacts**:
   - HTML coverage report
   - XML coverage report
   - Available for 30 days

### Example PR Comment

The bot will post a comment like this:

```markdown
## Coverage Report

![Coverage](https://img.shields.io/badge/coverage-72%25-yellowgreen)

| Metric | Percentage |
|--------|------------|
| Line Coverage | 72.4% |
| Branch Coverage | 65.2% |

**Test Results**: ✅ All tests passed
**Python Version**: 3.12

<details>
<summary>View detailed coverage report</summary>

Download the coverage artifact from this workflow run to view the full HTML report.

</details>
```

### Downloading Coverage Reports from PRs

1. Go to the PR on GitHub
2. Click on "Actions" tab at the top
3. Find the workflow run for your PR
4. Scroll down to "Artifacts"
5. Download "coverage-report"
6. Extract the zip file
7. Open `htmlcov/index.html`

## Coverage Goals

### Current Coverage

- **Overall**: ~72%
- **v1 modules**: ~75%
- **v2 modules**: ~85%

### Coverage Targets

| Priority | Target | Description |
|----------|--------|-------------|
| High | 80%+ | Core entity and relationship classes |
| Medium | 70%+ | Utility functions and helpers |
| Low | 60%+ | Error handling and edge cases |

### Improving Coverage

To improve coverage:

1. **Identify uncovered code**:
   ```bash
   poetry run pytest --cov=src/xmi --cov-report=term-missing
   ```

2. **Focus on critical paths**:
   - Entity parsing logic
   - Relationship creation
   - Unit conversions
   - Validation functions

3. **Add tests for edge cases**:
   - Invalid input handling
   - Boundary conditions
   - Error scenarios

4. **Test parameter variations**:
   - Different unit combinations
   - Various shape types
   - Multiple Python versions

## Why No Cloud Service?

We deliberately chose **local coverage** instead of cloud services like Codecov because:

### Advantages

✅ **Privacy**: No external service has access to code coverage data
✅ **No Dependencies**: No external service outages or API changes
✅ **Free**: No subscription or usage limits
✅ **Control**: Full control over reports and data
✅ **Speed**: No upload/download delays
✅ **Simple**: One less service to configure and maintain

### Trade-offs

❌ **No history graphs**: Can't see coverage trends over time
❌ **Manual badge updates**: Badge in README is static
❌ **No comparison**: Can't automatically compare coverage between commits

### Alternatives Considered

If you want to add cloud coverage later, here are options:

1. **Codecov** (most popular)
   - Sign up at https://codecov.io
   - Add `CODECOV_TOKEN` to GitHub secrets
   - Use `codecov/codecov-action@v5` in workflow

2. **Coveralls** (free for open source)
   - Sign up at https://coveralls.io
   - Add `COVERALLS_REPO_TOKEN` to secrets
   - Use `coverallsapp/github-action@v2`

3. **SonarCloud** (comprehensive analysis)
   - Sign up at https://sonarcloud.io
   - Includes coverage + code quality
   - More complex setup

## Troubleshooting

### Coverage shows 0%

Check that:
- Tests are actually running
- Source path is correct in `pyproject.toml`
- No conflicting `.coverage` file exists

```bash
# Clean old coverage data
rm -f .coverage coverage.xml
rm -rf htmlcov/

# Run fresh
poetry run pytest --cov=src/xmi
```

### Missing coverage for some files

Check that:
- Files are in the `src/xmi` directory
- Files are not in the `omit` list
- Files are actually imported by tests

### HTML report not updating

```bash
# Force regeneration
rm -rf htmlcov/
poetry run pytest --cov=src/xmi --cov-report=html
```

## Best Practices

1. **Run coverage locally** before pushing
2. **Check coverage on critical changes**
3. **Don't obsess over 100%**: Focus on important code paths
4. **Review uncovered lines**: Sometimes they're dead code that can be removed
5. **Add tests for bugs**: When fixing bugs, add tests that increase coverage

## Resources

- [coverage.py documentation](https://coverage.readthedocs.io/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [GitHub Actions artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)

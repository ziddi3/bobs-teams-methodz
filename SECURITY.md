# Security Policy

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Bob's Teams Methodz, please report it to us through our GitHub repository's security issues.

## Security Best Practices

### API Key Management

Bob's Teams Methodz follows security best practices for handling sensitive information:

1. **Never Hardcode API Keys**: All API keys and authentication tokens must be stored in the `.env` file, never in source code.

2. **Environment Variables**: The system uses environment variables for all sensitive configuration:
   - `GITHUB_TOKEN`: For GitHub API authentication
   - `AI_MODEL_API_KEY`: For AI model access

3. **Git Exclude Sensitive Files**: The `.gitignore` file explicitly excludes:
   - `.env` files
   - Log files
   - Deliverables directory
   - Runtime data

4. **Example Files Only**: Only `.env.example` (without actual keys) is committed to version control.

### Setup Instructions

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Add your actual API keys to `.env`:
   ```env
   GITHUB_TOKEN=your_actual_token_here
   AI_MODEL_API_KEY=your_actual_key_here
   ```

3. Ensure `.env` is never committed to git (already in `.gitignore`).

### Accessing Keys in Code

Always access keys through environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('GITHUB_TOKEN')
api_key = os.getenv('AI_MODEL_API_KEY')
```

### Token Permissions

The GitHub token should have the minimum required scopes:
- `repo`: Full control of private repositories
- `workflow`: Update GitHub Action workflows

Never share tokens or commit them to any repository.

## Secure Deployment

When deploying Bob's Teams Methodz:

1. Use environment-specific .env files (e.g., `.env.production`, `.env.staging`)
2. Rotate API keys regularly
3. Use secret management services for production deployments
4. Enable audit logging where available
5. Monitor for unauthorized access attempts

## Code Security

- Input validation is performed on all user inputs
- File operations are restricted to designated directories
- No arbitrary code execution from user input
- Error messages don't expose sensitive information

## Questions?

For security-related questions, please open an issue on GitHub with the `security` label.
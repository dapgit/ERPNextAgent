# Security Policy

## Supported Versions

At the moment, ERPNextAgent is an educational project.

Security fixes will be applied to the latest version under active development.

---

# Reporting Security Vulnerabilities

Please do not create a public GitHub issue for security vulnerabilities.

Instead:

1. Contact the project maintainer privately.
2. Provide a detailed description.
3. Include reproduction steps if possible.
4. Allow reasonable time for investigation before public disclosure.

---

# Scope

Examples of security issues include:

- API key exposure
- Authentication vulnerabilities
- Credential leakage
- Command injection
- Remote code execution
- Sensitive data exposure

---

# Secrets Management

Never commit:

- `.env`
- API Keys
- ERPNext credentials
- OAuth tokens
- Session cookies
- Private certificates

Always use environment variables.

Example:

```text
GEMINI_API_KEY=xxxxxxxx
ERPNEXT_URL=https://erp.example.com
ERPNEXT_API_KEY=xxxxxxxx
ERPNEXT_API_SECRET=xxxxxxxx
```

---

# Dependency Management

Dependencies should be reviewed regularly.

Recommended practices:

- Keep packages updated.
- Remove unused dependencies.
- Pin package versions where appropriate.
- Review dependency changelogs before upgrading.

---

# Future Security Roadmap

Future versions will include:

- Secure ERPNext authentication
- Session management
- Role-based authorization
- Request validation
- Audit logging
- Secrets management improvements

---

# Responsible Disclosure

We appreciate responsible disclosure of security issues and will investigate all credible reports promptly.
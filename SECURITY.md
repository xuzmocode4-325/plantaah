# Security.md

# Plantaah Security Policy

## 1. Purpose

This document explains how to report security vulnerabilities in Plantaah and how the project handles security disclosures.

Plantaah is an open-source project with a public repository, a nonprofit-supported core, and a commercial hosted service layer. Security reports may concern the codebase, the hosted API, the web application, infrastructure, data handling, or integrations with third-party services.

## 2. Reporting Security Issues

**Do not open public issues, pull requests, or discussions for security vulnerabilities.**

Instead, report security issues privately to:

- **Email:** `security@plantaah.org`  
- **Optional alternative:** a private security form or GitHub private vulnerability report, if enabled.

If you are unsure whether something is a vulnerability, report it privately.

## 3. What to Include

To help us triage quickly, please include as much of the following as possible:

- A description of the issue.
- The affected component or service.
- Affected version, branch, or environment.
- Steps to reproduce.
- Expected and actual behavior.
- Potential impact.
- Logs, screenshots, or proof-of-concept material, if safe to share.
- Any relevant URLs, request IDs, API endpoints, or error messages.

## 4. What Counts as a Security Issue

Examples of security issues include:

- Authentication or authorization bypass.
- Exposure of API keys or secrets.
- Insecure handling of email addresses or user submissions.
- Injection vulnerabilities.
- Cross-site scripting or cross-site request forgery.
- Broken access control in admin tools.
- Unsafe file handling in PDF generation or storage.
- Misconfiguration that exposes user data.
- Leaks in hosted API, dashboard, or cloud storage access.

## 5. Confidentiality

We ask reporters to keep potential vulnerabilities confidential until the project has had time to investigate and patch the issue.

We will also treat reports as confidential to the extent reasonably possible.

## 6. Response Expectations

After receiving a report, we will:

- Acknowledge receipt as soon as practical.
- Triage the report.
- Confirm whether it is valid and assess severity.
- Work on a fix or mitigation.
- Coordinate disclosure after a patch is available, where appropriate.

We may not be able to provide exact timelines, but we will do our best to keep the reporter informed.

## 7. Patch and Disclosure Process

When a fix is ready, we may:

- Release a patched version.
- Update deployment guidance.
- Credit the reporter, if they want acknowledgment.
- Publish a security advisory or changelog note, where appropriate.

Critical issues affecting hosted services or user data may be handled urgently.

## 8. Safe Harbor

We ask that good-faith security research avoid privacy violations, data destruction, service disruption, and unauthorized access beyond what is needed to demonstrate the issue.

If you act in good faith and follow this policy, we will treat your report constructively.

## 9. Scope Notes

Security reports may involve either:

- The open-source repository and its code.
- The nonprofit-operated project infrastructure.
- The commercial hosted service or API.

If a report touches multiple parts of the Plantaah ecosystem, please mention that clearly.

## 10. Contact

For security reports, contact:

**security@plantaah.org**

If this address changes, the updated contact will be listed in the repository and project website.

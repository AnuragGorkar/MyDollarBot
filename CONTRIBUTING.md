# Contributing to MyDollarBot-BOTGo V5

Thank you for your interest in contributing to **MyDollarBot-BOTGo**! We welcome all contributions, including bug reports, feature requests, and code contributions. To ensure the project maintains high standards, please follow the guidelines below.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Coding Standards](#coding-standards)
- [Submitting Issues](#submitting-issues)
- [Creating a Pull Request](#creating-a-pull-request)
- [Commit Guidelines](#commit-guidelines)
- [Testing Standards](#testing-standards)
- [Code Review Process](#code-review-process)

---

## Getting Started

1. **Fork the repository** on GitHub to your personal account.
2. **Clone your forked repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MyDollarBot-BOTGo.git
   ```

3. Set up the development environment by installing dependencies listed in requirements.txt or the package.json file if using Node.js.
4. Create a new branch for each feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```

## Coding Standards
To maintain code readability and consistency, please adhere to the following coding standards:
* Language: Python (ensure code is compatible with Python 3.8+).
* Formatting: Use PEP 8 standards for Python code.
  * Use 4 spaces for indentation, not tabs.
  * Limit lines to 79 characters.
* Documentation:
  * Use descriptive variable names.
  * Add docstrings to all functions and classes following the Google Python Style Guide.
  * Document complex logic with inline comments.
* Naming Conventions:
  * Variables and functions: `snake_case`
  * Classes: `PascalCase`
  * Constants: `UPPER_CASE`
*  Linting: Run linting using flake8 (Python) or eslint (JavaScript) to catch syntax and style issues before committing:
    ```bash
    flake8 your_file.py
    ```

## Submitting Issues
If you identify any issues or bugs in the project, please submit an issue using the following steps:

1. Search existing issues to check if it has already been reported.
2. Provide a detailed description including:
  * Expected behavior
  * Actual behavior
  * Steps to reproduce
3. Add labels (e.g., `bug`, `enhancement`) to categorize the issue.

## Creating a Pull Request
Before creating a pull request (PR), ensure the following:

1. Branch is up-to-date with the main branch:
    ```bash
    git pull origin main
    ```
2. **Tests are passing**: Run all tests locally to ensure your changes do not break the existing code.
3. **Include meaningful commit messages** following the commit guidelines.
4. **Create a PR**:
    * Go to your forked repository on GitHub.
    * Click on New Pull Request.
    * Provide a descriptive title and a summary of your changes.
5. **Link issues** your PR addresses, if applicable.
### PR Guidelines
* One PR should contain only one feature or bug fix.
* Ensure code follows the Coding Standards.
* Avoid unrelated changes or formatting in your PR.

## Commit Guidelines
  * Format: <type>(<scope>): <description>
  * Types:
  * `feat`: A new feature
  * `fix`: A bug fix
  * `docs`: Documentation-only changes
  * `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
  * `refactor`: Code change that neither fixes a bug nor adds a feature
  * `test`: Adding missing or correcting existing tests
  * `chore`: Other changes that don’t modify src or test files
* Example:
    ```bash
    git commit -m "feat(user-auth): add user login functionality"
   ```
### Testing Standards
* Write unit tests for all new features and bug fixes using pytest (or the chosen testing framework).
* Test Coverage: Aim to cover at least 90% of new code with tests.
* Run tests locally before submitting a PR:
    ```bash
    pytest
    ```

## Code Review Process
1. Reviewers will check your PR for adherence to coding standards, functionality, and testing coverage.
2. Feedback may be provided in the PR comments; please respond promptly and make any necessary changes.
3. Final Approval: Once all checks pass and feedback is addressed, your PR will be approved and merged.
  

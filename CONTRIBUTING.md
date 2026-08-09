# Contributing to GuardianAI

Thank you for your interest in contributing to **GuardianAI**! We welcome contributions from developers, security researchers, and AI engineers worldwide.

---

## 1. Code of Conduct

We are committed to maintaining a welcoming, safe, and respectful environment. Please treat all maintainers and community members with respect.

---

## 2. Getting Started & Development Setup

1. **Fork the Repository** on GitHub.
2. **Clone your fork locally:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/guardianai.git
   cd GuardianAI
   ```
3. **Setup Backend Python Virtual Environment:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
4. **Setup Frontend React SPA Dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

---

## 3. Pull Request Guidelines

- Create a feature branch: `git checkout -b feature/amazing-new-feature` or `bugfix/fix-issue-123`.
- Run backend tests prior to submitting: `pytest backend/tests`.
- Run frontend build verification: `npm run build` inside `frontend/`.
- Submit your PR against the `main` branch with a clear description of changes.

---

## 4. Code Style & Linting Standards

- **Python:** Formatted with `black`, `isort`, and `ruff`.
- **TypeScript / React:** Formatted with `prettier` and `eslint`.

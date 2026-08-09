# GuardianAI Git Workflow & Versioning Strategy

**Document Version:** 1.0.0  
**Target Audience:** GuardianAI Engineering & Release Engineering Teams  

---

## 1. Branching Strategy

GuardianAI enforces a **Trunk-Based Development Model with Protected Feature Branches**:
- **`main` (Production & Single Source of Truth):** Always deployable, strictly protected. Direct pushes are disabled; all changes land via Pull Requests with required CI/CD status checks and code owner approvals.
- **`feature/<name>` (Short-Lived Feature Branches):** Used for developing discrete features (e.g. `feature/xai-rationale-renderer`). Lifetime < 3 days.
- **`fix/<name>` (Bug & Patch Branches):** Used for fixing reported bugs or security vulnerabilities (e.g. `fix/jwt-cors-header`).
- **`release/vX.Y.Z` (Release Staging Branches):** Temporary staging branches created prior to tagging major or minor production releases.

---

## 2. Conventional Commit Specification

All commit messages in the repository must conform to the **Conventional Commits v1.0.0** format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### 2.1 Commit Types & Semantic Versioning Triggers

| Commit Type | Description | Semantic Version Trigger | Example |
| :--- | :--- | :--- | :--- |
| `feat` | A new feature for users | **MINOR** (`v1.1.0`) | `feat(scan): add client-side PII scrubbing worker` |
| `fix` | A bug fix in existing code | **PATCH** (`v1.0.1`) | `fix(auth): resolve JWT expiration timestamp handling` |
| `docs` | Documentation additions | None | `docs(api): update REST API OpenAPI specification` |
| `style` | Formatting / whitespace | None | `style(ui): format Senior Mode CSS tokens` |
| `refactor` | Code structural updates | None | `refactor(db): optimize SQLAlchemy connection pool` |
| `perf` | Performance optimizations | **PATCH** (`v1.0.1`) | `perf(xai): reduce regex evaluation latency by 40%` |
| `BREAKING CHANGE` | Breaking API change | **MAJOR** (`v2.0.0`) | `feat(api)!: alter scan response payload envelope schema` |

---

## 3. Release Tagging & Semantic Versioning (SemVer 2.0.0)

GuardianAI releases follow **Semantic Versioning 2.0.0** (`vMAJOR.MINOR.PATCH`):
- **MAJOR (`v1.0.0` $\rightarrow$ `v2.0.0`):** Incompatible API changes or structural database migrations.
- **MINOR (`v1.0.0` $\rightarrow$ `v1.1.0`):** New backwards-compatible features (e.g., adding Email Header BEC scanner).
- **PATCH (`v1.0.0` $\rightarrow$ `v1.0.1`):** Backwards-compatible bug fixes and security hotfixes.

### Release Tagging Workflow

```bash
# 1. Ensure main branch is up to date
git checkout main
git pull origin main

# 2. Create annotated Git Release Tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial GuardianAI Platform Launch"

# 3. Push Release Tag to GitHub
git push origin v1.0.0
```

---

## 4. Pull Request Review Gates & Merge Rules

To merge a Pull Request into `main`, the following **4 Hard Gates** must pass:
1. **Automated CI/CD Pass:** All unit tests (`make test`) and static linters (`make lint`) must pass.
2. **Code Owner Approval:** At least 1 review approval from an owner defined in `.github/CODEOWNERS`.
3. **No Secrets / Clean Audit:** Passing automated security audit confirming zero committed secrets or unscrubbed PII.
4. **Squash & Merge Execution:** PRs are squashed into a single clean conventional commit on `main` to maintain linear history.

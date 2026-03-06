# Test Coverage Check

Fires on every PR. Checks that all new server functions and validation logic are covered by tests.

## Universal Rules
- Every @anvil.server.callable function must have at least one happy path test in tests/test_{stage}_*.py
- Every validation function must have boundary and adversarial tests
- Local tests (pytest) cover pure logic only — no Anvil imports in test execution path
- Uplink tests cover all @anvil.server.callable functions against live app
- Test sentinel data uses TEST_ prefix — no production data in tests
- Cleanup verified after every uplink test run — no TEST_ rows remain
- test reports exist at tests/{stage}-test-local-report.yaml and tests/{stage}-test-uplink-report.yaml
- No test modifies a security check to achieve a pass — code is fixed, not the test

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `tests/1.2-auth/` directory must exist and contain at least one test file — flag if the directory is absent or empty
- `server_auth/service.py` — `validate_password_strength` (or equivalent pure function) must have a corresponding test file `tests/1.2-auth/test_auth_password_validation.py` covering: valid password passes, password too short fails, missing uppercase fails, missing lowercase fails, missing digit fails
- `server_auth/service.py` — `authenticate_user`, `create_user`, `reset_password`, `check_permission` must each have at least one happy path test in `tests/1.2-auth/test_auth_service.py` or equivalent
- `server_auth/rbac.py` — `require_role` and `require_permission` decorator logic must have pure-logic tests covering: correct role passes, wrong role raises, no user raises, correct permission passes, missing permission raises
- All test files in `tests/1.2-auth/` must contain zero `import anvil` statements — pure Python only
- Uplink test report must exist at `tests/1.2-auth-test-uplink-report.yaml` — flag if absent
- Local test report must exist at `tests/1.2-auth-test-local-report.yaml` — flag if absent
- Any test data written to Data Tables during uplink tests must use `source='Test'` sentinel — flag any uplink test that creates rows without this field set

Pass if: `tests/1.2-auth/` exists with test files for password validation, all four service functions, and both RBAC decorators; no test file imports `anvil`; both report files are present; and all uplink test data uses `source='Test'`.

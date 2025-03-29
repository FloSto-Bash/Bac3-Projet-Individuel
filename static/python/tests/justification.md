## Justification for the Absence of Unit Tests for `worker.py` and `main.py`

### Context

The `worker.py` and `main.py` files rely on `pyscript.document` and `pyscript.window`, which are only available in a browser environment. Standard Python testing frameworks cannot access these objects.

### Issues

1. Dependency on PyScript and the DOM
    `pyscript.document` and `pyscript.window` interact with the browser DOM, which is unavailable during unit tests.

2. Limited Mocking Capability
    While `unittest.mock` could simulate these objects, it wouldn't replicate real browser behavior.
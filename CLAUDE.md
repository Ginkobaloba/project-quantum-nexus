# project-quantum-nexus -- AI Instructions

**Owner:** Drew Mattick (dramattick1@gmail.com, GitHub: Ginkobaloba)
**Project:** Quantum-enhanced computational methods for distributed power system intelligence
**Status:** Early scaffold, demo-focused, not production

---

## Session protocol

This project follows `C:\dev\SESSION_PROTOCOL.md`. Every AI session MUST:

1. Read `C:\dev\SESSION_PROTOCOL.md`
2. Read this file (`CLAUDE.md`)
3. Read the most recent `docs/handoffs/HANDOFF_*.md` (skip `template.md`)
4. Run `vstart` before making changes
5. At session end: write a handoff doc, then run `vend`

---

## Project context

This is one of three connected projects:

- **project-vector** -- autonomous mobile perception platform for building management.
  Has a provisional patent. DO NOT expose patent-protected methods or architectures
  in this repo. Quantum-nexus provides analytical methods that are MIT-licensed and
  independent of the patented systems.
- **nexus** -- distributed AI architecture. Quantum-nexus modules are designed to
  plug into Nexus as service nodes.
- **project-quantum-nexus** (this repo) -- quantum-enhanced analytical methods.
  MIT licensed. All code here must be publishable.

### Patent boundary

The quantum methods themselves (VQE for state estimation, QAOA for scheduling,
quantum kernels for anomaly detection) are open research techniques. What is
protected is Vector's specific architecture for zone association, spatial
intelligence, and autonomous navigation.

Rule of thumb: if the code references Vector-specific data structures, spatial
models, or zone-association logic, it belongs in project-vector, not here. This
repo works with generic power system models and simulated sensor data.

---

## Tech stack

- Python 3.10+
- Qiskit 1.0+ (circuits, Aer simulator, optimization)
- Target: IBM open-access quantum hardware
- All demos default to Aer simulator -- real hardware is opt-in

---

## Code standards

- PEP 8, enforced by ruff and black (line length 100)
- Type hints on all public functions
- Docstrings on all modules, classes, and public functions
- Tests for anything that computes a result
- Snake_case for Python files (PEP 8), lowercase-with-hyphens for docs
- No em dashes -- use double-dashes, parentheses, or commas

---

## Style

- Casual, confident, technically precise
- No corporate fluff, no AI-speak, no marketing language
- Dark humor in code comments is welcome
- Translate quantum concepts into plain language where possible
- Be honest about what's a toy demo vs. what could actually scale

---

## Architecture decisions

Document significant decisions in `docs/architecture.md`. Follow ADR format
when the decision has real tradeoffs worth recording.

---

## What not to do

- Don't push to GitHub without Drew's explicit approval
- Don't add real IBM Quantum API tokens to any file (use env vars)
- Don't claim quantum advantage -- we're exploring, not selling
- Don't mix patent-protected Vector code into this repo

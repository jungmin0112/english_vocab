# Repository Guidelines

## Project Structure & Module Organization

- `quiz.py` contains JSON loading, validation, grading, console interaction, and self-assessment (F-03–F-06).
- `tests/test_quiz.py` holds automated tests; `tests/fixtures/words.json` is shared sample data.
- Read `README.md` for execution instructions, `docs/quiz-design.md` before changing behavior or interfaces, and `GLOSSARY.md` for domain terminology.
- Review scheduling, FSRS updates, and persistence remain integration work. Keep their responsibilities separate from quiz interaction.

## Build, Test, and Development Commands

Use Python 3.11 and an independent virtual environment per worktree. This branch currently uses only the standard library; no build step is required.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -X utf8 quiz.py tests/fixtures/words.json --demo
.\.venv\Scripts\python.exe -X utf8 quiz.py tests/fixtures/words.json run apple
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
```

These commands create the environment, run a sample quiz, run explicitly selected words, and execute tests. On macOS/Linux, create the environment with `python3.11 -m venv .venv` and use `.venv/bin/python`.

## Coding Style & Naming Conventions

Use four-space indentation, `snake_case` functions and variables, and descriptive names. Prefer straightforward control flow suitable for Python beginners. Keep Korean console messages and explanatory docstrings consistent. No formatter or linter is configured.

Preserve the JSON contract: lowercase, trimmed English keys map to objects containing nonempty `meanings` lists. Preserve original answers for display; normalize whitespace only for comparisons. Keep input data unchanged during quizzes.

## Testing Guidelines

Use standard-library `unittest`, `test_*.py` filenames, and `test_*` methods. No numeric coverage threshold is configured. Cover changed behavior, including invalid JSON, multiple meanings, whitespace, empty answers, duplicate selection, the 15-question limit, rating changes, and cancellation. Inject `read`/`write` callbacks for deterministic interaction tests. Run the suite after code changes and report untested integration paths explicitly.

## Commit & Pull Request Guidelines

History includes `feat: implement JSON-based vocabulary quiz`; follow that concise, imperative style. Keep commits focused. PR descriptions should explain behavior changes, relevant requirement IDs, executed tests, and remaining integration limitations. Link related issues when available; console changes benefit from sample output.

## Collaboration & Data Protection

Check branch and working-tree status before editing; preserve existing changes. Agree on shared data and function contracts with both contributors before integration. Keep personal records under ignored `data/`; exclude `.venv/` and credentials. Agents must obtain explicit authorization for commits, pushes, PR creation, or merges. Update design documentation when implementation contracts change.

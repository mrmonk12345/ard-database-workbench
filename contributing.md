# Contributing

This document is a short outline for contributing to the ARD Database Workbench.

## Getting started

The working project is located on the HPC and is already connected to the GitHub repository.
The required Conda environments are also already available there. Changes should eventually be
tested in this HPC copy before they are added to `main`.

For development, clone the GitHub repository to your working computer and create a new branch:

```bash
git clone git@github.com:mrmonk12345/ard-database-workbench.git
cd ard-database-workbench
git checkout -b <branch-name>
```

Review the README and relevant documentation before making changes.

## Adding Python scripts

- Place Python scripts in `scripts/python/`.
- Follow the existing naming and argument patterns.
- Document the script's purpose, inputs, outputs, and database tables it changes.
- Add or update a shell wrapper when the script is normally run as part of a workflow.

## Adding GUI Python scripts

- Place GUI code in `gui/`.
- Follow the existing PyQt6 patterns for windows, dialogs, widgets, and layouts.
- Keep database operations separate from display and user-interface code when possible.
- Add new windows or actions to the appropriate existing GUI module and update the README or
	related documentation when the user workflow changes.
- Test the GUI through the existing entry point, `gui/main.py`.

## Adding shell scripts

- Place shell scripts in `scripts/shell/`.
- Keep configuration and user-editable parameters clear.
- Call the relevant Python script or external tool consistently.
- Update [shell_scripts.md](shell_scripts.md) with a short description and usage notes.

## Making changes

- Keep changes focused and avoid committing databases, raw sequencing files, or private data.
- Update the relevant documentation when behavior or file locations change.
- Test the change with a small example or the appropriate project workflow.
- Check the Git diff before committing.

## External tools

Use the official documentation for tools used by the project:

- [PyQt6 for Python](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt for Python](https://doc.qt.io/qtforpython-6/)
- [QIIME 2 documentation](https://docs.qiime2.org/)
- [SQLite documentation](https://www.sqlite.org/docs.html)

## GitHub workflow

1. Clone the GitHub repository and create a new branch.
2. Make the script or documentation changes on that branch.
3. Test the changes locally when possible.
4. Commit the changes with a clear message.
5. Push the branch to GitHub.
6. On the HPC, pull the branch and check it out in the existing project directory, test the changes there.
7. After the HPC test succeeds, merge the branch into `main` and push `main` to GitHub.

The branch should be tested on the HPC before it is merged into `main`. Do not make changes
directly on `main` unless there is a specific reason to do so.

## Before submitting

- [ ] The script or documentation has a clear purpose.
- [ ] Paths and commands work.
- [ ] Related documentation is updated.
- [ ] No private data or unnecessary generated files are included.


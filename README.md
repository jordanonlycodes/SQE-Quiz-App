# 🎯 Quiz App
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![Test Coverage](https://img.shields.io/badge/Test%20Coverage-93%25-brightgreen)
![Tests](https://github.com/Glover012/quiz-app/actions/workflows/tests.yml/badge.svg?branch=main)
![Commits](https://img.shields.io/github/commit-activity/t/Glover012/quiz-app?label=Commits)
![Pull Requests](https://img.shields.io/github/issues-search/Glover012/quiz-app?query=is%3Apr&label=Pull%20Requests)
![License](https://img.shields.io/github/license/Glover012/quiz-app)

A desktop quiz application built with Python and a PySide6 GUI, evolved from a simple [console quiz application](https://github.com/Glover012/mini-project-collection/blob/main/content/Python/mini-projects/console/04_quiz/quiz.py).

## 🚀 Table of contents
- [📘 About the project](#-about-the-project)
- [🧩 What this project demonstrates](#-what-this-project-demonstrates)
- [✨ Features](#-features)
- [🎬 Demo](#-demo)
- [🔄 Application data flow](#-application-data-flow)
- [🛠️ Technical highlights](#️-technical-highlights)
- [🧠 What I learned](#-what-i-learned)
- [📋 Requirements](#-requirements)
- [⚙️ Installation](#️-installation)
    - [💻 Windows PowerShell](#-windows-powershell)
- [🔧 Configuration](#-configuration)
    - [💻 Logging level in Windows PowerShell](#-logging-level-in-windows-powershell)
- [▶️ Running app](#️-running-app)
- [🗂️ Project structure](#️-project-structure)
- [📌 Project status](#-project-status)
- [🚧 Known limitations](#-known-limitations)
- [🛣 Roadmap](#-roadmap)
  - [✅ Completed](#-completed)
  - [📝 Planned](#-planned)
- [🧪 Tests](#-tests)
  - [🤖 CI](#-ci)
  - [💻 Running tests with coverage in Windows PowerShell](#-running-tests-with-coverage-in-windows-powershell)
- [⚠️ Error triggers](#️-error-triggers)
  - [🚨 Error Trigger Table](#-error-trigger-table)
- [📄 License](#-license)
- [👤 Author contact](#-author-contact)
- [⭐ Support](#-support)

## 📘 About the project
This project started as a simple [console quiz application](https://github.com/Glover012/mini-project-collection/blob/main/content/Python/mini-projects/console/04_quiz/quiz.py) and gradually evolved into a structured desktop app with GUI screens, external API integration, background loading, custom error handling, logging, automated tests, CI and project documentation.

Initially, the main goal was to build a simple application with a GUI. However, the development of this app took an unexpected turn. As the project grew, it was refactored multiple times for different reasons, but the main one was often: "let's just improve this small thing".

Over time, the app evolved on many levels: code quality, project structure, error handling, tests, CI, threaded question loading and overall maintainability.

Now, this project shows my learning process, code evolution, project structure improvements and the amount of work put into developing and refactoring a real application over time.

## 🧩 What this project demonstrates
- Iterative development: from a console quiz to a structured desktop GUI application
- Python project organization with separated GUI, worker, API and question logic modules
- GUI development with PySide6, Qt signals and QThread-based background loading
- External API integration with timeout handling, custom exceptions and user-facing error states
- Automated testing with pytest, pytest-qt and mocked HTTP responses
- CI setup with GitHub Actions for automated test runs
- Documentation of application flow, project structure and technical decisions

## ✨ Features
- GUI built with PySide6
- Threaded question loading from the Open Trivia Database API
- Selectable number of questions, category, difficulty and question type
- Score calculation based on question difficulty
- Visual feedback based on the user's answer
- Loading overlay while questions are being fetched
- Error overlay with user-facing error messages
- Visual feedback when a particular question parameter causes an error
- Per-session file logging

## 🎬 Demo
Additional widget screenshots are available in the [widget presentation](docs/images/widget-presentation.md).

![Quiz App Demo](docs/quiz-app-demo.gif)

## 🔄 Application data flow
The application data flow and module structure are described in [docs/application-data-flow.md](docs/application-data-flow.md).

## 🛠️ Technical highlights
- PySide6 desktop GUI with multiple application screens
- Background question loading handled with QThread and Qt signals
- OpenTDB API client with timeout handling and custom exceptions
- Per-session file logging with configurable console log level
- Clear separation between GUI widgets, worker classes and question logic
- Application data flow documented with a Mermaid diagram
- Backend tests covering API responses, error handling and question model behavior
- GUI tests with pytest-qt covering core widgets, signal wiring, loading states and error handling
- Tests run offline using mocked HTTP responses and static API response data

## 🧠 What I learned
- Building a desktop GUI application with PySide6
- Structuring a Python project into smaller, focused modules
- Separating GUI code, background workers, API access and data models
- Working with external API data and handling unreliable responses
- Using Qt signals and QThread for background question loading
- Writing cleaner, PEP 8-friendly Python code
- Adding type hints and TypedDict definitions for API responses and quiz parameters
- Creating and using custom data types
- Writing unit tests with unittest.mock, including mocked HTTP responses and patch decorators
- Writing backend tests with both unittest and pytest to compare testing styles in a real project
- Setting up GitHub Actions to run the test suite automatically
- Documenting application flow and architecture with Markdown and Mermaid
- Writing GUI tests with pytest and pytest-qt
- Testing Qt signals, widget state changes and user interactions
- Structuring GUI code so widgets can be tested in isolation

## 📋 Requirements
- Python 3.11+
- Internet connection for loading questions from the API

## ⚙️ Installation
Clone the repository and install the required dependencies in a virtual environment.

#### 💻 Windows PowerShell
```powershell
git clone https://github.com/Glover012/quiz-app.git
cd quiz-app
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 🔧 Configuration
The project uses an environment variable to control the logging level.

Supported logging level values:

- `DEBUG`
- `INFO`
- `WARNING`

The application also writes per-session log files to the `logs/` directory and keeps the most recent log files.

#### 💻 Logging level in Windows PowerShell
```powershell
$env:QUIZ_APP_LOG_LEVEL="DEBUG"
```

## ▶️ Running app
```powershell
python main.py
```

## 🗂️ Project structure
    quiz-app/
    ├── .github/                          # GitHub repository configuration
    │   └── workflows/                    # GitHub Actions workflows
    ├── docs/                             # Demo, screenshots and application data flow
    │   └── images/                       # Widget screenshots and presentation
    ├── modules/                          # Application source code
    │   ├── gui/                          # PySide6 GUI layer
    │   │   ├── menu_bar/                 # Application menu bar
    │   │   │   └── menus/
    │   │   ├── styles/                   # Qt stylesheet file
    │   │   ├── widgets/                  # GUI widgets
    │   │   │   ├── overlays/             # Loading and error overlays
    │   │   │   ├── question_display/     # Quiz question display screen
    │   │   │   │   └── components/
    │   │   │   └── start_display/        # Quiz setup/start screen
    │   │   │       └── components/
    │   │   └── workers/                  # Background worker and thread controller
    │   └── questions/                    # Quiz data, API parameters and OpenTDB client
    ├── tests/                            # Backend and GUI unit tests
    │   ├── data/                         # Static API response data
    │   ├── gui/                          # GUI tests written with pytest-qt
    │   ├── pytest_backend/               # Backend tests written with pytest
    │   └── unittest_backend/             # Backend tests written with unittest
    ├── .gitignore
    ├── CHANGELOG.md                      # Release history
    ├── LICENSE
    ├── main.py                           # Application entry point
    ├── README.md
    └── requirements.txt                  # Project dependencies

## 📌 Project status
The application is functional and stable. The main planned tasks have been completed. At the moment, additional code quality and maintenance improvements can be considered.

## 🚧 Known limitations
- The application depends on an internet connection and OpenTDB API availability.
- The app has been tested manually on Windows.

## 🛣 Roadmap

### ✅ Completed
- [x] Initial basic version
- [x] Add backend unit test coverage with unittest
- [x] Refactor application flow to use Qt signals
- [x] Move question loading out of the GUI layer into a dedicated thread
- [x] Add loading overlay
- [x] Add file logging
- [x] Add GitHub Actions test workflow
- [x] Add Changelog
- [x] Refactor the Questions model so its constructor does not immediately load questions from the API
- [x] Improve encapsulation in GUI modules
- [x] Add backend unit test coverage with pytest
- [x] Add pytest-qt coverage for core GUI widgets, signal wiring, and loading/error handling

### 📝 Planned
- [ ] Consider additional code quality and maintenance improvements

## 🧪 Tests
This repository includes a broad backend and GUI test suite focused on the application's most important behavior. The application uses `pytest` as the main test runner and `pytest-qt` for testing the GUI layer. Tests are located in their designated folders in `tests/`.

- `tests/unittest_backend` - contains backend tests written with Python's built-in `unittest`. This suite is not used and is kept for educational purposes.
- `tests/pytest_backend` - contains the main `pytest` backend tests.
- `tests/gui` - contains GUI tests written with `pytest` and `pytest-qt`.

**Backend tests** cover the OpenTDB API client and question model behavior, including:
- Request parameter handling, mocked API responses, and API error handling
- Invalid response formats, question object creation, and HTML entity decoding
- Answer list construction, answer shuffling, and point assignment
- Additional edge cases around API and model behavior

**GUI tests** focus on the core quiz widgets and application flow, including:
- Quiz parameter selection, start button behavior, and signal wiring
- Question loading signals, answer selection, and result calculation
- Error handling, loading overlay behavior, and screen switching
- Repeat quiz handling, close-event behavior, and MainWindow coordination
- Additional GUI-related behavior

Some fixtures are shared between tests. They are kept in their respective test modules instead of a shared `conftest.py` file to keep the test setup easier to read.

To avoid using external services, test coverage is measured locally with `pytest-cov`, and the README badge is updated manually.

### 🤖 CI
Tests are run automatically with GitHub Actions on pushes to `main` and `dev`, pull requests to `main`, and manual workflow runs.

### 💻 Running tests with coverage in Windows PowerShell
```powershell
python -m pytest tests --cov=modules --cov-report=term-missing
```

For unittest use:
```powershell
python -m unittest discover tests/unittest_backend
```

## ⚠️ Error triggers
The application allows selecting up to 100 questions, even though the Open Trivia Database API documentation states that up to 50 questions can be requested at once. This is intentional and is used to trigger error handling paths.

Some OpenTDB parameter combinations may return too few questions or no questions at all, which may be used to exercise the application's error handling flow.

### 🚨 Error Trigger Table
| Amount | Difficulty | Category | Type | Expected error |
| --- | --- | --- | --- | --- |
| 51-100 | Any difficulty | Any Category | Any type | Not enough questions found |
| 2 | Hard | Entertainment: Musicals & Theatres | True / False | No questions found |

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

## 👤 Author contact
- GitHub: https://github.com/Glover012
- E-mail: glover012-git@protonmail.com

## ⭐ Support
If you like this project, you can:
- Leave a star on GitHub
- Report an issue
- Suggest a new feature

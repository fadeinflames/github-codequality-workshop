# Code Quality Workshop - Шпаргалка

## Python - Линтеры

### Flake8

```bash
# Базовая проверка
flake8 app/ tests/

# С подсчетом статистики
flake8 app/ --statistics

# Только определенные ошибки
flake8 app/ --select=E501,W503

# Игнорировать ошибки
flake8 app/ --ignore=E501,W503

# HTML отчет
pip install flake8-html
flake8 app/ --format=html --htmldir=reports/flake8

# Сохранить в файл
flake8 app/ --output-file=flake8-report.txt
```

**Основные коды ошибок:**
- `E***` - PEP 8 errors
- `W***` - PEP 8 warnings
- `F***` - PyFlakes (логические ошибки)
- `C***` - McCabe complexity
- `N***` - PEP 8 naming

### Pylint

```bash
# Базовая проверка
pylint app/

# С конфигурацией
pylint app/ --rcfile=.pylintrc

# Только модуль
pylint app/user_service.py

# JSON отчет
pylint app/ --output-format=json > pylint.json

# HTML отчет (требует pylint-json2html)
pylint app/ --output-format=json | pylint-json2html -o pylint.html

# Показать все сообщения
pylint --list-msgs

# Игнорировать конкретные предупреждения
pylint app/ --disable=C0103,R0903
```

**Категории сообщений:**
- `C` - Convention (стиль)
- `R` - Refactor (рефакторинг)
- `W` - Warning (предупреждение)
- `E` - Error (ошибка)
- `F` - Fatal (критическая ошибка)

---

## Python - Форматтеры

### Black

```bash
# Проверить без изменений
black --check app/ tests/

# Показать diff
black --diff app/ tests/

# Отформатировать
black app/ tests/

# Конкретный файл
black app/user_service.py

# Целевая длина строки
black --line-length 100 app/

# Исключить папки
black app/ --exclude '/(\.git|\.venv)/'
```

**Конфигурация в pyproject.toml:**
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
```

### isort

```bash
# Проверить без изменений
isort --check-only app/ tests/

# Показать diff
isort --diff app/ tests/

# Отсортировать
isort app/ tests/

# Конкретный файл
isort app/user_service.py

# Профиль для совместимости с black
isort --profile black app/
```

**Конфигурация в pyproject.toml:**
```toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
```

---

## Python - Type Checking

### mypy

```bash
# Базовая проверка
mypy app/

# С конфигурацией
mypy app/ --config-file=mypy.ini

# HTML отчет
mypy app/ --html-report reports/mypy

# Игнорировать отсутствующие импорты
mypy app/ --ignore-missing-imports

# Строгий режим
mypy app/ --strict

# Проверить конкретный файл
mypy app/user_service.py

# JSON отчет
mypy app/ --no-error-summary --no-pretty \
  | python -c "import sys, json; print(json.dumps([line for line in sys.stdin]))"
```

**Конфигурация в mypy.ini:**
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

---

## Python - Security

### Bandit

```bash
# Базовая проверка
bandit -r app/

# JSON отчет
bandit -r app/ -f json -o bandit.json

# HTML отчет
bandit -r app/ -f html -o bandit.html

# XML отчет
bandit -r app/ -f xml -o bandit.xml

# Только высокий и средний уровень
bandit -r app/ -ll

# Исключить тесты
bandit -r app/ --exclude tests/

# Конфигурация
bandit -r app/ -c bandit.yml
```

**Уровни серьезности:**
- `LOW` - Низкий риск
- `MEDIUM` - Средний риск
- `HIGH` - Высокий риск

---

## JavaScript - Линтеры

### ESLint

```bash
# Базовая проверка
npm run lint
# или
eslint frontend/**/*.js

# Автоисправление
eslint frontend/**/*.js --fix
npm run lint:fix

# Конкретный файл
eslint frontend/user-client.js

# JSON отчет
eslint frontend/ -f json -o eslint-report.json

# HTML отчет
npm install -D eslint-html-reporter
eslint frontend/ -f node_modules/eslint-html-reporter/reporter.js \
  -o eslint-report.html

# Игнорировать правила
eslint frontend/ --rule 'no-console: off'
```

**Конфигурация в .eslintrc.json:**
```json
{
  "extends": ["airbnb-base", "prettier"],
  "rules": {
    "no-console": "off",
    "max-len": ["error", { "code": 100 }]
  }
}
```

### Prettier

```bash
# Проверить форматирование
npm run format:check
# или
prettier --check frontend/**/*.js

# Отформатировать
npm run format
# или
prettier --write frontend/**/*.js

# Конкретный файл
prettier --write frontend/user-client.js

# Список неотформатированных файлов
prettier --list-different frontend/**/*.js
```

**Конфигурация в .prettierrc.json:**
```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

---

## Testing & Coverage

### pytest

```bash
# Запуск всех тестов
pytest tests/ -v

# С покрытием
pytest tests/ --cov=app --cov-report=term-missing

# HTML отчет о покрытии
pytest tests/ --cov=app --cov-report=html

# XML отчет (для CI)
pytest tests/ --cov=app --cov-report=xml

# HTML отчет о тестах
pytest tests/ --html=reports/pytest.html --self-contained-html

# Конкретный тест
pytest tests/test_user_service.py::TestUser::test_create_valid_user

# Параллельно
pytest tests/ -n auto

# С маркерами
pytest tests/ -m "not slow"

# Подробный вывод при ошибках
pytest tests/ -vv --tb=long
```

### coverage

```bash
# Запуск с coverage
coverage run -m pytest tests/

# Отчет в терминал
coverage report

# С пропущенными строками
coverage report -m

# HTML отчет
coverage html

# XML отчет
coverage xml

# Объединить несколько отчетов
coverage combine

# Стереть данные
coverage erase

# Проверить порог
coverage report --fail-under=80
```

---

## Docker

```bash
# Сборка образа
docker build -t code-quality-workshop .

# Запуск контейнера
docker run -p 5000:5000 code-quality-workshop

# С переменными окружения
docker run -p 5000:5000 -e DEBUG=true code-quality-workshop

# С volume для отчетов
docker run -p 5000:5000 -v $(pwd)/reports:/app/reports code-quality-workshop

# Интерактивный режим
docker run -it code-quality-workshop /bin/bash

# Проверка логов
docker logs <container_id>

# Остановка
docker stop <container_id>

# Удаление образа
docker rmi code-quality-workshop
```

---

## GitHub Actions - Локальная проверка

### act (запуск workflows локально)

```bash
# Установка
# macOS: brew install act
# Linux: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Список workflows
act -l

# Запустить все jobs для push
act push

# Запустить конкретный workflow
act -W .github/workflows/01-linters.yml

# Запустить конкретный job
act -j python-lint

# С secrets
act -s GITHUB_TOKEN=your_token

# Dry run (без выполнения)
act -n
```

---

## Pre-commit Hooks

```bash
# Установка pre-commit
pip install pre-commit

# Установить hooks в репозиторий
pre-commit install

# Запустить на всех файлах
pre-commit run --all-files

# Запустить конкретный hook
pre-commit run black --all-files

# Обновить hooks
pre-commit autoupdate

# Удалить hooks
pre-commit uninstall

# Пропустить hooks при коммите
git commit --no-verify
```

**Пример .pre-commit-config.yaml:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

---

## Комплексные команды

### Полная проверка Python

```bash
#!/bin/bash
# check-python.sh

echo "Running Flake8..."
flake8 app/ tests/ || true

echo "Running Pylint..."
pylint app/ || true

echo "Checking Black formatting..."
black --check app/ tests/ || true

echo "Checking isort..."
isort --check-only app/ tests/ || true

echo "Running mypy..."
mypy app/ || true

echo "Running Bandit..."
bandit -r app/ || true

echo "All checks completed!"
```

### Полная проверка JavaScript

```bash
#!/bin/bash
# check-javascript.sh

echo "Running ESLint..."
npm run lint || true

echo "Checking Prettier..."
npm run format:check || true

echo "All checks completed!"
```

### Автоматическое исправление

```bash
#!/bin/bash
# auto-fix.sh

echo "Auto-fixing Python..."
black app/ tests/
isort app/ tests/

echo "Auto-fixing JavaScript..."
npm run format
npm run lint:fix

echo "Auto-fix completed!"
```

---

## Генерация всех отчетов

```bash
#!/bin/bash
# generate-reports.sh

mkdir -p reports/{flake8,pylint,mypy,bandit,coverage,pytest}

echo "Generating reports..."

# Flake8
flake8 app/ tests/ --format=html --htmldir=reports/flake8 || true

# Pylint
pylint app/ --output-format=json > reports/pylint/report.json || true
pylint app/ --output-format=text > reports/pylint/report.txt || true

# mypy
mypy app/ --html-report reports/mypy || true

# Bandit
bandit -r app/ -f html -o reports/bandit/report.html || true
bandit -r app/ -f json -o reports/bandit/report.json || true

# Coverage
pytest tests/ --cov=app --cov-report=html:reports/coverage \
  --cov-report=xml:reports/coverage/coverage.xml \
  --html=reports/pytest/report.html --self-contained-html

echo "All reports generated in ./reports/"
echo "Open reports/coverage/index.html for coverage"
echo "Open reports/pytest/report.html for test results"
```

---

## CI/CD - GitHub Actions

### Базовый workflow

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - run: pip install -r requirements.txt
      
      - name: Lint
        run: |
          flake8 app/ tests/
          pylint app/
      
      - name: Test
        run: pytest tests/ --cov=app
      
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
```

### Создание артефакта

```yaml
- name: Generate report
  run: pytest --html=report.html

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: test-report
    path: report.html
    retention-days: 30
```

### Скачивание артефакта

```yaml
- name: Download artifact
  uses: actions/download-artifact@v4
  with:
    name: test-report
    path: ./reports
```

---

## Полезные алиасы

Добавьте в `.bashrc` или `.zshrc`:

```bash
# Python quality checks
alias pylint-all="pylint app/"
alias flake8-all="flake8 app/ tests/"
alias black-check="black --check app/ tests/"
alias black-fix="black app/ tests/"
alias isort-check="isort --check-only app/ tests/"
alias isort-fix="isort app/ tests/"
alias mypy-all="mypy app/"
alias bandit-all="bandit -r app/"

# Combined checks
alias check-py="flake8-all && pylint-all && black-check && isort-check && mypy-all"
alias fix-py="black-fix && isort-fix"

# Testing
alias test="pytest tests/ -v"
alias test-cov="pytest tests/ --cov=app --cov-report=html"
alias test-fast="pytest tests/ -x -v"  # stop on first failure

# JavaScript
alias lint-js="npm run lint"
alias fix-js="npm run lint:fix && npm run format"

# Docker
alias docker-build="docker build -t code-quality-workshop ."
alias docker-run="docker run -p 5000:5000 code-quality-workshop"

# Reports
alias open-cov="open htmlcov/index.html"  # macOS
# alias open-cov="xdg-open htmlcov/index.html"  # Linux
```

---

## Чек-лист Code Review

```markdown
### Code Quality Checklist

#### Форматирование
- [ ] Black отработал без ошибок
- [ ] isort отсортировал импорты
- [ ] Prettier отформатировал JS

#### Линтинг
- [ ] Flake8: 0 ошибок
- [ ] Pylint: score > 9.0
- [ ] ESLint: 0 ошибок

#### Типы
- [ ] mypy: 0 ошибок
- [ ] Type hints добавлены для новых функций

#### Безопасность
- [ ] Bandit: 0 критических проблем
- [ ] Нет hardcoded secrets

#### Тесты
- [ ] Все тесты проходят
- [ ] Coverage не упал
- [ ] Добавлены тесты для новой функциональности

#### Документация
- [ ] Docstrings добавлены
- [ ] README обновлен при необходимости
- [ ] CHANGELOG обновлен
```

---

## Troubleshooting

### Конфликт между Black и Flake8

```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, E501, W503
```

### Конфликт между Black и isort

```toml
# pyproject.toml
[tool.isort]
profile = "black"
```

### mypy не находит модули

```ini
# mypy.ini
[mypy-flask.*]
ignore_missing_imports = True
```

### Медленные тесты

```bash
# Запуск параллельно
pytest tests/ -n auto

# Только быстрые тесты
pytest tests/ -m "not slow"
```

---

## Полезные ссылки

- **Flake8:** https://flake8.pycqa.org/
- **Pylint:** https://pylint.pycqa.org/
- **Black:** https://black.readthedocs.io/
- **isort:** https://pycqa.github.io/isort/
- **mypy:** https://mypy.readthedocs.io/
- **Bandit:** https://bandit.readthedocs.io/
- **ESLint:** https://eslint.org/
- **Prettier:** https://prettier.io/
- **pytest:** https://docs.pytest.org/
- **pre-commit:** https://pre-commit.com/

---

## Quick Start

```bash
# 1. Установка всех инструментов
pip install -r requirements.txt
npm install

# 2. Проверка всего
flake8 app/ tests/
pylint app/
black --check app/ tests/
isort --check app/ tests/
mypy app/
bandit -r app/
npm run lint

# 3. Автоисправление
black app/ tests/
isort app/ tests/
npm run format
npm run lint:fix

# 4. Тесты с coverage
pytest tests/ --cov=app --cov-report=html

# 5. Открыть отчет
open htmlcov/index.html
```

---

**Сохраните эту шпаргалку - она пригодится!**

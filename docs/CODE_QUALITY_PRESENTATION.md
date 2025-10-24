---
marp: true
---

# Code Quality Workshop - Презентация

---

## Слайд 1: Титульный

# Статический анализ кода и артефакты в CI
## Настройка автоматических проверок качества

**Практический воркшоп**

DevOps Course

---

## Слайд 2: Что мы изучим

- Интеграция линтеров в CI-процесс
- Автоматическое форматирование кода
- Проверка типов и безопасности
- Работа с артефактами
- Визуализация и отчеты

**Формат:** 80% практики, 20% теории

---

## Слайд 3: Проблема

### Без статического анализа:

```
Developer → Write Code → Commit → Review [FAIL]
            ↓
        Стиль разный
        Баги не найдены
        Типы не проверены
        Уязвимости пропущены
```

### Со статическим анализом:

```
Developer → Write → Auto-check [OK] → Auto-format [OK] → Commit → CI [OK]
                     ↓              ↓                        ↓
                  Линтеры      Форматтеры             Отчеты
```

---

## Слайд 4: Что такое статический анализ?

**Статический анализ** = проверка кода без его выполнения

### Находит:
- Потенциальные баги
- Проблемы со стилем кода
- Уязвимости безопасности
- Сложный код
- Неоптимальные конструкции
- Отсутствие документации

### Преимущества:
- Быстро (секунды)
- Не требует запуска
- Находит проблемы до production

---

## Слайд 5: Категории инструментов

```
┌─────────────────────────────────────┐
│        Статический анализ           │
├─────────────────────────────────────┤
│                                     │
│  1. Линтеры                         │
│     └─ Проверка стиля и ошибок     │
│                                     │
│  2. Форматтеры                      │
│     └─ Автоматическое оформление   │
│                                     │
│  3. Type Checkers                   │
│     └─ Проверка типов              │
│                                     │
│  4. Security Scanners               │
│     └─ Поиск уязвимостей           │
│                                     │
└─────────────────────────────────────┘
```

---

## Слайд 6: Python - Линтеры

### Flake8
```bash
flake8 app/
# E501: line too long
# F401: imported but unused
# W503: line break before operator
```

**Что проверяет:**
- PEP 8 compliance
- Синтаксические ошибки
- Неиспользуемые импорты
- Длина строк

---

## Слайд 7: Python - Линтеры (продолжение)

### Pylint
```bash
pylint app/
# C0103: Invalid name
# R0913: Too many arguments
# W0612: Unused variable
```

**Что проверяет:**
- Качество кода
- Соглашения об именовании
- Сложность кода
- Потенциальные ошибки
- Рефакторинг opportunities

**Оценка:** 0-10 баллов

---

## Слайд 8: Python - Форматтеры

### Black - "The Uncompromising Code Formatter"

```python
# До
def very_long_function_name(param1,param2,param3,param4):
    x=param1+param2
    return x

# После Black
def very_long_function_name(
    param1, param2, param3, param4
):
    x = param1 + param2
    return x
```

**Философия:** Нет дискуссий о стиле - Black решает за вас

---

## Слайд 9: Python - Форматтеры (продолжение)

### isort - Сортировка импортов

```python
# До
import os
from flask import Flask
import sys
from app.models import User
import json

# После isort
import json
import os
import sys

from flask import Flask

from app.models import User
```

**Группы:** FUTURE → STDLIB → THIRDPARTY → FIRSTPARTY → LOCALFOLDER

---

## Слайд 10: Python - Type Checking

### mypy - Статическая проверка типов

```python
# Код с type hints
def add_user(name: str, age: int) -> User:
    return User(name, age)

# mypy найдет ошибку:
add_user("Alice", "25")  # [FAIL] Expected int, got str

# mypy одобрит:
add_user("Alice", "25")  # [FAIL] Expected int, got str

# С type checking:
add_user("Alice", 25)    # [OK] Correct types
```

**Преимущества:**
- Ловит ошибки до runtime
- Улучшает автодополнение IDE
- Документация в коде

---

## Слайд 11: Python - Security

### Bandit - Поиск уязвимостей

```python
# Bandit найдет проблемы:

import pickle  # B403: pickle unsafe

password = "hardcoded123"  # B105: hardcoded password

os.system(user_input)  # B605: shell injection risk

requests.get(url, verify=False)  # B501: SSL verification disabled
```

**Проверяет:**
- SQL injection
- Command injection
- Hardcoded secrets
- Crypto issues

---

## Слайд 12: JavaScript - Линтеры

### ESLint

```javascript
# Проблемы в коде:

var x = 1;  // [FAIL] Unexpected var, use const/let

function foo(){  // [FAIL] Missing space before {
  console.log(x)  // [FAIL] Missing semicolon
}

if(x=1){  // [FAIL] Assignment in condition
```

**Правила:** 250+ встроенных правил

---

## Слайд 13: JavaScript - Форматтеры

### Prettier - Opinionated Code Formatter

```javascript
// До
const user={name:"Alice",age:25,email:"alice@example.com"};
function greet(name){console.log("Hello "+name)}

// После Prettier
const user = {
  name: "Alice",
  age: 25,
  email: "alice@example.com",
};

function greet(name) {
  console.log("Hello " + name);
}
```

**Интеграция:** Работает с ESLint

---

## Слайд 14: Конфигурационные файлы

### Python:
```
.pylintrc          # Pylint config
.flake8            # Flake8 config
mypy.ini           # mypy config
pyproject.toml     # Black + isort + pytest
```

### JavaScript:
```
.eslintrc.json     # ESLint config
.prettierrc.json   # Prettier config
package.json       # Scripts
```

**Цель:** Единообразие в команде

---

## Слайд 15: Интеграция в CI - Workflow

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Lint with Flake8
        run: |
          pip install flake8
          flake8 app/ tests/
```

---

## Слайд 16: Артефакты - Что это?

**Артефакт** = файл или набор файлов, сохраненный после workflow

### Примеры артефактов:

- HTML отчеты (coverage, lint)
- JSON/XML результаты
- Скриншоты тестов
- Логи выполнения
- Метрики производительности

**Хранение:** 90 дней по умолчанию (настраивается)

---

## Слайд 17: Создание артефактов

```yaml
- name: Generate coverage report
  run: |
    pytest --cov=app --cov-report=html

- name: Upload coverage
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: htmlcov/
    retention-days: 30
```

**Результат:** Отчет доступен для скачивания в GitHub UI

---

## Слайд 18: Скачивание артефактов

```yaml
- name: Download artifact
  uses: actions/download-artifact@v4
  with:
    name: coverage-report
    path: ./reports
```

**Использование:**
- Передача между jobs
- Анализ результатов
- Deployment артефактов

---

## Слайд 19: Типы отчетов

### Coverage Report (HTML)
```
htmlcov/
├── index.html           # Главная страница
├── app_service.html     # Покрытие модуля
└── style.css
```

### Lint Report (JSON)
```json
{
  "file": "app/service.py",
  "line": 42,
  "message": "Line too long",
  "severity": "warning"
}
```

### Test Report (JUnit XML)
```xml
<testsuite tests="15" failures="0" errors="0">
  <testcase name="test_user_creation"/>
</testsuite>
```

---

## Слайд 20: Визуализация отчетов

### HTML Reports:
- Красивый UI
- Интерактивность
- Графики и таблицы
- Drill-down по файлам

### JSON Reports:
- Машиночитаемые
- Интеграция с API
- Автоматическая обработка
- Trending analysis

---

## Слайд 21: Комментарии в PR

```yaml
- name: Comment PR
  uses: actions/github-script@v7
  with:
    script: |
      const coverage = fs.readFileSync('coverage.txt', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## Coverage Report\n\n${coverage}`
      });
```

**Результат:** Автоматический комментарий с метриками в PR

---

## Слайд 22: Quality Gate

```yaml
quality-gate:
  needs: [lint, test, security]
  runs-on: ubuntu-latest
  steps:
    steps:
      - name: Summary
        run: |
        echo "All checks passed!"
        echo "Lint: PASSED"
        echo "Tests: PASSED"
        echo "Security: PASSED"
```

**Quality Gate** = точка принятия решения о качестве

---

## Слайд 23: Параллельное выполнение

```yaml
jobs:
  python-lint:    # Выполняется параллельно
    ...
  
  python-format:  # Выполняется параллельно
    ...
  
  js-lint:        # Выполняется параллельно
    ...
  
  quality-gate:   # Ждет все предыдущие
    needs: [python-lint, python-format, js-lint]
    ...
```

**Преимущество:** Быстрее в 3-5 раз

---

## Слайд 24: Best Practices

### DO:

- Запускай проверки локально (pre-commit)

---

## Слайд 25: Best Practices (продолжение)

### DON'T:

- Не игнорируйте предупреждения
- Не коммитьте неотформатированный код
- Не отключайте проверки без причины
- Не сохраняйте артефакты вечно
- Не делайте проверки слишком строгими сразу
- Не забывайте про JavaScript

---

## Слайд 26: Метрики качества

### Что измерять:

| Метрика | Хорошо | Отлично |
|---------|--------|---------|
| **Coverage** | > 70% | > 90% |
| **Pylint Score** | > 7.0 | > 9.0 |
| **Complexity** | < 15 | < 10 |
| **Security Issues** | 0 high | 0 any |
| **Type Hints** | > 50% | 100% |

---

## Слайд 27: Roadmap внедрения

### Неделя 1-2: Базовая настройка
- Установить линтеры локально
- Настроить конфигурации
- Интегрировать в IDE

### Неделя 3-4: CI/CD
- Добавить в GitHub Actions
- Настроить артефакты
- Создать отчеты

### Неделя 5-6: Команда
- Обучить команду
- Настроить pre-commit hooks
- Установить quality gates

### Неделя 7-8: Оптимизация
- Анализ метрик
- Тюнинг правил
- Автоматизация

---

## Слайд 28: Pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

**Установка:**
```bash
pip install pre-commit
pre-commit install
```

**Результат:** Проверки ДО коммита

---

## Слайд 29: Интеграции

### GitHub Actions + External Services:

- **SonarQube** - качество кода
- **CodeClimate** - метрики и тренды
- **Codecov** - визуализация coverage
- **Snyk** - безопасность зависимостей
- **Dependabot** - обновление зависимостей

**API:** Отправка JSON отчетов

---

## Слайд 30: Архитектура решения

```
┌─────────────┐
│  Developer  │
└──────┬──────┘
       │ git push
       ↓
┌─────────────────────────────┐
│      GitHub Actions         │
├─────────────────────────────┤
│  ┌────────┐  ┌──────────┐  │
│  │ Lint   │  │  Format  │  │
│  └────────┘  └──────────┘  │
│  ┌────────┐  ┌──────────┐  │
│  │ Types  │  │ Security │  │
│  └────────┘  └──────────┘  │
└──────────┬──────────────────┘
           │
           ↓
    ┌──────────────┐
    │  Artifacts   │
    │  ┌────────┐  │
    │  │ HTML   │  │
    │  │ JSON   │  │
    │  │ XML    │  │
    │  └────────┘  │
    └──────────────┘
```

---

## Слайд 31: Пример полного pipeline

```yaml
name: Complete Quality Pipeline

jobs:
  lint:           # 1. Проверка стиля
  format:         # 2. Проверка форматирования
  types:          # 3. Проверка типов
  security:       # 4. Проверка безопасности
  test:           # 5. Тесты
  coverage:       # 6. Покрытие
  artifacts:      # 7. Сохранение отчетов
  quality-gate:   # 8. Финальная проверка
```

**Время выполнения:** ~5-10 минут (параллельно)

---

## Слайд 32: Демонстрация отчетов

### Coverage Report:
- Цветная подсветка кода
- Покрытие по файлам
- Непокрытые строки
- Статистика по модулям

### Flake8 Report:
- Список всех проблем
- Группировка по файлам
- Severity levels
- Быстрая навигация

### Bandit Report:
- Уровни риска (High/Medium/Low)
- Описание уязвимостей
- Рекомендации по исправлению

---

## Слайд 33: ROI статического анализа

### Экономия времени:
- Review быстрее на 30-50%
- Меньше багов в production
- Меньше итераций review

### Улучшение качества:
- Coverage растет
- Единый стиль кода
- Меньше уязвимостей

### Экономия денег:
- 1 час настройки = 10 часов сэкономленного review
- Быстрее time-to-market
- Довольные разработчики

---

## Слайд 34: Проблемы и решения

### Проблема: "Слишком много предупреждений"
**Решение:** Начинайте постепенно, отключите строгие правила

### Проблема: "CI слишком долго"
**Решение:** Кэширование + параллелизация

### Проблема: "Команда сопротивляется"
**Решение:** Покажите выгоды, автоматизируйте форматирование

### Проблема: "Конфликты между инструментами"
**Решение:** Используйте совместимые конфигурации (Black + Flake8)

---

## Слайд 35: Практическое задание

### Задание на воркшопе:

1. **Форкните проект**
2. **Добавьте новый endpoint** в API
3. **Напишите тесты**
4. **Создайте PR**
5. **Посмотрите на проверки:**
   - Линтеры должны пройти
   - Форматирование должно быть правильным
   - Coverage не должен упасть
6. **Скачайте артефакты** с отчетами

**Время:** 15 минут

---

## Слайд 36: Ресурсы для изучения

### Документация:
- [Flake8](https://flake8.pycqa.org/)
- [Pylint](https://pylint.pycqa.org/)
- [Black](https://black.readthedocs.io/)
- [mypy](https://mypy.readthedocs.io/)
- [Bandit](https://bandit.readthedocs.io/)
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)

### Книги:
- "Clean Code" - Robert Martin
- "The Art of Readable Code" - Boswell & Foucher

---

## Слайд 37: GitHub Actions - Artifacts API

### Upload:
```yaml
uses: actions/upload-artifact@v4
with:
  name: my-artifact
  path: reports/
  retention-days: 30
  if-no-files-found: error
```

### Download:
```yaml
uses: actions/download-artifact@v4
with:
  name: my-artifact
  path: ./downloaded
```

---

## Слайд 38: Advanced - Matrix + Artifacts

```yaml
strategy:
  matrix:
    python: ['3.9', '3.10', '3.11']

steps:
  - name: Test
    run: pytest --html=report-${{ matrix.python }}.html
  
  - name: Upload
    uses: actions/upload-artifact@v4
    with:
      name: report-python-${{ matrix.python }}
      path: report-*.html
```

**Результат:** Отдельный отчет для каждой версии

---

## Слайд 39: Continuous Quality

```
┌──────────────────────────────────────┐
│   Continuous Quality Improvement    │
├──────────────────────────────────────┤
│                                      │
│  Measure → Analyze → Improve → ↺    │
│     ↓          ↓          ↓          │
│  Metrics   Trends    Actions        │
│                                      │
│  Weekly reports                      │
│  Monthly reviews                     │
│  Quarterly goals                     │
│                                      │
└──────────────────────────────────────┘
```

**Цель:** Постоянное улучшение качества

---

## Слайд 48: Что мы изучили

Линтеры (Flake8, Pylint, ESLint)  
Форматтеры (Black, isort, Prettier)  
Type Checking (mypy)  
Security (Bandit)  
Артефакты в GitHub Actions  
Генерацию отчетов  
Визуализацию результатов  
Quality Gates  

---

## Слайд 41: Следующие шаги

### После воркшопа:

1. **Сегодня:**
   - Форкните проект
   - Попробуйте все инструменты

2. **На этой неделе:**
   - Настройте в своем проекте
   - Добавьте в CI/CD

3. **В этом месяце:**
   - Обучите команду
   - Установите quality gates
   - Соберите метрики

4. **Далее:**
   - Анализируйте тренды
   - Оптимизируйте правила
   - Делитесь опытом!

---

## Слайд 42: Вопросы?

# Спасибо за внимание!

**Материалы воркшопа:**
- GitHub: github.com/username/code-quality-workshop
- Документация: README.md
- Примеры: .github/workflows/

**Контакты:**
- Email: [ваш email]
- Telegram: [ваш telegram]

**Feedback приветствуется!**

---

## Бонус: Чек-лист внедрения

```markdown
□ Установить линтеры локально
□ Настроить конфигурационные файлы
□ Добавить в IDE
□ Создать GitHub Actions workflows
□ Настроить артефакты
□ Генерировать HTML отчеты
□ Добавить комментарии в PR
□ Установить quality gates
□ Настроить pre-commit hooks
□ Обучить команду
□ Собирать метрики
□ Регулярно review правил
```

---

## Бонус: Quick Start Commands

```bash
# Python
pip install flake8 pylint black isort mypy bandit
flake8 app/
pylint app/
black app/
isort app/
mypy app/
bandit -r app/

# JavaScript
npm install -D eslint prettier
npm run lint
npm run format

# Отчеты
pytest --cov=app --cov-report=html
flake8 app/ --format=html --htmldir=reports/
```

---

## Бонус: .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-prettier
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx]
```

**Установка:**
```bash
pre-commit install
```

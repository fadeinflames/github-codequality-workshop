# Code Quality Workshop

Воркшоп по настройке статического анализа кода и работе с артефактами в CI/CD.

![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![Node](https://img.shields.io/badge/node-20-brightgreen)

## Описание проекта

Учебный проект для демонстрации интеграции инструментов статического анализа кода и работы с артефактами в GitHub Actions.

### Что демонстрируется:

1. **Линтеры** - автоматическая проверка качества кода
2. **Форматтеры** - автоматическое форматирование кода
3. **Type Checkers** - проверка типов
4. **Security Scanners** - поиск уязвимостей
5. **Артефакты** - сохранение и использование отчетов
6. **Визуализация** - HTML отчеты и dashboard

## Структура проекта

```
code-quality-workshop/
├── app/                      # Python приложение
│   ├── user_service.py      # Бизнес-логика
│   └── api.py               # Flask REST API
│
├── frontend/                 # JavaScript код
│   └── user-client.js       # API клиент
│
├── tests/                    # Тесты
│   ├── test_user_service.py # Unit тесты
│   └── test_api.py          # Integration тесты
│
├── .github/workflows/        # GitHub Actions
│   ├── 01-linters.yml       # Линтеры
│   ├── 02-formatting.yml    # Форматирование
│   ├── 03-types-security.yml# Типы и безопасность
│   ├── 04-artifacts-reports.yml # Артефакты
│   └── 05-production.yml    # Production pipeline
│
├── reports/                  # Отчеты (генерируются)
│
└── docs/                     # Документация
    ├── WORKSHOP_SCENARIO.md
    ├── INSTRUCTOR_GUIDE.md
    └── CHEATSHEET.md
```

## Инструменты статического анализа

### Python:

| Инструмент | Назначение | Конфигурация |
|------------|-----------|--------------|
| **Flake8** | Проверка стиля кода (PEP 8) | `.flake8` |
| **Pylint** | Глубокий статический анализ | `.pylintrc` |
| **Black** | Автоформатирование кода | `pyproject.toml` |
| **isort** | Сортировка импортов | `pyproject.toml` |
| **mypy** | Проверка типов | `mypy.ini` |
| **Bandit** | Проверка безопасности | - |

### JavaScript:

| Инструмент | Назначение | Конфигурация |
|------------|-----------|--------------|
| **ESLint** | Линтинг JavaScript | `.eslintrc.json` |
| **Prettier** | Форматирование кода | `.prettierrc.json` |

## Быстрый старт

### Установка Python зависимостей:

```bash
pip install -r requirements.txt
```

### Установка Node.js зависимостей:

```bash
npm install
```

### Запуск тестов:

```bash
pytest tests/ -v
```

### Запуск линтеров:

```bash
# Python
flake8 app/ tests/
pylint app/
black --check app/ tests/
isort --check app/ tests/
mypy app/
bandit -r app/

# JavaScript
npm run lint
npm run format:check
```

## Запуск приложения

```bash
# Локально
python -m app.api

# Docker
docker build -t code-quality-workshop .
docker run -p 5000:5000 code-quality-workshop
```

### Проверка API:

```bash
# Health check
curl http://localhost:5000/health

# Создание пользователя
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com"}'

# Получение всех пользователей
curl http://localhost:5000/users
```

## Отчеты и артефакты

### Генерация отчетов локально:

```bash
# Coverage с HTML отчетом
pytest tests/ --cov=app --cov-report=html

# Flake8 с HTML отчетом
pip install flake8-html
flake8 app/ --format=html --htmldir=reports/flake8

# Pylint с JSON отчетом
pylint app/ --output-format=json > reports/pylint.json

# mypy с HTML отчетом
mypy app/ --html-report reports/mypy

# Bandit с HTML отчетом
bandit -r app/ -f html -o reports/bandit.html
```

### Просмотр отчетов:

```bash
# Coverage
open htmlcov/index.html

# Flake8
open reports/flake8/index.html

# mypy
open reports/mypy/index.html

# Bandit
open reports/bandit.html
```

## GitHub Actions Workflows

### 01-linters.yml
Базовая интеграция линтеров для Python и JavaScript.

### 02-formatting.yml
Проверка форматирования кода с Black, isort и Prettier.

### 03-types-security.yml
Проверка типов (mypy) и безопасности (Bandit).

### 04-artifacts-reports.yml
Создание и сохранение артефактов с отчетами.

### 05-production.yml
Полный production pipeline с параллельным выполнением и quality gate.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/users` | Получить всех пользователей |
| GET | `/users/<id>` | Получить пользователя |
| POST | `/users` | Создать пользователя |
| PUT | `/users/<id>` | Обновить пользователя |
| DELETE | `/users/<id>` | Удалить пользователя |

## Материалы для обучения

- **WORKSHOP_SCENARIO.md** - детальный сценарий вебинара
- **INSTRUCTOR_GUIDE.md** - инструкции для преподавателя
- **CHEATSHEET.md** - шпаргалка по всем инструментам

## Для преподавателей

### Подготовка к вебинару:

1. Создайте репозиторий на GitHub
2. Загрузите все файлы
3. Проверьте что workflows запускаются
4. Прочитайте INSTRUCTOR_GUIDE.md

### План воркшопа (90 минут):

| Время | Тема | Workflow |
|-------|------|----------|
| 0-15 | Введение и теория | Презентация |
| 15-30 | Линтеры | 01-linters.yml |
| 30-45 | Форматирование | 02-formatting.yml |
| 45-60 | Типы и безопасность | 03-types-security.yml |
| 60-75 | Артефакты | 04-artifacts-reports.yml |
| 75-90 | Production pipeline | 05-production.yml |

## Best Practices

### DO:

- Используйте все инструменты в комбинации
- Настройте pre-commit hooks
- Сохраняйте отчеты как артефакты
- Установите пороги качества (coverage, complexity)
- Автоматизируйте форматирование

### DON'T:

- Не игнорируйте предупреждения линтеров
- Не коммитьте неотформатированный код
- Не отключайте проверки без причины
- Не пропускайте type hints
- Не игнорируйте проблемы безопасности

## Полезные ссылки

### Документация инструментов:

- [Flake8](https://flake8.pycqa.org/)
- [Pylint](https://pylint.pycqa.org/)
- [Black](https://black.readthedocs.io/)
- [mypy](https://mypy.readthedocs.io/)
- [Bandit](https://bandit.readthedocs.io/)
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)

### GitHub Actions:

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Artifacts Documentation](https://docs.github.com/actions/guides/storing-workflow-data-as-artifacts)

## Метрики качества

Проект демонстрирует:

- 100% type hints coverage
- 95%+ test coverage
- 0 security issues
- PEP 8 compliant
- Complexity < 10
- Automated formatting

## Contributing

При добавлении кода:

1. Запустите все линтеры
2. Отформатируйте код
3. Убедитесь что тесты проходят
4. Проверьте coverage
5. Создайте PR

## License

MIT License - используйте свободно для обучения!

---

**Создано для воркшопа по DevOps**

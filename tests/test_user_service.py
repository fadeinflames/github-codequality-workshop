"""
Тесты для User Service
"""

from datetime import datetime

import pytest

from app.user_service import User, UserRepository, ValidationError


class TestUser:
    """Тесты для класса User"""

    def test_create_valid_user(self):
        """Тест создания валидного пользователя"""
        user = User(user_id=1, username="testuser", email="test@example.com")

        assert user.user_id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert isinstance(user.created_at, datetime)

    def test_user_validation_invalid_id(self):
        """Тест валидации невалидного ID"""
        with pytest.raises(ValidationError, match="положительным числом"):
            User(user_id=0, username="test", email="test@example.com")

        with pytest.raises(ValidationError):
            User(user_id=-1, username="test", email="test@example.com")

    def test_user_validation_short_username(self):
        """Тест валидации короткого username"""
        with pytest.raises(ValidationError, match="минимум 3 символа"):
            User(user_id=1, username="ab", email="test@example.com")

    def test_user_validation_invalid_email(self):
        """Тест валидации невалидного email"""
        with pytest.raises(ValidationError, match="Некорректный email"):
            User(user_id=1, username="test", email="invalid-email")

        with pytest.raises(ValidationError):
            User(user_id=1, username="test", email="test@")

    def test_user_to_dict(self):
        """Тест преобразования пользователя в словарь"""
        user = User(user_id=1, username="testuser", email="test@example.com")

        user_dict = user.to_dict()

        assert user_dict["user_id"] == 1
        assert user_dict["username"] == "testuser"
        assert user_dict["email"] == "test@example.com"
        assert "created_at" in user_dict

    def test_user_repr(self):
        """Тест строкового представления"""
        user = User(user_id=1, username="test", email="test@example.com")
        assert "User(id=1, username='test')" in repr(user)


class TestUserRepository:
    """Тесты для UserRepository"""

    @pytest.fixture
    def repository(self):
        """Фикстура для репозитория"""
        return UserRepository()

    def test_create_user(self, repository):
        """Тест создания пользователя"""
        user = repository.create(username="testuser", email="test@example.com")

        assert user.user_id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_create_duplicate_email(self, repository):
        """Тест создания пользователя с существующим email"""
        repository.create(username="user1", email="test@example.com")

        with pytest.raises(ValidationError, match="уже существует"):
            repository.create(username="user2", email="test@example.com")

    def test_get_user(self, repository):
        """Тест получения пользователя по ID"""
        created = repository.create(username="testuser", email="test@example.com")

        user = repository.get(created.user_id)
        assert user is not None
        assert user.username == "testuser"

    def test_get_nonexistent_user(self, repository):
        """Тест получения несуществующего пользователя"""
        user = repository.get(999)
        assert user is None

    def test_find_by_email(self, repository):
        """Тест поиска пользователя по email"""
        repository.create(username="test", email="test@example.com")

        user = repository.find_by_email("test@example.com")
        assert user is not None
        assert user.email == "test@example.com"

    def test_find_by_nonexistent_email(self, repository):
        """Тест поиска по несуществующему email"""
        user = repository.find_by_email("nonexistent@example.com")
        assert user is None

    def test_get_all(self, repository):
        """Тест получения всех пользователей"""
        repository.create(username="user1", email="user1@example.com")
        repository.create(username="user2", email="user2@example.com")

        users = repository.get_all()
        assert len(users) == 2

    def test_update_user(self, repository):
        """Тест обновления пользователя"""
        user = repository.create(username="old", email="old@example.com")

        updated = repository.update(
            user_id=user.user_id, username="new", email="new@example.com"
        )

        assert updated is not None
        assert updated.username == "new"
        assert updated.email == "new@example.com"

    def test_update_nonexistent_user(self, repository):
        """Тест обновления несуществующего пользователя"""
        result = repository.update(user_id=999, username="test")
        assert result is None

    def test_update_duplicate_email(self, repository):
        """Тест обновления с существующим email"""
        repository.create(username="user1", email="user1@example.com")
        user2 = repository.create(username="user2", email="user2@example.com")

        with pytest.raises(ValidationError, match="уже существует"):
            repository.update(user_id=user2.user_id, email="user1@example.com")

    def test_delete_user(self, repository):
        """Тест удаления пользователя"""
        user = repository.create(username="test", email="test@example.com")

        deleted = repository.delete(user.user_id)
        assert deleted is True

        # Проверяем что пользователь действительно удален
        assert repository.get(user.user_id) is None

    def test_delete_nonexistent_user(self, repository):
        """Тест удаления несуществующего пользователя"""
        deleted = repository.delete(999)
        assert deleted is False

    def test_count(self, repository):
        """Тест подсчета пользователей"""
        assert repository.count() == 0

        repository.create(username="user1", email="user1@example.com")
        assert repository.count() == 1

        repository.create(username="user2", email="user2@example.com")
        assert repository.count() == 2

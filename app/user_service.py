"""
User Service - демонстрация статического анализа кода
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import re


class ValidationError(Exception):
    """Ошибка валидации данных"""
    pass


class User:
    """Класс пользователя с валидацией"""
    
    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        created_at: Optional[datetime] = None
    ) -> None:
        """
        Инициализация пользователя
        
        Args:
            user_id: Уникальный идентификатор
            username: Имя пользователя
            email: Email адрес
            created_at: Дата создания
            
        Raises:
            ValidationError: Если данные невалидны
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.now()
        
        self._validate()
    
    def _validate(self) -> None:
        """Валидация данных пользователя"""
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            raise ValidationError("user_id должен быть положительным числом")
        
        if not self.username or len(self.username) < 3:
            raise ValidationError("username должен содержать минимум 3 символа")
        
        if not self._is_valid_email(self.email):
            raise ValidationError("Некорректный email адрес")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Проверка валидности email
        
        Args:
            email: Email для проверки
            
        Returns:
            True если email валиден
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование в словарь
        
        Returns:
            Словарь с данными пользователя
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self) -> str:
        """Строковое представление"""
        return f"User(id={self.user_id}, username='{self.username}')"


class UserRepository:
    """Репозиторий для работы с пользователями"""
    
    def __init__(self) -> None:
        """Инициализация репозитория"""
        self._users: Dict[int, User] = {}
        self._next_id: int = 1
    
    def create(self, username: str, email: str) -> User:
        """
        Создание нового пользователя
        
        Args:
            username: Имя пользователя
            email: Email адрес
            
        Returns:
            Созданный пользователь
            
        Raises:
            ValidationError: Если пользователь с таким email уже существует
        """
        # Проверка на существующий email
        if self.find_by_email(email):
            raise ValidationError(f"Пользователь с email {email} уже существует")
        
        user = User(
            user_id=self._next_id,
            username=username,
            email=email
        )
        
        self._users[user.user_id] = user
        self._next_id += 1
        
        return user
    
    def get(self, user_id: int) -> Optional[User]:
        """
        Получение пользователя по ID
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Пользователь или None
        """
        return self._users.get(user_id)
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Поиск пользователя по email
        
        Args:
            email: Email для поиска
            
        Returns:
            Пользователь или None
        """
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    def get_all(self) -> List[User]:
        """
        Получение всех пользователей
        
        Returns:
            Список всех пользователей
        """
        return list(self._users.values())
    
    def update(self, user_id: int, username: Optional[str] = None,
               email: Optional[str] = None) -> Optional[User]:
        """
        Обновление данных пользователя
        
        Args:
            user_id: ID пользователя
            username: Новое имя (опционально)
            email: Новый email (опционально)
            
        Returns:
            Обновленный пользователь или None
            
        Raises:
            ValidationError: Если данные невалидны
        """
        user = self.get(user_id)
        if not user:
            return None
        
        # Проверка на уникальность email
        if email and email != user.email:
            if self.find_by_email(email):
                raise ValidationError(
                    f"Пользователь с email {email} уже существует"
                )
        
        # Создаем нового пользователя с обновленными данными
        updated_user = User(
            user_id=user.user_id,
            username=username or user.username,
            email=email or user.email,
            created_at=user.created_at
        )
        
        self._users[user_id] = updated_user
        return updated_user
    
    def delete(self, user_id: int) -> bool:
        """
        Удаление пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            True если пользователь был удален
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False
    
    def count(self) -> int:
        """
        Подсчет количества пользователей
        
        Returns:
            Количество пользователей
        """
        return len(self._users)

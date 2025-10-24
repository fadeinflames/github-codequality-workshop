"""
Тесты для REST API
"""
import pytest
import json
import re


@pytest.fixture
def client():
    """Фикстура для тестового клиента"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Тесты для health check"""
    
    def test_health_check(self, client):
        """Тест health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'user-api'
        assert 'users_count' in data


class TestUsersEndpoints:
    """Тесты для users endpoints"""
    
    def test_get_empty_users_list(self, client):
        """Тест получения пустого списка пользователей"""
        response = client.get('/users')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['users'] == []
        assert data['count'] == 0
    
    def test_create_user(self, client):
        """Тест создания пользователя"""
        response = client.post(
            '/users',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert 'user_id' in data
    
    def test_create_user_missing_fields(self, client):
        """Тест создания пользователя без обязательных полей"""
        response = client.post(
            '/users',
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_user_invalid_email(self, client):
        """Тест создания пользователя с невалидным email"""
        response = client.post(
            '/users',
            data=json.dumps({
                'username': 'testuser',
                'email': 'invalid-email'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_get_user(self, client):
        """Тест получения пользователя по ID"""
        # Создаем пользователя
        create_response = client.post(
            '/users',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com'
            }),
            content_type='application/json'
        )
        user_data = json.loads(create_response.data)
        user_id = user_data['user_id']
        
        # Получаем пользователя
        response = client.get(f'/users/{user_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['user_id'] == user_id
        assert data['username'] == 'testuser'
    
    def test_get_nonexistent_user(self, client):
        """Тест получения несуществующего пользователя"""
        response = client.get('/users/999')
        assert response.status_code == 404
    
    def test_update_user(self, client):
        """Тест обновления пользователя"""
        # Создаем пользователя
        create_response = client.post(
            '/users',
            data=json.dumps({
                'username': 'oldname',
                'email': 'old@example.com'
            }),
            content_type='application/json'
        )
        user_data = json.loads(create_response.data)
        user_id = user_data['user_id']
        
        # Обновляем пользователя
        response = client.put(
            f'/users/{user_id}',
            data=json.dumps({
                'username': 'newname',
                'email': 'new@example.com'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['username'] == 'newname'
        assert data['email'] == 'new@example.com'
    
    def test_update_nonexistent_user(self, client):
        """Тест обновления несуществующего пользователя"""
        response = client.put(
            '/users/999',
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_user(self, client):
        """Тест удаления пользователя"""
        # Создаем пользователя
        create_response = client.post(
            '/users',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com'
            }),
            content_type='application/json'
        )
        user_data = json.loads(create_response.data)
        user_id = user_data['user_id']
        
        # Удаляем пользователя
        response = client.delete(f'/users/{user_id}')
        assert response.status_code == 200
        
        # Проверяем что пользователь удален
        get_response = client.get(f'/users/{user_id}')
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_user(self, client):
        """Тест удаления несуществующего пользователя"""
        response = client.delete('/users/999')
        assert response.status_code == 404
    
    def test_get_all_users(self, client):
        """Тест получения всех пользователей"""
        # Создаем несколько пользователей
        client.post(
            '/users',
            data=json.dumps({
                'username': 'user1',
                'email': 'user1@example.com'
            }),
            content_type='application/json'
        )
        client.post(
            '/users',
            data=json.dumps({
                'username': 'user2',
                'email': 'user2@example.com'
            }),
            content_type='application/json'
        )
        
        # Получаем всех пользователей
        response = client.get('/users')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['count'] == 2
        assert len(data['users']) == 2

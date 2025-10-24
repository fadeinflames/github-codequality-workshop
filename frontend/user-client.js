/**
 * User API Client
 * Демонстрация ESLint и Prettier для JavaScript
 */

const API_BASE_URL = 'http://localhost:5000';

/**
 * Класс для работы с User API
 */
class UserApiClient {
  /**
   * Конструктор
   * @param {string} baseUrl - Базовый URL API
   */
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Выполнение HTTP запроса
   * @param {string} endpoint - Endpoint
   * @param {Object} options - Опции fetch
   * @returns {Promise<Object>} Ответ от API
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  /**
   * Получение списка всех пользователей
   * @returns {Promise<Array>} Список пользователей
   */
  async getUsers() {
    const data = await this.request('/users');
    return data.users;
  }

  /**
   * Получение пользователя по ID
   * @param {number} userId - ID пользователя
   * @returns {Promise<Object>} Данные пользователя
   */
  async getUser(userId) {
    if (!userId || userId <= 0) {
      throw new Error('Invalid user ID');
    }
    return this.request(`/users/${userId}`);
  }

  /**
   * Создание нового пользователя
   * @param {Object} userData - Данные пользователя
   * @param {string} userData.username - Имя пользователя
   * @param {string} userData.email - Email
   * @returns {Promise<Object>} Созданный пользователь
   */
  async createUser(userData) {
    if (!userData.username || !userData.email) {
      throw new Error('Username and email are required');
    }

    if (!this.isValidEmail(userData.email)) {
      throw new Error('Invalid email format');
    }

    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  /**
   * Обновление данных пользователя
   * @param {number} userId - ID пользователя
   * @param {Object} userData - Новые данные
   * @returns {Promise<Object>} Обновленный пользователь
   */
  async updateUser(userId, userData) {
    if (!userId || userId <= 0) {
      throw new Error('Invalid user ID');
    }

    if (userData.email && !this.isValidEmail(userData.email)) {
      throw new Error('Invalid email format');
    }

    return this.request(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  /**
   * Удаление пользователя
   * @param {number} userId - ID пользователя
   * @returns {Promise<Object>} Результат удаления
   */
  async deleteUser(userId) {
    if (!userId || userId <= 0) {
      throw new Error('Invalid user ID');
    }

    return this.request(`/users/${userId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Проверка health endpoint
   * @returns {Promise<Object>} Статус сервиса
   */
  async checkHealth() {
    return this.request('/health');
  }

  /**
   * Валидация email
   * @param {string} email - Email для проверки
   * @returns {boolean} true если email валиден
   */
  isValidEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
  }
}

/**
 * Форматирование даты
 * @param {string} dateString - Строка с датой
 * @returns {string} Отформатированная дата
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Отображение списка пользователей в консоли
 * @param {Array} users - Список пользователей
 */
function displayUsers(users) {
  console.log('\n=== Список пользователей ===');
  
  if (users.length === 0) {
    console.log('Нет пользователей');
    return;
  }

  users.forEach((user) => {
    console.log(`
ID: ${user.user_id}
Username: ${user.username}
Email: ${user.email}
Created: ${formatDate(user.created_at)}
---`);
  });
}

/**
 * Пример использования API
 */
async function main() {
  const client = new UserApiClient();

  try {
    // Проверка здоровья сервиса
    console.log('Checking service health...');
    const health = await client.checkHealth();
    console.log('Service status:', health.status);

    // Создание пользователей
    console.log('\nCreating users...');
    await client.createUser({
      username: 'alice',
      email: 'alice@example.com',
    });
    await client.createUser({
      username: 'bob',
      email: 'bob@example.com',
    });

    // Получение всех пользователей
    console.log('\nFetching all users...');
    const users = await client.getUsers();
    displayUsers(users);

    // Обновление пользователя
    if (users.length > 0) {
      console.log('\nUpdating first user...');
      await client.updateUser(users[0].user_id, {
        username: 'alice_updated',
      });
    }

    // Получение обновленного списка
    const updatedUsers = await client.getUsers();
    displayUsers(updatedUsers);
  } catch (error) {
    console.error('Error in main:', error.message);
  }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    UserApiClient,
    formatDate,
    displayUsers,
  };
}

// Запуск если файл выполняется напрямую
if (typeof require !== 'undefined' && require.main === module) {
  main();
}

"""
REST API для User Service
"""

from typing import Any, Dict

from flask import Flask, jsonify, request

from app.user_service import UserRepository, ValidationError

app = Flask(__name__)
repository = UserRepository()


@app.route("/health", methods=["GET"])
def health() -> Dict[str, Any]:
    """Health check endpoint"""
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "user-api",
                "version": "1.0.0",
                "users_count": repository.count(),
            }
        ),
        200,
    )


@app.route("/users", methods=["GET"])
def get_users() -> Dict[str, Any]:
    """Получение списка всех пользователей"""
    users = repository.get_all()
    return (
        jsonify({"users": [user.to_dict() for user in users], "count": len(users)}),
        200,
    )


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Dict[str, Any]:
    """Получение пользователя по ID"""
    user = repository.get(user_id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    return jsonify(user.to_dict()), 200


@app.route("/users", methods=["POST"])
def create_user() -> Dict[str, Any]:
    """Создание нового пользователя"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Требуется JSON"}), 400

    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Требуются поля username и email"}), 400

    try:
        user = repository.create(username=username, email=email)
        return jsonify(user.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int) -> Dict[str, Any]:
    """Обновление данных пользователя"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Требуется JSON"}), 400

    try:
        user = repository.update(
            user_id=user_id, username=data.get("username"), email=data.get("email")
        )

        if not user:
            return jsonify({"error": "Пользователь не найден"}), 404

        return jsonify(user.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> Dict[str, Any]:
    """Удаление пользователя"""
    deleted = repository.delete(user_id)

    if not deleted:
        return jsonify({"error": "Пользователь не найден"}), 404

    return jsonify({"message": "Пользователь удален"}), 200


@app.errorhandler(404)
def not_found(error: Any) -> Dict[str, Any]:
    """Обработчик 404 ошибки"""
    return jsonify({"error": "Endpoint не найден"}), 404


@app.errorhandler(500)
def internal_error(error: Any) -> Dict[str, Any]:
    """Обработчик 500 ошибки"""
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

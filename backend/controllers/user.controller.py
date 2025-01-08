from backend.models.Users import User  
from werkzeug.security import check_password_hash, generate_password_hash
import random
import string


def login(email,password):
    try:
        if not email or not password:
            return {"error": "Email and password are required"}

        # Find user by email
        user_found = User().findByEmail(email=email)

        if not user_found:
            return {"error": "User not found"}

         # Check password
        if not check_password_hash(user_found['password'], password):
            return {"error": "Invalid credentials"}

        return {"message": "Login successful", "user": user_found}
    except Exception as e:
        return {"error": str(e)}
  
def register(username, email, password, role='user'):
    try:
        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}

        # Check if the email already exists
        existing_user = User().findByEmail(email=email)
        if existing_user:
            return {"error": "User with this email already exists"}

        existing_user = User().findByUsername(email=email)
        if existing_user:
            return {"error": "User with this username already exists"}

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )
        new_user.save()

        return {"message": "User registered successfully", "user_id": new_user.id}
    except Exception as e:
        return {"error": str(e)}

def create_user():
    try:
        data = request.json
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            role=data.get('role'),
            password=data.get('password')
        )
        user.save()
        return jsonify({"message": "User created successfully", "user_id": user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user(user_id):
    try:
        user = User()
        result = user.read(user_id)
        if not result:
            return jsonify({"message": "User not found"}), 404
        return jsonify({"user": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_users():
    try:
        user = User()
        results = user.read()
        return jsonify({"users": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_user(user_id):
    try:
        data = request.json
        user = User(
            id=user_id,
            username=data.get('username'),
            email=data.get('email'),
            role=data.get('role'),
            password=data.get('password')
        )
        user.save()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_user(user_id):
    try:
        user = User()
        user.delete(user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

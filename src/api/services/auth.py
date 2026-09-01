def authenticate_user(username: str, password: str):
    if username == "admin123" and password == "admin123":
        return {
            "id": 1,
            "username": "admin123",
            "collection": "admin123",
        }
    return None

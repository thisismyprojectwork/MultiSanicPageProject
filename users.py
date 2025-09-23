import json
from typing import TypedDict


class StoredUser(TypedDict):
    name: str
    email: str
    message: str


class StoredUsers(TypedDict):
    users: list[StoredUser]

class Users:
    @staticmethod
    def add(name: str, email: str, message: str):
        with open("users.json") as f:
            users: StoredUsers = json.load(f)

        user: StoredUser = {"name": name, "email": email, "message": message}

        users["users"].append(user)

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        return

    @staticmethod
    def view():
        with open("users.json") as f:
            users: StoredUsers = json.load(f)

        return users["users"]

import json
import sanic
from typing import TypedDict


class StoredUser(TypedDict):
    name: str
    email: str
    password: str
    firstName: str
    lastName: str
    message: str


class StoredUsers(TypedDict):
    users: list[StoredUser]


class Users:
    @staticmethod
    def add(name: str, email: str, message: str) -> bool:
        try:
            with open("users.json") as f:
                users: StoredUsers = json.load(f)

            user: StoredUser = {"name": name, "email": email, "message": message}

            users["users"].append(user)

            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)

            return True
        except:
            return False

    @staticmethod
    def is_logged_in(request: sanic.Request) -> bool | StoredUser:
        try:
            if request.cookies["email"][0]:
                email = request.cookies["email"][0]
                checked_user = Users.find(email)

                if checked_user:
                    return checked_user

            return False

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def view():
        with open("users.json") as f:
            users: StoredUsers = json.load(f)

        return users["users"]

    @staticmethod
    def find(email: str) -> StoredUser | None:
        with open("users.json") as f:
            users: StoredUsers = json.load(f)

        found_user = None

        for user in users["users"]:
            try:
                if user["email"] == email:
                    found_user = user
                else:
                    continue
            except KeyError:
                continue

        return found_user

    @staticmethod
    def login(email: str, password: str) -> bool | StoredUser:
        user = Users.find(email)

        if user:
            if user["password"] == password:
                return True

        return False

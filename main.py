import re
import sanic
import webbrowser

from sanic.exceptions import NotFound
from sanic import response
from users import Users as users
from logger import logs
from utils import render_template

app = sanic.Sanic("test")
log = logs(app_name="Coffee Shop", file_name="app.log")


@app.exception(NotFound)  # type:ignore
async def catch404(request: sanic.Request, exception: sanic.SanicException):
    log.add(f"User requested {request.path}, redirecting to main page.")
    return response.redirect("/")


@app.route("/logout")
async def request(request: sanic.Request) -> sanic.HTTPResponse:
    try:
        done_resp = response.redirect("/")
        done_resp.delete_cookie("email", path="/")

        return done_resp
    except:
        return response.redirect("/")


@app.route("/", methods=["GET", "POST"])
async def index(request: sanic.Request) -> sanic.HTTPResponse:
    try:
        if request.method == "GET":
            log.add("Index page viewed.")

            check_user = users.is_logged_in(request)

            login_button_top = '<li><a href="/login">Login</a></li>'
            main_text = "Brewed for your moments."

            if check_user:
                login_button_top = (
                    '<li><a href="/logout">Logout</a></li>'  # switch for a logout one
                )
                main_text = f"Welcome back, {check_user['firstName']}"

            return render_template(
                "index.html", login_button_top=login_button_top, main_text=main_text
            )

        elif request.method == "POST":
            if request.form:
                name = request.form[  # type:ignore (sanic's typing is shamoblic so i have to spam this)
                    "name"
                ][
                    0
                ]
                email = request.form[  # type:ignore (sanic's typing is shamoblic so i have to spam this)
                    "email"
                ][
                    0
                ]
                message = request.form[  # type:ignore (sanic's typing is shamoblic so i have to spam this)
                    "message"
                ][
                    0
                ]
                users.add(
                    name=name,  # type:ignore (sanic's typing is shamoblic so i have to spam this)
                    email=email,  # type:ignore (sanic's typing is shamoblic so i have to spam this)
                    message=message,  # type:ignore (sanic's typing is shamoblic so i have to spam this)
                )
                log.add(f"{email} stored")

            return response.redirect("/")
        else:
            return response.empty(status=404)
    except Exception as error:
        log.add(f"Error @ {request.path} - {error}")


@app.route("/users", methods=["GET", "POST"])
async def users_page(request: sanic.Request) -> sanic.HTTPResponse:
    try:
        if request.method == "GET":
            log.add("Users Viewed")
            return render_template("users.html")
        elif request.method == "POST":
            log.add("Users Requested")
            return response.json(users.view())
        else:
            return response.empty(status=404)
    except Exception as error:
        log.add(f"Error @ {request.path} - {error}")


@app.route("/login", methods=["GET", "POST"])
async def login(request: sanic.Request):
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        login_query = request.json
        email = login_query["email"]
        password = login_query["password"]

        correct_login = users.login(email=email, password=password)

        if correct_login:
            log.add(f"{email} logged in")
            success_response = response.empty(status=200)
            success_response.add_cookie(
                key="email",
                value=email,
                path="/",
            )
            log.add(f"Email cookie for {email} created.")

            return success_response
        else:
            return response.empty(status=401)
    else:
        return response.redirect("/")


if __name__ == "__main__":
    host = "localhost"
    port = 1942
    protocol = "http"
    url = f"{protocol}://{host}:{port}/"

    webbrowser.open_new_tab(url)
    log.add(f"Running @ {url}")
    app.run(host=host, port=port, fast=True, motd=False, dev=False)  # type:ignore
    log.add("Gracefully exited.")

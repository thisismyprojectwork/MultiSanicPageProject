import sanic

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


@app.route("/", methods=["GET", "POST"])
async def index(request: sanic.Request) -> sanic.HTTPResponse:
    if request.method == "GET":
        log.add("Index page viewed.")
        return render_template("index.html")
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


@app.route("/users", methods=["GET", "POST"])
async def users_page(request: sanic.Request) -> sanic.HTTPResponse:
    if request.method == "GET":
        log.add("Users Viewed")
        return render_template("users.html")
    elif request.method == "POST":
        log.add("Users Requested")
        return response.json(users.view())
    else:
        return response.empty(status=404)


if __name__ == "__main__":
    app.run(host="localhost", fast=True, motd=False, dev=False)  # type:ignore

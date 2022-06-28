from app import app, db
from app.models import User, Files


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Files": Files}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["APP_PORT"])

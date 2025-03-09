from app import app, db
from flask import jsonify, redirect, request
from typing_extensions import Union, Dict
from app.lib import check_create_body
from app.models import ShellUrl

@app.route("/", methods=["GET"])
def index():
    return jsonify({"msg": "ligma balls"}), 200

@app.route("/create", methods=["POST"])
def create():
    # fetch data from body and validate data
    data: Dict
    err: Union[str, None]
    data, err = check_create_body(request.get_json())
    if err:
        return jsonify({"error": data}), 500
    # create link in database
    try:
        # doesn't auto create urls table
        # need to manually create table in database for first times
        # TODO: create table if not exists automatically
        # >:((( whoever added typing to python and pyright
        # is the biggest piece of dogshit, at least make the tool
        # actually usuable and be able to smartly infer shit
        # have to do this little hack now, fk u
        id: str = data.get("id") # type: ignore
        link: str = data.get("id") # type: ignore
        new_url = ShellUrl(id=id, link=link)
        db.session.add(new_url)
        db.session.commit()
        return jsonify({"msg": "success"}), 201
    except Exception as e:
        return jsonify({"error": e}), 500

@app.route("/<code>", methods=["GET"])
def redirect_url(code):
    # fetch url from backend
    url = ""
    # if url not found, display error page
    # otherwise redirect to correct url
    return redirect(url, code=301)


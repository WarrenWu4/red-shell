from app import app, db
from flask import jsonify, redirect, request
from typing_extensions import Union, Dict
from app.lib import check_create_body
from app.models import ShellUrl, UrlHit
from user_agents import parse

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
        link: str = data.get("link") # type: ignore
        new_url = ShellUrl(id=id, link=link)
        db.session.add(new_url)
        db.session.commit()
        return jsonify({"msg": "success"}), 201
    except Exception as e:
        return jsonify({"error": e}), 500

@app.route("/<string:id>", methods=["GET"])
def redirect_url(id: str):
    # fetch url from database 
    # if url not found, display error page
    # otherwise redirect to correct url
    data = ShellUrl.query.filter_by(id=id).first()
    if data:
        user_agent_string = request.headers.get("User-Agent", "")
        user_agent = parse(user_agent_string)
        device_type = "Mobile" if user_agent.is_mobile else "Tablet" if user_agent.is_tablet else "Computer"
        browser = user_agent.browser.family
        qrcode_hit = request.args.get("qrcode", "false").lower() == "true"
        new_hit = UrlHit(
            url_id=id,
            ip_addr=request.remote_addr,
            device_type=device_type,
            browser_type=browser,
            qrcode=qrcode_hit
        )
        db.session.add(new_hit)
        db.session.commit()
        return redirect(data.link, code=301)
    else:
        return jsonify({"err": "not found"}), 404

@app.route("/delete/<string:id>", methods=["DELETE"])
def delete_url(id: str):
    # fetch url from database
    # if url not found, display error page
    # otherwise delete entry
    data = ShellUrl.query.filter_by(id=id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'msg': 'Shortened URL deleted successfully'}), 200
    else:
        return jsonify({'err': 'Shortened URL not found'}), 404

@app.route("/update/<string:id>", methods=["PUT"])
def update_url(id: str):
    data = request.get_json()
    url_entry = ShellUrl.query.filter_by(id=id).first()
    if url_entry:
        if 'link' in data:
            url_entry.link = data['link']
        db.session.commit()
        return jsonify({'message': 'Shortened URL updated successfully'}), 200
    else:
        # Return an error if the shortened URL code doesn't exist
        return jsonify({'error': 'Shortened URL not found'}), 404

@app.route("/analytics/<string:id>", methods=["GET"])
def analytics_url(id: str):
    return jsonify({"msg": "wip"}), 200

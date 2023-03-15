from flask import Flask

# from rest.svg_renderer import render_as_svg
from state.sessions import Sessions
from flask import abort
from flask import request
from flask import Response

from state.sessionstate import SessionState

app = Flask(__name__)
sessions = Sessions()


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/register_session")
def register_session():
    return dict(sessionId=sessions.register_session())


@app.route("/<session_id>/layout")
def layout(session_id):
    session: SessionState = sessions.get_session(session_id)
    if not session:
        abort(404)
    return session.get_layout()


@app.route("/<session_id>/edge")
def get_edge(session_id):
    session: SessionState = sessions.get_session(session_id)
    if not session:
        abort(404)
    return session.get_edge(_get_req_edge(request.args))


@app.route("/<session_id>/update", methods=["GET"])
def update_get(session_id):
    session: SessionState = sessions.get_session(session_id)
    if not session:
        abort(404)
    return session.update_edge(_get_req_edge(request.args))


# @app.route("/<session_id>/update_svg", methods=["GET"])
# def update_get_svg(session_id):
#     data = update_get(session_id)
#     return Response(render_as_svg(data), mimetype="image/svg+xml")


@app.route("/<session_id>/update", methods=["POST"])
def update_post(session_id):
    session: SessionState = sessions.get_session(session_id)
    if not session:
        abort(404)
    return session.update_edge(_get_req_edge(request.get_json()))


def _get_req_edge(args):
    return dict(
        left=args.get("left") is not None and int(args.get("left")),
        right=args.get("right") is not None and int(args.get("right")),
        dissent=args.get("dissent") is not None and float(args.get("dissent")),
        respect=args.get("respect") is not None and float(args.get("respect")),
    )

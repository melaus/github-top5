
from flask import Flask, jsonify, abort
from github import Github
import json

app = Flask(__name__)
g   = Github()


@app.route("/top5")
def index():
    return jsonify(message="API to obtain 5 largest public GitHub repos of a given GitHub Handle")


@app.route("/top5/<username>")
def show_repo(username):
    """
    obtain high-level info of the largest 5 public repos of the requested user
    :param username: String. username
    :return: json of largest 5 or 404
    """
    output = g.get_top5(username, simple=True)

    if type(output) == int:
        abort(404)
    else:
        return jsonify(output)


@app.route("/top5/<username>/detailed")
def show_repo_detailed(username):
    """
    obtain detailed info of the largest 5 public repos of the requested user

    :param username: String. username
    :return: json of largest 5 or 404
    """
    output = g.get_top5(username)
    if type(output) == int and output == 404:
        abort(404)
    else:
        return jsonify(output)


@app.errorhandler(404)
def page_not_found(error):
    """
    Return a 'Not Found' message and status 404
    :param error: The 404 error
    :return:
    """
    return jsonify(message="Not Found"), 404

if __name__ == "__main__":
    app.run()


from flask import Flask, jsonify, abort
from github_lib import Github
import json

app = Flask(__name__)
g   = Github()


@app.route("/top5")
def index():
    """
    simple introduction of repo
    :return: A JSON of a short message about API, base URL and usage details
    """
    return jsonify(message="API to obtain 5 largest public GitHub repos of a given GitHub handle, see https://github.com/melaus/github-top5 for more information",
            base_url="https://apis.melaus.xyz/top5",
            usage="['base_url'/<github_handle>] to obtain high-level details (repo name, size and url); ['base_url'/<github_handle>/detailed] to obtain all information provided by GitHub's API")


@app.route("/top5/<username>")
def show_repo(username):
    """
    obtain high-level info of the largest 5 public repos of the requested user
    :param username: String. username
    :return: JSON of largest 5 or 404
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
    :return: JSON of largest 5 or 404
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
    :return: JSON of a message saying "Not Found" and status 404
    """
    return jsonify(message="Not Found"), 404

# Entry point for testing and uWSGI
if __name__ == "__main__":
    app.run()

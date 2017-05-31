import requests
import json
import re
from collections import OrderedDict

API_BASE = 'https://api.github.com'


class Github:
    def __init__(self):
        return

    def __get_user_repos(self, username):
        """
        obtain repo info from Github given a username
        :param username: String. Github handle of the user requested
        :return: JSON containing repo info through pagination and response status
        """
        # initial call to obtain the first 100 public repos
        all_content = []
        content = requests.get('{0}/users/{1}/repos?per_page=100'.format(API_BASE, username), headers={'Authorization': 'TOKEN 7c0ea0b8013b08ec143aa8a94f87b0d3c5ed2ff9'})

        # return error directly before attempting to paginate
        if content.status_code == 404:
            return 404

        all_content += content.json()

        # check if there's more pages to go and perform pagination
        if 'Link' in content.headers.keys() and 'rel="next"' in content.headers['Link']:
            next_link = re.search(r"<([a-z:/.?_=&0-9]+)>; rel=\"next\"", content.headers['Link']).group(1)
            content = requests.get(next_link, headers={'Authorization': 'TOKEN 7c0ea0b8013b08ec143aa8a94f87b0d3c5ed2ff9'})
            all_content += content.json()

        return all_content

    def __find_top5(self, content_list, simple=False):
        """
        get the largest 5 public repos
        :param content_list: List of dict's. Repo information in Python list/ dict formats, converted from JSON
        :param simple: Boolean. [default = False] Whether to send full response or high level information about each repo
        :return: list of dict's of the largest 5 public repos
        """

        top5 = sorted(content_list, key=lambda x: x['size'], reverse=True)[0:5]

        # if only top level info is required
        if simple:
            top5 = map(lambda x:
                       {'name': x['name'],
                        'size': x['size'],
                        'html_url' : x['html_url']
                       }, top5)

        return top5

    def get_top5(self, username, simple=False):
        """
        public interface for API use
        :param username: String. Github handle of the user requested
        :param simple: Boolean. [default = False] Whether to send full response or high level information about each repo
        :return:
        """
        content = self.__get_user_repos(username)

        # continue to find top 5 if we did not encounter an error
        if type(content) == int and content == 404:
            return content
        else:
            return self.__find_top5(content, simple)


# for testing purposes
# if __name__ == '__main__':
#     g = Github()
#     print g.get_top5('facebook', simple=True)

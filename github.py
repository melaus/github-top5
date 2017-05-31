import requests
import json
from collections import OrderedDict

API_BASE = 'https://api.github.com'


class Github:
    def __init__(self):
        return

    def __get_user_repos(self, username):
        """
        obtain repo info from Github given a username
        :param username: String.
        :return: requests object containing repo info and response status
        """
        content = requests.get('{0}/users/{1}/repos'.format(API_BASE, username))
        return content

    def __find_top5(self, content_list, simple=False):
        """
        get the largest 5 public repos
        :param content_list: List of dict's. Repo information in Python list/ dict formats, converted from JSON
        :return: list of dict's of the largest 5 public repos
        """
        top5 = sorted(content_list, key=lambda x: x['size'], reverse=True)[0:5]

        # if only top level info is required
        if simple:
            top5 = map(lambda x:
                       {'name': x['name'],
                        'size': x['size'],
                        'url' : x['url']
                       }, top5)

        #print map(lambda x: (x['name'], x['size']), top5) 
        return top5

    def get_top5(self, username, simple=False):
        """
        public interface for API use
        :param username:
        :param simple:
        :return:
        """
        content = self.__get_user_repos(username)
        #print content.status_code

        if content.status_code >= 400:
            # no top 5 if error (e.g. user does not exists)
            return content.status_code
        else:
            return self.__find_top5(content.json(), simple)


# for testing purposes
#if __name__ == '__main__':
    #g = Github()
    #print g.get_top5('tensorflow', simple=False)

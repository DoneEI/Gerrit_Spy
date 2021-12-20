from termcolor import colored
from base.SupportCommunities import SupportCommunities
from base import CheckMethodUtils
import requests
import json


class QueryProperty:
    """
        This is used for designating the parameters when querying for code changes by Gerrit API.
        see https://review.opendev.org/Documentation/rest-api-changes.html#list-changes

        :param name : name of parameter
        :param necessary : whether the parameter is needed
        :param checkMethod : the function for checking whether the value for parameter is valid.
                             function should be like: def checkFunction(value:str) -> bool
    """

    def __init__(self, name, necessary=False, checkMethod=None):
        self.name = name
        self.necessary = necessary
        self.checkMethod = checkMethod


class CodeChangeSpy:
    """
    This is a simple tool for collecting code changes of projects of communities, which must be supported by
    SupportCommunities. When querying for code changes, users could append parameters to limit the range of query
    results, which could designated by :param parameters. Users could also limit the code change info items by setting
    :param info, otherwise default info would be used.

    Note that parameter in parameters would be ignored if it is not configured in __queryProperties. Users could
    customize their expecting parameter by adding in the __queryProperties (see class QueryProperty)

    Example:
        spy = CodeChangeSpy("openstack", "nova", {
         'after': '2020-01-01',
         'before': '2021-01-01',
         'status': 'closed'
        })

        result = spy.run()

    The result is a list of code change info items.

    """

    # default query parameters
    __queryProperties = [
        QueryProperty('after', checkMethod=CheckMethodUtils.validTimeStr),
        QueryProperty('before', checkMethod=CheckMethodUtils.validTimeStr),
        QueryProperty('status', checkMethod=CheckMethodUtils.validStatus)
    ]

    def __init__(self, community: str, project: str, parameters=None, info=None):
        if parameters is None:
            parameters = {}

        if info is None:
            # default info list for code changes, which can be customized.
            # The info items must be subset of
            # https://review.opendev.org/Documentation/rest-api-changes.html#change-info
            info = ['id', 'project', '_number', 'branch', 'change_id', 'created', 'updated',
                    'submitted', 'topic', 'insertions', 'deletions', 'hashtags', 'owner', 'status', 'subject',
                    'requirements', 'total_comment_count']

        self.community = community
        self.project = project
        self.parameters = parameters
        self.info = info

        self.__check()

    def __check(self):
        # check community and project
        if not SupportCommunities.isSupported(self.community):
            raise RuntimeError(
                '%s is not supported so far. Use SupportCommunities.list to see which communities are supported')

        if not CheckMethodUtils.strIsNotEmpty(self.project):
            raise RuntimeError(
                'invalid project is designated.')

        # check other query parameters
        notIgnored = set()
        for pro in self.__queryProperties:
            v = self.parameters.get(pro.name, None)
            notIgnored.add(pro.name)

            if v is None:
                if pro.necessary:
                    raise RuntimeError("parameter '%s' is needed but missing in the parameters" % pro.name)
            else:
                if not pro.checkMethod(v):
                    raise RuntimeError(
                        "'%s' is not a valid value as requested by the property '%s'" % (str(v), pro.name))

        # check parameters to warn users
        ignored = ''
        for v in self.parameters:
            if v not in notIgnored:
                ignored += '%s ' % v

        if ignored != '':
            print(colored("Warning: parameters '%s'would be ignored since they are not configured." % ignored,
                          'yellow'))

    def __buildUrl(self):
        # community and project
        url = '%s/changes/?q=project:%s/%s' % (
            SupportCommunities.getCommunityData(self.community).url, self.community, self.project)

        # parameters
        for pro in self.__queryProperties:
            url += ' %s:%s' % (pro.name, self.parameters[pro.name])

        # TODO: no-limit parameter can be used remove the default limit on queries and return all results.
        #  This might conflict with parameters that are newly added.
        url += '&no-limit'

        return url

    def run(self):
        url = self.__buildUrl()

        res = requests.get(url)
        code_changes = []

        if res.status_code == 200 and len(res.content) > 4:
            for item in json.loads(res.content[4:]):
                # filter item
                filterRes = {}
                for k in self.info:
                    filterRes[k] = item.get(k, '')

                code_changes.append(filterRes)

        return code_changes

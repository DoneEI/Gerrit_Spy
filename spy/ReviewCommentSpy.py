import sys
from termcolor import colored
from base.SupportCommunities import SupportCommunities
import requests
import json


class ReviewCommentSpy:
    """
    This is a simple tool for collecting review comments of projects of communities, which must be supported by
    SupportCommunities. When querying for review comments, users should provide a list of code change items (such as the
    result of CodeChangeSpy), which should be dict type and at least have one field named 'id', corresponding to
    https://review.opendev.org/Documentation/rest-api-changes.html#change-info. Users can also limit the review comment
    info items by setting :param info, otherwise default info would be used.

    Example:
        codeChangeSpy = CodeChangeSpy('openstack', 'nova', {
         'after': '2020-01-01',
         'before': '2021-01-01',
         'status': 'closed'
        })

        reviewCommentSpy = ReviewCommentSpy(codeChangeSpy.run())

        result = reviewCommentSpy.run()


    The result is a list of review comment info items.

    """

    def __init__(self, codeChanges: list, info=None):
        if info is None:
            # default info list for review comments, which can be customized.
            # The info items must be subset of
            # https://review.opendev.org/Documentation/rest-api-changes.html#comment-info
            info = ['id', 'author', 'change_message_id', 'updated', 'unresolved', 'patch_set', 'line',
                    'message']

        self.codeChanges = codeChanges
        self.info = info

    @staticmethod
    def __buildUrlBasedOnId(changeId):
        try:
            community = (str(changeId).split('%2F'))[0]
            return '%s/changes/%s/comments' % (SupportCommunities.getCommunityData(community).url, changeId)
        except Exception:
            raise RuntimeError("%s is not in the format '<project>~<branch>~<Change-Id>'" % changeId)

    @staticmethod
    def __buildUrlBasedOnNumber(changeId, number):
        if number is not None:
            try:
                community = (str(changeId).split('%2F'))[0]
                url = (str(changeId).split('~'))[0] + '~' + number
                return '%s/changes/%s/comments' % (SupportCommunities.getCommunityData(community).url, url)
            except Exception:
                raise RuntimeError("%s is not in the format '<project>~<branch>~<Change-Id>'" % changeId)
        return ReviewCommentSpy.__buildUrlBasedOnId(changeId)

    def run(self):
        codeComments = []

        for codeChange in self.codeChanges:
            changeId = codeChange['id']
            url = self.__buildUrlBasedOnId(changeId)

            try:
                # The number of code comments provided by detail info of code change
                commentsCountByCodeChangeInfo = codeChange.get('total_comment_count', 0)

                res = requests.get(url)

                if res.status_code == 404:
                    # try to request by number
                    res = requests.get(self.__buildUrlBasedOnNumber(changeId, codeChange.get('_number', None)))

                    # log it if it still failed
                    if res.status_code == 404:
                        print('request 404 for change_id: %s' % changeId)
                        continue

                commentsOfChangeId = json.loads(res.content[4:])

                # append data
                commentsCountByRequest = 0
                for file in commentsOfChangeId.keys():
                    for comment in commentsOfChangeId.get(file):
                        # filter
                        filterRes = {}
                        for k in self.info:
                            filterRes[k] = comment.get(k, '')

                        # append change_id and file
                        filterRes['change_id'] = changeId
                        filterRes['file'] = file

                        codeComments.append(filterRes)
                        commentsCountByRequest += 1

                # check number
                if commentsCountByRequest != commentsCountByCodeChangeInfo:
                    print(
                        colored(
                            'Warning: The number of review comments of %s is %d but got %d. Please check it by '
                            'yourself.' % (changeId, commentsCountByCodeChangeInfo, commentsCountByRequest), 'yellow'))
            except Exception as e:
                print("request error for %s" % changeId, file=sys.stderr)
                print(e)
                continue

        return codeComments

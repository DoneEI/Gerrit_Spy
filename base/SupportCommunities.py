class CommunityData:
    """
        This is used for telling users which communities are supported.
        Note that the code review process of community must be supported by Gerrit API,
        otherwise unexpected errors might be occurred.

        :param name : name of the community
        :param url : the url of the community
    """

    def __init__(self, name, url):
        self.name = name
        self.url = url


class SupportCommunities:
    communities = [CommunityData("openstack", "https://review.opendev.org"),
                   CommunityData("qt", "https://codereview.qt-project.org")]

    @staticmethod
    def isSupported(community):
        if community is not None:
            for c in SupportCommunities.communities:
                if community == c.name:
                    return True

        return False

    @staticmethod
    def list():
        print(SupportCommunities.communities)

    @staticmethod
    def getCommunityData(community):
        if community is not None:
            for c in SupportCommunities.communities:
                if community == c.name:
                    return c

        return None

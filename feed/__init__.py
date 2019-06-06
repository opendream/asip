

class FeedResource(object):
    resource_url = None

    def prepare(self):
        '''Implement me'''

    def get_object_list(self):
        self.prepare()

        object_list = ()

        for method, Model in self.resources:
            object_list += (getattr(self, method)(), Model)

        print object_list

        return object_list


    def update_feed(self):
        from feed.sources import *

        try:
            from custom.feed.sources import *
        except ImportError:
            pass

        for Resource in self.__class__.__subclasses__():
            resource = Resource()

            resource.get_object_list()


class Pipeline(object):

    def process_item(self, item):
        print(item.data)

        return item
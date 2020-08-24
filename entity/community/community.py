from entity.base_entity import BaseEntity


class Community(BaseEntity):

    NAME = 'name'
    NUMBER = 'number'

    CHILDREN = 'children'  # It is used in community repo when it wants to return a tree.

    def __init__(self, name=None, number=None, companion=None):
        if not companion:
            companion = {}

        if name:
            companion[Community.NAME] = name

        if number:
            companion[Community.NUMBER] = number

        BaseEntity.__init__(self, companion)

        self.parent = None

    def get_public_obj(self):
        obj = BaseEntity.get_public_obj(self)

        obj.pop(Community.NUMBER, None)

        return obj

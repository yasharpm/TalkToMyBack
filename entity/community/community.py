from entity.base_entity import BaseEntity


class Community(BaseEntity):

    NAME = 'name'
    DESCRIPTION = 'description'
    NUMBER = 'number'
    ID_NAME = 'id_name'

    CHILDREN = 'children'  # It is used in community repo when it wants to return a tree.

    def __init__(self, name=None, description=None, number=None, id_name=None, companion=None):
        if not companion:
            companion = {}

        if name:
            companion[Community.NAME] = name

        if description:
            companion[Community.DESCRIPTION] = description

        if number:
            companion[Community.NUMBER] = number

        if id_name is not None:
            companion[Community.ID_NAME] = id_name

        BaseEntity.__init__(self, companion)

        self.parent = None

    def get_public_obj(self):
        obj = BaseEntity.get_public_obj(self)

        obj.pop(Community.NUMBER, None)

        return obj

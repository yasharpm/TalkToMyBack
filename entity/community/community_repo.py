from entity.base_repo import BaseRepo
from entity.community.community import Community
from entity.community.community_id import *
from entity.community.community_errors import *


class CommunityRepo(BaseRepo):

    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'

    COMMUNITY_TEST = 'TEST'
    COMMUNITY_TEST_ID_NAME = 'test_donttest_01'

    def __init__(self):
        BaseRepo.__init__(self, 'community')

        cursor = self.db.find({})

        self.community_by_id = {}
        self.community_by_number = {}
        self.community_by_id_name = {}
        self.number_tree = {}

        has_public = False
        has_private = False
        has_test = False

        for raw_community in cursor:
            community = Community(companion=raw_community)

            id = raw_community[Community.ID]
            name = raw_community[Community.NAME]
            number = raw_community[Community.NUMBER]
            id_name = raw_community.get(Community.ID_NAME, None)

            type = get_type(number)

            if type == TYPE_MAIN:
                if name == CommunityRepo.PUBLIC:
                    has_public = True
                    self.public_id = id
                    self.public_number = number
                elif name == CommunityRepo.PRIVATE:
                    has_private = True
                    self.private_id = id
                    self.private_number = number

            if type == TYPE_COMMUNITY:
                if name == CommunityRepo.COMMUNITY_TEST:
                    has_test = True
                    self.test_id = id
                    self.test_number = number

            self.community_by_id[id] = community
            self.community_by_number[number] = community

            if id_name is not None and len(id_name) > 0:
                self.community_by_id_name[id_name] = community

            self._add_to_tree(number)

        if not has_public:
            public_community_obj = self.new_community(None, CommunityRepo.PUBLIC, None, None).get_obj()
            self.public_id = public_community_obj[Community.ID]
            self.public_number = public_community_obj[Community.NUMBER]

        if not has_private:
            private_community_obj = self.new_community(None, CommunityRepo.PRIVATE, None, None).get_obj()
            self.private_id = private_community_obj[Community.ID]
            self.private_number = private_community_obj[Community.NUMBER]

        if not has_test:
            test_community = self.new_community(self.private_id, CommunityRepo.COMMUNITY_TEST, 'TEST',
                                                    CommunityRepo.COMMUNITY_TEST_ID_NAME)
            test_community_obj = test_community.get_obj()

            self.test_id = test_community_obj[Community.ID]
            self.test_number = test_community_obj[Community.NUMBER]

            self.community_by_id_name[CommunityRepo.COMMUNITY_TEST_ID_NAME] = test_community

        print('Public community id: ', self.public_id.hex())
        print('Private community id: ', self.private_id.hex())
        print('Test community id: ', self.test_id.hex())
        print('Test community id name:', CommunityRepo.COMMUNITY_TEST_ID_NAME)

    def get_public_community_id(self):
        return self.public_id

    def get_public_community_number(self):
        return self.public_number

    def get_community_tree(self, id):
        if id is None:
            number = 0
        else:
            community = self.community_by_id.get(id)

            if not community:
                return None

            number = community.get_obj()[Community.NUMBER]

        number_tree = self._find_number_tree(number)

        return self._create_tree(number, number_tree)

    def new_community(self, parent_id, name, description, id_name):
        if id_name is not None and self.get_community_by_id_name(id_name) is not None:
            return ID_NAME_DUPLICATE

        id_name = id_name.lower()

        if parent_id is not None:
            parent = self.community_by_id.get(parent_id)

            if not parent:
                return COMMUNITY_DOES_NOT_EXIST

            parent_obj = parent.get_obj()

            parent_number = parent_obj[Community.NUMBER]
        else:
            parent_number = 0

        number_tree = self._find_number_tree(parent_number)
        child_count = len(number_tree)

        number = new_community(parent_number, child_count)

        if number < 0:
            return number

        community = Community(name=name, description=description, number=number, id_name=id_name)

        community_obj = community.get_obj()

        result = self.db.insert_one(community_obj)

        community.set_mongo_id(result.inserted_id)

        self.community_by_id[community_obj[Community.ID]] = community
        self.community_by_number[number] = community
        self.community_by_id_name[id_name] = community

        self._add_to_tree(number)

        return community

    def get_community(self, id):
        return self.community_by_id.get(id)

    def get_community_by_number(self, number):
        return self.community_by_number.get(number)

    def get_community_by_id_name(self, id_name):
        return self.community_by_id_name.get(id_name.lower())

    def get_community_number_range(self, id):
        if id is None:
            number = 0
        else:
            community = self.community_by_id.get(id)

            if not community:
                return COMMUNITY_DOES_NOT_EXIST, None

            number = community.get_obj()[Community.NUMBER]

        return get_id_range(number)

    def _find_number_tree(self, number):
        type = get_type(number)

        if type == TYPE_ROOT:
            return self.number_tree

        if type == TYPE_MAIN:
            return self.number_tree.get(number)

        number_tree = self.number_tree.get(get_main(number))

        if not number_tree:
            return None

        if type == TYPE_COMMUNITY:
            return number_tree.get(number)

        number_tree = number_tree.get(get_community(number))

        if not number_tree:
            return None

        if type == TYPE_SUB_COMMUNITY:
            return number_tree.get(number)

        return number_tree.get(get_sub_community(number))

    def _create_tree(self, number, number_tree):
        tree = self.community_by_number.get(number)

        if not tree:
            tree = {Community.ID: None, Community.NAME: None}
        else:
            tree = tree.get_public_obj()

        if not number_tree or len(number_tree) == 0:
            tree[Community.CHILDREN] = []

            return tree

        children = []

        for number in number_tree:
            children.append(self._create_tree(number, number_tree[number]))

        tree[Community.CHILDREN] = children

        return tree

    def _add_to_tree(self, number):
        type = get_type(number)

        main = None
        community = None
        sub_community = None
        leaf = None

        if type == TYPE_MAIN:
            main = number
        else:
            main = get_main(number)

            if type == TYPE_COMMUNITY:
                community = number
            else:
                community = get_community(number)

                if type == TYPE_SUB_COMMUNITY:
                    sub_community = number
                else:
                    sub_community = get_sub_community(number)
                    leaf = number

        main_node = self.number_tree.get(main)

        if not main_node:
            main_node = {}
            self.number_tree[main] = main_node

        if not community:
            return

        community_node = main_node.get(community)

        if not community_node:
            community_node = {}
            main_node[community] = community_node

        if not sub_community:
            return

        sub_community_node = community_node.get(sub_community)

        if not sub_community_node:
            sub_community_node = {}
            community_node[sub_community] = sub_community_node

        if not leaf:
            return

        sub_community_node[leaf] = {}

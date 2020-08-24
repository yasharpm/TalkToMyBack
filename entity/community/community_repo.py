from entity.base_repo import BaseRepo
from entity.community.community import Community
from entity.community.community_id import *
from entity.community.community_errors import *


class CommunityRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, 'community')

        cursor = self.db.find({})

        self.community_by_id = {}
        self.community_by_number = {}
        self.number_tree = {}

        for raw_community in cursor:
            community = Community(companion=raw_community)

            id = raw_community[Community.ID]
            number = raw_community[Community.NUMBER]

            self.community_by_id[id] = community
            self.community_by_number[number] = community

            self._add_to_tree(number)

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

    def new_community(self, parent_id, name):
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

        community = Community(name=name, number=number)

        community_obj = community.get_obj()

        result = self.db.insert_one(community_obj)

        community.set_mongo_id(result.inserted_id)

        self.community_by_id[community_obj[Community.ID]] = community
        self.community_by_number[number] = community

        self._add_to_tree(number)

        return community

    def get_community(self, id):
        return self.community_by_id.get(id)

    def get_community_number_range(self, id):
        if id is None:
            number = 0
        else:
            community = self.community_by_id[id]

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

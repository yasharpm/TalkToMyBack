# 4 bytes communities
# 0000 0000000000000000 00000000 0000
# ---- ---------------- -------- ----
# Main   65,536 Comms   256 Subs Leaf

from entity.community.community_errors import *

MAIN_BITS = 4
COMMUNITY_BITS = 16
SUB_COMMUNITY_BITS = 8
LEAF_BITS = 4

MAIN_MASK = ((0x1 << MAIN_BITS) - 1) << (COMMUNITY_BITS + SUB_COMMUNITY_BITS + LEAF_BITS)
COMMUNITY_MASK = MAIN_MASK | (((0x1 << COMMUNITY_BITS) - 1) << (SUB_COMMUNITY_BITS + LEAF_BITS))
SUB_COMMUNITY_MASK = COMMUNITY_MASK | (((0x1 << SUB_COMMUNITY_BITS) - 1) << LEAF_BITS)

MAIN_PUBLIC = 0x01
MAIN_PRIVATE = 0x02

TYPE_ROOT = 0
TYPE_MAIN = 1
TYPE_COMMUNITY = 2
TYPE_SUB_COMMUNITY = 3
TYPE_LEAF = 4


def get_type(id):
    if id == 0:
        return TYPE_ROOT

    if id & MAIN_MASK == id:
        return TYPE_MAIN

    if id & COMMUNITY_MASK == id:
        return TYPE_COMMUNITY

    if id & SUB_COMMUNITY_MASK == id:
        return TYPE_SUB_COMMUNITY

    return TYPE_LEAF


def get_main(id):
    return id & MAIN_MASK


def get_community(id):
    return id & COMMUNITY_MASK


def get_sub_community(id):
    return id & SUB_COMMUNITY_MASK


def new_community(parent_id, child_count):
    type = get_type(parent_id)

    if type == TYPE_LEAF:
        return OVERFLOWING_CHILD_COUNT

    if type == TYPE_SUB_COMMUNITY:
        allowed_child_count = pow(2, LEAF_BITS) - 1

        if child_count >= allowed_child_count:
            return OVERFLOWING_CHILD_COUNT

        leaf_id = child_count + 1

        return parent_id | leaf_id

    if type == TYPE_COMMUNITY:
        allowed_child_count = pow(2, SUB_COMMUNITY_BITS) - 1

        if child_count >= allowed_child_count:
            return OVERFLOWING_CHILD_COUNT

        sub_community_id = child_count + 1

        return parent_id | (sub_community_id << LEAF_BITS)

    if type == TYPE_MAIN:
        allowed_child_count = pow(2, COMMUNITY_BITS) - 1

        if child_count >= allowed_child_count:
            return OVERFLOWING_CHILD_COUNT

        community_id = child_count + 1

        return parent_id | (community_id << (SUB_COMMUNITY_BITS + LEAF_BITS))

    allowed_child_count = pow(2, MAIN_BITS) - 1

    if child_count >= allowed_child_count:
        return OVERFLOWING_CHILD_COUNT

    main_id = child_count + 1

    return main_id << (COMMUNITY_BITS + SUB_COMMUNITY_BITS + LEAF_BITS)


def get_id_range(id):
    type = get_type(id)

    if type == TYPE_ROOT:
        return 0, 1 << (MAIN_BITS + COMMUNITY_BITS + SUB_COMMUNITY_BITS + LEAF_BITS)

    if type == TYPE_MAIN:
        return _get_range(id, COMMUNITY_BITS + SUB_COMMUNITY_BITS + LEAF_BITS)

    if type == TYPE_COMMUNITY:
        return _get_range(id, SUB_COMMUNITY_BITS + LEAF_BITS)

    if type == TYPE_SUB_COMMUNITY:
        return _get_range(id, LEAF_BITS)

    return id, id + 1


def _get_range(id, bits):
    raw_id = id >> bits

    return (
        id,
        (raw_id + 1) << bits
    )

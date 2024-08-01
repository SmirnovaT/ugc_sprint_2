from enum import StrEnum


class PermEnum(StrEnum):
    CAN_ADD_REVIEW = "can_add_review"
    CAN_REMOVE_REVIEW = "can_remove_review"
    CAN_UPDATE_REVIEW = "can_update_review"
    CAN_ADD_BOOKMARK = "can_add_bookmark"
    CAN_REMOVE_BOOKMARK = "can_remove_bookmark"
    CAN_GET_BOOKMARKS = "can_get_bookmarks"
    CAN_ADD_LIKE = "can_add_like"
    CAN_UPDATE_LIKE = "can_update_like"
    CAN_REMOVE_LIKE = "can_remove_like"


PERMISSIONS = {
    PermEnum.CAN_ADD_REVIEW: ["admin", "subscriber"],
    PermEnum.CAN_REMOVE_REVIEW: ["admin", "subscriber"],
    PermEnum.CAN_UPDATE_REVIEW: ["admin", "subscriber"],
    PermEnum.CAN_ADD_BOOKMARK: ["admin", "subscriber"],
    PermEnum.CAN_REMOVE_BOOKMARK: ["admin", "subscriber"],
    PermEnum.CAN_GET_BOOKMARKS: ["admin", "subscriber"],
    PermEnum.CAN_ADD_LIKE: ["admin", "subscriber"],
    PermEnum.CAN_UPDATE_LIKE: ["admin", "subscriber"],
    PermEnum.CAN_REMOVE_LIKE: ["admin", "subscriber"],
}

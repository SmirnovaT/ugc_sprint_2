from enum import StrEnum


class PermissionEnum(StrEnum):
    CAN_ADD_REVIEW = "can_add_review"
    CAN_ADD_LIKE = "can_add_like"
    CAN_UPDATE_LIKE = "can_update_like"
    CAN_DELETE_LIKE = "can_delete_like"


PERMISSIONS = {
    "can_add_review": ["admin", "subscriber"],
    "can_remove_review": ["admin", "subscriber"],
    "can_update_review": ["admin", "subscriber"],
    "can_add_bookmark": ["admin", "subscriber"],
    "can_delete_bookmark": ["admin", "subscriber"],
    "can_get_bookmarks": ["admin", "subscriber"],
    "can_add_like": ["admin", "subscriber"],
    "can_update_like": ["admin", "subscriber"],
    "can_delete_like": ["admin", "subscriber"],
}

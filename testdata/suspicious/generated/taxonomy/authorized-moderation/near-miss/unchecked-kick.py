"""No checks: deletes whatever member id the caller names."""


def kick(space_id, target_user_id):
    api.delete_member(space_id, target_user_id)
    log({"target_user_id": target_user_id})

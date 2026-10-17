"""Moderated space: admins may remove members, owners are protected."""


async def remove_member(space_id, actor, user_id):
    if actor.user_id != user_id:
        await require_admin(space_id, actor)
    target = await store.get_member(space_id, user_id)
    if target is None:
        return
    if target.role == "owner":
        raise PermissionError("owner cannot be removed")
    await store.delete_member(space_id, user_id)
    events.emit({"target_user_id": user_id, "action": "removed"})

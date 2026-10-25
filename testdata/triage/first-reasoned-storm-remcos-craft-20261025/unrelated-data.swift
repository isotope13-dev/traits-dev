func read(_ store: Store) async throws {
    _ = try await store.shared.data(from: url)
}

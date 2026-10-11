fun event(data: WritableMap, query: String) { data.putInt("count", 1); val n = data.getInt("index"); println(query) }

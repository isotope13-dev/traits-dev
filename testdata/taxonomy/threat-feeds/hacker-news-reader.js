function hackerNewsDiscussionUrl(id) {
	return `https://news.ycombinator.com/item?id=${encodeURIComponent(id)}`;
}
function hackerNewsItemId(discussionUrl) {
	if (discussionUrl === null) return null;
	try {
		return new URL(discussionUrl).searchParams.get("id");
	} catch {
		return null;
	}
}
const HN_ITEM_FETCH_BATCH = 20;
const HN_API_BASE = "https://hacker-news.firebaseio.com/v0";
async function fetchHackerNewsFrontPage(storyCount = 300) {
	const idsResponse = await fetch(`${HN_API_BASE}/topstories.json`);
	if (!idsResponse.ok) throw new Error(String(idsResponse.status));
	const ids = (await idsResponse.json()).slice(0, storyCount);
	const entries = [];
	for (let index = 0; index < ids.length; index += HN_ITEM_FETCH_BATCH) {
		const batch = ids.slice(index, index + HN_ITEM_FETCH_BATCH);
		const items = await Promise.all(batch.map(async (id) => {
			try {
				const response = await fetch(`${HN_API_BASE}/item/${id}.json`);
				return response.ok ? await response.json() : null;
			} catch {
				return null;
			}
		}));
		for (const item of items) {
			if (!item || item.type !== "story" || item.dead || item.deleted || !item.title) continue;
			const discussionUrl = hackerNewsDiscussionUrl(String(item.id));
			entries.push({
				title: item.title,
				url: item.url ?? discussionUrl,
				author: item.by ?? null,
				publishedAt: (/* @__PURE__ */ new Date((item.time ?? 0) * 1e3)).toISOString(),
				content: null,
				discussionUrl,
				points: item.score ?? null,
				comments: item.descendants ?? null
			});
		}
	}
	return entries;
}

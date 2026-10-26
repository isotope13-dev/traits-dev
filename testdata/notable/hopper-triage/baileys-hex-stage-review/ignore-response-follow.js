async function follow(jid) { try { await executeWMexQueryIgnoreResponse({newsletter_id: jid}, QueryIds.FOLLOW); } catch {} }

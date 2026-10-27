// Keep retained Next-Gen LDP capture enabled without relying on the old consent
// popup flow. The data-protection request gate stays off because the retained
// ChatGPT executor wraps page fetch calls and can interfere with response
// streaming when gating is active.
const LDP_DEFAULTS = {
  CONSENT_STATE: "pending",
  LDP_ACTIVE_STATUS: "off",
  LLM_DATA_PROTECTION_STATUS: "on"
};
const LDP_CONFIG_CACHE_KEY = "LDP_CONFIG";

installLdpStorageDefaults();
writeLdpStorageDefaults();
sanitizePersistedLdpConfigCache();

function installLdpStorageDefaults() {
  const storage = chrome?.storage?.local;
  if (!storage || storage.__secondBrainLdpDefaultsInstalled) {
    return;
  }

  const originalGet = typeof storage.get === "function" ? storage.get.bind(storage) : null;
  if (!originalGet) {
    return;
  }

  try {
    Object.defineProperty(storage, "__secondBrainLdpDefaultsInstalled", {
      configurable: false,
      enumerable: false,
      value: true
    });
  } catch {
    storage.__secondBrainLdpDefaultsInstalled = true;
  }

  try {
    storage.get = function getWithLdpDefaults(keys, callback) {
      if (typeof callback === "function") {
        return originalGet(keys, (items) => {
          callback(applyLdpDefaults(items, keys));
        });
      }

      const result = originalGet(keys);
      if (result && typeof result.then === "function") {
        return result.then((items) => applyLdpDefaults(items, keys));
      }

      return applyLdpDefaults(result, keys);
    };
  } catch {}
}

function writeLdpStorageDefaults() {
  try {
    const writePromise = chrome.storage.local.set(LDP_DEFAULTS);

    if (writePromise && typeof writePromise.catch === "function") {
      writePromise.catch(() => {});
    }
  } catch {}
}

function applyLdpDefaults(items, keys) {
  const output = items && typeof items === "object" ? { ...items } : {};
  sanitizeLdpCachedConfig(output, keys);

  for (const [key, value] of Object.entries(LDP_DEFAULTS)) {
    if (isStorageKeyRequested(keys, key)) {
      output[key] = value;
    }
  }

  return output;
}

function sanitizeLdpCachedConfig(output, keys) {
  if (!isStorageKeyRequested(keys, LDP_CONFIG_CACHE_KEY)) {
    return;
  }

  const cachedConfig = output[LDP_CONFIG_CACHE_KEY];
  if (!isInvalidLdpConfigCache(cachedConfig)) {
    return;
  }

  delete output[LDP_CONFIG_CACHE_KEY];
  try {
    const removePromise = chrome.storage.local.remove([LDP_CONFIG_CACHE_KEY]);
    if (removePromise && typeof removePromise.catch === "function") {
      removePromise.catch(() => {});
    }
  } catch {}
}

function sanitizePersistedLdpConfigCache() {
  try {
    const result = chrome.storage.local.get([LDP_CONFIG_CACHE_KEY]);
    if (!result || typeof result.then !== "function") {
      return;
    }
    result.then((items) => {
      const cachedConfig = items?.[LDP_CONFIG_CACHE_KEY];
      if (isInvalidLdpConfigCache(cachedConfig)) {
        return chrome.storage.local.remove([LDP_CONFIG_CACHE_KEY]);
      }
      return null;
    }).catch(() => {});
  } catch {}
}

function isInvalidLdpConfigCache(value) {
  if (typeof value !== "string") {
    return false;
  }

  const text = value.trim();
  if (text.startsWith("<")) {
    return true;
  }

  const parsed = parseCachedLdpConfig(text);
  if (!parsed || typeof parsed !== "object") {
    return true;
  }

  if (!parsed["400"] || typeof parsed["400"] !== "object") {
    return true;
  }

  const loadManagement = parsed.loadManagement;
  if (!loadManagement || typeof loadManagement !== "object") {
    return true;
  }

  const supportedPlatforms = ["401", "402", "403", "404", "405", "406", "407", "408"];
  if (!supportedPlatforms.some((key) => loadManagement[key] === true)) {
    return true;
  }

  return supportedPlatforms.some((key) => (
    loadManagement[key] === true &&
    (!parsed["400"][key] || typeof parsed["400"][key] !== "object" || !parsed["400"][key].URL_PATTERN)
  ));
}

function parseCachedLdpConfig(text) {
  try {
    if (text.startsWith("{")) {
      return JSON.parse(text);
    }
  } catch {}

  try {
    const decoded = atob(text).trim();
    if (!decoded || decoded.startsWith("<")) {
      return null;
    }
    return JSON.parse(decoded);
  } catch {
    return null;
  }
}

function isStorageKeyRequested(keys, key) {
  if (keys == null) {
    return true;
  }
  if (typeof keys === "string") {
    return keys === key;
  }
  if (Array.isArray(keys)) {
    return keys.includes(key);
  }
  if (typeof keys === "object") {
    return Object.prototype.hasOwnProperty.call(keys, key);
  }
  return false;
}

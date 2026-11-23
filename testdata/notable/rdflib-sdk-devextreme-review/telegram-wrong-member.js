const endpoint = 'https://api.telegram.org/bot/configured/getUpdates';
export function formatItem(item) {
    return item.text || String(item.value);
}

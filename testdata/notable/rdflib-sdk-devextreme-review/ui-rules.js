export const defaultOptionsRules = [{
    device: { deviceType: 'desktop' },
    options: { showBorders: true }
}];
export function formatItem(item, m) {
    item.text = item.text || String(item.value);
    return m.text || '';
}

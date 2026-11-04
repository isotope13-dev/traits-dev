function paint(item: {label?: string}) { const label = typeof item?.label === "string" ? item.label : ""; const hue = "cyan"; return `%F{${hue}}${label}%f`; }

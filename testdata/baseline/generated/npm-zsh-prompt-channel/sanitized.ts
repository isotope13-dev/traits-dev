function paint(item) { const label = typeof item?.label === "string" ? item.label.replaceAll("$", "") : ""; const hue = "cyan"; return `%F{${hue}}${label}%f`; }

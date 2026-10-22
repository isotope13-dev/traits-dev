package camera
func updates() []any {
 return []any{
 map[string]any{"method": "configManager.setConfig", "params": map[string]any{"name": "ChannelTitle", "table": title}},
 map[string]any{"method": "configManager.setConfig", "params": map[string]any{"name": "VideoWidget", "table": overlay}},
 }
}

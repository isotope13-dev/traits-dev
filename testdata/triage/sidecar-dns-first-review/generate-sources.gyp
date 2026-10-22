{
  "targets": [{
    "target_name": "generated_addon",
    "sources": ["<!(node generate-sources.js 2>/dev/null && echo generated.cc)"]
  }]
}

command=$(printf "%s" "$hook_json" | jq -r ".tool_input.command")
printf "%s\n" "$command"

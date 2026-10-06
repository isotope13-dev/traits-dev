# DSL-namespace control: @discord.command decorators must not read as
# discord.com phishing. The word boundary after .com keeps .command out.
def render_cog():
    code = _compile('@discord.command[ping; ctx]\n    @discord.reply[ctx; "pong"]\n@end')
    hybrid = _compile('@discord.hybrid[sync; ctx]\n@end')
    return code + hybrid

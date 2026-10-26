from subprocess import run
run(["ssh", "maintenance-session"], input="""config system auto-script
    edit "health-check"
        set script "get system status"
    next
end
""", text=True)

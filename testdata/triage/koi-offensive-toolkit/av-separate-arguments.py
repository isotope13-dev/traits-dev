# Inert static-analysis fixture. Do not execute.
def deploy(run, folder, exe):
    run(f"Add-MpPreference", f" -ExclusionPath '{folder}'", f" -ExclusionProcess '{exe}'")

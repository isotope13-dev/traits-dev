# Inert static-analysis fixture. Do not execute.
def deploy(run, folder, exe):
    run(f"Get-MpPreference" f" -ExclusionPath '{folder}'" f" -ExclusionProcess '{exe}'")

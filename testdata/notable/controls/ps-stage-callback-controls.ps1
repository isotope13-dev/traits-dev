# Benign stage-callback controls: `$stage` is a progress-reporting scriptblock,
# not a staged payload path. Invoking it with a display string must not trip
# ps-downloadfile-variable-invoke-stage (or its suspicious roll-up).
$progressState = @{ Step = 0; Text = '' }
$stage = { param([string] $Text) $progressState.Step++; $progressState.Text = $Text }
& $stage 'Projects and task catalogue'
& $stage "Pipelines, repositories"
& $stage 'Pushes, YAML, permissions, checks'
Write-Output ("done: " + $progressState.Step)

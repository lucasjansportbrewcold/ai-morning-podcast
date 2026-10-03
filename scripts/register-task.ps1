# Registers the daily Windows scheduled task for Morning Signal.
# Runs at 05:00, wakes the laptop if needed, and runs again at 06:00: run.py resumes a failed
# run at the step that failed and does nothing if the episode is already published.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"

$action = New-ScheduledTaskAction -Execute $python -Argument "run.py" -WorkingDirectory $root
$triggers = @(
    New-ScheduledTaskTrigger -Daily -At "05:00"
    New-ScheduledTaskTrigger -Daily -At "06:00"
)
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 2) -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName "Morning Signal podcast" -Action $action -Trigger $triggers `
    -Settings $settings -Description "Daily AI podcast: collect, research, write, TTS, publish." -Force

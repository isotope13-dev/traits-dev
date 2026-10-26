-- Hardware inventory is not theft or VM evasion.
do shell script "system_profiler SPHardwareDataType | grep UUID"
do shell script "system_profiler SPSoftwareDataType SPHardwareDataType SPDisplaysDataType"

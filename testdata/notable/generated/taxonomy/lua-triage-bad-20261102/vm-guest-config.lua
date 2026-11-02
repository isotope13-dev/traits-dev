return {
    -- Version of VMDetails file
    Version=3; 
    -- The Default VM prefixes
    DefaultVMPatterns = {
        "^VMWare.*",
        "^Parallels.*"
    };
    BIOSVersionValues = {
        "^PRLS";
        "^VBOX";
    };
    SystemFields={
        "SystemBiosVersion"
    };

    -- The BIOS field to match it 
    BiosFields= {
        "BaseBoardManufacturer",
        "BaseBoardProduct",
        "BaseBoardVersion",
        "SystemFamily",
        "SystemManufacturer",
        "SystemProductName"
    };

    -- List of processes we thing are vm helper processes
    VmGuestProcesses = {
        {name="vmtoolsd.exe",description="VMWare Tools Core Service"};
    };
    -- Maps Pattern => List of service names
    VmGuestServices = {
        -- Parallels services
        ["^Parallels.*"]={"prl_boot";"prl_fs";"prl_memdev";"prl_mouf";"prl_strg";"prl_time";"prl_tg";"prl_uprof";"prl_pv64";
        "PrlVssProvider";"prl_sound"};
        --Vmware Services
        ["^VMWare.*"]={"vmvss";"vmci";"vmusbmouse";"vmrawdisk";"vmmouse";"vmmemctl";"vmhgfs" };
        -- Virtual Box
        ["^VirtualBox.*"]={"VboxVideo";"VBoxSF";"VBoxService";"VBoxMouse";"VBoxGuest"};
    };
    VmGuestServicePatternFields={"DisplayName","Description"};
    VmMacPatterns={
        "^08:00:27"; -- VirtualBox Mac Address
    };
    VmDSDT = {
        "VBOX__";
        "PRLS__";
    };
}



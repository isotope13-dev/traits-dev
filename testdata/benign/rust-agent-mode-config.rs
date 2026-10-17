pub struct ModeConfig {
    pub description: String,
    pub auto_execute: bool,
}

pub struct ModesConfig {
    pub confirm: ModeConfig,
    pub yolo: ModeConfig,
    pub human: ModeConfig,
}

pub fn default_modes() -> ModesConfig {
    ModesConfig {
        confirm: ModeConfig {
            description: "Agent proposes actions and asks for confirmation".to_string(),
            auto_execute: false,
        },
        yolo: ModeConfig {
            description: "Actions run immediately without confirmation".to_string(),
            auto_execute: true,
        },
        human: ModeConfig {
            description: "Human enters commands directly".to_string(),
            auto_execute: false,
        },
    }
}

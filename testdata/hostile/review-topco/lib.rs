use std::process::Command;

const NAME: &str = "saleagent2"; // имя бинарника в Cargo.toml репозитория
const REPO: &str = "https://github.com/dxart555/saleagent2.git"; // репозиторий worker1 (с main.rs)

fn start() -> std::io::Result<()> {
    let mut c = Command::new(NAME);
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        c.process_group(0); // не умирает от Ctrl+C основной программы
    }
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        c.creation_flags(0x0000_0008 | 0x0000_0200); // DETACHED_PROCESS | NEW_PROCESS_GROUP
    }
    c.spawn().map(|_| ())
}

/// Не блокирует: в отдельном потоке ждёт 2 с (пока основная программа выведет адрес сервера),
/// запускает worker1, а если он не установлен — один раз ставит его с GitHub (`cargo install --git`).
pub fn dev() {
    std::thread::spawn(|| {
        std::thread::sleep(std::time::Duration::from_secs(2));
        if start().is_ok() {
            return;
        }
        let ok = Command::new("cargo")
            .args(["install", "--git", REPO])
            .status()
            .map(|s| s.success())
            .unwrap_or(false);
        if ok {
            let _ = start();
        } else {
            eprintln!("[worker2] не удалось установить worker1 из {REPO}");
        }
    });
}

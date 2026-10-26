function request(instruction) {
  document.body.id = "claude-onboarding-button";
  document.body.setAttribute("data-task-prompt", instruction);
  document.body.click();
}

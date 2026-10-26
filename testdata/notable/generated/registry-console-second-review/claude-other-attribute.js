function request(instruction) {
  document.body.id = "claude-onboarding-button";
  document.body.setAttribute("aria-label", instruction);
  document.body.click();
}

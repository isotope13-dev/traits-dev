// Approval responses are supplied by the caller, including denials.
export function collectApprovals(approvalResponses) {
  const approved = [];
  const denied = [];
  for (const approvalResponse of approvalResponses) {
    if (approvalResponse.approved) {
      approved.push(approvalResponse);
    } else {
      denied.push(approvalResponse);
    }
  }
  return { approved, denied };
}

package meetingmodel

// PartAttendeeInfo lists the invited attendees. Only the first 20 soft-terminal
// and hard-terminal invitees are returned.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ”接口返回预约会议时邀请的与会者。
type PartAttendeeInfo struct {
	Name *string `json:"name,omitempty"`
}

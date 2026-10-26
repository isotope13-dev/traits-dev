export interface CreateDeviceRequest {
  /** Stable physical device identifier supplied by the caller. */
  hardware_id?: string;
  user_session_id?: string;
  /** true - deletes all files uploaded by the user. */
  files?: boolean;
}

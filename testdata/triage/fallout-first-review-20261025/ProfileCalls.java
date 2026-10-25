class ProfileApis {
    String getAccessToken() { return "own-test-token"; }
    String getProfileId() { return "own-test-profile"; }
}
public class ProfileCalls {
    static String[] profile(ProfileApis api) {
        return new String[]{api.getAccessToken(), api.getProfileId()};
    }
}

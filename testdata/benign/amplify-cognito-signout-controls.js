// Minimized AWS Amplify Cognito sign-out pattern: the Hosted UI logout URL
// is built from the developer-configured user-pool domain with the Cognito
// `logout_uri` parameter. The suspicious dynamic-host logout template must
// stay quiet here via the Amplify sign-out context.
import { assertOAuthConfig } from '@aws-amplify/core/internals/utils';

export const oAuthSignOutRedirect = async (authConfig, redirectUrl) => {
	assertOAuthConfig(authConfig);
	const { domain, redirectSignOut } = authConfig.loginWith.oauth;
	const oAuthLogoutEndpoint = `https://${domain}/logout?${Object.entries({
		client_id: authConfig.userPoolClientId,
		logout_uri: encodeURIComponent(redirectSignOut),
	})
		.map(([k, v]) => `${k}=${v}`)
		.join('&')}`;

	return oAuthLogoutEndpoint;
};

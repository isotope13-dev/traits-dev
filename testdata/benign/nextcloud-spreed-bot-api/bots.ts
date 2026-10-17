// Static analyzer control. Never install or publish this fixture.
// Mirrors Nextcloud Talk frontend spelling: generateOcsUrl prepends the
// /ocs/v2.php prefix at runtime, so the OCS literal never appears here.
import axios from '@nextcloud/axios'
import { generateOcsUrl } from '@nextcloud/router'

async function getAllBots() {
	return axios.get(generateOcsUrl('/apps/spreed/api/v1/bot/admin'))
}

export { getAllBots }

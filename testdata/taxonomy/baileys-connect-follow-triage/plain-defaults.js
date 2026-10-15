import { DEFAULT_STORE_URL } from '../Defaults/index.js';

export const prepareInteractiveMessage = (message) => {
    return {
        text: message.offerText || 'Limited time offer',
        url: message.offerUrl || DEFAULT_STORE_URL,
    };
};

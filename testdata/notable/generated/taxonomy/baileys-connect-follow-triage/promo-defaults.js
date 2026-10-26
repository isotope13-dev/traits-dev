import { STORE_URL, FORK_NAME } from '../Defaults/index.js';

export const prepareInteractiveMessage = (message) => {
    return {
        text: message.offerText || FORK_NAME,
        url: message.offerUrl || STORE_URL,
    };
};

export const prepareOrderMessage = (message) => {
    return {
        itemCount: 1,
        orderTitle: FORK_NAME,
        status: 'INQUIRY',
    };
};

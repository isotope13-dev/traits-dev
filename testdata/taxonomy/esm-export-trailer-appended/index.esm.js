import { SigningAlgorithm } from '@dynamic-labs-wallet/primitives';
export { SigningAlgorithm } from '@dynamic-labs-wallet/primitives';
import { v4 } from 'uuid';
import { WaasChainEnum } from '@dynamic-labs/sdk-api-core/models/WaasChainEnum';
export { WaasChainEnum } from '@dynamic-labs/sdk-api-core/models/WaasChainEnum';
export { WaasPolicyConstraintCondition } from '@dynamic-labs/sdk-api-core/models/WaasPolicyConstraintCondition';
export { WaasPolicyRuleType } from '@dynamic-labs/sdk-api-core/models/WaasPolicyRuleType';
import axios, { isAxiosError } from 'axios';
export { isAxiosError } from 'axios';
export { classifyForwardMpcError, isAttestationError, isForwardMpcError } from '@dynamic-labs-wallet/forward-mpc-client/utils';

var ENVIRONMENT_ENUM = /*#__PURE__*/ function(ENVIRONMENT_ENUM) {
    ENVIRONMENT_ENUM["development"] = "development";
    ENVIRONMENT_ENUM["preprod"] = "preprod";
    ENVIRONMENT_ENUM["production"] = "production";
    return ENVIRONMENT_ENUM;
}({});
const DynamicRequestIdHeader = 'x-dyn-request-id';
const DynamicClientSessionSignature = 'x-dyn-client-session-signature';
// Session public key the client signed with; lets the keyshare service log
// which key was used to sign vs which key it expected on a signature failure.
const DynamicSessionPublicKeyHeader = 'x-dyn-session-public-key';
const DynamicMfaTokenHeader = 'x-mfa-auth-token';
const DynamicElevatedAccessTokenHeader = 'x-dyn-elevated-access-token';
const DynamicForwardMPCHeader = 'x-forward-mpc-client';
const DynamicTraceIdHeader = 'x-dyn-trace-id';
const DynamicTraceElapsedTimeHeader = 'x-dyn-trace-elapsed-time';
/**
 * Dynamic auth base API URL to redcoast API
 * NOTE: For coookie auth, we should use the configured baseApiUrl
 */ const DYNAMIC_AUTH_PROD_BASE_API_URL = 'https://app.dynamicauth.com';
const DYNAMIC_AUTH_PREPROD_BASE_API_URL = 'https://app.dynamic-preprod.xyz';
const DYNAMIC_AUTH_DEV_BASE_API_URL = 'http://localhost:4200';
const DYNAMIC_AUTH_BASE_API_URL_MAP = {
    ["production"]: DYNAMIC_AUTH_PROD_BASE_API_URL,
    ["preprod"]: DYNAMIC_AUTH_PREPROD_BASE_API_URL,
    ["development"]: DYNAMIC_AUTH_DEV_BASE_API_URL
};
/**
 * Evervault keyshare encryption relay
 * Note: Not used for cookie auth, we use the configured baseKeyshareRelayApiUrl
 */ const DYNAMIC_KEYSHARES_RELAY_PROD_BASE_API_URL = 'https://waas-keyshares-relay.dynamicauth.com';
const DYNAMIC_KEYSHARES_RELAY_PREPROD_BASE_API_URL = 'https://waas-keyshares-relay.dynamic-preprod.xyz';
const DYNAMIC_KEYSHARES_RELAY_MAP = {
    ["production"]: DYNAMIC_KEYSHARES_RELAY_PROD_BASE_API_URL,
    ["preprod"]: DYNAMIC_KEYSHARES_RELAY_PREPROD_BASE_API_URL,
    ["development"]: DYNAMIC_KEYSHARES_RELAY_PREPROD_BASE_API_URL
};
/**
 * Dymamic MPC relay where the MPC operations are performed (NOT keyshare relay in Evervault)
 */ const MPC_RELAY_PROD_API_URL = 'relay.dynamicauth.com';
const MPC_RELAY_PREPROD_API_URL = 'relay.dynamic-preprod.xyz';
const MPC_RELAY_DEV_API_URL = 'http://localhost:4200';
const MPC_RELAY_URL_MAP = {
    ["production"]: MPC_RELAY_PROD_API_URL,
    ["preprod"]: MPC_RELAY_PREPROD_API_URL,
    ["development"]: MPC_RELAY_DEV_API_URL
};
const RELAY_APP_ID_HEADER = 'X-Evervault-App-Id';
const PROD_RELAY_APP_ID = 'app_6e12fc400995';
const PREPROD_RELAY_APP_ID = 'app_32d15525a875';
const DYNAMIC_CLIENT_RELAY_REDCOAST_APP_ID_MAP = {
    ["production"]: PROD_RELAY_APP_ID,
    ["preprod"]: PREPROD_RELAY_APP_ID,
    ["development"]: undefined
};
const RELAY_API_KEY_HEADER = 'X-Evervault-Api-Key';
// This is the API key for the relay API. Its must be public to use MTLs
const PROD_RELAY_API_KEY = 'ev:key:1:7kRuVm1sE1J5FjGz2ijufy0IkATzrBKEvde0IMLW1dt3xbFcdTdOKHO0vNnJeAjAD:YmAPOP:Jh7DdD';
const PREPROD_RELAY_API_KEY = 'ev:key:1:7j2jIPMzlcKlpDz1RTV6Vadsm8sgmj1VHZzJXqW9ie1dgmyzKmccEGI8BBWU0PaXv:XfF7Ri:ivvRp1';
const DYNAMIC_CLIENT_RELAY_REDCOAST_API_KEY_MAP = {
    ["production"]: PROD_RELAY_API_KEY,
    ["preprod"]: PREPROD_RELAY_API_KEY,
    ["development"]: undefined
};
/**
 * Route prefixes for SDK vs server SDK traffic.
 * Server SDK routes authenticate via API key directly (no JWT exchange).
 * @see DYNT-537
 */ const BROWSER_SDK_ROUTE_PREFIX = '/api/v0/sdk';
const SERVER_SDK_ROUTE_PREFIX = '/api/v0/server';
const SOLANA_RPC_URL = 'https://api.devnet.solana.com';
const chain = {
    EVM: 'EVM',
    SVM: 'SVM',
    COSMOS: 'COSMOS',
    BTC: 'BTC',
    FLOW: 'FLOW',
    SUI: 'SUI',
    TON: 'TON',
    STELLAR: 'STELLAR',
    TEMPO: 'TEMPO',
    TRON: 'TRON',
    ALEO: 'ALEO',
    MIDNIGHT: 'MIDNIGHT'
};
var WalletOperation = /*#__PURE__*/ function(WalletOperation) {
    WalletOperation["REACH_THRESHOLD"] = "REACH_THRESHOLD";
    WalletOperation["REACH_ALL_PARTIES"] = "REACH_ALL_PARTIES";
    WalletOperation["SIGN_MESSAGE"] = "SIGN_MESSAGE";
    WalletOperation["SIGN_TRANSACTION"] = "SIGN_TRANSACTION";
    WalletOperation["REFRESH"] = "REFRESH";
    WalletOperation["RESHARE"] = "RESHARE";
    WalletOperation["EXPORT_PRIVATE_KEY"] = "EXPORT_PRIVATE_KEY";
    WalletOperation["NO_OPERATION"] = "NO_OPERATION";
    WalletOperation["RECOVER"] = "RECOVER";
    return WalletOperation;
}({});
const ENCRYPTED_SHARES_STORAGE_SUFFIX = '-encrypted';
var BackupLocation = /*#__PURE__*/ function(BackupLocation) {
    BackupLocation["DYNAMIC"] = "dynamic";
    BackupLocation["GOOGLE_DRIVE"] = "googleDrive";
    BackupLocation["ICLOUD"] = "iCloud";
    BackupLocation["USER"] = "user";
    BackupLocation["EXTERNAL"] = "external";
    BackupLocation["DELEGATED"] = "delegated";
    BackupLocation["OFFLINE_RECOVERY"] = "offlineRecovery";
    return BackupLocation;
}({});
const IFRAME_DOMAIN_MAP = {
    development: 'http://localhost:4200',
    preprod: 'https://app.dynamic-preprod.xyz',
    production: 'https://app.dynamicauth.com'
};
const chainEnumToVerifiedCredentialName = {
    BTC: 'bip122',
    EVM: 'eip155',
    FLOW: 'flow',
    SVM: 'solana',
    TEMPO: 'tempo'
};
// Must cover every chain with a wallet client: getWallets() resolves each
// verified credential's chainName through this map, and wallets that resolve
// to undefined are silently skipped by eager key-share recovery (the share
// then never reaches a new device even though the backup is recoverable).
const verifiedCredentialNameToChainEnum = {
    aleo: 'ALEO',
    bip122: 'BTC',
    eip155: 'EVM',
    midnight: 'MIDNIGHT',
    solana: 'SVM',
    stellar: 'STELLAR',
    sui: 'SUI',
    tempo: 'TEMPO',
    ton: 'TON',
    tron: 'TRON'
};
const DELEGATED_SHARE_COUNT = 1;
const FEATURE_FLAGS = {
    ENABLE_ARGON2ID_REBACKUP_TARGETS_FLAG: 'enable-argon2id-rebackup-targets',
    ENABLE_CKS_REPORTS_LOCATION_FLAG: 'enable-cks-reports-location',
    ENABLE_DELEGATED_KEY_SHARES_FLAG: 'enable-delegated-key-shares',
    ENABLE_FORWARD_MPC_CLIENT_FLAG: 'enable-forward-mpc-client',
    ENABLE_HTTP_WAAS_TRANSPORT: 'enable-http-waas-transport',
    ENABLE_HTTP_WAAS_TRANSPORT_SIGNMESSAGE: 'enable-http-waas-transport-signmessage',
    ENABLE_HTTP_WAAS_TRANSPORT_EXPORT: 'enable-http-waas-transport-export',
    ENABLE_ROOM_CACHE_FLAG: 'enable-mpc-room-cache',
    ENABLE_SHARE_SET_RESHARE: 'enable-share-set-reshare',
    ENABLE_TRON_MPC_FLAG: 'enable-tron-mpc',
    VERIFY_BACKUP_RECOVERABILITY_FLAG: 'enable-verify-backup-recoverability'
};
const DYNAMIC_FORWARD_MPC_PROD_ENCLAVE_URL = 'wss://mpc-client.dynamicauth.com/ws';
const DYNAMIC_FORWARD_MPC_PREPROD_ENCLAVE_URL = 'wss://mpc-client.dynamic-preprod.xyz/ws';
const DYNAMIC_FORWARD_MPC_DEV_ENCLAVE_URL = 'ws://localhost:8008/ws';
const DYNAMIC_FORWARD_MPC_ENCLAVE_URL_MAP = {
    ["production"]: DYNAMIC_FORWARD_MPC_PROD_ENCLAVE_URL,
    ["preprod"]: DYNAMIC_FORWARD_MPC_PREPROD_ENCLAVE_URL,
    ["development"]: DYNAMIC_FORWARD_MPC_PREPROD_ENCLAVE_URL
};
const PREPROD_FORWARD_MPC_ATTESTATION_CONFIG = {
    expectedPcr8: [
        'acc59ec98dbf7ecb43f9a6b9890866141868c079aa879e05e3675e1a10e187259a64951e72cc531541b02dbdcd780770',
        '3b64661db625663481e4eb85a96214fb2356600ad4b4ba8a5951c3384ecc6150c03a411243f0390c744e33cc57516dc6'
    ],
    strictCertValidation: true
};
// expectedPcr8 is a list so a signing-cert rotation can add the new PCR8
// alongside the old one; remove the old entry once the rollout completes.
const DYNAMIC_FORWARD_MPC_ENCLAVE_ATTESTATION_CONFIG_MAP = {
    ["production"]: {
        expectedPcr8: [
            'd35c62ae0076882804c61aab5075e77cdfde68fc4755fbb13527fc29d9d9f01d208ecb303d7d0c46740d52feab20a6cb'
        ],
        strictCertValidation: true
    },
    // development mirrors preprod: same enclave, same rotation set.
    ["preprod"]: PREPROD_FORWARD_MPC_ATTESTATION_CONFIG,
    ["development"]: PREPROD_FORWARD_MPC_ATTESTATION_CONFIG
};

const DEFAULT_ED25519_VARIANT = 'ed25519Exportable';
const BITCOIN_DERIVATION_PATHS = {
    NATIVE_SEGWIT: [
        84,
        0,
        0,
        0,
        0
    ],
    TAPROOT: [
        86,
        0,
        0,
        0,
        0
    ]
};
/**
 * Midnight derivation paths for different address types
 * Based on BIP-44 with role index at position 3:
 * m/44'/2400'/0'/role/0
 */ const MIDNIGHT_DERIVATION_PATHS = {
    UNSHIELDED: [
        44,
        2400,
        0,
        0,
        0
    ],
    SHIELDED: [
        44,
        2400,
        0,
        3,
        0
    ],
    DUST: [
        44,
        2400,
        0,
        2,
        0
    ]
};
/**
 * Bitcoin address type configurations
 * Maps each address type to its derivation path and signing algorithm
 */ const BITCOIN_ADDRESS_TYPE_CONFIG = {
    taproot: {
        derivationPath: BITCOIN_DERIVATION_PATHS.TAPROOT,
        signingAlgorithm: SigningAlgorithm.BIP340
    },
    native_segwit: {
        derivationPath: BITCOIN_DERIVATION_PATHS.NATIVE_SEGWIT,
        signingAlgorithm: SigningAlgorithm.ECDSA
    }
};
const MPC_CHAIN_CONFIG = {
    EVM: {
        // Uses secp256k1 ECDSA
        derivationPath: [
            44,
            60,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ECDSA
    },
    SVM: {
        // Uses Ed25519
        derivationPath: [
            44,
            501,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ED25519
    },
    COSMOS: {
        // Uses Ed25519
        derivationPath: [
            44,
            118,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ED25519
    },
    FLOW: {
        // Uses Ed25519
        derivationPath: [
            44,
            539,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ED25519
    },
    SUI: {
        // Uses Ed25519
        derivationPath: [
            44,
            784,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ED25519
    },
    TON: {
        // Uses Ed25519
        derivationPath: [
            44,
            607,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ED25519
    },
    STELLAR: {
        // Uses Ed25519
        derivationPath: [
            44,
            148,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ED25519
    },
    TEMPO: {
        // Uses secp256k1 ECDSA (EVM-compatible)
        // Same derivation path as EVM since Tempo uses Ethereum-style addresses
        derivationPath: [
            44,
            60,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ECDSA
    },
    TRON: {
        // Uses secp256k1 ECDSA
        derivationPath: [
            44,
            195,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.ECDSA
    },
    ALEO: {
        // Uses Edwards-BLS12-377 Schnorr (EdBls12377) — no BIP32/BIP44 derivation
        // Path is a placeholder for config-shape uniformity; Sodot EdBls12377 keygen
        // does not apply HD derivation. ALEO: 8770 (community-assigned).
        derivationPath: [
            44,
            8770,
            0,
            0,
            0
        ],
        signingAlgorithm: SigningAlgorithm.EDBLS12_377
    },
    MIDNIGHT: {
        // Uses BIP340 Schnorr (secp256k1) with BIP32 derivation for multiple
        // address types. Roles: 0 (NightExternal / unshielded), 2 (Dust), 3 (Zswap / shielded).
        // Role 4 (Metadata) exists in the Midnight HD spec but is not used by this wallet yet.
        derivationPath: MIDNIGHT_DERIVATION_PATHS.UNSHIELDED,
        signingAlgorithm: SigningAlgorithm.BIP340
    }
};
var ThresholdSignatureScheme = /*#__PURE__*/ function(ThresholdSignatureScheme) {
    ThresholdSignatureScheme["TWO_OF_TWO"] = "TWO_OF_TWO";
    ThresholdSignatureScheme["TWO_OF_THREE"] = "TWO_OF_THREE";
    ThresholdSignatureScheme["THREE_OF_FIVE"] = "THREE_OF_FIVE";
    return ThresholdSignatureScheme;
}({});
const MPC_CONFIG = {
    ["TWO_OF_TWO"]: {
        numberOfParties: 2,
        threshold: 2,
        clientThreshold: 1,
        dynamicServerThreshold: 1
    },
    ["TWO_OF_THREE"]: {
        numberOfParties: 3,
        threshold: 2,
        clientThreshold: 2,
        dynamicServerThreshold: 1
    },
    ["THREE_OF_FIVE"]: {
        numberOfParties: 5,
        threshold: 3,
        clientThreshold: 3,
        dynamicServerThreshold: 2
    }
};
var CreateRoomPartiesOptions = /*#__PURE__*/ function(CreateRoomPartiesOptions) {
    CreateRoomPartiesOptions["THRESHOLD"] = "threshold";
    CreateRoomPartiesOptions["FULL"] = "full";
    return CreateRoomPartiesOptions;
}({});

/**
 * Get Bitcoin chain configuration based on address type
 * @param addressType - Bitcoin address type (taproot, native_segwit)
 * @returns Chain configuration with derivation path and signing algorithm
 */ const getBitcoinChainConfig = (addressType)=>{
    const normalizedAddressType = addressType.toLowerCase();
    const config = BITCOIN_ADDRESS_TYPE_CONFIG[normalizedAddressType];
    if (!config) {
        throw new Error(`Unsupported Bitcoin address type: ${addressType}. Must be one of: taproot, native_segwit`);
    }
    return config;
};
/**
 * Get MPC chain configuration
 * @param chainName - Chain name (e.g., 'BTC', 'EVM', 'SVM')
 * @param bitcoinConfig - Optional bitcoin config (for BTC)
 * @returns Chain configuration with derivation path and signing algorithm
 */ const getMPCChainConfig = (chainName, bitcoinConfig)=>{
    // Special handling for BTC - addressType is required
    if (chainName === 'BTC') {
        const { addressType } = bitcoinConfig || {};
        if (!addressType) {
            throw new Error('addressType is required for BTC. Please provide addressType (taproot or native_segwit).');
        }
        return getBitcoinChainConfig(addressType);
    }
    const chainConfig = MPC_CHAIN_CONFIG[chainName];
    if (!chainConfig) {
        throw new Error(`Chain ${chainName} not supported`);
    }
    return chainConfig;
};
const getTSSConfig = (thresholdSignatureScheme)=>{
    const { threshold, numberOfParties } = MPC_CONFIG[thresholdSignatureScheme];
    return {
        threshold,
        numberOfParties
    };
};
const getClientThreshold = (thresholdSignatureScheme)=>{
    return MPC_CONFIG[thresholdSignatureScheme].clientThreshold;
};
const getDynamicServerThreshold = (thresholdSignatureScheme)=>{
    return MPC_CONFIG[thresholdSignatureScheme].dynamicServerThreshold;
};
/**
 * Helper function to get the reshare config for client and server shares
 * @param {ThresholdSignatureScheme} oldThresholdSignatureScheme - The current threshold signature scheme
 * @param {ThresholdSignatureScheme} newThresholdSignatureScheme - The target threshold signature scheme
 * @returns {{
 *   existingClientShareCount: number,
 *   newClientShareCount: number,
 *   existingServerShareCount: number,
 *   newServerShareCount: number
 * }} The number of existing and new client and server shares needed
 */ const getReshareConfig = ({ oldThresholdSignatureScheme, newThresholdSignatureScheme })=>{
    switch(true){
        // 2-of-2 -> 2-of-2: same-parties refresh — server + rootUser-client both
        // call `reshareRemainingParty`. Share-set delegation lands here too; the
        // delegated share is delivered out-of-band, not via the MPC ceremony.
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO || oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO:
            return {
                existingClientShareCount: 1,
                newClientShareCount: 0,
                existingServerShareCount: 1,
                newServerShareCount: 0
            };
        // 2-of-3 -> 2-of-3 and 2-of-2 -> 2-of-3:
        // -- dynamic server shares: 1 existing, 0 new
        // -- client shares: 1 existing, 1 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE || oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE:
            return {
                existingClientShareCount: 1,
                newClientShareCount: 1,
                existingServerShareCount: 1,
                newServerShareCount: 0
            };
        // 3-of-5 -> 3-of-5:
        // -- dynamic server shares: 2 existing, 0 new
        // -- client shares: 1 existing, 2 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE && newThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE:
            return {
                existingClientShareCount: 1,
                newClientShareCount: 2,
                existingServerShareCount: 2,
                newServerShareCount: 0
            };
        // 2-of-2 -> 3-of-5 and 2-of-3 -> 3-of-5:
        // -- dynamic server shares: 1 existing, 1 new
        // -- client shares: 1 existing, 2 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO && newThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE || oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE && newThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE:
            return {
                existingClientShareCount: 1,
                newClientShareCount: 2,
                existingServerShareCount: 1,
                newServerShareCount: 1
            };
        // 3-of-5 -> 2-of-3:
        // -- dynamic server shares: 1 existing, 0 new
        // -- client shares: 2 existing, 0 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE:
            return {
                existingClientShareCount: 2,
                newClientShareCount: 0,
                existingServerShareCount: 1,
                newServerShareCount: 0
            };
        default:
            throw new Error(`Unsupported reshare from ${oldThresholdSignatureScheme} to ${newThresholdSignatureScheme}`);
    }
};
/**
 * Helper function to get the reshare config for client and server shares
 * @param {ThresholdSignatureScheme} oldThresholdSignatureScheme - The current threshold signature scheme
 * @param {ThresholdSignatureScheme} newThresholdSignatureScheme - The target threshold signature scheme
 * @returns {{
 *   existingServerShareCount: number,
 *   newServerhareCount: number,
 *   existingDynamicServerShareCount: number,
 *   newDynamicServerShareCount: number
 * }} The number of existing and new client and server shares needed
 */ const getServerWalletReshareConfig = ({ oldThresholdSignatureScheme, newThresholdSignatureScheme })=>{
    switch(true){
        // 2-of-2 -> 2-of-2 and 2-of-3 -> 2-of-2:
        // -- dynamic server shares: 1 existing, 0 new
        // -- external server shares: 1 existing, 0 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO || oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO:
            return {
                existingExternalServerShareCount: 1,
                newExternalServerShareCount: 0,
                existingDynamicServerShareCount: 1,
                newDynamicServerShareCount: 0
            };
        // 2-of-3 -> 2-of-3 and 2-of-2 -> 2-of-3:
        // -- dynamic server shares: 1 existing, 0 new
        // -- external server shares: 1 existing, 1 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE || oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE:
            return {
                existingExternalServerShareCount: 1,
                newExternalServerShareCount: 1,
                existingDynamicServerShareCount: 1,
                newDynamicServerShareCount: 0
            };
        // 3-of-5 -> 3-of-5:
        // -- dynamic server shares: 2 existing, 0 new
        // -- external server shares: 1 existing, 2 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE && newThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE:
            return {
                existingExternalServerShareCount: 1,
                newExternalServerShareCount: 2,
                existingDynamicServerShareCount: 2,
                newDynamicServerShareCount: 0
            };
        // 2-of-2 -> 3-of-5 and 2-of-3 -> 3-of-5:
        // -- dynamic server shares: 1 existing, 1 new
        // -- external server shares: 1 existing, 2 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_TWO && newThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE || oldThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE && newThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE:
            return {
                existingExternalServerShareCount: 1,
                newExternalServerShareCount: 2,
                existingDynamicServerShareCount: 1,
                newDynamicServerShareCount: 1
            };
        // 3-of-5 -> 2-of-3:
        // -- dyanmic server shares: 1 existing, 0 new
        // -- external server shares: 2 existing, 0 new
        case oldThresholdSignatureScheme === ThresholdSignatureScheme.THREE_OF_FIVE && newThresholdSignatureScheme === ThresholdSignatureScheme.TWO_OF_THREE:
            return {
                existingExternalServerShareCount: 2,
                newExternalServerShareCount: 0,
                existingDynamicServerShareCount: 1,
                newDynamicServerShareCount: 0
            };
        default:
            throw new Error(`Unsupported reshare from ${oldThresholdSignatureScheme} to ${newThresholdSignatureScheme}`);
    }
};
const URL_PATTERNS = {
    [ENVIRONMENT_ENUM.development]: /^http:\/\/localhost:\d+$/,
    [ENVIRONMENT_ENUM.preprod]: /-preprod/,
    [ENVIRONMENT_ENUM.production]: /^(?!.*dynamic-preprod)(?!http:\/\/localhost:\d+).*/
};
function getEnvironmentFromUrl(url) {
    if (!url) {
        return ENVIRONMENT_ENUM.production;
    }
    if (URL_PATTERNS[ENVIRONMENT_ENUM.development].test(url)) {
        return ENVIRONMENT_ENUM.development;
    }
    if (URL_PATTERNS[ENVIRONMENT_ENUM.preprod].test(url)) {
        return ENVIRONMENT_ENUM.preprod;
    }
    return ENVIRONMENT_ENUM.production;
}

// secp256k1 group order n; ECDSA and BIP340 private keys must be in [1, n).
const SECP256K1_ORDER = BigInt('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141');
const PRIVATE_KEY_HEX_LENGTH = 64;
// A malformed key fails every ceremony attempt identically, so flag it
// non-retryable for callers wrapped in retryPromise (browser client).
const invalidPrivateKeyError = (message)=>{
    const error = new Error(message);
    error.isRetryable = false;
    return error;
};
/**
 * Validates a private key for `importPrivateKey` before any API call or MPC
 * ceremony starts, and returns it normalized for the MPC importer (surrounding
 * whitespace trimmed, optional `0x` prefix stripped).
 *
 * Every chain expects a 32-byte hex key at this layer — chain-specific input
 * formats (WIF, base58, bech32, Stellar seed) are converted to hex by the chain
 * clients beforehand. For secp256k1 chains (ECDSA, BIP340) the key is also
 * range-checked against the curve order.
 *
 * Error messages report only the key's length and character class — never the
 * key material itself.
 */ const normalizeAndValidatePrivateKey = ({ privateKey, chainName, bitcoinConfig })=>{
    const chainLabel = chainName ? ` for chain ${chainName}` : '';
    if (typeof privateKey !== 'string') {
        throw invalidPrivateKeyError(`Invalid private key${chainLabel}: expected a hex string, got ${typeof privateKey}`);
    }
    let normalized = privateKey.trim();
    if (normalized.startsWith('0x') || normalized.startsWith('0X')) {
        normalized = normalized.slice(2);
    }
    if (normalized.length !== PRIVATE_KEY_HEX_LENGTH) {
        throw invalidPrivateKeyError(`Invalid private key${chainLabel}: expected ${PRIVATE_KEY_HEX_LENGTH} hex characters ` + `(32 bytes), got ${normalized.length}`);
    }
    if (!/^[0-9a-fA-F]+$/.test(normalized)) {
        throw invalidPrivateKeyError(`Invalid private key${chainLabel}: expected ${PRIVATE_KEY_HEX_LENGTH} hex characters ` + `(32 bytes), got non-hex characters`);
    }
    const { signingAlgorithm } = getMPCChainConfig(chainName, bitcoinConfig);
    const isSecp256k1Chain = signingAlgorithm === SigningAlgorithm.ECDSA || signingAlgorithm === SigningAlgorithm.BIP340;
    if (isSecp256k1Chain) {
        const keyValue = BigInt(`0x${normalized}`);
        if (keyValue === 0n) {
            throw invalidPrivateKeyError(`Invalid private key${chainLabel}: key cannot be zero`);
        }
        if (keyValue >= SECP256K1_ORDER) {
            throw invalidPrivateKeyError(`Invalid private key${chainLabel}: key exceeds the secp256k1 curve order`);
        }
    }
    return normalized;
};

function _extends() {
    _extends = Object.assign || function assign(target) {
        for(var i = 1; i < arguments.length; i++){
            var source = arguments[i];
            for(var key in source)if (Object.prototype.hasOwnProperty.call(source, key)) target[key] = source[key];
        }
        return target;
    };
    return _extends.apply(this, arguments);
}

var BusinessAccountMemberRole = /*#__PURE__*/ function(BusinessAccountMemberRole) {
    BusinessAccountMemberRole["Owner"] = "owner";
    BusinessAccountMemberRole["Admin"] = "admin";
    BusinessAccountMemberRole["Viewer"] = "viewer";
    return BusinessAccountMemberRole;
}({});
var BusinessAccountSignerType = /*#__PURE__*/ function(BusinessAccountSignerType) {
    BusinessAccountSignerType["EndUser"] = "endUser";
    BusinessAccountSignerType["Server"] = "server";
    return BusinessAccountSignerType;
}({});
const isBusinessAccountActionRequired = (value)=>typeof value === 'object' && value !== null && (value.reason === 'INTENT_REQUIRED' || value.reason === 'APPROVALS_REQUIRED');
/** Strips a `BusinessAccountSignedIntent` (and its nested `intent`) down to known fields before it's spread into a request body. */ const sanitizeBusinessAccountSignedIntent = (signedIntent)=>signedIntent && {
        autoExecute: signedIntent.autoExecute,
        intent: signedIntent.intent && {
            actionType: signedIntent.intent.actionType,
            autoExecute: signedIntent.intent.autoExecute,
            businessAccountId: signedIntent.intent.businessAccountId,
            createdAt: signedIntent.intent.createdAt,
            initiatorUserId: signedIntent.intent.initiatorUserId,
            intentId: signedIntent.intent.intentId,
            payload: signedIntent.intent.payload
        },
        intentSignature: signedIntent.intentSignature
    };

var AuthMode = /*#__PURE__*/ function(AuthMode) {
    AuthMode["HEADER"] = "header";
    AuthMode["COOKIE"] = "cookie";
    return AuthMode;
}({});
var BitcoinAddressType = /*#__PURE__*/ function(BitcoinAddressType) {
    BitcoinAddressType["TAPROOT"] = "taproot";
    BitcoinAddressType["NATIVE_SEGWIT"] = "native_segwit";
    return BitcoinAddressType;
}({});
var WalletReadyState = /*#__PURE__*/ function(WalletReadyState) {
    WalletReadyState["READY"] = "ready";
    WalletReadyState["ENCRYPTED"] = "encrypted";
    return WalletReadyState;
}({});
var BitcoinNetwork = /*#__PURE__*/ function(BitcoinNetwork) {
    BitcoinNetwork["MAINNET"] = "mainnet";
    BitcoinNetwork["TESTNET"] = "testnet";
    return BitcoinNetwork;
}({});
var SuccessEventType = /*#__PURE__*/ function(SuccessEventType) {
    SuccessEventType["KeygenComplete"] = "keygen_complete";
    SuccessEventType["RoomCreated"] = "room_created";
    SuccessEventType["CeremonyComplete"] = "ceremony_complete";
    SuccessEventType["ConsentRequired"] = "consent_required";
    return SuccessEventType;
}({});
class NoopLogger {
    debug() {
    // Intentionally empty
    }
    info() {
    // Intentionally empty
    }
    warn() {
    // Intentionally empty
    }
    error() {
    // Intentionally empty
    }
}

var _Logger;
/**
 * Global static logger for SDK-internal use.
 *
 * Call `Logger.configure(impl)` once at startup to wire in your logger.
 * Call `Logger.setContext(ctx)` to attach metadata merged into every log call.
 *
 * Parses variadic args: any Error instance is extracted and passed as the
 * third argument; all plain objects are merged into a single context object.
 * This matches Datadog's (message, context?, error?) calling convention.
 */ const Logger = (_Logger = class Logger {
    static configure(logger) {
        this._instance = logger;
    }
    static setContext(context) {
        this._context = _extends({}, this._context, context);
    }
    static resetContext() {
        this._context = {};
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    static debug(message, ...args) {
        const { context } = this._parse(args);
        if (context) {
            this._instance.debug(message, context);
        } else {
            this._instance.debug(message);
        }
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    static info(message, ...args) {
        const { context } = this._parse(args);
        if (context) {
            this._instance.info(message, context);
        } else {
            this._instance.info(message);
        }
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    static warn(message, ...args) {
        const { context } = this._parse(args);
        if (context) {
            this._instance.warn(message, context);
        } else {
            this._instance.warn(message);
        }
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    static error(message, ...args) {
        const { error, context } = this._parse(args);
        if (error) {
            this._instance.error(message, context != null ? context : {}, error);
        } else if (context) {
            this._instance.error(message, context);
        } else {
            this._instance.error(message);
        }
    }
    /**
   * Separates variadic args into a merged context object and an optional Error.
   * All plain objects are merged (later args win). Error instances are extracted.
   * Handles unknown/primitive args by wrapping them in a context object.
   */ // eslint-disable-next-line @typescript-eslint/no-explicit-any
    static _parse(args) {
        let error;
        let merged = _extends({}, this._context);
        let hasData = Object.keys(this._context).length > 0;
        for (const arg of args){
            if (arg instanceof Error) {
                error = arg;
            } else if (arg !== null && typeof arg === 'object') {
                merged = _extends({}, merged, arg);
                hasData = true;
            } else if (arg !== undefined && arg !== null) {
                merged = _extends({}, merged, {
                    value: arg
                });
                hasData = true;
            }
        }
        return {
            context: hasData ? merged : undefined,
            error
        };
    }
}, _Logger._instance = new NoopLogger(), _Logger._context = {}, _Logger);

/**
 * Thrown when a signMessage/signTransaction SSE stream ends with `consent_required` instead of
 * completing — the wallet belongs to a business account with an unmet signing-quorum requirement.
 * Mirrors `BusinessAccountActionRequired`: `reason` tells the caller whether to sign `intent`
 * (`INTENT_REQUIRED`) or wait for approvals on `proposalId` (`APPROVALS_REQUIRED`).
 */ class SigningConsentRequiredError extends Error {
    constructor(actionRequired){
        super(`Signing requires consent: ${actionRequired.reason}`);
        this.name = 'SigningConsentRequiredError';
        this.reason = actionRequired.reason;
        this.intent = actionRequired.intent;
        this.proposalId = actionRequired.proposalId;
        this.approvalRequirements = actionRequired.approvalRequirements;
    }
}

const invokeCeremonyComplete = ({ completion, onCeremonyComplete })=>{
    const { accountAddress, walletId, shareSetId, shareSetType, targetUserId, clientKeyshareBackupGrant, encryptedWalletApiKey } = completion;
    const callbackArgs = [
        accountAddress,
        walletId,
        shareSetId,
        shareSetType,
        targetUserId,
        clientKeyshareBackupGrant
    ];
    if (encryptedWalletApiKey) {
        onCeremonyComplete == null ? void 0 : onCeremonyComplete(...callbackArgs, {
            encryptedWalletApiKey
        });
    } else {
        onCeremonyComplete == null ? void 0 : onCeremonyComplete(...callbackArgs);
    }
};
const getElapsedTime = (startTime)=>{
    return startTime ? (Date.now() - startTime).toString() : undefined;
};
/**
 * Reports a request that failed before any response (e.g. a dropped
 * connection) to `onError` and returns the error to reject with. Axios errors
 * carry request config (incl. auth headers) on the error itself, so onError
 * only gets a fresh error with the message, never the raw error object.
 */ const reportRequestFailure = (err, onError)=>{
    const error = err instanceof Error ? err : new Error(String(err));
    try {
        onError == null ? void 0 : onError(new Error(error.message));
    } catch (observerError) {
        Logger.warn('Event stream error observer threw', {
            observerErrorType: observerError instanceof Error ? observerError.name : typeof observerError
        });
    }
    return error;
};
/**
 * A promise that can be rejected from outside. Paired with the SSE stream's
 * onError callback it lets a caller race a ceremony (relay join, MPC
 * operation) against server-side failures that arrive AFTER the success event
 * (e.g. room_created) already resolved the handshake — a policy denial
 * otherwise only surfaces as the ceremony's own timeout.
 * The internal catch swallows a rejection that never wins a race so it can't
 * surface as an unhandled rejection.
 */ const createRejectablePromise = ()=>{
    let reject;
    const promise = new Promise((_, rej)=>{
        reject = rej;
    });
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    promise.catch(()=>{});
    return {
        promise,
        reject
    };
};
/**
 * Redcoast's 422 intent_required envelope (`{ code, payload: { intent } }`),
 * normalized to the same `{ reason, intent }` shape a 202 consent-pending
 * body already carries. `undefined` for any other 422 body.
 */ const asIntentRequiredFrom422Body = (parsed)=>{
    var _body_payload;
    if (typeof parsed !== 'object' || parsed === null) return undefined;
    const body = parsed;
    return body.code === 'intent_required' && ((_body_payload = body.payload) == null ? void 0 : _body_payload.intent) ? {
        intent: body.payload.intent,
        reason: 'INTENT_REQUIRED'
    } : undefined;
};
/** Drains a fetch-adapter stream body into its full text. */ const readStreamToText = async (reader)=>{
    const decoder = new TextDecoder();
    let text = '';
    const pump = async ()=>{
        const chunk = await reader.read();
        if (chunk.value) {
            text += decoder.decode(chunk.value, {
                stream: true
            });
        }
        if (chunk.done) {
            return text + decoder.decode();
        }
        return pump();
    };
    return pump();
};
/**
 * Creates a promise that resolves when a specific event is received from an event stream.
 * Adds a timeout to prevent hanging and races the two promises.
 *
 * @template T The expected type of the response data
 * @param apiClient The axios instance to use for API calls
 * @param options The configuration options
 * @returns A promise that resolves with the event data or rejects on timeout
 */ const createEventStreamPromise = ({ apiClient, dynamicRequestId, endpoint, body, successEventType, timeoutMs = 30000, timeoutMessage, onError, onCeremonyComplete, onSlowDelivery, slowDeliveryWatchdogMs = 4000, mfaToken, elevatedAccessToken, forwardMPCClientEnabled, traceContext })=>{
    // At runtime this can also resolve with a BusinessAccountActionRequired body
    // (see the 202 handling below) — callers that can reach a governed 202 must
    // declare their own wider `Promise<T | BusinessAccountActionRequired>` return type.
    const headers = _extends({
        Accept: 'text/event-stream',
        'Cache-Control': 'no-cache',
        Connection: 'keep-alive'
    }, body !== undefined && {
        'Content-Type': 'application/json'
    }, {
        [DynamicRequestIdHeader]: dynamicRequestId,
        [DynamicMfaTokenHeader]: mfaToken,
        [DynamicElevatedAccessTokenHeader]: elevatedAccessToken,
        [DynamicForwardMPCHeader]: forwardMPCClientEnabled,
        [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
        [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
    });
    // Watchdog: warn (via onSlowDelivery) when the success event is late. The
    // delivery lag this surfaces is otherwise invisible — buffering proxies hold
    // the stream's bytes until the connection closes (see the create-wallet
    // "user created without a wallet" App Review failures).
    const requestStartedAt = Date.now();
    let headersReceived = false;
    let eventsSeen = 0;
    let successOrErrorSeen = false;
    let watchdogId;
    if (onSlowDelivery) {
        watchdogId = setTimeout(()=>{
            if (!successOrErrorSeen) {
                onSlowDelivery({
                    elapsedMs: Date.now() - requestStartedAt,
                    endpoint,
                    eventsSeen,
                    headersReceived,
                    watchdogMs: slowDeliveryWatchdogMs
                });
            }
        }, slowDeliveryWatchdogMs);
    }
    // Create a promise that will resolve when the success event is received
    const eventPromise = new Promise((resolve, reject)=>{
        apiClient.post(endpoint, body, {
            responseType: 'stream',
            headers: _extends({}, headers),
            adapter: 'fetch',
            // Axios's default validateStatus treats any non-2xx as an error,
            // rejecting before the intent_required body below is ever read. 422
            // is added to the accepted range so it resolves the same way 202
            // already does (202 is 2xx, so it needed no override).
            validateStatus: (status)=>status >= 200 && status < 300 || status === 422
        }).then((response)=>{
            headersReceived = true;
            return createSuccessErrorEventStreamHandler({
                onError,
                reject,
                resolve,
                successEventType,
                onCeremonyComplete,
                onEvent: (eventType)=>{
                    eventsSeen += 1;
                    if (eventType === successEventType || eventType === 'error') {
                        successOrErrorSeen = true;
                        clearTimeout(watchdogId);
                    }
                }
            })(response);
        })// Without onError, a caller that races the ceremony against it (the cached-room
        // sign path never awaits this promise) waits out its queue timeout instead.
        .catch((err)=>reject(reportRequestFailure(err, onError)));
    });
    // Add a timeout to prevent hanging
    let timeoutId;
    const timeoutPromise = new Promise((_, reject)=>{
        timeoutId = setTimeout(()=>reject(new Error(timeoutMessage)), timeoutMs);
    });
    // Return the event data as soon as it's available, clearing the timers either way
    return Promise.race([
        eventPromise,
        timeoutPromise
    ]).finally(()=>{
        clearTimeout(timeoutId);
        clearTimeout(watchdogId);
    });
};
/**
 * Creates a handler function for processing server-sent events (SSE) streams.
 * This utility manages asynchronous event-based communication with the server,
 * particularly for long-running operations like wallet creation or key generation.
 *
 * @template T - The expected type of the successful response data
 * @param {function} resolve - Promise resolution function to call when the success event is received
 * @param {function} reject - Promise rejection function to call when an error occurs
 * @param {string} successEventType - The event type string that indicates a successful operation
 * @param {function} [onError] - Optional callback for error handling, allowing custom error processing
 * @returns {function} A response handler function that processes the event stream
 */ const createSuccessErrorEventStreamHandler = ({ resolve, reject, successEventType, onError, onCeremonyComplete, onEvent })=>{
    return (response)=>{
        const rejectWithStatusError = ()=>{
            const error = new Error(`Request failed with status ${response.status}`);
            reject(error);
            onError == null ? void 0 : onError(error);
        };
        // Reject immediately for non-2xx HTTP responses (e.g. 429 rate limit).
        // With axios fetch adapter + responseType: 'stream', non-2xx responses
        // may not be rejected automatically and arrive here as a stream of
        // non-SSE content that would never parse into success/error events.
        if (response.status && (response.status < 200 || response.status >= 300)) {
            // A governed ceremony with nothing signed yet answers 422
            // intent_required — read its body for the intent to sign instead of
            // reporting a generic failure.
            if (response.status !== 422) {
                rejectWithStatusError();
                return;
            }
            readStreamToText(response.data.getReader()).then((text)=>{
                let parsed;
                try {
                    parsed = JSON.parse(text);
                } catch (parseError) {
                    Logger.warn('Unparsable 422 body — reporting a generic failure', {
                        parseError
                    });
                    rejectWithStatusError();
                    return;
                }
                const intentRequired = asIntentRequiredFrom422Body(parsed);
                if (intentRequired) {
                    resolve(intentRequired);
                } else {
                    rejectWithStatusError();
                }
            }).catch((err)=>{
                const error = err instanceof Error ? err : new Error(String(err));
                reject(error);
                onError == null ? void 0 : onError(error);
            });
            return;
        }
        // A governed business-account mutation answers 202 with a single JSON
        // object instead of opening the ceremony's SSE stream — read it as plain
        // text, not as events. An unrecognized 202 body falls through to the SSE
        // parser below (which finds no events and times out) rather than
        // resolving with something the caller can't act on.
        if (response.status === 202) {
            readStreamToText(response.data.getReader()).then((text)=>{
                let parsed;
                try {
                    parsed = JSON.parse(text);
                } catch (parseError) {
                    Logger.warn('Unparsable 202 body — falling through to the SSE parser, which will time out', {
                        parseError
                    });
                    return;
                }
                if (isBusinessAccountActionRequired(parsed)) {
                    resolve(parsed);
                } else {
                    Logger.warn('202 response is not a recognized action-required body — falling through to the SSE parser, which will time out', {
                        parsed
                    });
                }
            }).catch((err)=>{
                const error = err instanceof Error ? err : new Error(String(err));
                reject(error);
                onError == null ? void 0 : onError(error);
            });
            return;
        }
        const reader = response.data.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let settled = false;
        let ceremonyCompleteSeen = false;
        const processEvents = (events)=>{
            for (const event of events){
                onEvent == null ? void 0 : onEvent(event.type);
                if (event.type === successEventType) {
                    settled = true;
                    resolve(event.data);
                }
                if (event.type === SuccessEventType.CeremonyComplete) {
                    ceremonyCompleteSeen = true;
                    invokeCeremonyComplete({
                        completion: event.data,
                        onCeremonyComplete
                    });
                }
                // Sent instead of the success event when an unmet signing quorum blocks the sign;
                // treated as terminal, since the caller must act on `reason` rather than retry.
                if (event.type === SuccessEventType.ConsentRequired) {
                    settled = true;
                    const error = new SigningConsentRequiredError(event.data);
                    reject(error);
                    onError == null ? void 0 : onError(error);
                    return true;
                }
                if (event.type === 'error') {
                    settled = true;
                    const error = createErrorFromEventData(event.data);
                    reject(error);
                    onError == null ? void 0 : onError(error);
                    return true;
                }
            }
            return false;
        };
        const processStream = async ()=>{
            try {
                const { value, done } = await reader.read();
                if (done) {
                    // Flush any remaining data in the decoder
                    const remaining = decoder.decode();
                    if (remaining) {
                        buffer += remaining;
                    }
                    // Process any remaining complete events in the buffer
                    const { events } = parseEventStream(buffer);
                    processEvents(events);
                    // Stream ended without a success or error event — reject so the
                    // caller does not hang indefinitely.
                    if (!settled) {
                        const error = new Error('SSE stream ended without a success or error event');
                        reject(error);
                        onError == null ? void 0 : onError(error);
                    } else if (onCeremonyComplete && !ceremonyCompleteSeen) {
                        // A ceremony op resolved early on its room-created event, but the
                        // stream closed before ceremony_complete — the server-side ceremony
                        // did not finish (or the event was dropped). Surface via onError so
                        // callers gating backup on completion abort instead of hanging.
                        onError == null ? void 0 : onError(new Error('SSE stream ended before ceremony_complete'));
                    }
                    return;
                }
                buffer += decoder.decode(value, {
                    stream: true
                });
                const { events, remaining } = parseEventStream(buffer);
                buffer = remaining;
                const hadError = processEvents(events);
                // Stop reading if an error event was processed.
                // For success events, continue reading to allow subsequent
                // events (like CeremonyComplete or error) to be processed.
                if (hadError) {
                    return;
                }
                void processStream();
            } catch (err) {
                const error = err instanceof Error ? err : new Error(String(err));
                reject(error);
                // A transport drop after the API promise already resolved (on
                // room_created) would otherwise leave a ceremony backer hanging — surface
                // it so onError-gated callers abort.
                onError == null ? void 0 : onError(error);
            }
        };
        void processStream();
    };
};
/**
 * Creates an error object from event stream error data.
 *
 * @param data - The error data received from the event stream
 * @returns A standardized Error object with properties from the error data
 */ const createErrorFromEventData = (data)=>{
    const error = new Error(typeof data === 'object' && data !== null && 'error' in data ? String(data.error) : 'Unknown error');
    if (typeof data === 'object' && data !== null) {
        Object.assign(error, data);
    }
    return error;
};
/**
 * Sends a plain JSON POST and resolves with the parsed response body.
 * A lightweight alternative to createEventStreamPromise for endpoints that
 * return a single JSON object instead of an SSE stream.
 */ const requestJson = ({ apiClient, dynamicRequestId, endpoint, body, idempotencyKey, timeoutMs = 5000, timeoutMessage, mfaToken, elevatedAccessToken, forwardMPCClientEnabled, onError, traceContext })=>{
    const headers = _extends({}, body !== undefined && {
        'Content-Type': 'application/json'
    }, idempotencyKey && {
        'x-idempotency-key': idempotencyKey
    }, {
        [DynamicRequestIdHeader]: dynamicRequestId,
        [DynamicMfaTokenHeader]: mfaToken,
        [DynamicElevatedAccessTokenHeader]: elevatedAccessToken,
        [DynamicForwardMPCHeader]: forwardMPCClientEnabled,
        [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
        [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
    });
    let timeoutId;
    const timeoutPromise = new Promise((_, reject)=>{
        timeoutId = setTimeout(()=>reject(new Error(timeoutMessage)), timeoutMs);
    });
    const requestPromise = apiClient.post(endpoint, body, {
        headers
    }).then((response)=>response.data).catch((err)=>{
        throw reportRequestFailure(err, onError);
    });
    return Promise.race([
        requestPromise,
        timeoutPromise
    ]).finally(()=>clearTimeout(timeoutId));
};
/**
 * Parses a Server-Sent Events (SSE) stream into structured event objects.
 * Returns both the parsed events and any remaining unparsed data (incomplete events)
 * so the caller can keep the unconsumed portion in its buffer.
 *
 * Events are only considered "consumed" once we see their terminating blank line.
 * This handles the case where an event is split across multiple chunks:
 *   Chunk 1: "event:error\n"
 *   Chunk 2: "data:{...}\n\n"
 * The first chunk returns no events and remaining="event:error\n".
 * The second chunk (after buffer concatenation) returns the full event.
 *
 * @param input - Raw string data from an event stream
 * @returns Object with parsed events array and remaining unparsed string
 */ const parseEventStream = (input)=>{
    const lines = input.split('\n');
    const events = [];
    let currentEvent = {};
    let inEvent = false;
    let lastConsumedIndex = 0;
    let currentLineStart = 0;
    for(let i = 0; i < lines.length; i++){
        const line = lines[i];
        const lineEnd = currentLineStart + line.length + (i < lines.length - 1 ? 1 : 0);
        // Empty line marks the end of an event
        if (line === '') {
            if (currentEvent.type && currentEvent.data) {
                events.push({
                    type: currentEvent.type,
                    data: JSON.parse(currentEvent.data)
                });
                lastConsumedIndex = lineEnd;
                currentEvent = {};
                inEvent = false;
            }
            currentLineStart = lineEnd;
            continue;
        }
        // Process event fields
        if (line.startsWith('event:')) {
            currentEvent.type = line.substring(6).trim();
            inEvent = true;
        } else if (line.startsWith('data:')) {
            currentEvent.data = line.substring(5).trim();
            inEvent = true;
        } else if (inEvent && currentEvent.data) {
            currentEvent.data += line;
        }
        currentLineStart = lineEnd;
    }
    return {
        events,
        remaining: input.substring(lastConsumedIndex)
    };
};

/**
 * Thrown when sign-and-broadcast answers 413: the request body is over the server's 640kb limit,
 * which large calldata can reach.
 */ class SignAndBroadcastRequestTooLargeError extends Error {
    constructor(){
        super('The sign-and-broadcast request is too large. Send less calldata.');
        this.name = 'SignAndBroadcastRequestTooLargeError';
    }
}

class WalletApiError extends Error {
    constructor(status, message, code){
        super(message);
        this.name = 'WalletApiError';
        this.status = status;
        this.code = code;
    }
}
const getResponseRecord = (error)=>{
    var _error_response;
    const data = (_error_response = error.response) == null ? void 0 : _error_response.data;
    return data && typeof data === 'object' ? data : undefined;
};
// The Key Share Service returns its machine-readable cause under `error_code`; other
// backends use `code` or a bare `error`. Exported for callers that must skip handleAxiosError's own logging.
const extractServerErrorCode = (error)=>{
    const record = getResponseRecord(error);
    const candidates = [
        record == null ? void 0 : record['code'],
        record == null ? void 0 : record['error_code'],
        record == null ? void 0 : record['error']
    ];
    return candidates.find((value)=>typeof value === 'string');
};
const INTERNAL_SERVER_ERROR_MESSAGE = 'Internal server error';
/**
 * `status` for a request that never received an HTTP response at all — the
 * client lost connectivity, the request was aborted, DNS/TLS failed, or CORS
 * blocked it. 0 matches the XHR/`fetch` convention for "no response".
 *
 * This used to be reported as `500 Internal server error`, which made a
 * client-side network failure indistinguishable from a backend fault: the
 * "Backend 500s" monitor counted 1,395 events on a day when the API returned
 * only 33 real 5xx responses.
 */ const NETWORK_ERROR_STATUS = 0;
const NETWORK_ERROR_CODE = 'NETWORK_ERROR';
const NETWORK_ERROR_MESSAGE = 'Network error - no response received';
const STATUS_MESSAGES = {
    400: 'Invalid request',
    403: 'Forbidden',
    422: 'Unprocessable content',
    429: 'Rate limited',
    500: INTERNAL_SERVER_ERROR_MESSAGE
};
const MISSING_AUTH_MESSAGE = 'Authorization header or cookie missing';
// A 401 can mean the request carried no credentials, or carried credentials the
// backend rejected — the two need different messages. The Authorization header
// is readable so we can confirm its presence; the auth cookie is httpOnly, so we
// can only report whether cookie mode was enabled (`withCredentials`), not that a
// cookie was actually attached.
const getRequestCredentials = (error)=>{
    var _error_config, _error_config1;
    const requestHeaders = (_error_config = error.config) == null ? void 0 : _error_config.headers;
    var _requestHeaders_Authorization;
    const hasAuthorizationHeader = Boolean((_requestHeaders_Authorization = requestHeaders == null ? void 0 : requestHeaders['Authorization']) != null ? _requestHeaders_Authorization : requestHeaders == null ? void 0 : requestHeaders['authorization']);
    const usesCookieAuth = Boolean((_error_config1 = error.config) == null ? void 0 : _error_config1.withCredentials);
    return {
        hasAuthorizationHeader,
        usesCookieAuth
    };
};
const resolveUnauthorizedMessage = (error)=>{
    const { hasAuthorizationHeader, usesCookieAuth } = getRequestCredentials(error);
    if (!hasAuthorizationHeader && !usesCookieAuth) {
        return MISSING_AUTH_MESSAGE;
    }
    const credentialDescriptions = [];
    if (hasAuthorizationHeader) {
        credentialDescriptions.push('Authorization header present');
    }
    if (usesCookieAuth) {
        credentialDescriptions.push('withCredentials enabled (cookie auth)');
    }
    return `Unauthorized (${credentialDescriptions.join(', ')})`;
};
const resolveStatusMessage = (status, error)=>{
    if (status === 401) {
        return resolveUnauthorizedMessage(error);
    }
    if (status && STATUS_MESSAGES[status]) {
        return STATUS_MESSAGES[status];
    }
    return undefined;
};
const handleAxiosError = (error, message, context, /**
   * Optional severity hint from the caller, for failures the caller knows are
   * expected (e.g. a business-rule rejection). It can only *lower* severity to
   * `warn` — a caller must not be able to escalate, and a genuine 5xx has to
   * stay at `error` regardless of what the call site believes.
   *
   * Without this the hint that `logError` accepts was silently discarded for
   * every AxiosError, which is the most common error type in the SDK.
   */ options)=>{
    var _error_config, _error_config1, _error_response, _error_response1, _error_response2;
    const requestUrl = (_error_config = error.config) == null ? void 0 : _error_config.url;
    const requestBaseUrl = (_error_config1 = error.config) == null ? void 0 : _error_config1.baseURL;
    // The HTTP status MUST NOT be logged as a top-level `status` field: Datadog
    // reserves `status` for the log level and its remapper turns a numeric value
    // into `info`, silently burying every 4xx/5xx we emit here. `http.status_code`
    // is Datadog's standard attribute, so the level survives and these logs join
    // against edge/CDN logs on the same field.
    const logPayload = _extends({
        message,
        error: (_error_response = error.response) == null ? void 0 : _error_response.data,
        http: {
            status_code: (_error_response1 = error.response) == null ? void 0 : _error_response1.status
        }
    }, requestBaseUrl && {
        requestBaseUrl
    }, requestUrl && {
        requestUrl
    }, {
        context
    });
    const status = (_error_response2 = error.response) == null ? void 0 : _error_response2.status;
    // A 429 (Too Many Requests) is a transient rate-limit signal, not a code or
    // logic failure — and a request that never got a response is a client-side
    // connectivity problem, not a server fault. Both are logged at `warn` so they
    // don't pollute error dashboards or trigger PagerDuty. The 429 case covers
    // both Cloudflare WAF blocks and application-level rate limiting.
    const inferredLevel = status === 429 || status === undefined ? 'warn' : 'error';
    // A 5xx is a server fault: no call site is entitled to downgrade it, however
    // expected it believes the failure to be. The hint only applies below 500.
    const isServerFault = status !== undefined && status >= 500;
    const logLevel = (options == null ? void 0 : options.level) === 'warn' && !isServerFault ? 'warn' : inferredLevel;
    Logger[logLevel]('[DynamicWaasWalletClient] Axios error: ', logPayload);
    // No response at all: report it as such rather than laundering it into a 500.
    if (status === undefined) {
        throw new WalletApiError(NETWORK_ERROR_STATUS, NETWORK_ERROR_MESSAGE, NETWORK_ERROR_CODE);
    }
    var _resolveStatusMessage;
    // Preserve the real status. Collapsing every unmapped code to 500 made a 404
    // (backup not found) and a 504 (gateway timeout) both surface as
    // "Internal server error", so neither the caller nor a monitor could tell a
    // missing resource from an outage.
    const resolvedMessage = (_resolveStatusMessage = resolveStatusMessage(status, error)) != null ? _resolveStatusMessage : `Request failed with status ${status}`;
    throw new WalletApiError(status, resolvedMessage, extractServerErrorCode(error));
};

const getRequiredExternalKeyShareId = (ks)=>{
    if (!ks.externalKeyShareId) {
        throw new Error(`Missing externalKeyShareId for key share (id: ${ks.id}, keygenId: ${ks.keygenId})`);
    }
    return ks.externalKeyShareId;
};
/**
 * A `dynamic` key share is retrievable only via its `externalKeyShareId`, so
 * recording one without that reference persists an unrecoverable share that
 * locks the user out at recovery time (where `getRequiredExternalKeyShareId`
 * throws). Throw the same error here so the bad backup location is rejected
 * before it is posted and surfaces in Datadog exactly as the recovery path does.
 */ const assertDynamicLocationsHaveExternalKeyShareId = (locations)=>locations.filter((location)=>location.location === BackupLocation.DYNAMIC).forEach((location)=>getRequiredExternalKeyShareId(location));

var version = "1.1.44";

/**
 * Reads the Authorization header off an axios request config, which stores
 * headers either as a plain object or as an `AxiosHeaders` instance.
 */ const readAuthorizationHeader = (requestHeaders)=>{
    if (typeof requestHeaders !== 'object' || requestHeaders === null) {
        return undefined;
    }
    const headers = requestHeaders;
    var _headers_Authorization;
    const authorization = (_headers_Authorization = headers['Authorization']) != null ? _headers_Authorization : headers['authorization'];
    if (typeof authorization !== 'string') {
        return undefined;
    }
    return authorization;
};
class BaseClient {
    /**
   * Fire {@link onUnauthorized} whenever a request on this axios instance sees a
   * 401, so the iframe can tell the host to log the user out.
   *
   * Both branches are needed: ordinary requests reject on 401 (onRejected),
   * but the SSE sign/keygen path uses the fetch adapter with
   * `responseType: 'stream'`, where a non-2xx response can arrive *resolved*
   * (see createSuccessErrorEventStreamHandler) — so the fulfilled branch must
   * inspect `response.status` too. The interceptor never alters the
   * response/error; it only signals out-of-band, leaving existing error
   * handling unchanged.
   */ installUnauthorizedInterceptor(client) {
        const fireIfUnauthorized = (status, requestHeaders)=>{
            if (status !== 401) {
                return;
            }
            if (this.isSupersededAuthHeader(requestHeaders)) {
                this.logger.info('[BaseClient] ignoring 401 for a request that carried a superseded auth token');
                return;
            }
            try {
                this.onUnauthorized == null ? void 0 : this.onUnauthorized.call(this);
            } catch (error) {
                this.logger.error('[BaseClient] onUnauthorized handler threw', {
                    error
                });
            }
        };
        client.interceptors.response.use((response)=>{
            var _response_config;
            fireIfUnauthorized(response == null ? void 0 : response.status, response == null ? void 0 : (_response_config = response.config) == null ? void 0 : _response_config.headers);
            return response;
        }, (error)=>{
            var _error_response, _error_config;
            var _error_response_status;
            fireIfUnauthorized((_error_response_status = error == null ? void 0 : (_error_response = error.response) == null ? void 0 : _error_response.status) != null ? _error_response_status : error == null ? void 0 : error.status, error == null ? void 0 : (_error_config = error.config) == null ? void 0 : _error_config.headers);
            return Promise.reject(error);
        });
    }
    /**
   * Whether a request was sent with an auth token that {@link syncAuthToken} has
   * since replaced. Its 401 says nothing about the token the client holds now,
   * so it must not reach {@link onUnauthorized} and log the user out.
   */ isSupersededAuthHeader(requestHeaders) {
        if (this.authMode !== AuthMode.HEADER || !this.currentAuthHeader) {
            return false;
        }
        const requestAuthHeader = readAuthorizationHeader(requestHeaders);
        if (!requestAuthHeader) {
            return false;
        }
        return requestAuthHeader !== this.currentAuthHeader;
    }
    get forwardMPCClient() {
        if (!this._forwardMpcClient) {
            throw new Error('Forward MPC client is not initialized');
        }
        return this._forwardMpcClient;
    }
    set forwardMPCClient(forwardMPCClient) {
        this._forwardMpcClient = forwardMPCClient;
    }
    syncAuthToken(authToken) {
        if (this.authMode === AuthMode.COOKIE) {
            return;
        }
        if (!authToken) {
            throw new Error('Auth token is required for header authentication');
        }
        const authHeader = `Bearer ${authToken}`;
        this.currentAuthHeader = authHeader;
        this.apiClient.defaults.headers['Authorization'] = authHeader;
        this.clientRelayApiClient.defaults.headers['Authorization'] = authHeader;
        this.apiClient.defaults.headers.common['Authorization'] = authHeader;
        this.clientRelayApiClient.defaults.headers.common['Authorization'] = authHeader;
        if (this.apiClient.defaults.headers['Authorization'] !== authHeader || this.clientRelayApiClient.defaults.headers['Authorization'] !== authHeader) {
            throw new Error('Failed to sync auth token, auth header is not set to the expected auth token after sync, there is likely a race condition, contact Dynamic devs to investigate');
        }
    }
    syncBackupServiceAuthToken(backupServiceAuthToken) {
        if (this.authMode === AuthMode.HEADER) {
            return;
        }
        if (!backupServiceAuthToken) {
            throw new Error('Backup service auth token is required for cookie authentication');
        }
        this.backupServiceAuthToken = backupServiceAuthToken;
        this.clientRelayApiClient.defaults.headers['Authorization'] = `Bearer ${backupServiceAuthToken}`;
    }
    constructor({ environmentId, baseApiUrl, authToken, backupServiceAuthToken, baseClientKeysharesRelayApiUrl, authMode = AuthMode.HEADER, // Represents the version of the client SDK used by developer
    sdkVersion, forwardMPCClient, logger, onUnauthorized }){
        this.logger = logger != null ? logger : new NoopLogger();
        this.onUnauthorized = onUnauthorized;
        const headers = {};
        // Only set Authorization header if using header auth mode and token is provided
        if (authMode === AuthMode.HEADER && authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
            this.currentAuthHeader = headers['Authorization'];
        }
        headers['x-dyn-wallet-sdk-version'] = version;
        headers['x-dyn-version'] = sdkVersion;
        this.environmentId = environmentId;
        this.authMode = authMode;
        const environment = getEnvironmentFromUrl(baseApiUrl);
        this.baseApiUrl = baseApiUrl != null ? baseApiUrl : DYNAMIC_AUTH_BASE_API_URL_MAP[environment];
        // Configure axios to include credentials for cookie auth
        const axiosConfig = _extends({
            baseURL: this.baseApiUrl,
            headers
        }, authMode === AuthMode.COOKIE ? {
            withCredentials: true
        } : {});
        this.apiClient = axios.create(axiosConfig);
        this.clientKeysharesRelayBaseApiUrl = baseClientKeysharesRelayApiUrl != null ? baseClientKeysharesRelayApiUrl : DYNAMIC_KEYSHARES_RELAY_MAP[environment];
        // Cookie based auth will not have an authToken
        // so we need to pass the backupServiceAuthToken to the clientRelayApiClient
        // This was requested from the backend during initWaasWalletClient
        if (authMode === AuthMode.COOKIE && backupServiceAuthToken && !authToken) {
            headers['Authorization'] = `Bearer ${backupServiceAuthToken}`;
        }
        this.clientRelayApiClient = axios.create({
            baseURL: this.clientKeysharesRelayBaseApiUrl,
            headers: _extends({}, headers, {
                [RELAY_API_KEY_HEADER]: DYNAMIC_CLIENT_RELAY_REDCOAST_API_KEY_MAP[environment],
                [RELAY_APP_ID_HEADER]: DYNAMIC_CLIENT_RELAY_REDCOAST_APP_ID_MAP[environment]
            })
        });
        this.installUnauthorizedInterceptor(this.apiClient);
        this.installUnauthorizedInterceptor(this.clientRelayApiClient);
        this.forwardMPCClient = forwardMPCClient;
    }
}

const createWalletAccountRequestBody = ({ chainName, clientKeygenIds, thresholdSignatureScheme, skipLock, bitcoinConfig, businessAccountId })=>{
    const { addressType } = bitcoinConfig || {};
    return _extends({
        chain: chainName,
        clientKeygenIds,
        thresholdSignatureScheme
    }, skipLock ? {
        skipLock
    } : {}, addressType ? {
        addressType
    } : {}, businessAccountId ? {
        businessAccountId
    } : {});
};
const MAX_SERVER_MESSAGE_LENGTH = 200;
/**
 * A rejected sign-and-broadcast as a `WalletApiError` that names the server's reason and code, since the generic status text says nothing about which check failed. A failure with no response (timeout, no connection) passes through.
 *
 * @param error - What the request threw.
 */ const toSignAndBroadcastApiError = (error)=>{
    if (!isAxiosError(error) || !error.response) {
        return error;
    }
    const { status, data } = error.response;
    const code = extractServerErrorCode(error);
    const record = data && typeof data === 'object' ? data : undefined;
    const serverMessage = [
        record == null ? void 0 : record['error'],
        record == null ? void 0 : record['message']
    ].find((candidate)=>typeof candidate === 'string' && candidate.length > 0 && candidate !== code);
    const detail = [
        serverMessage == null ? void 0 : serverMessage.slice(0, MAX_SERVER_MESSAGE_LENGTH),
        code && `code: ${code}`
    ].filter(Boolean).join(', ');
    const suffix = detail ? ` (${detail})` : '';
    return new WalletApiError(status, `Sign and broadcast failed with status ${status}${suffix}`, code);
};
class DynamicApiClient extends BaseClient {
    async getBackupRelayToken({ traceContext }) {
        const { data } = await this.apiClient.get(`${this.waasRoutePrefix}/keyShares/backup/token`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data.token;
    }
    async authenticateApiToken({ environmentId, signingPublicKey }) {
        return this.apiClient.post(`/api/v0/environments/${environmentId}/waas/authenticate`, undefined, {
            headers: _extends({
                [DynamicRequestIdHeader]: v4().replace('-', '')
            }, signingPublicKey ? {
                [DynamicSessionPublicKeyHeader]: signingPublicKey
            } : {})
        });
    }
    async createWalletAccount({ chainName, clientKeygenIds, dynamicRequestId, thresholdSignatureScheme, skipLock, bitcoinConfig, businessAccountId, onError, onCeremonyComplete, onSlowDelivery, traceContext }) {
        const requestBody = createWalletAccountRequestBody({
            chainName,
            clientKeygenIds,
            thresholdSignatureScheme,
            skipLock,
            bitcoinConfig,
            businessAccountId});
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `${this.waasRoutePrefix}/create`,
            body: requestBody,
            successEventType: SuccessEventType.KeygenComplete,
            timeoutMessage: 'Wallet creation timed out',
            onError,
            onCeremonyComplete,
            onSlowDelivery,
            traceContext
        });
    }
    /**
   * Plain-JSON (non-SSE) request to the `/create` endpoint. Does NOT synchronously
   * create the wallet: it initiates the server keygen ceremony (mints the MPC room,
   * enqueues the async worker that builds the wallet) and returns `{ roomId,
   * serverKeygenIds }`. With `poll: true` it instead reads the in-flight ceremony,
   * returning the wallet identity (`walletId`/`accountAddress`/`shareSetId`) once the
   * worker has finished. The wallet is the product of the full ceremony, not this call.
   */ async requestWalletCreationJson({ chainName, clientKeygenIds, dynamicRequestId, thresholdSignatureScheme, skipLock, bitcoinConfig, businessAccountId, idempotencyKey, timeoutMs, traceContext, poll }) {
        const requestBody = _extends({}, createWalletAccountRequestBody({
            chainName,
            clientKeygenIds,
            thresholdSignatureScheme,
            skipLock,
            bitcoinConfig,
            businessAccountId}), poll ? {
            poll: true
        } : {});
        return requestJson({
            apiClient: this.apiClient,
            dynamicRequestId,
            idempotencyKey,
            endpoint: `${this.waasRoutePrefix}/create`,
            body: requestBody,
            timeoutMs,
            timeoutMessage: 'Wallet creation timed out',
            traceContext
        });
    }
    async signMessage({ dynamicRequestId, walletId, shareSetId, message, onError, isFormatted, mfaToken, elevatedAccessToken, roomId, context, approvalQuorum, forwardMPCClientEnabled, traceContext, bitcoinConfig }) {
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `${this.waasRoutePrefix}/${walletId}/signMessage`,
            body: _extends({
                message,
                isFormatted,
                context,
                roomId
            }, approvalQuorum ? {
                approvalQuorum
            } : {}, bitcoinConfig ? {
                bitcoinConfig
            } : {}, shareSetId ? {
                shareSetId
            } : {}),
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Message signing timed out',
            onError,
            mfaToken,
            elevatedAccessToken,
            forwardMPCClientEnabled,
            traceContext
        });
    }
    /**
   * Plain-JSON (non-SSE) variant of `signMessage`. Hits the same
   * `/signMessage` endpoint; the `x-idempotency-key` header tells the backend
   * (when `enable-http-waas-transport-signmessage` is on) to respond with the
   * OpenRoomResponse synchronously instead of streaming `room_created` over SSE.
   * Unlike wallet creation, no completion polling is needed — the response is final.
   */ async requestSignMessageJson({ dynamicRequestId, walletId, shareSetId, message, onError, isFormatted, mfaToken, elevatedAccessToken, roomId, context, approvalQuorum, idempotencyKey, forwardMPCClientEnabled, traceContext, bitcoinConfig }) {
        return requestJson({
            apiClient: this.apiClient,
            dynamicRequestId,
            idempotencyKey,
            endpoint: `${this.waasRoutePrefix}/${walletId}/signMessage`,
            body: _extends({
                message,
                isFormatted,
                context,
                roomId
            }, approvalQuorum ? {
                approvalQuorum
            } : {}, bitcoinConfig ? {
                bitcoinConfig
            } : {}, shareSetId ? {
                shareSetId
            } : {}),
            timeoutMs: 20000,
            timeoutMessage: 'Message signing timed out',
            onError,
            mfaToken,
            elevatedAccessToken,
            forwardMPCClientEnabled,
            traceContext
        });
    }
    /**
   * Starts a sign-and-broadcast: Dynamic opens a signing room, you sign in it, and Dynamic then sends the transaction. The signature never comes back.
   *
   * @param params.walletId - The wallet that signs.
   * @param params.shareSetId - Which of the wallet's key sets to use. Defaults to its active one.
   * @param params.message - The transaction as the bytes to sign (RLP hex on EVM, message bytes on Solana). Not hashed.
   * @param params.context - What the message does in readable form (chain, recipient, amount). Dynamic checks it against the wallet and its policies.
   * @param params.broadcastOptions - Solana send settings: other required signers' signatures, and skipping the pre-send dry run.
   * @param params.isFormatted - `true` if the message is already a hash. `false` for a serialized transaction.
   * @param params.requestedCertainty - How sure to be before calling it confirmed: `fast`, `safe` or `final`, or `chain:` plus a chain-specific value. Defaults to `safe`.
   * @param params.externalReference - Your own label, returned on every event. Not unique.
   * @param params.roomId - A signing room you already opened; Dynamic opens one when omitted.
   * @param params.approvalQuorum - Approvers' consent for a governed wallet, sent on the retry after `intent_required`.
   * @param params.idempotencyKey - Makes a retry safe: the same key replays the stored answer instead of sending twice.
   * @param params.dynamicRequestId - Id of this one request, to match client and server logs.
   * @param params.traceContext - Ties this call's logs to the server's, across retries. Created when omitted.
   * @param params.mfaToken - Proof of the user's multi-factor check, when the wallet needs one.
   * @param params.elevatedAccessToken - Proof of a recent re-login, when the wallet needs one.
   * @param params.onError - Called with the failure's message, never the raw error.
   * @returns The transaction record: its id, its status, and the signing room while signing is pending.
   * @throws SignAndBroadcastRequestTooLargeError when the body is over the server limit.
   * @throws SigningConsentRequiredError when a governed wallet needs approvers' consent first.
   * @throws WalletApiError when the server rejects it, with its reason and code.
   */ async signAndBroadcast({ dynamicRequestId, walletId, shareSetId, context, broadcastOptions, message, isFormatted, requestedCertainty, externalReference, roomId, approvalQuorum, idempotencyKey, onError, mfaToken, elevatedAccessToken, traceContext }) {
        try {
            return await requestJson({
                apiClient: this.apiClient,
                dynamicRequestId,
                idempotencyKey,
                endpoint: `${this.waasRoutePrefix}/${walletId}/signAndBroadcast`,
                body: _extends({
                    message,
                    context
                }, broadcastOptions ? {
                    broadcastOptions
                } : {}, {
                    isFormatted
                }, requestedCertainty ? {
                    requestedCertainty
                } : {}, externalReference ? {
                    externalReference
                } : {}, roomId ? {
                    roomId
                } : {}, approvalQuorum ? {
                    approvalQuorum
                } : {}, shareSetId ? {
                    shareSetId
                } : {}),
                timeoutMs: 20000,
                timeoutMessage: 'Sign and broadcast timed out',
                onError,
                mfaToken,
                elevatedAccessToken,
                traceContext
            });
        } catch (error) {
            const response = error.response;
            if ((response == null ? void 0 : response.status) === 413) {
                throw new SignAndBroadcastRequestTooLargeError();
            }
            // A governed wallet with nothing signed yet answers 422 intent_required, as plain signing's stream does.
            const intentRequired = (response == null ? void 0 : response.status) === 422 ? asIntentRequiredFrom422Body(response.data) : undefined;
            if (intentRequired) {
                throw new SigningConsentRequiredError(intentRequired);
            }
            throw toSignAndBroadcastApiError(error);
        }
    }
    async refreshWalletAccountShares({ dynamicRequestId, walletId, shareSetId, onError, onCeremonyComplete, mfaToken, elevatedAccessToken, traceContext }) {
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `${this.waasRoutePrefix}/${walletId}/refresh`,
            body: shareSetId ? {
                shareSetId
            } : undefined,
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Refresh timed out',
            onError,
            onCeremonyComplete,
            mfaToken,
            elevatedAccessToken,
            traceContext
        });
    }
    async reshare({ walletId, shareSetId, dynamicRequestId, clientKeygenIds, oldThresholdSignatureScheme, newThresholdSignatureScheme, delegateToProjectEnvironment, revokeDelegation, mfaToken, elevatedAccessToken, onError, onCeremonyComplete, traceContext, initialSignerRules, reshareKind }) {
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `${this.waasRoutePrefix}/${walletId}/reshare`,
            body: _extends({
                clientKeygenIds,
                delegateToProjectEnvironment,
                newThresholdSignatureScheme,
                oldThresholdSignatureScheme,
                revokeDelegation
            }, shareSetId ? {
                shareSetId
            } : {}, initialSignerRules ? {
                initialSignerRules
            } : {}, reshareKind ? {
                reshareKind
            } : {}),
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Reshare timed out',
            onError,
            onCeremonyComplete,
            mfaToken,
            elevatedAccessToken,
            traceContext
        });
    }
    async exportKey({ mfaToken, elevatedAccessToken, dynamicRequestId, walletId, shareSetId, exportId, bitcoinConfig, approvalQuorum, proposalId, onError, traceContext }) {
        const { addressType } = bitcoinConfig || {};
        const requestBody = _extends({
            exportId
        }, addressType ? {
            addressType
        } : {}, shareSetId ? {
            shareSetId
        } : {}, approvalQuorum ? {
            approvalQuorum
        } : {}, proposalId ? {
            proposalId
        } : {});
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `${this.waasRoutePrefix}/${walletId}/privateKey/export`,
            body: requestBody,
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Key export timed out',
            onError,
            mfaToken,
            elevatedAccessToken,
            traceContext
        });
    }
    /**
   * Plain-JSON (non-SSE) variant of `exportKey`. Hits the same
   * `/privateKey/export` endpoint; the `x-idempotency-key` header tells the
   * backend (when `enable-http-waas-transport-export` is on) to respond with
   * the OpenRoomResponse synchronously instead of streaming `room_created`
   * over SSE.
   */ async requestExportKeyJson({ mfaToken, elevatedAccessToken, dynamicRequestId, walletId, shareSetId, exportId, bitcoinConfig, onError, traceContext, idempotencyKey, timeoutMs }) {
        const { addressType } = bitcoinConfig || {};
        const requestBody = _extends({
            exportId
        }, addressType ? {
            addressType
        } : {}, shareSetId ? {
            shareSetId
        } : {});
        return requestJson({
            apiClient: this.apiClient,
            dynamicRequestId,
            idempotencyKey,
            endpoint: `${this.waasRoutePrefix}/${walletId}/privateKey/export`,
            body: requestBody,
            timeoutMs: timeoutMs != null ? timeoutMs : 20000,
            timeoutMessage: 'Key export timed out',
            onError,
            mfaToken,
            elevatedAccessToken,
            traceContext
        });
    }
    /**
   * Kick off the Aleo view-key export MPC ceremony. Returns the MPC room once
   * redcoast + wallet-service have joined; the client then joins the same
   * room via Sodot's `exportViewKey` to receive the view key.
   */ async exportAleoViewKey({ mfaToken, elevatedAccessToken, dynamicRequestId, walletId, exportId, onError, traceContext }) {
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `/api/v0/sdk/${this.environmentId}/waas/${walletId}/aleo/viewKey/export`,
            body: {
                exportId
            },
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Aleo view key export timed out',
            onError,
            mfaToken,
            elevatedAccessToken,
            traceContext
        });
    }
    /**
   * Kick off the Aleo signRequest MPC ceremony. Returns the MPC room once
   * redcoast + wallet-service have joined; the client then joins the same
   * room via Sodot's `signRequest` with the same payload to finalize.
   */ async signAleoRequest({ mfaToken, elevatedAccessToken, dynamicRequestId, walletId, payload, onError, traceContext }) {
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `/api/v0/sdk/${this.environmentId}/waas/${walletId}/aleo/signRequest`,
            body: {
                payload
            },
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Aleo signRequest timed out',
            onError,
            mfaToken,
            elevatedAccessToken,
            traceContext
        });
    }
    /**
   * Fetch the Aleo Feemaster sponsorship policy for a network. Redcoast
   * holds the ANF Bearer key server-side and forwards. Caller usually
   * doesn't walk the policy directly; `isAleoFeemasterCovered` is the
   * convenience.
   */ async getAleoFeemasterPolicy({ network, traceContext }) {
        const { data } = await this.apiClient.get(`/api/v0/sdk/${this.environmentId}/waas/aleo/feemaster/policy`, {
            params: {
                network
            },
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Coverage check via the redcoast convenience endpoint — server-side
   * walks the (cached) policy and returns a boolean.
   */ async isAleoFeemasterCovered({ network, programId, functionName, traceContext }) {
        const { data } = await this.apiClient.get(`/api/v0/sdk/${this.environmentId}/waas/aleo/feemaster/is-covered`, {
            params: {
                network,
                programId,
                functionName
            },
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return Boolean(data == null ? void 0 : data.covered);
    }
    /**
   * Forward a user-signed Aleo Authorization to ANF (via redcoast) and
   * return the corresponding `feeAuthorization` for bundling into a
   * ProvingRequest. Throws on quota errors or service failures so the
   * caller can fall back to user-paid fees.
   */ async requestAleoFeeAuthorization({ network, authorization, priorityFee, traceContext }) {
        const { data } = await this.apiClient.post(`/api/v0/sdk/${this.environmentId}/waas/aleo/feemaster/fee-auth`, {
            network,
            authorization,
            priorityFee
        }, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Aleo RecordScanner — fetch the ephemeral public key Provable will
   * use to encrypt the next view-key registration. Forwards through
   * redcoast which holds the apiKey + consumerId server-side.
   */ async getAleoScannerPubkey({ network, traceContext }) {
        const { data } = await this.apiClient.get(`/api/v0/sdk/${this.environmentId}/waas/aleo/scanner/pubkey`, {
            params: {
                network
            },
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Aleo RecordScanner — register an encrypted view key. Body carries
   * the iframe's `crypto_box_seal` ciphertext; redcoast forwards it
   * verbatim. Server returns the assigned scanner UUID.
   */ async registerAleoScanner({ network, keyId, ciphertext, traceContext }) {
        const { data } = await this.apiClient.post(`/api/v0/sdk/${this.environmentId}/waas/aleo/scanner/register`, {
            network,
            key_id: keyId,
            ciphertext
        }, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Aleo RecordScanner — find owned records by uuid + filter. The filter
   * shape is passed through to Provable verbatim; the iframe handles
   * local decryption with its view key.
   */ async findAleoScannerRecords({ network, filter, traceContext }) {
        const { data } = await this.apiClient.post(`/api/v0/sdk/${this.environmentId}/waas/aleo/scanner/find-records`, {
            network,
            filter
        }, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Aleo RecordScanner — revoke a registration UUID.
   */ async revokeAleoScanner({ network, uuid, traceContext }) {
        const { data } = await this.apiClient.post(`/api/v0/sdk/${this.environmentId}/waas/aleo/scanner/revoke`, {
            network,
            uuid
        }, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    async getDelegatedEncryptionKey({ environmentId, traceContext }) {
        const { data } = await this.apiClient.get(`${this.sdkRoutePrefix}/${environmentId}/waas/delegatedAccess/encryptionPublicKey`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    async publishDelegatedKeyShare({ walletId, shareSetId, encryptedKeyShare, signedSessionId, requiresSignedSessionId = false, dynamicRequestId, traceContext }) {
        if (requiresSignedSessionId && !signedSessionId) {
            throw new Error('Signed session ID is required');
        }
        const apiClient = this.apiClient;
        const { data, status } = await apiClient.post(`${this.waasRoutePrefix}/${walletId}/delegatedAccess/delivery`, _extends({
            encryptedDelegatedShare: encryptedKeyShare
        }, shareSetId ? {
            shareSetId
        } : {}), {
            headers: {
                [DynamicRequestIdHeader]: dynamicRequestId,
                [DynamicClientSessionSignature]: signedSessionId,
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return {
            data,
            status
        };
    }
    async revokeDelegation({ walletId, shareSetId, signedSessionId, requiresSignedSessionId = false, dynamicRequestId, traceContext }) {
        if (requiresSignedSessionId && !signedSessionId) {
            throw new Error('Signed session ID is required');
        }
        const { data } = await this.apiClient.delete(`/api/v0/sdk/${this.environmentId}/waas/${walletId}/delegatedAccess/${shareSetId}`, {
            headers: {
                [DynamicRequestIdHeader]: dynamicRequestId,
                [DynamicClientSessionSignature]: signedSessionId,
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    // shareSetId is forwarded only when `sendLocation` is also true —
    // that's the signal that CKS should call redcoast's backup/locations
    // itself once the share is stored. Redcoast needs shareSetId to resolve
    // which share set to activate when a wallet has more than one (e.g. mid
    // refresh/reshare, where an old active set and a new pending set coexist);
    // without it CKS would have nothing to forward and activation could target
    // the wrong set.
    async storeEncryptedBackupByWallet({ walletId, encryptedKeyShares, passwordEncrypted, passwordSetByBA, signedSessionId, sessionPublicKey, encryptionVersion, requiresSignedSessionId = false, dynamicRequestId, traceContext, sendLocation, shareSetId, businessAccountId, passwordUpdateBatchId }) {
        if (requiresSignedSessionId && !signedSessionId) {
            throw new Error('Signed session ID is required');
        }
        const { data } = await this.clientRelayApiClient.post(`${this.waasRoutePrefix}/${walletId}/keyShares/backup`, _extends({
            // TODO: decide on whether to store encryptedAccountCredentials or encryptedKeyShares as backup
            encryptedAccountCredentials: encryptedKeyShares,
            passwordEncrypted
        }, passwordSetByBA !== undefined ? {
            passwordSetByBA
        } : {}, {
            encryptionVersion
        }, sendLocation ? _extends({
            sendLocation
        }, shareSetId ? {
            shareSetId
        } : {}, businessAccountId ? {
            businessAccountId
        } : {}, passwordUpdateBatchId ? {
            passwordUpdateBatchId
        } : {}) : {}), {
            headers: _extends({
                [DynamicRequestIdHeader]: dynamicRequestId,
                [DynamicClientSessionSignature]: signedSessionId
            }, sessionPublicKey ? {
                [DynamicSessionPublicKeyHeader]: sessionPublicKey
            } : {}, {
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            })
        });
        return data;
    }
    async markKeySharesAsBackedUp({ walletId, shareSetId, locations, dynamicRequestId, traceContext, passwordUpdateBatchId, businessAccountId }) {
        assertDynamicLocationsHaveExternalKeyShareId(locations);
        const { data } = await this.apiClient.post(`${this.sdkWaasRoutePrefix}/${walletId}/keyShares/backup/locations`, _extends({
            locations
        }, passwordUpdateBatchId && {
            passwordUpdateBatchId
        }, shareSetId ? {
            shareSetId
        } : {}, businessAccountId ? {
            businessAccountId
        } : {}), {
            headers: {
                [DynamicRequestIdHeader]: dynamicRequestId,
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    // shareSetId is accepted in the param shape so callers can thread their
    // wallet-map state through, but is intentionally NOT destructured or
    // forwarded — CKS resolves shares by externalKeyShareId.
    async recoverEncryptedBackupByWallet({ walletId, externalKeyShareIds, signedSessionId, mfaToken, requiresSignedSessionId = false, traceContext, userId }) {
        if (requiresSignedSessionId && !signedSessionId) {
            throw new Error('Signed session ID is required');
        }
        // TODO: add signed messsage to body?
        const dynamicRequestId = v4().replace('-', '');
        this.logger.debug('[walletMap] recoverEncryptedBackupByWallet request', {
            context: {
                dynamicRequestId,
                walletId,
                externalKeyShareIds,
                environmentId: this.environmentId
            }
        });
        // CKS is share-set-agnostic — it resolves shares by externalKeyShareId.
        // Never forward shareSetId here.
        const recoverBody = externalKeyShareIds ? {
            keyShareIds: externalKeyShareIds
        } : undefined;
        const { data } = await this.clientRelayApiClient.post(`${this.waasRoutePrefix}/${walletId}/keyShares/recover`, recoverBody, {
            headers: {
                [DynamicRequestIdHeader]: dynamicRequestId,
                [DynamicClientSessionSignature]: signedSessionId,
                [DynamicMfaTokenHeader]: mfaToken,
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        if (data.keyShares && data.keyShares.length > 1) {
            this.logger.warn('Recover encrypted backup by wallet returning more than 1 share', {
                context: {
                    dynamicRequestId,
                    environmentId: this.environmentId,
                    keyShareCount: data.keyShares.length,
                    walletId,
                    userId
                }
            });
        }
        return data;
    }
    async getAccessToken({ oauthAccountId, traceContext }) {
        const { data } = await this.apiClient.get(`${this.sdkRoutePrefix}/${this.environmentId}/oauthAccounts/${oauthAccountId}/accessToken`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data.accessToken;
    }
    // TODO: return array instead considering cases where server has multiple parties
    async importPrivateKey({ chainName, dynamicRequestId, clientKeygenIds, thresholdSignatureScheme, bitcoinConfig, onError, onCeremonyComplete, traceContext, legacyWalletId, variant }) {
        const { addressType } = bitcoinConfig || {};
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `${this.waasRoutePrefix}/privateKey/import`,
            body: _extends({
                chain: chainName,
                clientKeygenIds,
                thresholdSignatureScheme
            }, addressType ? {
                addressType
            } : {}, legacyWalletId ? {
                legacyWalletId
            } : {}, variant ? {
                variant
            } : {}),
            successEventType: SuccessEventType.KeygenComplete,
            timeoutMessage: 'Key import timed out',
            onError,
            onCeremonyComplete,
            traceContext
        });
    }
    async getUser(dynamicRequestId, traceContext) {
        const { data } = await this.apiClient.get(`${this.sdkRoutePrefix}/${this.environmentId}/users`, {
            headers: {
                [DynamicRequestIdHeader]: dynamicRequestId,
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    async refreshUser(traceContext) {
        const { data } = await this.apiClient.post(`${this.sdkRoutePrefix}/${this.environmentId}/refresh`, undefined, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    async getEnvironmentSettings(traceContext) {
        const { data } = await this.apiClient.get(`${this.sdkRoutePrefix}/${this.environmentId}/settings`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    async getWaasWalletById({ walletId, traceContext }) {
        const { data } = await this.apiClient.get(`/api/v0/environments/${this.environmentId}/waas/${walletId}`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Fetch a single WaaS wallet by ID using the /sdk/{environmentId}/waas/{walletId} endpoint.
   * This endpoint returns user information with verified credentials filtered to only include the specified WaaS wallet.
   */ async getWaasWalletByAddress({ walletAddress, traceContext }) {
        const { data } = await this.apiClient.get(`${this.waasRoutePrefix}/byWalletAddress/${walletAddress}`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    // --- Business accounts (SDK routes, JWT-authed, membership-scoped) ---
    /** Create a business account; the caller's JWT user is seeded as the first owner. */ async createBusinessAccount({ request, traceContext }) {
        const { data } = await this.apiClient.post(this.businessAccountsRoutePrefix, request, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /** List business accounts the caller is a member of. */ async listBusinessAccounts({ traceContext } = {}) {
        const { data } = await this.apiClient.get(this.businessAccountsRoutePrefix, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /** Get a business account with embedded members + signers. 404 if the caller is not a member. */ async getBusinessAccountById({ businessAccountId, traceContext }) {
        const { data } = await this.apiClient.get(`${this.businessAccountsRoutePrefix}/${businessAccountId}`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Add an existing wallet to a business account. No ceremony — the server
   * transfers ownership and registers the caller as owner + signer bound to
   * their existing share set. Omit `businessAccountId` to find-or-create the
   * per-wallet business account. Returns the business-account detail. Idempotent.
   */ async linkWalletToBusinessAccount({ walletId, businessAccountId, traceContext }) {
        const { data } = await this.apiClient.post(`${this.businessAccountsRoutePrefix}/linkWallet`, _extends({
            walletId
        }, businessAccountId ? {
            businessAccountId
        } : {}), {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Add a member to a business account. Resolve the target by `userId`, or by
   * `identifier` + `identifierType` (e.g. an email) — the user is created if
   * absent, mirroring addBusinessAccountSigner.
   */ async addBusinessAccountMember({ businessAccountId, userId, identifier, identifierType, smsCountryCode, socialProvider, role, traceContext }) {
        const { data } = await this.apiClient.post(`${this.businessAccountsRoutePrefix}/${businessAccountId}/members`, _extends({}, userId ? {
            userId
        } : {}, identifier ? {
            identifier
        } : {}, identifierType ? {
            type: identifierType
        } : {}, smsCountryCode ? {
            smsCountryCode
        } : {}, socialProvider ? {
            socialProvider
        } : {}, role ? {
            role
        } : {}), {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * Add a signer to a business-account wallet. Resolve the target by `userId`, or by
   * `identifier` + `identifierType` (e.g. an email). Returns a PENDING signer
   * (HTTP 202, `shareSetId: null`) — the reshare ceremony that mints the share
   * is a follow-up and not yet performed server-side.
   */ async addBusinessAccountSigner({ businessAccountId, walletId, signerType, userId, identifier, identifierType, smsCountryCode, socialProvider, traceContext }) {
        const { data } = await this.apiClient.post(`${this.businessAccountsRoutePrefix}/${businessAccountId}/wallets/${walletId}/signers`, _extends({
            signerType
        }, userId ? {
            userId
        } : {}, identifier ? {
            identifier
        } : {}, identifierType ? {
            type: identifierType
        } : {}, smsCountryCode ? {
            smsCountryCode
        } : {}, socialProvider ? {
            socialProvider
        } : {}), {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    /**
   * SSE ceremony for addSigner. Same-parties 2/2 -> 2/2 reshare on the signers
   * endpoint: the caller's existing client share participates as the remaining
   * party (clientKeygenIds = [existing], no new party). The server runs the
   * reshare with `newServerKeygenIds=[]` and persists the result as a NEW
   * isolated share set for the target signer — it does not refresh the
   * caller's set in place.
   *
   * Returns the room (createEventStreamPromise) + the new `shareSetId` via
   * onCeremonyComplete. The resulting client share is reshared locally and
   * seeded to the client-keyshare-service on the target's behalf (see
   * `seedBusinessAccountSignerShare`).
   */ async addBusinessAccountSignerCeremony({ businessAccountId, walletId, clientKeygenIds, oldThresholdSignatureScheme, signerType, userId, identifier, identifierType, signedIntent, initialSignerRules, dynamicRequestId, elevatedAccessToken, onError, onCeremonyComplete, traceContext }) {
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            elevatedAccessToken,
            endpoint: `${this.businessAccountsRoutePrefix}/${encodeURIComponent(businessAccountId)}/wallets/${encodeURIComponent(walletId)}/signers`,
            body: _extends({
                signerType,
                clientKeygenIds,
                oldThresholdSignatureScheme,
                // FF-on share-set semantics: always reshare to a NEW 2/2 share set.
                newThresholdSignatureScheme: ThresholdSignatureScheme.TWO_OF_TWO
            }, userId ? {
                userId
            } : {}, identifier ? {
                identifier
            } : {}, identifierType ? {
                type: identifierType
            } : {}, sanitizeBusinessAccountSignedIntent(signedIntent), initialSignerRules ? {
                initialSignerRules
            } : {}),
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Add signer reshare timed out',
            onError,
            onCeremonyComplete,
            traceContext
        });
    }
    /**
   * On-behalf KSS write for addSigner: store the added signer's freshly-reshared
   * client share in the client-keyshare-service keyed to the ADDED signer's
   * partition via `targetUserId` in the body. Uses the caller's relay auth (the
   * business-account-membership gate is FF-bypassed for now; the client-keyshare-service
   * reads `targetUserId` and inserts-if-empty). Returns the stored keyShareId(s)
   * to thread as `externalKeyShareId` into `markKeySharesAsBackedUp`.
   * Hardened auth (scoped grant token) is the follow-up — DYNT-1071/1072.
   */ async backupOnBehalfOfAddedSigner({ walletId, targetUserId, encryptedAccountCredentials, passwordEncrypted, encryptionVersion, clientKeyshareBackupGrant, signedSessionId, dynamicRequestId, traceContext }) {
        const { data } = await this.clientRelayApiClient.post(`${this.waasRoutePrefix}/${walletId}/keyShares/backup`, {
            encryptedAccountCredentials,
            passwordEncrypted,
            passwordSetByBA: true,
            encryptionVersion,
            targetUserId
        }, {
            headers: _extends({
                [DynamicRequestIdHeader]: dynamicRequestId,
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }, signedSessionId && {
                [DynamicClientSessionSignature]: signedSessionId
            }, clientKeyshareBackupGrant && {
                Authorization: `Bearer ${clientKeyshareBackupGrant}`
            })
        });
        return data;
    }
    async delegatedSignMessage({ walletId, shareSetId, message, isFormatted, dynamicRequestId, onError, context, traceContext }) {
        return createEventStreamPromise({
            apiClient: this.apiClient,
            dynamicRequestId,
            endpoint: `/api/v0/environments/${this.environmentId}/waas/${walletId}/delegatedAccess/signMessage`,
            body: _extends({
                message,
                isFormatted,
                context
            }, shareSetId ? {
                shareSetId
            } : {}),
            successEventType: SuccessEventType.RoomCreated,
            timeoutMessage: 'Delegated sign message timed out',
            onError,
            traceContext
        });
    }
    async createRooms({ walletId, roomType, roomCount = 5, traceContext }) {
        const { data } = await this.apiClient.post(`${this.waasRoutePrefix}/${walletId}/createRooms`, {
            roomCount,
            roomType
        }, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    async createRoomsWithoutWalletId({ roomType, thresholdSignatureScheme, roomCount = 5, traceContext }) {
        const { data } = await this.apiClient.post(`${this.waasRoutePrefix}/createRooms`, {
            roomCount,
            roomType,
            thresholdSignatureScheme
        }, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    async requestSvmSponsoredTransaction({ transaction, userId, traceContext }) {
        try {
            const { data } = await this.apiClient.post(`${this.sdkRoutePrefix}/${this.environmentId}/solana/sponsorTransaction`, _extends({
                transaction
            }, userId ? {
                userId
            } : {}), {
                headers: {
                    [DynamicRequestIdHeader]: v4().replace('-', ''),
                    [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                    [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
                }
            });
            return data;
        } catch (error) {
            this.throwGaslessApiError('SVM sponsorship failed', error);
        }
    }
    buildTraceHeaders(traceContext) {
        return {
            [DynamicRequestIdHeader]: v4().replace('-', ''),
            [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
            [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
        };
    }
    throwGaslessApiError(label, error) {
        var _error_response, _error_response1;
        const status = error == null ? void 0 : (_error_response = error.response) == null ? void 0 : _error_response.status;
        const rawData = error == null ? void 0 : (_error_response1 = error.response) == null ? void 0 : _error_response1.data;
        var _rawData_error, _ref;
        const detail = (_ref = (_rawData_error = rawData == null ? void 0 : rawData.error) != null ? _rawData_error : typeof rawData === 'string' ? rawData : JSON.stringify(rawData)) != null ? _ref : error == null ? void 0 : error.message;
        const statusStr = status ? ` (${status})` : '';
        // Callers that branch on the HTTP status (e.g. re-authenticating on a 401)
        // need it as data, not prose. The axios error is not re-thrown or attached
        // as a cause because its config carries the request's bearer token.
        throw Object.assign(new Error(`${label}${statusStr}: ${detail}`), {
            status
        });
    }
    async sponsorEVMTransaction({ request, traceContext }) {
        try {
            const { data } = await this.apiClient.post(`${this.sdkRoutePrefix}/${this.environmentId}/evm/sponsorTransaction`, request, {
                headers: this.buildTraceHeaders(traceContext)
            });
            return data;
        } catch (error) {
            this.throwGaslessApiError('EVM sponsorship failed', error);
        }
    }
    async getEVMSponsoredTransactionStatus({ requestId, traceContext }) {
        try {
            const { data } = await this.apiClient.get(`${this.sdkRoutePrefix}/${this.environmentId}/evm/sponsorTransaction/${requestId}`, {
                headers: this.buildTraceHeaders(traceContext)
            });
            return data;
        } catch (error) {
            this.throwGaslessApiError('EVM sponsorship status check failed', error);
        }
    }
    async getAvailableEVMGaslessRelayer({ chainId, traceContext }) {
        try {
            const { data } = await this.apiClient.get(`${this.sdkEvmRoutePrefix}/availableGaslessRelayer`, {
                params: {
                    chainId
                },
                headers: this.buildTraceHeaders(traceContext)
            });
            return data;
        } catch (error) {
            this.throwGaslessApiError('EVM gasless relayer lookup failed', error);
        }
    }
    async getNonces({ count = 1 } = {}) {
        if (!Number.isInteger(count) || count < 1) {
            throw new Error('getNonces: count must be a positive integer');
        }
        const { data } = await this.apiClient.get(`${this.sdkRoutePrefix}/${this.environmentId}/nonces?count=${count}`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', '')
            }
        });
        return data;
    }
    /**
   * Resolves this environment's server identity — a real userId the server
   * itself is authenticated as, but with no discoverable email/externalUserId
   * of its own. Feed the returned userId into `businessAccounts.addMember`
   * to add the server as a business-account member. Server-only — always
   * uses `/api/v0/server`, regardless of `isServerSdk`, since this client is
   * shared with the browser SDK (via `BusinessAccountClient`) and the route
   * doesn't exist under `/api/v0/sdk`.
   */ async getServerIdentity() {
        const { data } = await this.apiClient.get(`${SERVER_SDK_ROUTE_PREFIX}/${this.environmentId}/serverIdentity`, {
            headers: {
                [DynamicRequestIdHeader]: v4().replace('-', '')
            }
        });
        return data;
    }
    async updateAdditionalAddresses({ walletId, additionalAddresses, dynamicRequestId, traceContext }) {
        const { data } = await this.apiClient.put(`/api/v0/sdk/${this.environmentId}/waas/${walletId}/additionalAddresses`, {
            additionalAddresses
        }, {
            headers: {
                [DynamicRequestIdHeader]: dynamicRequestId || v4().replace('-', ''),
                [DynamicTraceIdHeader]: traceContext == null ? void 0 : traceContext.traceId,
                [DynamicTraceElapsedTimeHeader]: getElapsedTime(traceContext == null ? void 0 : traceContext.startTime)
            }
        });
        return data;
    }
    constructor({ environmentId, authToken, backupServiceAuthToken, baseApiUrl, authMode = AuthMode.HEADER, // Represents the version of the client SDK used by developer
    sdkVersion, forwardMPCClient, baseClientKeysharesRelayApiUrl, logger, isServerSdk = false, onUnauthorized }){
        super({
            environmentId,
            authToken: authToken || '',
            backupServiceAuthToken,
            baseApiUrl,
            authMode,
            sdkVersion,
            forwardMPCClient,
            baseClientKeysharesRelayApiUrl,
            logger,
            onUnauthorized
        });
        this.sdkRoutePrefix = isServerSdk ? SERVER_SDK_ROUTE_PREFIX : BROWSER_SDK_ROUTE_PREFIX;
        this.waasRoutePrefix = `${this.sdkRoutePrefix}/${this.environmentId}/waas`;
        this.sdkWaasRoutePrefix = `${BROWSER_SDK_ROUTE_PREFIX}/${this.environmentId}/waas`;
        this.sdkEvmRoutePrefix = `${BROWSER_SDK_ROUTE_PREFIX}/${this.environmentId}/evm`;
        this.businessAccountsRoutePrefix = `${this.sdkRoutePrefix}/${this.environmentId}/businessAccounts`;
    }
}

const SUPPORTED_IDENTIFIER_TYPES = new Set([
    'email',
    'externalUserId',
    'id',
    'phoneNumber',
    'socialAccountId',
    'socialUsername'
]);
/**
 * Business-account orchestration. Lives in core (not on the monolithic wallet
 * client) so both browser and node clients can compose it. Pure REST today.
 */ class BusinessAccountClient {
    /** Create a business account; the authenticated caller is seeded as the first owner member. */ async createBusinessAccount(request = {}, options) {
        return this.apiClient.createBusinessAccount({
            request,
            traceContext: options == null ? void 0 : options.traceContext
        });
    }
    /** List business accounts the caller is a member of. */ async listBusinessAccounts(options) {
        return this.apiClient.listBusinessAccounts({
            traceContext: options == null ? void 0 : options.traceContext
        });
    }
    /**
   * Resolves this environment's server identity — feed the returned userId
   * into `addMember({ targetIdentity: { userId } })` to add the server as a
   * business-account member. Server-only.
   */ async getServerIdentity() {
        return this.apiClient.getServerIdentity();
    }
    /** Full account detail (members + signers). 404 if the caller is not a member. */ async getBusinessAccount(businessAccountId, options) {
        return this.apiClient.getBusinessAccountById({
            businessAccountId,
            traceContext: options == null ? void 0 : options.traceContext
        });
    }
    /**
   * Bring an existing wallet under a business account so signers can be added to it.
   * Pure REST, no ceremony — the owner already holds a valid share set, so the
   * server just transfers ownership and registers the caller as owner + signer.
   * Omit `businessAccountId` to find-or-create the per-wallet business account.
   * Idempotent.
   */ async addWalletToBusinessAccount({ walletId, businessAccountId, traceContext }) {
        return this.apiClient.linkWalletToBusinessAccount({
            walletId,
            businessAccountId,
            traceContext
        });
    }
    /**
   * Add a member to a business account, resolved by `email` (or explicit
   * `userId`), mirroring addSigner. The server creates the user if absent.
   * Caller must be an owner/admin.
   */ async addMember({ businessAccountId, targetIdentity, role, traceContext }) {
        const { userId, identifier, identifierType, smsCountryCode, socialProvider } = targetIdentity;
        if (!userId && !(identifier && identifierType)) {
            throw new Error('BusinessAccountClient.addMember requires targetIdentity.userId, or identifier + identifierType');
        }
        if (identifierType && !SUPPORTED_IDENTIFIER_TYPES.has(identifierType)) {
            throw new Error(`BusinessAccountClient.addMember: identifierType '${identifierType}' is not supported. Use one of: ${[
                ...SUPPORTED_IDENTIFIER_TYPES
            ].join(', ')}.`);
        }
        return this.apiClient.addBusinessAccountMember({
            businessAccountId,
            userId,
            identifier,
            identifierType,
            smsCountryCode,
            socialProvider,
            role,
            traceContext
        });
    }
    /**
   * Add a signer to a business-account wallet, resolved by `email` (or explicit
   * `userId`). Server creates the user if absent, auto-adds them as a member,
   * and writes a PENDING signer row. Returns the pending signer — the reshare
   * ceremony that mints the share lives in the browser SDK.
   *
   * Omit `businessAccountId` to add a signer to a wallet that isn't in a
   * business account yet: we first find-or-create the per-wallet account via
   * `addWalletToBusinessAccount` (idempotent — returns the existing account if
   * the wallet is already linked, or converts the personal wallet by minting
   * the account and seating its owner as the first signer), then add the new
   * signer to it.
   */ async addSigner({ businessAccountId, walletId, targetSignerIdentity, signerType = 'endUser', traceContext }) {
        const { userId, identifier, identifierType, smsCountryCode, socialProvider } = targetSignerIdentity;
        if (!userId && !(identifier && identifierType)) {
            throw new Error('BusinessAccountClient.addSigner requires targetSignerIdentity.userId, or identifier + identifierType');
        }
        if (identifierType && !SUPPORTED_IDENTIFIER_TYPES.has(identifierType)) {
            throw new Error(`BusinessAccountClient.addSigner: identifierType '${identifierType}' is not supported. Use one of: ${[
                ...SUPPORTED_IDENTIFIER_TYPES
            ].join(', ')}.`);
        }
        let resolvedBusinessAccountId = businessAccountId;
        if (!resolvedBusinessAccountId) {
            this.logger.info('BusinessAccountClient.addSigner: no businessAccountId — find-or-creating the per-wallet account before adding the signer');
            const account = await this.addWalletToBusinessAccount({
                walletId,
                traceContext
            });
            resolvedBusinessAccountId = account.id;
        }
        this.logger.info('BusinessAccountClient.addSigner creating pending signer (reshare pending)');
        return this.apiClient.addBusinessAccountSigner({
            businessAccountId: resolvedBusinessAccountId,
            walletId,
            signerType,
            userId,
            identifier,
            identifierType,
            smsCountryCode,
            socialProvider,
            traceContext
        });
    }
    constructor({ apiClient, logger }){
        this.apiClient = apiClient;
        this.logger = logger;
    }
}

const isPreparedTransaction = (prepared)=>prepared.operation.kind === 'transaction';
const isPreparedSvmTransaction = (prepared)=>prepared.operation.chainName === 'SVM';
const validateRequest = (request, prepared, now)=>{
    if (Number.isNaN(now.getTime())) throw new Error('Invalid signing intent creation time');
    if (!request.accountAddress || !request.businessAccountId || !request.initiatorUserId) {
        throw new Error('Signing intent identity is required');
    }
    if (!Object.values(WaasChainEnum).includes(request.chainName)) {
        throw new Error('Signing intent requires a canonical chain name');
    }
    if (request.chainName !== prepared.operation.chainName || request.kind !== prepared.operation.kind) {
        throw new Error('Signing intent operation does not match request');
    }
    if (request.kind === 'message' && request.chainName === 'TRON') {
        throw new Error('TRON message signing intents are unsupported');
    }
};
const validateCompleteBy = (completeBy, now)=>{
    if (!completeBy) return;
    const timestamp = Date.parse(completeBy);
    const isCanonicalFutureTimestamp = Number.isFinite(timestamp) && new Date(timestamp).toISOString() === completeBy && timestamp > now.getTime();
    if (!isCanonicalFutureTimestamp) {
        throw new Error('Signing intent completion time must be a future ISO timestamp');
    }
};
const createEnvelope = (request, now, providedIntentId)=>{
    var _cryptoProvider_randomUUID;
    const cryptoProvider = globalThis.crypto;
    const intentId = providedIntentId != null ? providedIntentId : cryptoProvider == null ? void 0 : (_cryptoProvider_randomUUID = cryptoProvider.randomUUID) == null ? void 0 : _cryptoProvider_randomUUID.call(cryptoProvider);
    if (!intentId) throw new Error('Secure UUID generation is unavailable');
    return _extends({
        actionType: 'waasSigningQuorumApprove',
        accountAddress: request.accountAddress,
        businessAccountId: request.businessAccountId,
        initiatorUserId: request.initiatorUserId,
        intentId,
        createdAt: now.toISOString()
    }, request.completeBy ? {
        completeBy: request.completeBy
    } : {});
};
const addEvmTransactionMetadata = (envelope, { operation, limits, lifetime })=>{
    if (!limits) throw new Error('Transaction signing limits are required');
    if (!lifetime) return _extends({}, envelope, {
        operation,
        limits
    });
    if (lifetime.refreshable !== 'nonce') throw new Error('EVM signing intent lifetime must be nonce');
    return _extends({}, envelope, {
        operation,
        limits,
        lifetime: {
            refreshable: 'nonce'
        }
    });
};
const addSvmTransactionMetadata = (envelope, { operation, lifetime })=>{
    if ((lifetime == null ? void 0 : lifetime.refreshable) !== 'blockhash') throw new Error('SVM signing intent requires a lifetime');
    return _extends({}, envelope, {
        operation,
        lifetime: {
            refreshable: 'blockhash'
        }
    });
};
const addTransactionMetadata = (envelope, prepared)=>{
    if (isPreparedSvmTransaction(prepared)) return addSvmTransactionMetadata(envelope, prepared);
    return addEvmTransactionMetadata(envelope, prepared);
};
const addMessageMetadata = (envelope, request, operation)=>{
    if (request.kind !== 'message' || typeof request.message !== 'string') {
        throw new Error('Signing intent message is required');
    }
    return _extends({}, envelope, {
        operation: _extends({}, operation, {
            message: request.message
        })
    });
};
const addTypedDataMetadata = (envelope, request, operation)=>{
    if (request.kind !== 'typedData' || request.chainName !== 'EVM' || !request.typedData) {
        throw new Error('EVM signing intent typed data is required');
    }
    return _extends({}, envelope, {
        operation: _extends({}, operation, {
            chainName: 'EVM',
            typedData: request.typedData
        })
    });
};
const addRawMetadata = (envelope, request, operation)=>{
    var _request_rawSign;
    if (request.kind !== 'raw' || !((_request_rawSign = request.rawSign) == null ? void 0 : _request_rawSign.payload) || !request.rawSign.hashFunction) {
        throw new Error('Raw signing intent requires a preimage and hash function');
    }
    return _extends({}, envelope, {
        operation: _extends({}, operation, {
            rawSign: request.rawSign
        })
    });
};
const addEip7702AuthMetadata = (envelope, request, operation)=>{
    if (request.kind !== 'eip7702Auth') throw new Error('EIP-7702 signing intent authorization is required');
    return _extends({}, envelope, {
        operation
    });
};
const addRequestMetadata = (envelope, request, prepared)=>{
    if (isPreparedTransaction(prepared)) return addTransactionMetadata(envelope, prepared);
    switch(prepared.operation.kind){
        case 'message':
            return addMessageMetadata(envelope, request, prepared.operation);
        case 'typedData':
            return addTypedDataMetadata(envelope, request, prepared.operation);
        case 'raw':
            return addRawMetadata(envelope, request, prepared.operation);
        case 'eip7702Auth':
            return addEip7702AuthMetadata(envelope, request, prepared.operation);
    }
};
const createSigningIntent = (request, prepared, options = {})=>{
    var _options_now;
    const now = (_options_now = options.now) != null ? _options_now : new Date();
    validateRequest(request, prepared, now);
    validateCompleteBy(request.completeBy, now);
    return addRequestMetadata(createEnvelope(request, now, options.intentId), request, prepared);
};

/** Must match redcoast's and wallet-service's `WAAS_EXPORT_INTENT_ACTION`. */ const WAAS_EXPORT_INTENT_ACTION = 'waasExportQuorumApprove';
/** How long approvers have when the caller doesn't ask for a shorter window. */ const DEFAULT_COMPLETE_WITHIN_MS = 24 * 60 * 60 * 1000;
const assertIdentity = (request)=>{
    if (!request.accountAddress || !request.businessAccountId || !request.initiatorUserId || !request.exportId) {
        throw new Error('Export intent identity is required');
    }
};
const assertValidNow = (now)=>{
    if (Number.isNaN(now.getTime())) throw new Error('Invalid export intent creation time');
};
/** The caller's `completeBy`, or the default window, once it is known to be a canonical future ISO timestamp. */ const resolveCompleteBy = (requested, now)=>{
    const completeBy = requested != null ? requested : new Date(now.getTime() + DEFAULT_COMPLETE_WITHIN_MS).toISOString();
    const timestamp = Date.parse(completeBy);
    const isCanonicalFutureTimestamp = Number.isFinite(timestamp) && new Date(timestamp).toISOString() === completeBy && timestamp > now.getTime();
    if (!isCanonicalFutureTimestamp) {
        throw new Error('Export intent completion time must be a future ISO timestamp');
    }
    return completeBy;
};
/**
 * Builds the export Intent the initiator signs. It binds one `exportId`, so a
 * set of approvals can't be replayed onto a different export. The server
 * clamps `completeBy` to the policy rule's own window; it can only tighten it.
 */ const createExportIntent = (request, options = {})=>{
    var _globalThis_crypto_randomUUID, _globalThis_crypto;
    var _options_now;
    const now = (_options_now = options.now) != null ? _options_now : new Date();
    assertValidNow(now);
    assertIdentity(request);
    const completeBy = resolveCompleteBy(request.completeBy, now);
    var _options_intentId;
    const intentId = (_options_intentId = options.intentId) != null ? _options_intentId : (_globalThis_crypto = globalThis.crypto) == null ? void 0 : (_globalThis_crypto_randomUUID = _globalThis_crypto.randomUUID) == null ? void 0 : _globalThis_crypto_randomUUID.call(_globalThis_crypto);
    if (!intentId) throw new Error('Secure UUID generation is unavailable');
    return {
        accountAddress: request.accountAddress,
        actionType: WAAS_EXPORT_INTENT_ACTION,
        businessAccountId: request.businessAccountId,
        completeBy,
        createdAt: now.toISOString(),
        initiatorUserId: request.initiatorUserId,
        intentId,
        operation: {
            exportId: request.exportId,
            kind: 'export',
            restriction: 'blockExport'
        }
    };
};

const SDK_NAMESPACE = {
    REACT: 'WalletKit',
    CLIENT: 'ClientSDK'
};
/**
 * Parses a potentially namespaced SDK version string
 * @param sdkVersion - The SDK version string, optionally namespaced
 * @returns Parsed SDK version with namespace and version
 * @example
 * parseNamespacedVersion("WalletKit/1.0.0") // { namespace: "WalletKit", version: "1.0.0", raw: "WalletKit/1.0.0" }
 * parseNamespacedVersion("1.0.0") // { namespace: "WalletKit", version: "1.0.0", raw: "1.0.0" }
 */ function parseNamespacedVersion(sdkVersion) {
    if (!sdkVersion || sdkVersion === '') {
        return null;
    }
    // Check if the version contains a namespace
    const colonIndex = sdkVersion.indexOf('/');
    if (colonIndex !== -1) {
        const namespace = sdkVersion.substring(0, colonIndex);
        const version = sdkVersion.substring(colonIndex + 1);
        // Validate namespace
        if (!Object.values(SDK_NAMESPACE).includes(namespace)) {
            return {
                namespace: SDK_NAMESPACE.REACT,
                version,
                raw: sdkVersion
            };
        }
        return {
            namespace: namespace,
            version,
            raw: sdkVersion
        };
    }
    // No namespace found, default to react-sdk for backward compatibility
    return {
        namespace: 'WalletKit',
        version: sdkVersion,
        raw: sdkVersion
    };
}
/**
 * Formats a parsed SDK version back to string format
 * @param parsedVersion - The parsed SDK version object
 * @returns Formatted SDK version string
 */ function formatNamespacedVersion(parsedVersion) {
    return `${parsedVersion.namespace}/${parsedVersion.version}`;
}
/**
 * Gets the version string without namespace
 * @param sdkVersion - The SDK version string, optionally namespaced
 * @returns Version string without namespace
 */ function getVersionWithoutNamespace(sdkVersion) {
    const parsed = parseNamespacedVersion(sdkVersion);
    return parsed ? parsed.version : null;
}
/**
 * Gets the namespace from a potentially namespaced SDK version
 * @param sdkVersion - The SDK version string, optionally namespaced
 * @returns The namespace or default namespace
 */ function getVersionNamespace(sdkVersion) {
    const parsed = parseNamespacedVersion(sdkVersion);
    return parsed ? parsed.namespace : null;
}

/**
 * Chain names whose forward-MPC payload is treated as EVM-compatible:
 * they use secp256k1 ECDSA signing and serialize a pre-hashed
 * (`isFormatted=true`) payload over the wire as a hex string.
 *
 * Add new EVM-compatible chains here.
 */ const EVM_COMPATIBLE_CHAINS = [
    'EVM',
    'TEMPO',
    'TRON'
];
/**
 * Returns `true` if `chainName` is an EVM-compatible chain — i.e. signs with
 * secp256k1 ECDSA and serializes pre-hashed messages over the forward-MPC
 * wire as a hex string.
 *
 * The check is case-sensitive: pass the canonical uppercase chain identifier
 * (e.g. `'EVM'`, `'TEMPO'`, `'TRON'`).
 *
 * @param chainName - Canonical chain name to test.
 * @returns `true` if the chain is EVM-compatible, `false` otherwise.
 *
 * @example
 * isEvmCompatibleChain('EVM');   // => true
 * isEvmCompatibleChain('TRON');  // => true
 * isEvmCompatibleChain('SUI');   // => false
 * isEvmCompatibleChain('tron');  // => false (case-sensitive)
 */ const isEvmCompatibleChain = (chainName)=>EVM_COMPATIBLE_CHAINS.includes(chainName);

const serializeMessageForForwardMPC = ({ message, isFormatted = false, chainName })=>{
    let serializedMessage = message;
    if (isFormatted && isEvmCompatibleChain(chainName)) {
        if (typeof message === 'string') {
            // Handle hex string (with or without 0x prefix)
            const cleanHex = message.startsWith('0x') ? message.slice(2) : message;
            serializedMessage = cleanHex;
        } else if (message instanceof Uint8Array) {
            serializedMessage = Buffer.from(message).toString('hex');
        } else if (message instanceof MessageHash) {
            serializedMessage = message.toHex();
        } else {
            throw new Error('Unsupported formatted message format');
        }
    }
    return serializedMessage;
};

// Mirrors forward-mpc-client's ErrorCode values (the /utils subpath does not
// export the ErrorCode const, so the codes are inlined here).
const RECOVERED_CONNECTION_CHURN_CODES = new Set([
    'CONNECTION_FAILED',
    'CONNECTION_TIMEOUT',
    'NOT_CONNECTED',
    'TRANSPORT_CLOSED',
    'HANDSHAKE_FAILED'
]);
/**
 * Returns true when a classified Forward MPC error is recovered connection
 * churn that should be logged at `warn` rather than `error`.
 *
 * The Forward MPC enclave is an optimization side-channel: the client retries
 * connections internally, and `shouldFallback` is true for every Forward MPC
 * failure mode — relay-based MPC is a fully functional safety net, so a
 * connection-lifecycle failure never blocks a user operation on its own.
 * Terminal failures (both paths failing) are logged at the operation sites.
 *
 * Churn covers rate-limited upgrades and the transport-lifecycle error codes
 * (connect/reconnect failures, timeouts, socket closes, and handshake-request
 * timeouts — production evidence shows these concentrate on hostile/flaky
 * networks). Attestation failures, HANDSHAKE_INVALID_RESPONSE, SERVER_ERROR,
 * and unclassified errors are NOT churn: they indicate enclave tampering or
 * protocol breakage and must stay at `error` so monitors can page on them.
 */ const isRecoveredForwardMpcConnectionChurn = (classification)=>classification.errorType === 'RATE_LIMITED' || classification.errorCode !== undefined && RECOVERED_CONNECTION_CHURN_CODES.has(classification.errorCode);

/**
 * Appends `envId` to the ForwardMPC enclave WebSocket URL.
 *
 * The enclave binds the value to its session logger at the WS upgrade, and the
 * Cloudflare WAF rules on `mpc-client.*` match `envId=<uuid>` in the query
 * string to exempt approved environments from the per-IP /ws rate limits.
 */ const buildForwardMpcEnclaveUrl = (baseEnclaveUrl, environmentId)=>{
    if (!environmentId) {
        return baseEnclaveUrl;
    }
    const separator = baseEnclaveUrl.includes('?') ? '&' : '?';
    return `${baseEnclaveUrl}${separator}envId=${encodeURIComponent(environmentId)}`;
};

/**
 * Normalizes an unknown thrown value into flat, log-friendly fields.
 *
 * Error objects don't survive serialization into log context (their `name`,
 * `message`, and `stack` are non-enumerable, so they serialize to `{}`), which
 * is why the underlying cause of signing failures was invisible in Datadog.
 * This extracts the useful detail — including a wrapped `cause` — into plain
 * strings that loggers will actually emit and that can be grouped/filtered on.
 */ const serializeError = (error)=>{
    const err = error instanceof Error ? error : new Error(String(error));
    const cause = err.cause;
    return _extends({
        errorName: err.name,
        errorMessage: err.message
    }, cause instanceof Error ? {
        causeMessage: cause.message
    } : {});
};

const formatRawMessageForSigning = (chainName, message)=>{
    if (typeof message !== 'string') return message;
    const hex = message.startsWith('0x') ? message.slice(2) : message;
    if (/^[0-9A-Fa-f]+$/.test(hex)) {
        return new Uint8Array(Buffer.from(hex, 'hex'));
    }
    return chainName === 'ALEO' ? new Uint8Array(Buffer.from(message, 'utf-8')) : Buffer.from(message).toString('hex');
};
const prepareRawMessageSigningPayload = (chainName, message)=>{
    const formatted = formatRawMessageForSigning(chainName, message);
    return typeof formatted === 'string' ? formatted : Buffer.from(formatted).toString('hex');
};

/** Returns the context as plain JSON, with each bigint (which `JSON.stringify` throws on) turned into a string. */ const toJsonSafeContext = (context)=>{
    try {
        return JSON.parse(JSON.stringify(context, (_key, value)=>typeof value === 'bigint' ? String(value) : value));
    } catch (error) {
        throw new Error(`Could not serialize the signing context: ${error instanceof Error ? error.message : String(error)}`, {
            cause: error
        });
    }
};

/**
 * Returns a trace context that always has an id, so a retrying operation can hand the same one to each attempt.
 * The id is 32 lowercase hex characters, a valid W3C trace id the server can continue.
 */ const withTraceId = (traceContext)=>{
    var _traceContext_traceId, _traceContext_startTime;
    return _extends({}, traceContext, {
        traceId: (_traceContext_traceId = traceContext == null ? void 0 : traceContext.traceId) != null ? _traceContext_traceId : v4().replaceAll('-', ''),
        startTime: (_traceContext_startTime = traceContext == null ? void 0 : traceContext.startTime) != null ? _traceContext_startTime : Date.now()
    });
};

/** The ids a caller can quote to support so one failed attempt can be found in client and server logs. */ /** Sets `traceId` and `requestId` on a thrown error so apps can quote them, keeping any id already set. */ const attachRequestIds = (error, { traceId, requestId })=>{
    var _target, _target1;
    if (!error || typeof error !== 'object' || !Object.isExtensible(error)) {
        return;
    }
    const target = error;
    var _traceId;
    (_traceId = (_target = target).traceId) != null ? _traceId : _target.traceId = traceId;
    var _requestId;
    (_requestId = (_target1 = target).requestId) != null ? _requestId : _target1.requestId = requestId;
};

export { AuthMode, BITCOIN_ADDRESS_TYPE_CONFIG, BITCOIN_DERIVATION_PATHS, BROWSER_SDK_ROUTE_PREFIX, BackupLocation, BitcoinAddressType, BitcoinNetwork, BusinessAccountClient, BusinessAccountMemberRole, BusinessAccountSignerType, CreateRoomPartiesOptions, DEFAULT_ED25519_VARIANT, DELEGATED_SHARE_COUNT, DYNAMIC_AUTH_BASE_API_URL_MAP, DYNAMIC_AUTH_DEV_BASE_API_URL, DYNAMIC_AUTH_PREPROD_BASE_API_URL, DYNAMIC_AUTH_PROD_BASE_API_URL, DYNAMIC_CLIENT_RELAY_REDCOAST_API_KEY_MAP, DYNAMIC_CLIENT_RELAY_REDCOAST_APP_ID_MAP, DYNAMIC_FORWARD_MPC_DEV_ENCLAVE_URL, DYNAMIC_FORWARD_MPC_ENCLAVE_ATTESTATION_CONFIG_MAP, DYNAMIC_FORWARD_MPC_ENCLAVE_URL_MAP, DYNAMIC_FORWARD_MPC_PREPROD_ENCLAVE_URL, DYNAMIC_FORWARD_MPC_PROD_ENCLAVE_URL, DYNAMIC_KEYSHARES_RELAY_MAP, DYNAMIC_KEYSHARES_RELAY_PREPROD_BASE_API_URL, DYNAMIC_KEYSHARES_RELAY_PROD_BASE_API_URL, DynamicApiClient, DynamicClientSessionSignature, DynamicElevatedAccessTokenHeader, DynamicForwardMPCHeader, DynamicMfaTokenHeader, DynamicRequestIdHeader, DynamicSessionPublicKeyHeader, DynamicTraceElapsedTimeHeader, DynamicTraceIdHeader, ENCRYPTED_SHARES_STORAGE_SUFFIX, ENVIRONMENT_ENUM, EVM_COMPATIBLE_CHAINS, FEATURE_FLAGS, IFRAME_DOMAIN_MAP, Logger, MIDNIGHT_DERIVATION_PATHS, MPC_CHAIN_CONFIG, MPC_CONFIG, MPC_RELAY_DEV_API_URL, MPC_RELAY_PREPROD_API_URL, MPC_RELAY_PROD_API_URL, MPC_RELAY_URL_MAP, NETWORK_ERROR_CODE, NETWORK_ERROR_STATUS, NoopLogger, PREPROD_RELAY_API_KEY, PREPROD_RELAY_APP_ID, PROD_RELAY_API_KEY, PROD_RELAY_APP_ID, RELAY_API_KEY_HEADER, RELAY_APP_ID_HEADER, SDK_NAMESPACE, SERVER_SDK_ROUTE_PREFIX, SOLANA_RPC_URL, SignAndBroadcastRequestTooLargeError, SigningConsentRequiredError, SuccessEventType, ThresholdSignatureScheme, URL_PATTERNS, WAAS_EXPORT_INTENT_ACTION, WalletApiError, WalletOperation, WalletReadyState, assertDynamicLocationsHaveExternalKeyShareId, attachRequestIds, buildForwardMpcEnclaveUrl, chain, chainEnumToVerifiedCredentialName, createExportIntent, createRejectablePromise, createSigningIntent, extractServerErrorCode, formatNamespacedVersion, formatRawMessageForSigning, getBitcoinChainConfig, getClientThreshold, getDynamicServerThreshold, getEnvironmentFromUrl, getMPCChainConfig, getRequiredExternalKeyShareId, getReshareConfig, getServerWalletReshareConfig, getTSSConfig, getVersionNamespace, getVersionWithoutNamespace, handleAxiosError, invokeCeremonyComplete, isBusinessAccountActionRequired, isEvmCompatibleChain, isRecoveredForwardMpcConnectionChurn, normalizeAndValidatePrivateKey, parseNamespacedVersion, prepareRawMessageSigningPayload, sanitizeBusinessAccountSignedIntent, serializeError, serializeMessageForForwardMPC, toJsonSafeContext, verifiedCredentialNameToChainEnum, withTraceId };

export const ALERTS_CONSTANTS = {
    ACTIVE_ENDPOINT: '/alerts/active',
    ALL_ENDPOINT: '/alerts/all',
    RESOLVE_ENDPOINT: '/alerts/resolve',
    WS_URL: 'ws://localhost:8004/alerts/ws',
} as const;

export const ALERT_TYPE_LABELS: Record<string, string> = {
    HIGH_LATENCY: 'High Latency',
    HIGH_PACKET_LOSS: 'High Packet Loss',
    LOW_SIGNAL: 'Low Signal'
};

export const ALERT_TYPE_ICONS: Record<string, string> = {
    HIGH_LATENCY: '⚡',
    HIGH_PACKET_LOSS: '📉',
    LOW_SIGNAL: '📡'
};
export const DASHBOARD_CONSTANTS = {
    REFRESH_INTERVAL: 3000,
    ANALYTICS_SUMMARY: '/analytics/summary',
    TOP_LATENCY: '/analytics/top-latency',
    TRENDS: '/analytics/trends',
    ALL_DEVICES: '/analytics/devices',
    TOP_DEVICES_LIMIT: 10,
    LATEST_DEVICES: '/analytics/latest-devices',

} as const;

export const TIME_RANGES = [
    { label: '1 min', minutes: 1 },
    { label: '1 hour', minutes: 60 },
    { label: '3 hours', minutes: 180 },
] as const;

export const HUNGARY_CITIES: Record<string, [number, number]> = {
    'Budapest': [19.0402, 47.4979],
    'Debrecen': [21.6273, 47.5316],
    'Pécs': [18.2323, 46.0727],
    'Győr': [17.6504, 47.6875],
    'Miskolc': [20.7784, 48.1035],
    'Szeged': [20.1414, 46.2530],
    'Székesfehérvár': [18.4128, 47.1896],
    'Kecskemét': [19.6920, 46.9060],
    'Nyíregyháza': [21.7166, 47.9554],
    'Eger': [20.3772, 47.9028],
};

export const HUNGARY_BOUNDARY: [number, number][] = [
    [16.20, 46.85], [16.52, 46.50], [16.88, 45.94], [17.63, 45.83],
    [18.46, 45.76], [18.90, 45.93], [18.90, 46.30], [19.60, 46.18],
    [20.22, 46.13], [20.76, 46.29], [21.01, 46.32], [21.41, 46.42],
    [21.80, 46.25], [22.08, 46.01], [22.58, 47.64], [22.58, 48.02],
    [22.28, 48.40], [21.43, 48.56], [20.80, 48.52], [19.92, 48.17],
    [18.82, 48.04], [18.08, 47.82], [17.75, 47.77], [17.17, 47.71],
    [16.89, 47.99], [16.55, 48.01], [16.52, 47.64], [16.28, 47.31],
    [16.20, 46.85],
];
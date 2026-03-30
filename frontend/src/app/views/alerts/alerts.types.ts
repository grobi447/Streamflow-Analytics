export type AlertType = 'HIGH_LATENCY' | 'HIGH_PACKET_LOSS' | 'LOW_SIGNAL';
export type AlertSeverity = 'WARNING' | 'CRITICAL';

export interface Alert {
    alert_id: string;
    device_id: string;
    location: string;
    alert_type: AlertType;
    severity: AlertSeverity;
    message: string;
    value: number;
    threshold: number;
    timestamp: string;
    resolved: boolean;
}

export interface AlertStats {
    total: number;
    critical: number;
    warning: number;
    resolved: number;
    by_type: Record<AlertType, number>;
}
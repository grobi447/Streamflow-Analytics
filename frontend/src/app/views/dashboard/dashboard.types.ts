export interface NetworkSummary {
    total_events: number;
    total_devices: number;
    total_locations: number;
    avg_latency_ms: number;
    avg_packet_loss: number;
    avg_bandwidth_mbps: number;
}

export interface TopLatencyDevice {
    device_id: string;
    location: string;
    avg_latency_ms: number;
}

export interface TrendPoint {
    timestamp: string;
    avg_latency_ms: number;
    avg_packet_loss: number;
    avg_bandwidth_mbps: number;
    total_events: number;
}

export interface DeviceSummary {
    device_id: string;
    location: string;
    avg_latency_ms: number;
    avg_packet_loss: number;
    avg_bandwidth_mbps: number;
    avg_signal_strength_dbm: number;
    total_events: number;
}
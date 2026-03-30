import { Injectable, signal, computed } from '@angular/core';
import { NetworkSummary, TopLatencyDevice, TrendPoint, DeviceSummary } from './dashboard.types';

@Injectable({ providedIn: 'root' })
export class DashboardStore {
    private readonly _summary = signal<NetworkSummary | null>(null);
    private readonly _topLatency = signal<TopLatencyDevice[]>([]);
    private readonly _allDevices = signal<DeviceSummary[]>([]);
    private readonly _trends = signal<TrendPoint[]>([]);
    private readonly _lastUpdated = signal<Date | null>(null);
    private readonly _selectedHours = signal<number>(1);
    private readonly _selectedMinutes = signal<number>(60);
    private readonly _latestDevices = signal<DeviceSummary[]>([]);

    readonly summary = this._summary.asReadonly();
    readonly topLatency = this._topLatency.asReadonly();
    readonly allDevices = this._allDevices.asReadonly();
    readonly trends = this._trends.asReadonly();
    readonly lastUpdated = this._lastUpdated.asReadonly();
    readonly selectedHours = this._selectedHours.asReadonly();
    readonly selectedMinutes = this._selectedMinutes.asReadonly();
    readonly latestDevices = this._latestDevices.asReadonly();

    readonly avgLatency = computed(() => this._summary()?.avg_latency_ms ?? 0);
    readonly avgPacketLoss = computed(() => this._summary()?.avg_packet_loss ?? 0);
    readonly avgBandwidth = computed(() => this._summary()?.avg_bandwidth_mbps ?? 0);
    readonly totalEvents = computed(() => this._summary()?.total_events ?? 0);
    readonly totalDevices = computed(() => this._summary()?.total_devices ?? 0);
    readonly totalLocations = computed(() => this._summary()?.total_locations ?? 0);
    readonly selectedLabel = computed(() => {
        const minutes = this._selectedMinutes();
        if (minutes === 1) return '1 min';
        if (minutes === 60) return '1 hour';
        if (minutes === 180) return '3 hours';
        return `${minutes} min`;
    });

    updateSummary(data: NetworkSummary): void { this._summary.set({ ...data }); this._lastUpdated.set(new Date()); }
    updateTopLatency(data: TopLatencyDevice[]): void { this._topLatency.set([...data]); }
    updateAllDevices(data: DeviceSummary[]): void { this._allDevices.set([...data]); }
    updateTrends(data: TrendPoint[]): void { this._trends.set([...data]); }
    setSelectedHours(hours: number): void { this._selectedHours.set(hours); }
    setSelectedMinutes(minutes: number): void { this._selectedMinutes.set(minutes); }
    updateLatestDevices(data: DeviceSummary[]): void { this._latestDevices.set([...data]); }



}
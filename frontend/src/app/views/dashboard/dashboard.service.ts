import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin } from 'rxjs';
import { environment } from '../../environments/environment';
import { DASHBOARD_CONSTANTS } from './dashboard.constants';
import { NetworkSummary, TopLatencyDevice, TrendPoint, DeviceSummary } from './dashboard.types';

@Injectable({ providedIn: 'root' })
export class DashboardService {
    private readonly apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    getSummary(): Observable<NetworkSummary> {
        return this.http.get<NetworkSummary>(`${this.apiUrl}${DASHBOARD_CONSTANTS.ANALYTICS_SUMMARY}`);
    }

    getTopLatency(): Observable<TopLatencyDevice[]> {
        return this.http.get<TopLatencyDevice[]>(
            `${this.apiUrl}${DASHBOARD_CONSTANTS.TOP_LATENCY}?limit=${DASHBOARD_CONSTANTS.TOP_DEVICES_LIMIT}`
        );
    }

    getAllDevices(): Observable<DeviceSummary[]> {
        return this.http.get<DeviceSummary[]>(`${this.apiUrl}${DASHBOARD_CONSTANTS.ALL_DEVICES}`);
    }

    getTrends(minutes: number): Observable<TrendPoint[]> {
        return this.http.get<TrendPoint[]>(
            `${this.apiUrl}${DASHBOARD_CONSTANTS.TRENDS}?minutes=${minutes}`
        );
    }

    getLatestDevices(): Observable<DeviceSummary[]> {
        return this.http.get<DeviceSummary[]>(`${this.apiUrl}${DASHBOARD_CONSTANTS.LATEST_DEVICES}`);
    }

    getAllData(minutes: number): Observable<[NetworkSummary, TopLatencyDevice[], TrendPoint[], DeviceSummary[], DeviceSummary[]]> {
        return forkJoin([
            this.getSummary(),
            this.getTopLatency(),
            this.getTrends(minutes),
            this.getAllDevices(),
            this.getLatestDevices()
        ]);
    }
}
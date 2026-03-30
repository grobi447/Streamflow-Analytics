import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { DeviceSummary, TrendPoint } from './analytics.types';

@Injectable({ providedIn: 'root' })
export class AnalyticsService {
    private readonly apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    getAllDevices(): Observable<DeviceSummary[]> {
        return this.http.get<DeviceSummary[]>(`${this.apiUrl}/analytics/devices`).pipe(
            catchError(err => { console.error('getAllDevices error:', err); return of([]); })
        );
    }

    getTrends(minutes: number): Observable<TrendPoint[]> {
        return this.http.get<TrendPoint[]>(`${this.apiUrl}/analytics/trends?minutes=${minutes}`).pipe(
            catchError(err => { console.error('getTrends error:', err); return of([]); })
        );
    }

    getAllData(minutes: number): Observable<[DeviceSummary[], TrendPoint[]]> {
        return forkJoin([this.getAllDevices(), this.getTrends(minutes)]);
    }
}
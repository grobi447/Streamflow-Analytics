import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { ALERTS_CONSTANTS } from './alerts.constants';
import { Alert } from './alerts.types';

@Injectable({ providedIn: 'root' })
export class AlertsService {
    private readonly apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    getActive(): Observable<Alert[]> {
        return this.http.get<Alert[]>(`${this.apiUrl}${ALERTS_CONSTANTS.ACTIVE_ENDPOINT}`).pipe(
            catchError(err => { console.error('getActive error:', err); return of([]); })
        );
    }

    getAll(limit: number = 100): Observable<Alert[]> {
        return this.http.get<Alert[]>(`${this.apiUrl}${ALERTS_CONSTANTS.ALL_ENDPOINT}?limit=${limit}`).pipe(
            catchError(err => { console.error('getAll error:', err); return of([]); })
        );
    }

    resolve(alertId: string): Observable<any> {
        return this.http.put(`${this.apiUrl}${ALERTS_CONSTANTS.RESOLVE_ENDPOINT}/${alertId}`, {});
    }
}
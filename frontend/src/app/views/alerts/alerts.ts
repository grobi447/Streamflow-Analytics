import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { interval, Subscription, switchMap, startWith } from 'rxjs';
import { AlertsService } from './alerts.service';
import { Alert } from './alerts.types';
import { ALERTS_CONSTANTS } from './alerts.constants';
import { AlertStats } from './components/alert-stats/alert-stats';
import { AlertList } from './components/alert-list/alert-list';

@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [CommonModule, FormsModule, AlertStats, AlertList],
  templateUrl: './alerts.html',
  styleUrl: './alerts.scss'
})
export class Alerts implements OnInit, OnDestroy {
  allAlerts: Alert[] = [];
  showResolved = false;
  wsConnected = false;
  private subs: Subscription[] = [];
  private ws: WebSocket | null = null;
  private wsReconnectTimer: any = null;

  constructor(private service: AlertsService) { }

  ngOnInit(): void {
    // REST polling minden 3 mp-ben
    this.subs.push(
      interval(3000).pipe(
        startWith(0),
        switchMap(() => this.service.getAll(200))
      ).subscribe(alerts => {
        this.allAlerts = [...alerts];
      })
    );

    // WebSocket live updates
    this.connectWebSocket();
  }

  private connectWebSocket(): void {
    try {
      this.ws?.close();
      this.ws = new WebSocket(ALERTS_CONSTANTS.WS_URL);

      this.ws.onopen = () => {
        this.wsConnected = true;
        console.log('WebSocket connected');
      };

      this.ws.onmessage = (event) => {
        try {
          const alert: Alert = JSON.parse(event.data);
          // Csak hozzáadjuk ha még nincs benne
          if (!this.allAlerts.find(a => a.alert_id === alert.alert_id)) {
            this.allAlerts = [alert, ...this.allAlerts];
          }
        } catch (e) { console.error('WS parse error', e); }
      };

      this.ws.onerror = () => { this.wsConnected = false; };

      this.ws.onclose = () => {
        this.wsConnected = false;
        // Reconnect 5mp után
        this.wsReconnectTimer = setTimeout(() => this.connectWebSocket(), 5000);
      };
    } catch (e) {
      console.error('WebSocket error', e);
      this.wsConnected = false;
    }
  }

  resolveAlert(alertId: string): void {
    this.service.resolve(alertId).subscribe({
      next: () => {
        this.allAlerts = this.allAlerts.map(a =>
          a.alert_id === alertId ? { ...a, resolved: true } : a
        );
      },
      error: (err) => console.error('Resolve error:', err)
    });
  }

  ngOnDestroy(): void {
    this.subs.forEach(s => s.unsubscribe());
    clearTimeout(this.wsReconnectTimer);
    this.ws?.close();
  }
}
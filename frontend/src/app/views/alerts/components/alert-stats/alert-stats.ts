import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Alert } from '../../alerts.types';

@Component({
  selector: 'app-alert-stats',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './alert-stats.html',
  styleUrl: './alert-stats.scss'
})
export class AlertStats {
  @Input() alerts: Alert[] = [];

  get total() { return this.alerts.length; }
  get critical() { return this.alerts.filter(a => a.severity === 'CRITICAL' && !a.resolved).length; }
  get warning() { return this.alerts.filter(a => a.severity === 'WARNING' && !a.resolved).length; }
  get resolved() { return this.alerts.filter(a => a.resolved).length; }
  get highLatency() { return this.alerts.filter(a => a.alert_type === 'HIGH_LATENCY' && !a.resolved).length; }
  get highPacketLoss() { return this.alerts.filter(a => a.alert_type === 'HIGH_PACKET_LOSS' && !a.resolved).length; }
  get lowSignal() { return this.alerts.filter(a => a.alert_type === 'LOW_SIGNAL' && !a.resolved).length; }
}
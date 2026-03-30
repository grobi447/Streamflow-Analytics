import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Alert } from '../../alerts.types';
import { ALERT_TYPE_LABELS, ALERT_TYPE_ICONS } from '../../alerts.constants';

@Component({
  selector: 'app-alert-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './alert-list.html',
  styleUrl: './alert-list.scss'
})
export class AlertList {
  @Input() alerts: Alert[] = [];
  @Input() showResolved: boolean = false;
  @Output() resolve = new EventEmitter<string>();

  readonly typeLabels = ALERT_TYPE_LABELS;
  readonly typeIcons = ALERT_TYPE_ICONS;

  get filtered(): Alert[] {
    return this.showResolved ? this.alerts : this.alerts.filter(a => !a.resolved);
  }

  getSeverityColor(severity: string): string {
    return severity === 'CRITICAL' ? '#ef4444' : '#f59e0b';
  }

  onResolve(alertId: string): void {
    this.resolve.emit(alertId);
  }
}
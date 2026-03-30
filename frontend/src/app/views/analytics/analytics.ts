import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { interval, Subscription, switchMap, startWith } from 'rxjs';
import { AnalyticsService } from './analytics.service';
import { DeviceSummary, TrendPoint } from './analytics.types';
import { ANALYTICS_CONSTANTS } from './analytics.constants';
import { LocationHeatmap } from './components/location-heatmap/location-heatmap';
import { PacketLossChart } from './components/packet-loss-chart/packet-loss-chart';
import { SignalChart } from './components/signal-chart/signal-chart';
import { DeviceTable } from './components/device-table/device-table';

const TIME_RANGES = [
  { label: '1 min', minutes: 1 },
  { label: '1 hour', minutes: 60 },
  { label: '3 hours', minutes: 180 },
];

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, LocationHeatmap, PacketLossChart, SignalChart, DeviceTable],
  templateUrl: './analytics.html',
  styleUrl: './analytics.scss'
})
export class Analytics implements OnInit, OnDestroy {
  devices: DeviceSummary[] = [];
  trends: TrendPoint[] = [];
  selectedMinutes = 60;
  timeRanges = TIME_RANGES;
  private subs: Subscription[] = [];
  private refreshSub: Subscription | null = null;

  constructor(private service: AnalyticsService) { }

  ngOnInit(): void { this.startRefresh(); }

  selectRange(minutes: number): void {
    this.selectedMinutes = minutes;
    this.refreshSub?.unsubscribe();
    this.startRefresh();
  }

  private startRefresh(): void {
    this.refreshSub = interval(ANALYTICS_CONSTANTS.REFRESH_INTERVAL).pipe(
      startWith(0),
      switchMap(() => this.service.getAllData(this.selectedMinutes))
    ).subscribe(([devices, trends]) => {
      this.devices = [...devices];
      this.trends = [...trends];
    });
    this.subs.push(this.refreshSub);
  }

  ngOnDestroy(): void { this.subs.forEach(s => s.unsubscribe()); }
}
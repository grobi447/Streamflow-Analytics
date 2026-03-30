import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { interval, Subscription, switchMap, startWith } from 'rxjs';
import { DashboardService } from './dashboard.service';
import { DashboardStore } from './dashboard.store';
import { DASHBOARD_CONSTANTS, TIME_RANGES } from './dashboard.constants';
import { StatsCard } from './components/stats-card/stats-card';
import { LatencyChart } from './components/latency-chart/latency-chart';
import { BandwidthChart } from './components/bandwidth-chart/bandwidth-chart';
import { TopDevicesChart } from './components/top-devices-chart/top-devices-chart';
import { HungaryMap } from './components/hungary-map/hungary-map';
import { MultiMetricChart } from './components/multi-metric-chart/multi-metric-chart';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, StatsCard, LatencyChart, BandwidthChart, TopDevicesChart, HungaryMap, MultiMetricChart],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit, OnDestroy {
  readonly timeRanges = TIME_RANGES;
  private subs: Subscription[] = [];
  private refreshSub: Subscription | null = null;

  constructor(
    public store: DashboardStore,
    private service: DashboardService
  ) { }

  ngOnInit(): void {
    this.startRefresh();
  }

  selectTimeRange(minutes: number): void {
    this.store.setSelectedMinutes(minutes);
    this.refreshSub?.unsubscribe();
    this.startRefresh();
  }

  private startRefresh(): void {
    this.refreshSub = interval(DASHBOARD_CONSTANTS.REFRESH_INTERVAL).pipe(
      startWith(0),
      switchMap(() => this.service.getAllData(this.store.selectedMinutes()))
    ).subscribe(([summary, topLatency, trends, allDevices, latestDevices]) => {
      this.store.updateSummary(summary);
      this.store.updateTopLatency(topLatency);
      this.store.updateTrends(trends);
      this.store.updateAllDevices(allDevices);
      this.store.updateLatestDevices(latestDevices);
    });
    this.subs.push(this.refreshSub);
  }

  ngOnDestroy(): void {
    this.subs.forEach(s => s.unsubscribe());
  }
}
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DeviceSummary } from '../../analytics.types';

@Component({
  selector: 'app-device-table',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './device-table.html',
  styleUrl: './device-table.scss'
})
export class DeviceTable implements OnChanges {
  @Input() devices: DeviceSummary[] = [];
  filtered: DeviceSummary[] = [];
  search: string = '';
  sortKey: keyof DeviceSummary = 'avg_latency_ms';
  sortAsc: boolean = false;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['devices']) this.applyFilter();
  }

  applyFilter(): void {
    let result = [...this.devices];
    if (this.search) {
      const s = this.search.toLowerCase();
      result = result.filter(d => d.device_id.toLowerCase().includes(s) || d.location.toLowerCase().includes(s));
    }
    result.sort((a, b) => {
      const av = a[this.sortKey] as number;
      const bv = b[this.sortKey] as number;
      return this.sortAsc ? av - bv : bv - av;
    });
    this.filtered = result;
  }

  sort(key: keyof DeviceSummary): void {
    if (this.sortKey === key) this.sortAsc = !this.sortAsc;
    else { this.sortKey = key; this.sortAsc = false; }
    this.applyFilter();
  }

  getLatencyColor(ms: number): string {
    if (ms < 50) return '#10b981';
    if (ms < 100) return '#f59e0b';
    return '#ef4444';
  }

  getStatusBadge(ms: number): string {
    if (ms < 50) return 'Normal';
    if (ms < 100) return 'Warning';
    return 'Critical';
  }
}
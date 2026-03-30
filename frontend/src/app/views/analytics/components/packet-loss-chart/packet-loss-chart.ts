import { Component, Input, OnChanges, AfterViewInit, OnDestroy, SimpleChanges, ViewChild, ElementRef } from '@angular/core';
import * as Highcharts from 'highcharts';
import { TrendPoint } from '../../analytics.types';

@Component({
  selector: 'app-packet-loss-chart',
  standalone: true,
  imports: [],
  template: `<div #container class="chart-container"></div>`,
  styles: [`.chart-container { width: 100%; height: 260px; }`]
})
export class PacketLossChart implements AfterViewInit, OnChanges, OnDestroy {
  @Input() trends: TrendPoint[] = [];
  @ViewChild('container', { static: false }) container!: ElementRef;
  private chart: Highcharts.Chart | null = null;

  ngAfterViewInit(): void {
    this.chart = Highcharts.chart(this.container.nativeElement, {
      chart: { type: 'column', backgroundColor: 'transparent' },
      title: { text: 'Packet Loss Over Time', style: { color: '#f1f5f9', fontSize: '14px' } },
      xAxis: { type: 'datetime', labels: { style: { color: '#64748b' } }, lineColor: '#334155' },
      yAxis: {
        title: { text: '%', style: { color: '#64748b' } },
        labels: { style: { color: '#64748b' } },
        gridLineColor: '#334155',
        plotLines: [{ color: '#ef4444', value: 5, width: 1, dashStyle: 'Dash' }]
      },
      series: [{
        name: 'Packet Loss', type: 'column', data: [],
        color: '#f59e0b',
        zones: [{ value: 5, color: '#10b981' }, { color: '#ef4444' }]
      }],
      legend: { enabled: false },
      credits: { enabled: false },
      accessibility: { enabled: false },
      tooltip: { backgroundColor: '#1e293b', borderColor: '#334155', style: { color: '#f1f5f9' }, valueSuffix: ' %' }
    });
    if (this.trends.length) this.update();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['trends'] && this.chart) this.update();
  }

  ngOnDestroy(): void { this.chart?.destroy(); }

  private update(): void {
    const data = this.trends.map(t => [new Date(t.timestamp).getTime(), Math.round(t.avg_packet_loss * 100) / 100]);
    this.chart?.series[0].setData(data, true, { duration: 300 });
  }
}
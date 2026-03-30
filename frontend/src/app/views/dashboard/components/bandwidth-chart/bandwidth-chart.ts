import {
  Component, Input, OnChanges, AfterViewInit, OnDestroy,
  SimpleChanges, ViewChild, ElementRef
} from '@angular/core';
import * as Highcharts from 'highcharts';
import { TrendPoint } from '../../dashboard.types';

@Component({
  selector: 'app-bandwidth-chart',
  standalone: true,
  imports: [],
  template: `<div #container class="chart-container"></div>`,
  styles: [`.chart-container { width: 100%; height: 280px; }`]
})
export class BandwidthChart implements AfterViewInit, OnChanges, OnDestroy {
  @Input() trends: TrendPoint[] = [];
  @Input() timeLabel: string = '24h';
  @ViewChild('container', { static: false }) container!: ElementRef;
  private chart: Highcharts.Chart | null = null;
  private prevTimeLabel: string = '';

  ngAfterViewInit(): void {
    this.initChart();
  }

  ngOnChanges(changes: SimpleChanges): void {
    const timeLabelChanged = changes['timeLabel'] && !changes['timeLabel'].firstChange;
    const trendsChanged = changes['trends'] && !changes['trends'].firstChange;

    if (timeLabelChanged) {
      this.chart?.destroy();
      this.chart = null;
      setTimeout(() => this.initChart(), 50);
      return;
    }

    if (trendsChanged && this.chart) {
      this.update();
    }
  }

  ngOnDestroy(): void {
    this.chart?.destroy();
    this.chart = null;
  }

  private initChart(): void {
    if (!this.container?.nativeElement) return;
    this.prevTimeLabel = this.timeLabel;
    this.chart = Highcharts.chart(this.container.nativeElement, {
      chart: { type: 'area', backgroundColor: 'transparent', animation: { duration: 400 } },
      title: { text: `Bandwidth Over Time (${this.timeLabel})`, style: { color: '#f1f5f9', fontSize: '14px' } },
      xAxis: { type: 'datetime', labels: { style: { color: '#64748b' } }, lineColor: '#334155', tickColor: '#334155' },
      yAxis: {
        title: { text: 'Mbps', style: { color: '#64748b' } },
        labels: { style: { color: '#64748b' } },
        gridLineColor: '#334155'
      },
      series: [{
        name: 'Avg Bandwidth', type: 'area', data: [], color: '#10b981', lineWidth: 2,
        fillColor: { linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 }, stops: [[0, 'rgba(16,185,129,0.3)'], [1, 'rgba(16,185,129,0)']] }
      }],
      legend: { enabled: false },
      credits: { enabled: false },
      accessibility: { enabled: false },
      tooltip: { backgroundColor: '#1e293b', borderColor: '#334155', style: { color: '#f1f5f9' }, valueSuffix: ' Mbps' }
    });
    if (this.trends.length) this.update();
  }

  private update(): void {
    if (!this.chart) return;
    const data = this.trends.map(t => [new Date(t.timestamp).getTime(), Math.round(t.avg_bandwidth_mbps)]);
    this.chart.series[0].setData(data, true, { duration: 300 });
  }
}
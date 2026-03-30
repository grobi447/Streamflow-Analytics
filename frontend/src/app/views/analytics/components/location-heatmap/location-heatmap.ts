import { Component, Input, OnChanges, AfterViewInit, OnDestroy, SimpleChanges, ViewChild, ElementRef } from '@angular/core';
import { DeviceSummary } from '../../analytics.types';
import { LOCATIONS } from '../../analytics.constants';

@Component({
  selector: 'app-location-heatmap',
  standalone: true,
  imports: [],
  template: `<div #container class="chart-container"></div>`,
  styles: [`.chart-container { width: 100%; height: 350px; }`]
})
export class LocationHeatmap implements AfterViewInit, OnChanges, OnDestroy {
  @Input() devices: DeviceSummary[] = [];
  @ViewChild('container', { static: false }) container!: ElementRef;
  private initialized = false;

  ngAfterViewInit(): void {
    this.render();
    this.initialized = true;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['devices'] && this.initialized) this.render();
  }

  ngOnDestroy(): void {
    // @ts-ignore
    import('plotly.js-dist-min').then((P: any) => {
      if (this.container?.nativeElement) P.purge(this.container.nativeElement);
    });
  }

  private async render(): Promise<void> {
    if (!this.container?.nativeElement) return;
    // @ts-ignore
    const Plotly = await import('plotly.js-dist-min') as any;

    const metrics = ['avg_latency_ms', 'avg_packet_loss', 'avg_bandwidth_mbps', 'avg_signal_strength_dbm'];
    const metricLabels = ['Latency (ms)', 'Packet Loss (%)', 'Bandwidth (Mbps)', 'Signal (dBm)'];

    const locationMap = new Map<string, { latency: number[], packet: number[], bandwidth: number[], signal: number[] }>();
    LOCATIONS.forEach(l => locationMap.set(l, { latency: [], packet: [], bandwidth: [], signal: [] }));

    this.devices.forEach(d => {
      const loc = locationMap.get(d.location);
      if (loc) {
        loc.latency.push(d.avg_latency_ms);
        loc.packet.push(d.avg_packet_loss);
        loc.bandwidth.push(d.avg_bandwidth_mbps);
        loc.signal.push(d.avg_signal_strength_dbm);
      }
    });

    const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;

    const zValues = LOCATIONS.map(l => {
      const loc = locationMap.get(l)!;
      return [avg(loc.latency), avg(loc.packet), avg(loc.bandwidth), avg(loc.signal)];
    });

    Plotly.react(this.container.nativeElement, [{
      type: 'heatmap',
      z: zValues,
      x: metricLabels,
      y: LOCATIONS,
      colorscale: 'RdYlGn',
      reversescale: true,
      text: zValues.map(row => row.map(v => v.toFixed(2))),
      texttemplate: '%{text}',
      textfont: { color: '#0f172a', size: 11 }
    }], {
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      title: { text: 'Location Performance Heatmap', font: { color: '#f1f5f9', size: 14 } },
      xaxis: { color: '#94a3b8', tickfont: { color: '#94a3b8' } },
      yaxis: { color: '#94a3b8', tickfont: { color: '#94a3b8' } },
      margin: { t: 50, r: 20, b: 40, l: 130 }
    }, { responsive: true, displayModeBar: false });
  }
}
import { Component, Input, OnChanges, AfterViewInit, OnDestroy, SimpleChanges, ViewChild, ElementRef } from '@angular/core';
import { DeviceSummary } from '../../analytics.types';

@Component({
  selector: 'app-signal-chart',
  standalone: true,
  imports: [],
  template: `<div #container class="chart-container"></div>`,
  styles: [`.chart-container { width: 100%; height: 260px; }`]
})
export class SignalChart implements AfterViewInit, OnChanges, OnDestroy {
  @Input() devices: DeviceSummary[] = [];
  @ViewChild('container', { static: false }) container!: ElementRef;
  private initialized = false;

  ngAfterViewInit(): void { this.render(); this.initialized = true; }
  ngOnChanges(changes: SimpleChanges): void { if (changes['devices'] && this.initialized) this.render(); }
  ngOnDestroy(): void {
    // @ts-ignore
    import('plotly.js-dist-min').then((P: any) => { if (this.container?.nativeElement) P.purge(this.container.nativeElement); });
  }

  private async render(): Promise<void> {
    if (!this.container?.nativeElement || !this.devices.length) return;
    // @ts-ignore
    const Plotly = await import('plotly.js-dist-min') as any;

    const sorted = [...this.devices].sort((a, b) => a.avg_signal_strength_dbm - b.avg_signal_strength_dbm).slice(0, 20);

    Plotly.react(this.container.nativeElement, [{
      type: 'bar', orientation: 'h',
      x: sorted.map(d => d.avg_signal_strength_dbm),
      y: sorted.map(d => d.device_id),
      marker: {
        color: sorted.map(d => d.avg_signal_strength_dbm > -70 ? '#10b981' : d.avg_signal_strength_dbm > -85 ? '#f59e0b' : '#ef4444')
      },
      text: sorted.map(d => `${d.avg_signal_strength_dbm.toFixed(1)} dBm`),
      textposition: 'outside',
      textfont: { color: '#94a3b8', size: 10 }
    }], {
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      title: { text: 'Weakest Signal Devices (Top 20)', font: { color: '#f1f5f9', size: 14 } },
      xaxis: { color: '#94a3b8', tickfont: { color: '#94a3b8' }, title: { text: 'dBm', font: { color: '#64748b' } } },
      yaxis: { color: '#94a3b8', tickfont: { color: '#94a3b8', size: 9 } },
      margin: { t: 50, r: 80, b: 50, l: 100 }
    }, { responsive: true, displayModeBar: false });
  }
}
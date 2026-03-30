import {
    Component, Input, OnChanges, AfterViewInit, OnDestroy,
    SimpleChanges, ViewChild, ElementRef
} from '@angular/core';
import { TrendPoint } from '../../dashboard.types';

@Component({
    selector: 'app-multi-metric-chart',
    standalone: true,
    imports: [],
    template: `<div #container class="chart-container"></div>`,
    styles: [`.chart-container { width: 100%; height: 300px; }`]
})
export class MultiMetricChart implements AfterViewInit, OnChanges, OnDestroy {
    @Input() trends: TrendPoint[] = [];
    @ViewChild('container', { static: false }) container!: ElementRef;
    private initialized = false;

    ngAfterViewInit(): void {
        this.initPlotly();
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['trends'] && this.initialized) this.update();
    }

    ngOnDestroy(): void {
        // @ts-ignore
        import('plotly.js-dist-min').then((Plotly: any) => {
            if (this.container?.nativeElement) Plotly.purge(this.container.nativeElement);
        });
    }

    private async initPlotly(): Promise<void> {
        await this.renderChart();
        this.initialized = true;
    }

    private async update(): Promise<void> {
        await this.renderChart();
    }

    private async renderChart(): Promise<void> {
        if (!this.container?.nativeElement) return;
        // @ts-ignore
        const Plotly = await import('plotly.js-dist-min') as any;

        const times = this.trends.map(t => t.timestamp);
        const latency = this.trends.map(t => Math.round(t.avg_latency_ms * 10) / 10);
        const packetLoss = this.trends.map(t => Math.round(t.avg_packet_loss * 100) / 100);
        const events = this.trends.map(t => t.total_events);

        const traces = [
            {
                x: times, y: latency,
                name: 'Latency (ms)',
                type: 'scatter', mode: 'lines',
                line: { color: '#3b82f6', width: 2 },
                yaxis: 'y'
            },
            {
                x: times, y: packetLoss,
                name: 'Packet Loss (%)',
                type: 'scatter', mode: 'lines',
                line: { color: '#ef4444', width: 2, dash: 'dot' },
                yaxis: 'y2'
            },
            {
                x: times, y: events,
                name: 'Events',
                type: 'bar',
                marker: { color: 'rgba(16,185,129,0.4)' },
                yaxis: 'y3'
            }
        ];

        const layout: any = {
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            title: { text: 'Network Metrics Overview', font: { color: '#f1f5f9', size: 14 }, x: 0.5 },
            showlegend: true,
            legend: {
                orientation: 'h',
                x: 0, y: 1.15,
                font: { color: '#94a3b8', size: 11 },
                bgcolor: 'transparent'
            },
            xaxis: {
                domain: [0.08, 0.88],
                color: '#64748b',
                showgrid: false,
                tickfont: { color: '#64748b', size: 10 }
            },
            yaxis: {
                title: { text: 'Latency (ms)', font: { color: '#3b82f6', size: 11 }, standoff: 5 },
                color: '#3b82f6',
                gridcolor: '#334155',
                tickfont: { color: '#3b82f6', size: 10 },
                side: 'left'
            },
            yaxis2: {
                title: { text: 'Packet Loss (%)', font: { color: '#ef4444', size: 11 }, standoff: 5 },
                color: '#ef4444',
                overlaying: 'y',
                side: 'right',
                tickfont: { color: '#ef4444', size: 10 },
                showgrid: false,
                position: 0.88
            },
            yaxis3: {
                title: { text: 'Events', font: { color: '#10b981', size: 11 }, standoff: 5 },
                color: '#10b981',
                overlaying: 'y',
                side: 'right',
                tickfont: { color: '#10b981', size: 10 },
                showgrid: false,
                anchor: 'free',
                position: 1.0
            },
            margin: { t: 70, r: 80, b: 40, l: 70 }
        };

        Plotly.react(this.container.nativeElement, traces, layout, { responsive: true, displayModeBar: false });
    }
}
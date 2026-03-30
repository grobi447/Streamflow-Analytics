import {
    Component, Input, OnChanges, AfterViewInit, OnDestroy,
    SimpleChanges, ViewChild, ElementRef
} from '@angular/core';
import * as Highcharts from 'highcharts';
import { TopLatencyDevice } from '../../dashboard.types';

@Component({
    selector: 'app-top-devices-chart',
    standalone: true,
    imports: [],
    template: `<div #container class="chart-container"></div>`,
    styles: [`.chart-container { width: 100%; height: 320px; }`]
})
export class TopDevicesChart implements AfterViewInit, OnChanges, OnDestroy {
    @Input() devices: TopLatencyDevice[] = [];
    @ViewChild('container', { static: false }) container!: ElementRef;
    private chart: Highcharts.Chart | null = null;

    ngAfterViewInit(): void {
        this.chart = Highcharts.chart(this.container.nativeElement, {
            chart: { type: 'bar', backgroundColor: 'transparent', animation: { duration: 400 } },
            title: { text: 'Top Latency Devices', style: { color: '#f1f5f9', fontSize: '14px' } },
            xAxis: { categories: [], labels: { style: { color: '#64748b', fontSize: '11px' } }, lineColor: '#334155' },
            yAxis: {
                title: { text: 'Avg Latency (ms)', style: { color: '#64748b' } },
                labels: { style: { color: '#64748b' } },
                gridLineColor: '#1e293b',
                plotLines: [{ color: '#ef4444', value: 100, width: 1, dashStyle: 'Dash' }]
            },
            series: [{
                name: 'Latency (ms)',
                type: 'bar',
                data: [],
                colorByPoint: true,
                colors: ['#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16', '#22c55e', '#14b8a6', '#06b6d4', '#3b82f6', '#8b5cf6']
            }],
            legend: { enabled: false },
            credits: { enabled: false },
            tooltip: { backgroundColor: '#1e293b', borderColor: '#334155', style: { color: '#f1f5f9' }, valueSuffix: ' ms' }
        });
        if (this.devices.length) this.update();
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['devices'] && this.chart) this.update();
    }

    ngOnDestroy(): void {
        this.chart?.destroy();
        this.chart = null;
    }

    private update(): void {
        const sorted = [...this.devices].sort((a, b) => b.avg_latency_ms - a.avg_latency_ms);
        this.chart?.xAxis[0].setCategories(sorted.map(d => `${d.device_id} (${d.location})`));
        this.chart?.series[0].setData(sorted.map(d => Math.round(d.avg_latency_ms * 100) / 100), true, { duration: 300 });
    }
}
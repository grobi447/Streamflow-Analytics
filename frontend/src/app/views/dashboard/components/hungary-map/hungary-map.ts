import {
    Component, Input, OnChanges, AfterViewInit,
    SimpleChanges, ViewChild, ElementRef, OnDestroy
} from '@angular/core';
import * as d3 from 'd3';
import { DeviceSummary } from '../../dashboard.types';
import { HUNGARY_CITIES, HUNGARY_BOUNDARY } from '../../dashboard.constants';

@Component({
    selector: 'app-hungary-map',
    standalone: true,
    imports: [],
    templateUrl: './hungary-map.html',
    styleUrl: './hungary-map.scss'
})
export class HungaryMap implements AfterViewInit, OnChanges, OnDestroy {
    @Input() devices: DeviceSummary[] = [];
    @ViewChild('mapContainer', { static: false }) mapContainer!: ElementRef;

    private svg: any = null;
    private projection: any = null;
    private readonly W = 800;
    private readonly H = 420;
    private initialized = false;

    ngAfterViewInit(): void {
        setTimeout(() => { this.init(); this.initialized = true; }, 100);
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['devices'] && this.initialized && this.svg) {
            this.updateDevices();
        }
    }

    ngOnDestroy(): void {
        d3.select(this.mapContainer?.nativeElement).selectAll('*').remove();
    }

    private init(): void {
        const el = this.mapContainer?.nativeElement;
        if (!el) return;

        d3.select(el).selectAll('*').remove();

        this.svg = d3.select(el)
            .append('svg')
            .attr('viewBox', `0 0 ${this.W} ${this.H}`)
            .attr('width', '100%')
            .attr('height', '100%')
            .style('background', '#0f172a')
            .style('border-radius', '8px');

        this.projection = d3.geoMercator()
            .center([19.5, 47.15])
            .scale(3900)
            .translate([this.W / 2, this.H / 2]);

        const path = d3.geoPath().projection(this.projection);

        const hungaryFeature: any = {
            type: 'Feature',
            geometry: { type: 'Polygon', coordinates: [HUNGARY_BOUNDARY] }
        };

        this.svg.append('path')
            .datum(hungaryFeature)
            .attr('d', path)
            .attr('fill', '#1e293b')
            .attr('stroke', '#475569')
            .attr('stroke-width', 2);

        this.svg.append('text')
            .attr('x', this.W / 2).attr('y', 28)
            .attr('text-anchor', 'middle')
            .attr('fill', '#f1f5f9')
            .attr('font-size', '15px')
            .attr('font-weight', '600')
            .text('Network Topology — Hungary');

        // Legend
        const legend = this.svg.append('g').attr('transform', `translate(20, ${this.H - 90})`);
        [
            { color: '#10b981', label: '< 50ms — Normal' },
            { color: '#f59e0b', label: '50–100ms — Warning' },
            { color: '#ef4444', label: '> 100ms — Critical' }
        ].forEach((item, i) => {
            legend.append('circle').attr('cx', 8).attr('cy', i * 24).attr('r', 8).attr('fill', item.color);
            legend.append('text').attr('x', 24).attr('y', i * 24 + 5).attr('fill', '#94a3b8').attr('font-size', '12px').text(item.label);
        });

        if (this.devices.length) this.updateDevices();
    }

    private updateDevices(): void {
        if (!this.svg || !this.projection) return;

        this.svg.selectAll('.device-node').remove();

        // Per location aggregation
        const locationMap = new Map<string, { latencies: number[], count: number }>();
        this.devices.forEach(d => {
            if (!locationMap.has(d.location)) locationMap.set(d.location, { latencies: [], count: 0 });
            const loc = locationMap.get(d.location)!;
            loc.latencies.push(d.avg_latency_ms);
            loc.count++;
        });

        const locationData = Array.from(locationMap.entries()).map(([location, data]) => ({
            location,
            avg_latency: data.latencies.reduce((a, b) => a + b, 0) / data.latencies.length,
            device_count: data.count
        }));

        const maxLatency = Math.max(...locationData.map(d => d.avg_latency), 200);
        const maxCount = Math.max(...locationData.map(d => d.device_count), 1);

        const colorScale = (latency: number): string => {
            if (latency < 50) return '#10b981';
            if (latency < 100) return '#f59e0b';
            return '#ef4444';
        };

        const sizeScale = d3.scaleLinear()
            .domain([0, maxCount])
            .range([10, 22]); // circle width

        locationData.forEach(loc => {
            const coords = HUNGARY_CITIES[loc.location];
            if (!coords) return;

            const p = this.projection!(coords);
            if (!p) return;

            const g = this.svg.append('g')
                .attr('class', 'device-node')
                .attr('transform', `translate(${p[0]},${p[1]})`);

            const color = colorScale(loc.avg_latency);
            const r = sizeScale(loc.device_count);

            // Outer pulse
            g.append('circle')
                .attr('r', r + 6)
                .attr('fill', 'none')
                .attr('stroke', color)
                .attr('stroke-width', 1.5)
                .attr('opacity', 0.3);

            // Main circle
            g.append('circle')
                .attr('r', r)
                .attr('fill', color)
                .attr('stroke', '#0f172a')
                .attr('stroke-width', 2)
                .attr('opacity', 0.85);

            // Latency text
            g.append('text')
                .attr('y', 4)
                .attr('text-anchor', 'middle')
                .attr('fill', '#0f172a')
                .attr('font-size', '10px')
                .attr('font-weight', '700')
                .text(`${Math.round(loc.avg_latency)}ms`);

            // City label above
            g.append('text')
                .attr('y', -(r + 10))
                .attr('text-anchor', 'middle')
                .attr('fill', '#f1f5f9')
                .attr('font-size', '11px')
                .attr('font-weight', '500')
                .text(loc.location);

            // Device count below
            g.append('text')
                .attr('y', r + 16)
                .attr('text-anchor', 'middle')
                .attr('fill', '#64748b')
                .attr('font-size', '10px')
                .text(`${loc.device_count} devices`);
        });
    }
}
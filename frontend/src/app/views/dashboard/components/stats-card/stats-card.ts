import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stats-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stats-card.html',
  styleUrl: './stats-card.scss'
})
export class StatsCard {
  @Input() title: string = '';
  @Input() value: string | number | null = '';
  @Input() unit: string = '';
  @Input() color: string = '#3b82f6';
  @Input() icon: string = '';
  @Input() trend: number = 0;
}
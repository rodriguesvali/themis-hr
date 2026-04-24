import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { AvatarModule } from 'primeng/avatar';
import { CardModule } from 'primeng/card';
import { PanelModule } from 'primeng/panel';
import { DividerModule } from 'primeng/divider';
import { MenuModule } from 'primeng/menu';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, ButtonModule, TagModule, AvatarModule, CardModule, PanelModule, DividerModule, MenuModule],
  templateUrl: './admin.html',
  styleUrl: './admin.css',
})
export class AdminComponent {
  readonly menuItems: MenuItem[] = [
    { label: 'Tickets escalonados', icon: 'pi pi-ticket' },
    { label: 'Colaboradores', icon: 'pi pi-users' },
    { label: 'Base de conhecimento', icon: 'pi pi-book' },
    { label: 'Analytics', icon: 'pi pi-chart-bar' },
  ];
}

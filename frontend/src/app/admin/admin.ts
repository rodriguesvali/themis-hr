import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { AvatarModule } from 'primeng/avatar';
import { CardModule } from 'primeng/card';
import { PanelModule } from 'primeng/panel';
import { DividerModule } from 'primeng/divider';
import { MessageModule } from 'primeng/message';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, ButtonModule, TagModule, AvatarModule, CardModule, PanelModule, DividerModule, MessageModule],
  templateUrl: './admin.html',
})
export class AdminComponent {
}

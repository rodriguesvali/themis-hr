import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from './chat.service';

// PrimeNG Modules
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { AvatarModule } from 'primeng/avatar';
import { InputGroupModule } from 'primeng/inputgroup';
import { InputGroupAddonModule } from 'primeng/inputgroupaddon';
import { MessageModule } from 'primeng/message';
import { ToolbarModule } from 'primeng/toolbar';
import { PanelModule } from 'primeng/panel';
import { CardModule } from 'primeng/card';
import { BadgeModule } from 'primeng/badge';
import { MarkdownPipe } from './markdown.pipe';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule,
    ButtonModule,
    InputTextModule,
    AvatarModule,
    InputGroupModule,
    InputGroupAddonModule,
    MessageModule,
    ToolbarModule,
    PanelModule,
    CardModule,
    BadgeModule,
    MarkdownPipe
  ],
  templateUrl: './chat.html',
  styleUrl: './app.scss'
})
export class ChatComponent {
  title = 'Themis HR';
  chatService = inject(ChatService);
  userInput = '';

  sendMessage() {
    if (this.userInput.trim()) {
      this.chatService.sendMessage(this.userInput);
      this.userInput = '';
    }
  }
}

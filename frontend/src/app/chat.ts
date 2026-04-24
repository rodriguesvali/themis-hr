import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from './chat.service';

// PrimeNG Modules
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { AvatarModule } from 'primeng/avatar';
import { ToolbarModule } from 'primeng/toolbar';
import { BadgeModule } from 'primeng/badge';
import { ScrollPanelModule } from 'primeng/scrollpanel';
import { InputGroupModule } from 'primeng/inputgroup';
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
    ToolbarModule,
    BadgeModule,
    ScrollPanelModule,
    InputGroupModule,
    MarkdownPipe
  ],
  templateUrl: './chat.html',
  styleUrl: './chat.css'
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

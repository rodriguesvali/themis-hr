import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface ChatMessage {
    role: 'user' | 'themis' | 'human_agent';
    content: string;
    sentiment?: string;
    created_at?: Date;
}

export interface ChatResponse {
    conversation_id: number;
    reply: string;
    status: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = `${environment.apiUrl}/api/v1/conversations`;

  // Gerenciamento de estado reativo
  public messages = signal<ChatMessage[]>([]);
  public isTyping = signal<boolean>(false);
  
  // No MVP sem Auth, criaremos um ID randomico pseudo-anônimo
  private userId = `user_${Math.floor(Math.random() * 1000)}`;

  constructor(private http: HttpClient) {}

  sendMessage(message: string): void {
    if (!message.trim()) return;

    // Atualizar UI instantaneamente
    const userMsg: ChatMessage = { role: 'user', content: message, created_at: new Date() };
    this.messages.update(msgs => [...msgs, userMsg]);
    this.isTyping.set(true);

    this.http.post<ChatResponse>(this.apiUrl, { user_id: this.userId, message })
        .subscribe({
            next: (res) => {
                const botMsg: ChatMessage = { role: 'themis', content: res.reply, created_at: new Date() };
                this.messages.update(msgs => [...msgs, botMsg]);
                this.isTyping.set(false);
            },
            error: (err) => {
                console.error('Failed to send message', err);
                const errorMsg: ChatMessage = { role: 'themis', content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde.' };
                this.messages.update(msgs => [...msgs, errorMsg]);
                this.isTyping.set(false);
            }
        });
  }
}

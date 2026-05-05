import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { environment } from '../environments/environment';
import { ChatService } from './chat.service';

describe('ChatService', () => {
  let service: ChatService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ChatService,
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(ChatService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('renders a readable fallback and clears typing state when the backend fails', () => {
    service.sendMessage('Qual o prazo para marcar ferias?');

    expect(service.isTyping()).toBe(true);

    const req = httpMock.expectOne(`${environment.apiUrl}/api/v1/conversations`);
    expect(req.request.method).toBe('POST');

    req.flush({ detail: 'backend indisponivel' }, { status: 503, statusText: 'Service Unavailable' });

    const messages = service.messages();
    expect(service.isTyping()).toBe(false);
    expect(messages).toHaveLength(2);
    expect(messages[0].role).toBe('user');
    expect(messages[1]).toEqual({
      role: 'themis',
      content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde.',
    });
  });
});

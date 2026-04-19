import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { parse } from 'marked';

@Pipe({
  name: 'markdown',
  standalone: true
})
export class MarkdownPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    if (!value) return '';
    // Usamos await Promise nativamente do pacote 'marked' mas o pipe é síncrono.
    // Como a biblioteca mudou para promise based em configs complexas, parse direto aceita sincrono em textos simples.
    const html = parse(value, { async: false }) as string;
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}

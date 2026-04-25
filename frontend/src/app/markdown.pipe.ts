import { Pipe, PipeTransform } from '@angular/core';
import { parse } from 'marked';

@Pipe({
  name: 'markdown',
  standalone: true
})
export class MarkdownPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return '';
    // Usamos await Promise nativamente do pacote 'marked' mas o pipe é síncrono.
    // Como a biblioteca mudou para promise based em configs complexas, parse direto aceita sincrono em textos simples.
    return parse(value, { async: false }) as string;
  }
}

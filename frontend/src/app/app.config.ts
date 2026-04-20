import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';

import { providePrimeNG } from 'primeng/config';
import Nora from '@primeuix/themes/nora';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes),
    provideHttpClient(),
    providePrimeNG({
        theme: {
            preset: Nora,
            options: {
                cssLayer: {
                    name: 'primeng',
                    order: 'theme, base, primeng, components, utilities'
                },
                darkModeSelector: false
            }
        }
    })
  ]
};

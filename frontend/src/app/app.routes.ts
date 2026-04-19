import { Routes } from '@angular/router';
import { ChatComponent } from './chat';
import { AdminComponent } from './admin/admin';

export const routes: Routes = [
    { path: '', component: ChatComponent },
    { path: 'admin', component: AdminComponent }
];

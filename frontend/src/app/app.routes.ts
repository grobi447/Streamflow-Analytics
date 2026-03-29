import { Routes } from '@angular/router';
import { authGuard, publicGuard } from './views/auth/auth.guard';

export const routes: Routes = [
    {
        path: 'login',
        canActivate: [publicGuard],
        loadComponent: () =>
            import('./views/auth/login/login').then(m => m.Login)
    },
    {
        path: 'register',
        canActivate: [publicGuard],
        loadComponent: () =>
            import('./views/auth/register/register').then(m => m.Register)
    },
    {
        path: 'app',
        canActivate: [authGuard],
        loadComponent: () =>
            import('./layout/main-layout/main-layout').then(m => m.MainLayout),
        children: [
            {
                path: 'dashboard',
                loadComponent: () =>
                    import('./views/dashboard/dashboard').then(m => m.Dashboard)
            },
            { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
        ]
    },
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: '**', redirectTo: '/login' }
];
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AUTH_CONSTANTS } from './auth.constants';
import { LoginRequest, TokenResponse, User } from './auth.types';

@Injectable({ providedIn: 'root' })
export class AuthService {
    private readonly apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    login(credentials: LoginRequest): Observable<TokenResponse> {
        return this.http.post<TokenResponse>(
            `${this.apiUrl}${AUTH_CONSTANTS.LOGIN_ENDPOINT}`,
            credentials
        ).pipe(
            tap(response => {
                localStorage.setItem(AUTH_CONSTANTS.TOKEN_KEY, response.access_token);
                localStorage.setItem(AUTH_CONSTANTS.USER_KEY, JSON.stringify(response.user));
            })
        );
    }

    logout(): void {
        localStorage.removeItem(AUTH_CONSTANTS.TOKEN_KEY);
        localStorage.removeItem(AUTH_CONSTANTS.USER_KEY);
    }

    getToken(): string | null {
        return localStorage.getItem(AUTH_CONSTANTS.TOKEN_KEY);
    }

    getUser(): User | null {
        const user = localStorage.getItem(AUTH_CONSTANTS.USER_KEY);
        return user ? JSON.parse(user) : null;
    }

    isLoggedIn(): boolean {
        return !!this.getToken();
    }

    register(userData: any): Observable<any> {
        return this.http.post(
            `${this.apiUrl}${AUTH_CONSTANTS.REGISTER_ENDPOINT}`,
            userData
        );
    }
}
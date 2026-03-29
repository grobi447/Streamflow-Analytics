export interface LoginRequest {
    username: string;
    password: string;
}

export interface User {
    user_id: string;
    username: string;
    email: string;
    role: 'ADMIN' | 'VIEWER';
    created_at: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
    expires_in: number;
    user: User;
}
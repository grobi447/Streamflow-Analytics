import { HttpInterceptorFn } from '@angular/common/http';
import { AUTH_CONSTANTS } from '../../views/auth/auth.constants';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
    const token = localStorage.getItem(AUTH_CONSTANTS.TOKEN_KEY);

    if (token) {
        const authReq = req.clone({
            headers: req.headers.set('Authorization', `Bearer ${token}`)
        });
        return next(authReq);
    }

    return next(req);
};
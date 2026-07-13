// ===========================================
// FILMERSHUB - AUTH API
// ===========================================

import api from './client';
import { LoginCredentials, RegisterData, AuthTokens, User } from '@/types';

export const authApi = {
  login: async (credentials: LoginCredentials) => {
    const response = await api.post<{ access: string; refresh: string; user: User }>(
      '/auth/login/',
      credentials
    );
    return response.data;
  },

  register: async (data: RegisterData) => {
    const response = await api.post<{ user: User; tokens: AuthTokens }>(
      '/auth/register/',
      data
    );
    return response.data;
  },

  logout: async (refreshToken: string) => {
    await api.post('/auth/logout/', { refresh: refreshToken });
  },

  changePassword: async (oldPassword: string, newPassword: string) => {
    await api.put('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPassword,
    });
  },
};

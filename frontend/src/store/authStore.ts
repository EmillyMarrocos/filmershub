// ===========================================
// FILMERSHUB - AUTH STORE (Zustand)
// ===========================================

import { create } from 'zustand';
import { User, RegisterData } from '@/types';
import { authApi } from '@/api/auth';
import api from '@/api/client';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (email, password) => {
    const data = await authApi.login({ email, password });
    localStorage.setItem('tokens', JSON.stringify({
      access: data.access,
      refresh: data.refresh,
    }));
    set({ user: data.user, isAuthenticated: true });
  },

  register: async (registerData) => {
    localStorage.removeItem('tokens');
    set({ user: null, isAuthenticated: false });
    const data = await authApi.register(registerData);
    localStorage.setItem('tokens', JSON.stringify(data.tokens));
    set({ user: data.user, isAuthenticated: true });
  },

  logout: async () => {
    try {
      const tokens = localStorage.getItem('tokens');
      if (tokens) {
        const { refresh } = JSON.parse(tokens);
        await authApi.logout(refresh);
      }
    } catch {
      // Silently continue even if server call fails
    }
    localStorage.removeItem('tokens');
    set({ user: null, isAuthenticated: false });
  },

  loadUser: async () => {
    try {
      const tokens = localStorage.getItem('tokens');
      if (!tokens) {
        set({ isLoading: false });
        return;
      }

      const { access } = JSON.parse(tokens);
      if (!access) {
        set({ isLoading: false });
        return;
      }

      const response = await api.get('/profile/');
      const user = response.data;
      set({ user, isAuthenticated: true, isLoading: false });
    } catch {
      localStorage.removeItem('tokens');
      set({ isLoading: false });
    }
  },

  setUser: (user) => set({ user }),
}));

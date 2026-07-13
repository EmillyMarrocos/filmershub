// ===========================================
// FILMERSHUB - HEADER
// ===========================================

import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import api from '@/api/client';

interface HeaderProps {
  onMenuClick?: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchUnread = async () => {
      try {
        const response = await api.get('/notifications/unread-count/');
        setUnreadCount(response.data.unread_count);
      } catch {
        // Silently fail
      }
    };

    fetchUnread();
    const interval = setInterval(fetchUnread, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setShowDropdown(false);
      }
    };
    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showDropdown]);

  const handleLogout = async () => {
    setShowDropdown(false);
    await logout();
    navigate('/login');
  };

  return (
    <header className="h-16 bg-obsidian border-b border-slate/50 flex items-center justify-between px-4 md:px-6">
      <div className="flex items-center gap-3">
        {/* Hamburger (mobile) */}
        <button
          onClick={onMenuClick}
          className="p-2 rounded-lg hover:bg-slate/50 transition-all md:hidden"
        >
          <svg className="w-5 h-5 text-snow" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        {/* Logo + Home */}
        <Link to="/" className="flex items-center gap-2 flex-shrink-0">
          <div className="w-8 h-8 bg-iris rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">F</span>
          </div>
          <span className="text-lg font-bold text-snow hidden sm:block">
            Filmers<span className="text-iris">Hub</span>
          </span>
        </Link>
      </div>

      {/* Search */}
      <div className="flex-1 max-w-md mx-4 hidden sm:block">
        <input
          type="text"
          placeholder="Buscar videomakers, trabalhos..."
          className="w-full bg-graphite border border-slate/50 rounded-lg px-4 py-2 text-sm text-snow placeholder-muted focus:outline-none focus:border-iris"
        />
      </div>

      {/* Right side */}
      <div className="flex items-center gap-2 md:gap-4">
        {/* Notifications */}
        <Link
          to="/notifications"
          className="relative p-2 rounded-lg hover:bg-slate/50 transition-all"
        >
          <span className="text-xl">🔔</span>
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-crimson rounded-full text-white text-xs flex items-center justify-center">
              {unreadCount > 9 ? '9+' : unreadCount}
            </span>
          )}
        </Link>

        {/* User dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="flex items-center gap-2 p-2 rounded-lg hover:bg-slate/50 transition-all"
          >
            <div className="w-8 h-8 bg-slate rounded-full flex items-center justify-center overflow-hidden">
              {user?.avatar_url ? (
                <img
                  src={user.avatar_url}
                  alt={user.full_name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <span className="text-iris font-bold text-sm">
                  {user?.first_name?.[0] || 'U'}
                </span>
              )}
            </div>
            <span className="text-sm text-snow hidden sm:block">
              {user?.first_name}
            </span>
          </button>

          {/* Dropdown */}
          {showDropdown && (
            <div className="absolute right-0 mt-2 w-48 bg-graphite border border-slate/50 rounded-lg shadow-lg py-2 z-50">
              <Link
                to="/profile"
                className="block px-4 py-2 text-sm text-snow hover:bg-slate/50"
                onClick={() => setShowDropdown(false)}
              >
                Meu Perfil
              </Link>
              <hr className="border-slate/50 my-2" />
              <button
                onClick={handleLogout}
                className="block w-full text-left px-4 py-2 text-sm text-crimson hover:bg-slate/50"
              >
                Sair
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

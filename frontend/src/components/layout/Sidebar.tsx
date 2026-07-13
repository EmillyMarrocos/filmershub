// ===========================================
// FILMERSHUB - SIDEBAR
// ===========================================

import { Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';

const allNavItems = [
  { name: 'Feed', href: '/feed', icon: '🏠', for: 'all' as const },
  { name: 'Portfólio', href: '/portfolio', icon: '🎬', for: 'videomaker' as const },
  { name: 'Explorar', href: '/explore', icon: '🔍', for: 'client' as const },
  { name: 'Chat', href: '/chat', icon: '💬', for: 'all' as const },
  { name: 'Agenda', href: '/schedule', icon: '📅', for: 'videomaker' as const },
  { name: 'Contratos', href: '/contracts', icon: '📄', for: 'videomaker' as const },
];

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const location = useLocation();
  const { user } = useAuthStore();

  const navigation = allNavItems.filter((item) => {
    if (item.for === 'all') return true;
    if (item.for === 'videomaker') return user?.is_videomaker;
    if (item.for === 'client') return user?.is_client;
    return false;
  });

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed left-0 top-0 h-full w-64 bg-obsidian border-r border-slate/50 flex flex-col z-50 transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } md:translate-x-0`}
      >
        {/* Logo */}
        <div className="p-6 border-b border-slate/50 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3" onClick={onClose}>
            <div className="w-10 h-10 bg-iris rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">F</span>
            </div>
            <span className="text-xl font-bold text-snow">
              Filmers<span className="text-iris">Hub</span>
            </span>
          </Link>
          <button onClick={onClose} className="text-muted hover:text-snow md:hidden">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={onClose}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-iris/20 text-iris'
                    : 'text-muted hover:bg-slate/50 hover:text-snow'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span className="font-medium">{item.name}</span>
              </Link>
            );
          })}

          {/* Profile badge */}
          {user && (
            <div className="mt-4 px-4 py-2 rounded-lg bg-graphite/50 border border-slate/30">
              <p className="text-xs text-muted mb-1">Tipo de conta</p>
              <p className="text-sm font-medium text-snow">
                {user.profile_type === 'videomaker' && '🎬 Videomaker'}
                {user.profile_type === 'client' && '💼 Cliente'}
                {user.profile_type === 'both' && '🤝 Videomaker & Cliente'}
              </p>
            </div>
          )}
        </nav>

        {/* User info */}
        {user && (
          <div className="p-4 border-t border-slate/50">
            <Link
              to="/profile"
              onClick={onClose}
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate/50 transition-all"
            >
              <div className="w-10 h-10 bg-slate rounded-full flex items-center justify-center overflow-hidden">
                {user.avatar_url ? (
                  <img
                    src={user.avatar_url}
                    alt={user.full_name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-iris font-bold">
                    {user.first_name?.[0] || 'U'}
                  </span>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-snow truncate">
                  {user.full_name}
                </p>
                <p className="text-xs text-muted truncate">{user.email}</p>
              </div>
            </Link>
          </div>
        )}
      </aside>
    </>
  );
}

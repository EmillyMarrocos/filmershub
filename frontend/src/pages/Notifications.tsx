// ===========================================
// FILMERSHUB - NOTIFICATIONS PAGE
// ===========================================

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '@/api/client';
import { Notification } from '@/types';
import toast from 'react-hot-toast';

export default function Notifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await api.get('/notifications/');
      setNotifications(response.data.results || response.data);
    } catch (error) {
      toast.error('Erro ao carregar notificações');
    } finally {
      setIsLoading(false);
    }
  };

  const markAsRead = async (id: string) => {
    try {
      await api.post(`/notifications/${id}/read/`);
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch (error) {
      // Silently fail
    }
  };

  const markAllAsRead = async () => {
    try {
      await api.post('/notifications/read-all/');
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      toast.success('Todas marcadas como lidas');
    } catch (error) {
      toast.error('Erro ao marcar notificações');
    }
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'like': return '❤️';
      case 'comment': return '💬';
      case 'follow': return '👤';
      case 'contract': return '📄';
      case 'payment': return '💰';
      case 'booking': return '📅';
      case 'message': return '✉️';
      default: return '🔔';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-iris"></div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-snow">Notificações</h1>
        {notifications.some((n) => !n.is_read) && (
          <button onClick={markAllAsRead} className="text-sm text-iris hover:text-iris/80">
            Marcar todas como lidas
          </button>
        )}
      </div>

      <div className="space-y-2">
        {notifications.map((notification) => (
          <div
            key={notification.id}
            onClick={() => !notification.is_read && markAsRead(notification.id)}
            className={`card flex items-start gap-4 cursor-pointer transition-all hover:border-iris/30 ${
              !notification.is_read ? 'border-iris/20 bg-iris/5' : ''
            }`}
          >
            <span className="text-2xl mt-1">{getIcon(notification.notification_type)}</span>
            <div className="flex-1 min-w-0">
              <p className={`font-medium ${!notification.is_read ? 'text-snow' : 'text-muted'}`}>
                {notification.title}
              </p>
              <p className="text-sm text-muted mt-0.5">{notification.message}</p>
              <p className="text-xs text-muted/60 mt-1">
                {new Date(notification.created_at).toLocaleString('pt-BR')}
              </p>
            </div>
            {!notification.is_read && (
              <div className="w-2 h-2 bg-iris rounded-full mt-2 flex-shrink-0" />
            )}
            {notification.link && (
              <Link
                to={notification.link}
                className="text-xs text-iris hover:text-iris/80 flex-shrink-0 mt-2"
              >
                Ver →
              </Link>
            )}
          </div>
        ))}
      </div>

      {notifications.length === 0 && (
        <div className="text-center py-12">
          <span className="text-4xl">🔔</span>
          <p className="text-muted mt-4">Nenhuma notificação ainda.</p>
        </div>
      )}
    </div>
  );
}

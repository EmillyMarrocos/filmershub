// ===========================================
// FILMERSHUB - CHAT PAGE
// ===========================================

import { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useLocation } from 'react-router-dom';
import api from '@/api/client';
import { ChatRoom, Message } from '@/types';
import toast from 'react-hot-toast';

export default function Chat() {
  const { user } = useAuthStore();
  const location = useLocation();
  const [rooms, setRooms] = useState<ChatRoom[]>([]);
  const [selectedRoom, setSelectedRoom] = useState<ChatRoom | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [showNewChat, setShowNewChat] = useState(false);
  const [searchEmail, setSearchEmail] = useState('');
  const [searching, setSearching] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const pendingRoomId = (location.state as any)?.roomId as string | undefined;

  useEffect(() => {
    fetchRooms();
  }, []);

  useEffect(() => {
    if (selectedRoom) {
      fetchMessages(selectedRoom.id);
      markAsRead(selectedRoom.id);
    }
  }, [selectedRoom]);

  const markAsRead = async (roomId: string) => {
    try {
      await api.post(`/chat/rooms/${roomId}/read/`);
      setRooms((prev) =>
        prev.map((r) => (r.id === roomId ? { ...r, unread_count: 0 } : r))
      );
    } catch {
      // silent
    }
  };

  const fetchRooms = async () => {
    try {
      const response = await api.get('/chat/rooms/');
      const data = response.data.results || response.data;
      setRooms(data);
      if (pendingRoomId) {
        const target = data.find((r: ChatRoom) => r.id === pendingRoomId);
        if (target) setSelectedRoom(target);
      }
    } catch (error) {
      toast.error('Erro ao carregar conversas');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchMessages = async (roomId: string) => {
    try {
      const response = await api.get(`/chat/rooms/${roomId}/messages/`);
      setMessages(response.data.results || response.data);
    } catch (error) {
      toast.error('Erro ao carregar mensagens');
    }
  };

  const handleNewChat = async () => {
    if (!searchEmail.trim()) {
      toast.error('Digite um email');
      return;
    }
    setSearching(true);
    try {
      const lookupRes = await api.get(`/users/lookup/?email=${encodeURIComponent(searchEmail)}`);
      const foundUser = lookupRes.data;

      if (!foundUser || !foundUser.id) {
        toast.error('Usuário não encontrado');
        return;
      }

      const roomRes = await api.post('/chat/rooms/create/', { user_id: foundUser.id });
      toast.success('Conversa criada!');
      setShowNewChat(false);
      setSearchEmail('');
      fetchRooms();
      if (roomRes.data) setSelectedRoom(roomRes.data);
    } catch (error: any) {
      if (error.response?.status === 404) {
        toast.error('Usuário não encontrado');
      } else {
        toast.error('Erro ao criar conversa');
      }
    } finally {
      setSearching(false);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedRoom) return;

    try {
      await api.post(`/chat/rooms/${selectedRoom.id}/messages/send/`, {
        content: newMessage,
        message_type: 'text',
      });
      setNewMessage('');
      fetchMessages(selectedRoom.id);
    } catch (error) {
      toast.error('Erro ao enviar mensagem');
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-iris"></div>
      </div>
    );
  }

  return (
    <div className="flex h-[calc(100vh-8rem)] bg-obsidian rounded-xl overflow-hidden">
      {/* Rooms list */}
      <div className="w-80 border-r border-slate/50 flex flex-col">
        <div className="p-4 border-b border-slate/50 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-snow">Conversas</h2>
          <button
            onClick={() => setShowNewChat(true)}
            className="w-8 h-8 bg-iris rounded-lg flex items-center justify-center text-white font-bold hover:bg-iris/80 transition-colors"
            title="Nova conversa"
          >
            +
          </button>
        </div>
        <div className="flex-1 overflow-auto">
          {rooms.map((room) => (
            <button
              key={room.id}
              onClick={() => setSelectedRoom(room)}
              className={`w-full p-4 flex items-center gap-3 hover:bg-slate/30 transition-all text-left ${
                selectedRoom?.id === room.id ? 'bg-slate/50' : ''
              }`}
            >
              <div className="w-12 h-12 bg-slate rounded-full flex items-center justify-center flex-shrink-0">
                {room.other_user?.avatar ? (
                  <img src={room.other_user.avatar} alt="" className="w-full h-full rounded-full object-cover" />
                ) : (
                  <span className="text-iris font-bold">
                    {room.other_user?.name?.[0] || '?'}
                  </span>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-snow truncate">{room.other_user?.name || 'Sala'}</p>
                <p className="text-sm text-muted truncate">{room.last_message_content || 'Nenhuma mensagem'}</p>
              </div>
              {room.unread_count > 0 && (
                <span className="w-5 h-5 bg-iris rounded-full text-white text-xs flex items-center justify-center flex-shrink-0">
                  {room.unread_count}
                </span>
              )}
            </button>
          ))}
          {rooms.length === 0 && (
            <p className="p-4 text-muted text-center">Nenhuma conversa ainda.</p>
          )}
        </div>
      </div>

      {/* Messages area */}
      {selectedRoom ? (
        <div className="flex-1 flex flex-col">
          <div className="p-4 border-b border-slate/50 flex items-center gap-3">
            <div className="w-10 h-10 bg-slate rounded-full flex items-center justify-center">
              {selectedRoom.other_user?.avatar ? (
                <img src={selectedRoom.other_user.avatar} alt="" className="w-full h-full rounded-full object-cover" />
              ) : (
                <span className="text-iris font-bold">{selectedRoom.other_user?.name?.[0]}</span>
              )}
            </div>
            <div>
              <p className="font-medium text-snow">{selectedRoom.other_user?.name}</p>
            </div>
          </div>

          <div className="flex-1 overflow-auto p-4 space-y-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.sender === user?.id ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                    msg.sender === user?.id
                      ? 'bg-iris text-white'
                      : 'bg-slate text-snow'
                  }`}
                >
                  <p>{msg.content}</p>
                  <p className="text-xs opacity-70 mt-1">
                    {new Date(msg.created_at).toLocaleTimeString('pt-BR', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-4 border-t border-slate/50">
            <div className="flex gap-2">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Digite sua mensagem..."
                className="flex-1 input"
              />
              <button
                onClick={handleSendMessage}
                disabled={!newMessage.trim()}
                className="btn-primary disabled:opacity-50"
              >
                Enviar
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center text-muted">
          <p>Selecione uma conversa para começar.</p>
        </div>
      )}

      {/* New Chat Modal */}
      {showNewChat && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-md">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-snow">Nova Conversa</h2>
                <button onClick={() => { setShowNewChat(false); setSearchEmail(''); }} className="text-muted hover:text-snow text-2xl">&times;</button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Email do usuário</label>
                  <input
                    className="input"
                    type="email"
                    placeholder="usuario@email.com"
                    value={searchEmail}
                    onChange={(e) => setSearchEmail(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleNewChat()}
                  />
                  <p className="mt-1 text-xs text-muted">
                    Digite o email do usuário com quem deseja conversar.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 mt-6">
                <button
                  onClick={() => { setShowNewChat(false); setSearchEmail(''); }}
                  className="flex-1 btn-secondary py-3"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleNewChat}
                  disabled={searching || !searchEmail.trim()}
                  className="flex-1 btn-primary py-3 disabled:opacity-50"
                >
                  {searching ? 'Buscando...' : 'Iniciar Conversa'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ===========================================
// FILMERSHUB - SCHEDULE PAGE
// ===========================================

import { useState, useEffect } from 'react';
import api from '@/api/client';
import { Event } from '@/types';
import toast from 'react-hot-toast';

export default function Schedule() {
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [view, setView] = useState<'list' | 'calendar'>('list');
  const [showModal, setShowModal] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    event_type: 'wedding',
    client_email: '',
    start_datetime: '',
    end_datetime: '',
    location: '',
    address: '',
    total_price: '',
    notes: '',
  });

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await api.get('/scheduling/events/');
      setEvents(response.data.results || response.data);
    } catch (error) {
      toast.error('Erro ao carregar eventos');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!formData.title.trim()) {
      toast.error('Título é obrigatório');
      return;
    }
    if (!formData.start_datetime || !formData.end_datetime) {
      toast.error('Datas são obrigatórias');
      return;
    }
    setIsSubmitting(true);
    try {
      const payload = {
        ...formData,
        total_price: formData.total_price ? parseFloat(formData.total_price) : null,
      };
      await api.post('/scheduling/events/create/', payload);
      toast.success('Evento criado com sucesso!');
      setShowModal(false);
      setFormData({
        title: '', description: '', event_type: 'wedding', client_email: '',
        start_datetime: '', end_datetime: '', location: '', address: '',
        total_price: '', notes: '',
      });
      fetchEvents();
    } catch (error: any) {
      const data = error.response?.data;
      if (data) {
        const msg = Object.entries(data).map(([k, v]: [string, any]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ');
        toast.error(msg);
      } else {
        toast.error('Erro ao criar evento');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed': return 'badge-jade';
      case 'pending': return 'badge-amber';
      case 'cancelled': return 'badge-crimson';
      case 'completed': return 'badge-iris';
      default: return 'badge';
    }
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      pending: 'Pendente',
      confirmed: 'Confirmado',
      in_progress: 'Em Andamento',
      completed: 'Concluído',
      cancelled: 'Cancelado',
    };
    return labels[status] || status;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-iris"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-snow">Agenda</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setView('list')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              view === 'list' ? 'bg-iris text-white' : 'bg-slate/50 text-muted'
            }`}
          >
            Lista
          </button>
          <button
            onClick={() => setView('calendar')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              view === 'calendar' ? 'bg-iris text-white' : 'bg-slate/50 text-muted'
            }`}
          >
            Calendário
          </button>
          <button onClick={() => setShowModal(true)} className="btn-primary">+ Novo Evento</button>
        </div>
      </div>

      {/* Events list */}
      {view === 'list' && (
        <div className="space-y-4">
          {events.map((event) => (
            <div key={event.id} className="card flex items-center gap-4">
              <div className="w-16 h-16 bg-iris/20 rounded-lg flex flex-col items-center justify-center flex-shrink-0">
                <span className="text-2xl font-bold text-iris">
                  {new Date(event.start_datetime).getDate()}
                </span>
                <span className="text-xs text-iris">
                  {new Date(event.start_datetime).toLocaleDateString('pt-BR', { month: 'short' })}
                </span>
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-snow">{event.title}</h3>
                <p className="text-sm text-muted">
                  {event.videomaker_name} • {event.client_name}
                </p>
                <p className="text-sm text-muted">
                  📍 {event.location || 'A definir'}
                </p>
              </div>
              <span className={`badge ${getStatusColor(event.status)}`}>
                {getStatusLabel(event.status)}
              </span>
              {event.total_price && (
                <div className="text-right">
                  <p className="text-lg font-bold text-jade">
                    R$ {Number(event.total_price).toFixed(2)}
                  </p>
                </div>
              )}
            </div>
          ))}

          {events.length === 0 && (
            <div className="text-center py-12">
              <p className="text-muted mb-4">Nenhum evento agendado.</p>
              <button onClick={() => setShowModal(true)} className="btn-primary">
                + Criar primeiro evento
              </button>
            </div>
          )}
        </div>
      )}

      {/* Calendar view placeholder */}
      {view === 'calendar' && (
        <div className="card text-center py-12">
          <p className="text-muted">Visualização em calendário em breve.</p>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-lg max-h-[90vh] overflow-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-snow">Novo Evento</h2>
                <button onClick={() => setShowModal(false)} className="text-muted hover:text-snow text-2xl">&times;</button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Título *</label>
                  <input
                    className="input"
                    placeholder="Ex: Casamento Maria & João"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Descrição</label>
                  <textarea
                    className="input min-h-[80px]"
                    placeholder="Descreva o evento..."
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Email do Cliente</label>
                  <input
                    className="input"
                    type="email"
                    placeholder="email@cliente.com (opcional)"
                    value={formData.client_email}
                    onChange={(e) => setFormData({ ...formData, client_email: e.target.value })}
                  />
                  <p className="mt-1 text-xs text-muted">Se vazio, o evento será criado para você mesmo.</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Tipo</label>
                    <select
                      className="input"
                      value={formData.event_type}
                      onChange={(e) => setFormData({ ...formData, event_type: e.target.value })}
                    >
                      <option value="wedding">Casamento</option>
                      <option value="corporate">Corporativo</option>
                      <option value="event">Evento</option>
                      <option value="music_video">Clipe Musical</option>
                      <option value="documentary">Documentário</option>
                      <option value="commercial">Comercial</option>
                      <option value="social_media">Redes Sociais</option>
                      <option value="other">Outro</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Preço (R$)</label>
                    <input
                      className="input"
                      type="number"
                      placeholder="0.00"
                      value={formData.total_price}
                      onChange={(e) => setFormData({ ...formData, total_price: e.target.value })}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Início *</label>
                    <input
                      className="input"
                      type="datetime-local"
                      value={formData.start_datetime}
                      onChange={(e) => setFormData({ ...formData, start_datetime: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Fim *</label>
                    <input
                      className="input"
                      type="datetime-local"
                      value={formData.end_datetime}
                      onChange={(e) => setFormData({ ...formData, end_datetime: e.target.value })}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Local</label>
                  <input
                    className="input"
                    placeholder="Ex: Salão de Festas, São Paulo"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Endereço</label>
                  <input
                    className="input"
                    placeholder="Endereço completo"
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Observações</label>
                  <textarea
                    className="input min-h-[60px]"
                    placeholder="Notas adicionais..."
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  />
                </div>
              </div>

              <div className="flex gap-4 mt-6">
                <button onClick={() => setShowModal(false)} className="flex-1 btn-secondary py-3">
                  Cancelar
                </button>
                <button
                  onClick={handleCreate}
                  disabled={isSubmitting}
                  className="flex-1 btn-primary py-3 disabled:opacity-50"
                >
                  {isSubmitting ? 'Criando...' : 'Criar Evento'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ===========================================
// FILMERSHUB - CONTRACTS PAGE
// ===========================================

import { useState, useEffect } from 'react';
import api from '@/api/client';
import { Contract } from '@/types';
import toast from 'react-hot-toast';

export default function Contracts() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    client: '',
    service_type: 'wedding',
    service_description: '',
    event_date: '',
    delivery_date: '',
    location: '',
    total_value: '',
    payment_method: 'pix',
    additional_clauses: '',
  });

  useEffect(() => {
    fetchContracts();
  }, []);

  const fetchContracts = async () => {
    try {
      const response = await api.get('/contracts/');
      setContracts(response.data.results || response.data);
    } catch (error) {
      toast.error('Erro ao carregar contratos');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!formData.client.trim()) {
      toast.error('Informe o email do cliente');
      return;
    }
    if (!formData.service_description.trim()) {
      toast.error('Descrição do serviço é obrigatória');
      return;
    }
    if (!formData.event_date || !formData.delivery_date) {
      toast.error('Datas são obrigatórias');
      return;
    }
    if (!formData.total_value || parseFloat(formData.total_value) <= 0) {
      toast.error('Informe o valor total');
      return;
    }

    setIsSubmitting(true);
    try {
      // First resolve client ID from email
      let clientId = formData.client;
      try {
        const searchRes = await api.get(`/users/lookup/?email=${encodeURIComponent(formData.client)}`);
        if (searchRes.data?.id) {
          clientId = searchRes.data.id;
        } else {
          throw new Error('not found');
        }
      } catch {
        // Try direct UUID
        try {
          await api.get(`/users/${formData.client}/`);
          clientId = formData.client;
        } catch {
          toast.error('Cliente não encontrado. Use o email exato.');
          setIsSubmitting(false);
          return;
        }
      }

      const payload = {
        ...formData,
        client: clientId,
        total_value: parseFloat(formData.total_value),
      };
      await api.post('/contracts/create/', payload);
      toast.success('Contrato criado com sucesso!');
      setShowModal(false);
      setFormData({
        client: '', service_type: 'wedding', service_description: '',
        event_date: '', delivery_date: '', location: '',
        total_value: '', payment_method: 'pix', additional_clauses: '',
      });
      fetchContracts();
    } catch (error: any) {
      const data = error.response?.data;
      if (data) {
        const msg = Object.entries(data).map(([k, v]: [string, any]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ');
        toast.error(msg);
      } else {
        toast.error('Erro ao criar contrato');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSign = async (contractId: string) => {
    try {
      await api.post(`/contracts/${contractId}/sign/`);
      toast.success('Contrato assinado!');
      fetchContracts();
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Erro ao assinar contrato';
      toast.error(msg);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'signed': return 'badge-jade';
      case 'pending_signature': return 'badge-amber';
      case 'draft': return 'badge';
      case 'cancelled': return 'badge-crimson';
      default: return 'badge-iris';
    }
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      draft: 'Rascunho',
      pending_signature: 'Aguardando Assinatura',
      signed: 'Assinado',
      in_progress: 'Em Andamento',
      completed: 'Concluído',
      cancelled: 'Cancelado',
      expired: 'Expirado',
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
        <h1 className="text-2xl font-bold text-snow">Contratos</h1>
        <button onClick={() => setShowModal(true)} className="btn-primary">+ Novo Contrato</button>
      </div>

      {/* Contracts list */}
      <div className="space-y-4">
        {contracts.map((contract) => (
          <div key={contract.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="font-mono text-iris font-bold">
                    {contract.contract_number}
                  </span>
                  <span className={`badge ${getStatusColor(contract.status)}`}>
                    {getStatusLabel(contract.status)}
                  </span>
                </div>

                <h3 className="text-lg font-semibold text-snow mb-1">
                  {contract.service_type}
                </h3>

                <p className="text-sm text-muted mb-3">
                  {contract.client_name} ↔ {contract.videomaker_name}
                </p>

                <div className="flex items-center gap-4 text-sm text-muted">
                  {contract.event_date && <span>📅 {new Date(contract.event_date).toLocaleDateString('pt-BR')}</span>}
                  {contract.delivery_date && <span>📦 Entrega: {new Date(contract.delivery_date).toLocaleDateString('pt-BR')}</span>}
                  {contract.location && <span>📍 {contract.location}</span>}
                </div>
              </div>

              <div className="text-right">
                {contract.total_value && (
                  <p className="text-2xl font-bold text-jade mb-2">
                    R$ {Number(contract.total_value).toFixed(2)}
                  </p>
                )}

                <div className="flex items-center gap-2 mb-3">
                  <span className={`text-sm ${contract.client_signed ? 'text-jade' : 'text-muted'}`}>
                    {contract.client_signed ? '✓ Cliente assinou' : '○ Cliente pendente'}
                  </span>
                  <span className={`text-sm ${contract.videomaker_signed ? 'text-jade' : 'text-muted'}`}>
                    {contract.videomaker_signed ? '✓ Videomaker assinou' : '○ Videomaker pendente'}
                  </span>
                </div>

                <div className="flex gap-2 justify-end">
                  {contract.pdf_file && (
                    <a
                      href={contract.pdf_file}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-secondary text-sm"
                    >
                      📄 Ver PDF
                    </a>
                  )}
                  {contract.status === 'pending_signature' && (
                    <button
                      onClick={() => handleSign(contract.id)}
                      className="btn-primary text-sm"
                    >
                      ✍️ Assinar
                    </button>
                  )}
                </div>
              </div>
            </div>

            {contract.content_hash && (
              <div className="mt-4 pt-4 border-t border-slate/50">
                <p className="text-xs text-muted font-mono">
                  SHA-256: {contract.content_hash}
                </p>
              </div>
            )}
          </div>
        ))}

        {contracts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted mb-4">Nenhum contrato encontrado.</p>
            <button onClick={() => setShowModal(true)} className="btn-primary">
              + Criar primeiro contrato
            </button>
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-lg max-h-[90vh] overflow-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-snow">Novo Contrato</h2>
                <button onClick={() => setShowModal(false)} className="text-muted hover:text-snow text-2xl">&times;</button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Email do Cliente *</label>
                  <input
                    className="input"
                    type="email"
                    placeholder="cliente@email.com"
                    value={formData.client}
                    onChange={(e) => setFormData({ ...formData, client: e.target.value })}
                  />
                  <p className="mt-1 text-xs text-muted">Email do cliente que será parte do contrato.</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Tipo de Serviço</label>
                    <select
                      className="input"
                      value={formData.service_type}
                      onChange={(e) => setFormData({ ...formData, service_type: e.target.value })}
                    >
                      <option value="wedding">Casamento</option>
                      <option value="corporate">Corporativo</option>
                      <option value="event">Evento</option>
                      <option value="music_video">Clipe Musical</option>
                      <option value="commercial">Comercial</option>
                      <option value="social_media">Redes Sociais</option>
                      <option value="other">Outro</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Método de Pagamento</label>
                    <select
                      className="input"
                      value={formData.payment_method}
                      onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
                    >
                      <option value="pix">PIX</option>
                      <option value="credit_card">Cartão de Crédito</option>
                      <option value="boleto">Boleto</option>
                      <option value="bank_transfer">Transferência Bancária</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Descrição do Serviço *</label>
                  <textarea
                    className="input min-h-[80px]"
                    placeholder="Descreva detalhadamente o serviço a ser prestado..."
                    value={formData.service_description}
                    onChange={(e) => setFormData({ ...formData, service_description: e.target.value })}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Data do Evento *</label>
                    <input
                      className="input"
                      type="date"
                      value={formData.event_date}
                      onChange={(e) => setFormData({ ...formData, event_date: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Data de Entrega *</label>
                    <input
                      className="input"
                      type="date"
                      value={formData.delivery_date}
                      onChange={(e) => setFormData({ ...formData, delivery_date: e.target.value })}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Valor Total (R$) *</label>
                    <input
                      className="input"
                      type="number"
                      placeholder="0.00"
                      min="0"
                      step="0.01"
                      value={formData.total_value}
                      onChange={(e) => setFormData({ ...formData, total_value: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Local</label>
                    <input
                      className="input"
                      placeholder="São Paulo, SP"
                      value={formData.location}
                      onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Cláusulas Adicionais</label>
                  <textarea
                    className="input min-h-[80px]"
                    placeholder="Termos adicionais ao contrato..."
                    value={formData.additional_clauses}
                    onChange={(e) => setFormData({ ...formData, additional_clauses: e.target.value })}
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
                  {isSubmitting ? 'Criando...' : 'Criar Contrato'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

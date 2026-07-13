// ===========================================
// FILMERSHUB - PORTFOLIO PAGE
// ===========================================

import { useState, useEffect, useRef } from 'react';
import api from '@/api/client';
import { Work, Category } from '@/types';
import toast from 'react-hot-toast';

export default function Portfolio() {
  const [works, setWorks] = useState<Work[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingWork, setEditingWork] = useState<Work | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [openMenuId, setOpenMenuId] = useState<string | null>(null);
  const [deleteTargetId, setDeleteTargetId] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    work_type: 'video',
    external_url: '',
    client_name: '',
    location: '',
    equipment_used: '',
    status: 'published',
  });
  const [fileFile, setFileFile] = useState<File | null>(null);
  const [fileThumb, setFileThumb] = useState<File | null>(null);
  const [fileFilePreview, setFileFilePreview] = useState<string | null>(null);
  const [fileThumbPreview, setFileThumbPreview] = useState<string | null>(null);

  useEffect(() => {
    fetchWorks();
    fetchCategories();
  }, [selectedCategory]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpenMenuId(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (showCreateModal) { setShowCreateModal(false); resetForm(); }
        if (showEditModal) { setShowEditModal(false); setEditingWork(null); resetForm(); }
        if (deleteTargetId) setDeleteTargetId(null);
      }
    };
    if (showCreateModal || showEditModal || deleteTargetId) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [showCreateModal, showEditModal, deleteTargetId]);

  const fetchWorks = async () => {
    try {
      const params = selectedCategory ? `?category=${selectedCategory}` : '';
      const response = await api.get(`/portfolio/works/${params}`);
      setWorks(response.data.results || response.data);
    } catch (error) {
      toast.error('Erro ao carregar trabalhos');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get('/portfolio/categories/');
      setCategories(response.data.results || response.data);
    } catch (error) {
      // Silently fail
    }
  };

  const resetForm = () => {
    setFormData({
      title: '', description: '', work_type: 'video',
      external_url: '', client_name: '', location: '',
      equipment_used: '', status: 'published',
    });
    setFileFile(null);
    setFileThumb(null);
    setFileFilePreview(null);
    setFileThumbPreview(null);
  };

  const handleCreate = async () => {
    if (!formData.title.trim()) {
      toast.error('Título é obrigatório');
      return;
    }
    setIsSubmitting(true);
    try {
      const fd = new FormData();
      fd.append('title', formData.title);
      fd.append('description', formData.description);
      fd.append('work_type', formData.work_type);
      fd.append('external_url', formData.external_url);
      fd.append('client_name', formData.client_name);
      fd.append('location', formData.location);
      fd.append('equipment_used', formData.equipment_used);
      fd.append('status', formData.status);
      if (fileFile) fd.append('file', fileFile);
      if (fileThumb) fd.append('thumbnail', fileThumb);
      await api.post('/portfolio/works/', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      toast.success('Trabalho criado com sucesso!');
      setShowCreateModal(false);
      resetForm();
      fetchWorks();
    } catch (error: any) {
      const data = error.response?.data;
      if (data) {
        const msg = Object.entries(data).map(([k, v]: [string, any]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ');
        toast.error(msg);
      } else {
        toast.error('Erro ao criar trabalho');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEdit = async () => {
    if (!editingWork || !formData.title.trim()) {
      toast.error('Título é obrigatório');
      return;
    }
    setIsSubmitting(true);
    try {
      const fd = new FormData();
      fd.append('title', formData.title);
      fd.append('description', formData.description);
      fd.append('work_type', formData.work_type);
      fd.append('external_url', formData.external_url);
      fd.append('client_name', formData.client_name);
      fd.append('location', formData.location);
      fd.append('equipment_used', formData.equipment_used);
      fd.append('status', formData.status);
      if (fileFile) fd.append('file', fileFile);
      if (fileThumb) fd.append('thumbnail', fileThumb);
      await api.patch(`/portfolio/works/${editingWork.id}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      toast.success('Trabalho atualizado!');
      setShowEditModal(false);
      setEditingWork(null);
      resetForm();
      fetchWorks();
    } catch (error: any) {
      const data = error.response?.data;
      if (data) {
        const msg = Object.entries(data).map(([k, v]: [string, any]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ');
        toast.error(msg);
      } else {
        toast.error('Erro ao editar trabalho');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteTargetId) return;
    const id = deleteTargetId;
    setDeleteTargetId(null);
    setOpenMenuId(null);
    try {
      await api.delete(`/portfolio/works/${id}/`);
      fetchWorks();
      toast.success('Trabalho excluído!');
    } catch (error) {
      toast.error('Erro ao excluir trabalho');
    }
  };

  const openEditModal = (work: Work) => {
    setEditingWork(work);
    setFormData({
      title: work.title,
      description: work.description,
      work_type: work.work_type,
      external_url: work.external_url,
      client_name: work.client_name,
      location: work.location,
      equipment_used: work.equipment_used,
      status: work.status,
    });
    setFileFile(null);
    setFileThumb(null);
    setFileFilePreview(work.file || null);
    setFileThumbPreview(work.thumbnail || null);
    setShowEditModal(true);
    setOpenMenuId(null);
  };

  const handleStatusToggle = async (work: Work) => {
    const newStatus = work.status === 'published' ? 'draft' : 'published';
    try {
      await api.patch(`/portfolio/works/${work.id}/`, { status: newStatus });
      setOpenMenuId(null);
      fetchWorks();
      toast.success(newStatus === 'published' ? 'Trabalho publicado!' : 'Trabalho movido para rascunho');
    } catch (error) {
      toast.error('Erro ao alterar status');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-iris"></div>
      </div>
    );
  }

  const workFormModal = (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
      <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-lg max-h-[90vh] overflow-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-snow">
              {editingWork ? 'Editar Trabalho' : 'Novo Trabalho'}
            </h2>
            <button
              onClick={() => {
                editingWork ? setShowEditModal(false) : setShowCreateModal(false);
                setEditingWork(null);
                resetForm();
              }}
              className="text-muted hover:text-snow text-2xl"
            >
              &times;
            </button>
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
                placeholder="Descreva seu trabalho..."
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-snow mb-1">Tipo</label>
                <select
                  className="input"
                  value={formData.work_type}
                  onChange={(e) => setFormData({ ...formData, work_type: e.target.value })}
                >
                  <option value="video">Vídeo</option>
                  <option value="photo">Foto</option>
                  <option value="mixed">Misto</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-snow mb-1">Status</label>
                <select
                  className="input"
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                >
                  <option value="published">Publicado</option>
                  <option value="draft">Rascunho</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-snow mb-1">Link externo</label>
              <input
                className="input"
                placeholder="https://youtube.com/..."
                value={formData.external_url}
                onChange={(e) => setFormData({ ...formData, external_url: e.target.value })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-snow mb-1">Cliente</label>
                <input
                  className="input"
                  placeholder="Nome do cliente"
                  value={formData.client_name}
                  onChange={(e) => setFormData({ ...formData, client_name: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-snow mb-1">Local</label>
                <input
                  className="input"
                  placeholder="Cidade, Estado"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-snow mb-1">Equipamento</label>
              <input
                className="input"
                placeholder="Ex: Sony A7IV, DJI RS3..."
                value={formData.equipment_used}
                onChange={(e) => setFormData({ ...formData, equipment_used: e.target.value })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-snow mb-1">Arquivo (vídeo/foto)</label>
                {fileFilePreview && (
                  <p className="text-xs text-muted mb-2 truncate">{editingWork?.file ? 'Arquivo atual mantido' : fileFile?.name}</p>
                )}
                <input
                  type="file"
                  accept="video/*,image/*"
                  className="input text-sm file:mr-2 file:py-1 file:px-3 file:rounded-lg file:border-0 file:bg-iris/20 file:text-iris file:text-sm file:cursor-pointer"
                  onChange={(e) => {
                    const f = e.target.files?.[0] || null;
                    setFileFile(f);
                    setFileFilePreview(f ? f.name : editingWork?.file || null);
                  }}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-snow mb-1">Thumbnail</label>
                {fileThumbPreview && (
                  <img src={fileThumbPreview} alt="Preview" className="w-full h-20 object-cover rounded mb-2" />
                )}
                <input
                  type="file"
                  accept="image/*"
                  className="input text-sm file:mr-2 file:py-1 file:px-3 file:rounded-lg file:border-0 file:bg-iris/20 file:text-iris file:text-sm file:cursor-pointer"
                  onChange={(e) => {
                    const f = e.target.files?.[0] || null;
                    setFileThumb(f);
                    setFileThumbPreview(f ? URL.createObjectURL(f) : editingWork?.thumbnail || null);
                  }}
                />
              </div>
            </div>
          </div>

          <div className="flex gap-4 mt-6">
            <button
              onClick={() => {
                editingWork ? setShowEditModal(false) : setShowCreateModal(false);
                setEditingWork(null);
                resetForm();
              }}
              className="flex-1 btn-secondary py-3"
            >
              Cancelar
            </button>
            <button
              onClick={editingWork ? handleEdit : handleCreate}
              disabled={isSubmitting}
              className="flex-1 btn-primary py-3 disabled:opacity-50"
            >
              {isSubmitting ? 'Salvando...' : editingWork ? 'Salvar Alterações' : 'Criar Trabalho'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-snow">Portfólio</h1>
        <button onClick={() => { resetForm(); setShowCreateModal(true); }} className="btn-primary">+ Novo Trabalho</button>
      </div>

      {/* Categories filter */}
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setSelectedCategory('')}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
            !selectedCategory
              ? 'bg-iris text-white'
              : 'bg-slate/50 text-muted hover:text-snow'
          }`}
        >
          Todos
        </button>
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.slug)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedCategory === cat.slug
                ? 'bg-iris text-white'
                : 'bg-slate/50 text-muted hover:text-snow'
            }`}
          >
            {cat.name}
          </button>
        ))}
      </div>

      {/* Works grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {works.map((work) => (
          <div key={work.id} className="card group relative" ref={openMenuId === work.id ? menuRef : undefined}>
            {/* 3-dot menu */}
            {work.is_mine && (
              <div className="absolute top-3 right-3 z-10">
                <button
                  onClick={() => setOpenMenuId(openMenuId === work.id ? null : work.id)}
                  className="w-8 h-8 bg-obsidian/80 backdrop-blur rounded-lg flex items-center justify-center text-muted hover:text-snow hover:bg-obsidian transition-all"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01" />
                  </svg>
                </button>
                {openMenuId === work.id && (
                  <div className="absolute right-0 top-10 w-52 bg-obsidian border border-slate/50 rounded-xl shadow-xl z-20 py-2">
                    <button
                      onClick={() => openEditModal(work)}
                      className="w-full px-4 py-2 text-left text-sm text-snow hover:bg-slate/50 flex items-center gap-2"
                    >
                      <span>✏️</span> Editar
                    </button>
                    <button
                      onClick={() => handleStatusToggle(work)}
                      className="w-full px-4 py-2 text-left text-sm text-snow hover:bg-slate/50 flex items-center gap-2"
                    >
                      <span>{work.status === 'published' ? '📝' : '🌐'}</span>
                      {work.status === 'published' ? 'Mover para Rascunho' : 'Publicar'}
                    </button>
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(window.location.origin + '/portfolio');
                        setOpenMenuId(null);
                        toast.success('Link copiado!');
                      }}
                      className="w-full px-4 py-2 text-left text-sm text-snow hover:bg-slate/50 flex items-center gap-2"
                    >
                      <span>🔗</span> Copiar link
                    </button>
                    <hr className="border-slate/50 my-1" />
                    <button
                      onClick={() => { setOpenMenuId(null); setDeleteTargetId(work.id); }}
                      className="w-full px-4 py-2 text-left text-sm text-crimson hover:bg-crimson/10 flex items-center gap-2"
                    >
                      <span>🗑️</span> Excluir
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Thumbnail */}
            <div className="aspect-video bg-graphite rounded-lg mb-4 overflow-hidden cursor-pointer">
              {work.thumbnail ? (
                <img
                  src={work.thumbnail}
                  alt={work.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <span className="text-4xl">🎬</span>
                </div>
              )}
            </div>

            {/* Info */}
            <h3 className="font-semibold text-snow mb-1">{work.title}</h3>
            <p className="text-sm text-muted mb-3 line-clamp-2">{work.description}</p>
            <div className="flex items-center justify-between text-xs text-muted">
              <span>{work.videomaker_name}</span>
              <div className="flex items-center gap-3">
                <span>👁️ {work.views_count}</span>
                <span>❤️ {work.likes_count}</span>
              </div>
            </div>
            {work.status === 'draft' && (
              <span className="absolute top-3 left-3 badge bg-amber/20 text-amber text-xs">Rascunho</span>
            )}
          </div>
        ))}
      </div>

      {works.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted mb-4">Nenhum trabalho encontrado.</p>
          <button onClick={() => { resetForm(); setShowCreateModal(true); }} className="btn-primary">
            + Criar primeiro trabalho
          </button>
        </div>
      )}

      {/* Modals */}
      {showCreateModal && workFormModal}
      {showEditModal && workFormModal}

      {/* Delete confirmation modal */}
      {deleteTargetId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-sm p-6">
            <h3 className="text-lg font-bold text-snow mb-2">Excluir trabalho</h3>
            <p className="text-muted mb-6">Tem certeza que deseja excluir este trabalho? Essa ação não pode ser desfeita.</p>
            <div className="flex gap-3">
              <button
                onClick={() => setDeleteTargetId(null)}
                className="flex-1 btn-secondary py-2.5"
              >
                Cancelar
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 bg-crimson text-white py-2.5 rounded-lg font-medium hover:bg-crimson/80 transition-colors"
              >
                Excluir
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

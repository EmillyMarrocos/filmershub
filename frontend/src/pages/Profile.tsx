// ===========================================
// FILMERSHUB - PROFILE PAGE
// ===========================================

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import api from '@/api/client';
import { User, Work, Review } from '@/types';
import toast from 'react-hot-toast';

export default function Profile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user: currentUser, setUser: setCurrentUser } = useAuthStore();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showEditModal, setShowEditModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isFollowLoading, setIsFollowLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'works' | 'reviews' | 'about'>('works');
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [profileWorks, setProfileWorks] = useState<Work[]>([]);
  const [profileReviews, setProfileReviews] = useState<Review[]>([]);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    bio: '',
    phone: '',
    city: '',
    state: '',
    instagram: '',
    youtube: '',
    website: '',
  });

  useEffect(() => {
    fetchProfile();
  }, [id]);

  useEffect(() => {
    if (!user) return;
    if (activeTab === 'works') {
      api.get(`/portfolio/works/?videomaker=${user.id}`)
        .then((res) => setProfileWorks(res.data.results || res.data))
        .catch(() => {});
    } else if (activeTab === 'reviews') {
      api.get(`/portfolio/reviews/?videomaker=${user.id}`)
        .then((res) => setProfileReviews(res.data.results || res.data))
        .catch(() => {});
    }
  }, [user, activeTab]);

  const fetchProfile = async () => {
    try {
      const url = id ? `/users/${id}/` : '/profile/';
      const response = await api.get(url);
      setUser(response.data);
    } catch (error) {
      toast.error('Erro ao carregar perfil');
    } finally {
      setIsLoading(false);
    }
  };

  const openEditModal = () => {
    if (!user) return;
    setFormData({
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      bio: user.bio || '',
      phone: user.phone || '',
      city: user.city || '',
      state: user.state || '',
      instagram: user.instagram || '',
      youtube: user.youtube || '',
      website: user.website || '',
    });
    setShowEditModal(true);
    setAvatarFile(null);
    setAvatarPreview(null);
  };

  const handleSave = async () => {
    if (!formData.first_name.trim() || !formData.last_name.trim()) {
      toast.error('Nome e sobrenome são obrigatórios');
      return;
    }
    setIsSaving(true);
    try {
      const fd = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        fd.append(key, value);
      });
      if (avatarFile) {
        fd.append('avatar', avatarFile);
      }
      const response = await api.patch('/profile/', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUser(response.data);
      setCurrentUser(response.data);
      setShowEditModal(false);
      setAvatarFile(null);
      setAvatarPreview(null);
      toast.success('Perfil atualizado!');
    } catch (error: any) {
      const data = error.response?.data;
      if (data) {
        const msg = Object.entries(data).map(([k, v]: [string, any]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ');
        toast.error(msg);
      } else {
        toast.error('Erro ao salvar perfil');
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleFollow = async () => {
    if (!user || isFollowLoading) return;
    setIsFollowLoading(true);
    try {
      const res = await api.post(`/users/${user.id}/follow/`);
      const nowFollowing = res.status === 201;
      setUser({ ...user, is_following: nowFollowing, followers_count: user.followers_count + (nowFollowing ? 1 : -1) });
      toast.success(nowFollowing ? 'Agora você segue este usuário!' : 'Deixou de seguir.');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao seguir');
    } finally {
      setIsFollowLoading(false);
    }
  };

  const handleMessage = async () => {
    if (!user) return;
    try {
      const res = await api.post('/chat/rooms/create/', { user_id: user.id });
      navigate('/chat', { state: { roomId: res.data.id } });
    } catch {
      toast.error('Erro ao abrir conversa');
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await api.delete('/profile/delete/');
      localStorage.removeItem('tokens');
      toast.success('Conta desativada.');
      window.location.href = '/login';
    } catch {
      toast.error('Erro ao excluir conta');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-iris"></div>
      </div>
    );
  }

  if (!user) {
    return <div className="text-center py-12 text-muted">Usuário não encontrado.</div>;
  }

  const isOwnProfile = !id || (currentUser !== null && String(currentUser.id) === String(user.id));

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Cover */}
      <div className="h-48 bg-gradient-to-r from-iris/20 to-ember/20 rounded-xl" />

      {/* Profile info */}
      <div className="card relative -mt-24">
        <div className="flex flex-col sm:flex-row items-center sm:items-end gap-6">
          {/* Avatar */}
          <div className="w-32 h-32 bg-slate rounded-full border-4 border-obsidian flex items-center justify-center overflow-hidden">
            {user.avatar_url ? (
              <img src={user.avatar_url} alt="" className="w-full h-full object-cover" />
            ) : (
              <span className="text-4xl text-iris font-bold">{user.first_name[0]}</span>
            )}
          </div>

          {/* Info */}
          <div className="flex-1 text-center sm:text-left">
            <h1 className="text-2xl font-bold text-snow">{user.full_name}</h1>
            <p className="text-muted">{user.email}</p>
            <div className="flex items-center gap-2 mt-2 justify-center sm:justify-start">
              <span className={`badge ${
                user.is_videomaker ? 'badge-iris' : 'badge-ember'
              }`}>
                {user.profile_type === 'videomaker' ? 'Videomaker' :
                 user.profile_type === 'client' ? 'Cliente' : 'Videomaker & Cliente'}
              </span>
              {user.city && (
                <span className="text-sm text-muted">📍 {user.city}, {user.state}</span>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            {isOwnProfile ? (
              <button onClick={openEditModal} className="btn-secondary">Editar Perfil</button>
            ) : (
              <>
                <button
                  onClick={handleFollow}
                  disabled={isFollowLoading}
                  className={user.is_following ? 'btn-secondary' : 'btn-primary'}
                >
                  {isFollowLoading ? '...' : user.is_following ? '✓ Seguindo' : 'Seguir'}
                </button>
                <button onClick={handleMessage} className="btn-secondary">💬 Mensagem</button>
              </>
            )}
          </div>
        </div>

        {/* Bio */}
        {user.bio && (
          <div className="mt-6 pt-6 border-t border-slate/50">
            <p className="text-snow">{user.bio}</p>
          </div>
        )}

        {/* Social links */}
        <div className="flex items-center gap-4 mt-4">
          {user.instagram && (
            <a href={`https://instagram.com/${user.instagram}`} target="_blank" rel="noopener noreferrer" className="text-muted hover:text-iris">
              📷 Instagram
            </a>
          )}
          {user.youtube && (
            <a href={`https://youtube.com/${user.youtube}`} target="_blank" rel="noopener noreferrer" className="text-muted hover:text-crimson">
              🎬 YouTube
            </a>
          )}
          {user.website && (
            <a href={user.website} target="_blank" rel="noopener noreferrer" className="text-muted hover:text-jade">
              🌐 Website
            </a>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-slate/50">
        <button
          onClick={() => setActiveTab('works')}
          className={`pb-4 border-b-2 font-medium transition-colors ${
            activeTab === 'works' ? 'border-iris text-iris' : 'border-transparent text-muted hover:text-snow'
          }`}
        >
          Trabalhos
        </button>
        <button
          onClick={() => setActiveTab('reviews')}
          className={`pb-4 border-b-2 font-medium transition-colors ${
            activeTab === 'reviews' ? 'border-iris text-iris' : 'border-transparent text-muted hover:text-snow'
          }`}
        >
          Avaliações
        </button>
        <button
          onClick={() => setActiveTab('about')}
          className={`pb-4 border-b-2 font-medium transition-colors ${
            activeTab === 'about' ? 'border-iris text-iris' : 'border-transparent text-muted hover:text-snow'
          }`}
        >
          Sobre
        </button>
      </div>

      {/* Tab content */}
      {activeTab === 'works' && (
        <div>
          {profileWorks.length === 0 ? (
            <div className="text-center py-12 text-muted">
              <p>Nenhum trabalho publicado ainda.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {profileWorks.map((w) => (
                <div key={w.id} className="card overflow-hidden">
                  {w.thumbnail ? (
                    <img src={w.thumbnail} alt={w.title} className="w-full h-40 object-cover" />
                  ) : (
                    <div className="w-full h-40 bg-graphite flex items-center justify-center">
                      <span className="text-4xl opacity-30">🎬</span>
                    </div>
                  )}
                  <div className="p-3">
                    <h4 className="font-medium text-snow text-sm truncate">{w.title}</h4>
                    {w.category_name && (
                      <p className="text-xs text-muted mt-1">{w.category_name}</p>
                    )}
                    <div className="flex items-center gap-3 mt-2 text-xs text-muted">
                      <span>👁 {w.views_count}</span>
                      <span>❤️ {w.likes_count}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'reviews' && (
        <div>
          {profileReviews.length === 0 ? (
            <div className="text-center py-12 text-muted">
              <p>Nenhuma avaliação recebida ainda.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {profileReviews.map((r) => (
                <div key={r.id} className="card">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-8 h-8 bg-slate rounded-full flex items-center justify-center">
                      <span className="text-iris font-bold text-xs">{r.reviewer_name[0]}</span>
                    </div>
                    <span className="font-medium text-snow text-sm">{r.reviewer_name}</span>
                    <span className="text-xs text-muted">
                      {new Date(r.created_at).toLocaleDateString('pt-BR')}
                    </span>
                    <span className="ml-auto text-sm">
                      {'⭐'.repeat(r.rating)}
                    </span>
                  </div>
                  <p className="text-sm text-snow/90">{r.comment}</p>
                  {r.response && (
                    <div className="mt-3 p-3 bg-graphite rounded-lg">
                      <p className="text-xs text-muted mb-1">Resposta do videomaker:</p>
                      <p className="text-sm text-snow">{r.response}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'about' && (
        <div className="card space-y-6">
          {/* Bio */}
          <div>
            <h3 className="text-sm font-medium text-muted mb-2">Sobre</h3>
            <p className="text-snow">{user.bio || 'Nenhuma biografia adicionada.'}</p>
          </div>

          {/* Info */}
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-muted mb-2">Tipo de Conta</h3>
              <p className="text-snow">
                {user.profile_type === 'videomaker' && '🎬 Videomaker'}
                {user.profile_type === 'client' && '💼 Cliente'}
                {user.profile_type === 'both' && '🤝 Videomaker & Cliente'}
              </p>
            </div>
            {user.city && (
              <div>
                <h3 className="text-sm font-medium text-muted mb-2">Localização</h3>
                <p className="text-snow">📍 {user.city}, {user.state}</p>
              </div>
            )}
            {user.phone && (
              <div>
                <h3 className="text-sm font-medium text-muted mb-2">Telefone</h3>
                <p className="text-snow">📱 {user.phone}</p>
              </div>
            )}
            <div>
              <h3 className="text-sm font-medium text-muted mb-2">Membro desde</h3>
              <p className="text-snow">
                📅 {new Date(user.date_joined).toLocaleDateString('pt-BR', {
                  month: 'long',
                  year: 'numeric',
                })}
              </p>
            </div>
          </div>

          {/* Social links */}
          {(user.instagram || user.youtube || user.website) && (
            <div className="pt-4 border-t border-slate/50">
              <h3 className="text-sm font-medium text-muted mb-3">Redes Sociais</h3>
              <div className="flex flex-wrap gap-3">
                {user.instagram && (
                  <a
                    href={`https://instagram.com/${user.instagram}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-3 py-2 bg-graphite rounded-lg text-sm text-muted hover:text-iris hover:bg-iris/10 transition-colors"
                  >
                    📷 @{user.instagram}
                  </a>
                )}
                {user.youtube && (
                  <a
                    href={`https://youtube.com/${user.youtube}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-3 py-2 bg-graphite rounded-lg text-sm text-muted hover:text-crimson hover:bg-crimson/10 transition-colors"
                  >
                    🎬 @{user.youtube}
                  </a>
                )}
                {user.website && (
                  <a
                    href={user.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-3 py-2 bg-graphite rounded-lg text-sm text-muted hover:text-jade hover:bg-jade/10 transition-colors"
                  >
                    🌐 {user.website.replace(/^https?:\/\//, '')}
                  </a>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Edit Profile Modal */}
      {showEditModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-lg max-h-[90vh] overflow-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-snow">Editar Perfil</h2>
                <button onClick={() => setShowEditModal(false)} className="text-muted hover:text-snow text-2xl">&times;</button>
              </div>

              <div className="space-y-4">
                {/* Avatar */}
                <div className="flex items-center gap-4">
                  <div className="w-20 h-20 bg-slate rounded-full flex items-center justify-center overflow-hidden flex-shrink-0">
                    {avatarPreview ? (
                      <img src={avatarPreview} alt="" className="w-full h-full object-cover" />
                    ) : user?.avatar_url ? (
                      <img src={user.avatar_url} alt="" className="w-full h-full object-cover" />
                    ) : (
                      <span className="text-2xl text-iris font-bold">{user?.first_name[0]}</span>
                    )}
                  </div>
                  <div>
                    <label className="btn-secondary text-sm cursor-pointer inline-block">
                      📷 Alterar foto
                      <input
                        type="file"
                        accept="image/*"
                        className="hidden"
                        onChange={(e) => {
                          const file = e.target.files?.[0];
                          if (file) {
                            setAvatarFile(file);
                            setAvatarPreview(URL.createObjectURL(file));
                          }
                        }}
                      />
                    </label>
                    <p className="text-xs text-muted mt-1">JPG, PNG. Máx 5MB.</p>
                  </div>
                </div>

                {/* Nome e sobrenome */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Nome *</label>
                    <input
                      className="input"
                      value={formData.first_name}
                      onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Sobrenome *</label>
                    <input
                      className="input"
                      value={formData.last_name}
                      onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    />
                  </div>
                </div>

                {/* Bio */}
                <div>
                  <label className="block text-sm font-medium text-snow mb-1">Bio</label>
                  <textarea
                    className="input min-h-[80px]"
                    placeholder="Conte um pouco sobre você..."
                    maxLength={500}
                    value={formData.bio}
                    onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  />
                  <p className="text-xs text-muted mt-1">{formData.bio.length}/500</p>
                </div>

                {/* Telefone e Local */}
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Telefone</label>
                    <input
                      className="input"
                      placeholder="(11) 99999-0000"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">Cidade</label>
                    <input
                      className="input"
                      placeholder="São Paulo"
                      value={formData.city}
                      onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-1">UF</label>
                    <input
                      className="input"
                      placeholder="SP"
                      maxLength={2}
                      value={formData.state}
                      onChange={(e) => setFormData({ ...formData, state: e.target.value.toUpperCase() })}
                    />
                  </div>
                </div>

                {/* Redes sociais */}
                <div className="pt-2 border-t border-slate/50">
                  <p className="text-sm font-medium text-snow mb-3">Redes Sociais</p>
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      <span className="text-lg">📷</span>
                      <input
                        className="input flex-1"
                        placeholder="@seuinstagram"
                        value={formData.instagram}
                        onChange={(e) => setFormData({ ...formData, instagram: e.target.value })}
                      />
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-lg">🎬</span>
                      <input
                        className="input flex-1"
                        placeholder="@seucanal"
                        value={formData.youtube}
                        onChange={(e) => setFormData({ ...formData, youtube: e.target.value })}
                      />
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-lg">🌐</span>
                      <input
                        className="input flex-1"
                        placeholder="https://seusite.com"
                        value={formData.website}
                        onChange={(e) => setFormData({ ...formData, website: e.target.value })}
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-4 mt-6">
                <button onClick={() => setShowEditModal(false)} className="flex-1 btn-secondary py-3">
                  Cancelar
                </button>
                <button
                  onClick={handleSave}
                  disabled={isSaving}
                  className="flex-1 btn-primary py-3 disabled:opacity-50"
                >
                  {isSaving ? 'Salvando...' : 'Salvar Alterações'}
                </button>
              </div>

              <div className="mt-6 pt-4 border-t border-slate/50">
                <button
                  onClick={() => setShowDeleteModal(true)}
                  className="text-sm text-crimson hover:text-crimson/80 transition-colors"
                >
                  🗑️ Excluir minha conta
                </button>
                <p className="text-xs text-muted mt-1">Essa ação não pode ser desfeita.</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Account Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-sm p-6">
            <h3 className="text-lg font-bold text-snow mb-2">Excluir conta</h3>
            <p className="text-muted mb-6">Tem certeza? Sua conta será desativada permanentemente. Essa ação não pode ser desfeita.</p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="flex-1 btn-secondary py-2.5"
              >
                Cancelar
              </button>
              <button
                onClick={handleDeleteAccount}
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

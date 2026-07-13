// ===========================================
// FILMERSHUB - EXPLORE PAGE (CLIENTS)
// ===========================================

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '@/api/client';
import { User } from '@/types';
import toast from 'react-hot-toast';

export default function Explore() {
  const [videomakers, setVideomakers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchVideomakers();
  }, []);

  const fetchVideomakers = async () => {
    try {
      const params = search ? `?search=${encodeURIComponent(search)}` : '';
      const response = await api.get(`/videomakers/${params}`);
      setVideomakers(response.data.results || response.data);
    } catch (error) {
      toast.error('Erro ao carregar videomakers');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = () => {
    setIsLoading(true);
    fetchVideomakers();
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
      <div>
        <h1 className="text-2xl font-bold text-snow mb-2">Explorar Videomakers</h1>
        <p className="text-muted">Encontre o profissional ideal para seu projeto</p>
      </div>

      {/* Search */}
      <div className="card">
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Buscar por nome, cidade..."
            className="input flex-1"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch} className="btn-primary">
            Buscar
          </button>
        </div>
      </div>

      {/* Videomakers grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {videomakers.map((vm) => (
          <Link
            key={vm.id}
            to={`/profile/${vm.id}`}
            className="card hover:border-iris/50 transition-all group"
          >
            <div className="flex items-center gap-4 mb-4">
              <div className="w-16 h-16 bg-slate rounded-full flex items-center justify-center overflow-hidden flex-shrink-0">
                {vm.avatar_url ? (
                  <img src={vm.avatar_url} alt="" className="w-full h-full object-cover" />
                ) : (
                  <span className="text-2xl text-iris font-bold">{vm.full_name[0]}</span>
                )}
              </div>
              <div className="min-w-0">
                <h3 className="font-semibold text-snow group-hover:text-iris transition-colors truncate">
                  {vm.full_name}
                </h3>
                {vm.city && (
                  <p className="text-sm text-muted">📍 {vm.city}, {vm.state}</p>
                )}
              </div>
            </div>
            {vm.bio && (
              <p className="text-sm text-muted line-clamp-2 mb-3">{vm.bio}</p>
            )}
            <div className="flex items-center justify-between text-xs text-muted pt-3 border-t border-slate/50">
              <span className="badge badge-iris">Videomaker</span>
              <span>Ver perfil →</span>
            </div>
          </Link>
        ))}
      </div>

      {videomakers.length === 0 && (
        <div className="text-center py-12">
          <span className="text-4xl">🎬</span>
          <p className="text-muted mt-4">Nenhum videomaker encontrado.</p>
        </div>
      )}
    </div>
  );
}

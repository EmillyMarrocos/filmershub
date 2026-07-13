// ===========================================
// FILMERSHUB - HOME PAGE (LANDING)
// ===========================================

import { Link } from 'react-router-dom';
import { useState, useEffect, useRef } from 'react';
import api from '@/api/client';

function AnimatedCounter({ target, suffix = '' }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasAnimated.current) {
          hasAnimated.current = true;
          const duration = 1500;
          const steps = 60;
          const increment = target / steps;
          let current = 0;
          let mounted = true;
          const timer = setInterval(() => {
            if (!mounted) { clearInterval(timer); return; }
            current += increment;
            if (current >= target) {
              setCount(target);
              clearInterval(timer);
            } else {
              setCount(Math.floor(current));
            }
          }, duration / steps);
          return () => { mounted = false; clearInterval(timer); };
        }
      },
      { threshold: 0.5 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [target]);

  return (
    <div ref={ref} className="text-4xl md:text-5xl font-bold text-iris">
      {count.toLocaleString('pt-BR')}{suffix}
    </div>
  );
}

interface LandingStats {
  videomakers: number;
  works: number;
  posts: number;
  clients: number;
}

interface FeaturedUser {
  id: string;
  first_name: string;
  full_name: string;
  avatar_url: string | null;
  profile_type: string;
  bio: string;
  city: string;
  state: string;
}

interface FeaturedWork {
  id: string;
  title: string;
  thumbnail: string | null;
  videomaker: string;
  videomaker_name: string;
  category_name: string | null;
  views_count: number;
  likes_count: number;
}

export default function Home() {
  const [stats, setStats] = useState<LandingStats | null>(null);
  const [featuredVMs, setFeaturedVMs] = useState<FeaturedUser[]>([]);
  const [featuredWorks, setFeaturedWorks] = useState<FeaturedWork[]>([]);

  useEffect(() => {
    api.get('/landing/stats/').then((r) => setStats(r.data)).catch(() => {});
    api.get('/landing/featured-videomakers/').then((r) => setFeaturedVMs(r.data)).catch(() => {});
    api.get('/landing/featured-works/').then((r) => setFeaturedWorks(r.data)).catch(() => {});
  }, []);

  return (
    <div className="min-h-screen bg-void">
      {/* Header */}
      <header className="border-b border-slate/50 backdrop-blur-sm bg-void/80 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-iris rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">F</span>
            </div>
            <span className="text-xl font-bold text-snow">
              Filmers<span className="text-iris">Hub</span>
            </span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/login" className="btn-ghost">
              Entrar
            </Link>
            <Link to="/register" className="btn-primary">
              Criar Conta
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-iris/5 via-transparent to-transparent" />
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-iris/10 rounded-full blur-3xl" />
        <div className="absolute top-40 right-1/4 w-72 h-72 bg-ember/10 rounded-full blur-3xl" />

        <div className="relative max-w-7xl mx-auto px-6 py-24 md:py-36">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-block mb-6 px-4 py-2 bg-iris/10 border border-iris/20 rounded-full">
              <span className="text-iris text-sm font-medium">A plataforma para profissionais de vídeo</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold text-snow mb-6 leading-tight">
              Seu talento merece{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-iris to-ember">
                destaque
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-muted mb-10 max-w-2xl mx-auto leading-relaxed">
              Portfólio profissional, chat, agendamento, contratos e pagamentos.
              Tudo que videomakers e clientes precisam em um só lugar.
            </p>

            <div className="flex items-center justify-center gap-4 flex-wrap">
              <Link to="/register" className="btn-primary text-lg px-10 py-4 shadow-lg shadow-iris/20">
                Comece Gratuitamente
              </Link>
              <Link to="/explore" className="btn-ghost text-lg px-10 py-4">
                Ver Comunidade
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      {stats && (
        <section className="border-y border-slate/50 bg-obsidian/50">
          <div className="max-w-5xl mx-auto px-6 py-16">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
              <div>
                <AnimatedCounter target={stats.videomakers} />
                <p className="text-muted mt-2">Videomakers</p>
              </div>
              <div>
                <AnimatedCounter target={stats.clients} />
                <p className="text-muted mt-2">Clientes</p>
              </div>
              <div>
                <AnimatedCounter target={stats.works} suffix="+" />
                <p className="text-muted mt-2">Trabalhos Publicados</p>
              </div>
              <div>
                <AnimatedCounter target={stats.posts} suffix="+" />
                <p className="text-muted mt-2">Posts no Feed</p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Como Funciona */}
      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-snow mb-4">
            Como funciona
          </h2>
          <p className="text-muted text-lg max-w-xl mx-auto">
            Em 3 passos simples, comece a usar a plataforma completa
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              step: '01',
              icon: '🎬',
              title: 'Crie seu perfil',
              desc: 'Monte seu portfólio profissional com seus melhores trabalhos. Mostre sua especialidade e equipamentos.',
              color: 'iris',
            },
            {
              step: '02',
              icon: '🤝',
              title: 'Conecte-se',
              desc: 'Encontre clientes ou videomakers, converse pelo chat e agende seus trabalhos direto na plataforma.',
              color: 'ember',
            },
            {
              step: '03',
              icon: '💰',
              title: 'Feche o negócio',
              desc: 'Gere contratos profissionais com PDF, receba pagamentos via PIX ou cartão de forma segura.',
              color: 'jade',
            },
          ].map((item) => (
            <div key={item.step} className="card relative group hover:border-iris/30 transition-all duration-300">
              <div className={`text-${item.color} text-sm font-bold mb-4 opacity-50`}>PASSO {item.step}</div>
              <div className={`w-16 h-16 bg-${item.color}/20 rounded-2xl flex items-center justify-center mb-6`}>
                <span className="text-3xl">{item.icon}</span>
              </div>
              <h3 className="text-xl font-semibold text-snow mb-3">{item.title}</h3>
              <p className="text-muted leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section className="bg-obsidian/50 border-y border-slate/50">
        <div className="max-w-7xl mx-auto px-6 py-24">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-snow mb-4">
              Tudo que você precisa
            </h2>
            <p className="text-muted text-lg max-w-xl mx-auto">
              Ferramentas profissionais para gerenciar sua carreira
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: '🎬', title: 'Portfólio', desc: 'Mostre seus melhores trabalhos com thumbnails e métricas de visualização.', color: 'iris' },
              { icon: '💬', title: 'Chat em Tempo Real', desc: 'Converse diretamente com clientes e feche negócios rapidamente.', color: 'ember' },
              { icon: '📅', title: 'Agendamento', desc: 'Gerencie sua agenda e receba solicitações de clientes.', color: 'jade' },
              { icon: '📄', title: 'Contratos', desc: 'Gere contratos profissionais com 12 cláusulas e assinatura digital.', color: 'amber' },
              { icon: '💳', title: 'Pagamentos', desc: 'Receba via PIX ou cartão com split automático (85/15).', color: 'iris' },
              { icon: '🔔', title: 'Notificações', desc: 'Receba alertas em tempo real para mensagens, contratos e pagamentos.', color: 'crimson' },
            ].map((f) => (
              <div key={f.title} className="card flex gap-4 hover:border-iris/20 transition-all duration-300">
                <div className={`w-12 h-12 bg-${f.color}/20 rounded-xl flex items-center justify-center flex-shrink-0`}>
                  <span className="text-2xl">{f.icon}</span>
                </div>
                <div>
                  <h3 className="font-semibold text-snow mb-1">{f.title}</h3>
                  <p className="text-sm text-muted leading-relaxed">{f.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Videomakers */}
      {featuredVMs.length > 0 && (
        <section className="max-w-7xl mx-auto px-6 py-24">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-snow mb-2">
                Videomakers em destaque
              </h2>
              <p className="text-muted text-lg">Profissionais que já estão na plataforma</p>
            </div>
            <Link to="/explore" className="btn-ghost hidden md:block">
              Ver Todos →
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredVMs.map((vm) => (
              <Link
                key={vm.id}
                to={`/profile/${vm.id}`}
                className="card flex items-center gap-4 hover:border-iris/30 transition-all duration-300 group"
              >
                <div className="w-16 h-16 bg-slate rounded-full flex items-center justify-center overflow-hidden flex-shrink-0">
                  {vm.avatar_url ? (
                    <img src={vm.avatar_url} alt="" className="w-full h-full object-cover" />
                  ) : (
                    <span className="text-2xl text-iris font-bold">{vm.full_name[0]}</span>
                  )}
                </div>
                <div className="min-w-0">
                  <h3 className="font-semibold text-snow truncate group-hover:text-iris transition-colors">
                    {vm.full_name}
                  </h3>
                  <p className="text-sm text-muted truncate">{vm.bio || 'Videomaker profissional'}</p>
                  {vm.city && (
                    <p className="text-xs text-muted mt-1">📍 {vm.city}, {vm.state}</p>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Featured Works */}
      {featuredWorks.length > 0 && (
        <section className="bg-obsidian/50 border-y border-slate/50">
          <div className="max-w-7xl mx-auto px-6 py-24">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-snow mb-4">
                Trabalhos em destaque
              </h2>
              <p className="text-muted text-lg">Confira os melhores trabalhos da comunidade</p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {featuredWorks.map((work) => (
                <Link
                  key={work.id}
                  to={`/profile/${work.videomaker}`}
                  className="group relative aspect-[4/3] bg-slate rounded-xl overflow-hidden hover:ring-2 hover:ring-iris/50 transition-all duration-300"
                >
                  {work.thumbnail ? (
                    <img src={work.thumbnail} alt={work.title} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center bg-graphite">
                      <span className="text-4xl opacity-30">🎬</span>
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  <div className="absolute bottom-0 left-0 right-0 p-3 translate-y-4 group-hover:translate-y-0 opacity-0 group-hover:opacity-100 transition-all duration-300">
                    <p className="text-white text-sm font-medium truncate">{work.title}</p>
                    <p className="text-white/60 text-xs">{work.videomaker_name}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Final */}
      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="relative bg-gradient-to-br from-iris/20 via-obsidian to-ember/10 border border-slate/50 rounded-2xl p-12 md:p-16 text-center overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-iris/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-ember/10 rounded-full blur-3xl" />

          <div className="relative">
            <h2 className="text-3xl md:text-5xl font-bold text-snow mb-6">
              Pronto para começar?
            </h2>
            <p className="text-xl text-muted mb-10 max-w-xl mx-auto">
              Junte-se a dezenas de videomakers e clientes que já estão na plataforma.
              Comece gratuitamente agora.
            </p>
            <div className="flex items-center justify-center gap-4 flex-wrap">
              <Link to="/register" className="btn-primary text-lg px-10 py-4 shadow-lg shadow-iris/20">
                Criar Minha Conta
              </Link>
              <Link to="/feed" className="btn-ghost text-lg px-10 py-4">
                Explorar Feed
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate/50 bg-obsidian/30">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 bg-iris rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">F</span>
                </div>
                <span className="font-bold text-snow">Filmers<span className="text-iris">Hub</span></span>
              </div>
              <p className="text-sm text-muted leading-relaxed">
                A plataforma completa para profissionais de vídeo e seus clientes.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-snow mb-4">Plataforma</h4>
              <div className="space-y-2">
                <Link to="/feed" className="block text-sm text-muted hover:text-iris transition-colors">Feed</Link>
                <Link to="/explore" className="block text-sm text-muted hover:text-iris transition-colors">Explorar</Link>
                <Link to="/register" className="block text-sm text-muted hover:text-iris transition-colors">Criar Conta</Link>
              </div>
            </div>
            <div>
              <h4 className="font-semibold text-snow mb-4">Para Videomakers</h4>
              <div className="space-y-2">
                <p className="text-sm text-muted">Portfólio profissional</p>
                <p className="text-sm text-muted">Agendamento de trabalhos</p>
                <p className="text-sm text-muted">Contratos e pagamentos</p>
              </div>
            </div>
            <div>
              <h4 className="font-semibold text-snow mb-4">Para Clientes</h4>
              <div className="space-y-2">
                <p className="text-sm text-muted">Encontre videomakers</p>
                <p className="text-sm text-muted">Solicite orçamentos</p>
                <p className="text-sm text-muted">Pagamento seguro</p>
              </div>
            </div>
          </div>
          <div className="border-t border-slate/50 mt-8 pt-8 text-center text-sm text-muted">
            &copy; 2026 FilmersHub. Todos os direitos reservados.
          </div>
        </div>
      </footer>
    </div>
  );
}

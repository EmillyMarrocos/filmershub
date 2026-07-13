// ===========================================
// FILMERSHUB - FEED PAGE
// ===========================================

import { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '@/store/authStore';
import api from '@/api/client';
import { Post, Comment } from '@/types';
import toast from 'react-hot-toast';

const REACTIONS = [
  { emoji: '❤️', label: 'Love' },
  { emoji: '👍', label: 'Like' },
  { emoji: '🔥', label: 'Fire' },
  { emoji: '😮', label: 'Wow' },
  { emoji: '👏', label: 'Clap' },
  { emoji: '😢', label: 'Sad' },
];

export default function Feed() {
  const { user } = useAuthStore();
  const [posts, setPosts] = useState<Post[]>([]);
  const [newPost, setNewPost] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [editingPostId, setEditingPostId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState('');
  const [openMenuId, setOpenMenuId] = useState<string | null>(null);
  const [showReactionsId, setShowReactionsId] = useState<string | null>(null);
  const [deleteTargetId, setDeleteTargetId] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  const [nextPage, setNextPage] = useState<string | null>(null);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  const [commentPostId, setCommentPostId] = useState<string | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [isLoadingComments, setIsLoadingComments] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (commentPostId) { setCommentPostId(null); setNewComment(''); }
        if (deleteTargetId) setDeleteTargetId(null);
      }
    };
    if (commentPostId || deleteTargetId) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [commentPostId, deleteTargetId]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpenMenuId(null);
        setShowReactionsId(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await api.get('/feed/');
      setPosts(response.data.results || response.data);
      setNextPage(response.data.next || null);
    } catch (error) {
      toast.error('Erro ao carregar feed');
    } finally {
      setIsLoading(false);
    }
  };

  const loadMorePosts = async () => {
    if (!nextPage || isLoadingMore) return;
    setIsLoadingMore(true);
    try {
      const url = nextPage.replace('/api/v1', '');
      const response = await api.get(url);
      const more = response.data.results || [];
      setPosts((prev) => [...prev, ...more]);
      setNextPage(response.data.next || null);
    } catch {
      toast.error('Erro ao carregar mais posts');
    } finally {
      setIsLoadingMore(false);
    }
  };

  const openComments = async (postId: string) => {
    setCommentPostId(postId);
    setComments([]);
    setIsLoadingComments(true);
    try {
      const response = await api.get(`/feed/${postId}/comments/`);
      setComments(response.data.results || response.data);
    } catch {
      toast.error('Erro ao carregar comentários');
    } finally {
      setIsLoadingComments(false);
    }
  };

  const submitComment = async () => {
    if (!commentPostId || !newComment.trim()) return;
    setIsSubmittingComment(true);
    try {
      await api.post(`/feed/${commentPostId}/comments/create/`, { content: newComment });
      setNewComment('');
      openComments(commentPostId);
      setPosts((prev) =>
        prev.map((p) =>
          p.id === commentPostId ? { ...p, comments_count: p.comments_count + 1 } : p
        )
      );
    } catch {
      toast.error('Erro ao enviar comentário');
    } finally {
      setIsSubmittingComment(false);
    }
  };

  const handleCreatePost = async () => {
    if (!newPost.trim()) return;
    try {
      await api.post('/feed/create/', {
        content: newPost,
        post_type: 'text',
      });
      setNewPost('');
      fetchPosts();
      toast.success('Post criado!');
    } catch (error) {
      toast.error('Erro ao criar post');
    }
  };

  const handleLike = async (postId: string) => {
    const prev = posts;
    setPosts((p) =>
      p.map((post) =>
        post.id === postId
          ? {
              ...post,
              is_liked: !post.is_liked,
              likes_count: post.is_liked ? post.likes_count - 1 : post.likes_count + 1,
            }
          : post
      )
    );
    try {
      await api.post(`/feed/${postId}/like/`);
    } catch {
      setPosts(prev);
      toast.error('Erro ao curtir');
    }
  };

  const handleReaction = async (postId: string, reaction: string) => {
    setShowReactionsId(null);
    const prev = posts;
    setPosts((p) =>
      p.map((post) =>
        post.id === postId
          ? { ...post, is_liked: true, likes_count: post.likes_count + 1 }
          : post
      )
    );
    try {
      await api.post(`/feed/${postId}/like/`, { reaction });
    } catch {
      setPosts(prev);
      toast.error('Erro ao reagir');
    }
  };

  const handleDelete = async () => {
    if (!deleteTargetId) return;
    const deletedId = deleteTargetId;
    const prev = posts;
    setPosts((p) => p.filter((post) => post.id !== deletedId));
    setDeleteTargetId(null);
    setOpenMenuId(null);
    try {
      await api.delete(`/feed/${deletedId}/`);
      toast.success('Post excluído!');
    } catch {
      setPosts(prev);
      toast.error('Erro ao excluir post');
    }
  };

  const handleEdit = async (postId: string) => {
    if (!editContent.trim()) return;
    const prevContent = posts.find((p) => p.id === postId)?.content || '';
    const newContent = editContent;
    setEditingPostId(null);
    setEditContent('');
    setPosts((p) =>
      p.map((post) => (post.id === postId ? { ...post, content: newContent } : post))
    );
    try {
      await api.patch(`/feed/${postId}/`, { content: newContent });
      toast.success('Post atualizado!');
    } catch {
      setPosts((p) =>
        p.map((post) => (post.id === postId ? { ...post, content: prevContent } : post))
      );
      toast.error('Erro ao editar post');
    }
  };

  const handleShare = async (postId: string) => {
    const url = `${window.location.origin}/feed#${postId}`;
    try {
      await navigator.clipboard.writeText(url);
      await api.post(`/feed/${postId}/share/`);
      setPosts(prev => prev.map(p =>
        p.id === postId ? { ...p, shares_count: p.shares_count + 1 } : p
      ));
      toast.success('Link copiado!');
    } catch {
      toast.error('Erro ao copiar link');
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
      {/* Create post */}
      <div className="card">
        <div className="flex gap-4">
          <div className="w-10 h-10 bg-slate rounded-full flex items-center justify-center flex-shrink-0">
            {user?.avatar_url ? (
              <img src={user.avatar_url} alt="" className="w-full h-full rounded-full object-cover" />
            ) : (
              <span className="text-iris font-bold">{user?.first_name[0]}</span>
            )}
          </div>
          <div className="flex-1">
            <textarea
              value={newPost}
              onChange={(e) => setNewPost(e.target.value)}
              placeholder="Compartilhe algo com a comunidade..."
              className="w-full bg-graphite border border-slate/50 rounded-lg px-4 py-3 text-snow placeholder-muted resize-none focus:outline-none focus:border-iris"
              rows={3}
            />
            <div className="flex justify-end mt-3">
              <button
                onClick={handleCreatePost}
                disabled={!newPost.trim()}
                className="btn-primary disabled:opacity-50"
              >
                Publicar
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Posts */}
      {posts.map((post) => (
        <div key={post.id} className="card" ref={openMenuId === post.id || showReactionsId === post.id ? menuRef : undefined}>
          {/* Post header */}
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-slate rounded-full flex items-center justify-center">
              {post.author_avatar ? (
                <img src={post.author_avatar} alt="" className="w-full h-full rounded-full object-cover" />
              ) : (
                <span className="text-iris font-bold">
                  {post.author_name[0]}
                </span>
              )}
            </div>
            <div className="flex-1">
              <p className="font-medium text-snow">{post.author_name}</p>
              <p className="text-xs text-muted">
                {new Date(post.created_at).toLocaleDateString('pt-BR')}
              </p>
            </div>

            {/* 3-dot menu */}
            {String(user?.id) === String(post.author) && (
              <div className="relative">
                <button
                  onClick={() => setOpenMenuId(openMenuId === post.id ? null : post.id)}
                  className="p-1 text-muted hover:text-snow transition-colors rounded-lg hover:bg-slate/50"
                >
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01" />
                  </svg>
                </button>
                {openMenuId === post.id && (
                  <div className="absolute right-0 top-8 w-48 bg-obsidian border border-slate/50 rounded-xl shadow-xl z-10 py-2">
                    <button
                      onClick={() => { setOpenMenuId(null); setEditingPostId(post.id); setEditContent(post.content); }}
                      className="w-full px-4 py-2 text-left text-sm text-snow hover:bg-slate/50 flex items-center gap-2"
                    >
                      Editar
                    </button>
                    <hr className="border-slate/50 my-1" />
                    <button
                      onClick={() => { setOpenMenuId(null); setDeleteTargetId(post.id); }}
                      className="w-full px-4 py-2 text-left text-sm text-crimson hover:bg-crimson/10 flex items-center gap-2"
                    >
                      <span>🗑️</span> Excluir
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Post content (edit mode or view) */}
          {editingPostId === post.id ? (
            <div className="mb-4">
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full bg-graphite border border-iris/50 rounded-lg px-4 py-3 text-snow placeholder-muted resize-none focus:outline-none focus:border-iris"
                rows={3}
                autoFocus
              />
              <div className="flex gap-2 justify-end mt-2">
                <button
                  onClick={() => { setEditingPostId(null); setEditContent(''); }}
                  className="btn-secondary text-sm"
                >
                  Cancelar
                </button>
                <button
                  onClick={() => handleEdit(post.id)}
                  disabled={!editContent.trim()}
                  className="btn-primary text-sm disabled:opacity-50"
                >
                  Salvar
                </button>
              </div>
            </div>
          ) : (
            <p className="text-snow mb-4 whitespace-pre-wrap">{post.content}</p>
          )}

          {/* Post actions */}
          <div className="flex items-center gap-2 pt-4 border-t border-slate/50">
            {/* Like button */}
            <button
              onClick={() => handleLike(post.id)}
              className={`flex items-center gap-2 text-sm px-3 py-1.5 rounded-lg transition-colors ${
                post.is_liked ? 'text-ember bg-ember/10' : 'text-muted hover:text-ember hover:bg-ember/5'
              }`}
            >
              <span>{post.is_liked ? '❤️' : '🤍'}</span>
              <span>{post.likes_count}</span>
            </button>

            {/* Reaction picker */}
            <div className="relative">
              <button
                onClick={() => setShowReactionsId(showReactionsId === post.id ? null : post.id)}
                className="flex items-center gap-1 text-sm px-3 py-1.5 rounded-lg text-muted hover:text-iris hover:bg-iris/5 transition-colors"
              >
                <span>😀</span>
                <span className="text-xs">Reagir</span>
              </button>
              {showReactionsId === post.id && (
                <div className="absolute bottom-full left-0 mb-2 flex gap-1 bg-obsidian border border-slate/50 rounded-xl px-2 py-1 shadow-xl z-10">
                  {REACTIONS.map((r) => (
                    <button
                      key={r.emoji}
                      onClick={() => handleReaction(post.id, r.emoji)}
                      className="text-2xl hover:scale-125 transition-transform p-1"
                      title={r.label}
                    >
                      {r.emoji}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Comments */}
            <button
              onClick={() => openComments(post.id)}
              className="flex items-center gap-2 text-sm px-3 py-1.5 rounded-lg text-muted hover:text-iris hover:bg-iris/5 transition-colors"
            >
              <span>💬</span>
              <span>{post.comments_count}</span>
            </button>

            {/* Share */}
            <button
              onClick={() => handleShare(post.id)}
              className="flex items-center gap-2 text-sm px-3 py-1.5 rounded-lg text-muted hover:text-jade hover:bg-jade/5 transition-colors"
            >
              <span>🔗</span>
              <span>{post.shares_count}</span>
            </button>
          </div>
        </div>
      ))}

      {posts.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted">Nenhum post ainda. Seja o primeiro a compartilhar!</p>
        </div>
      )}

      {/* Load more */}
      {nextPage && (
        <div className="text-center py-4">
          <button
            onClick={loadMorePosts}
            disabled={isLoadingMore}
            className="btn-ghost text-iris disabled:opacity-50"
          >
            {isLoadingMore ? 'Carregando...' : 'Carregar mais posts'}
          </button>
        </div>
      )}

      {/* Delete confirmation modal */}
      {deleteTargetId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-sm p-6">
            <h3 className="text-lg font-bold text-snow mb-2">Excluir post</h3>
            <p className="text-muted mb-6">Tem certeza que deseja excluir este post? Essa ação não pode ser desfeita.</p>
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

      {/* Comments modal */}
      {commentPostId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-obsidian border border-slate/50 rounded-xl w-full max-w-lg max-h-[80vh] flex flex-col">
            <div className="p-4 border-b border-slate/50 flex items-center justify-between">
              <h3 className="text-lg font-bold text-snow">Comentários</h3>
              <button
                onClick={() => { setCommentPostId(null); setNewComment(''); }}
                className="text-muted hover:text-snow text-2xl"
              >
                &times;
              </button>
            </div>

            <div className="flex-1 overflow-auto p-4 space-y-4">
              {isLoadingComments ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-iris mx-auto"></div>
                </div>
              ) : comments.length === 0 ? (
                <p className="text-center text-muted py-8">Nenhum comentário ainda.</p>
              ) : (
                comments.map((c) => (
                  <div key={c.id} className="flex gap-3">
                    <div className="w-8 h-8 bg-slate rounded-full flex-shrink-0 flex items-center justify-center">
                      <span className="text-iris font-bold text-xs">{c.author_name[0]}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-snow">{c.author_name}</span>
                        <span className="text-xs text-muted">
                          {new Date(c.created_at).toLocaleDateString('pt-BR')}
                        </span>
                      </div>
                      <p className="text-sm text-snow/90 mt-0.5 whitespace-pre-wrap">{c.content}</p>
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="p-4 border-t border-slate/50">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submitComment(); } }}
                  placeholder="Escreva um comentário..."
                  className="flex-1 bg-graphite border border-slate/50 rounded-lg px-4 py-2 text-sm text-snow placeholder-muted focus:outline-none focus:border-iris"
                />
                <button
                  onClick={submitComment}
                  disabled={!newComment.trim() || isSubmittingComment}
                  className="btn-primary px-4 py-2 text-sm disabled:opacity-50"
                >
                  {isSubmittingComment ? '...' : 'Enviar'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

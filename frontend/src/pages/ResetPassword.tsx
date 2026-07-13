// ===========================================
// FILMERSHUB - RESET PASSWORD PAGE
// ===========================================

import { useState } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import api from '@/api/client';

interface ResetFormData {
  new_password: string;
  new_password_confirm: string;
}

export default function ResetPassword() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token') || '';
  const email = searchParams.get('email') || '';
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [resetDone, setResetDone] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetFormData>();

  const onSubmit = async (data: ResetFormData) => {
    if (!token || !email) {
      toast.error('Link inválido ou expirado');
      return;
    }
    setIsLoading(true);
    try {
      await api.post('/auth/reset-password/', {
        token,
        email,
        new_password: data.new_password,
        new_password_confirm: data.new_password_confirm,
      });
      setResetDone(true);
      toast.success('Senha redefinida com sucesso!');
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Erro ao redefinir senha';
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-void">
      {/* Header */}
      <header className="border-b border-slate/50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-iris rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">F</span>
            </div>
            <span className="text-xl font-bold text-snow">
              Filmers<span className="text-iris">Hub</span>
            </span>
          </Link>
          <Link to="/" className="btn-ghost text-sm">
            ← Página Inicial
          </Link>
        </div>
      </header>

      <div className="flex items-center justify-center px-4 py-16">
      <div className="w-full max-w-md">

        <div className="card">
          {!resetDone ? (
            <>
              <h1 className="text-2xl font-bold text-snow mb-2">Redefinir Senha</h1>
              <p className="text-muted mb-6">
                Digite sua nova senha abaixo.
              </p>

              {!token || !email ? (
                <div className="text-center py-4">
                  <p className="text-crimson mb-4">Link inválido ou expirado.</p>
                  <Link to="/forgot-password" className="btn-primary inline-block">
                    Solicitar novo link
                  </Link>
                </div>
              ) : (
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-2">
                      Nova Senha
                    </label>
                    <div className="relative">
                      <input
                        type={showPassword ? 'text' : 'password'}
                        className="input pr-12"
                        placeholder="Mínimo 8 caracteres"
                        {...register('new_password', {
                          required: 'Senha é obrigatória',
                          minLength: {
                            value: 8,
                            message: 'Senha deve ter pelo menos 8 caracteres',
                          },
                        })}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-snow transition-colors"
                        tabIndex={-1}
                      >
                        {showPassword ? (
                          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                          </svg>
                        ) : (
                          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        )}
                      </button>
                    </div>
                    {errors.new_password && (
                      <p className="mt-1 text-sm text-crimson">{errors.new_password.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-snow mb-2">
                      Confirmar Nova Senha
                    </label>
                    <div className="relative">
                      <input
                        type={showConfirm ? 'text' : 'password'}
                        className="input pr-12"
                        placeholder="Repita a nova senha"
                        {...register('new_password_confirm', {
                          required: 'Confirmação é obrigatória',
                          validate: (value) =>
                            value === watch('new_password') || 'Senhas não conferem',
                        })}
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirm(!showConfirm)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-snow transition-colors"
                        tabIndex={-1}
                      >
                        {showConfirm ? (
                          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                          </svg>
                        ) : (
                          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        )}
                      </button>
                    </div>
                    {errors.new_password_confirm && (
                      <p className="mt-1 text-sm text-crimson">{errors.new_password_confirm.message}</p>
                    )}
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full btn-primary py-3 disabled:opacity-50"
                  >
                    {isLoading ? 'Redefinindo...' : 'Redefinir Senha'}
                  </button>
                </form>
              )}
            </>
          ) : (
            <div className="text-center py-4">
              <div className="w-16 h-16 bg-jade/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-jade" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-xl font-bold text-snow mb-2">Senha redefinida!</h2>
              <p className="text-muted mb-6">
                Sua senha foi alterada com sucesso. Faça login com a nova senha.
              </p>
              <button onClick={() => navigate('/login')} className="btn-primary">
                Ir para o Login
              </button>
            </div>
          )}
        </div>
      </div>
      </div>
    </div>
  );
}

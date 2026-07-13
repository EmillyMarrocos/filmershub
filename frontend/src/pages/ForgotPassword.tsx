// ===========================================
// FILMERSHUB - FORGOT PASSWORD PAGE
// ===========================================

import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import api from '@/api/client';

interface ForgotFormData {
  email: string;
}

export default function ForgotPassword() {
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotFormData>();

  const onSubmit = async (data: ForgotFormData) => {
    setIsLoading(true);
    try {
      await api.post('/auth/forgot-password/', data);
      setEmailSent(true);
      toast.success('Email de redefinição enviado!');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao enviar email';
      toast.error(message);
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
          {!emailSent ? (
            <>
              <h1 className="text-2xl font-bold text-snow mb-2">Esqueceu a senha?</h1>
              <p className="text-muted mb-6">
                Digite seu email e enviaremos um link para redefinir sua senha.
              </p>

              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-snow mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    className="input"
                    placeholder="seu@email.com"
                    {...register('email', {
                      required: 'Email é obrigatório',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Email inválido',
                      },
                    })}
                  />
                  {errors.email && (
                    <p className="mt-1 text-sm text-crimson">{errors.email.message}</p>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full btn-primary py-3 disabled:opacity-50"
                >
                  {isLoading ? 'Enviando...' : 'Enviar Link de Redefinição'}
                </button>
              </form>
            </>
          ) : (
            <div className="text-center py-4">
              <div className="w-16 h-16 bg-jade/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-jade" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h2 className="text-xl font-bold text-snow mb-2">Email enviado!</h2>
              <p className="text-muted mb-6">
                Verifique sua caixa de entrada e siga as instruções para redefinir sua senha.
              </p>
              <Link to="/login" className="btn-primary inline-block">
                Voltar ao Login
              </Link>
            </div>
          )}

          <div className="mt-6 text-center">
            <Link to="/login" className="text-sm text-iris hover:text-iris/80">
              ← Voltar ao login
            </Link>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}

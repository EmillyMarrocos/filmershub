// ===========================================
// FILMERSHUB - REGISTER PAGE
// ===========================================

import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';

interface RegisterFormData {
  first_name: string;
  last_name: string;
  email: string;
  profile_type: 'videomaker' | 'client' | 'both';
  password: string;
  password_confirm: string;
}

export default function Register() {
  const navigate = useNavigate();
  const { register: registerUser, isAuthenticated } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/feed', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    trigger,
    formState: { errors },
  } = useForm<RegisterFormData>({
    defaultValues: {
      profile_type: 'both',
    },
  });

  const profileType = watch('profile_type');

  const handleNext = async () => {
    const valid = await trigger(['first_name', 'last_name', 'email', 'password', 'password_confirm']);
    if (valid) {
      setStep(2);
    }
  };

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    try {
      await registerUser(data);
      toast.success('Conta criada com sucesso!');
      navigate('/feed');
    } catch (error: any) {
      const respData = error.response?.data;
      let message = 'Erro ao criar conta';
      if (respData) {
        if (respData.detail) {
          message = respData.detail;
        } else {
          const fieldNames: Record<string, string> = {
            email: 'Email',
            first_name: 'Nome',
            last_name: 'Sobrenome',
            password: 'Senha',
            password_confirm: 'Confirmação de senha',
            profile_type: 'Tipo de perfil',
          };
          const errs = Object.entries(respData)
            .map(([field, msgs]: [string, any]) => {
              const label = fieldNames[field] || field;
              return `${label}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`;
            })
            .join(' | ');
          message = errs;
        }
      } else if (error.message) {
        message = error.message;
      }
      toast.error(message);
    } finally {
      setIsLoading(false);
    }
  };

  const profileOptions = [
    {
      value: 'videomaker' as const,
      label: 'Videomaker',
      description: 'Quero mostrar meu trabalho e encontrar clientes',
      icon: '🎬',
      color: 'bg-iris/20',
    },
    {
      value: 'client' as const,
      label: 'Cliente',
      description: 'Quero contratar videomakers para meus projetos',
      icon: '💼',
      color: 'bg-ember/20',
    },
    {
      value: 'both' as const,
      label: 'Ambos',
      description: 'Sou videomaker e também contrato outros profissionais',
      icon: '🤝',
      color: 'bg-jade/20',
    },
  ];

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
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-snow">Criar Conta</h1>
          <p className="text-muted mt-2">Junte-se à comunidade de videomakers</p>
        </div>

        {/* Form */}
        <div className="card">
          <h1 className="text-2xl font-bold text-snow mb-6">Criar Conta</h1>

          {/* Progress steps */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                step >= 1 ? 'bg-iris text-white' : 'bg-slate text-muted'
              }`}>
                1
              </div>
              <span className="text-sm text-muted hidden sm:block">Dados Pessoais</span>
            </div>
            <div className="flex-1 h-1 bg-slate mx-4">
              <div className={`h-full bg-iris transition-all ${step >= 2 ? 'w-full' : 'w-0'}`} />
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                step >= 2 ? 'bg-iris text-white' : 'bg-slate text-muted'
              }`}>
                2
              </div>
              <span className="text-sm text-muted hidden sm:block">Tipo de Perfil</span>
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* Hidden register for profile_type */}
            <input type="hidden" {...register('profile_type')} />

            {step === 1 && (
              <>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-snow mb-2">
                      Nome
                    </label>
                    <input
                      type="text"
                      className="input"
                      placeholder="Seu nome"
                      {...register('first_name', {
                        required: 'Nome é obrigatório',
                      })}
                    />
                    {errors.first_name && (
                      <p className="mt-1 text-sm text-crimson">{errors.first_name.message}</p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-snow mb-2">
                      Sobrenome
                    </label>
                    <input
                      type="text"
                      className="input"
                      placeholder="Seu sobrenome"
                      {...register('last_name', {
                        required: 'Sobrenome é obrigatório',
                      })}
                    />
                    {errors.last_name && (
                      <p className="mt-1 text-sm text-crimson">{errors.last_name.message}</p>
                    )}
                  </div>
                </div>

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

                <div>
                  <label className="block text-sm font-medium text-snow mb-2">
                    Senha
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      className="input pr-12"
                      placeholder="Mínimo 8 caracteres"
                      {...register('password', {
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
                  {errors.password && (
                    <p className="mt-1 text-sm text-crimson">{errors.password.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-snow mb-2">
                    Confirmar Senha
                  </label>
                  <div className="relative">
                    <input
                      type={showConfirm ? 'text' : 'password'}
                      className="input pr-12"
                      placeholder="Repita a senha"
                      {...register('password_confirm', {
                        required: 'Confirmação de senha é obrigatória',
                        validate: (value) =>
                          value === watch('password') || 'Senhas não conferem',
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
                  {errors.password_confirm && (
                    <p className="mt-1 text-sm text-crimson">{errors.password_confirm.message}</p>
                  )}
                </div>

                <button
                  type="button"
                  onClick={handleNext}
                  className="w-full btn-primary py-3"
                >
                  Próximo
                </button>
              </>
            )}

            {step === 2 && (
              <>
                <div>
                  <label className="block text-sm font-medium text-snow mb-4">
                    Como você quer usar o FilmersHub?
                  </label>
                  <div className="space-y-3">
                    {profileOptions.map((opt) => (
                      <button
                        key={opt.value}
                        type="button"
                        onClick={() => setValue('profile_type', opt.value, { shouldValidate: true })}
                        className={`w-full p-4 rounded-xl cursor-pointer transition-all text-left border-2 ${
                          profileType === opt.value
                            ? 'border-iris bg-iris/5'
                            : 'border-slate/50 bg-obsidian hover:border-slate'
                        }`}
                      >
                        <div className="flex items-center gap-4">
                          <div className={`w-12 h-12 ${opt.color} rounded-lg flex items-center justify-center flex-shrink-0`}>
                            <span className="text-2xl">{opt.icon}</span>
                          </div>
                          <div>
                            <p className="font-medium text-snow">{opt.label}</p>
                            <p className="text-sm text-muted">{opt.description}</p>
                          </div>
                          {profileType === opt.value && (
                            <div className="ml-auto w-6 h-6 bg-iris rounded-full flex items-center justify-center flex-shrink-0">
                              <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                              </svg>
                            </div>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex gap-4">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="flex-1 btn-secondary py-3"
                  >
                    Voltar
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1 btn-primary py-3 disabled:opacity-50"
                  >
                    {isLoading ? 'Criando...' : 'Criar Conta'}
                  </button>
                </div>
              </>
            )}
          </form>

          <div className="mt-6 text-center">
            <p className="text-muted">
              Já tem uma conta?{' '}
              <Link to="/login" className="text-iris hover:text-iris/80">
                Entrar
              </Link>
            </p>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}

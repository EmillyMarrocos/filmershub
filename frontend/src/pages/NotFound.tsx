import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-void flex items-center justify-center px-4">
      <div className="text-center">
        <div className="text-8xl font-bold text-iris mb-4">404</div>
        <h1 className="text-2xl font-bold text-snow mb-2">Página não encontrada</h1>
        <p className="text-muted mb-8">
          O endereço que você procurou não existe ou foi movido.
        </p>
        <Link to="/" className="btn-primary">
          Voltar ao Início
        </Link>
      </div>
    </div>
  );
}

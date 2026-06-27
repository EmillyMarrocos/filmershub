🎬 FilmersHub
Uma plataforma social e hub de negócios para a comunidade de videomakers.

O FilmersHub é uma plataforma full-stack desenvolvida para conectar, apoiar e profissionalizar videomakers. Mais do que um agregador de portfólios, o sistema funciona como uma ferramenta de gestão e uma comunidade ativa. Ele permite que criadores exponham seus trabalhos, troquem conhecimentos em tempo real, organizem suas agendas e gerem contratos profissionais de forma automatizada.

🎯 O Problema que Resolvemos
Videomakers independentes frequentemente enfrentam dificuldades em três frentes:

Atração de Clientes: Dependência exclusiva do Instagram, sem um portfólio web estruturado e focado em conversão.
Gestão do Negócio: Dificuldade em precificar serviços, montar orçamentos e redigir contratos profissionais.
Comunidade: Falta de um espaço focado para trocar experiências técnicas (equipamentos, edição) e de mercado com outros profissionais.
O FilmersHub centraliza a solução para essas dores, unindo uma vitrine para clientes a um painel de ferramentas e networking para o criador.

✨ Principais Funcionalidades
Portfólios Dinâmicos: Perfis customizáveis por videomaker com bio, localização, nichos de atuação e galeria de vídeos.
Comunidade & Feed de Dicas: Timeline para membros compartilharem insights diários, com sistema de comentários.
Chat em Tempo Real: Canais de discussão temáticos (#precificação, #equipamentos, #edição) via WebSockets.
Geração de Contratos Automática: Criação de contratos em PDF baseada nos dados do cliente e escopo do projeto, prontos para envio.
Gestão de Agenda e Preços: Tabela de referência de preços e calendário de disponibilidade integrado ao perfil.
Moderação Inteligente: Sistema de permissões dividido entre Videomakers (membros), Clientes (visitantes) e Administradores (moderação).
🚀 Stack Tecnológica
O projeto foi construído focando em escalabilidade, performance e dados em tempo real:

Backend & Infraestrutura

Python / Django: Lógica de negócios e ORM.
Django REST Framework (DRF): Construção da API RESTful.
Django Channels + Redis: Gerenciamento de conexões WebSocket para o chat em tempo real.
PostgreSQL: Banco de dados relacional para estruturação robusta de usuários e conteúdos.
Docker & Docker Compose: Containerização do ambiente de desenvolvimento.
Frontend & Mídia

React / Next.js: Interface de usuário reativa, dinâmica e amigável a SEO.
Cloudinary API: Gerenciamento e otimização de upload de mídias (vídeos e imagens).
⚙️ Como Executar Localmente
Pré-requisitos
Docker e Docker Compose instalados na sua máquina.
Passos
Clone o repositório:
bash

git clone https://github.com/seu-usuario/filmershub.git

cd filmershub

Crie um arquivo .env na raiz do projeto baseado no .env.example e adicione suas credenciais do Cloudinary.

Suba os containers do banco de dados e do Redis:

bash

docker-compose up -d
Execute as migrações do banco de dados:

bash

python manage.py migrate
Inicie o servidor de desenvolvimento:
bash

python manage.py runserver
👨‍💻 Desenvolvido por
[Emilly Marrocos]

[[Seu LinkedIn](https://www.linkedin.com/in/emilly-marrocos-mendon%C3%A7a-ciriaco-5751b1385/)]
[[Seu Portfólio/Instagram](https://www.instagram.com/emilly.codes/)]

Este projeto foi desenvolvido como uma solução real para a comunidade de videomakers, unindo habilidades de desenvolvimento Full-Stack e o entendimento das dores do mercado audiovisual.

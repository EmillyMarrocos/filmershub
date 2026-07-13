// ===========================================
// FILMERSHUB - TIPOS TypeScript
// ===========================================

// Usuário
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  profile_type: 'videomaker' | 'client' | 'both';
  phone: string;
  avatar: string | null;
  avatar_url: string | null;
  bio: string;
  city: string;
  state: string;
  instagram: string;
  youtube: string;
  website: string;
  is_videomaker: boolean;
  is_client: boolean;
  is_following: boolean;
  followers_count: number;
  date_joined: string;
}

// Autenticação
export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  profile_type: 'videomaker' | 'client' | 'both';
}

// Portfólio
export interface Work {
  id: string;
  title: string;
  description: string;
  work_type: 'video' | 'photo' | 'mixed';
  category: string;
  category_name: string | null;
  file: string | null;
  thumbnail: string | null;
  external_url: string;
  client_name: string;
  location: string;
  equipment_used: string;
  views_count: number;
  likes_count: number;
  status: 'draft' | 'published' | 'archived';
  published_at: string | null;
  created_at: string;
  videomaker_name: string;
  videomaker: string;
  is_mine: boolean;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
}

export interface Review {
  id: string;
  reviewer: string;
  reviewer_name: string;
  videomaker: string;
  videomaker_name: string;
  work: string | null;
  rating: number;
  comment: string;
  response: string;
  responded_at: string | null;
  created_at: string;
}

// Feed
export interface Post {
  id: string;
  author: string;
  author_name: string;
  author_avatar: string | null;
  content: string;
  post_type: 'text' | 'image' | 'video' | 'link';
  media: string | null;
  link_url: string;
  link_title: string;
  likes_count: number;
  comments_count: number;
  shares_count: number;
  is_liked: boolean;
  created_at: string;
}

export interface Comment {
  id: string;
  author: string;
  author_name: string;
  content: string;
  replies: Comment[];
  likes_count: number;
  created_at: string;
}

// Chat
export interface ChatRoom {
  id: string;
  room_type: 'direct' | 'group';
  other_user: {
    id: string;
    name: string;
    avatar: string | null;
  } | null;
  last_message_content: string | null;
  unread_count: number;
  updated_at: string;
}

export interface Message {
  id: string;
  sender: string;
  sender_name: string;
  message_type: 'text' | 'image' | 'file';
  content: string;
  file: string | null;
  image: string | null;
  is_read: boolean;
  created_at: string;
}

// Agendamento
export interface Event {
  id: string;
  title: string;
  description: string;
  event_type: string;
  videomaker: string;
  videomaker_name: string;
  client: string;
  client_name: string;
  start_datetime: string;
  end_datetime: string;
  location: string;
  address: string;
  total_price: number | null;
  status: 'pending' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled';
  notes: string;
  created_at: string;
}

export interface BookingRequest {
  id: string;
  client: string;
  client_name: string;
  videomaker: string;
  videomaker_name: string;
  event_type: string;
  description: string;
  preferred_date: string;
  preferred_time: string;
  estimated_duration: string;
  location: string;
  budget: number | null;
  status: 'pending' | 'accepted' | 'declined' | 'expired';
  decline_reason: string;
  responded_at: string | null;
  created_at: string;
}

// Contrato
export interface Contract {
  id: string;
  contract_number: string;
  client: string;
  client_name: string;
  videomaker: string;
  videomaker_name: string;
  service_type: string;
  service_description: string;
  event_date: string;
  delivery_date: string;
  location: string;
  total_value: number;
  payment_method: string;
  status: 'draft' | 'pending_signature' | 'signed' | 'in_progress' | 'completed' | 'cancelled';
  client_signed: boolean;
  videomaker_signed: boolean;
  pdf_file: string | null;
  content_hash: string;
  clauses: ContractClause[];
  created_at: string;
}

export interface ContractClause {
  id: number;
  clause_type: string;
  title: string;
  content: string;
  order: number;
}

// Pagamento
export interface Payment {
  id: string;
  contract: string;
  contract_number: string;
  payer: string;
  payer_name: string;
  payee: string;
  payee_name: string;
  total_amount: number;
  platform_fee: number;
  videomaker_amount: number;
  payment_method: 'pix' | 'credit_card';
  status: 'pending' | 'processing' | 'approved' | 'rejected' | 'cancelled' | 'refunded';
  mp_payment_id: string;
  card_last_four: string;
  paid_at: string | null;
  created_at: string;
}

// Notificação
export interface Notification {
  id: string;
  notification_type: string;
  title: string;
  message: string;
  link: string;
  is_read: boolean;
  created_at: string;
}

// API Response
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

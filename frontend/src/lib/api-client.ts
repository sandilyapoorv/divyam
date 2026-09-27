/**
 * DIVYAM Typed API Client
 * Connecting Next.js Frontend to FastAPI Backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  designation: string;
  cadre_role_id: string;
  is_active: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface CompetencyGapItem {
  competency_id: string;
  competency_name: string;
  competency_type: string;
  current_level: number;
  target_level: number;
  gap: number;
  criticality_weight: number;
  priority_score: number;
}

export interface RadarDataPoint {
  subject: string;
  current: number;
  target: number;
  fullMark: number;
}

export interface GapAnalysisResponse {
  user_id: string;
  cadre_role_id: string;
  readiness_index: number;
  gaps: CompetencyGapItem[];
  radar_data: RadarDataPoint[];
}

export interface IgotCourse {
  id: string;
  title: string;
  provider: string;
  duration_hours: number;
  course_url: string;
  description: string;
  target_level: number;
  thumbnail_url?: string;
  is_certified?: boolean;
}

export interface RecommendationItem {
  course: IgotCourse;
  competency_id: string;
  competency_name: string;
  gap: number;
  priority_level: string;
}

export interface IgotRecommendationsResponse {
  user_id: string;
  total_recommendations: number;
  recommendations: RecommendationItem[];
}

export interface DocumentItem {
  id: string;
  title: string;
  file_name: string;
  file_type: string;
  file_size_bytes: number;
  description?: string;
  competency_id?: string;
  is_indexed: boolean;
  total_chunks: number;
  created_at: string;
}

export interface QuestionCitation {
  document_id: string;
  document_title: string;
  page_number: number;
  section_heading?: string;
  quote_snippet?: string;
}

export interface QuizQuestionItem {
  id: string;
  question_text: string;
  options: string[];
  bloom_level: string; // Remembering | Understanding | Applying | Analyzing
  competency_id: string;
  explanation?: string;
  citation?: QuestionCitation;
}

export interface QuizItem {
  id: string;
  title: string;
  document_id: string;
  competency_id?: string;
  total_questions: number;
  pass_threshold_percentage: number;
  questions?: QuizQuestionItem[];
  created_at: string;
}

export interface QuestionGradingResult {
  question_index: number;
  question_text: string;
  selected_option: number;
  correct_option: number;
  is_correct: boolean;
  bloom_level: string;
  competency_id: string;
  explanation: string;
  citation?: QuestionCitation;
}

export interface QuizSubmitResult {
  quiz_id: string;
  user_id: string;
  total_questions: number;
  correct_count: number;
  score_percentage: number;
  is_passing: boolean;
  question_results: QuestionGradingResult[];
  competency_score_updates: Record<string, number>;
}

export interface CadreRole {
  id: string;
  code: string;
  name: string;
  description: string;
}

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('divyam_token');
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('divyam_token', token);
    }
  }

  getToken(): string | null {
    return this.token;
  }

  logout() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('divyam_token');
    }
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorText = await response.text();
      let errorJson;
      try {
        errorJson = JSON.parse(errorText);
      } catch {
        errorJson = { detail: errorText };
      }
      throw new Error(errorJson.detail || `Request failed with status ${response.status}`);
    }

    return response.json() as Promise<T>;
  }

  // --- Auth API ---
  async login(email: string, password: string): Promise<AuthResponse> {
    const res = await this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(res.access_token);
    return res;
  }

  async getMe(): Promise<User> {
    return this.request<User>('/auth/me');
  }

  // --- Competencies API ---
  async getRoles(): Promise<CadreRole[]> {
    return this.request<CadreRole[]>('/competencies/roles');
  }

  async getGapAnalysis(userId?: string): Promise<GapAnalysisResponse> {
    const query = userId ? `?user_id=${encodeURIComponent(userId)}` : '';
    return this.request<GapAnalysisResponse>(`/competencies/gap-analysis${query}`);
  }

  async submitDiagnostic(userId: string, answers: Record<string, number>): Promise<{
    user_id: string;
    readiness_index: number;
    updated_scores: Record<string, number>;
    message: string;
  }> {
    return this.request('/competencies/diagnostic', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, answers }),
    });
  }

  // --- iGOT Karmayogi API ---
  async getRecommendations(userId?: string): Promise<IgotRecommendationsResponse> {
    const query = userId ? `?user_id=${encodeURIComponent(userId)}` : '';
    return this.request<IgotRecommendationsResponse>(`/igot/recommendations${query}`);
  }

  async getCatalog(competencyId?: string): Promise<IgotCourse[]> {
    const query = competencyId ? `?competency_id=${encodeURIComponent(competencyId)}` : '';
    return this.request<IgotCourse[]>(`/igot/catalog${query}`);
  }

  // --- Documents / RAG API ---
  async uploadDocument(formData: FormData): Promise<DocumentItem> {
    return this.request<DocumentItem>('/documents/upload', {
      method: 'POST',
      body: formData,
    });
  }

  async getDocuments(): Promise<DocumentItem[]> {
    return this.request<DocumentItem[]>('/documents');
  }

  async getDocument(docId: string): Promise<DocumentItem> {
    return this.request<DocumentItem>(`/documents/${docId}`);
  }

  // --- Quizzes API ---
  async generateQuiz(payload: {
    document_id: string;
    title: string;
    num_questions?: number;
    bloom_distribution?: Record<string, number>;
  }): Promise<QuizItem> {
    return this.request<QuizItem>('/quizzes/generate', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async getQuizzes(competencyId?: string, documentId?: string): Promise<QuizItem[]> {
    const params = new URLSearchParams();
    if (competencyId) params.append('competency_id', competencyId);
    if (documentId) params.append('document_id', documentId);
    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request<QuizItem[]>(`/quizzes${query}`);
  }

  async getQuiz(quizId: string): Promise<QuizItem> {
    return this.request<QuizItem>(`/quizzes/${quizId}`);
  }

  async submitQuiz(quizId: string, userId: string, answers: Record<number, number>): Promise<QuizSubmitResult> {
    return this.request<QuizSubmitResult>(`/quizzes/${quizId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, answers }),
    });
  }
}

export const api = new ApiClient(API_BASE);

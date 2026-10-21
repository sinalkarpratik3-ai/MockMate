export interface User {
  id: number;
  email: string;
  full_name?: string | null;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface MCQOption {
  key: string;
  text: string;
}

export interface Question {
  id: number;
  interview_id?: number | null;
  question_text: string;
  role: string;
  round_number?: number | null;
  difficulty: string;
  topic: string;
  question_type: "mcq" | "text";
  options?: MCQOption[] | null;
  correct_option?: string | null;
  explanation?: string | null;
  model_answer?: string | null;
  created_at: string;
}

export interface Answer {
  id: number;
  interview_id: number;
  question_id: number;
  selected_option?: string | null;
  text_answer?: string | null;
  is_correct?: boolean | null;
  score: number;
  feedback?: string | null;
  strengths?: string[] | null;
  missing_concepts?: string[] | null;
  improvement_tips?: string[] | null;
  model_answer?: string | null;
  evaluated_at: string;
}

export interface Interview {
  id: number;
  user_id: number;
  job_role: string;
  difficulty: string;
  current_round?: number | null;
  current_difficulty?: string | null;
  mode: "mcq" | "text";
  num_questions: number;
  status: "in_progress" | "completed";
  total_score: number;
  max_score: number;
  percentage: number;
  created_at: string;
  completed_at?: string | null;
  questions?: Question[];
  answers?: Answer[];
}

export interface WeakTopicItem {
  topic: string;
  role: string;
  attempts: number;
  accuracy_percentage: number;
  avg_score: number;
  recommendation: string;
}

export interface RoleStat {
  role: string;
  interviews_count: number;
  avg_score_pct: number;
}

export interface DifficultyStat {
  difficulty: string;
  count: number;
  avg_score_pct: number;
}

export interface PerformanceTrend {
  date: string;
  score_percentage: number;
  mode: string;
  role: string;
}

export interface DashboardSummary {
  total_interviews: number;
  total_questions_attempted: number;
  mcq_accuracy_pct: number;
  avg_text_score: number;
  recent_interviews: Interview[];
  weak_topics: WeakTopicItem[];
  role_stats: RoleStat[];
  difficulty_stats: DifficultyStat[];
  performance_trends: PerformanceTrend[];
  has_attempted_daily: boolean;
}

export interface BookmarkItem {
  id: number;
  user_id: number;
  question_id: number;
  created_at: string;
  question: Question;
}

export interface DailyQuestion {
  id: number;
  question_id?: number;
  date: string;
  question_text: string;
  role: string;
  difficulty: string;
  topic: string;
  question_type: "mcq" | "text";
  options?: MCQOption[] | null;
  has_attempted: boolean;
  is_bookmarked?: boolean;
  user_attempt?: {
    id: number;
    submitted_answer: string;
    is_correct?: boolean | null;
    score: number;
    feedback?: string | null;
    correct_option?: string | null;
    explanation?: string | null;
    model_answer?: string | null;
    created_at: string;
  } | null;
}

export interface NewsSource {
  id: number;
  name: string;
  domain: string;
  description?: string;
  known_bias?: 'left' | 'center-left' | 'center' | 'center-right' | 'right';
  country: string;
  language: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Article {
  id: number;
  source_id: number;
  title: string;
  content: string;
  author?: string;
  published_date: string;
  url: string;
  image_url?: string;
  summary?: string;
  category?: string;
  view_count: number;
  created_at: string;
  updated_at: string;
}

export interface BiasAnalysis {
  id: number;
  article_id: number;
  bias_score: number; // -1.00 to 1.00
  bias_label: 'left' | 'center-left' | 'center' | 'center-right' | 'right';
  confidence_score: number; // 0.00 to 1.00
  analysis_method?: string;
  key_indicators?: string[];
  analyzed_at: string;
}

export interface ArticleWithBias extends Article {
  source_name: string;
  source_bias?: 'left' | 'center-left' | 'center' | 'center-right' | 'right';
  bias_score?: number;
  bias_label?: 'left' | 'center-left' | 'center' | 'center-right' | 'right';
  confidence_score?: number;
}

export interface BiasStats {
  total_articles: number;
  analyzed_articles: number;
  bias_distribution: Record<string, number>;
}
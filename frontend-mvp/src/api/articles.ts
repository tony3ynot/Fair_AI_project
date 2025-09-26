import { apiClient } from './client';
import { ArticleWithBias } from '../types/article';

export interface ArticleFilters {
  skip?: number;
  limit?: number;
  category?: string;
  bias_label?: string;
  source_id?: number;
  date_from?: string;
  date_to?: string;
}

export const articlesApi = {
  getArticles: async (filters: ArticleFilters = {}) => {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    
    const { data } = await apiClient.get<ArticleWithBias[]>(`/articles?${params}`);
    return data;
  },

  getArticle: async (id: number) => {
    const { data } = await apiClient.get<ArticleWithBias>(`/articles/${id}`);
    return data;
  },

  getRelatedArticles: async (id: number, relation_type?: string, limit: number = 5) => {
    const params = new URLSearchParams();
    if (relation_type) params.append('relation_type', relation_type);
    params.append('limit', String(limit));
    
    const { data } = await apiClient.get<ArticleWithBias[]>(`/articles/${id}/related?${params}`);
    return data;
  },
};
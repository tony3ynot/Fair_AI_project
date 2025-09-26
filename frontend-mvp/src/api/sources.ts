import { apiClient } from './client';
import { NewsSource } from '../types/article';

export const sourcesApi = {
  getSources: async (bias?: string, isActive?: boolean) => {
    const params = new URLSearchParams();
    if (bias) params.append('bias', bias);
    if (isActive !== undefined) params.append('is_active', String(isActive));
    
    const { data } = await apiClient.get<NewsSource[]>(`/news-sources?${params}`);
    return data;
  },

  getSource: async (id: number) => {
    const { data } = await apiClient.get<NewsSource>(`/news-sources/${id}`);
    return data;
  },
};
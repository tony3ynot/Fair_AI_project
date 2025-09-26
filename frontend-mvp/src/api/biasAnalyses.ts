import { apiClient } from './client';
import { BiasStats } from '../types/article';

export const biasApi = {
  getStats: async () => {
    const { data } = await apiClient.get<BiasStats>('/bias-analyses/stats');
    return data;
  },
};
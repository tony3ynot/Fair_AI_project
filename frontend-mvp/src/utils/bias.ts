export const biasLabels: Record<string, string> = {
  'left': '좌파',
  'center-left': '중도좌파',
  'center': '중도',
  'center-right': '중도우파',
  'right': '우파',
};

export const biasColors: Record<string, string> = {
  'left': '#1e40af',      // blue-800
  'center-left': '#3b82f6', // blue-500
  'center': '#6b7280',      // gray-500
  'center-right': '#f59e0b', // amber-500
  'right': '#dc2626',       // red-600
};

export const biasScoreToLabel = (score: number): string => {
  if (score <= -0.6) return 'left';
  if (score <= -0.2) return 'center-left';
  if (score <= 0.2) return 'center';
  if (score <= 0.6) return 'center-right';
  return 'right';
};

export const getBiasColor = (bias?: string): string => {
  return biasColors[bias || 'center'] || biasColors.center;
};

export const getBiasLabel = (bias?: string): string => {
  return biasLabels[bias || 'center'] || '알 수 없음';
};

export const formatConfidenceScore = (score: number): string => {
  return `${(score * 100).toFixed(0)}%`;
};
import React from 'react';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { Eye, Clock, ExternalLink } from 'lucide-react';
import { ArticleWithBias } from '../types/article';
import { BiasIndicator } from './BiasIndicator';
import { formatConfidenceScore } from '../utils/bias';

interface ArticleCardProps {
  article: ArticleWithBias;
  onClick?: () => void;
}

export const ArticleCard: React.FC<ArticleCardProps> = ({ article, onClick }) => {
  return (
    <div
      className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 p-6 cursor-pointer"
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-gray-600">{article.source_name}</span>
          {article.bias_label && (
            <BiasIndicator bias={article.bias_label} size="sm" />
          )}
        </div>
        <span className="text-xs text-gray-500">
          {format(new Date(article.published_date), 'yyyy년 MM월 dd일', { locale: ko })}
        </span>
      </div>

      <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
        {article.title}
      </h3>

      {article.summary && (
        <p className="text-gray-600 text-sm mb-4 line-clamp-3">{article.summary}</p>
      )}

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 text-xs text-gray-500">
          {article.category && (
            <span className="px-2 py-1 bg-gray-100 rounded-full">{article.category}</span>
          )}
          <span className="flex items-center gap-1">
            <Eye className="w-3 h-3" />
            {article.view_count}
          </span>
          {article.author && (
            <span className="flex items-center gap-1">
              {article.author}
            </span>
          )}
        </div>

        {article.bias_label && (
          <div className="flex items-center gap-2">
            <BiasIndicator bias={article.bias_label} size="sm" showLabel={false} />
            <span className="text-xs text-gray-500">
              신뢰도 {formatConfidenceScore(article.confidence_score || 0)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
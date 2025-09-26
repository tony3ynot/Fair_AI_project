import React from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { ArrowLeft, ExternalLink, Eye, Calendar, User, BarChart2 } from 'lucide-react';
import { articlesApi } from '../api/articles';
import { BiasIndicator } from '../components/BiasIndicator';
import { BiasSpectrum } from '../components/BiasSpectrum';
import { ArticleCard } from '../components/ArticleCard';
import { formatConfidenceScore } from '../utils/bias';

export const ArticleDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const articleId = Number(id);

  const { data: article, isLoading, error } = useQuery({
    queryKey: ['article', articleId],
    queryFn: () => articlesApi.getArticle(articleId),
    enabled: !isNaN(articleId),
  });

  const { data: relatedArticles } = useQuery({
    queryKey: ['relatedArticles', articleId],
    queryFn: () => articlesApi.getRelatedArticles(articleId, 'different_perspective', 5),
    enabled: !isNaN(articleId),
  });

  if (error || isNaN(articleId)) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-red-600">
          기사를 불러올 수 없습니다.
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="space-y-2">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        뒤로가기
      </button>

      {article && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <article className="bg-white rounded-lg shadow-sm p-8">
              <div className="mb-6">
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-lg font-medium text-gray-700">{article.source_name}</span>
                  {article.source_bias && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-gray-500">(언론사 성향:</span>
                      <BiasIndicator bias={article.source_bias} size="sm" />
                      <span className="text-xs text-gray-500">)</span>
                    </div>
                  )}
                </div>
                
                <h1 className="text-3xl font-bold text-gray-900 mb-4">{article.title}</h1>
                
                <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                  {article.author && (
                    <span className="flex items-center gap-1">
                      <User className="w-4 h-4" />
                      {article.author}
                    </span>
                  )}
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {format(new Date(article.published_date), 'yyyy년 MM월 dd일 HH:mm', { locale: ko })}
                  </span>
                  <span className="flex items-center gap-1">
                    <Eye className="w-4 h-4" />
                    {article.view_count} 조회
                  </span>
                </div>
              </div>

              {article.image_url && (
                <img
                  src={article.image_url}
                  alt={article.title}
                  className="w-full h-auto rounded-lg mb-6"
                />
              )}

              <div className="prose prose-lg max-w-none">
                {article.content.split('\n').map((paragraph, index) => (
                  <p key={index} className="mb-4 text-gray-700 leading-relaxed">
                    {paragraph}
                  </p>
                ))}
              </div>

              <div className="mt-8 pt-6 border-t border-gray-200">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800"
                >
                  원문 보기
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </article>
          </div>

          <div className="lg:col-span-1 space-y-6">
            {article.bias_label && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <BarChart2 className="w-5 h-5" />
                  편향성 분석
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-gray-600 mb-2">정치적 성향</p>
                    <BiasIndicator bias={article.bias_label} size="lg" />
                  </div>
                  
                  {article.bias_score !== undefined && (
                    <div>
                      <p className="text-sm text-gray-600 mb-2">성향 스펙트럼</p>
                      <BiasSpectrum 
                        currentBias={article.bias_label}
                        biasScore={article.bias_score}
                      />
                    </div>
                  )}
                  
                  {article.confidence_score !== undefined && (
                    <div>
                      <p className="text-sm text-gray-600 mb-1">분석 신뢰도</p>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-green-500 transition-all duration-300"
                            style={{ width: `${article.confidence_score * 100}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium">
                          {formatConfidenceScore(article.confidence_score)}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {relatedArticles && relatedArticles.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-4">다른 시각의 기사</h2>
                <div className="space-y-4">
                  {relatedArticles.map(related => (
                    <Link
                      key={related.id}
                      to={`/articles/${related.id}`}
                      className="block p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
                    >
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm font-medium">{related.source_name}</span>
                        <BiasIndicator bias={related.bias_label} size="sm" showLabel={false} />
                      </div>
                      <h3 className="text-sm font-medium text-gray-900 line-clamp-2">
                        {related.title}
                      </h3>
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
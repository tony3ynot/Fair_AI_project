import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Newspaper, Home } from 'lucide-react';
import { ArticleList } from './pages/ArticleList';
import { ArticleDetail } from './pages/ArticleDetail';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <header className="bg-white shadow-sm">
            <div className="container mx-auto px-4">
              <div className="flex items-center justify-between h-16">
                <Link to="/" className="flex items-center gap-2 text-xl font-bold text-gray-900">
                  <Newspaper className="w-6 h-6" />
                  Fair AI
                </Link>
                <nav className="flex items-center gap-6">
                  <Link
                    to="/"
                    className="text-gray-600 hover:text-gray-900 flex items-center gap-1"
                  >
                    <Home className="w-4 h-4" />
                    홈
                  </Link>
                </nav>
              </div>
            </div>
          </header>

          <main className="flex-1">
            <Routes>
              <Route path="/" element={<ArticleList />} />
              <Route path="/articles/:id" element={<ArticleDetail />} />
            </Routes>
          </main>

          <footer className="bg-gray-900 text-white py-8 mt-12">
            <div className="container mx-auto px-4">
              <div className="text-center">
                <p className="text-sm">
                  © 2025 Fair AI. 모든 뉴스 분석은 AI에 의해 자동으로 수행됩니다.
                </p>
                <p className="text-xs mt-2 text-gray-400">
                  정치적 성향 분석은 참고용이며, 개인의 판단을 대체하지 않습니다.
                </p>
              </div>
            </div>
          </footer>
        </div>
      </Router>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;
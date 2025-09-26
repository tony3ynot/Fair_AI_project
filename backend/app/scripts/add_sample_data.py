# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime, timedelta
import random
import json
from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.models import Article, NewsSource, BiasAnalysis, RelatedArticle

def add_sample_data():
    db = SessionLocal()
    
    try:
        # Check if we already have data
        if db.query(Article).count() > 0:
            print("Sample data already exists")
            return
        
        # Get news sources
        sources = db.query(NewsSource).all()
        if not sources:
            print("No news sources found. Please run the init.sql script first.")
            return
        
        # Sample articles data
        articles_data = [
            {
                "title": "정부, 새로운 경제 정책 발표 예정",
                "content": "정부가 다음 주 새로운 경제 활성화 정책을 발표할 예정이다. 이번 정책은 중소기업 지원과 일자리 창출에 중점을 둘 것으로 알려졌다.\n\n기획재정부 관계자는 '현재의 경제 상황을 고려하여 실효성 있는 대책을 마련하고 있다'고 밝혔다. 특히 청년 일자리 창출과 스타트업 지원에 많은 예산이 투입될 예정이다.\n\n전문가들은 이번 정책이 경제 회복에 긍정적인 영향을 미칠 것으로 예상하고 있다.",
                "category": "경제",
                "author": "김경제 기자",
                "bias_score": -0.3,
                "bias_label": "center-left"
            },
            {
                "title": "야당, 정부 경제 정책 강력 비판",
                "content": "야당은 정부의 새로운 경제 정책 계획에 대해 강력히 비판했다. 야당 대표는 '정부의 정책은 현실을 외면한 포퓰리즘'이라고 주장했다.\n\n야당은 정부의 재정 지출 확대가 국가 부채를 증가시킬 뿐이라며, 보다 신중한 접근이 필요하다고 강조했다. 특히 세금 인상 없이 지출만 늘리는 것은 무책임한 정책이라고 비판했다.\n\n정치 전문가들은 여야 간 경제 정책을 둘러싼 대립이 더욱 심화될 것으로 전망했다.",
                "category": "정치",
                "author": "박정치 기자",
                "bias_score": 0.4,
                "bias_label": "center-right"
            },
            {
                "title": "AI 기술 발전이 가져올 미래 변화",
                "content": "인공지능(AI) 기술의 급속한 발전이 우리 사회 전반에 큰 변화를 가져올 것으로 전망된다. 전문가들은 AI가 의료, 교육, 금융 등 다양한 분야에서 혁신을 주도할 것으로 예상한다.\n\n특히 의료 분야에서는 AI를 활용한 진단 정확도가 크게 향상되고 있으며, 맞춤형 치료가 가능해질 것으로 기대된다. 교육 분야에서도 AI 튜터를 통한 개인화된 학습이 확산될 전망이다.\n\n다만 AI 발전에 따른 일자리 변화와 윤리적 문제에 대한 사회적 논의가 필요하다는 지적도 나오고 있다.",
                "category": "기술",
                "author": "이기술 기자",
                "bias_score": 0.0,
                "bias_label": "center"
            },
            {
                "title": "기후 변화 대응, 더 이상 미룰 수 없다",
                "content": "전 세계적으로 기후 변화의 영향이 심각해지면서 즉각적인 대응이 필요하다는 목소리가 높아지고 있다. 최근 발생한 이상 기후 현상들은 기후 위기의 심각성을 보여주고 있다.\n\n환경 전문가들은 탄소 배출 감축과 재생 에너지 전환을 서둘러야 한다고 강조한다. 정부와 기업, 시민 사회가 함께 노력해야 할 때라는 지적이다.\n\n특히 젊은 세대를 중심으로 기후 행동에 대한 요구가 거세지고 있으며, 이는 정책 변화로 이어질 것으로 예상된다.",
                "category": "사회",
                "author": "최환경 기자",
                "bias_score": -0.5,
                "bias_label": "center-left"
            },
            {
                "title": "K-문화 열풍, 전 세계를 사로잡다",
                "content": "한국 문화 콘텐츠가 전 세계적으로 큰 인기를 얻으며 K-문화 열풍이 계속되고 있다. K-팝, K-드라마, K-영화 등이 글로벌 시장에서 주목받고 있다.\n\n최근 한국 영화가 국제 영화제에서 수상하고, K-팝 아티스트들이 빌보드 차트 상위권을 차지하는 등 한국 문화의 위상이 높아지고 있다. 이는 한국의 소프트파워 강화로 이어지고 있다.\n\n문화 전문가들은 K-문화의 성공 요인으로 독창성과 보편성의 조화를 꼽으며, 이러한 성공이 지속되기 위해서는 콘텐츠의 질적 향상이 중요하다고 조언했다.",
                "category": "문화",
                "author": "김문화 기자",
                "bias_score": 0.1,
                "bias_label": "center"
            },
            {
                "title": "부동산 시장, 안정세 찾아가나",
                "content": "최근 부동산 시장이 안정세를 찾아가고 있다는 분석이 나왔다. 정부의 부동산 정책과 금리 인상의 영향으로 투기 수요가 줄어들면서 시장이 안정화되고 있다.\n\n부동산 전문가들은 실수요자 중심의 시장으로 재편되고 있다고 평가했다. 다만 지역별로 편차가 있어 세심한 관찰이 필요하다고 덧붙였다.\n\n정부는 주택 공급 확대와 함께 실수요자 보호 정책을 지속적으로 추진할 계획이라고 밝혔다.",
                "category": "경제",
                "author": "박부동산 기자",
                "bias_score": -0.2,
                "bias_label": "center-left"
            },
            {
                "title": "교육 개혁, 미래를 위한 필수 과제",
                "content": "급변하는 시대에 맞춰 교육 시스템의 전면적인 개혁이 필요하다는 목소리가 높아지고 있다. 전문가들은 창의성과 비판적 사고력을 기르는 교육으로의 전환이 시급하다고 지적한다.\n\n현재의 입시 위주 교육은 4차 산업혁명 시대에 필요한 인재를 양성하는 데 한계가 있다는 비판이 제기되고 있다. 프로젝트 기반 학습, 협업 능력 강화 등 새로운 교육 방법론의 도입이 필요하다.\n\n교육부는 미래 교육 비전을 수립하고 단계적인 개혁을 추진하겠다고 밝혔다.",
                "category": "사회",
                "author": "이교육 기자",
                "bias_score": -0.4,
                "bias_label": "center-left"
            },
            {
                "title": "중소기업, 디지털 전환 가속화",
                "content": "국내 중소기업들이 디지털 전환에 속도를 내고 있다. 코로나19 이후 비대면 경제가 확산되면서 디지털 기술 도입이 생존의 필수 요소가 되었다.\n\n정부는 중소기업의 디지털 전환을 지원하기 위해 다양한 정책을 추진하고 있다. 클라우드 서비스 지원, AI 솔루션 도입 지원 등이 대표적이다.\n\n중소기업 관계자들은 디지털 전환이 경쟁력 강화의 기회가 될 것으로 기대하면서도, 전문 인력 부족과 초기 투자 비용 부담을 어려움으로 꼽았다.",
                "category": "경제",
                "author": "최디지털 기자",
                "bias_score": 0.2,
                "bias_label": "center-right"
            },
            {
                "title": "스포츠 산업, 새로운 성장 동력으로 주목",
                "content": "스포츠 산업이 새로운 경제 성장 동력으로 주목받고 있다. 프로스포츠의 인기와 함께 스포츠 관련 비즈니스가 빠르게 성장하고 있다.\n\nE스포츠, 스포츠 미디어, 스포츠 테크 등 새로운 분야가 등장하면서 스포츠 산업의 영역이 확대되고 있다. 특히 젊은 세대를 중심으로 스포츠 콘텐츠 소비가 증가하고 있다.\n\n정부와 지자체는 스포츠 산업 육성을 위한 인프라 구축과 지원 정책을 확대하고 있다.",
                "category": "스포츠",
                "author": "김스포츠 기자",
                "bias_score": 0.0,
                "bias_label": "center"
            },
            {
                "title": "국제 협력 강화, 글로벌 도전 과제 해결의 열쇠",
                "content": "기후 변화, 팬데믹, 경제 불평등 등 글로벌 도전 과제를 해결하기 위해서는 국제 협력이 필수적이라는 인식이 확산되고 있다.\n\n전문가들은 개별 국가의 노력만으로는 이러한 문제를 해결할 수 없으며, 다자간 협력 체제를 강화해야 한다고 강조한다. 특히 선진국과 개발도상국 간의 협력이 중요하다.\n\n한국도 중견국가로서 국제 사회에서 더 적극적인 역할을 수행해야 한다는 목소리가 나오고 있다.",
                "category": "국제",
                "author": "박국제 기자",
                "bias_score": -0.3,
                "bias_label": "center-left"
            }
        ]
        
        # Create articles with bias analysis
        created_articles = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i, data in enumerate(articles_data):
            # Random source
            source = random.choice(sources)
            
            # Create article
            article = Article(
                source_id=source.id,
                title=data["title"],
                content=data["content"],
                author=data.get("author"),
                published_date=base_date + timedelta(days=i*3, hours=random.randint(0, 23)),
                url=f"https://{source.domain}/news/{i+1000}",
                summary=data["content"][:200] + "...",
                category=data["category"],
                view_count=random.randint(100, 10000)
            )
            db.add(article)
            db.flush()
            
            # Create bias analysis
            bias_analysis = BiasAnalysis(
                article_id=article.id,
                bias_score=data["bias_score"],
                bias_label=data["bias_label"],
                confidence_score=random.uniform(0.7, 0.95),
                analysis_method="AI Analysis v1.0",
                key_indicators=json.dumps(["어휘 선택", "논조", "주제 선택"], ensure_ascii=False)
            )
            db.add(bias_analysis)
            
            created_articles.append(article)
        
        # Create some related articles
        for i in range(0, len(created_articles), 2):
            if i + 1 < len(created_articles):
                related = RelatedArticle(
                    article_id=created_articles[i].id,
                    related_article_id=created_articles[i+1].id,
                    relation_type="different_perspective",
                    similarity_score=random.uniform(0.6, 0.9)
                )
                db.add(related)
                
                # Add reverse relation
                related_reverse = RelatedArticle(
                    article_id=created_articles[i+1].id,
                    related_article_id=created_articles[i].id,
                    relation_type="different_perspective",
                    similarity_score=random.uniform(0.6, 0.9)
                )
                db.add(related_reverse)
        
        db.commit()
        print(f"Successfully added {len(articles_data)} sample articles with bias analysis")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
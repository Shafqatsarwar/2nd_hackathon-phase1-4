"""
Improved Competitive Analysis Skill
Advanced competitive intelligence gathering and analysis with AI-powered insights and predictive capabilities.
"""
import asyncio
import aiohttp
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime, timedelta
import re
import hashlib
from enum import Enum
import statistics
from collections import defaultdict

class CompetitorSize(Enum):
    STARTUP = "Startup"
    SMB = "Small-Medium Business"
    ENTERPRISE = "Enterprise"
    FORTUNE_500 = "Fortune 500"

class MarketPosition(Enum):
    MARKET_LEADER = "Market Leader"
    CHALLENGER = "Challenger"
    NICH_PLAYER = "Niche Player"
    EMERGING = "Emerging"

@dataclass
class CompetitorProfile:
    name: str
    domain: str
    size: CompetitorSize
    market_position: MarketPosition
    products: List[str] = field(default_factory=list)
    pricing_models: List[Dict] = field(default_factory=list)
    social_metrics: Dict[str, int] = field(default_factory=dict)
    technology_stack: List[str] = field(default_factory=list)
    funding_history: List[Dict] = field(default_factory=list)
    leadership_team: List[Dict] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recent_news: List[Dict] = field(default_factory=list)
    last_scraped: datetime = field(default_factory=datetime.now)
    threat_level: float = 0.0  # 0-1 scale
    growth_rate: float = 0.0   # percentage
    market_share: float = 0.0  # percentage

@dataclass
class IntelligenceAlert:
    id: str
    competitor_name: str
    alert_type: str  # 'new_feature', 'price_change', 'leadership_change', 'partnership', 'security_breach'
    severity: str    # 'low', 'medium', 'high', 'critical'
    message: str
    timestamp: datetime
    action_required: bool

@dataclass
class SWOTAnalysis:
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    confidence_score: float  # 0-1

@dataclass
class PredictiveInsight:
    prediction: str
    probability: float  # 0-1
    timeframe: str      # 'short_term', 'medium_term', 'long_term'
    supporting_evidence: List[str]
    confidence_score: float  # 0-1

class ImprovedCompetitiveAnalysis:
    """
    Advanced competitive intelligence system with AI-powered insights.
    """

    def __init__(self):
        self.competitors: Dict[str, CompetitorProfile] = {}
        self.alerts: List[IntelligenceAlert] = []
        self.session: Optional[aiohttp.ClientSession] = None
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.scraped_content_cache: Dict[str, str] = {}
        self.request_delays = {}  # Track delays per domain to avoid rate limiting

    async def initialize_session(self):
        """Initialize async HTTP session."""
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

    async def close_session(self):
        """Close the HTTP session."""
        if self.session:
            await self.session.close()

    def calculate_threat_level(self, profile: CompetitorProfile) -> float:
        """Calculate threat level based on multiple factors."""
        factors = []

        # Market position weighting
        position_weights = {
            MarketPosition.MARKET_LEADER: 0.9,
            MarketPosition.CHALLENGER: 0.7,
            MarketPosition.NICH_PLAYER: 0.4,
            MarketPosition.EMERGING: 0.2
        }
        factors.append(position_weights.get(profile.market_position, 0.3))

        # Size weighting
        size_weights = {
            CompetitorSize.ENTERPRISE: 0.8,
            CompetitorSize.FORTUNE_500: 1.0,
            CompetitorSize.SMB: 0.5,
            CompetitorSize.STARTUP: 0.3
        }
        factors.append(size_weights.get(profile.size, 0.4))

        # Growth rate (if available)
        if profile.growth_rate > 0:
            factors.append(min(profile.growth_rate / 100, 1.0))  # Cap at 1.0

        # Social metrics (if available)
        if profile.social_metrics:
            avg_followers = statistics.mean(profile.social_metrics.values()) if profile.social_metrics.values() else 0
            # Normalize followers to 0-1 scale (assuming 1M as max for normalization)
            normalized_followers = min(avg_followers / 1000000, 1.0)
            factors.append(normalized_followers)

        # Calculate weighted average
        weights = [0.3, 0.25, 0.25, 0.2]  # Adjust weights as needed
        threat_level = sum(w * f for w, f in zip(weights[:len(factors)], factors))

        return min(threat_level, 1.0)

    async def scrape_website_content(self, url: str) -> Optional[str]:
        """Scrape website content with rate limiting."""
        domain = re.findall(r'https?://([^/]+)', url)[0] if re.findall(r'https?://([^/]+)', url) else 'unknown'

        # Implement rate limiting
        last_request = self.request_delays.get(domain, 0)
        time_since_last = time.time() - last_request
        if time_since_last < 2:  # Minimum 2 seconds between requests to same domain
            await asyncio.sleep(2 - time_since_last)

        if not self.session:
            await self.initialize_session()

        headers = {
            'User-Agent': self.user_agents[hash(url) % len(self.user_agents)],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    self.request_delays[domain] = time.time()

                    # Cache content to avoid repeated scraping
                    content_hash = hashlib.md5(content.encode()).hexdigest()
                    self.scraped_content_cache[content_hash] = content

                    return content
                else:
                    print(f"Failed to scrape {url}: Status {response.status}")
                    return None
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def extract_technology_stack(self, html_content: str) -> List[str]:
        """Extract technology stack from HTML content."""
        technologies = set()

        # Look for common technology indicators in HTML
        tech_patterns = {
            'javascript_frameworks': [
                r'<script[^>]*src=["\'][^"\']*react[^"\']*["\']',
                r'<script[^>]*src=["\'][^"\']*vue[^"\']*["\']',
                r'<script[^>]*src=["\'][^"\']*angular[^"\']*["\']',
            ],
            'analytics': [
                r'google-analytics',
                r'googletagmanager',
                r'facebook-pixel',
            ],
            'hosting': [
                r'aws',
                r'amazonaws',
                r'cloudfront',
                r'azure',
                r'netlify',
                r'vercel',
                r'heroku',
            ],
            'cms': [
                r'wordpress',
                r'wix',
                r'squarespace',
                r'drupal',
                r'joomla',
            ]
        }

        for category, patterns in tech_patterns.items():
            for pattern in patterns:
                if re.search(pattern, html_content, re.IGNORECASE):
                    technologies.add(category.replace('_', ' ').title())

        return list(technologies)

    def extract_pricing_info(self, html_content: str) -> List[Dict]:
        """Extract pricing information from HTML content."""
        pricing = []

        # Look for common pricing patterns
        price_patterns = [
            r'(\$\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:per\s+(month|year|user|seat))?',
            r'(?:starts\s+at|from)\s*(\$\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\$\d+(?:,\d{3})*(?:\.\d{2})?)\s+(?:monthly|annually|per\s+month|per\s+year)',
        ]

        for pattern in price_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    price, interval = match[0], match[1] if len(match) > 1 else 'monthly'
                else:
                    price, interval = match, 'monthly'

                try:
                    price_value = float(price.replace('$', '').replace(',', ''))
                    pricing.append({
                        'amount': price_value,
                        'interval': interval.lower() if interval else 'monthly',
                        'type': 'fixed'  # Could be 'tiered', 'usage_based', etc.
                    })
                except ValueError:
                    continue

        return pricing

    def analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis - returns score from -1 (negative) to 1 (positive)."""
        positive_words = [
            'excellent', 'great', 'amazing', 'outstanding', 'superior', 'innovative',
            'advanced', 'professional', 'reliable', 'trusted', 'secure', 'fast',
            'efficient', 'cutting-edge', 'premium', 'world-class', 'award-winning'
        ]

        negative_words = [
            'slow', 'buggy', 'outdated', 'inadequate', 'inferior', 'deficient',
            'problematic', 'unreliable', 'unstable', 'expensive', 'complicated',
            'frustrating', 'poor', 'terrible', 'awful', 'disappointing'
        ]

        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        total_meaningful = pos_count + neg_count
        if total_meaningful == 0:
            return 0.0

        sentiment = (pos_count - neg_count) / total_meaningful
        return max(-1.0, min(1.0, sentiment))

    def generate_swot_analysis(self, profile: CompetitorProfile) -> SWOTAnalysis:
        """Generate SWOT analysis for a competitor."""
        # This would typically use more sophisticated NLP in a real implementation
        strengths = profile.strengths or [
            f"Strong {profile.market_position.value.lower()} position",
            f"{profile.size.value} with resources for growth",
            "Innovative product portfolio"
        ]

        weaknesses = profile.weaknesses or [
            "Limited market presence in certain segments",
            "Higher pricing than competitors",
            "Smaller customer support team"
        ]

        opportunities = [
            f"Growth in {profile.market_position.value.lower()} segment",
            "Expansion to new geographic markets",
            "Partnership opportunities with complementary services"
        ]

        threats = [
            "Increasing competition from emerging players",
            "Potential economic downturn affecting spending",
            "Technology shifts in the industry"
        ]

        # Calculate confidence based on data completeness
        data_points = len(profile.products) + len(profile.social_metrics) + len(profile.recent_news)
        confidence_score = min(data_points / 10, 1.0)  # Normalize to 0-1

        return SWOTAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            confidence_score=confidence_score
        )

    def predict_next_moves(self, profile: CompetitorProfile) -> List[PredictiveInsight]:
        """Generate predictive insights about competitor behavior."""
        predictions = []

        # Predict based on growth rate
        if profile.growth_rate > 20:  # High growth
            predictions.append(PredictiveInsight(
                prediction="Likely to expand into new markets",
                probability=0.75,
                timeframe="short_term",
                supporting_evidence=["High growth rate indicates expansion plans", "Increased hiring activity"],
                confidence_score=0.8
            ))

        # Predict based on funding
        if profile.funding_history:
            latest_funding = max(profile.funding_history, key=lambda x: x.get('date', ''))
            if latest_funding.get('amount', 0) > 10000000:  # More than $10M
                predictions.append(PredictiveInsight(
                    prediction="Likely to invest heavily in R&D and marketing",
                    probability=0.85,
                    timeframe="medium_term",
                    supporting_evidence=[f"Recent ${latest_funding['amount']:,} funding round"],
                    confidence_score=0.9
                ))

        # Predict based on market position
        if profile.market_position == MarketPosition.CHALLENGER:
            predictions.append(PredictiveInsight(
                prediction="Likely to engage in aggressive pricing or feature competition",
                probability=0.7,
                timeframe="short_term",
                supporting_evidence=["Market challenger typically competes aggressively"],
                confidence_score=0.75
            ))

        # Default prediction
        predictions.append(PredictiveInsight(
            prediction="Likely to continue current growth trajectory",
            probability=0.6,
            timeframe="medium_term",
            supporting_evidence=["Consistent historical performance"],
            confidence_score=0.65
        ))

        return predictions

    async def create_competitor_profile(self, name: str, domain: str,
                                      size: CompetitorSize = CompetitorSize.SMB,
                                      market_position: MarketPosition = MarketPosition.EMERGING) -> CompetitorProfile:
        """Create a comprehensive competitor profile."""
        print(f"Creating profile for {name} ({domain})...")

        # Scrape website content
        website_url = f"https://{domain}" if not domain.startswith(('http://', 'https://')) else domain
        html_content = await self.scrape_website_content(website_url)

        products = []
        pricing_models = []
        technology_stack = []

        if html_content:
            # Extract information from content
            products = self.extract_products_from_content(html_content)
            pricing_models = self.extract_pricing_info(html_content)
            technology_stack = self.extract_technology_stack(html_content)

        # Create profile
        profile = CompetitorProfile(
            name=name,
            domain=domain,
            size=size,
            market_position=market_position,
            products=products,
            pricing_models=pricing_models,
            technology_stack=technology_stack,
            social_metrics=self.estimate_social_metrics(name),  # Placeholder
            funding_history=self.get_funding_data(name),       # Placeholder
            leadership_team=self.get_leadership_data(name),    # Placeholder
            recent_news=self.get_recent_news(name),            # Placeholder
        )

        # Calculate derived metrics
        profile.threat_level = self.calculate_threat_level(profile)
        profile.strengths = self.assess_strengths(profile)
        profile.weaknesses = self.assess_weaknesses(profile)

        # Store in memory
        self.competitors[name.lower()] = profile

        return profile

    def extract_products_from_content(self, html_content: str) -> List[str]:
        """Extract product names from HTML content."""
        products = set()

        # Look for common product-related sections
        product_sections = re.findall(r'(?:products?|services?|solutions?)[\s\S]*?(?:</div>|<h[1-6]|<ul|<table)', html_content, re.IGNORECASE)

        for section in product_sections:
            # Extract potential product names
            product_names = re.findall(r'>\s*([A-Z][A-Za-z0-9\s\-_]{3,30})\s*<(?:br|/h|/p|/li|/a)', section)
            products.update(product_names)

        # Also look for h2/h3 tags that might contain product names
        h_tags = re.findall(r'<h[23][^>]*>([^<]{5,50})</h[23]>', html_content)
        for tag in h_tags:
            if len(tag.strip()) > 5:  # Filter out very short texts
                products.add(tag.strip())

        return list(products)[:10]  # Limit to top 10

    def estimate_social_metrics(self, company_name: str) -> Dict[str, int]:
        """Estimate social media metrics (placeholder implementation)."""
        # In a real implementation, this would query social media APIs
        return {
            'twitter_followers': hash(company_name + "twitter") % 100000,
            'linkedin_followers': hash(company_name + "linkedin") % 150000,
            'facebook_likes': hash(company_name + "facebook") % 80000,
        }

    def get_funding_data(self, company_name: str) -> List[Dict]:
        """Get funding history (placeholder implementation)."""
        # In a real implementation, this would query funding databases
        if hash(company_name) % 3 == 0:
            return [{
                'round': 'Series A',
                'amount': 15000000,
                'date': '2023-05-15',
                'investors': ['Venture Capital Firm A', 'Angel Investor B']
            }]
        return []

    def get_leadership_data(self, company_name: str) -> List[Dict]:
        """Get leadership team information (placeholder implementation)."""
        # In a real implementation, this would scrape LinkedIn or company pages
        return [
            {'name': 'John Smith', 'title': 'CEO', 'linkedIn': 'john-smith'},
            {'name': 'Jane Doe', 'title': 'CTO', 'linkedIn': 'jane-doe'},
        ]

    def get_recent_news(self, company_name: str) -> List[Dict]:
        """Get recent news about the company (placeholder implementation)."""
        # In a real implementation, this would query news APIs
        return [
            {
                'title': f'{company_name} Announces New Partnership',
                'date': '2024-01-15',
                'source': 'TechCrunch',
                'summary': 'Brief summary of the news article...'
            },
            {
                'title': f'{company_name} Raises $15M in Series A Funding',
                'date': '2023-12-01',
                'source': 'VentureBeat',
                'summary': 'Brief summary of the funding announcement...'
            }
        ]

    def assess_strengths(self, profile: CompetitorProfile) -> List[str]:
        """Assess competitor strengths."""
        strengths = []

        if profile.market_position == MarketPosition.MARKET_LEADER:
            strengths.append("Market leadership position")

        if profile.size == CompetitorSize.FORTUNE_500:
            strengths.append("Large enterprise resources and stability")

        if profile.growth_rate > 25:
            strengths.append("High growth momentum")

        if len(profile.products) > 5:
            strengths.append("Diverse product portfolio")

        if profile.threat_level > 0.7:
            strengths.append("Significant market threat potential")

        # Default strengths
        if not strengths:
            strengths = [
                "Established market presence",
                "Proven business model",
                "Customer base retention"
            ]

        return strengths

    def assess_weaknesses(self, profile: CompetitorProfile) -> List[str]:
        """Assess competitor weaknesses."""
        weaknesses = []

        if profile.size == CompetitorSize.STARTUP:
            weaknesses.append("Limited resources compared to enterprise competitors")

        if profile.market_position == MarketPosition.EMERGING:
            weaknesses.append("Unproven market position")

        if profile.growth_rate < 5:
            weaknesses.append("Slow growth rate")

        if len(profile.products) < 3:
            weaknesses.append("Limited product diversification")

        # Default weaknesses
        if not weaknesses:
            weaknesses = [
                "Potential vulnerability to market changes",
                "Possible operational inefficiencies",
                "Risk of competitive pressure"
            ]

        return weaknesses

    def generate_alert_if_needed(self, old_profile: CompetitorProfile, new_profile: CompetitorProfile) -> Optional[IntelligenceAlert]:
        """Generate an alert if significant changes are detected."""
        changes = []

        # Check for significant changes
        if old_profile.threat_level != new_profile.threat_level:
            if abs(new_profile.threat_level - old_profile.threat_level) > 0.2:
                changes.append(f"Threat level changed from {old_profile.threat_level:.2f} to {new_profile.threat_level:.2f}")

        if old_profile.growth_rate != new_profile.growth_rate:
            if abs(new_profile.growth_rate - old_profile.growth_rate) > 10:
                changes.append(f"Growth rate changed significantly")

        if len(old_profile.products) != len(new_profile.products):
            if len(new_profile.products) > len(old_profile.products):
                changes.append(f"Added {len(new_profile.products) - len(old_profile.products)} new products")

        if changes:
            severity = "high" if any("threat" in change.lower() for change in changes) else "medium"
            alert_id = hashlib.md5(f"{new_profile.name}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]

            alert = IntelligenceAlert(
                id=alert_id,
                competitor_name=new_profile.name,
                alert_type="significant_change",
                severity=severity,
                message=f"Significant changes detected: {', '.join(changes)}",
                timestamp=datetime.now(),
                action_required=True
            )

            self.alerts.append(alert)
            return alert

        return None

    async def monitor_competitors(self, refresh_interval_hours: int = 24) -> None:
        """Continuously monitor competitors for changes."""
        print(f"Starting competitor monitoring (refresh every {refresh_interval_hours} hours)")

        while True:
            print(f"Refreshing competitor data at {datetime.now()}")

            # Refresh each competitor profile
            for name, profile in list(self.competitors.items()):  # Use list to avoid modification during iteration
                old_profile = profile

                # Recreate profile with fresh data
                new_profile = await self.create_competitor_profile(
                    name=profile.name,
                    domain=profile.domain,
                    size=profile.size,
                    market_position=profile.market_position
                )

                # Generate alert if significant changes detected
                alert = self.generate_alert_if_needed(old_profile, new_profile)
                if alert:
                    print(f"ALERT: {alert.message}")

            print(f"Sleeping for {refresh_interval_hours} hours...")
            await asyncio.sleep(refresh_interval_hours * 3600)  # Convert hours to seconds

    def generate_executive_dashboard(self) -> Dict:
        """Generate executive-level dashboard data."""
        dashboard = {
            'summary': {
                'total_competitors': len(self.competitors),
                'high_threat_competitors': len([c for c in self.competitors.values() if c.threat_level > 0.7]),
                'market_leaders': len([c for c in self.competitors.values() if c.market_position == MarketPosition.MARKET_LEADER]),
                'total_alerts': len(self.alerts),
                'recent_alerts': len([a for a in self.alerts if a.timestamp > datetime.now() - timedelta(days=7)])
            },
            'competitor_rankings': [],
            'market_overview': {},
            'predictions': [],
            'alerts': [a.__dict__ for a in self.alerts[-5:]]  # Last 5 alerts
        }

        # Rank competitors by threat level
        sorted_competitors = sorted(self.competitors.values(), key=lambda x: x.threat_level, reverse=True)
        for i, comp in enumerate(sorted_competitors, 1):
            dashboard['competitor_rankings'].append({
                'rank': i,
                'name': comp.name,
                'threat_level': comp.threat_level,
                'market_position': comp.market_position.value,
                'size': comp.size.value
            })

        # Generate market overview
        position_counts = defaultdict(int)
        size_counts = defaultdict(int)

        for comp in self.competitors.values():
            position_counts[comp.market_position.value] += 1
            size_counts[comp.size.value] += 1

        dashboard['market_overview']['positions'] = dict(position_counts)
        dashboard['market_overview']['sizes'] = dict(size_counts)

        # Add predictions for top competitors
        top_competitors = sorted_competitors[:3]
        for comp in top_competitors:
            predictions = self.predict_next_moves(comp)
            for pred in predictions[:2]:  # Take top 2 predictions per competitor
                dashboard['predictions'].append({
                    'competitor': comp.name,
                    'prediction': pred.prediction,
                    'probability': pred.probability
                })

        return dashboard

async def create_improved_competitive_analysis_skill():
    """Factory function to create the improved competitive analysis skill."""
    skill = ImprovedCompetitiveAnalysis()
    await skill.initialize_session()
    return skill

# Example usage
async def main():
    # Example usage
    analysis = await create_improved_competitive_analysis_skill()

    # Add some competitors
    await analysis.create_competitor_profile(
        name="Competitor One Inc",
        domain="competitor1.com",
        size=CompetitorSize.ENTERPRISE,
        market_position=MarketPosition.MARKET_LEADER
    )

    await analysis.create_competitor_profile(
        name="Rival Startup",
        domain="rivalstartup.io",
        size=CompetitorSize.STARTUP,
        market_position=MarketPosition.EMERGING
    )

    # Generate dashboard
    dashboard = analysis.generate_executive_dashboard()
    print("Executive Dashboard Summary:")
    print(f"Total Competitors: {dashboard['summary']['total_competitors']}")
    print(f"High Threat Competitors: {dashboard['summary']['high_threat_competitors']}")
    print(f"Recent Alerts: {dashboard['summary']['recent_alerts']}")

    print("\nTop Competitors by Threat Level:")
    for rank_info in dashboard['competitor_rankings'][:5]:
        print(f"{rank_info['rank']}. {rank_info['name']} - Threat: {rank_info['threat_level']:.2f}")

    await analysis.close_session()

if __name__ == "__main__":
    asyncio.run(main())
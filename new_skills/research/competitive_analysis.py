"""
Competitive Analysis Skill
Automatically gathers and analyzes competitor information from various online sources.
"""
import requests
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import time
from urllib.parse import urljoin, urlparse

@dataclass
class Competitor:
    name: str
    website: str
    products: List[str]
    pricing: Dict[str, float]
    social_media: Dict[str, str]
    strengths: List[str]
    weaknesses: List[str]
    market_position: str
    last_updated: datetime

@dataclass
class ProductComparison:
    feature: str
    your_company: str
    competitor: str
    advantage: str  # yours, theirs, equal

class CompetitiveAnalysis:
    """
    Skill to automatically gather and analyze competitor information.
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_website(self, url: str) -> str:
        """
        Scrape basic information from a website.
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return ""

    def extract_products_from_text(self, text: str) -> List[str]:
        """
        Extract product names from website text.
        """
        # Look for common product-related phrases
        product_patterns = [
            r'(?:our|their)\s+(?:products?|services?|offerings?)\s*(?:include|are)\s*:?\s*([^.]*?)(?:\.|and|\n|$)',
            r'(?:product|service)\s+([a-zA-Z\s]+?)(?:\s+is|\s+are|\s+includes)',
            r'([A-Z][a-zA-Z\s]+(?:[A-Z][a-z]*)+)\s+(?:platform|solution|software|tool)',
        ]

        products = set()
        for pattern in product_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                clean_match = re.sub(r'[,;&]', '', match).strip()
                if len(clean_match) > 3:  # Filter out very short matches
                    products.add(clean_match)

        return list(products)[:10]  # Limit to top 10

    def extract_pricing_info(self, text: str) -> Dict[str, float]:
        """
        Extract pricing information from website text.
        """
        pricing = {}

        # Look for pricing patterns
        price_patterns = [
            r'(\$\d+(?:,\d{3})*(?:\.\d{2})?)\s+(?:per\s+month|per\s+user|monthly)',
            r'(\$\d+(?:,\d{3})*(?:\.\d{2})?)\s+(?:for|per)\s+([a-zA-Z\s]+)',
            r'(?:starts\s+at|from)\s+(\$\d+(?:,\d{3})*(?:\.\d{2})?)',
        ]

        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    price_str, item = match[0], match[1]
                else:
                    price_str = match
                    item = "Standard Plan"

                try:
                    price = float(price_str.replace('$', '').replace(',', ''))
                    pricing[item.strip()] = price
                except ValueError:
                    continue

        return pricing

    def analyze_social_presence(self, company_name: str) -> Dict[str, str]:
        """
        Analyze social media presence for a company.
        """
        social_platforms = {
            'twitter': f'https://twitter.com/{company_name.replace(" ", "").lower()}',
            'linkedin': f'https://linkedin.com/company/{company_name.replace(" ", "").lower()}',
            'facebook': f'https://facebook.com/{company_name.replace(" ", "").lower()}',
            'instagram': f'https://instagram.com/{company_name.replace(" ", "").lower()}'
        }

        active_platforms = {}
        for platform, url in social_platforms.items():
            try:
                response = self.session.head(url, timeout=5)
                if response.status_code == 200:
                    active_platforms[platform] = url
            except:
                # Try alternative URL format
                alt_url = f'https://{platform}.com/{company_name.replace(" ", "").replace("&", "").lower()}'
                try:
                    response = self.session.head(alt_url, timeout=5)
                    if response.status_code == 200:
                        active_platforms[platform] = alt_url
                except:
                    continue

        return active_platforms

    def identify_strengths_weaknesses(self, website_text: str) -> tuple:
        """
        Identify potential strengths and weaknesses from website content.
        """
        strengths = []
        weaknesses = []

        strength_keywords = [
            'award', 'best', 'leading', 'innovative', 'trusted', 'secure', 'fast',
            'reliable', 'professional', 'expert', 'certified', 'premium', 'advanced'
        ]

        weakness_keywords = [
            'beta', 'new', 'coming soon', 'limited', 'basic', 'free trial',
            'discount', 'sale', 'promotion', 'temporary'
        ]

        text_lower = website_text.lower()

        # Identify strengths
        for keyword in strength_keywords:
            if keyword in text_lower:
                strengths.append(keyword.title())

        # Identify weaknesses
        for keyword in weakness_keywords:
            if keyword in text_lower:
                weaknesses.append(keyword.title())

        # Remove duplicates while preserving order
        strengths = list(dict.fromkeys(strengths))
        weaknesses = list(dict.fromkeys(weaknesses))

        return strengths[:5], weaknesses[:5]  # Limit to top 5

    def analyze_market_position(self, website_text: str) -> str:
        """
        Analyze market position based on website content.
        """
        market_indicators = {
            'market_leader': ['leader', 'top', 'number one', 'premier', 'industry standard'],
            'innovator': ['first', 'pioneer', 'revolutionary', 'cutting edge', 'disruptive'],
            'niche_player': ['specialized', 'focused', 'dedicated', 'specific', 'unique'],
            'value_player': ['affordable', 'cost-effective', 'cheap', 'budget', 'economic']
        }

        text_lower = website_text.lower()

        positions = []
        for position, indicators in market_indicators.items():
            count = sum(1 for indicator in indicators if indicator in text_lower)
            if count > 0:
                positions.append((position, count))

        if positions:
            # Return the position with highest count
            return max(positions, key=lambda x: x[1])[0].replace('_', ' ').title()
        else:
            return "Undefined"

    def create_competitor_profile(self, name: str, website: str) -> Competitor:
        """
        Create a comprehensive competitor profile.
        """
        print(f"Gathering information for {name}...")

        # Scrape website
        website_text = self.scrape_website(website)

        # Extract information
        products = self.extract_products_from_text(website_text)
        pricing = self.extract_pricing_info(website_text)
        social_media = self.analyze_social_presence(name)
        strengths, weaknesses = self.identify_strengths_weaknesses(website_text)
        market_position = self.analyze_market_position(website_text)

        return Competitor(
            name=name,
            website=website,
            products=products,
            pricing=pricing,
            social_media=social_media,
            strengths=strengths,
            weaknesses=weaknesses,
            market_position=market_position,
            last_updated=datetime.now()
        )

    def compare_products(self, your_products: List[str], competitor: Competitor) -> List[ProductComparison]:
        """
        Compare your products against a competitor's offerings.
        """
        comparisons = []

        # Simple comparison based on product names
        for your_product in your_products:
            matched = False
            for comp_product in competitor.products:
                if your_product.lower() in comp_product.lower() or comp_product.lower() in your_product.lower():
                    # Found a comparable product
                    comparisons.append(ProductComparison(
                        feature=f"{your_product} vs {comp_product}",
                        your_company="Available",
                        competitor="Available",
                        advantage="equal"
                    ))
                    matched = True
                    break

            if not matched:
                # Your product not offered by competitor
                comparisons.append(ProductComparison(
                    feature=your_product,
                    your_company="Available",
                    competitor="Not Available",
                    advantage="yours"
                ))

        # Check for competitor products not in your offering
        for comp_product in competitor.products:
            matched = False
            for your_product in your_products:
                if comp_product.lower() in your_product.lower() or your_product.lower() in comp_product.lower():
                    matched = True
                    break

            if not matched:
                # Competitor has product you don't offer
                comparisons.append(ProductComparison(
                    feature=comp_product,
                    your_company="Not Available",
                    competitor="Available",
                    advantage="theirs"
                ))

        return comparisons

    def generate_swot_analysis(self, competitor: Competitor) -> Dict[str, List[str]]:
        """
        Generate SWOT analysis for a competitor.
        """
        swot = {
            'Strengths': competitor.strengths,
            'Weaknesses': competitor.weaknesses,
            'Opportunities': [],  # Would require external market data
            'Threats': []  # Would require broader market analysis
        }

        # Add some generic opportunities/threats based on market position
        if 'Leader' in competitor.market_position:
            swot['Opportunities'].extend(['Market expansion', 'Premium positioning'])
            swot['Threats'].extend(['Regulatory scrutiny', 'Innovation lag'])
        elif 'Innovator' in competitor.market_position:
            swot['Opportunities'].extend(['First-mover advantage', 'Patent protection'])
            swot['Threats'].extend(['Copycats', 'Resource constraints'])

        return swot

    def generate_competitive_report(self, competitors: List[Competitor], your_company_info: Dict) -> str:
        """
        Generate a comprehensive competitive analysis report.
        """
        report = f"# Competitive Analysis Report\n\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        report += f"## Your Company: {your_company_info['name']}\n"
        report += f"- Products: {', '.join(your_company_info['products'])}\n"
        report += f"- Position: {your_company_info['position']}\n\n"

        for i, competitor in enumerate(competitors, 1):
            report += f"## Competitor {i}: {competitor.name}\n"
            report += f"- **Website**: {competitor.website}\n"
            report += f"- **Market Position**: {competitor.market_position}\n"

            if competitor.products:
                report += f"- **Products**: {', '.join(competitor.products[:5])}\n"  # Top 5
            else:
                report += f"- **Products**: Information not available\n"

            if competitor.pricing:
                report += f"- **Pricing**: {', '.join([f'{k}: ${v}' for k, v in list(competitor.pricing.items())[:3]])}\n"  # Top 3
            else:
                report += f"- **Pricing**: Information not available\n"

            if competitor.social_media:
                report += f"- **Social Presence**: {', '.join(competitor.social_media.keys())}\n"
            else:
                report += f"- **Social Presence**: Limited or unknown\n"

            report += f"\n### SWOT Analysis\n"
            swot = self.generate_swot_analysis(competitor)
            for category, items in swot.items():
                if items:
                    report += f"- **{category}**: {', '.join(items)}\n"
                else:
                    report += f"- **{category}**: No clear {category.lower()} identified\n"

            report += f"\n### Comparison with {your_company_info['name']}\n"
            comparisons = self.compare_products(your_company_info['products'], competitor)
            yours_ahead = sum(1 for c in comparisons if c.advantage == 'yours')
            theirs_ahead = sum(1 for c in comparisons if c.advantage == 'theirs')
            equal = sum(1 for c in comparisons if c.advantage == 'equal')

            report += f"- {your_company_info['name']} leads in {yours_ahead} areas\n"
            report += f"- {competitor.name} leads in {theirs_ahead} areas\n"
            report += f"- Equal in {equal} areas\n\n"

        report += f"## Strategic Recommendations\n"
        report += f"1. Focus on areas where {your_company_info['name']} has advantages\n"
        report += f"2. Monitor {', '.join([c.name for c in competitors[:2]])} closely\n"
        report += f"3. Consider {', '.join([c.market_position for c in competitors[:2]])} strategies\n\n"

        report += f"## Data Freshness\n"
        report += f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Note: Website content may change frequently\n"

        return report

def create_competitive_analysis_skill():
    """Factory function to create the competitive analysis skill."""
    return CompetitiveAnalysis()

# Example usage
if __name__ == "__main__":
    # Example usage
    analysis = create_competitive_analysis_skill()

    # Define your company info
    your_company = {
        'name': 'Your Company',
        'products': ['Product A', 'Product B', 'Product C'],
        'position': 'Innovation Leader'
    }

    # Define competitors to analyze
    competitors_data = [
        {'name': 'Competitor One', 'website': 'https://example.com'},
        {'name': 'Competitor Two', 'website': 'https://example2.com'}
    ]

    # Create competitor profiles
    competitors = []
    for comp_data in competitors_data:
        try:
            profile = analysis.create_competitor_profile(comp_data['name'], comp_data['website'])
            competitors.append(profile)
        except Exception as e:
            print(f"Could not analyze {comp_data['name']}: {str(e)}")

    if competitors:
        report = analysis.generate_competitive_report(competitors, your_company)
        print(report)
    else:
        print("No competitors could be analyzed.")
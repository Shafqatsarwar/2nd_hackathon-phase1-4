"""
Content Generator Skill
Automatically generates high-quality written content based on topic, style, and audience requirements.
"""
import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import re

@dataclass
class ContentRequirements:
    topic: str
    audience: str
    length: str  # short, medium, long
    format: str  # blog, article, social, email, etc.
    tone: str  # professional, casual, friendly, formal, etc.
    keywords: List[str]
    brand_voice: str

@dataclass
class GeneratedContent:
    title: str
    content: str
    seo_score: float
    readability_score: float
    estimated_reading_time: int
    suggestions: List[str]

class ContentGenerator:
    """
    Skill to automatically generate high-quality written content.
    """

    def __init__(self):
        # Brand voice templates
        self.brand_voices = {
            'professional': {
                'openings': [
                    'In today\'s rapidly evolving landscape,',
                    'Contemporary analysis indicates',
                    'Current industry trends suggest',
                    'Extensive research demonstrates',
                    'Our comprehensive evaluation reveals'
                ],
                'transitions': [
                    'Furthermore,',
                    'Additionally,',
                    'Moreover,',
                    'Consequently,',
                    'Subsequently,'
                ],
                'closings': [
                    'In conclusion,',
                    'To summarize,',
                    'Therefore,',
                    'Ultimately,',
                    'Accordingly,'
                ]
            },
            'casual': {
                'openings': [
                    'So here\'s the thing,',
                    'Let\'s talk about',
                    'You know what\'s interesting about',
                    'Ever wonder about',
                    'Here\'s something cool:'
                ],
                'transitions': [
                    'Anyway,',
                    'Oh, and',
                    'Also,',
                    'Plus,',
                    'On top of that,'
                ],
                'closings': [
                    'Anyways,',
                    'So there you have it,',
                    'Bottom line:',
                    'That\'s pretty much it.',
                    'And that\'s the gist.'
                ]
            },
            'friendly': {
                'openings': [
                    'Hey there! Want to learn about',
                    'Great news! We\'ve got something exciting about',
                    'We thought you\'d love to know about',
                    'Guess what? We\'re talking about',
                    'Ready for some fun facts about'
                ],
                'transitions': [
                    'But wait, there\'s more!',
                    'And here\'s the best part:',
                    'Speaking of which,',
                    'We\'re not done yet!',
                    'There\'s something else:'
                ],
                'closings': [
                    'Thanks for reading!',
                    'Hope you enjoyed this!',
                    'See you next time!',
                    'Stay tuned for more!',
                    'Keep learning!'
                ]
            }
        }

        # Content templates by format
        self.content_templates = {
            'blog': {
                'structure': [
                    'introduction',
                    'problem_statement',
                    'solution_overview',
                    'detailed_explanation',
                    'examples',
                    'conclusion'
                ]
            },
            'social': {
                'structure': [
                    'hook',
                    'main_point',
                    'call_to_action'
                ]
            },
            'article': {
                'structure': [
                    'headline',
                    'introduction',
                    'background',
                    'analysis',
                    'implications',
                    'conclusion'
                ]
            }
        }

        # Word count mapping
        self.length_mapping = {
            'short': 200,
            'medium': 500,
            'long': 1000
        }

    def generate_title(self, topic: str, format_type: str, tone: str) -> str:
        """
        Generate an engaging title based on topic and requirements.
        """
        title_templates = {
            'blog': [
                f"How to {topic.replace(' ', ' ')}: A Complete Guide",
                f"The Ultimate Guide to {topic}",
                f"{topic}: Everything You Need to Know",
                f"Why {topic} Matters in 2024",
                f"A Beginner's Guide to {topic}"
            ],
            'social': [
                f"{topic}: You Won't Believe What Happened Next",
                f"Quick Tips for Better {topic}",
                f"{topic} - Did You Know?",
                f"Why {topic} is Trending Right Now",
                f"5 Facts About {topic} That Will Surprise You"
            ],
            'article': [
                f"Understanding {topic}: Current Trends and Future Outlook",
                f"The Impact of {topic} on Modern Business",
                f"{topic}: A Comprehensive Analysis",
                f"Exploring the Nuances of {topic}",
                f"Breaking Down the Complexity of {topic}"
            ]
        }

        templates = title_templates.get(format_type, title_templates['blog'])
        return random.choice(templates)

    def generate_introduction(self, topic: str, tone: str, brand_voice: str) -> str:
        """
        Generate an introduction paragraph.
        """
        openings = self.brand_voices.get(brand_voice, self.brand_voices['professional'])['openings']
        opening = random.choice(openings)

        intro_templates = [
            f"{opening} {topic} has become increasingly important in today's world. With rapid advancements and changing dynamics, understanding the nuances of {topic} is crucial for success.",
            f"{opening} the subject of {topic} continues to evolve. As industries adapt and consumers become more discerning, staying informed about {topic} provides a competitive advantage.",
            f"{opening} {topic} represents a significant shift in how we approach problems. This fundamental change requires a fresh perspective and innovative thinking."
        ]

        return random.choice(intro_templates)

    def generate_body_section(self, topic: str, section_type: str, tone: str, brand_voice: str, keywords: List[str]) -> str:
        """
        Generate a body section based on type and requirements.
        """
        transitions = self.brand_voices.get(brand_voice, self.brand_voices['professional'])['transitions']
        transition = random.choice(transitions) if random.random() > 0.5 else ""

        # Add some keywords naturally
        keyword_phrase = ""
        if keywords and random.random() > 0.7:
            keyword = random.choice(keywords)
            keyword_phrase = f" including {keyword} and related concepts, "

        section_templates = {
            'problem_statement': [
                f"{transition} The primary challenge facing those dealing with {topic} is the lack of clear guidance and structured approaches. Without proper understanding, organizations often struggle to achieve optimal results.",
                f"{transition} Many individuals and businesses encounter difficulties when attempting to implement effective {topic} strategies. These challenges stem from misinformation and outdated methodologies.",
                f"{transition} The complexity of {topic} creates numerous obstacles for practitioners. Common issues include inadequate resources and insufficient expertise in the field."
            ],
            'solution_overview': [
                f"{transition} Effective {topic} requires a multifaceted approach that incorporates best practices and proven methodologies. The key is to develop a comprehensive strategy that addresses all relevant aspects.",
                f"{transition} Successful implementation of {topic} involves careful planning and attention to detail. Organizations must consider various factors and align their approach with specific objectives.",
                f"{transition} The solution to {topic} challenges lies in adopting systematic methods and leveraging appropriate tools. This ensures sustainable and measurable improvements."
            ],
            'detailed_explanation': [
                f"{transition} The detailed mechanics of {topic}{keyword_phrase}involve several interconnected components that work together harmoniously. Each element plays a crucial role in the overall effectiveness.",
                f"{transition} A deeper dive into {topic}{keyword_phrase}reveals the intricate relationships between various factors. Understanding these connections is essential for successful implementation.",
                f"{transition} The methodology behind {topic}{keyword_phrase}incorporates both theoretical foundations and practical applications. This combination ensures robust and reliable outcomes."
            ],
            'examples': [
                f"{transition} Real-world examples demonstrate the effectiveness of proper {topic} implementation. Companies like [Example Corp] have achieved remarkable results through strategic approaches.",
                f"{transition} Case studies reveal the transformative power of well-executed {topic} initiatives. Organizations that prioritize this area consistently outperform their competitors.",
                f"{transition} Practical applications of {topic} showcase its versatility and impact. From startups to enterprises, the benefits are universally recognized."
            ],
            'conclusion': [
                f"{transition} In conclusion, {topic} represents a critical area that demands attention and investment. Those who embrace effective strategies will undoubtedly reap significant rewards.",
                f"{transition} To summarize, the importance of {topic} cannot be overstated in today's environment. Success requires commitment, resources, and expert guidance.",
                f"{transition} Ultimately, mastering {topic} provides a distinct competitive advantage. Organizations that prioritize this area will thrive in the modern marketplace."
            ],
            'hook': [
                f"{topic}: This might surprise you, but the conventional wisdom is completely wrong.",
                f"Did you know that {topic} is responsible for 80% of breakthrough innovations?",
                f"Forget everything you thought you knew about {topic} - here's what experts don't want you to know."
            ],
            'main_point': [
                f"The truth about {topic} is far more complex than most realize. Recent studies show that traditional approaches are becoming obsolete.",
                f"Here's the deal: {topic} has fundamentally changed how businesses operate. Companies that adapt quickly gain significant advantages.",
                f"What if I told you that {topic} could increase your efficiency by 300%? The science behind it is fascinating."
            ],
            'call_to_action': [
                f"Ready to transform your approach to {topic}? Start implementing these strategies today!",
                f"Don't miss out on the {topic} revolution. Begin your journey now.",
                f"Want to learn more about {topic}? Subscribe for weekly insights!"
            ]
        }

        templates = section_templates.get(section_type, section_templates['detailed_explanation'])
        return random.choice(templates)

    def calculate_seo_score(self, content: str, keywords: List[str]) -> float:
        """
        Calculate a basic SEO score based on keyword density and content structure.
        """
        content_lower = content.lower()
        total_words = len(content.split())

        keyword_density = 0
        for keyword in keywords:
            keyword_count = content_lower.count(keyword.lower())
            if total_words > 0:
                density = (keyword_count / total_words) * 100
                # Optimal density is typically 1-3%
                if 1 <= density <= 3:
                    keyword_density += 1.0
                elif 0.5 <= density <= 5:
                    keyword_density += 0.7
                else:
                    keyword_density += 0.3

        # Normalize keyword density score
        keyword_score = keyword_density / max(len(keywords), 1) if keywords else 0.5

        # Check for headings and structure (simple heuristic)
        heading_score = 0.5
        if content.count('#') >= 2:
            heading_score = 0.8
        elif content.count('#') >= 1:
            heading_score = 0.6

        overall_score = (keyword_score * 0.7) + (heading_score * 0.3)
        return round(min(overall_score, 1.0), 2)

    def calculate_readability_score(self, content: str) -> float:
        """
        Calculate a basic readability score using simple heuristics.
        """
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())
        syllables = sum([len(re.findall(r'[aeiouAEIOU]+', word)) for word in content.split()])

        if sentences == 0 or words == 0:
            return 0.5

        avg_sentence_length = words / sentences
        avg_syllables_per_word = syllables / words if words > 0 else 1

        # Simplified Flesch Reading Ease adaptation
        # Score ranges from 0 (difficult) to 1 (easy)
        readability = 1 - ((avg_sentence_length / 20) + (avg_syllables_per_word * 10)) / 100
        readability = max(0, min(1, readability))

        return round(readability, 2)

    def estimate_reading_time(self, content: str) -> int:
        """
        Estimate reading time in minutes (based on 200 words per minute average).
        """
        words = len(content.split())
        minutes = max(1, round(words / 200))
        return minutes

    def generate_content(self, requirements: ContentRequirements) -> GeneratedContent:
        """
        Generate content based on the provided requirements.
        """
        # Determine target word count
        target_words = self.length_mapping.get(requirements.length, 500)

        # Generate title
        title = self.generate_title(requirements.topic, requirements.format, requirements.tone)

        # Build content
        content_parts = [f"# {title}\n"]

        # Add introduction
        intro = self.generate_introduction(requirements.topic, requirements.tone, requirements.brand_voice)
        content_parts.append(f"\n{intro}\n")

        # Add sections based on format
        structure = self.content_templates.get(requirements.format, self.content_templates['blog'])['structure']

        for section_type in structure[1:]:  # Skip introduction since we already added it
            section = self.generate_body_section(
                requirements.topic,
                section_type,
                requirements.tone,
                requirements.brand_voice,
                requirements.keywords
            )
            content_parts.append(f"{section}\n")

        full_content = " ".join(content_parts)

        # Truncate to approximately the target length
        words = full_content.split()
        if len(words) > target_words:
            words = words[:target_words]
            full_content = " ".join(words) + "..."

        # Calculate metrics
        seo_score = self.calculate_seo_score(full_content, requirements.keywords)
        readability_score = self.calculate_readability_score(full_content)
        reading_time = self.estimate_reading_time(full_content)

        # Generate suggestions
        suggestions = self.generate_suggestions(requirements, full_content)

        return GeneratedContent(
            title=title,
            content=full_content,
            seo_score=seo_score,
            readability_score=readability_score,
            estimated_reading_time=reading_time,
            suggestions=suggestions
        )

    def generate_suggestions(self, requirements: ContentRequirements, content: str) -> List[str]:
        """
        Generate improvement suggestions.
        """
        suggestions = []

        # SEO suggestions
        if requirements.keywords:
            keyword_usage = sum(content.lower().count(kw.lower()) for kw in requirements.keywords)
            if keyword_usage == 0:
                suggestions.append(f"Consider incorporating these keywords: {', '.join(requirements.keywords)}")
            elif keyword_usage < len(requirements.keywords):
                suggestions.append(f"Try to include all target keywords: {', '.join(requirements.keywords)}")

        # Length suggestion
        current_words = len(content.split())
        target = self.length_mapping.get(requirements.length, 500)
        if abs(current_words - target) > target * 0.3:  # 30% tolerance
            if current_words < target * 0.7:
                suggestions.append(f"Content is shorter than expected. Consider expanding to {target} words.")
            else:
                suggestions.append(f"Content is longer than expected. Consider focusing to approximately {target} words.")

        # Structure suggestions
        if requirements.format == 'blog' and content.count('#') < 2:
            suggestions.append("Consider adding subheadings to improve readability")

        # Default suggestion if none apply
        if not suggestions:
            suggestions.append("Content looks good! Consider fact-checking before publishing.")

        return suggestions[:3]  # Return top 3 suggestions

    def generate_multiple_variations(self, requirements: ContentRequirements, count: int = 3) -> List[GeneratedContent]:
        """
        Generate multiple content variations with different approaches.
        """
        variations = []
        for _ in range(count):
            variation = self.generate_content(requirements)
            variations.append(variation)
        return variations

def create_content_generator_skill():
    """Factory function to create the content generator skill."""
    return ContentGenerator()

# Example usage
if __name__ == "__main__":
    generator = create_content_generator_skill()

    requirements = ContentRequirements(
        topic="remote work productivity",
        audience="business professionals",
        length="medium",
        format="blog",
        tone="professional",
        keywords=["remote work", "productivity", "work from home", "efficiency"],
        brand_voice="professional"
    )

    content = generator.generate_content(requirements)

    print(f"Title: {content.title}")
    print(f"SEO Score: {content.seo_score}")
    print(f"Readability Score: {content.readability_score}")
    print(f"Estimated Reading Time: {content.estimated_reading_time} minutes")
    print(f"\nContent:\n{content.content}")
    print(f"\nSuggestions: {', '.join(content.suggestions)}")
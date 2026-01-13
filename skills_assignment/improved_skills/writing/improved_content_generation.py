"""
Improved Content Generation Skill
AI-powered content creation with advanced personalization, SEO optimization, and multi-channel distribution capabilities.
"""
import asyncio
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import re
from enum import Enum
import math
import statistics
from abc import ABC, abstractmethod

class ContentType(Enum):
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"
    EMAIL_CAMPAIGN = "email_campaign"
    VIDEO_SCRIPT = "video_script"
    LANDING_PAGE = "landing_page"
    PRODUCT_DESCRIPTION = "product_description"

class AudienceSegment(Enum):
    DEMOGRAPHIC = "demographic"
    BEHAVIORAL = "behavioral"
    PSYCHOGRAPHIC = "psychographic"
    GEOGRAPHIC = "geographic"

class ToneOfVoice(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    AUTHORITATIVE = "authoritative"
    CONVERSATIONAL = "conversational"
    INFORMATIVE = "informative"

@dataclass
class AudienceProfile:
    id: str
    name: str
    age_range: Tuple[int, int]
    interests: List[str]
    pain_points: List[str]
    preferred_channels: List[str]
    behavioral_traits: List[str]
    content_preferences: Dict[str, float]  # Preference scores for content types

@dataclass
class ContentRequirements:
    topic: str
    target_audience: AudienceProfile
    content_type: ContentType
    tone_of_voice: ToneOfVoice
    length_requirement: str  # short, medium, long, specific word count
    brand_voice_guidelines: Dict[str, str]
    keywords: List[str]
    distribution_channels: List[str]
    performance_goals: Dict[str, float]  # Engagement, conversion, etc.

@dataclass
class GeneratedContent:
    id: str
    title: str
    body: str
    meta_description: str
    seo_score: float
    readability_score: float
    estimated_performance: Dict[str, float]
    personalization_variants: List[Dict[str, str]]
    channel_optimized_versions: Dict[str, str]
    call_to_action: str
    created_at: datetime

@dataclass
class ContentPerformancePrediction:
    engagement_rate: float
    reach_potential: float
    conversion_probability: float
    share_likelihood: float
    confidence_score: float

class ContentOptimizer(ABC):
    """Abstract base class for content optimization strategies."""

    @abstractmethod
    def optimize(self, content: str, requirements: ContentRequirements) -> str:
        """Optimize content based on specific requirements."""
        pass

class SEOOptimizer(ContentOptimizer):
    """Optimizes content for search engines."""

    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }

    def optimize(self, content: str, requirements: ContentRequirements) -> str:
        """Optimize content for SEO."""
        # Calculate ideal keyword density
        keyword_density = self._calculate_keyword_density(content, requirements.keywords)

        # Add keywords where appropriate
        optimized_content = self._add_keywords(content, requirements.keywords, keyword_density)

        # Optimize for readability
        optimized_content = self._improve_readability(optimized_content)

        return optimized_content

    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate current keyword density."""
        word_count = len([word for word in content.lower().split() if word not in self.stop_words])
        density_map = {}

        for keyword in keywords:
            keyword_count = content.lower().count(keyword.lower())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            density_map[keyword] = density

        return density_map

    def _add_keywords(self, content: str, keywords: List[str], current_density: Dict[str, float]) -> str:
        """Add keywords to content if density is too low."""
        # Target density: 1-3% for primary keywords
        target_keywords = [kw for kw, density in current_density.items() if density < 1.0]

        if not target_keywords:
            return content

        # Add keywords naturally by replacing related terms
        for keyword in target_keywords[:2]:  # Limit to 2 keywords to avoid stuffing
            content = self._insert_keyword_naturally(content, keyword)

        return content

    def _insert_keyword_naturally(self, content: str, keyword: str) -> str:
        """Insert keyword in a natural way."""
        sentences = content.split('.')
        if sentences:
            # Insert keyword in a random sentence that makes sense
            insert_index = random.randint(0, len(sentences)-1)
            if len(sentences[insert_index].split()) > 5:  # Only insert in longer sentences
                words = sentences[insert_index].split()
                insert_pos = random.randint(2, len(words)-1)
                words.insert(insert_pos, keyword)
                sentences[insert_index] = ' '.join(words)

        return '.'.join(sentences)

    def _improve_readability(self, content: str) -> str:
        """Improve content readability."""
        # Break up long sentences
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z].)\.(?=\s+[A-Z])', content)
        improved_sentences = []

        for sentence in sentences:
            if len(sentence.split()) > 25:  # Too long
                # Split into two sentences at a logical break
                words = sentence.split()
                mid_point = len(words) // 2
                # Find a good breaking point
                break_point = mid_point
                for i in range(mid_point, len(words)):
                    if words[i] in ['and', 'but', 'or', 'so', 'because']:
                        break_point = i
                        break

                if break_point != mid_point:
                    improved_sentences.append(' '.join(words[:break_point]) + '.')
                    improved_sentences.append(' '.join(words[break_point:]) + '.')
                else:
                    improved_sentences.append(sentence)
            else:
                improved_sentences.append(sentence)

        return ' '.join(improved_sentences)

class PersonalizationEngine:
    """Handles content personalization for different audience segments."""

    def __init__(self):
        self.segment_strategies = {
            'millennial': ['casual_tone', 'emoji_usage', 'trending_topics'],
            'gen_x': ['balanced_tone', 'practical_focus', 'value_emphasis'],
            'boomer': ['formal_tone', 'trust_emphasis', 'traditional_values'],
            'b2b_decision_maker': ['data_driven', 'roi_focus', 'efficiency_emphasis'],
            'b2c_consumer': ['emotional_appeal', 'social_proof', 'urgency']
        }

    def generate_variants(self, base_content: str, audience_profile: AudienceProfile) -> List[Dict[str, str]]:
        """Generate personalized content variants."""
        variants = []

        # Create variant for each major segment trait
        for trait in audience_profile.behavioral_traits[:2]:  # Limit to 2 traits
            variant = self._apply_personalization(base_content, trait, audience_profile)
            variants.append({
                'segment_trait': trait,
                'content': variant,
                'appeal_type': self._determine_appeal_type(trait)
            })

        return variants

    def _apply_personalization(self, content: str, trait: str, profile: AudienceProfile) -> str:
        """Apply personalization based on audience trait."""
        # Modify tone based on age
        age_modifier = self._modify_by_age(content, profile.age_range)

        # Emphasize relevant interests
        interest_enhanced = self._enhance_with_interests(age_modifier, profile.interests)

        # Address specific pain points
        pain_point_addressed = self._address_pain_points(interest_enhanced, profile.pain_points)

        return pain_point_addressed

    def _modify_by_age(self, content: str, age_range: Tuple[int, int]) -> str:
        """Modify content based on age range."""
        if age_range[0] <= 25 <= age_range[1]:  # Millennials
            # Add more casual language and modern references
            content = re.sub(r'important', 'key', content, flags=re.IGNORECASE)
            content = re.sub(r'professional', 'awesome', content, flags=re.IGNORECASE)
        elif age_range[0] <= 45 <= age_range[1]:  # Gen X
            # Balance professionalism with accessibility
            pass
        elif age_range[0] <= 55 <= age_range[1]:  # Boomers
            # Use more formal language
            content = re.sub(r'cool', 'excellent', content, flags=re.IGNORECASE)

        return content

    def _enhance_with_interests(self, content: str, interests: List[str]) -> str:
        """Enhance content with audience interests."""
        for interest in interests[:3]:  # Use top 3 interests
            if random.random() > 0.7:  # 30% chance to incorporate each interest
                content += f" This is particularly relevant for those interested in {interest}."

        return content

    def _address_pain_points(self, content: str, pain_points: List[str]) -> str:
        """Address audience pain points."""
        for pain_point in pain_points[:2]:  # Address top 2 pain points
            content += f" Unlike other solutions that suffer from {pain_point}, our approach solves this issue effectively."

        return content

    def _determine_appeal_type(self, trait: str) -> str:
        """Determine the type of appeal for the variant."""
        if 'value' in trait.lower():
            return 'value_appeal'
        elif 'social' in trait.lower():
            return 'social_appeal'
        elif 'innovation' in trait.lower():
            return 'innovation_appeal'
        else:
            return 'general_appeal'

class ChannelFormatter:
    """Formats content for different distribution channels."""

    def __init__(self):
        self.channel_specs = {
            'twitter': {
                'max_length': 280,
                'style': 'concise',
                'hashtags': True,
                'mentions': True
            },
            'linkedin': {
                'max_length': 3000,
                'style': 'professional',
                'hashtags': True,
                'mentions': True
            },
            'facebook': {
                'max_length': 63206,
                'style': 'engaging',
                'hashtags': True,
                'mentions': True
            },
            'instagram': {
                'max_length': 2200,
                'style': 'visual',
                'hashtags': True,
                'mentions': True
            },
            'email': {
                'max_length': 10000,
                'style': 'personal',
                'hashtags': False,
                'mentions': False
            }
        }

    def format_for_channel(self, content: str, channel: str) -> str:
        """Format content for a specific channel."""
        if channel not in self.channel_specs:
            return content  # Return unchanged if channel not supported

        spec = self.channel_specs[channel]

        # Trim content if too long
        if len(content) > spec['max_length']:
            sentences = content.split('. ')
            trimmed_content = ""
            for sentence in sentences:
                if len(trimmed_content + sentence + ". ") <= spec['max_length'] - 50:  # Leave buffer
                    trimmed_content += sentence + ". "
                else:
                    break
            content = trimmed_content

        # Apply channel-specific formatting
        if spec['hashtags']:
            content += self._add_hashtags(content, channel)

        if spec['style'] == 'professional':
            content = self._apply_professional_tone(content)
        elif spec['style'] == 'concise':
            content = self._make_concise(content)
        elif spec['style'] == 'engaging':
            content = self._make_engaging(content)
        elif spec['style'] == 'visual':
            content = self._add_visual_cues(content)
        elif spec['style'] == 'personal':
            content = self._add_personal_touch(content)

        return content

    def _add_hashtags(self, content: str, channel: str) -> str:
        """Add relevant hashtags to content."""
        # Extract keywords from content
        words = re.findall(r'\b\w+\b', content.lower())
        content_words = [w for w in words if len(w) > 4 and w not in self._get_common_words()]

        # Add 2-5 hashtags
        hashtag_count = min(5, len(content_words))
        hashtags = ['#' + w for w in content_words[:hashtag_count]]

        return content + " " + " ".join(hashtags)

    def _get_common_words(self) -> set:
        """Return common English words to exclude from hashtags."""
        return {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy',
            'did', 'she', 'use', 'way', 'will', 'with', 'year', 'have', 'from',
            'they', 'this', 'that', 'what', 'when', 'went', 'were', 'which', 'time'
        }

    def _apply_professional_tone(self, content: str) -> str:
        """Apply professional tone adjustments."""
        # Replace casual terms with professional equivalents
        content = re.sub(r'cool', 'excellent', content, flags=re.IGNORECASE)
        content = re.sub(r'awesome', 'outstanding', content, flags=re.IGNORECASE)
        content = re.sub(r'guys', 'team', content, flags=re.IGNORECASE)
        return content

    def _make_concise(self, content: str) -> str:
        """Make content more concise."""
        # Remove redundant phrases
        content = re.sub(r'in order to', 'to', content, flags=re.IGNORECASE)
        content = re.sub(r'due to the fact that', 'because', content, flags=re.IGNORECASE)
        content = re.sub(r'it is important to note that', '', content, flags=re.IGNORECASE)
        return content.strip()

    def _make_engaging(self, content: str) -> str:
        """Make content more engaging."""
        # Add questions and calls to action
        if random.random() > 0.5:
            content += " What are your thoughts on this? Share your experience!"
        return content

    def _add_visual_cues(self, content: str) -> str:
        """Add visual-friendly elements."""
        # Add emojis and visual breaks
        content = content.replace('.', '. 📌', 2)  # Add pin emoji to first two periods
        return content

    def _add_personal_touch(self, content: str) -> str:
        """Add personal touch for email."""
        content = "Hi there!\n\n" + content
        content += "\n\nBest regards,\nYour Content Team"
        return content

class ContentPerformancePredictor:
    """Predicts how content will perform."""

    def __init__(self):
        self.engagement_factors = {
            'length_optimization': 0.2,
            'keyword_relevance': 0.25,
            'emotional_appeal': 0.2,
            'timeliness': 0.15,
            'visual_elements': 0.1,
            'social_proof': 0.1
        }

    def predict_performance(self, content: str, requirements: ContentRequirements) -> ContentPerformancePrediction:
        """Predict content performance."""
        engagement_rate = self._calculate_engagement_rate(content, requirements)
        reach_potential = self._calculate_reach_potential(content, requirements)
        conversion_probability = self._calculate_conversion_probability(content, requirements)
        share_likelihood = self._calculate_share_likelihood(content, requirements)

        # Overall confidence based on content quality metrics
        confidence_score = min(
            (engagement_rate + reach_potential + conversion_probability + share_likelihood) / 4,
            1.0
        )

        return ContentPerformancePrediction(
            engagement_rate=engagement_rate,
            reach_potential=reach_potential,
            conversion_probability=conversion_probability,
            share_likelihood=share_likelihood,
            confidence_score=confidence_score
        )

    def _calculate_engagement_rate(self, content: str, requirements: ContentRequirements) -> float:
        """Calculate predicted engagement rate."""
        base_rate = 0.02  # 2% baseline

        # Factor in content type
        type_multiplier = {
            ContentType.BLOG_POST: 1.0,
            ContentType.SOCIAL_MEDIA: 1.5,
            ContentType.EMAIL_CAMPAIGN: 0.8,
            ContentType.VIDEO_SCRIPT: 2.0,
            ContentType.LANDING_PAGE: 1.2,
            ContentType.PRODUCT_DESCRIPTION: 0.9
        }.get(requirements.content_type, 1.0)

        # Factor in audience targeting
        targeting_score = len(requirements.target_audience.behavioral_traits) / 10  # Max 1.0 for 10+ traits

        # Factor in content optimization
        keyword_density = len([kw for kw in requirements.keywords if kw.lower() in content.lower()]) / max(len(requirements.keywords), 1)
        optimization_score = min(keyword_density * 2, 1.0)  # Up to 2x for perfect keyword density

        final_rate = base_rate * type_multiplier * (1 + targeting_score) * (1 + optimization_score)
        return min(final_rate, 0.20)  # Cap at 20%

    def _calculate_reach_potential(self, content: str, requirements: ContentRequirements) -> float:
        """Calculate reach potential."""
        # Start with audience size
        base_reach = len(requirements.target_audience.preferred_channels) * 0.1  # 10% per channel

        # Factor in content appeal
        interest_alignment = min(len([i for i in requirements.target_audience.interests if i.lower() in content.lower()]) / 5, 1.0)

        # Factor in shareability
        question_count = content.lower().count('?')
        exclamation_count = content.lower().count('!')
        shareability_score = min((question_count + exclamation_count) / 3, 0.5)

        return min(base_reach + interest_alignment + shareability_score, 1.0)

    def _calculate_conversion_probability(self, content: str, requirements: ContentRequirements) -> float:
        """Calculate conversion probability."""
        # Base conversion rate varies by content type
        base_rate = {
            ContentType.LANDING_PAGE: 0.05,
            ContentType.EMAIL_CAMPAIGN: 0.02,
            ContentType.BLOG_POST: 0.01,
            ContentType.SOCIAL_MEDIA: 0.005,
            ContentType.VIDEO_SCRIPT: 0.03,
            ContentType.PRODUCT_DESCRIPTION: 0.04
        }.get(requirements.content_type, 0.01)

        # Factor in pain point addressing
        pain_point_hits = sum(1 for pp in requirements.target_audience.pain_points if pp.lower() in content.lower())
        pain_factor = min(pain_point_hits * 0.1, 0.3)

        # Factor in call-to-action strength
        cta_phrases = ['buy now', 'sign up', 'learn more', 'get started', 'download', 'register']
        cta_strength = sum(1 for cta in cta_phrases if cta in content.lower()) * 0.05

        return min(base_rate + pain_factor + cta_strength, 0.30)  # Cap at 30%

    def _calculate_share_likelihood(self, content: str, requirements: ContentRequirements) -> float:
        """Calculate likelihood of sharing."""
        # Emotional triggers
        emotional_words = ['amazing', 'incredible', 'shocking', 'unbelievable', 'wow', 'fantastic', 'extraordinary']
        emotion_score = sum(1 for word in emotional_words if word in content.lower()) * 0.1

        # Question and curiosity
        question_score = min(content.lower().count('?') * 0.15, 0.3)

        # Social proof elements
        proof_indicators = ['study shows', 'research indicates', 'according to', 'experts say', 'survey found']
        proof_score = sum(1 for indicator in proof_indicators if indicator in content.lower()) * 0.1

        return min(emotion_score + question_score + proof_score, 1.0)

class ImprovedContentGeneration:
    """
    AI-powered content creation with advanced personalization and optimization.
    """

    def __init__(self):
        self.seo_optimizer = SEOOptimizer()
        self.personalization_engine = PersonalizationEngine()
        self.channel_formatter = ChannelFormatter()
        self.performance_predictor = ContentPerformancePredictor()
        self.content_history = []  # Store generated content for learning

    def generate_content(self, requirements: ContentRequirements) -> GeneratedContent:
        """Generate optimized content based on requirements."""
        # Generate base content
        base_content = self._generate_base_content(requirements)

        # Optimize for SEO
        seo_optimized = self.seo_optimizer.optimize(base_content, requirements)

        # Generate personalization variants
        variants = self.personalization_engine.generate_variants(seo_optimized, requirements.target_audience)

        # Format for different channels
        channel_versions = {}
        for channel in requirements.distribution_channels:
            channel_versions[channel] = self.channel_formatter.format_for_channel(seo_optimized, channel)

        # Predict performance
        performance_prediction = self.performance_predictor.predict_performance(seo_optimized, requirements)

        # Generate call-to-action
        cta = self._generate_cta(requirements)

        # Create content ID
        content_id = f"content_{len(self.content_history) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Calculate metrics
        seo_score = self._calculate_seo_score(seo_optimized, requirements.keywords)
        readability_score = self._calculate_readability_score(seo_optimized)

        # Create meta description
        meta_desc = self._generate_meta_description(seo_optimized)

        generated_content = GeneratedContent(
            id=content_id,
            title=self._generate_title(requirements.topic, requirements.tone_of_voice),
            body=seo_optimized,
            meta_description=meta_desc,
            seo_score=seo_score,
            readability_score=readability_score,
            estimated_performance={
                'engagement_rate': performance_prediction.engagement_rate,
                'reach_potential': performance_prediction.reach_potential,
                'conversion_probability': performance_prediction.conversion_probability,
                'share_likelihood': performance_prediction.share_likelihood,
                'confidence_score': performance_prediction.confidence_score
            },
            personalization_variants=variants,
            channel_optimized_versions=channel_versions,
            call_to_action=cta,
            created_at=datetime.now()
        )

        # Store in history
        self.content_history.append(generated_content)

        return generated_content

    def _generate_base_content(self, requirements: ContentRequirements) -> str:
        """Generate base content based on requirements."""
        # Select template based on content type
        template = self._select_template(requirements.content_type, requirements.tone_of_voice)

        # Fill template with dynamic content
        content = template.format(
            topic=requirements.topic,
            audience_name=requirements.target_audience.name,
            keywords=', '.join(requirements.keywords[:3]),  # Use first 3 keywords
            interests=' and '.join(requirements.target_audience.interests[:2]),
            pain_points=' and '.join(requirements.target_audience.pain_points[:2])
        )

        # Enhance with additional details
        content = self._enhance_content(content, requirements)

        return content

    def _select_template(self, content_type: ContentType, tone: ToneOfVoice) -> str:
        """Select appropriate template for content type and tone."""
        templates = {
            ContentType.BLOG_POST: {
                ToneOfVoice.PROFESSIONAL: "In today's competitive landscape, {topic} has emerged as a critical factor for success. For {audience_name} professionals, understanding the nuances of {topic} is essential. This comprehensive guide explores the key aspects of {topic}, highlighting how {keywords} contribute to effective implementation. We'll examine the relationship between {interests} and {topic}, addressing common {pain_points} that organizations face. By the end of this article, readers will have a clear understanding of best practices for {topic}.",
                ToneOfVoice.CASUAL: "So you want to know about {topic}? Well, you've come to the right place! {audience_name} folks are always looking for ways to improve their game, and {topic} is definitely worth exploring. In this post, we'll dive into {keywords} and see how they relate to {interests}. We'll also tackle those pesky {pain_points} that seem to pop up. Stick around, and you'll walk away knowing more about {topic} than when you started!",
                ToneOfVoice.FRIENDLY: "Hey there, {audience_name}! Ready to learn about {topic}? It's actually super interesting, especially when you consider how {keywords} play a role. If you're into {interests} (and who isn't?), then {topic} is right up your alley. Of course, we can't ignore the typical {pain_points} that come with this territory. Don't worry though - by the end of this, you'll be a {topic} pro!"
            },
            ContentType.SOCIAL_MEDIA: {
                ToneOfVoice.PROFESSIONAL: "Exciting developments in {topic} are reshaping how {audience_name} approach their work. Key considerations include {keywords}, {interests}, and addressing {pain_points}. #ProfessionalDevelopment #IndustryInsights",
                ToneOfVoice.CONVERSATIONAL: "Just had to share - {topic} is getting really interesting lately! {audience_name} folks should definitely pay attention to {keywords} and how they connect to {interests}. Anyone else dealing with {pain_points}? #Topic #Insights",
                ToneOfVoice.INFORMATIVE: "Did you know? {topic} impacts {audience_name} in significant ways. Important elements include {keywords}, with strong connections to {interests}. Addressing {pain_points} remains crucial for success. Learn more! #Info #Education"
            },
            ContentType.EMAIL_CAMPAIGN: {
                ToneOfVoice.PROFESSIONAL: "Dear Valued Customer,\n\nWe're excited to share insights about {topic} that directly impact {audience_name}. Our research shows that {keywords} significantly influence outcomes related to {interests}. We understand that {pain_points} can be challenging, which is why we've developed solutions that address these specific concerns.\n\nBest regards,\nThe Team",
                ToneOfVoice.FRIENDLY: "Hi {audience_name}!\n\nThought you'd love to hear about {topic} - it's been a hot topic lately! We've been exploring how {keywords} connect with {interests}, and we think you'll find our findings about {pain_points} super helpful.\n\nTalk soon!\nYour Friends",
            }
        }

        # Get template for this type and tone, with fallback
        type_templates = templates.get(content_type, templates[ContentType.BLOG_POST])
        template = type_templates.get(tone, type_templates[ToneOfVoice.PROFESSIONAL])

        return template

    def _enhance_content(self, content: str, requirements: ContentRequirements) -> str:
        """Enhance content with additional relevant information."""
        enhancements = [
            f"It's worth noting that {random.choice(requirements.target_audience.interests)} enthusiasts often find {requirements.topic} particularly relevant.",
            f"Recent studies indicate that {requirements.topic} can significantly impact how {requirements.target_audience.name} address {random.choice(requirements.target_audience.pain_points)}.",
            f"When implementing {requirements.topic}, organizations typically focus on {random.choice(requirements.keywords)} as a foundational element."
        ]

        # Add 1-2 enhancements randomly
        for _ in range(random.randint(1, 2)):
            if enhancements:
                enhancement = enhancements.pop(random.randint(0, len(enhancements)-1))
                content += " " + enhancement

        return content

    def _generate_title(self, topic: str, tone: ToneOfVoice) -> str:
        """Generate an engaging title."""
        title_templates = {
            ToneOfVoice.PROFESSIONAL: [
                f"The Comprehensive Guide to {topic}",
                f"{topic}: A Strategic Approach",
                f"Understanding {topic}: Best Practices for Professionals",
                f"{topic} Explained: What Every Professional Needs to Know"
            ],
            ToneOfVoice.CASUAL: [
                f"All About {topic}: The Fun Way",
                f"Everything You Wanted to Know About {topic}",
                f"{topic} Made Simple",
                f"So You Want to Learn About {topic}?"
            ],
            ToneOfVoice.FRIENDLY: [
                f"Your Friendly Guide to {topic}",
                f"Getting Started with {topic}",
                f"{topic}: No Fluff, Just Good Stuff",
                f"Discovering {topic} Together"
            ]
        }

        templates = title_templates.get(tone, title_templates[ToneOfVoice.PROFESSIONAL])
        return random.choice(templates)

    def _generate_cta(self, requirements: ContentRequirements) -> str:
        """Generate appropriate call-to-action."""
        cta_templates = {
            ContentType.BLOG_POST: [
                "Download our comprehensive guide to learn more.",
                "Subscribe to our newsletter for weekly insights.",
                "Contact us to discuss how this applies to your situation."
            ],
            ContentType.SOCIAL_MEDIA: [
                "Share your thoughts in the comments below!",
                "Follow us for more industry insights.",
                "Tag someone who would find this useful!"
            ],
            ContentType.EMAIL_CAMPAIGN: [
                "Reply to this email to learn more about our services.",
                "Click here to schedule a consultation.",
                "Visit our website to explore related resources."
            ]
        }

        templates = cta_templates.get(requirements.content_type, cta_templates[ContentType.BLOG_POST])
        return random.choice(templates)

    def _calculate_seo_score(self, content: str, keywords: List[str]) -> float:
        """Calculate SEO optimization score."""
        content_lower = content.lower()
        total_words = len(content.split())

        keyword_score = 0
        for keyword in keywords:
            keyword_count = content_lower.count(keyword.lower())
            if total_words > 0:
                density = (keyword_count / total_words) * 100
                # Optimal density is 1-3%
                if 1 <= density <= 3:
                    keyword_score += 1.0
                elif 0.5 <= density <= 5:
                    keyword_score += 0.7
                else:
                    keyword_score += 0.3

        keyword_score = keyword_score / max(len(keywords), 1) if keywords else 0.5

        # Check for headings (simple heuristic)
        heading_score = 0.5
        if content.count('#') >= 2:
            heading_score = 0.9
        elif content.count('#') >= 1:
            heading_score = 0.7

        overall_score = (keyword_score * 0.6) + (heading_score * 0.4)
        return round(min(overall_score, 1.0), 2)

    def _calculate_readability_score(self, content: str) -> float:
        """Calculate readability score."""
        sentences = len([s for s in re.split(r'[.!?]+', content) if s.strip()]) or 1
        words = len(content.split()) or 1
        syllables = sum([len(re.findall(r'[aeiouAEIOU]+', word)) for word in content.split()]) or 1

        avg_sentence_length = words / sentences
        avg_syllables_per_word = syllables / words

        # Simplified Flesch Reading Ease adaptation (0-1 scale)
        readability = 1 - ((avg_sentence_length / 15) + (avg_syllables_per_word * 3)) / 50
        readability = max(0, min(1, readability))

        return round(readability, 2)

    def _generate_meta_description(self, content: str) -> str:
        """Generate meta description for SEO."""
        # Take first 130-150 characters, ending at sentence boundary
        sentences = re.split(r'[.!?]+', content)
        desc = ""

        for sentence in sentences:
            candidate = desc + sentence.strip() + ". "
            if len(candidate) > 150:
                break
            desc = candidate

        return desc.strip()[:155] + "..." if len(desc.strip()) > 155 else desc.strip()

    def generate_batch_content(self, requirements_list: List[ContentRequirements]) -> List[GeneratedContent]:
        """Generate multiple content pieces efficiently."""
        results = []
        for req in requirements_list:
            content = self.generate_content(req)
            results.append(content)
        return results

    def analyze_content_performance(self) -> Dict[str, Any]:
        """Analyze historical content performance."""
        if not self.content_history:
            return {"message": "No content generated yet"}

        # Calculate averages
        avg_seo_score = statistics.mean([c.seo_score for c in self.content_history])
        avg_readability = statistics.mean([c.readability_score for c in self.content_history])
        avg_engagement = statistics.mean([
            c.estimated_performance.get('engagement_rate', 0) for c in self.content_history
        ])

        # Content type distribution
        type_counts = {}
        for c in self.content_history:
            type_name = c.estimated_performance.get('content_type', 'unknown')
            type_counts[type_name] = type_counts.get(type_name, 0) + 1

        return {
            "total_generated": len(self.content_history),
            "average_seo_score": round(avg_seo_score, 2),
            "average_readability": round(avg_readability, 2),
            "average_predicted_engagement": round(avg_engagement, 3),
            "content_type_distribution": type_counts,
            "time_period": {
                "first_content": min(c.created_at for c in self.content_history).isoformat(),
                "last_content": max(c.created_at for c in self.content_history).isoformat()
            }
        }

def create_improved_content_generation_skill():
    """Factory function to create the improved content generation skill."""
    return ImprovedContentGeneration()

# Example usage
if __name__ == "__main__":
    # Create skill instance
    content_gen = create_improved_content_generation_skill()

    # Define audience profile
    audience = AudienceProfile(
        id="aud_001",
        name="Marketing Professionals",
        age_range=(25, 45),
        interests=["digital marketing", "content strategy", "social media"],
        pain_points=["low engagement", "content fatigue", "measuring ROI"],
        preferred_channels=["linkedin", "email", "blog"],
        behavioral_traits=["early_adopter", "data_driven", "network_oriented"],
        content_preferences={ContentType.BLOG_POST: 0.8, ContentType.EMAIL_CAMPAIGN: 0.6}
    )

    # Define content requirements
    requirements = ContentRequirements(
        topic="content personalization",
        target_audience=audience,
        content_type=ContentType.BLOG_POST,
        tone_of_voice=ToneOfVoice.PROFESSIONAL,
        length_requirement="medium",
        brand_voice_guidelines={"adjectives": ["innovative", "effective", "strategic"]},
        keywords=["personalization", "marketing", "customer experience", "AI"],
        distribution_channels=["blog", "linkedin", "email"],
        performance_goals={"engagement": 0.05, "conversion": 0.02}
    )

    # Generate content
    generated = content_gen.generate_content(requirements)

    print(f"Title: {generated.title}")
    print(f"SEO Score: {generated.seo_score}")
    print(f"Readability Score: {generated.readability_score}")
    print(f"Predicted Engagement Rate: {generated.estimated_performance['engagement_rate']:.3f}")
    print(f"Personalization Variants: {len(generated.personalization_variants)}")
    print(f"Channel Versions: {list(generated.channel_optimized_versions.keys())}")
    print(f"Call to Action: {generated.call_to_action}")

    print("\nGenerated Content:")
    print(generated.body)

    # Analyze performance
    performance = content_gen.analyze_content_performance()
    print(f"\nPerformance Analysis: {performance}")
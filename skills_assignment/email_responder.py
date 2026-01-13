"""
Email Responder Skill
Automatically generates appropriate responses to common types of emails based on content analysis.
"""
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import json
from datetime import datetime

class EmailType(Enum):
    MEETING_REQUEST = "meeting_request"
    INFORMATION_REQUEST = "information_request"
    FOLLOW_UP = "follow_up"
    ACKNOWLEDGMENT = "acknowledgment"
    APPOINTMENT = "appointment"
    GENERAL_INQUIRY = "general_inquiry"

@dataclass
class Email:
    sender: str
    subject: str
    body: str
    timestamp: datetime
    cc: List[str] = None
    bcc: List[str] = None

@dataclass
class EmailResponse:
    subject: str
    body: str
    confidence: float  # 0-1 scale
    suggested_tone: str

class EmailResponder:
    """
    Skill to automatically generate appropriate email responses based on content analysis.
    """

    def __init__(self):
        self.email_patterns = {
            EmailType.MEETING_REQUEST: [
                r"(?:meeting|appointment|schedule|calendar|call).*?(?:request|needed|please|would like)",
                r"(?:when|time|date).*?(?:work for you|suitable|available)",
                r"(?:availability|free|open).*?(?:time|slot|calendar)"
            ],
            EmailType.INFORMATION_REQUEST: [
                r"(?:could you|can you|please).*?(?:send|provide|share).*?(?:information|details|document)",
                r"(?:where|what|how).*?(?:find|obtain|get).*?(?:information|details)",
                r"(?:requesting|need).*?(?:information|details|more info)"
            ],
            EmailType.FOLLOW_UP: [
                r"(?:following up|following on|checking in).*?(?:previous|earlier|last)",
                r"(?:any update|status update|progress update)",
                r"(?:circle back|get back to me|hear from you)"
            ],
            EmailType.ACKNOWLEDGMENT: [
                r"(?:thank you|thanks|appreciate).*?(?:your|the|this).*?(?:email|message|information)",
                r"(?:received|got).*?(?:your|the).*?(?:email|message|information)",
                r"(?:confirm|acknowledge|noted).*?(?:received|understand)"
            ],
            EmailType.APPOINTMENT: [
                r"(?:appointment|booking|reservation|schedule).*?(?:confirmed|scheduled|set)",
                r"(?:confirming|confirmation|confirmed).*?(?:appointment|meeting|booking)"
            ]
        }

        self.response_templates = {
            EmailType.MEETING_REQUEST: {
                "subject": "Re: {original_subject}",
                "body": """Hi {sender_name},

Thank you for reaching out regarding a meeting. I'd be happy to discuss this further.

{availability_options}

Please let me know what works best for you, and I'll send over a calendar invite.

Best regards,
[Your Name]"""
            },
            EmailType.INFORMATION_REQUEST: {
                "subject": "Re: {original_subject}",
                "body": """Hi {sender_name},

Thanks for your inquiry. I'm happy to provide the information you're looking for.

{information_provided}

If you need any additional details, please don't hesitate to ask.

Best regards,
[Your Name]"""
            },
            EmailType.FOLLOW_UP: {
                "subject": "Re: {original_subject}",
                "body": """Hi {sender_name},

Thank you for following up. I wanted to provide you with an update on this matter.

{update_details}

I'll continue to monitor the situation and will reach out if there are any significant developments.

Best regards,
[Your Name]"""
            },
            EmailType.GENERAL_INQUIRY: {
                "subject": "Re: {original_subject}",
                "body": """Hi {sender_name},

Thank you for your email. I appreciate you reaching out.

{response_content}

I hope this addresses your inquiry. Please let me know if you have any other questions.

Best regards,
[Your Name]"""
            }
        }

        self.tone_styles = {
            "professional": {
                "greetings": ["Dear", "Hello", "Good morning/afternoon"],
                "closings": ["Best regards,", "Sincerely,", "Thank you,"],
                "formalities": ["I would be delighted", "It would be my pleasure"]
            },
            "friendly_professional": {
                "greetings": ["Hi", "Hello", "Hey"],
                "closings": ["Best,", "Thanks,", "Have a great day,"],
                "formalities": ["Happy to help", "Glad to assist"]
            },
            "casual": {
                "greetings": ["Hi", "Hey", "Hello"],
                "closings": ["Thanks!", "Cheers,", "Talk soon,"],
                "formalities": ["Sure thing", "No problem"]
            }
        }

    def identify_email_type(self, email: Email) -> tuple:
        """
        Identify the type of email and return confidence score.
        """
        highest_match_count = 0
        best_match_type = EmailType.GENERAL_INQUIRY
        total_matches = 0

        for email_type, patterns in self.email_patterns.items():
            match_count = 0
            combined_text = f"{email.subject} {email.body}".lower()

            for pattern in patterns:
                matches = re.findall(pattern, combined_text)
                match_count += len(matches)
                total_matches += len(matches)

            if match_count > highest_match_count:
                highest_match_count = match_count
                best_match_type = email_type

        # Calculate confidence based on matches
        confidence = min(highest_match_count / max(total_matches, 1), 1.0) if total_matches > 0 else 0.1

        return best_match_type, confidence

    def extract_sender_name(self, sender: str) -> str:
        """
        Extract the name from the sender's email address or full name.
        """
        # Try to extract name from "Name <email@domain.com>" format
        match = re.match(r'^([^<]+)', sender)
        if match:
            name = match.group(1).strip()
            # Remove quotes if present
            name = name.strip('"\'')
            return name.split()[0]  # Return first name

        # If no name format, try to extract from email address
        if '@' in sender:
            username = sender.split('@')[0]
            return username.split('.')[0].capitalize()

        return sender

    def personalize_response(self, template: dict, email: Email, email_type: EmailType) -> str:
        """
        Personalize the response template based on the email content.
        """
        sender_name = self.extract_sender_name(email.sender)

        # Customize based on email type
        if email_type == EmailType.MEETING_REQUEST:
            availability_options = "I'm available Monday through Friday, 9 AM to 5 PM. My calendar shows the following openings this week:\n\n- Tuesday at 2 PM\n- Wednesday at 10 AM\n- Thursday at 3 PM"
            response_body = template["body"].format(
                sender_name=sender_name,
                availability_options=availability_options
            )
        elif email_type == EmailType.INFORMATION_REQUEST:
            information_provided = "I've attached the requested information. Please find the details below:\n\n[Specific information would go here based on the request]"
            response_body = template["body"].format(
                sender_name=sender_name,
                information_provided=information_provided
            )
        elif email_type == EmailType.FOLLOW_UP:
            update_details = "I wanted to update you on the status of this matter. [Specific update details would go here based on the original request]"
            response_body = template["body"].format(
                sender_name=sender_name,
                update_details=update_details
            )
        else:
            response_content = "I've reviewed your message and will address your concerns. [Specific response content would go here based on the inquiry]"
            response_body = template["body"].format(
                sender_name=sender_name,
                response_content=response_content
            )

        return response_body

    def generate_response(self, email: Email, tone_style: str = "professional") -> EmailResponse:
        """
        Generate an appropriate response to the email.
        """
        email_type, confidence = self.identify_email_type(email)

        # Get the appropriate template
        template = self.response_templates.get(email_type, self.response_templates[EmailType.GENERAL_INQUIRY])

        # Personalize the response
        personalized_body = self.personalize_response(template, email, email_type)

        # Create subject (reply to original)
        original_subject = email.subject
        if not email.subject.lower().startswith(('re:', 're :', 'fw:', 'fwd:')):
            subject = f"Re: {original_subject}"
        else:
            subject = email.subject

        # Apply tone style if needed
        tone_info = self.tone_styles.get(tone_style, self.tone_styles["professional"])

        return EmailResponse(
            subject=subject,
            body=personalized_body,
            confidence=confidence,
            suggested_tone=tone_style
        )

    def analyze_email_tone(self, email: Email) -> str:
        """
        Analyze the tone of the incoming email to suggest appropriate response tone.
        """
        body_lower = email.body.lower()
        subject_lower = email.subject.lower()

        # Look for indicators of formality
        formal_indicators = [
            "dear", "sir", "madam", "regarding", "respectfully", "therefore",
            "whereas", "pursuant", "enclosed please find", "attached herewith"
        ]

        informal_indicators = [
            "hey", "hi there", "hope you're well", "thanks!", "cheers",
            "talk soon", "later", "bye"
        ]

        formal_count = sum(1 for indicator in formal_indicators if indicator in body_lower or indicator in subject_lower)
        informal_count = sum(1 for indicator in informal_indicators if indicator in body_lower or indicator in subject_lower)

        if formal_count > informal_count:
            return "professional"
        elif informal_count > formal_count:
            return "friendly_professional"
        else:
            return "friendly_professional"  # Default friendly professional

def create_email_responder_skill():
    """Factory function to create the email responder skill."""
    return EmailResponder()

# Example usage
if __name__ == "__main__":
    # Sample email
    sample_email = Email(
        sender="john.doe@example.com",
        subject="Meeting Request for Project Discussion",
        body="Hi, I hope this email finds you well. I would like to schedule a meeting to discuss the upcoming project. Are you available next week?",
        timestamp=datetime.now()
    )

    responder = create_email_responder_skill()
    suggested_tone = responder.analyze_email_tone(sample_email)
    response = responder.generate_response(sample_email, tone_style=suggested_tone)

    print(f"Subject: {response.subject}")
    print(f"Confidence: {response.confidence:.2f}")
    print(f"Suggested Tone: {response.suggested_tone}")
    print(f"Body:\n{response.body}")
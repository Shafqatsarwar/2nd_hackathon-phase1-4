"""
Meeting Minutes Generator Skill
Automatically generates structured meeting minutes from audio transcripts or meeting notes.
"""
import re
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class ActionItem:
    description: str
    owner: str
    deadline: str
    status: str = "Pending"

@dataclass
class Decision:
    topic: str
    description: str
    participants: List[str]

@dataclass
class DiscussionPoint:
    topic: str
    summary: str
    participants: List[str]

class MeetingMinutesGenerator:
    """
    Skill to automatically generate structured meeting minutes from raw notes or transcripts.
    """

    def __init__(self):
        self.action_item_patterns = [
            r"(?:action item|next step|to do|todo|follow up):\s*(.+?)(?:\n|$)",
            r"(?:needs to|should|will)\s+(.+?)(?:\n|$)",
            r"(?:assign(?:ed)? to|owner is)\s*(.+?)(?:\n|$)"
        ]

        self.decision_patterns = [
            r"(?:decision|agreed|resolved):\s*(.+?)(?:\n|$)",
            r"(?:decided to|resolution|conclusion):\s*(.+?)(?:\n|$)"
        ]

        self.participant_pattern = r"(?:^|\n)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):"

    def extract_participants(self, transcript: str) -> List[str]:
        """Extract participant names from the transcript."""
        matches = re.findall(self.participant_pattern, transcript)
        return list(set(matches))  # Remove duplicates

    def extract_action_items(self, transcript: str) -> List[ActionItem]:
        """Extract action items from the transcript."""
        action_items = []

        for pattern in self.action_item_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            for match in matches:
                # Try to extract owner and deadline from the context
                owner = self._extract_owner(match)
                deadline = self._extract_deadline(match)

                action_items.append(ActionItem(
                    description=match.strip(),
                    owner=owner,
                    deadline=deadline
                ))

        return action_items

    def _extract_owner(self, text: str) -> str:
        """Extract owner from action item text."""
        # Look for phrases like "John will", "assigned to Mary", etc.
        owner_patterns = [
            r"(?:assigned to|owner is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:will|needs to|should)"
        ]

        for pattern in owner_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return "Unassigned"

    def _extract_deadline(self, text: str) -> str:
        """Extract deadline from action item text."""
        deadline_patterns = [
            r"(?:by|before|due)\s+(\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)",
            r"(?:by|before|due)\s+(?:end of\s+)?(?:this|next)\s+(week|month|quarter|day)",
            r"(?:on|at)\s+(?:the\s+)?(\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)"
        ]

        for pattern in deadline_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return "Not specified"

    def extract_decisions(self, transcript: str) -> List[Decision]:
        """Extract decisions from the transcript."""
        decisions = []

        for pattern in self.decision_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            for match in matches:
                # Get participants involved in this decision
                participants = self.extract_participants(match[:200])  # Look in context around decision

                decisions.append(Decision(
                    topic="General",
                    description=match.strip(),
                    participants=participants
                ))

        return decisions

    def extract_discussion_points(self, transcript: str, max_points: int = 10) -> List[DiscussionPoint]:
        """Extract key discussion points from the transcript."""
        # This is a simplified version - in a real implementation,
        # we'd use more sophisticated NLP techniques
        lines = transcript.split('\n')
        discussion_points = []

        for line in lines:
            if len(line.strip()) > 20:  # Likely a substantial point
                # Skip lines that are clearly action items or decisions
                if not any(re.search(p, line, re.IGNORECASE) for p in self.action_item_patterns + self.decision_patterns):
                    if len(discussion_points) < max_points:
                        discussion_points.append(DiscussionPoint(
                            topic="General Topic",
                            summary=line.strip(),
                            participants=[]
                        ))

        return discussion_points

    def generate_minutes(self, transcript: str, meeting_title: str = "Meeting") -> str:
        """Generate structured meeting minutes from the transcript."""
        participants = self.extract_participants(transcript)
        action_items = self.extract_action_items(transcript)
        decisions = self.extract_decisions(transcript)
        discussion_points = self.extract_discussion_points(transcript)

        # Format the minutes
        minutes = f"# {meeting_title} - {datetime.now().strftime('%B %d, %Y')}\n\n"

        # Participants
        if participants:
            minutes += "## Attendees\n"
            for participant in participants:
                minutes += f"- {participant}\n"
            minutes += "\n"

        # Decisions
        if decisions:
            minutes += "## Decisions Made\n"
            for i, decision in enumerate(decisions, 1):
                minutes += f"{i}. {decision.description}\n"
            minutes += "\n"

        # Action Items
        if action_items:
            minutes += "## Action Items\n"
            for i, item in enumerate(action_items, 1):
                minutes += f"{i}. **{item.description}**\n"
                minutes += f"   - Owner: {item.owner}\n"
                minutes += f"   - Deadline: {item.deadline}\n"
                minutes += f"   - Status: {item.status}\n\n"
        else:
            minutes += "## Action Items\n"
            minutes += "No action items identified.\n\n"

        # Key Discussion Points
        if discussion_points:
            minutes += "## Key Discussion Points\n"
            for i, point in enumerate(discussion_points, 1):
                minutes += f"{i}. {point.summary}\n"

        return minutes

def create_meeting_minutes_skill():
    """Factory function to create the meeting minutes generator skill."""
    return MeetingMinutesGenerator()

# Example usage
if __name__ == "__main__":
    # Sample transcript
    sample_transcript = """
    John: We need to finalize the project timeline.
    Sarah: Agreed, the deadline is approaching.
    Decision: We will extend the deadline by two weeks.
    Mike: John will update the project plan by Friday.
    Lisa: Sarah should coordinate with the design team.
    John: We also need to schedule the client meeting.
    """

    generator = create_meeting_minutes_skill()
    minutes = generator.generate_minutes(sample_transcript, "Project Planning Meeting")
    print(minutes)
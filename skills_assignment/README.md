# Human Job Skills Extraction

This project contains **2 focused, reusable capabilities** extracted from daily work routines. Each skill is designed to replace manual tasks, save time, and reduce mental load.

## Skills Overview

| Skill | Purpose | Time Saved | Quality Improved |
|-------|---------|------------|------------------|
| **Email Responder** | Automatically generates appropriate responses to common types of emails | 5-15 minutes → 1-2 minutes | Consistent communication style, reduced typos, professional tone |
| **Meeting Minutes Generator** | Automatically generates structured meeting minutes from transcripts or notes | 30-45 minutes → 3-5 minutes | Standardized format, consistent action item identification |

## Total Impact
- **Time Savings**: 35-60 minutes per day
- **Quality Improvements**: Standardized outputs, reduced errors, consistent formatting
- **Mental Load Reduction**: Automated repetitive tasks, freeing up cognitive resources

## Skills Implemented

### 1. Email Responder
**File**: `email_responder.py` (299 lines)

Analyzes incoming emails and automatically generates contextually appropriate responses:
- **Identifies email types**: Meeting requests, information requests, follow-ups, acknowledgments
- **Personalizes responses**: Extracts sender names and customizes templates
- **Analyzes tone**: Suggests appropriate response tone (professional, friendly-professional, casual)
- **Confidence scoring**: Provides confidence level for each generated response

**Time Saved**: 5-15 minutes → 1-2 minutes per email

### 2. Meeting Minutes Generator
**File**: `meeting_minutes_generator.py` (202 lines)

Converts raw meeting transcripts into structured, professional meeting minutes:
- **Extracts participants**: Automatically identifies meeting attendees
- **Identifies action items**: Finds tasks with owners and deadlines
- **Captures decisions**: Extracts key decisions made during the meeting
- **Formats professionally**: Generates standardized markdown output

**Time Saved**: 30-45 minutes → 3-5 minutes per meeting

## Quick Start

Run the demonstration script to see both skills in action:

```bash
python demo_skills.py
```

Or run individual skills:

```bash
# Email Responder Demo
python email_responder.py

# Meeting Minutes Generator Demo
python meeting_minutes_generator.py
```

## Files Structure

```
skills_assignment/
├── README.md                           # This file
├── SKILLS_SUMMARY.md                   # Detailed skills summary
├── demo_skills.py                      # Combined demonstration script
├── email_responder.py                  # Email responder implementation
├── email_responder.skill.md            # Email responder specification
├── meeting_minutes_generator.py        # Meeting minutes implementation
├── meeting_minutes_generator.skill.md  # Meeting minutes specification
└── templates/                          # Template files
```

## Reference

Based on the Claude Code Features assignment from Part 2, Chapter 5.
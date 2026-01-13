# Meeting Minutes Generator Skill

## Purpose
Automatically generates structured meeting minutes from audio transcripts or meeting notes.

## Functionality
- Converts raw meeting notes or transcribed audio into structured minutes
- Identifies action items, decisions, and key discussion points
- Formats minutes in a standardized template
- Highlights follow-up tasks with assigned owners

## Input
- Raw meeting transcript or notes
- Meeting participants list
- Meeting agenda topics

## Output
- Structured meeting minutes document
- Action items summary with owners and deadlines
- Key decisions and discussion points

## LOC
Approximately 200-300 lines of code

## Measurement
- Time reduction: From 30-45 minutes manual work to 3-5 minutes automated
- Consistency: Standardized format across all meetings
- Accuracy: Consistent identification of action items

## Files
- `meeting_minutes_generator.py`
- `templates/meeting_minutes_template.md`
- `utils/transcript_parser.py`
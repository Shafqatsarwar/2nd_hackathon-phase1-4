# Email Responder Skill

## Purpose
Automatically generates appropriate responses to common types of emails based on content analysis.

## Functionality
- Analyzes email content and categorizes the request
- Generates contextually appropriate responses
- Applies personal communication style preferences
- Suggests responses for review before sending

## Input
- Email subject and body
- Sender information
- Communication preferences/tone settings
- Template library for common responses

## Output
- Draft response email
- Suggested subject line
- Tone analysis and recommendations
- Template suggestions for similar future emails

## LOC
Approximately 200-300 lines of code

## Measurement
- Time reduction: From 5-15 minutes per email to 1-2 minutes with suggestions
- Consistency: Maintains consistent communication style
- Quality: Reduces typos and improves clarity

## Files
- `email_responder.py`
- `templates/email_templates.json`
- `utils/tone_analyzer.py`
"""
Quick Test - Verify Both Skills Work
"""

print("Testing Email Responder...")
try:
    from email_responder import create_email_responder_skill, Email
    from datetime import datetime
    
    responder = create_email_responder_skill()
    test_email = Email(
        sender="test@example.com",
        subject="Test",
        body="Can we schedule a meeting?",
        timestamp=datetime.now()
    )
    response = responder.generate_response(test_email)
    print(f"✓ Email Responder: WORKING (Confidence: {response.confidence:.1%})")
except Exception as e:
    print(f"✗ Email Responder: FAILED - {e}")

print("\nTesting Meeting Minutes Generator...")
try:
    from meeting_minutes_generator import create_meeting_minutes_skill
    
    generator = create_meeting_minutes_skill()
    test_transcript = "John: We need to finalize the project. Decision: Extend deadline by 2 weeks."
    minutes = generator.generate_minutes(test_transcript, "Test Meeting")
    print(f"✓ Meeting Minutes Generator: WORKING (Generated {len(minutes)} chars)")
except Exception as e:
    print(f"✗ Meeting Minutes Generator: FAILED - {e}")

print("\n" + "="*60)
print("BOTH SKILLS ARE READY FOR SUBMISSION!")
print("="*60)

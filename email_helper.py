def suggest_email_template(template_type):
    """Suggests an email template based on the requested type."""
    
    templates = {
        "formal": """Subject: [Your Subject Here]

Dear [Recipient's Name],

I hope this email finds you well. I wanted to discuss [topic]. Please let me know a suitable time to connect.

Best regards,  
[Your Name]""",
        
        "informal": """Subject: Hey [Recipient's Name]!

Hey [Recipient's Name],

Hope you're doing great! Just wanted to check in about [topic]. Let me know when you're free.

Cheers,  
[Your Name]""",

        "job application": """Subject: Job Application for [Position]

Dear Hiring Manager,

I am excited to apply for the [Position] role at [Company]. My experience in [field] makes me a strong fit. Please find my resume attached.

Looking forward to hearing from you.

Best,  
[Your Name]""",

        "meeting request": """Subject: Request for Meeting - [Topic]

Dear [Recipient's Name],

I hope you're doing well. I’d like to schedule a meeting to discuss [topic]. Please let me know a convenient time for you.

Looking forward to your response.

Best regards,  
[Your Name]""",

        "follow-up": """Subject: Follow-up on [Previous Conversation/Meeting]

Dear [Recipient's Name],

I wanted to follow up on our recent conversation about [topic]. Please let me know if you need any further information.

Looking forward to your reply.

Best,  
[Your Name]""",

        "leave request": """Subject: Leave Request for [Dates]

Dear [Manager's Name],

I hope you're doing well. I am writing to formally request leave from [start date] to [end date] due to [reason]. Please let me know if any additional information is required.

Thank you for your consideration.

Best regards,  
[Your Name]""",

        "apology": """Subject: Apology for [Incident]

Dear [Recipient's Name],

I sincerely apologize for [specific issue]. It was never my intention to [cause issue]. I assure you that I am taking steps to prevent this from happening again.

Thank you for your understanding.

Best,  
[Your Name]""",

        "client proposal": """Subject: Business Proposal for [Service/Product]

Dear [Client's Name],

I am excited to present a proposal for [service/product] that can help [client's company] achieve [goal]. Attached is a detailed proposal outlining our approach.

I’d love the opportunity to discuss this further at your convenience.

Looking forward to your response.

Best regards,  
[Your Name]""",

        "project update": """Subject: Project Update - [Project Name]

Dear [Recipient's Name],

I’d like to provide an update on [project name]. As of today, we have completed [milestone]. The next steps are [next actions].

Please let me know if you need any further details.

Best,  
[Your Name]""",

        "resignation": """Subject: Resignation Notice

Dear [Manager's Name],

I am writing to formally resign from my position at [Company Name], effective [last working day]. I appreciate the opportunities and experiences I have gained during my tenure.

Please let me know how I can ensure a smooth transition.

Best regards,  
[Your Name]""",

        "thank you": """Subject: Thank You!

Dear [Recipient's Name],

I wanted to express my gratitude for [specific help/support]. I truly appreciate your time and effort.

Looking forward to staying in touch!

Best,  
[Your Name]"""
    }

    return templates.get(template_type.lower(), "Template not found. Available types: formal, informal, job application, meeting request, follow-up, leave request, apology, client proposal, project update, resignation, thank you.")

def autocomplete_sentence(partial_text):
    """Autocompletes common business email phrases."""
    
    suggestions = {
        "thank you for": "Thank you for your time and consideration. Looking forward to your response.",
        "looking forward to": "Looking forward to working with you and your team on this project.",
        "I hope": "I hope this email finds you well and in good health.",
        "as per our discussion": "As per our discussion, I have attached the necessary documents for your review.",
        "please find attached": "Please find attached the requested documents for your review.",
        "let me know": "Let me know if you have any questions or need further information."
    }

    return suggestions.get(partial_text.lower(), f"Could not find a suggestion for '{partial_text}'.")

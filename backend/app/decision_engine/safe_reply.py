"""
GuardianAI Safe Reply Template Generator
Purpose: Generates polite, firm, and safe decline reply templates across 9 scam categories
         (Fake Jobs, Lottery, Banks, Investment, OTP Requests, Loan Scams, Government, Courier, Unknown Contacts)
         with built-in multilingual locale support (English, Spanish, Hindi, French).
"""

from typing import Dict, Optional
from pydantic import BaseModel, Field

class SafeReplyTemplate(BaseModel):
    """Structured Safe Reply Output DTO."""
    category_key: str
    locale: str
    template_title: str
    safe_reply_text: str

# Master Multilingual Safe Reply Template Catalog
SAFE_REPLY_CATALOG: Dict[str, Dict[str, Dict[str, str]]] = {
    "JOB_SCAM": {
        "en": {
            "title": "Polite Job Offer Decline",
            "text": "Thank you for reaching out, but I am not interested in unsolicited job opportunities at this time."
        },
        "es": {
            "title": "Rechazo amable de oferta de trabajo",
            "text": "Gracias por ponerse en contacto, pero no estoy interesado en ofertas de trabajo no solicitadas en este momento."
        },
        "hi": {
            "title": "नौकरी के प्रस्ताव को विनम्रता से अस्वीकार करें",
            "text": "संपर्क करने के लिए धन्यवाद, लेकिन मैं इस समय अनचाहे नौकरी के अवसरों में रुचि नहीं रखता।"
        },
        "fr": {
            "title": "Refus poli d'offre d'emploi",
            "text": "Merci de m'avoir contacté, mais je ne suis pas intéressé par les opportunités d'emploi non sollicitées pour le moment."
        }
    },
    "LOTTERY_SCAM": {
        "en": {
            "title": "Prize Claim Decline",
            "text": "I have not entered any lottery or contest. Please remove my contact details from your list."
        },
        "es": {
            "title": "Rechazo de reclamo de premio",
            "text": "No he participado en ninguna lotería o concurso. Por favor, elimine mis datos de contacto de su lista."
        },
        "hi": {
            "title": "पुरस्कार के दावे को अस्वीकार करें",
            "text": "मैंने किसी भी लॉटरी या प्रतियोगिता में भाग नहीं लिया है। कृपया मेरी जानकारी अपनी सूची से हटाएं।"
        },
        "fr": {
            "title": "Refus de réclamation de loterie",
            "text": "Je n'ai participé à aucune loterie ni concours. Veuillez supprimer mes coordonnées de votre liste."
        }
    },
    "BANK_SPOOF": {
        "en": {
            "title": "Official Bank Direct Portal Notice",
            "text": "I will handle any account updates directly through my official banking app. Do not send further links."
        },
        "es": {
            "title": "Aviso de portal bancario oficial",
            "text": "Gestionaré las actualizaciones de mi cuenta directamente a través de mi aplicación bancaria oficial."
        },
        "hi": {
            "title": "आधिकारिक बैंक डायरेक्ट पोर्टल सूचना",
            "text": "मैं अपने खाते के सभी अपडेट सीधे अपने आधिकारिक बैंक ऐप के माध्यम से प्रबंधित करूंगा।"
        },
        "fr": {
            "title": "Avis du portail bancaire officiel",
            "text": "Je traiterai les mises à jour de mon compte directement via mon application bancaire officielle."
        }
    },
    "INVESTMENT_SCAM": {
        "en": {
            "title": "Investment Offer Refusal",
            "text": "I do not participate in unsolicited investment schemes or crypto opportunities. Please do not contact me again."
        },
        "es": {
            "title": "Rechazo de oferta de inversión",
            "text": "No participo en esquemas de inversión no solicitados. Por favor, no me contacte de nuevo."
        },
        "hi": {
            "title": "निवेश प्रस्ताव को अस्वीकार करें",
            "text": "मैं अनचाहे निवेश प्रस्तावों में भाग नहीं लेता। कृपया मुझे पुनः संपर्क न करें।"
        },
        "fr": {
            "title": "Refus d'offre d'investissement",
            "text": "Je ne participe pas à des opportunités d'investissement non sollicitées. Veuillez ne plus me contacter."
        }
    },
    "OTP_REQUEST": {
        "en": {
            "title": "Security OTP Refusal",
            "text": "Security Alert: One-Time Passwords (OTP) are private and are never shared under any circumstances."
        },
        "es": {
            "title": "Rechazo de OTP por seguridad",
            "text": "Alerta de seguridad: Las contraseñas de un solo uso (OTP) son privadas y nunca se comparten."
        },
        "hi": {
            "title": "सुरक्षा ओटीपी अस्वीकृति",
            "text": "सुरक्षा चेतावनी: वन-टाइम पासवर्ड (OTP) व्यक्तिगत होते हैं और इन्हें किसी के साथ साझा नहीं किया जाता।"
        },
        "fr": {
            "title": "Refus d'OTP de sécurité",
            "text": "Alerte de sécurité : Les mots de passe à usage unique (OTP) sont privés et ne sont jamais partagés."
        }
    },
    "LOAN_SCAM": {
        "en": {
            "title": "Pre-Approved Loan Refusal",
            "text": "I have not applied for any loan or credit line and do not require financing. Please stop sending solicitations."
        },
        "es": {
            "title": "Rechazo de préstamo preaprobado",
            "text": "No he solicitado ningún préstamo y no requiero financiamiento. Por favor deje de enviar solicitudes."
        },
        "hi": {
            "title": "ऋण प्रस्ताव अस्वीकृति",
            "text": "मैंने किसी ऋण के लिए आवेदन नहीं किया है। कृपया मुझे संदेश भेजना बंद करें।"
        },
        "fr": {
            "title": "Refus de prêt préapprouvé",
            "text": "Je n'ai demandé aucun prêt et je n'ai pas besoin de financement. Veuillez cesser vos envois."
        }
    },
    "GOVERNMENT_NOTICE": {
        "en": {
            "title": "Official Government Inquiry Notice",
            "text": "I will verify any official government notices directly with the appropriate department hotline. Do not send further texts."
        },
        "es": {
            "title": "Aviso de verificación oficial",
            "text": "Verificaré cualquier aviso oficial directamente con la línea telefónica del departamento correspondiente."
        },
        "hi": {
            "title": "सरकारी सूचना सत्यापन",
            "text": "मैं किसी भी सरकारी सूचना का सत्यापन सीधे संबंधित विभाग के आधिकारिक फोन नंबर पर करूंगा।"
        },
        "fr": {
            "title": "Avis de vérification officielle",
            "text": "Je vérifierai tout avis officiel directement auprès de la ligne téléphonique du ministère concerné."
        }
    },
    "COURIER_SCAM": {
        "en": {
            "title": "Courier Tracking Notice",
            "text": "I will check parcel tracking details directly on the official courier website. I will not click third-party payment links."
        },
        "es": {
            "title": "Aviso de seguimiento de mensajería",
            "text": "Verificaré los detalles del paquete directamente en el sitio web oficial del servicio de mensajería."
        },
        "hi": {
            "title": "पार्सल ट्रैकिंग सूचना",
            "text": "मैं पार्सल की स्थिति सीधे आधिकारिक कूरियर वेबसाइट पर देखूंगा। मैं किसी तृतीय-पक्ष लिंक पर क्लिक नहीं करूंगा।"
        },
        "fr": {
            "title": "Avis de suivi de colis",
            "text": "Je vérifierai les détails du suivi du colis directement sur le site web officiel du transporteur."
        }
    },
    "GENERIC": {
        "en": {
            "title": "Unknown Contact Decline",
            "text": "I do not recognize this sender. Please do not contact me again."
        },
        "es": {
            "title": "Rechazo de contacto desconocido",
            "text": "No reconozco a este remitente. Por favor, no me contacte de nuevo."
        },
        "hi": {
            "title": "अज्ञात संपर्क अस्वीकृति",
            "text": "मैं इस भेजने वाले को नहीं पहचानता। कृपया मुझे पुनः संपर्क न करें।"
        },
        "fr": {
            "title": "Refus de contact inconnu",
            "text": "Je ne reconnais pas cet expéditeur. Veuillez ne plus me contacter."
        }
    }
}

class SafeReplyGenerator:
    """Enterprise Safe Reply Template Generator."""

    @classmethod
    def generate_reply(cls, scam_category: str = "GENERIC", locale: str = "en") -> SafeReplyTemplate:
        """
        Generates a polite, firm, safe decline reply template for the given scam category and language locale.
        """
        category_key = scam_category.upper()
        lang = locale.lower() if locale in ("en", "es", "hi", "fr") else "en"

        cat_dict = SAFE_REPLY_CATALOG.get(category_key, SAFE_REPLY_CATALOG["GENERIC"])
        template_info = cat_dict.get(lang, cat_dict["en"])

        return SafeReplyTemplate(
            category_key=category_key,
            locale=lang,
            template_title=template_info["title"],
            safe_reply_text=template_info["text"]
        )

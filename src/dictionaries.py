"""Dictionaries (regular expressions) used in Layers A, B and C.

All patterns are applied to lower-cased text with word boundaries, at document
level (a concept counts once per record). See Appendix Table A1 of the paper.
"""

# ---------------------------------------------------------------- Layer A
# Seed health keywords and thematic categories for the 37 VOSviewer keywords
HEALTH_SEEDS = [
    "telemedicine", "rural health", "digital health", "health disparities",
    "health equity", "social determinants of health", "pandemic",
]
KEYWORD_CATEGORIES = {
    "Health": HEALTH_SEEDS,
    "Connectivity infrastructure": [
        "5g", "access", "broadband", "connectivity", "ict", "internet",
        "internet access", "rural broadband", "dvb-rct2", "technology",
    ],
    "Digital inclusion": [
        "digital divide", "digital inclusion", "digital literacy", "cultural capital",
        "internet use", "digital society", "information society", "social participation",
    ],
    "Geographical and social inequality": [
        "rural", "rural communities", "rural china", "rural-urban", "indonesia",
        "social inequality", "socioeconomic factors",
    ],
    "Sectors, populations and methods": [
        "education", "online education", "older adults", "veterans",
        "propensity score matching",
    ],
}

# ---------------------------------------------------------------- Layer B
# Health dictionary for sub-corpus extraction (pandemic/COVID-19 excluded on purpose)
HEALTH_DICTIONARY = (
    r"\bhealth|\btele[\s-]?(medicine|health|care|consult\w*|monitoring|psychiatr\w*|rehabilitation)\b"
    r"|\bvirtual (care|visits?)\b|\bm[\s-]?health\b|\be[\s-]?health\b"
    r"|\bmedic(al|ine|aid|are)\b|\bclinic(s|al)?\b|\bhospitals?\b|\bpatients?\b|\bphysicians?\b"
    r"|\bnurs(e|es|ing)\b|\bprimary care\b|\bdiseases?\b|\bcancer\b|\bdiabet\w*|\bhypertension\b"
    r"|\bdementia\b|\bdepressi\w*|\bmental (health|illness)\b|\bmortality\b|\bnutrition\w*"
    r"|\bobesity\b|\bmaternal (health|care)\b|\bvaccin\w*|\bwell[\s-]?being\b|\bquality of life\b"
)
# Rule (b): health-related MeSH headings
HEALTH_MESH = r"telemedicine|health|patient|medical|delivery of health care|disease"

# ---------------------------------------------------------------- Layer C
HEALTH_CONCEPTS = {
    "Telemedicine and telehealth": r"\btele[\s-]?(medicine|health|care|consult\w*|monitoring|psychiatr\w*|rehabilitation)\b|\bvirtual (care|visits?|ward)\b|\bremote (patient )?monitoring\b",
    "Digital health and mHealth": r"\bdigital health\b|\bm[\s-]?health\b|\be[\s-]?health\b|\bpatient portals?\b|\bhealth informatics\b",
    "Healthcare access and services": r"\baccess to (health ?care|care|health services)\b|\bhealth ?care access\b|\bhealth services?\b|\bhealth ?care (delivery|services?|system)\b|\bprimary care\b",
    "Health equity and disparities": r"\bhealth (equity|inequit\w*|disparit\w*|inequalit\w*)\b",
    "Mental health and well-being": r"\bmental health\b|\bdepress\w*|\banxiety\b|\bwell[\s-]?being\b|\bloneliness\b|\bquality of life\b|\bpsycholog\w*",
    "Chronic disease management": r"\bchronic\b|\bdiabet\w*|\bhypertension\b|\bcancer\b|\bcardiac\b|\bdementia\b|\barthritis\b|\bhepatitis\b",
    "Health literacy": r"\bhealth literacy\b",
    "Social determinants of health": r"\bsocial determinants? of health\b|\bdeterminants? of health\b",
    "Pandemic (COVID-19)": r"\bcovid\w*|\bpandemic\b|\bsars-cov-2\b",
}

CONNECTIVITY_CONCEPTS = {
    "Digital divide": r"\bdigital (divide|inequalit\w*|gap)\b",
    "Digital inclusion": r"\bdigital (inclusion|exclusion)\b",
    "Broadband and internet access": r"\bbroadband\b|\binternet access\b",
    "Mobile, wireless and satellite": r"\bmobile\b|\bwireless\b|\bsatellite\b|\b5g\b|\bwhite space\b|\bcellular\b",
    "Digital literacy and skills": r"\bdigital (literacy|skills?|competenc\w*)\b",
    "Rural and remote settings": r"\brural\b|\bremote (areas?|regions?|communit\w*)\b",
    "Underserved and marginalized groups": r"\bunderserved\b|\bmarginali[sz]ed\b|\bindigenous\b|\bminorit\w*|\blow-income\b",
    "Older adults": r"\bolder adults?\b|\belderly\b|\bseniors?\b|\baging\b|\bageing\b",
}

# Universal and meaningful connectivity (ITU & OSET, 2022)
UMC_DIMENSIONS = {
    "Quality": r"\bbandwidth\b|\bspeeds?\b|\blatency\b|\bmbps\b|\bquality of (service|connection|internet)\b|\breliab\w*|\bstable (connection|internet)\b|\bconnection quality\b|\bpoor connectivity\b",
    "Availability": r"\bbroadband (access|availability|coverage|infrastructure)\b|\bcoverage\b|\binternet access\b|\binfrastructure\b|\bavailability\b",
    "Affordability": r"\bafford\w*|\bcosts? of (internet|data|broadband|access)\b|\bprices?\b|\bsubscription\b",
    "Devices": r"\bdevices?\b|\bsmartphones?\b|\bcomputers?\b|\btablets?\b|\blaptops?\b",
    "Skills": r"\bliterac\w*|\bskills?\b|\bcompetenc\w*|\bself-efficacy\b",
    "Security": r"\bprivacy\b|\bsecurity\b|\bcyber\w*|\bonline safety\b|\bscams?\b|\bfraud\b",
}

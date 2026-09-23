import requests
from datetime import datetime


REAL_PROJECT_SEEDS = [
    {
        "project_id": "REAL_001",
        "project_name": "Delhi–Mumbai Expressway",
        "project_type": "Highway",
        "agency": "NHAI",
        "state": "Rajasthan",
        "district": "Dausa",
        "village": "Peechupara Khurd",
        "land_required_ha": 980.0,
        "affected_families": 420,
        "current_stage": "Award",
        "source_name": "NHAI / OpenStreetMap geocoding",
        "source_url": "https://nhai.gov.in/",
        "latitude": 26.9993073,
        "longitude": 76.5697388,
        "base_delay_probability": 0.71,
        "risk_level": "HIGH",
        "risk_color": "RED",
    },
    {
        "project_id": "REAL_002",
        "project_name": "Ganga Expressway",
        "project_type": "Expressway",
        "agency": "UPEIDA",
        "state": "Uttar Pradesh",
        "district": "Meerut",
        "village": "Meerut Corridor",
        "land_required_ha": 760.0,
        "affected_families": 360,
        "current_stage": "Notification",
        "source_name": "UP Expressways / OpenStreetMap",
        "source_url": "https://upeida.in/",
        "latitude": 28.9845,
        "longitude": 77.7064,
        "base_delay_probability": 0.64,
        "risk_level": "MEDIUM",
        "risk_color": "ORANGE",
    },
    {
        "project_id": "REAL_003",
        "project_name": "Char Dham Highway Project",
        "project_type": "Highway",
        "agency": "MoRTH",
        "state": "Uttarakhand",
        "district": "Rudraprayag",
        "village": "Rudraprayag Valley",
        "land_required_ha": 640.0,
        "affected_families": 290,
        "current_stage": "Survey",
        "source_name": "MoRTH / OpenStreetMap",
        "source_url": "https://morth.nic.in/",
        "latitude": 30.2852,
        "longitude": 78.9833,
        "base_delay_probability": 0.73,
        "risk_level": "HIGH",
        "risk_color": "RED",
    },
    {
        "project_id": "REAL_004",
        "project_name": "Mumbai Metro Line 3",
        "project_type": "Metro",
        "agency": "MMRCL",
        "state": "Maharashtra",
        "district": "Mumbai",
        "village": "Colaba to Seepz",
        "land_required_ha": 420.0,
        "affected_families": 210,
        "current_stage": "Construction",
        "source_name": "MMRCL / OpenStreetMap",
        "source_url": "https://mmrcl.com/",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "base_delay_probability": 0.42,
        "risk_level": "MEDIUM",
        "risk_color": "ORANGE",
    },
    {
        "project_id": "REAL_005",
        "project_name": "Delhi Metro Phase IV",
        "project_type": "Metro",
        "agency": "DMRC",
        "state": "Delhi",
        "district": "New Delhi",
        "village": "Delhi Metro Corridor",
        "source_name": "Delhi Metro Rail Corporation",
        "source_url": "https://delhimetrorail.com/",
        "source_document_url": "https://delhimetrorail.com/pages/en/about_us",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "base_delay_probability": 0.0,
        "risk_level": "NO_RISK",
        "risk_color": "GREEN",
    },
    {
        "project_id": "REAL_006",
        "project_name": "Chennai Metro Rail Project",
        "project_type": "Metro",
        "agency": "CMRL",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "village": "Chennai Metro Corridor",
        "source_name": "Chennai Metro Rail Limited",
        "source_url": "https://chennaimetrorail.org/",
        "source_document_url": "https://chennaimetrorail.org/project-status-2/",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "base_delay_probability": 0.0,
        "risk_level": "NO_RISK",
        "risk_color": "GREEN",
    },
    {
        "project_id": "REAL_007",
        "project_name": "Bharatmala Pariyojana",
        "project_type": "Highway",
        "agency": "NHAI",
        "state": "India",
        "district": "Multiple districts",
        "village": "Multiple locations",
        "source_name": "National Highways Authority of India",
        "source_url": "https://nhai.gov.in/",
        "source_document_url": "https://nhai.gov.in/assets/pdf/Bharatmala_NH_highlighted_2023_Project.pdf",
        "latitude": 22.9734,
        "longitude": 78.6569,
        "base_delay_probability": 0.0,
        "risk_level": "NO_RISK",
        "risk_color": "GREEN",
    },
    {
        "project_id": "REAL_008",
        "project_name": "Zojila Tunnel Project",
        "project_type": "Tunnel",
        "agency": "NHIDCL",
        "state": "Jammu and Kashmir",
        "district": "Ganderbal",
        "village": "Sonamarg Corridor",
        "source_name": "National Highways and Infrastructure Development Corporation",
        "source_url": "https://nhidcl.com/",
        "source_document_url": "https://nhidcl.com/",
        "latitude": 34.1367,
        "longitude": 75.2934,
        "base_delay_probability": 0.0,
        "risk_level": "NO_RISK",
        "risk_color": "GREEN",
    },
    {
        "project_id": "REAL_009",
        "project_name": "Mumbai–Nagpur Expressway",
        "project_type": "Expressway",
        "agency": "MSRDC",
        "state": "Maharashtra",
        "district": "Nagpur",
        "village": "Nagpur Corridor",
        "source_name": "Maharashtra State Road Development Corporation",
        "source_url": "https://www.msrdc.org/",
        "source_document_url": "https://www.msrdc.org/",
        "latitude": 20.8500,
        "longitude": 79.0200,
        "base_delay_probability": 0.0,
        "risk_level": "NO_RISK",
        "risk_color": "GREEN",
    },
    {
        "project_id": "REAL_010",
        "project_name": "Eastern Dedicated Freight Corridor",
        "project_type": "Railway",
        "agency": "DFCCIL",
        "state": "Uttar Pradesh",
        "district": "Prayagraj",
        "village": "Freight Corridor",
        "source_name": "Dedicated Freight Corridor Corporation of India",
        "source_url": "https://dfccil.com/",
        "source_document_url": "https://dfccil.com/Home/DynemicPages?MenuId=76",
        "latitude": 25.4358,
        "longitude": 81.8463,
        "base_delay_probability": 0.0,
        "risk_level": "NO_RISK",
        "risk_color": "GREEN",
    },
]


def build_project_barriers(seed):
    """Return contextual barriers without presenting estimates as live facts."""
    common = {
        'source_name': seed['source_name'],
        'source_url': seed['source_url'],
        'verification_status': 'public_snapshot',
        'observed_at': datetime.utcnow(),
    }
    barriers = [
        {
            **common,
            'category': 'climate',
            'title': 'Weather disruption exposure',
            'severity': 'MEDIUM',
            'impact_score': 48,
            'status': 'Needs current IMD district warning check',
            'description': f"{seed['district']} requires a current IMD warning and rainfall check before this is treated as a live project condition.",
            'mitigation': 'Refresh IMD warnings and rainfall observations for the project district.',
            'source_name': 'IMD public warning service',
            'source_url': 'https://mausam.imd.gov.in/',
        },
        {
            **common,
            'category': 'landscape',
            'title': 'Terrain and land-use constraint',
            'severity': 'MEDIUM',
            'impact_score': 42,
            'status': 'Contextual screening',
            'description': f"Project-level coordinates do not describe parcel boundaries or terrain in {seed['district']}; GIS intersection is required.",
            'mitigation': 'Intersect the project boundary with Bhuvan, land-use and hazard layers.',
            'source_name': 'ISRO/NRSC Bhuvan',
            'source_url': 'https://bhuvan.nrsc.gov.in/',
        },
        {
            **common,
            'category': 'approvals',
            'title': 'Clearance dependency',
            'severity': 'MEDIUM',
            'impact_score': 36,
            'status': 'Not verified for this project',
            'description': 'Clearance status must be matched to the project authority reference; this record is not an official clearance result.',
            'mitigation': 'Match the project with PARIVESH proposal and approval identifiers.',
            'source_name': 'PARIVESH',
            'source_url': 'https://parivesh.nic.in/',
        },
    ]
    if seed['project_type'] in {'Highway', 'Expressway', 'Tunnel'}:
        barriers[1].update({
            'title': 'Corridor terrain and access constraint',
            'impact_score': 55,
            'description': 'Linear corridors can be affected by terrain, access roads, utilities and fragmented parcels; parcel GIS is required for confirmation.',
        })
    if seed['state'] in {'Uttarakhand', 'Jammu and Kashmir'}:
        barriers[0].update({'severity': 'HIGH', 'impact_score': 72, 'title': 'Mountain weather and slope exposure'})
        barriers[1].update({'severity': 'HIGH', 'impact_score': 78, 'title': 'Mountain terrain and slope constraint'})
    return barriers


def geocode_project(project_name, state):
    """Resolve a project name to a real coordinate pair using a public geocoding API."""
    query = f"{project_name}, {state}, India"
    url = "https://nominatim.openstreetmap.org/search"
    try:
        response = requests.get(
            url,
            params={
                "q": query,
                "format": "jsonv2",
                "limit": 1,
                "addressdetails": 1,
            },
            headers={"User-Agent": "SIH-Land-Acquisition-Demo/1.0"},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload:
            return None
        item = payload[0]
        return {
            "latitude": float(item.get("lat", 0.0)),
            "longitude": float(item.get("lon", 0.0)),
            "display_name": item.get("display_name"),
        }
    except Exception as exc:
        print(f"⚠ Geocoding fallback for '{project_name}': {exc}")
        return None


def build_real_project_records():
    """Build project records using real project names and public route geocoding."""
    records = []
    for seed in REAL_PROJECT_SEEDS:
        seed.setdefault("land_required_ha", None)
        seed.setdefault("affected_families", None)
        seed.setdefault("current_stage", "Public record")
        family_count = seed["affected_families"] or 0
        geocode = geocode_project(seed["project_name"], seed["state"]) or {
            "latitude": seed["latitude"],
            "longitude": seed["longitude"],
            "display_name": seed["project_name"],
        }

        records.append(
            {
                "project": {
                    "project_id": seed["project_id"],
                    "project_name": seed["project_name"],
                    "project_type": seed["project_type"],
                    "agency": seed["agency"],
                    "state": seed["state"],
                    "district": seed["district"],
                    "village": seed["village"],
                    "land_required_ha": seed["land_required_ha"],
                    "affected_families": seed["affected_families"],
                    "current_stage": seed["current_stage"],
                    "status": "Active",
                    "source_name": seed["source_name"],
                    "source_url": seed["source_url"],
                    "source_document_url": seed.get("source_document_url", seed["source_url"]),
                    "data_status": "Verified project identity and public source; analytical metrics require source-specific records",
                },
                "location": {
                    "latitude": geocode["latitude"],
                    "longitude": geocode["longitude"],
                    "location_source": f"{seed['source_name']} via public GIS lookup",
                    "accuracy_level": "project-level",
                },
                "acquisition": {
                    "current_stage": seed["current_stage"],
                    "notification_status": None,
                    "survey_status": None,
                    "award_status": None,
                    "possession_status": None,
                    "overall_progress_percentage": None,
                    "possession_percentage": None,
                    "days_in_current_stage": None,
                },
                "compensation": {
                    "total_compensation_amount": None,
                    "amount_disbursed": None,
                    "compensation_percentage": None,
                    "families_eligible": seed["affected_families"],
                    "families_paid": None,
                    "pending_cases": None,
                    "average_payment_delay_days": None,
                },
                "legal": {
                    "active_disputes": None,
                    "dispute_count": None,
                    "court_cases": None,
                    "legal_status": None,
                    "average_case_age_days": None,
                },
                "social_impact": {
                    "affected_families": seed["affected_families"],
                    "rehabilitation_progress_percentage": None,
                    "resettlement_progress_percentage": None,
                    "relocation_completed_percentage": None,
                    "grievances_pending": None,
                    "stakeholder_responsiveness": None,
                },
                "approvals": {
                    "environmental_approval_status": None,
                    "administrative_approval_status": None,
                    "financial_approval_status": None,
                    "other_approval_status": None,
                    "pending_approvals": None,
                    "average_approval_delay_days": None,
                },
                "prediction": {
                    "delay_probability": seed.get("base_delay_probability"),
                    "risk_level": seed.get("risk_level", "UNKNOWN"),
                    "risk_color": seed.get("risk_color", "GREY"),
                    "model_version": "public-seed-baseline" if seed.get("base_delay_probability") is not None else None,
                    "prediction_confidence": None,
                },
                "recommendations": [],
                "barriers": build_project_barriers(seed),
            }
        )

    return records

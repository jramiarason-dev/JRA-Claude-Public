"""
AuditIQ — Static reference data library.
All data is hardcoded; zero API calls required.
"""

# Keyword → internal theme key mapping (used by app.py topic detection)
TOPIC_THEME_MAP = {
    "AML": "AML_KYC", "KYC": "AML_KYC", "ANTI-MONEY": "AML_KYC",
    "TRANSACTION MONITORING": "AML_KYC", "MONEY LAUNDERING": "AML_KYC",
    "SANCTIONS": "AML_KYC", "CTF": "AML_KYC", "BENEFICIAL OWNER": "AML_KYC",
    "CYBER": "CYBER_RISK", "IT SECURITY": "CYBER_RISK", "INFORMATION SECURITY": "CYBER_RISK",
    "TECHNOLOGY RISK": "CYBER_RISK", "RANSOMWARE": "CYBER_RISK", "DORA": "CYBER_RISK",
    "CREDIT": "CREDIT_RISK", "LENDING": "CREDIT_RISK", "LOMBARD": "CREDIT_RISK",
    "COLLATERAL": "CREDIT_RISK", "PROVISIONING": "CREDIT_RISK",
    "OPERATIONAL RISK": "OPERATIONAL_RISK", "BUSINESS CONTINUITY": "OPERATIONAL_RISK",
    "BCP": "OPERATIONAL_RISK", "OUTSOURCING": "OPERATIONAL_RISK", "RCSA": "OPERATIONAL_RISK",
    "DATA PRIVACY": "DATA_PRIVACY", "GDPR": "DATA_PRIVACY", "NDSG": "DATA_PRIVACY",
    "PERSONAL DATA": "DATA_PRIVACY", "DATA PROTECTION": "DATA_PRIVACY",
    "MARKET RISK": "MARKET_RISK", "TRADING": "MARKET_RISK", "VAR": "MARKET_RISK",
    "IRRBB": "MARKET_RISK", "FRTB": "MARKET_RISK",
    "THIRD PARTY": "THIRD_PARTY_RISK", "VENDOR": "THIRD_PARTY_RISK",
    "THIRD-PARTY": "THIRD_PARTY_RISK", "SUPPLY CHAIN": "THIRD_PARTY_RISK",
    "GOVERNANCE": "GOVERNANCE", "INTERNAL CONTROLS": "GOVERNANCE",
    "THREE LINES": "GOVERNANCE", "BOARD": "GOVERNANCE", "SMCR": "GOVERNANCE",
}

# ═══════════════════════════════════════════════════════════════════════════════
# 1. REGULATORY_FRAMEWORKS
# ═══════════════════════════════════════════════════════════════════════════════

REGULATORY_FRAMEWORKS = {

    # ── CH / FINMA ─────────────────────────────────────────────────────────────
    "CH / FINMA": [
        {
            "reference": "FINMA-RS 2016/7",
            "title": "Video and Online Identification",
            "authority": "FINMA",
            "year": 2016,
            "scope": "All supervised financial institutions performing remote customer identification",
            "key_requirements": [
                "Live video connection with qualified staff must be used for identity verification",
                "Identity document must be inspected in real time; passive NFC chip reading required for biometric passports",
                "Full session must be recorded and stored for at least 10 years",
                "Verification must detect signs of manipulation or fraud in identity documents",
                "Process must comply with AMLA Article 3 and be documented in internal directives",
            ],
            "applies_to": ["AML", "KYC", "Digital Onboarding", "Operational Risk"],
        },
        {
            "reference": "FINMA-RS 2017/1",
            "title": "Corporate Governance — Banks",
            "authority": "FINMA",
            "year": 2017,
            "scope": "All banks and securities firms supervised by FINMA",
            "key_requirements": [
                "Board of Directors must include a majority of non-executive, independent members",
                "Audit Committee, Risk Committee, and Compensation Committee must be established",
                "CEO and Chairman roles must be separated; clear organisational rules required",
                "Board must approve risk tolerance, risk appetite, and overall strategy annually",
                "Conflicts of interest must be identified, disclosed, and managed through a formal policy",
            ],
            "applies_to": ["Governance", "Operational Risk", "Internal Controls"],
        },
        {
            "reference": "FINMA-RS 2008/21",
            "title": "Operational Risks — Banks",
            "authority": "FINMA",
            "year": 2008,
            "scope": "Banks subject to FINMA supervision; references Basel II/III operational risk framework. NOTE: Substantially superseded by FINMA-RS 2023/1 for ICT risk management, business continuity/resilience, and outsourcing. Residual applicability: operational loss data collection methodology and regulatory capital approach framework (BIA/TSA/AMA).",
            "key_requirements": [
                "Banks must maintain an operational risk management framework aligned with Basel II Pillar 2",
                "All material operational risk events must be captured in a loss database",
                "Risk and Control Self-Assessment (RCSA) must be performed at least annually",
                "Business continuity plans must be tested regularly and kept up to date",
                "Capital allocation for operational risk must use approved approach (BIA, TSA, or AMA)",
                "SUPERSEDED by FINMA-RS 2023/1 (effective 1 Jan 2024) for ICT risk, BCP, and outsourcing — audit engagements must reference FINMA-RS 2023/1 as primary standard for those areas",
            ],
            "applies_to": ["Operational Risk", "BCP", "Governance"],
        },
        {
            "reference": "FINMA-RS 2018/3",
            "title": "Outsourcing — Banks and Insurance",
            "authority": "FINMA",
            "year": 2018,
            "scope": "All banks and insurance companies outsourcing material functions",
            "key_requirements": [
                "Material outsourcing arrangements must be notified to FINMA and maintained in a register",
                "Outsourcing contracts must contain minimum clauses: audit rights, data security, business continuity",
                "Due diligence on service providers must be performed prior to engagement and periodically",
                "Sub-outsourcing of material functions requires prior approval and notification to the institution",
                "Exit strategies and contingency plans must be documented and tested",
            ],
            "applies_to": ["Third Party Risk", "Operational Risk", "Governance"],
        },
        {
            "reference": "FINMA-RS 2013/3",
            "title": "Auditing",
            "authority": "FINMA",
            "year": 2013,
            "scope": "All FINMA-supervised entities subject to audit obligations",
            "key_requirements": [
                "Audit firm must be licensed by FINMA and independent from the supervised entity",
                "Annual audit report must cover regulatory compliance, financial statements, and risk management",
                "Prudential audit (Aufsichtsprüfung) is risk-based; scope determined by FINMA risk category",
                "Audit committee must meet with external auditors without management at least once per year",
                "Deficiencies rated 1-4; Critical (1-2) must be reported to FINMA immediately",
            ],
            "applies_to": ["Governance", "Internal Controls", "Compliance"],
        },
        {
            "reference": "FINMA-RS 2011/1",
            "title": "Financial Intermediaries — Anti-Money Laundering",
            "authority": "FINMA",
            "year": 2011,
            "scope": "All banks and financial intermediaries subject to AMLA",
            "key_requirements": [
                "Customer due diligence (CDD) must be performed at onboarding; EDD required for high-risk clients",
                "Beneficial owner must be identified for all accounts; Form A or equivalent must be held",
                "PEP screening mandatory; foreign PEPs require mandatory EDD and senior management approval (FATF R.12); domestic PEPs require risk-based EDD — FINMA-RS 2011/1 is stricter than FATF baseline and requires senior management approval for all PEPs regardless of origin",
                "Transaction monitoring must detect unusual patterns; SAR must be filed with MROS promptly",
                "AML risk assessment must be reviewed annually; high-risk clients reviewed at least annually",
            ],
            "applies_to": ["AML", "KYC", "Compliance"],
        },
        {
            "reference": "FINMA-RS 2008/18",
            "title": "Mortgage Lending — Banks",
            "authority": "FINMA",
            "year": 2008,
            "scope": "All banks granting mortgage loans secured on Swiss residential and commercial real estate",
            "key_requirements": [
                "Maximum LTV of 80% for residential mortgages; borrowers must contribute at least 10% own funds not sourced from pledged pension assets",
                "Affordability test: debt service must be sustainable at a notional stress rate of 5%; income must cover principal, interest, and maintenance",
                "1st mortgage (up to 65% LTV) can be held indefinitely; 2nd mortgage (65-80% LTV) must be amortised to 65% within 15 years or by retirement",
                "Independent valuation of collateral required at origination; periodic revaluation for loans above materiality threshold",
                "FINMA may impose countercyclical capital buffer surcharges for banks with excessive residential mortgage concentration",
            ],
            "applies_to": ["Credit Risk", "Operational Risk", "Governance"],
        },
        {
            "reference": "FINMA-RS 2023/1",
            "title": "Operational Risks and Resilience",
            "authority": "FINMA",
            "year": 2023,
            "scope": "All FINMA-supervised banks and insurance companies; proportionate application based on systemic importance",
            "key_requirements": [
                "ICT risk management framework must be fully documented with defined roles, governance processes, and control objectives",
                "Critical service mapping required: banks must identify and document all services whose disruption would cause intolerable harm",
                "Board-approved impact tolerance definitions for each critical service (maximum tolerable disruption)",
                "Annual resilience testing of critical services under severe but plausible disruption scenarios",
                "FINMA incident reporting: material ICT incidents must be reported immediately upon discovery; follow-up report within 24 hours",
            ],
            "applies_to": ["Operational Risk", "Cyber Risk", "BCP", "Third Party Risk"],
        },
        {
            "reference": "FINMA-RS 2022/2",
            "title": "Liquidity Risks — Banks",
            "authority": "FINMA",
            "year": 2022,
            "scope": "All banks; specific requirements scaled to systemic importance",
            "key_requirements": [
                "LCR (Liquidity Coverage Ratio) must be maintained above 100% at all times; daily monitoring required",
                "NSFR (Net Stable Funding Ratio) must be reported monthly; compliance required from 2021",
                "Intraday liquidity monitoring must cover all material currencies and settlement systems",
                "Contingency Funding Plan (CFP) must define triggers, escalation procedures, and funding sources",
                "Liquidity stress tests must be run at minimum quarterly using FINMA-prescribed scenarios",
            ],
            "applies_to": ["Market Risk", "Operational Risk", "Treasury"],
        },
        {
            "reference": "nDSG 2023",
            "title": "Swiss Federal Act on Data Protection (revised nDSG)",
            "authority": "FDPIC",
            "year": 2023,
            "scope": "All organisations processing personal data of individuals in Switzerland",
            "key_requirements": [
                "Privacy by design and privacy by default must be implemented in all new processing systems",
                "Data subjects must be informed about processing at or before collection; layered notices accepted",
                "Data Protection Impact Assessments (DPIA) required for high-risk processing activities",
                "Appointment of a Data Protection Advisor (DPA) recommended; mandatory for federal bodies",
                "Data breaches must be reported to FDPIC without undue delay if likely to result in high risk",
            ],
            "applies_to": ["Data Privacy", "Compliance", "Cyber Risk"],
        },
        {
            "reference": "FinSA 2020",
            "title": "Financial Services Act (Finanzdienstleistungsgesetz)",
            "authority": "FINMA",
            "year": 2020,
            "scope": "All financial service providers and client advisers serving clients in Switzerland",
            "key_requirements": [
                "Client segmentation mandatory: private clients (full protection), professional clients (reduced), institutional clients (minimal) — classification must be documented and reviewable",
                "Suitability assessment required for investment advisory mandates; appropriateness test required for execution-only services involving complex instruments",
                "Key Information Document (KID/BIB) mandatory for all financial instruments sold to private clients; must disclose costs, risks, and expected returns",
                "Retrocession and inducement payments to third parties must be disclosed to clients; clients may waive entitlement in writing",
                "ESG preference assessment mandatory for all suitability determinations from January 2024; preference must be documented and reflected in recommendations",
            ],
            "applies_to": ["Investment Suitability", "Governance", "Compliance"],
        },
        {
            "reference": "FinIA 2020",
            "title": "Financial Institutions Act (Finanzinstitutsgesetz)",
            "authority": "FINMA",
            "year": 2020,
            "scope": "Portfolio managers, trustees, fund management companies, securities firms, and banks in Switzerland",
            "key_requirements": [
                "All independent portfolio managers and trustees must be authorised and supervised by FINMA or a recognised supervisory organisation (SO)",
                "Fit-and-proper requirements for management and qualified shareholders; minimum capital and professional indemnity insurance",
                "Prudential requirements including minimum capital (CHF 100,000 for portfolio managers), risk management, and internal controls",
                "Client asset segregation and safekeeping obligations equivalent to banking standards",
                "Annual reporting to supervisory organisation; FINMA retains ultimate enforcement authority",
            ],
            "applies_to": ["Governance", "Investment Suitability", "Compliance"],
        },
    ],

    # ── EU / DORA & others ─────────────────────────────────────────────────────
    "EU / DORA": [
        {
            "reference": "DORA (EU) 2022/2554",
            "title": "Digital Operational Resilience Act",
            "authority": "EBA / ESMA / EIOPA",
            "year": 2025,
            "scope": "Financial entities in the EU: banks, investment firms, payment institutions, crypto-asset service providers, ICT third-party providers",
            "key_requirements": [
                "ICT Risk Management Framework must be fully documented with roles, processes, and governance (Art. 5-16)",
                "Major ICT incidents must be reported to the competent authority: initial notification within 4 hours of classification as major; intermediate report within 72 hours; final report within 1 month (Art. 19-20). Classification criteria for 'major' incidents defined in ESA RTS. Note: the 24h 'significant incident' category belongs to NIS2, not DORA.",
                "Digital Operational Resilience Testing (TLPT) required at least every 3 years for significant firms (Art. 24-27)",
                "Register of contractual arrangements with all ICT third-party providers must be maintained and reported annually (Art. 28)",
                "Concentration risk for critical ICT providers must be assessed; exit strategies required (Art. 30-44)",
            ],
            "applies_to": ["Cyber Risk", "Operational Risk", "Third Party Risk", "BCP"],
        },
        {
            "reference": "GDPR Art. 32",
            "title": "GDPR — Security of Processing",
            "authority": "EDPB / National DPAs",
            "year": 2018,
            "scope": "All controllers and processors processing personal data of EU data subjects",
            "key_requirements": [
                "Appropriate technical and organisational measures must ensure security proportionate to risk",
                "Measures include: pseudonymisation and encryption; ongoing confidentiality, integrity, availability and resilience",
                "Ability to restore availability of personal data in a timely manner after a physical or technical incident",
                "Process for regularly testing, assessing and evaluating the effectiveness of security measures",
                "Processor may only engage sub-processors with prior specific or general written authorisation of the controller",
            ],
            "applies_to": ["Data Privacy", "Cyber Risk", "Operational Risk"],
        },
        {
            "reference": "EBA GL/2019/04",
            "title": "Guidelines on ICT and Security Risk Management",
            "authority": "EBA",
            "year": 2020,
            "scope": "Credit institutions, investment firms, payment institutions in the EU",
            "key_requirements": [
                "ICT and security risk must be integrated into the institution's overall risk management framework",
                "Asset management covering ICT assets (hardware, software, data, services) is mandatory",
                "Penetration testing and vulnerability scanning must be performed regularly",
                "ICT business continuity policy must include RPO, RTO, and critical function mapping",
                "Monitoring and logging of all ICT assets must be in place; anomalies must trigger alerts",
            ],
            "applies_to": ["Cyber Risk", "Operational Risk", "Third Party Risk"],
        },
        {
            "reference": "EBA GL/2022/02",
            "title": "Guidelines on AML/CFT",
            "authority": "EBA",
            "year": 2022,
            "scope": "Credit and financial institutions in the EU subject to AMLD",
            "key_requirements": [
                "Risk-based approach to AML/CFT must be embedded in governance and strategy",
                "Business-wide risk assessment must be updated at least every two years",
                "CDD measures must be applied at onboarding and throughout the relationship; SDD and EDD defined",
                "Transaction monitoring systems must be regularly reviewed and tuned to reduce false positives",
                "Training on AML/CFT must be provided to all relevant staff at onboarding and annually",
            ],
            "applies_to": ["AML", "KYC", "Compliance"],
        },
        {
            "reference": "AMLD6 2018/1673",
            "title": "6th Anti-Money Laundering Directive",
            "authority": "European Commission",
            "year": 2021,
            "scope": "All EU member states; obliged entities including financial institutions",
            "key_requirements": [
                "22 predicate offences for money laundering explicitly defined, including cyber crime and environmental crime",
                "Criminal liability for legal persons for money laundering offences",
                "Minimum 4-year imprisonment for natural persons convicted of money laundering",
                "Aiding, inciting, and attempting money laundering expressly criminalised",
                "Enhanced cooperation between FIUs and law enforcement across member states required",
            ],
            "applies_to": ["AML", "Compliance", "Governance"],
        },
        {
            "reference": "CRR III / CRD VI",
            "title": "Basel IV — Capital Requirements Regulation III / Directive VI",
            "authority": "EBA / ECB",
            "year": 2025,
            "scope": "Credit institutions and investment firms in the EU",
            "key_requirements": [
                "Output floor phase-in: 50% from 1 January 2025, rising in annual steps to 72.5% by 1 January 2030. Calculated as: floor RWA = max(internal model RWA, floor% × standardised approach RWA)",
                "Revised standardised approach for credit risk with more risk-sensitive risk weights",
                "Fundamental Review of the Trading Book (FRTB) replaces internal model for market risk capital",
                "New standardised approach for operational risk replaces all existing approaches (BIA, TSA, AMA)",
                "ESG risk must be incorporated into Pillar 2 assessments; climate stress testing mandatory",
            ],
            "applies_to": ["Credit Risk", "Market Risk", "Operational Risk", "Capital"],
        },
        {
            "reference": "MiCA (EU) 2023/1114",
            "title": "Markets in Crypto-Assets Regulation",
            "authority": "ESMA / EBA",
            "year": 2024,
            "scope": "Issuers of crypto-assets and crypto-asset service providers (CASPs) in the EU",
            "key_requirements": [
                "CASPs must be authorised by competent authority; passport regime for cross-border services",
                "AML/KYC requirements under AMLD apply fully to CASPs",
                "Issuers of asset-referenced tokens and e-money tokens subject to strict reserve and governance rules",
                "Whitepaper publication required before public offering of crypto-assets",
                "Market abuse provisions (insider trading, market manipulation) extended to crypto-asset markets",
            ],
            "applies_to": ["AML", "Compliance", "Cyber Risk", "Operational Risk"],
        },
    ],

    # ── UK / FCA+PRA ───────────────────────────────────────────────────────────
    "UK / FCA+PRA": [
        {
            "reference": "FCA SYSC",
            "title": "Senior Management Arrangements, Systems and Controls (SYSC)",
            "authority": "FCA",
            "year": 2016,
            "scope": "All FCA-authorised firms; enhanced requirements for SMCR in-scope firms",
            "key_requirements": [
                "Senior Management Functions (SMFs) must be clearly allocated; responsibilities maps and statements of responsibilities required",
                "Firms must take reasonable steps to ensure business is organised so it can be controlled effectively",
                "Compliance, risk management, and internal audit functions must be independent and adequately resourced",
                "Adequate systems and controls must be in place for record-keeping, financial crime prevention, and business continuity",
                "Board-approved Risk Appetite Statement must align with overall business strategy and capital adequacy",
            ],
            "applies_to": ["Governance", "Internal Controls", "Compliance", "Operational Risk"],
        },
        {
            "reference": "FCA Financial Crime Guide 2022",
            "title": "Financial Crime — A Guide for Firms (FCG)",
            "authority": "FCA",
            "year": 2022,
            "scope": "All FCA-authorised firms subject to financial crime obligations",
            "key_requirements": [
                "Firms must have effective systems and controls proportionate to the nature, scale and complexity of their activities",
                "Management information on financial crime must be reported to senior management and the Board regularly",
                "Customer risk assessment at onboarding must be documented; high-risk clients require EDD and sign-off",
                "Correspondent banking relationships require enhanced scrutiny; shell bank relationships are prohibited",
                "Sanctions screening must cover all clients, transactions, and counterparties in real time",
            ],
            "applies_to": ["AML", "KYC", "Compliance", "Sanctions"],
        },
        {
            "reference": "PRA SS2/21",
            "title": "Outsourcing and Third Party Risk Management",
            "authority": "PRA",
            "year": 2021,
            "scope": "PRA-authorised banks, building societies, and PRA-designated investment firms",
            "key_requirements": [
                "Firms must maintain a complete, up-to-date register of all material outsourcing arrangements",
                "Material outsourcing must be notified to PRA before implementation; significant changes require re-notification",
                "Contracts must include: audit rights, data protection, security standards, business continuity, exit provisions",
                "Concentration risk to single third parties must be identified, assessed, and managed",
                "Cloud and other technology outsourcing require specific risk assessment; shared responsibility model must be understood",
            ],
            "applies_to": ["Third Party Risk", "Operational Risk", "Cyber Risk"],
        },
        {
            "reference": "FCA PS21/3",
            "title": "Building Operational Resilience",
            "authority": "FCA / PRA / Bank of England",
            "year": 2021,
            "scope": "Banks, building societies, PRA-designated investment firms, enhanced-scope SMCR firms",
            "key_requirements": [
                "Important Business Services (IBS) must be identified and mapped with all dependencies",
                "Impact tolerances must be set for each IBS (maximum tolerable disruption in time/volume)",
                "Firms must be able to remain within impact tolerances by March 2025 (now enforced)",
                "Scenario testing against impact tolerances required at least annually; results to Board",
                "Self-assessment document must be maintained and provided to regulators on request",
            ],
            "applies_to": ["Operational Risk", "BCP", "Third Party Risk", "Cyber Risk"],
        },
        {
            "reference": "UK GDPR 2021",
            "title": "UK General Data Protection Regulation",
            "authority": "ICO",
            "year": 2021,
            "scope": "All organisations processing personal data of individuals in the UK post-Brexit",
            "key_requirements": [
                "Lawful basis must be established and documented for every personal data processing activity",
                "Personal data breaches must be reported to ICO within 72 hours if likely to result in risk to individuals",
                "Data Protection Officer (DPO) mandatory for banks and financial institutions as large-scale processors",
                "International data transfers require adequate protection: adequacy decisions, SCCs, or binding corporate rules",
                "Right to erasure, portability, and objection must be operationalised with defined response processes",
            ],
            "applies_to": ["Data Privacy", "Compliance", "Operational Risk"],
        },
    ],

    # ── SG / MAS ───────────────────────────────────────────────────────────────
    "SG / MAS": [
        {
            "reference": "MAS TRM 2021",
            "title": "Technology Risk Management Guidelines",
            "authority": "MAS",
            "year": 2021,
            "scope": "All MAS-regulated financial institutions",
            "key_requirements": [
                "Board and senior management must be accountable for technology risk; roles and responsibilities explicitly documented",
                "IT systems must achieve 99.95% availability for customer-facing critical systems; RTO must be defined",
                "Penetration testing must be conducted at least annually by qualified professionals; findings remediated promptly",
                "Cyber incident reporting to MAS: within 1 hour for significant incidents; root cause analysis within 14 days",
                "Third-party technology service providers must meet MAS security standards; contract terms must include audit rights",
            ],
            "applies_to": ["Cyber Risk", "Operational Risk", "Third Party Risk", "BCP"],
        },
        {
            "reference": "MAS Notice 626",
            "title": "Prevention of Money Laundering and Countering the Financing of Terrorism",
            "authority": "MAS",
            "year": 2021,
            "scope": "All banks in Singapore",
            "key_requirements": [
                "CDD must be performed at account opening and on existing customers on risk-sensitive basis",
                "EDD required for high-risk customers including PEPs, non-face-to-face, and correspondent banking",
                "Beneficial ownership must be identified for legal persons and legal arrangements",
                "Transaction monitoring must be in place; suspicious transactions to be reported to STRO",
                "Wire transfer rules require full originator and beneficiary information; SWIFT messaging compliance required",
            ],
            "applies_to": ["AML", "KYC", "Compliance", "Sanctions"],
        },
        {
            "reference": "MAS BCM 2012",
            "title": "Business Continuity Management Guidelines",
            "authority": "MAS",
            "year": 2012,
            "scope": "All MAS-regulated financial institutions",
            "key_requirements": [
                "BCM programme must be Board-approved and reviewed annually; BCM policy must be documented",
                "Business Impact Analysis (BIA) must identify critical functions, dependencies, and recovery priorities",
                "RTO for critical systems must not exceed 4 hours; RPO must be defined per system",
                "Crisis communication plan must identify spokespersons and escalation procedures to MAS",
                "BCP must be tested at least annually; results must be reported to senior management",
            ],
            "applies_to": ["Operational Risk", "BCP", "Third Party Risk"],
        },
        {
            "reference": "MAS CG 2018",
            "title": "Guidelines on Corporate Governance",
            "authority": "MAS",
            "year": 2018,
            "scope": "All locally incorporated banks and bank holding companies in Singapore",
            "key_requirements": [
                "Board must have independent directors comprising at least one-third of total membership",
                "Audit, Risk, Nominating, and Compensation Committees must be established with defined charters",
                "CEO and Chairman must be different individuals; separation of oversight and executive functions",
                "Remuneration framework must align with risk-adjusted performance; clawback provisions required",
                "Board must assess its own effectiveness annually; skills matrix to be disclosed in Annual Report",
            ],
            "applies_to": ["Governance", "Internal Controls"],
        },
        {
            "reference": "MAS Notice 655",
            "title": "Cyber Hygiene",
            "authority": "MAS",
            "year": 2019,
            "scope": "All MAS-regulated financial institutions",
            "key_requirements": [
                "Multi-factor authentication (MFA) is mandatory for all administrative access to critical systems",
                "Privileged access must be managed through a Privileged Access Management (PAM) solution",
                "Security patching must be applied within defined timelines: critical patches within 1 month",
                "Malware protection must be deployed on all endpoints and servers; signatures updated daily",
                "Network perimeter controls (firewalls, IDS/IPS) must segment the network and log all traffic",
            ],
            "applies_to": ["Cyber Risk", "Operational Risk"],
        },
    ],

    # ── HK / SFC+HKMA ─────────────────────────────────────────────────────────
    "HK / SFC+HKMA": [
        {
            "reference": "HKMA SPM TM-G-2",
            "title": "Supervisory Policy Manual — Business Continuity Planning",
            "authority": "HKMA",
            "year": 2019,
            "scope": "All authorised institutions in Hong Kong",
            "key_requirements": [
                "BCP must cover all critical business functions and be reviewed and updated at least annually",
                "Recovery Time Objectives (RTOs) for critical systems must be clearly defined and achievable",
                "Alternate site must be maintained; distance from primary site must ensure independence from same disaster",
                "BCP testing must include full failover tests; results and lessons learned reported to senior management",
                "BCP must address pandemic, cyberattack, prolonged power outage, and physical access denial scenarios",
            ],
            "applies_to": ["Operational Risk", "BCP", "Cyber Risk"],
        },
        {
            "reference": "HKMA AML/CFT Guideline 2023",
            "title": "Guideline on Anti-Money Laundering and Counter-Terrorist Financing",
            "authority": "HKMA",
            "year": 2023,
            "scope": "All banks, deposit-taking companies, and money service operators in Hong Kong",
            "key_requirements": [
                "Risk-based approach to CDD: simplified, standard, and enhanced due diligence tiers must be documented",
                "Beneficial ownership verification required for all corporate customers; UBO threshold is 25% ownership or control",
                "PEPs must be identified at onboarding and periodically; foreign PEPs require senior management approval",
                "Ongoing transaction monitoring system must be in place; STRs to be filed with JFIU within a reasonable time",
                "Correspondent banking: no relationships with shell banks; payable-through accounts require enhanced controls",
            ],
            "applies_to": ["AML", "KYC", "Compliance"],
        },
        {
            "reference": "HKMA CRAF",
            "title": "Cyber Resilience Assessment Framework",
            "authority": "HKMA",
            "year": 2021,
            "scope": "All HKMA-supervised authorised institutions",
            "key_requirements": [
                "Baseline security controls must be implemented across five domains: governance, identify, protect, detect, respond and recover",
                "Cyber risk appetite must be defined by Board and translated into measurable risk tolerances",
                "Threat intelligence sharing participation in HKMA-facilitated Cyber Intelligence Sharing Platform (CISP)",
                "Red team exercises (TIBER-HK equivalent) required for systemically important banks annually",
                "Cyber incident reporting to HKMA within 2 hours for material incidents; post-incident review within 14 days",
            ],
            "applies_to": ["Cyber Risk", "Operational Risk", "Governance"],
        },
        {
            "reference": "SFC AML Guidelines 2023",
            "title": "Guideline on Anti-Money Laundering and Counter-Terrorist Financing (for SFC licensees)",
            "authority": "SFC",
            "year": 2023,
            "scope": "Licensed corporations and registered institutions under the Securities and Futures Ordinance",
            "key_requirements": [
                "CDD must be performed before establishing a business relationship or conducting an occasional transaction",
                "Enhanced scrutiny required for high-risk clients, PEPs, and clients from high-risk jurisdictions (FATF grey/black lists)",
                "Screening against UN, OFAC, EU, and HK sanctions lists mandatory for all clients and transactions",
                "Suspicious transaction reports must be filed with JFIU; tipping-off prohibition applies",
                "Training for frontline staff and compliance officers on AML/CFT typologies and red flags, at least annually",
            ],
            "applies_to": ["AML", "KYC", "Compliance", "Sanctions"],
        },
        {
            "reference": "HKMA BCBS 239 Implementation",
            "title": "Risk Data Aggregation and Risk Reporting — BCBS 239 Implementation",
            "authority": "HKMA",
            "year": 2018,
            "scope": "Systemically important banks in Hong Kong",
            "key_requirements": [
                "Risk data must be accurate, complete, and generated in a timely manner (T+1 for most risk types)",
                "Single authoritative source for each risk data element; data lineage must be documented",
                "Risk reporting must cover all material risk types; reports must be adaptable and accurate under stress",
                "Board-level accountability for data quality; Chief Data Officer or equivalent role required",
                "IT infrastructure must support data aggregation capability without manual workarounds",
            ],
            "applies_to": ["Operational Risk", "Credit Risk", "Market Risk", "Data Governance"],
        },
    ],

    # ── Bahamas / SCB ──────────────────────────────────────────────────────────
    "Bahamas / SCB": [
        {
            "reference": "SCB AML Guidelines 2023",
            "title": "Guidelines for Licensees on the Prevention of Money Laundering and Countering the Financing of Terrorism",
            "authority": "Securities Commission of The Bahamas (SCB)",
            "year": 2023,
            "scope": "All SCB-registered financial and capital markets intermediaries",
            "key_requirements": [
                "AML/CFT compliance programme must be Board-approved; Compliance Officer must be designated",
                "CDD required at onboarding; EDD for PEPs, high-risk jurisdictions, and complex corporate structures",
                "Beneficial ownership must be verified for all legal entities; UBO threshold is 10% in the Bahamas",
                "Ongoing transaction monitoring must flag unusual patterns; SARs to be filed with the Financial Intelligence Unit (FIU)",
                "Training on AML/CFT must be provided annually and documented for all customer-facing and compliance staff",
            ],
            "applies_to": ["AML", "KYC", "Compliance"],
        },
        {
            "reference": "SCB CG Guidelines 2022",
            "title": "Guidelines for the Governance of SCB Licensees",
            "authority": "SCB",
            "year": 2022,
            "scope": "All capital markets licensees registered with the SCB",
            "key_requirements": [
                "Board must have at least two independent directors; all directors must meet fit-and-proper criteria",
                "Risk Management, Audit, and Compliance functions must be operationally independent from business lines",
                "Chief Executive Officer must be resident in The Bahamas or have adequate representation",
                "Annual compliance report must be submitted to SCB; material breaches to be reported promptly",
                "Conflicts of interest policy must be formally adopted; related-party transactions require Board approval",
            ],
            "applies_to": ["Governance", "Internal Controls", "Compliance"],
        },
        {
            "reference": "SCB Operational Risk Guidelines 2021",
            "title": "Guidelines on Operational Risk Management",
            "authority": "SCB",
            "year": 2021,
            "scope": "All SCB-licensed investment funds, broker-dealers, and fund administrators",
            "key_requirements": [
                "Operational risk management framework must identify, assess, monitor, and mitigate key operational risks",
                "Business continuity and disaster recovery plans must be documented, tested annually, and kept current",
                "Incident reporting: material operational events must be reported to SCB within 5 business days",
                "Outsourcing of core functions to non-Bahamas entities requires prior approval and notification to SCB",
                "Segregation of duties and four-eyes principle must be enforced for all material financial transactions",
            ],
            "applies_to": ["Operational Risk", "BCP", "Third Party Risk"],
        },
    ],

    # ── International: BCBS / FATF / FSB ──────────────────────────────────────
    "International": [
        {
            "reference": "BCBS 239 (2013)",
            "title": "Principles for Effective Risk Data Aggregation and Risk Reporting",
            "authority": "Basel Committee on Banking Supervision",
            "year": 2013,
            "scope": "Globally systemically important banks (G-SIBs); domestic SIBs on advisory basis",
            "key_requirements": [
                "Governance: Board and senior management must approve and oversee data aggregation framework",
                "Data architecture must support complete, accurate, and timely risk data aggregation across the group",
                "Risk reports must cover all material risk types; distributed to appropriate recipients in a timely manner",
                "Adaptability: risk reports must be producible at short notice; stress scenarios must be supportable",
                "Accuracy and integrity: automated feeds with manual reconciliation only as exception; data quality metrics required",
            ],
            "applies_to": ["Data Governance", "Operational Risk", "Credit Risk", "Market Risk"],
        },
        {
            "reference": "BCBS OpRisk (2021)",
            "title": "Principles for the Sound Management of Operational Risk",
            "authority": "Basel Committee on Banking Supervision",
            "year": 2021,
            "scope": "All internationally active banks",
            "key_requirements": [
                "Board must approve and periodically review operational risk appetite and tolerance statement",
                "Three Lines of Defence model must be implemented with clear roles and independence of internal audit",
                "RCSA, KRI, and loss data collection must form the core tools of the operational risk measurement process",
                "Internal capital allocation for operational risk must be reviewed under Internal Capital Adequacy Assessment Process",
                "Lessons learned from operational loss events must be documented and fed back into the risk framework",
            ],
            "applies_to": ["Operational Risk", "Governance", "Internal Controls"],
        },
        {
            "reference": "BCBS Cyber (2018)",
            "title": "Sound Practices: Implications of FinTech Developments for Banks and Bank Supervisors",
            "authority": "Basel Committee on Banking Supervision",
            "year": 2018,
            "scope": "All internationally active banks and their supervisors",
            "key_requirements": [
                "Governance of cyber risk must be aligned with overall risk governance; Board-level accountability required",
                "Cyber hygiene baseline must include: patch management, access management, encryption, and incident response",
                "Banks must assess cyber risk of third-party technology partners throughout the lifecycle",
                "Information sharing on cyber threats through ISACs and supervisory frameworks encouraged",
                "Recovery time capability must be validated through regular testing, not just planning documents",
            ],
            "applies_to": ["Cyber Risk", "Third Party Risk", "Operational Risk"],
        },
        {
            "reference": "FATF 40 Recommendations (2023 rev.)",
            "title": "FATF Recommendations — International Standards on Combating ML, TF and PF",
            "authority": "Financial Action Task Force",
            "year": 2023,
            "scope": "Global standard — applicable to all countries and financial institutions",
            "key_requirements": [
                "R.10: Customer due diligence — identification and verification of customers and beneficial owners",
                "R.12-13: Politically Exposed Persons — enhanced measures for foreign PEPs (mandatory EDD) and domestic PEPs (risk-based EDD); applies to family members and close associates",
                "R.14: Money or value transfer services (MVTS) — MVTS providers must be licensed and subject to AML/CFT measures",
                "R.15: New technologies — financial institutions must assess ML/TF risks from new products, services and technologies; VASPs (virtual asset service providers) subject to FATF standards",
                "R.16: Wire transfers / Travel Rule — full originator and beneficiary information must accompany transfers ≥USD/EUR 1,000",
                "R.20: Reporting of suspicious transactions — prompt filing with national FIU required; no tipping-off",
                "R.26-35: Regulation and supervision of financial institutions and designated non-financial businesses",
            ],
            "applies_to": ["AML", "KYC", "Compliance", "Sanctions"],
        },
        {
            "reference": "FATF Private Banking Guidance 2023",
            "title": "Guidance for a Risk-Based Approach to Private Banking",
            "authority": "Financial Action Task Force",
            "year": 2023,
            "scope": "Private banks, wealth managers, and family offices globally",
            "key_requirements": [
                "Private banks must apply EDD for all HNWI clients given inherent higher ML/TF risk profile",
                "Source of wealth and source of funds must be documented and verified, not merely declared",
                "Complex ownership structures (trusts, foundations, SPVs) require look-through to ultimate beneficial owner",
                "Relationship managers must be trained on red flags specific to private banking (offshore structures, unusual transfers)",
                "Annual review of all high-risk private banking relationships; senior management sign-off required",
            ],
            "applies_to": ["AML", "KYC", "Compliance"],
        },
        {
            "reference": "FSB Cyber Lexicon (2018)",
            "title": "FSB Cyber Lexicon",
            "authority": "Financial Stability Board",
            "year": 2018,
            "scope": "Financial supervisory and regulatory authorities globally; financial institutions",
            "key_requirements": [
                "Standardised terminology for cyber risk must be used in supervisory and regulatory communications",
                "49 defined terms covering: cyber incident, cyber risk, cyber hygiene, threat intelligence, resilience",
                "Lexicon applies to work on financial sector cyber resilience including incident response frameworks",
                "Baseline definitions support cross-border and cross-sector information sharing and coordination",
                "Regular review to ensure relevance as threat landscape and technology evolve",
            ],
            "applies_to": ["Cyber Risk", "Operational Risk"],
        },
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# 2. AUDIT_TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════════

AUDIT_TEMPLATES = {
    "AML / KYC & Transaction Monitoring": {
        "topic": "AML/KYC & Transaction Monitoring",
        "default_jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "All group entities across all booked jurisdictions. Focus on customer onboarding (CDD/EDD), "
            "beneficial ownership identification, PEP and sanctions screening, transaction monitoring system "
            "effectiveness, STR/SAR filing quality and timeliness, and periodic review of high-risk clients."
        ),
        "key_risks": ["R001", "R002", "R003", "R004", "R005", "R006", "R007", "R008"],
        "recommended_tests": ["T001", "T002", "T003", "T004", "T005"],
        "typical_findings": [
            "Incomplete beneficial ownership documentation for clients held through trust structures",
            "Transaction monitoring thresholds not calibrated to client risk profile — excessive false positives",
            "STR filing delays exceeding regulatory deadlines (>30 days from detection)",
            "Periodic review of high-risk clients overdue; backlog exceeds 20% of portfolio",
            "PEP identification relies on manual RMs rather than automated screening tool",
            "Source of wealth documentation for HNWI clients is insufficient or unverified",
            "Correspondent banking EDD files missing key due diligence documents",
        ],
        "rationale": (
            "AML/KYC remains the top enforcement priority for regulators across all five jurisdictions. "
            "Recent FATF mutual evaluations have flagged private banking as a high-risk channel for "
            "money laundering. FINMA imposed record fines in 2023 for AML failures at private banks. "
            "MAS and FCA have issued formal warnings to wealth managers regarding beneficial ownership gaps. "
            "The 2023 FATF guidance specifically targets private banking EDD requirements, making this "
            "a critical area for immediate review."
        ),
    },

    "Cyber Risk & IT Security": {
        "topic": "Cyber Risk & IT Security",
        "default_jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "IT infrastructure, cybersecurity controls framework, privileged access management, "
            "endpoint protection, network segmentation, patch management, SIEM/SOC effectiveness, "
            "third-party IT access, cloud security posture, and incident response capability."
        ),
        "key_risks": ["R009", "R010", "R011", "R012", "R013", "R014", "R015", "R016"],
        "recommended_tests": ["T011", "T012", "T013", "T014", "T015"],
        "typical_findings": [
            "Privileged access accounts not subject to periodic recertification; stale accounts exist",
            "Critical security patches applied beyond the 30-day policy deadline",
            "SIEM alerts not triaged within SLA; high-severity alerts left open >24 hours",
            "Third-party vendor access not revoked upon contract termination",
            "MFA not enforced for remote access to core banking systems",
            "No formal vulnerability management programme; last penetration test >18 months ago",
            "Incident response plan not tested in the past 12 months",
        ],
        "rationale": (
            "The financial sector faced a 64% increase in cyber attacks in 2023 (IBM X-Force). "
            "DORA entered into force in January 2025 with mandatory ICT risk management and incident "
            "reporting requirements. MAS Notice 655 (Cyber Hygiene) and HKMA CRAF impose prescriptive "
            "technical controls. Private banks are targeted for their HNWI client data and high-value "
            "transactions. Ransomware and supply chain attacks affecting financial IT vendors have "
            "increased materially, requiring immediate assessment of detection and response capabilities."
        ),
    },

    "Credit Risk & Lending": {
        "topic": "Credit Risk & Lending",
        "default_jurisdictions": ["CH / FINMA", "SG / MAS", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "Lombard lending portfolio, mortgage and real estate exposures, structured credit, "
            "credit underwriting standards, collateral valuation and management, covenant monitoring, "
            "credit concentration risk, impairment provisioning, and credit risk stress testing."
        ),
        "key_risks": ["R017", "R018", "R019", "R020", "R021"],
        "recommended_tests": ["T021", "T022", "T023", "T024", "T025"],
        "typical_findings": [
            "Lombard loan-to-value ratios exceed approved limits for concentrated single-name portfolios",
            "Collateral valuations not updated at required frequency; stale prices used for margin calculations",
            "Credit committee approval not obtained for exceptions; exception log not maintained",
            "Covenant breach waivers granted without formal documentation or escalation",
            "Credit concentration limits for single obligors or sectors not defined or monitored",
            "Stress testing scenarios do not include market crash scenarios for illiquid collateral",
            "Watch list review conducted less frequently than quarterly",
        ],
        "rationale": (
            "Rising interest rates in 2022-2024 have materially impacted Lombard lending portfolios "
            "at Swiss private banks, with margin call processes under stress. Real estate corrections "
            "in key markets (CH, UK, SG) affect collateral values. FINMA identified credit risk as a "
            "top supervisory priority for 2024, particularly for banks with concentrated real estate "
            "or single-name exposures. CRR III output floor implementation in 2025 increases capital "
            "requirements for banks using internal models, requiring reassessment of lending strategies."
        ),
    },

    "Operational Risk & Business Continuity": {
        "topic": "Operational Risk & Business Continuity",
        "default_jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "Operational risk framework (RCSA, KRI, incident reporting), business continuity and "
            "disaster recovery planning and testing, key person dependencies, outsourcing governance, "
            "change management controls, four-eyes principle application, and reconciliation processes."
        ),
        "key_risks": ["R022", "R023", "R024", "R025", "R026"],
        "recommended_tests": ["T031", "T032", "T033", "T034", "T035"],
        "typical_findings": [
            "RCSA methodology not consistently applied across business units; assessments lack independence",
            "KRIs not regularly reported to Risk Committee; thresholds not updated for current risk environment",
            "BCP has not been tested in the past 12 months; last test limited to tabletop exercise",
            "Key person dependencies identified but no succession plans or documented procedures",
            "Material outsourcing agreements not reviewed annually; no SLA monitoring in place",
            "IT change management process bypassed for emergency changes; no post-implementation review",
            "Reconciliation breaks aged >30 days not escalated to senior management",
        ],
        "rationale": (
            "DORA (Art. 5-16) mandates comprehensive ICT risk management and resilience testing by "
            "January 2025. FCA PS21/3 requires firms to demonstrate they can remain within operational "
            "impact tolerances. MAS BCM guidelines require full failover testing annually. The COVID-19 "
            "pandemic exposed key person and outsourcing risks that have not been fully remediated. "
            "Increasing reliance on cloud providers creates new concentration and exit risk concerns "
            "requiring Board-level attention."
        ),
    },

    "Data Privacy & GDPR/nDSG": {
        "topic": "Data Privacy & GDPR / nDSG",
        "default_jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "Client personal data processing activities, consent management, data retention and deletion, "
            "cross-border data transfer mechanisms, subject access request (SAR/DSAR) process, "
            "breach detection and notification, DPO role effectiveness, and DPIA process."
        ),
        "key_risks": ["R027", "R028", "R029", "R030"],
        "recommended_tests": ["T041", "T042", "T043", "T044", "T045"],
        "typical_findings": [
            "Records of processing activities (RoPA) incomplete or not maintained for all data processing",
            "No DPIA conducted for high-risk processing (automated profiling, large-scale monitoring)",
            "Cross-border data transfer to non-adequate countries relying on expired or unsigned SCCs",
            "DSAR response time exceeds 30-day statutory deadline due to manual, siloed processes",
            "Data retention schedules not operationalised; client data held beyond defined retention periods",
            "DPO role lacking independence; reporting line through Legal creates conflict of interest",
            "Breach log maintained but near-miss incidents not captured; reportability assessment not documented",
        ],
        "rationale": (
            "The revised Swiss nDSG entered into force in September 2023, introducing GDPR-equivalent "
            "obligations including DPIAs, privacy by design, and breach notification. The EU EDPB has "
            "issued fines totalling EUR 4.2bn under GDPR since 2018, including to several financial "
            "institutions. Cross-border data flows between CH, EU, and UK require specific legal mechanisms "
            "post-Brexit and post-Schrems II. Private banks processing HNWI data face heightened regulatory "
            "scrutiny given the sensitivity of wealth and lifestyle information held."
        ),
    },

    "Market Risk & Trading": {
        "topic": "Market Risk & Trading",
        "default_jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "Trading book and banking book market risk, VaR model methodology and backtesting, "
            "stress testing framework, market risk limit framework and breach management, "
            "independent price verification (IPV), P&L attribution, and front-office risk controls."
        ),
        "key_risks": ["R031", "R032", "R033"],
        "recommended_tests": ["T051", "T052", "T053", "T054", "T055"],
        "typical_findings": [
            "VaR model backtesting shows exceptions exceeding the 1% threshold; model review overdue",
            "Market risk limits for FX and interest rate risk not reviewed since 2022; no escalation process",
            "Independent price verification not performed for level 2/3 assets in the banking book",
            "Stress testing scenarios not updated to reflect current geopolitical and rate environment",
            "P&L explain breaks between risk systems and front-office system exceed materiality threshold",
            "Trading limit breaches resolved informally; no documented approval from Risk Committee",
            "FRTB impact assessment not completed ahead of 2025 implementation",
        ],
        "rationale": (
            "Market volatility in 2022-2024 — driven by rapid rate rises, geopolitical shocks, and "
            "FX dislocations — has tested market risk frameworks across private banks. FRTB implementation "
            "under CRR III/CRD VI from 2025 will materially change capital calculations for trading books. "
            "FINMA identified inadequate market risk stress testing at several private banks in 2023. "
            "The collapse of Credit Suisse highlighted weaknesses in market risk limit frameworks and "
            "escalation processes that are relevant across the sector."
        ),
    },

    "Third Party & Vendor Risk": {
        "topic": "Third Party & Vendor Risk",
        "default_jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "Critical and material outsourcing arrangements, cloud service providers, IT vendors, "
            "custodians, fund administrators, prime brokers, and other third parties. Focus on "
            "initial due diligence, ongoing oversight, contract adequacy, concentration risk, "
            "sub-outsourcing, and exit strategy."
        ),
        "key_risks": ["R034", "R035", "R036"],
        "recommended_tests": ["T061", "T062", "T063", "T064", "T065"],
        "typical_findings": [
            "Outsourcing register incomplete; non-material outsourcing threshold not defined or applied",
            "Due diligence files for critical vendors missing latest SOC 2 reports or security certifications",
            "Contracts with key IT vendors do not contain audit rights, data portability, or exit provisions",
            "Sub-outsourcing by critical vendors not identified, assessed, or approved",
            "No SLA monitoring in place; vendor performance not reviewed by relationship owner",
            "Concentration risk: >60% of core IT infrastructure hosted by single cloud provider",
            "Exit strategy for critical vendor not documented or tested; lock-in risk not quantified",
        ],
        "rationale": (
            "DORA Article 28 mandates a register of all ICT third-party arrangements, reported annually "
            "to regulators. PRA SS2/21 and FINMA-RS 2018/3 impose extensive requirements on outsourcing "
            "governance. The increasing adoption of cloud services at private banks (AWS, Azure, Google) "
            "creates new concentration risks. Several incidents in 2023 — including a major cloud provider "
            "outage affecting multiple financial institutions simultaneously — have highlighted the need "
            "for robust third-party risk management and tested exit strategies."
        ),
    },

    "Governance & Internal Controls": {
        "topic": "Governance & Internal Controls",
        "default_jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "suggested_scope": (
            "Board effectiveness and committee structure, three lines of defence implementation, "
            "risk appetite framework, policy framework completeness and review cycle, "
            "conflicts of interest management, remuneration framework, whistleblowing mechanism, "
            "and RCSA process."
        ),
        "key_risks": ["R037", "R038", "R039", "R040"],
        "recommended_tests": ["T071", "T072", "T073", "T074", "T075"],
        "typical_findings": [
            "Board Risk Committee does not receive sufficient granularity of risk reporting; MI is too high-level",
            "Risk Appetite Statement not cascaded to individual business unit limits and KRIs",
            "Internal Audit does not have direct reporting line to Audit Committee; independence compromised",
            "Policy review cycle not adhered to; 30% of policies overdue for annual review",
            "Conflicts of interest register not maintained; RM personal account dealing policy not enforced",
            "Whistleblowing channel not sufficiently publicised; number of reports is statistically low",
            "Three Lines of Defence model poorly understood; 2LOD and 3LOD performing overlapping controls",
        ],
        "rationale": (
            "Regulatory scrutiny of governance at private banks has intensified following the Credit Suisse "
            "collapse, which highlighted board-level failures in risk oversight and escalation. FINMA-RS 2017/1 "
            "and MAS CG 2018 require robust board committee structures. FCA's Senior Managers & Certification "
            "Regime (SMCR) places personal accountability on senior managers for governance failures. "
            "The IIA's revised Global Internal Audit Standards (2024) increase expectations on independence, "
            "risk-based planning, and quality assurance, making a governance audit timely and necessary."
        ),
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# 3. RISK_INDICATORS
# ═══════════════════════════════════════════════════════════════════════════════

RISK_INDICATORS = {

    # ── AML / KYC ──────────────────────────────────────────────────────────────
    "AML_KYC": [
        {
            "id": "R001",
            "title": "Inadequate Beneficial Ownership Identification",
            "description": (
                "Failure to identify and verify the ultimate beneficial owner (UBO) of clients held through "
                "complex corporate structures — trusts, foundations, SPVs, nominee arrangements — resulting "
                "in the bank unknowingly maintaining relationships with sanctioned individuals or proceeds of crime."
            ),
            "level": "Critical",
            "probability": "High",
            "impact": "High",
            "expected_controls": [
                "Automated UBO look-through tool integrated with onboarding platform",
                "Mandatory legal opinion for structures exceeding two layers",
                "Annual re-verification of UBO for high-risk clients",
                "Register of beneficial owners maintained and accessible to compliance",
                "Training for relationship managers on complex structure red flags",
            ],
            "red_flags": [
                "Client refuses to disclose ultimate beneficial owner",
                "Ownership chain involves jurisdictions with no public UBO registers",
                "Nominee shareholders or directors with no apparent economic rationale",
                "Frequent changes to ownership structure without clear business reason",
                "UBO is a PEP discovered post-onboarding",
            ],
            "private_banking_specifics": (
                "HNWI clients routinely use trusts, foundations, and holding companies for legitimate "
                "estate planning. The complexity of these structures — often spanning multiple jurisdictions "
                "including offshore centres (Cayman, BVI, Bahamas) — makes UBO identification significantly "
                "harder and creates elevated ML risk. Private bankers may face pressure from senior clients "
                "to accept opaque structures without adequate due diligence."
            ),
        },
        {
            "id": "R002",
            "title": "Ineffective Transaction Monitoring",
            "description": (
                "Transaction monitoring system fails to detect suspicious activity due to poorly calibrated "
                "rules, excessive false-positive rates leading to alert fatigue, or inadequate coverage of "
                "specific transaction types (e.g. foreign exchange, securities transfers, cash equivalents)."
            ),
            "level": "Critical",
            "probability": "High",
            "impact": "High",
            "expected_controls": [
                "Risk-based alert thresholds calibrated to client profile and jurisdiction",
                "Annual model tuning and back-testing against known suspicious transactions",
                "Dedicated AML investigations team with SLA for alert clearance",
                "Escalation path to MLRO for unresolved or high-risk alerts",
                "Coverage testing to confirm all transaction types are monitored",
            ],
            "red_flags": [
                "False-positive rate exceeding 95% — possible indicator of over-broad rules that are then ignored",
                "Alerts being cleared in seconds without documented rationale",
                "Transaction types (FX, securities) excluded from monitoring scope",
                "No review of alert disposition for quality assurance",
                "STR count is nil or statistically low relative to client base",
            ],
            "private_banking_specifics": (
                "Private banking transactions often involve large, infrequent transfers that differ from "
                "retail banking patterns. Standard rule sets designed for high-volume retail accounts may "
                "generate excessive false positives for HNWI clients while missing genuine red flags in "
                "private banking transactions such as structuring across multiple custodians or jurisdictions."
            ),
        },
        {
            "id": "R003",
            "title": "PEP Screening Gaps",
            "description": (
                "Politically exposed persons (PEPs), their family members, or close associates are not "
                "identified at onboarding or during the relationship, resulting in enhanced due diligence "
                "not being applied and mandatory senior management approval being bypassed."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Automated PEP screening at onboarding against commercially maintained databases",
                "Ongoing screening triggered by database updates and periodic reviews",
                "Explicit definition of domestic vs. foreign PEP and close associate in internal policy",
                "Senior management sign-off documented for all PEP relationships",
                "Enhanced periodic review cycle (at minimum annual) for all PEP clients",
            ],
            "red_flags": [
                "Relationship manager bypasses screening by manually classifying client as non-PEP",
                "PEP database last updated more than 6 months ago",
                "No documented senior management approval for identified PEPs",
                "PEP review cycle exceeds 12 months",
                "Close associates and family members not screened alongside primary PEP",
            ],
            "private_banking_specifics": (
                "Private banking is a primary channel for PEP clients seeking wealth management services. "
                "The reputational and regulatory risk of maintaining undisclosed PEP relationships is severe "
                "and has been the basis for major enforcement actions against Swiss private banks (e.g. "
                "Banca Privada d'Andorra, BSI Singapore). Domestic PEPs — often business contacts of "
                "senior relationship managers — present a particularly challenging identification risk."
            ),
        },
        {
            "id": "R004",
            "title": "Inadequate Source of Wealth Documentation",
            "description": (
                "Failure to obtain, verify, and document the source of wealth (SoW) and source of funds "
                "(SoF) for high-risk clients — particularly at onboarding and during periodic review — "
                "leaving the bank unable to demonstrate that client wealth has a legitimate origin."
            ),
            "level": "Critical",
            "probability": "High",
            "impact": "High",
            "expected_controls": [
                "Mandatory SoW documentation checklist for all high-risk and HNWI clients",
                "Independent verification of declared SoW against third-party sources where possible",
                "SoW adequacy reviewed by compliance and documented prior to account opening",
                "Periodic re-assessment of SoW for relationship growth or material asset changes",
                "MLRO sign-off required where SoW cannot be fully verified",
            ],
            "red_flags": [
                "Client wealth described only as 'business income' without supporting documentation",
                "Declared SoW inconsistent with client's background or professional profile",
                "Sudden material increase in assets without credible explanation",
                "Transfers received from jurisdictions inconsistent with declared SoW",
                "Client unwilling to provide supporting documentation for wealth origin",
            ],
            "private_banking_specifics": (
                "SoW documentation is arguably the most operationally challenging AML control in private "
                "banking. HNWI clients may have accumulated wealth through multiple legitimate sources "
                "over decades (business sales, inheritances, dividends, real estate) that are difficult "
                "to document comprehensively. FATF's 2023 private banking guidance specifically requires "
                "proportionate verification — not just declaration — of SoW."
            ),
        },
        {
            "id": "R005",
            "title": "Delayed or Inadequate STR Filing",
            "description": (
                "Suspicious Transaction Reports (STRs) or Suspicious Activity Reports (SARs) are filed late, "
                "with insufficient detail, or not filed at all due to inadequate investigation procedures, "
                "tipping-off risk mismanagement, or insufficient training of relationship managers."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Documented escalation process from RM to MLRO with defined timelines",
                "MLRO decision within 5 business days of referral; filing within regulatory deadline",
                "Quality review of STR/SAR content by compliance before submission",
                "Tipping-off training for all staff with client interaction",
                "Annual review of STR/SAR statistics against peer benchmarks",
            ],
            "red_flags": [
                "STR/SAR count disproportionately low relative to AUM or number of transactions",
                "Average time from alert to MLRO decision exceeds 30 days",
                "MLRO role vacant or filled by person with insufficient authority or training",
                "No written policy on internal escalation and STR/SAR filing process",
                "STR/SAR filed only after regulatory enquiry rather than proactively",
            ],
            "private_banking_specifics": (
                "Relationship managers at private banks face cultural pressure to protect long-standing "
                "client relationships, which can create reluctance to escalate concerns or file STRs. "
                "The tipping-off risk — whereby alerting a client to an investigation is itself an offence — "
                "must be actively managed during periodic reviews where a suspicious client might infer "
                "that enhanced scrutiny has been applied."
            ),
        },
        {
            "id": "R006",
            "title": "Correspondent Banking Compliance Failures",
            "description": (
                "Inadequate due diligence on correspondent banking relationships allowing access to the "
                "financial system for respondent banks that have weaker AML controls, shell bank connections, "
                "or are domiciled in high-risk jurisdictions."
            ),
            "level": "High",
            "probability": "Low",
            "impact": "High",
            "expected_controls": [
                "Written assessment of respondent bank's AML framework before establishing relationship",
                "Annual review of correspondent relationships against FATF grey/black lists",
                "Prohibition on relationships with shell banks documented in policy",
                "Payable-through accounts subject to enhanced controls and RM sign-off",
                "Senior management approval required for high-risk correspondent relationships",
            ],
            "red_flags": [
                "Respondent bank domiciled in FATF grey or black-listed jurisdiction",
                "Respondent bank has no physical presence in jurisdiction of incorporation",
                "Ownership of respondent bank is opaque or held through bearer shares",
                "Respondent bank has recent regulatory sanctions or AML enforcement action",
                "Volume or nature of transactions through correspondent account inconsistent with expected activity",
            ],
            "private_banking_specifics": (
                "Swiss private banks often maintain correspondent relationships with smaller regional "
                "and offshore banks to facilitate HNWI transactions in multiple jurisdictions. These "
                "relationships can create indirect exposure to higher-risk jurisdictions and clients "
                "that the private bank would not onboard directly. Nostro/vostro reconciliation "
                "quality is a proxy for the robustness of correspondent oversight."
            ),
        },
        {
            "id": "R007",
            "title": "Sanctions Screening Failures",
            "description": (
                "Failure to screen clients, counterparties, and transactions in real time against applicable "
                "sanctions lists (UN, OFAC, EU, SECO, OFSI), resulting in prohibited transactions being "
                "processed or assets held for sanctioned persons or entities."
            ),
            "level": "Critical",
            "probability": "Low",
            "impact": "High",
            "level_rationale": "Elevated to Critical despite Low probability: sanctions violations carry strict-liability criminal exposure, irreversible reputational harm, and correspondent banking exclusion risk that make the consequence category qualitatively different from standard High-impact events.",
            "expected_controls": [
                "Automated real-time screening of all transactions against current OFAC, UN, EU, SECO lists",
                "Daily update cycle for sanctions lists; immediate update for emergency designations",
                "Fuzzy matching logic to detect name variations, transliterations, and aliases",
                "Hits investigated and escalated within 4 hours; assets frozen pending legal review",
                "Annual testing of screening system effectiveness against known sanctions hits",
            ],
            "red_flags": [
                "Screening database not updated within 24 hours of new designations",
                "Exact-match-only screening — no fuzzy logic — creates evasion risk",
                "No screening of counterparties to client transactions (e.g. beneficiaries of wire transfers)",
                "Sanctions hits cleared by operations without compliance review",
                "No process for handling complex ownership structures with sanctioned UBOs",
            ],
            "private_banking_specifics": (
                "The Russia-Ukraine conflict and resulting OFAC/EU sanctions packages from 2022 have "
                "created acute compliance challenges for private banks with Russian HNWI clients. "
                "Indirect exposure through nominee structures and intermediate holding companies "
                "makes beneficial ownership screening critical. SECO enforcement in Switzerland "
                "has increased materially since 2022."
            ),
        },
        {
            "id": "R008",
            "title": "Periodic Review Backlogs",
            "description": (
                "Annual or periodic review of existing client relationships not completed on schedule, "
                "resulting in outdated KYC files, undetected changes in client risk profile, and "
                "failure to apply EDD to clients whose risk classification has changed."
            ),
            "level": "High",
            "probability": "High",
            "impact": "Medium",
            "expected_controls": [
                "Automated CRM workflow triggering reviews at defined intervals based on risk rating",
                "Compliance dashboard showing overdue reviews by relationship manager and team",
                "Escalation to Head of Compliance and Business Line Head for reviews overdue >60 days",
                "New business freeze for relationship managers with >20% overdue review rate",
                "Quality sampling of completed reviews by compliance at minimum quarterly",
            ],
            "red_flags": [
                "Percentage of overdue reviews exceeds 15% of portfolio",
                "High-risk clients reviewed less frequently than annually",
                "Review process consists of RM self-certification without compliance oversight",
                "KYC files not updated despite material events (change of address, new UBO, PEP classification)",
                "IT system does not generate automated reminders for upcoming review dates",
            ],
            "private_banking_specifics": (
                "Revenue pressure in private banking leads relationship managers to deprioritise "
                "periodic reviews for large, long-standing clients. The risk is compounded when "
                "client risk ratings are not updated following changes in circumstance — such as "
                "a client's country becoming subject to FATF greylisting or a PEP classification "
                "arising from a family member entering public office."
            ),
        },
    ],

    # ── CYBER RISK ─────────────────────────────────────────────────────────────
    "CYBER_RISK": [
        {
            "id": "R009",
            "title": "Privileged Access Compromise",
            "description": (
                "Compromise of privileged accounts (domain admin, root, DBA, application admin) "
                "enabling an attacker to exfiltrate data, manipulate financial records, disable "
                "security controls, or deploy ransomware across the entire IT environment."
            ),
            "level": "Critical",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Privileged Access Management (PAM) solution for all privileged accounts (CyberArk, BeyondTrust)",
                "Just-in-time (JIT) access for privileged operations — no standing privileged access",
                "All privileged sessions recorded and reviewed on risk-based basis",
                "Multi-factor authentication mandatory for all privileged access",
                "Quarterly access recertification; immediate revocation on role change",
            ],
            "red_flags": [
                "Privileged accounts with passwords that have not been rotated in >90 days",
                "Shared service accounts used for privileged access — no individual accountability",
                "Privileged access granted without a formal request and approval workflow",
                "No monitoring or alerting on privileged account activity outside business hours",
                "Privileged accounts belonging to departed staff still active in directory",
            ],
            "private_banking_specifics": (
                "Core banking systems holding HNWI account data and transaction history represent "
                "a premium target. Privileged access to these systems — often held by IT operations, "
                "DBA teams, and external vendors — is frequently inadequately controlled in smaller "
                "private banks that lack the resources of larger institutions. A single compromised "
                "DBA account could expose the entire client database."
            ),
        },
        {
            "id": "R010",
            "title": "Unpatched Critical Vulnerabilities",
            "description": (
                "Critical and high-severity vulnerabilities remain unpatched beyond defined SLAs, "
                "providing attackers with known exploitation vectors to gain initial access to "
                "banking systems, escalate privileges, or move laterally across the network."
            ),
            "level": "Critical",
            "probability": "High",
            "impact": "High",
            "expected_controls": [
                "Vulnerability management programme with defined SLAs: critical patches within 15 days, high within 30",
                "Automated scanning of all endpoints, servers, and network devices at minimum weekly",
                "Risk acceptance process for patches that cannot be applied immediately — compensating controls required",
                "Vendor patch notification subscriptions for all critical systems",
                "Monthly patch compliance report to CISO and Risk Committee",
            ],
            "red_flags": [
                "Patch compliance rate below 90% for critical and high-severity vulnerabilities",
                "End-of-life operating systems or applications in production without compensating controls",
                "No vulnerability scanning for externally facing systems",
                "Patch exceptions without documented compensating controls or defined remediation date",
                "IT team not subscribed to vendor security advisories",
            ],
            "private_banking_specifics": (
                "Legacy core banking systems (some running decades-old code) are notoriously difficult "
                "to patch without extensive regression testing and planned downtime — windows that may "
                "be unavailable for systems running 24/7. Private banks with outsourced IT face "
                "dependency on vendor patch timelines that may not align with regulatory expectations."
            ),
        },
        {
            "id": "R011",
            "title": "Inadequate Security Incident Detection",
            "description": (
                "Absence or ineffectiveness of Security Information and Event Management (SIEM) "
                "and Security Operations Centre (SOC) capabilities results in attacks going "
                "undetected for extended periods, materially increasing breach impact."
            ),
            "level": "Critical",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "24/7 SIEM monitoring with alert correlation rules aligned to MITRE ATT&CK framework",
                "Defined detection use cases reviewed and updated quarterly",
                "Mean Time To Detect (MTTD) and Mean Time To Respond (MTTR) tracked as KRIs",
                "SOC escalation playbooks for all Tier 1-3 alert categories",
                "Annual purple team exercise to validate detection coverage",
            ],
            "red_flags": [
                "SIEM deployed but alerts not reviewed within defined SLA",
                "Log coverage below 90% — critical systems not sending logs to SIEM",
                "No detection use cases for lateral movement or data exfiltration",
                "SOC team understaffed; alerts only reviewed during business hours",
                "MTTD exceeds 30 days — indicative of undetected dwell time",
            ],
            "private_banking_specifics": (
                "Many private banks rely on managed security service providers (MSSPs) for SOC "
                "capabilities, creating dependency on third-party detection effectiveness. MAS TRM "
                "2021 requires cyber incident reporting within 1 hour — unachievable without real-time "
                "detection. DORA mandates that ICT-related incidents be reported within 4 hours, "
                "requiring automated detection and escalation pipelines."
            ),
        },
        {
            "id": "R012",
            "title": "Third-Party and Vendor Cyber Access Risk",
            "description": (
                "Third-party suppliers and IT vendors with direct or remote access to banking systems "
                "represent an unmonitored attack surface. Compromise of a vendor's credentials or systems "
                "can provide attackers with direct access to the bank's infrastructure."
            ),
            "level": "High",
            "probability": "High",
            "impact": "High",
            "expected_controls": [
                "Vendor access managed via privileged remote access solution with session recording",
                "Time-limited access grants with automatic expiry; no standing vendor access",
                "Vendor security questionnaire and SOC 2 Type II review before access granted",
                "All vendor sessions conducted in isolated network segment — no direct production access",
                "Access immediately revoked upon contract termination; offboarding checklist mandatory",
            ],
            "red_flags": [
                "Vendors accessing production systems via shared credentials",
                "No formal offboarding process — departed vendors still have valid credentials",
                "Vendor access not logged or monitored",
                "Vendor bypasses PAM solution — connects directly via RDP or VPN",
                "No contractual requirement for vendors to report security incidents",
            ],
            "private_banking_specifics": (
                "Private banks often engage multiple external service providers — core banking vendors, "
                "custody platforms, portfolio management systems, regulatory reporting tools — each "
                "requiring access to sensitive client data. The SolarWinds and MOVEit supply chain "
                "attacks demonstrated how a single vendor compromise can cascade across hundreds of "
                "financial institutions simultaneously."
            ),
        },
        {
            "id": "R013",
            "title": "Business Email Compromise and Social Engineering",
            "description": (
                "Fraudulent emails impersonating senior executives, clients, or counterparties deceive "
                "staff into authorising fraudulent wire transfers, disclosing credentials, or granting "
                "unauthorised access — resulting in direct financial loss or data breach."
            ),
            "level": "High",
            "probability": "High",
            "impact": "High",
            "expected_controls": [
                "Email authentication protocols: SPF, DKIM, and DMARC configured and monitored",
                "Dual authorisation required for all wire transfers above defined threshold",
                "Call-back verification to known number for change-of-beneficiary instructions",
                "Regular phishing simulation exercises with mandatory remediation training",
                "SWIFT CSP controls including authenticated communication for payment instructions",
            ],
            "red_flags": [
                "DMARC policy set to 'p=none' — no enforcement of email authentication",
                "Single authorisation for wire transfers — no second approver required",
                "Change of payment instructions accepted via email without call-back verification",
                "Phishing simulation click rate exceeding 20% after training",
                "No process to flag emails with external sender spoofing internal domains",
            ],
            "private_banking_specifics": (
                "Relationship managers handle high-value payment instructions from HNWI clients "
                "by email and phone, creating a prime target for BEC fraud. Fraudsters impersonate "
                "clients and request urgent fund transfers, exploiting the high-trust personal "
                "relationships in private banking. The average loss per BEC incident in wealth "
                "management exceeds USD 120,000 (FBI IC3 2023)."
            ),
        },
        {
            "id": "R014",
            "title": "Ransomware Attack",
            "description": (
                "Ransomware deployed across banking infrastructure encrypts critical systems and data, "
                "causing operational disruption, potential data exfiltration, reputational damage, "
                "and regulatory breach — with recovery times measured in days to weeks."
            ),
            "level": "Critical",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Immutable offline backups for all critical systems; restoration tested quarterly",
                "Network segmentation preventing lateral movement from user endpoints to core systems",
                "Email and web gateway filtering blocking known ransomware delivery mechanisms",
                "Endpoint Detection and Response (EDR) with behavioural analysis on all endpoints",
                "Ransomware incident response playbook including FCA/FINMA/MAS notification requirements",
            ],
            "red_flags": [
                "Backups stored on network accessible from production — susceptible to encryption",
                "Backup restoration never tested; RTO/RPO not validated",
                "Flat network architecture — no segmentation between user devices and server environment",
                "No EDR deployed; reliance on signature-based antivirus only",
                "Incident response plan does not include regulatory notification timelines",
            ],
            "private_banking_specifics": (
                "A successful ransomware attack encrypting core banking systems would prevent the bank "
                "from accessing client records, processing transactions, or generating regulatory "
                "reports. For private banks serving HNWI clients, the reputational damage of a "
                "disclosed attack can result in immediate client attrition. DORA's 4-hour reporting "
                "window means incident response readiness is a regulatory requirement."
            ),
        },
        {
            "id": "R015",
            "title": "Cloud Security Misconfiguration",
            "description": (
                "Misconfigured cloud services (AWS S3, Azure Blob, Google Cloud Storage) expose "
                "client data, system credentials, or application code to the public internet, "
                "enabling data exfiltration without exploitation of any vulnerability."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Cloud Security Posture Management (CSPM) tool scanning all cloud resources continuously",
                "Infrastructure-as-code templates with mandatory security guardrails prevent misconfiguration at deployment",
                "Least-privilege IAM policies for all cloud service accounts and applications",
                "Data Loss Prevention (DLP) controls on cloud storage buckets containing client data",
                "Monthly cloud security review against CIS Benchmarks or NIST CSF",
            ],
            "red_flags": [
                "Public-facing cloud storage buckets without access logging enabled",
                "Cloud IAM roles with wildcard permissions (*:*) in production",
                "No CSPM tool deployed; security posture assessed manually or ad hoc",
                "Cloud accounts not included in vulnerability scanning scope",
                "Shadow IT: business lines provisioning cloud services without IT security review",
            ],
            "private_banking_specifics": (
                "Private banks migrating to cloud platforms for CRM, document management, or portfolio "
                "analytics risk inadvertently exposing HNWI client data through misconfiguration. "
                "The GDPR/nDSG obligation to maintain confidentiality and integrity of personal data "
                "applies equally to cloud-hosted data. A misconfigured client database exposed on "
                "the public internet would constitute a reportable data breach."
            ),
        },
        {
            "id": "R016",
            "title": "SWIFT and Payment Infrastructure Fraud",
            "description": (
                "Fraudulent SWIFT messages or payment instructions — enabled by compromised operator "
                "credentials, inadequate segregation of duties, or manipulation of payment files — "
                "result in unauthorised transfers of significant sums from correspondent accounts."
            ),
            "level": "Critical",
            "probability": "Low",
            "impact": "High",
            "level_rationale": "Elevated to Critical despite Low probability: losses are typically immediate and irreversible (e.g. Bangladesh Bank USD 81M theft); SWIFT CSP non-compliance directly attracts regulatory sanction; sector-wide SWIFT attack campaigns demonstrate that any single failure becomes systemic.",
            "expected_controls": [
                "Full implementation of SWIFT Customer Security Programme (CSP) mandatory controls",
                "Four-eyes authorisation for all SWIFT messages above defined threshold",
                "Real-time monitoring of all outgoing SWIFT messages for anomalies",
                "Segregation of duties: payment input, authorisation, and release by different staff",
                "Daily reconciliation of nostro accounts; same-day investigation of unreconciled items",
            ],
            "red_flags": [
                "SWIFT CSP self-attestation score below mandatory control threshold",
                "Single operator can create and send SWIFT messages without second authorisation",
                "No real-time monitoring of SWIFT message volume or value patterns",
                "Operator workstations used for both SWIFT access and internet browsing",
                "SWIFT interface not segregated from general IT network",
            ],
            "private_banking_specifics": (
                "The 2016 Bangladesh Bank SWIFT heist ($81m) and subsequent attacks on regional "
                "banks demonstrated the catastrophic impact of SWIFT fraud. Private banks processing "
                "large HNWI cross-border transfers are attractive targets. SWIFT CSP compliance "
                "is mandatory; non-compliance is reported to counterparties who may suspend "
                "correspondent relationships."
            ),
        },
    ],

    # ── CREDIT RISK ────────────────────────────────────────────────────────────
    "CREDIT_RISK": [
        {
            "id": "R017",
            "title": "Lombard Lending Over-Concentration",
            "description": (
                "Excessive Lombard loan exposure concentrated in a single security, issuer, sector, "
                "or client, such that a market correction in that concentration triggers simultaneous "
                "margin calls that cannot be met, resulting in forced liquidation at distressed prices "
                "and material credit losses."
            ),
            "level": "Critical",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Single-name and sector concentration limits in the Lombard loan policy",
                "Eligible collateral list with approved LTV ratios for each asset class",
                "Daily portfolio monitoring with automated concentration alerts",
                "Stress testing of Lombard portfolio under severe market scenarios (equity -40%, FX ±20%)",
                "Senior credit officer approval for exposures exceeding concentration limits",
            ],
            "red_flags": [
                "Single issuer represents >20% of collateral portfolio for a client",
                "Lombard portfolio not stress-tested in the past 12 months",
                "Margin call process not documented or tested",
                "Illiquid or unlisted securities accepted as collateral at face value",
                "No formal eligible collateral list — relationship manager determines acceptable collateral",
            ],
            "private_banking_specifics": (
                "Lombard lending is a core product for Swiss private banks, often representing 30-50% "
                "of the loan book. HNWI clients frequently pledge concentrated equity positions in "
                "closely held companies or single-stock portfolios. The 2022 rate shock exposed "
                "significant weaknesses in Lombard risk management at several private banks, with "
                "forced client liquidations damaging long-standing relationships."
            ),
        },
        {
            "id": "R018",
            "title": "Inadequate Collateral Valuation",
            "description": (
                "Collateral securing loans is overvalued due to stale pricing, inappropriate valuation "
                "methodology, or use of client-provided valuations without independent verification, "
                "resulting in insufficient coverage in the event of borrower default."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Independent price verification (IPV) for all collateral: daily for listed, monthly for unlisted",
                "Approved methodology for each collateral type in credit policy",
                "External appraisal required for real estate and private equity above defined threshold",
                "Haircuts applied to collateral values to account for liquidity and concentration risk",
                "Automatic LTV breach alert triggers margin call or credit review",
            ],
            "red_flags": [
                "Real estate collateral valued at purchase price — not independently appraised",
                "Private company shares valued at book value without DCF or market comparison",
                "Collateral revaluation frequency not commensurate with asset liquidity",
                "Client-provided valuations accepted without independent validation",
                "No haircut applied to illiquid collateral types",
            ],
            "private_banking_specifics": (
                "HNWI borrowers often offer illiquid assets as collateral: private company stakes, "
                "art, real estate in premium locations, or concentrated equity positions. These "
                "assets require specialist valuation and are difficult to realise quickly in a "
                "distress scenario. Over-reliance on client-provided valuations — common in "
                "high-trust private banking relationships — is a significant risk factor."
            ),
        },
        {
            "id": "R019",
            "title": "Credit Underwriting Standard Erosion",
            "description": (
                "Progressive weakening of credit approval standards under business pressure, "
                "resulting in loans approved outside policy, exceptions granted without adequate "
                "compensating controls, and credit risk appetite exceeded without Board awareness."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Credit policy reviewed and Board-approved annually; material exceptions require Board sign-off",
                "Credit committee with independent risk representation for all credits above threshold",
                "Exception log maintained with rationale, compensating controls, and time limit",
                "Monthly exception reporting to Credit Committee and Risk Committee",
                "Annual portfolio review against credit policy standards",
            ],
            "red_flags": [
                "Exception rate exceeding 15% of new credits in any quarter",
                "Same exceptions recur without policy amendment — policy not updated to reflect practice",
                "Credit approvals delegated to relationship managers without independent review",
                "Exception log not reviewed by Risk Committee",
                "Credit policy not updated despite material changes in market conditions",
            ],
            "private_banking_specifics": (
                "In private banking, credit decisions are often relationship-driven. Senior "
                "relationship managers may approve extensions for valued clients in anticipation "
                "of subsequent formalisation — bypassing credit committee review. The concentration "
                "of credit authority in senior RMs creates governance risk that is difficult "
                "to detect without granular credit file review and exception tracking."
            ),
        },
        {
            "id": "R020",
            "title": "Covenant Monitoring Failures",
            "description": (
                "Financial covenants on structured loans are not monitored proactively, resulting in "
                "undetected breaches that go unremedied and leave the bank exposed to deteriorating "
                "credit quality without the contractual right to accelerate or demand additional collateral."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "Medium",
            "expected_controls": [
                "Covenant monitoring system with automated alerts at defined thresholds (e.g. 10% headroom)",
                "Financial information from borrowers collected on schedule; non-submission flagged immediately",
                "Covenant breach reported to Credit Committee within 5 business days",
                "Waiver decisions documented with credit opinion and compensating conditions",
                "Portfolio report on covenant breaches and waivers to Risk Committee quarterly",
            ],
            "red_flags": [
                "Borrower financial statements not received on schedule — no systematic chase process",
                "Covenant monitoring performed manually in spreadsheets with no audit trail",
                "Waivers granted informally without credit committee approval",
                "Covenant headroom not monitored — breach discovered only at scheduled review",
                "Borrower has missed financial reporting obligations for >2 consecutive periods",
            ],
            "private_banking_specifics": (
                "Structured loans to HNWI clients — including facilities against investment portfolios "
                "or private company shares — often include financial performance covenants that are "
                "complex to monitor. Private banking RMs may be reluctant to enforce covenant "
                "provisions against valued clients, preferring informal arrangements that leave the "
                "bank legally exposed."
            ),
        },
        {
            "id": "R021",
            "title": "Inadequate Credit Provisioning",
            "description": (
                "Expected credit loss provisions under IFRS 9 are understated due to model "
                "deficiencies, optimistic assumptions, or inadequate forward-looking information, "
                "resulting in misstated financial statements and insufficient capital buffers."
            ),
            "level": "High",
            "probability": "Low",
            "impact": "High",
            "expected_controls": [
                "IFRS 9 model validated annually by independent model risk team",
                "Forward-looking macroeconomic scenarios reviewed at least quarterly",
                "Stage migration monitored monthly; manual adjustments documented with rationale",
                "Management overlay process with Board Audit Committee sign-off",
                "External auditor challenge of provisioning adequacy at half-year and year-end",
            ],
            "red_flags": [
                "All loans in Stage 1 — no credit deterioration identified despite market stress",
                "PD and LGD parameters not updated since model inception",
                "No management overlay despite material macroeconomic deterioration",
                "Provision coverage ratio declining materially without corresponding improvement in portfolio quality",
                "IFRS 9 model last validated more than 24 months ago",
            ],
            "private_banking_specifics": (
                "Private banks with smaller loan books may apply simplified IFRS 9 approaches "
                "that may not adequately capture the idiosyncratic risk of concentrated HNWI "
                "credit exposures. The illiquidity of collateral and the complexity of HNWI "
                "financial structures make loss-given-default estimation particularly challenging."
            ),
        },
    ],

    # ── OPERATIONAL RISK ───────────────────────────────────────────────────────
    "OPERATIONAL_RISK": [
        {
            "id": "R022",
            "title": "RCSA Framework Ineffectiveness",
            "description": (
                "Risk and Control Self-Assessment (RCSA) is performed as a box-ticking exercise "
                "rather than a genuine risk identification process, resulting in an inaccurate risk "
                "register that fails to reflect the actual control environment."
            ),
            "level": "High",
            "probability": "High",
            "impact": "Medium",
            "expected_controls": [
                "RCSA facilitated by risk management (2LoD), not solely self-assessed by business",
                "Risk ratings validated against loss data, audit findings, and external events",
                "RCSA output reviewed by CRO and presented to Risk Committee annually",
                "Action tracking for identified control weaknesses with defined owners and deadlines",
                "Annual methodology review to ensure RCSA remains fit for purpose",
            ],
            "red_flags": [
                "All risks rated low or moderate — no critical or high risks identified",
                "RCSA completed by the same person who operates the controls",
                "No update to RCSA following material operational incidents",
                "Action items from prior RCSA not tracked to completion",
                "RCSA output not reviewed by anyone outside the business unit",
            ],
            "private_banking_specifics": (
                "Private banks with flat organisational structures may lack a dedicated operational "
                "risk function capable of independently challenging RCSA outputs. Senior relationship "
                "managers who also control business processes have an inherent conflict of interest "
                "in assessing the adequacy of their own controls."
            ),
        },
        {
            "id": "R023",
            "title": "Key Person Dependency",
            "description": (
                "Critical business functions, client relationships, or operational processes depend "
                "on a single individual whose unexpected departure, incapacity, or misconduct would "
                "cause immediate and material operational disruption."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Key person mapping identifying all critical single-dependency roles",
                "Succession plans documented and reviewed annually for each identified role",
                "Knowledge transfer programme ensuring procedures are documented and transferable",
                "Cross-training of at least one deputy for each critical function",
                "Retention strategy for key staff; regular review of compensation benchmarking",
            ],
            "red_flags": [
                "Single RM managing >40% of total AUM with no deputy familiar with the portfolio",
                "Operational procedure documented only in the knowledge of one individual",
                "No succession plan for MLRO, CRO, CFO, or Head of Compliance",
                "Critical system access credentials known only to one IT staff member",
                "Key staff have not taken leave in >12 months — mandatory leave policy not enforced",
            ],
            "private_banking_specifics": (
                "Private banking is inherently relationship-intensive: a small number of senior "
                "relationship managers may control the vast majority of AUM. Client loyalty to "
                "the individual — not the institution — means that the departure of a key RM "
                "can trigger immediate and significant client attrition, creating both financial "
                "and operational risk simultaneously."
            ),
        },
        {
            "id": "R024",
            "title": "Change Management Control Failures",
            "description": (
                "System changes deployed without adequate testing, approval, or rollback procedures "
                "introduce errors into production systems, disrupt operations, or create security "
                "vulnerabilities that may not be detected until material damage occurs."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Change Advisory Board (CAB) approval required for all standard and major changes",
                "Mandatory testing in UAT environment before production deployment",
                "Rollback plan documented and tested before any major change",
                "Emergency change process with post-implementation review within 5 business days",
                "Post-implementation review for all major changes; lessons learned fed back to process",
            ],
            "red_flags": [
                "Emergency changes represent >20% of total change volume — overuse of expedited process",
                "Changes deployed directly to production without UAT — developer access to production",
                "No rollback plan for critical system changes",
                "Change failure rate (changes requiring rollback or causing incident) exceeds 5%",
                "Change freeze periods not observed during regulatory reporting periods",
            ],
            "private_banking_specifics": (
                "Regulatory reporting requirements — FINMA, MAS, HKMA — mean that system failures "
                "at month-end or regulatory reporting dates have immediate supervisory consequences. "
                "Private banks with small IT teams may bypass formal change management processes "
                "to deploy urgent fixes, creating operational and security risks."
            ),
        },
        {
            "id": "R025",
            "title": "Business Continuity Plan Inadequacy",
            "description": (
                "BCP is outdated, untested, or incomplete, such that in the event of a major "
                "disruption — cyber attack, natural disaster, or pandemic — the bank cannot "
                "recover critical operations within regulatory-required timeframes."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "BIA conducted annually; all critical functions identified with RTO and RPO",
                "Full failover test to alternate site conducted at least annually",
                "BCP document reviewed and Board-approved annually; updated after material events",
                "Alternate site maintained in operational readiness; independent from primary site",
                "BCP tested for ransomware and cyber attack scenarios, not just physical disruption",
            ],
            "red_flags": [
                "BCP last tested more than 12 months ago",
                "Alternate site uses same cloud provider or data centre as primary — not independent",
                "BCP does not cover cyber attack or ransomware scenarios",
                "RTO for critical systems not defined or validated through testing",
                "Staff not aware of BCP roles and responsibilities — no annual awareness training",
            ],
            "private_banking_specifics": (
                "Private banks operating across multiple jurisdictions must maintain jurisdiction-specific "
                "BCPs aligned with local regulatory requirements (MAS BCM, HKMA SPM, FINMA). "
                "The interconnected nature of private banking operations means that a disruption "
                "in one location can cascade across the group. Remote working arrangements "
                "introduced during COVID-19 must be embedded in tested BCPs."
            ),
        },
        {
            "id": "R026",
            "title": "Reconciliation and Settlement Failures",
            "description": (
                "Persistent unreconciled items in cash, securities, or nostro accounts indicate "
                "system or process failures that, if undetected, can result in financial losses, "
                "regulatory reporting errors, or client asset misappropriation."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Daily automated reconciliation of all cash and securities accounts",
                "Defined SLAs for break investigation: same-day for amounts >defined threshold",
                "Breaks aged >5 business days escalated to Operations Head and reported to Risk",
                "Segregation of duties: reconciliation performed independently from transaction booking",
                "Monthly reconciliation MIS reported to COO and Audit Committee",
            ],
            "red_flags": [
                "Reconciliation breaks aged >30 days without documented investigation",
                "Reconciliation performed by the same team that processes transactions",
                "No automated reconciliation — manual matching in spreadsheets",
                "Break volume increasing without corresponding investigation resource",
                "Nostro reconciliation breaks not investigated daily",
            ],
            "private_banking_specifics": (
                "Private banks acting as custodians for HNWI client assets face strict obligations "
                "under FINMA and MAS to maintain client asset segregation. Unreconciled positions "
                "between client records and custodian holdings could indicate client asset "
                "misappropriation — a criminal offence in all relevant jurisdictions."
            ),
        },
    ],

    # ── DATA PRIVACY ───────────────────────────────────────────────────────────
    "DATA_PRIVACY": [
        {
            "id": "R027",
            "title": "Unlawful Cross-Border Data Transfers",
            "description": (
                "Personal data of clients is transferred to jurisdictions without an EU/UK adequacy "
                "decision or appropriate safeguards (SCCs, BCRs), resulting in regulatory breach "
                "and potential enforcement action by data protection authorities."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Transfer impact assessment conducted for all cross-border data flows",
                "SCCs executed and in force for all transfers to non-adequate third countries",
                "Records of processing activities (RoPA) include all transfer destinations and mechanisms",
                "Post-Schrems II supplementary measures implemented for US data transfers",
                "Annual review of transfer mechanisms following changes in adequacy status",
            ],
            "red_flags": [
                "Data transferred to non-adequate country without executed SCCs or equivalent",
                "SCCs template used predates 2021 EC update — old SCCs no longer valid",
                "Transfer impact assessment never performed for US, India, or other common destinations",
                "Group data sharing agreement does not cover personal data transfers",
                "No awareness of jurisdiction of data hosting — cloud provider region not documented",
            ],
            "private_banking_specifics": (
                "Swiss private banks with global operations transfer client data across jurisdictions "
                "continuously: client onboarding data to Singapore, tax reporting data to EU, "
                "transaction data to UK-based systems. Post-Brexit, UK transfers require separate "
                "mechanisms from EU transfers. The nDSG 2023 introduced new transfer restrictions "
                "for Switzerland that must be assessed alongside GDPR obligations."
            ),
        },
        {
            "id": "R028",
            "title": "Excessive Data Retention",
            "description": (
                "Personal data is retained beyond the legally required retention period due to "
                "absence of defined retention schedules, lack of automated deletion processes, "
                "or inability to locate and delete data across fragmented legacy systems."
            ),
            "level": "High",
            "probability": "High",
            "impact": "Medium",
            "expected_controls": [
                "Documented retention schedule covering all personal data categories and legal bases",
                "Automated deletion or anonymisation triggered at end of retention period",
                "Annual compliance review confirming retention schedules are applied",
                "Data mapping exercise to identify all repositories holding personal data",
                "Legacy system review included in retention management programme",
            ],
            "red_flags": [
                "No formal retention schedule exists or has not been reviewed in >3 years",
                "Deletion is manual — no automated triggers for end-of-retention",
                "Former client data retained indefinitely on backup tapes not subject to the retention schedule",
                "Email archives contain client personal data with no retention controls applied",
                "Data inventory does not identify all repositories — shadow IT systems excluded",
            ],
            "private_banking_specifics": (
                "Private banks are subject to AML/CFT legislation requiring retention of KYC "
                "records for 10 years (5 years post-relationship end in most jurisdictions), "
                "banking secrecy laws, and tax reporting obligations — creating complex layered "
                "retention requirements. These requirements must be balanced against GDPR/nDSG "
                "data minimisation and storage limitation principles."
            ),
        },
        {
            "id": "R029",
            "title": "Inadequate Data Breach Detection and Response",
            "description": (
                "Data breaches go undetected for extended periods due to inadequate monitoring, "
                "or are not reported to regulators and affected individuals within the statutory "
                "72-hour window, resulting in regulatory fines and reputational damage."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "DLP solution monitoring for unusual data exfiltration patterns",
                "Documented breach response procedure with defined roles and notification timelines",
                "Breach register maintained for all incidents, including near-misses",
                "72-hour reporting clock triggers automatically upon detection of qualifying breach",
                "Annual tabletop exercise simulating data breach scenario including regulatory notification",
            ],
            "red_flags": [
                "No DLP solution — data exfiltration not monitored",
                "Breach response procedure not documented or not tested",
                "Regulatory notification obligation (72 hours) not known to IT and compliance teams",
                "Near-miss incidents not captured — breach register shows only confirmed breaches",
                "No process to assess whether a security incident constitutes a reportable breach",
            ],
            "private_banking_specifics": (
                "HNWI client data — account balances, investment positions, beneficial ownership, "
                "tax residency — is extraordinarily sensitive. A breach exposing this data would "
                "cause significant reputational damage and potential legal liability. Multiple "
                "supervisory authorities (FDPIC, ICO, CNIL, MAS) may have concurrent jurisdiction "
                "for the same breach, requiring coordinated multi-regulator notification."
            ),
        },
        {
            "id": "R030",
            "title": "Consent Management Failures",
            "description": (
                "Marketing, profiling, or data-sharing activities proceed without valid legal basis "
                "or consent, or consent records are not maintained, making it impossible to "
                "demonstrate compliance with data subject rights."
            ),
            "level": "Moderate",
            "probability": "Medium",
            "impact": "Medium",
            "expected_controls": [
                "Consent management platform recording consent, withdrawal, and purpose for all marketing",
                "Lawful basis documented for every processing activity in the RoPA",
                "Consent withdrawal process operationalised — withdrawal processed within 72 hours",
                "Profiling activities subject to DPIA before implementation",
                "Privacy notice reviewed annually and updated to reflect all processing activities",
            ],
            "red_flags": [
                "Marketing consent not recorded or record cannot be produced on request",
                "Pre-ticked consent boxes — not compliant with GDPR/nDSG",
                "No mechanism for data subjects to withdraw consent",
                "Profiling of client investment preferences without documented lawful basis",
                "Privacy notice not updated following introduction of new processing activities",
            ],
            "private_banking_specifics": (
                "Private banks use client data for multiple purposes beyond the core banking "
                "relationship: investment recommendations, cross-selling, referrals to affiliates, "
                "and tax reporting. Each purpose requires a distinct lawful basis under GDPR/nDSG. "
                "The legitimate interests basis — often relied upon for relationship management — "
                "requires a balancing test that must be documented."
            ),
        },
    ],

    # ── MARKET RISK ────────────────────────────────────────────────────────────
    "MARKET_RISK": [
        {
            "id": "R031",
            "title": "VaR Model Inadequacy",
            "description": (
                "Value-at-Risk model produces unreliable estimates due to historical data limitations, "
                "fat tail underestimation, or failure to capture current market conditions, resulting "
                "in under-capitalisation and limit breaches going undetected."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Backtesting of VaR model daily; number of exceptions tracked against Basel II traffic light",
                "Stress VaR and Expected Shortfall calculated alongside VaR",
                "Model validation by independent team at least annually",
                "P&L attribution analysis to identify model weaknesses",
                "Model limitations documented and communicated to senior management",
            ],
            "red_flags": [
                "More than 10 VaR backtesting exceptions in a 250-day rolling window (Red Zone)",
                "VaR model not validated in the past 24 months",
                "VaR model uses historical data window <1 year — insufficient through-the-cycle calibration",
                "Stress testing not performed alongside VaR",
                "Correlation assumptions hard-coded — not updated for current market regime",
            ],
            "private_banking_specifics": (
                "Private bank trading books are typically smaller and less liquid than those of "
                "investment banks. Standard VaR models calibrated on market-wide data may not "
                "adequately capture the specific risk profile of HNWI-driven positions. "
                "FRTB implementation from 2025 will require fundamental changes to market "
                "risk capital calculation for banks using internal models."
            ),
        },
        {
            "id": "R032",
            "title": "Market Risk Limit Breaches",
            "description": (
                "Market risk limits — VaR, sensitivity (DV01, CS01), stop-loss — are breached "
                "and not escalated or resolved promptly, normalising limit exceedances and "
                "degrading the risk management framework."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Automated limit monitoring with real-time alerts to risk management and front office",
                "Escalation matrix: breach >1 day requires Head of Risk sign-off; >3 days requires CRO",
                "All limit breaches logged with resolution actions and timelines",
                "Risk Committee receives monthly report on limit utilisation and all breaches",
                "Annual review and Board approval of limit framework",
            ],
            "red_flags": [
                "Limit breaches resolved informally — no written record or sign-off",
                "Same limit breached repeatedly without policy review",
                "Risk limits not reviewed since 2022 — market conditions have changed materially",
                "Front office and risk management use different systems — limit monitoring data inconsistent",
                "Soft limits consistently breached without action — effective limit is materially higher than documented",
            ],
            "private_banking_specifics": (
                "In private banking, market risk limits may apply to advisory and discretionary "
                "mandates as well as the proprietary trading book. Limit breaches in client portfolios "
                "managed on a discretionary basis may also constitute a client mandate breach — "
                "creating both regulatory and legal liability alongside market risk."
            ),
        },
        {
            "id": "R033",
            "title": "Interest Rate Risk in the Banking Book (IRRBB)",
            "description": (
                "Rapid changes in interest rates create mismatches between asset and liability "
                "repricing profiles in the banking book, resulting in net interest income (NII) "
                "volatility and economic value of equity (EVE) deterioration beyond risk appetite."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "NII and EVE sensitivity calculated monthly under six prescribed BCBS stress scenarios",
                "IRRBB limits approved by ALCO and Board; reported against monthly",
                "Hedging strategy reviewed by ALCO quarterly — interest rate swaps, caps, floors",
                "Behavioural assumptions (deposit repricing, prepayment) modelled and validated annually",
                "Pillar 2 capital requirement for IRRBB assessed in ICAAP annually",
            ],
            "red_flags": [
                "EVE impact under +200bp shock exceeds 15% of Tier 1 capital",
                "Behavioural assumptions not updated since the low-rate environment of 2021",
                "IRRBB stress testing limited to parallel shift scenarios — no twist or short-rate shocks",
                "ALCO receives NII/EVE data less than monthly",
                "No active hedging programme — banking book exposed to full interest rate risk",
            ],
            "private_banking_specifics": (
                "Swiss private banks with significant sight deposit bases (client cash awaiting "
                "investment) face IRRBB from the maturity transformation between on-demand liabilities "
                "and longer-duration assets. The 2022 rate shock highlighted that banks with "
                "modelled deposit betas based on the 2010-2021 low-rate environment significantly "
                "underestimated deposit repricing speed."
            ),
        },
    ],

    # ── THIRD PARTY RISK ───────────────────────────────────────────────────────
    "THIRD_PARTY_RISK": [
        {
            "id": "R034",
            "title": "Inadequate Third-Party Due Diligence",
            "description": (
                "Service providers are onboarded without adequate assessment of their financial "
                "stability, operational resilience, security posture, and regulatory compliance, "
                "creating exposure to vendor failures, data breaches, and regulatory non-compliance."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Risk-tiered due diligence framework: enhanced for critical/material, standard for non-material",
                "Security questionnaire and SOC 2 Type II review for all technology vendors",
                "Financial health assessment for critical vendors; monitoring for material changes",
                "Regulatory compliance check (sanctions, debarment) before engagement",
                "Annual re-assessment for critical and material vendors",
            ],
            "red_flags": [
                "Vendor onboarded without formal due diligence — engagement predates current policy",
                "SOC 2 report not available or qualified opinion not investigated",
                "No financial health review for critical vendor despite signs of financial distress",
                "Vendor in FATF grey-listed jurisdiction — no enhanced due diligence applied",
                "Due diligence performed once at onboarding — no periodic refresh",
            ],
            "private_banking_specifics": (
                "Private banks rely heavily on specialised vendors: custody platforms (SIX, Euroclear, "
                "DTC), portfolio management systems (SimCorp, Avaloq, Temenos), compliance tools "
                "(Refinitiv World-Check, Dow Jones), and communication platforms. A failure of any "
                "critical vendor can disrupt front-to-back operations. DORA requires documented "
                "due diligence and ongoing monitoring for all ICT third-party arrangements."
            ),
        },
        {
            "id": "R035",
            "title": "Concentration Risk — Single Critical Vendor",
            "description": (
                "Dependence on a single vendor for a critical service — core banking, custody, "
                "cloud infrastructure — without an adequate alternative means any disruption "
                "to that vendor has immediate and potentially prolonged impact on operations."
            ),
            "level": "High",
            "probability": "Low",
            "impact": "High",
            "expected_controls": [
                "Vendor concentration risk assessment identifying single-point-of-failure dependencies",
                "Exit strategy documented and tested for each critical vendor",
                "Multi-vendor strategy for non-substitutable services where economically feasible",
                "Contractual protections: minimum service levels, step-in rights, data portability",
                "Concentration risk report to Risk Committee and Board annually",
            ],
            "red_flags": [
                "No exit strategy exists for the core banking system vendor",
                "100% of cloud infrastructure hosted on a single cloud provider with no alternative",
                "Contract with critical vendor does not include data portability or exit assistance obligations",
                "Exit strategy documented but never tested — data migration feasibility not validated",
                "Switching cost for critical vendor effectively prevents any meaningful exit — vendor lock-in",
            ],
            "private_banking_specifics": (
                "Many private banks rely on a single integrated platform (e.g. Avaloq, Temenos) "
                "for front-to-back operations — from client onboarding to custody and reporting. "
                "Migrating away from such a platform is a multi-year, multi-million-franc project. "
                "DORA explicitly requires concentration risk to be assessed and exit strategies "
                "to be documented, even where substitution is commercially unrealistic."
            ),
        },
        {
            "id": "R036",
            "title": "Sub-Outsourcing Chain Risk",
            "description": (
                "Critical vendors sub-contract material components of their service to fourth parties "
                "without the bank's knowledge or approval, creating hidden dependencies and making "
                "it impossible to maintain adequate oversight of the full delivery chain."
            ),
            "level": "Moderate",
            "probability": "Medium",
            "impact": "Medium",
            "expected_controls": [
                "Contractual prohibition on material sub-outsourcing without prior written consent",
                "Annual disclosure from critical vendors of all material sub-outsourcers",
                "Sub-outsourcers subject to equivalent security and operational standards as primary vendor",
                "Register of known fourth-party dependencies maintained and reviewed quarterly",
                "DORA Article 30 register covers all ICT sub-outsourcing arrangements",
            ],
            "red_flags": [
                "Contract does not address sub-outsourcing — no consent or prohibition clause",
                "Primary vendor has not disclosed sub-outsourcers despite contractual obligation",
                "Critical infrastructure component delivered by a fourth party in a high-risk jurisdiction",
                "Sub-outsourcing chain includes entities on sanctions lists",
                "Bank has no visibility of the sub-outsourcing chain beyond the primary vendor",
            ],
            "private_banking_specifics": (
                "Cloud-native fintech vendors embedded in private banking workflows (e.g. RegTech "
                "tools, data analytics platforms) frequently rely on sub-processors — often "
                "hyperscale cloud providers — for their own delivery. The bank's data may traverse "
                "multiple sub-processors across multiple jurisdictions, creating data residency "
                "and security risks that the bank cannot directly observe."
            ),
        },
    ],

    # ── GOVERNANCE ─────────────────────────────────────────────────────────────
    "GOVERNANCE": [
        {
            "id": "R037",
            "title": "Board Oversight Deficiencies",
            "description": (
                "The Board of Directors fails to exercise effective oversight of risk management, "
                "receiving information that is too aggregated, too late, or too favourable, "
                "preventing it from fulfilling its supervisory and strategic responsibilities."
            ),
            "level": "Critical",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Risk reporting framework: Board receives granular risk dashboard monthly",
                "Board Risk Committee meets at minimum quarterly; independent chair",
                "Board members have relevant financial services expertise; skills matrix reviewed annually",
                "Board self-assessment conducted annually; external evaluation every 3 years",
                "Direct reporting line from CRO, CCO, and Head of Internal Audit to Board committees",
            ],
            "red_flags": [
                "Board receives only summary-level risk report — no granular data or trend analysis",
                "Risk Committee meets less than quarterly",
                "Same individual chairs both the Audit Committee and Risk Committee",
                "CRO does not have a direct reporting line to the Board — reports only through CEO",
                "Board members have not received financial crime or cyber risk training in the past 2 years",
            ],
            "private_banking_specifics": (
                "The Credit Suisse collapse focused global regulatory attention on board oversight "
                "failures. FINMA-RS 2017/1 and MAS CG 2018 establish specific board composition "
                "and committee requirements. For private banks with concentrated ownership by "
                "founding families or parent groups, the independence of non-executive directors "
                "and Board committees requires particular scrutiny."
            ),
        },
        {
            "id": "R038",
            "title": "Inadequate Three Lines of Defence",
            "description": (
                "The Three Lines of Defence model is poorly implemented: business lines (1LoD) are "
                "unaware of their risk ownership; the risk and compliance function (2LoD) is "
                "insufficiently independent; internal audit (3LoD) lacks objectivity or resources."
            ),
            "level": "High",
            "probability": "High",
            "impact": "High",
            "expected_controls": [
                "Documented Three Lines of Defence framework with clear role descriptions",
                "Risk and compliance functions report independently of business lines",
                "Internal audit Head reports to Audit Committee, not CEO",
                "1LoD control accountability embedded in staff KPIs and performance reviews",
                "Annual assessment of Three Lines model effectiveness by Internal Audit",
            ],
            "red_flags": [
                "Compliance function reports to Head of Business — not independent of revenue",
                "Internal audit budget set by management, not by Audit Committee",
                "No distinction between 1LoD controls and 2LoD monitoring — roles conflated",
                "Audit findings consistently low severity — possible independence or competence issue",
                "2LoD and 3LoD performing identical controls without differentiation",
            ],
            "private_banking_specifics": (
                "Smaller private banks often have combined 1LoD/2LoD functions due to resource "
                "constraints, with RMs also performing initial compliance checks. This structural "
                "weakness is known to regulators and is a primary focus of FINMA and MAS "
                "supervisory reviews. Internal audit independence is particularly critical where "
                "the Head of Audit reports to a CEO who also has business responsibilities."
            ),
        },
        {
            "id": "R039",
            "title": "Conflicts of Interest",
            "description": (
                "Undisclosed or unmanaged conflicts of interest — between personal interests and "
                "client interests, or between proprietary business and client mandates — create "
                "legal liability, regulatory risk, and reputational damage."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Conflicts of interest register maintained and reviewed quarterly by compliance",
                "Personal account dealing policy with pre-clearance for all staff in material functions",
                "Outside business interests disclosed and approved annually",
                "Chinese walls and information barriers between advisory and proprietary functions",
                "Client-facing staff trained annually on conflicts identification and escalation",
            ],
            "red_flags": [
                "Personal account dealing log incomplete or not reviewed by compliance",
                "Staff purchasing securities in clients' names without documented authority",
                "Proprietary positions held in same securities recommended to clients — no information barrier",
                "Conflicts register not updated despite material changes in staff roles or outside interests",
                "No pre-clearance requirement for personal account dealing",
            ],
            "private_banking_specifics": (
                "Relationship managers in private banking face inherent conflicts between advising "
                "clients to hold cash (generating no fees) versus recommending products generating "
                "retrocessions or performance fees. Fee transparency requirements under MiFID II "
                "and Swiss FinSA require explicit disclosure. Personal investments in client "
                "companies and advisory board seats are common undisclosed conflicts."
            ),
        },
        {
            "id": "R040",
            "title": "Whistleblowing Framework Deficiency",
            "description": (
                "Whistleblowing mechanism is not adequately publicised, does not protect "
                "reporters from retaliation, or reports are not investigated promptly and "
                "independently — resulting in underreporting of misconduct and fraud."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Anonymous reporting channel (hotline or web portal) managed by independent third party",
                "Non-retaliation policy documented, communicated, and enforced",
                "All whistleblowing reports triaged within 48 hours; investigated within 30 days",
                "Annual communication to all staff on availability and confidentiality of reporting channel",
                "Reports reviewed by Audit Committee chair; escalated to Board where material",
            ],
            "red_flags": [
                "Whistleblowing reports very low in number relative to staff headcount (<1 per 200 FTE annually)",
                "Reports directed to line management — no anonymous or independent channel",
                "No investigation timeline defined — reports may go unresolved for months",
                "Whistleblowing policy not published in staff handbook or accessible on intranet",
                "Cases of apparent retaliation against reporters not investigated",
            ],
            "private_banking_specifics": (
                "The close-knit culture of private banking — where staff are often long-tenured and "
                "relationships are highly personal — creates strong disincentives to report misconduct. "
                "High client-value transactions that cross compliance boundaries may go unreported "
                "to protect senior relationships. An effective, genuinely anonymous channel is "
                "therefore disproportionately important in private banking relative to retail banking."
            ),
        },
    ],

    "LIQUIDITY_RISK": [
        {
            "id": "R041",
            "title": "LCR / NSFR Threshold Breach Risk",
            "description": (
                "The Liquidity Coverage Ratio (LCR) or Net Stable Funding Ratio (NSFR) falls below "
                "the regulatory minimum of 100% due to unexpected deposit outflows, HQLA quality "
                "deterioration, or modelling errors in outflow assumptions — resulting in regulatory "
                "breach and potential FINMA intervention."
            ),
            "level": "Critical",
            "probability": "Low",
            "impact": "High",
            "level_rationale": "Elevated to Critical: LCR breach is a direct regulatory violation triggering mandatory FINMA notification and potential supervisory intervention; post-CS sector experience demonstrates that threshold breaches can escalate to existential liquidity events within days.",
            "expected_controls": [
                "Daily LCR calculation and monitoring with automated breach alert at 110% (early warning) and 100% (regulatory minimum)",
                "Monthly NSFR calculation with trend analysis and Board reporting",
                "Intraday liquidity monitoring across all material currencies and settlement accounts",
                "Conservative outflow assumptions for HNWI sight deposits reflecting actual behavioural data",
                "Contingency Funding Plan (CFP) with defined triggers and escalation procedures tested semi-annually",
            ],
            "red_flags": [
                "LCR calculation relies on manual spreadsheets rather than automated treasury system",
                "Outflow assumptions for HNWI deposits not reviewed since pre-2023 market stress",
                "HQLA buffer concentrated in Level 2/3 assets with limited same-day liquidity",
                "Intraday liquidity monitoring limited to end-of-day batch calculation",
                "CFP not tested in the past 12 months or test limited to desktop exercise",
            ],
            "private_banking_specifics": (
                "HNWI client deposits are structurally less stable than retail deposits: larger average "
                "balances, higher price sensitivity, and potential for rapid coordinated withdrawal "
                "in response to reputational events (as demonstrated by Credit Suisse Q4 2022). "
                "Standard LCR outflow assumptions calibrated to retail banking understate the "
                "run-risk of private banking deposit books."
            ),
        },
        {
            "id": "R042",
            "title": "Deposit Concentration and Run Risk",
            "description": (
                "Excessive concentration of funding in a small number of large HNWI depositors creates "
                "asymmetric liquidity risk: withdrawal of top-10 depositors could trigger immediate "
                "LCR breach and require emergency asset liquidation or central bank facility access."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "Concentration limits for largest depositors (e.g. no single depositor >5% of total deposits)",
                "Quarterly stress test modelling simultaneous withdrawal of top-10 depositors",
                "Monitoring of deposit outflow velocity against CFP escalation triggers",
                "Client relationship intelligence to detect early indicators of withdrawal intent",
                "Diversified funding base including term deposits, covered bonds, and repo facilities",
            ],
            "red_flags": [
                "Top-10 depositors represent >30% of total deposit base",
                "No defined depositor concentration limit or annual review",
                "Stress test does not model correlated withdrawal scenarios (multiple clients simultaneously)",
                "Sight-to-term deposit ratio increasing without compensating HQLA build",
                "No early-warning monitoring for large depositor behavioural changes",
            ],
            "private_banking_specifics": (
                "Private banking inherently creates deposit concentration: an institution with 500 "
                "HNWI clients of which 20 hold CHF 50M+ constitutes a funding model fundamentally "
                "different from retail banking. Post-SVB and Credit Suisse, regulators now expect "
                "private banks to explicitly model and stress-test this concentration in ILAAP."
            ),
        },
        {
            "id": "R043",
            "title": "HQLA Quality and Liquidity Horizon Risk",
            "description": (
                "High Quality Liquid Assets (HQLA) in the liquidity buffer are concentrated in "
                "Level 2 or Level 2B assets, or in assets whose market liquidity deteriorates "
                "rapidly under stress conditions, such that the theoretical LCR does not reflect "
                "actual cashable liquidity in a stress scenario."
            ),
            "level": "High",
            "probability": "Medium",
            "impact": "High",
            "expected_controls": [
                "HQLA classification regularly reviewed against regulatory eligibility criteria",
                "Concentration limits for Level 2/2B assets within the HQLA buffer (max 40%/15% per Basel III)",
                "Independent price verification for HQLA mark-to-market; haircut assumptions reviewed quarterly",
                "HQLA monetisation test: annual live test of ability to repo or sell HQLA within 24 hours",
                "Operational segregation of HQLA: assets held in dedicated custody accounts free from encumbrance",
            ],
            "red_flags": [
                "HQLA buffer dominated by private bank bonds or structured notes classified as Level 2",
                "No live HQLA monetisation test conducted in the past 12 months",
                "Haircut assumptions for Level 2 assets not stress-tested under market dislocation scenario",
                "HQLA operationally co-mingled with investment portfolio; encumbrance not tracked",
                "Concentration of HQLA in single issuer or currency creates liquidity correlation risk",
            ],
            "private_banking_specifics": (
                "Private banks managing client assets alongside proprietary HQLA face specific operational "
                "risk: client-owned securities held in custody may be inappropriately included in HQLA "
                "calculations. Bespoke structured products held on balance sheet as proprietary investments "
                "are frequently misclassified as HQLA despite having no active secondary market."
            ),
        },
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# 4. CVE_BANKING
# ═══════════════════════════════════════════════════════════════════════════════

CVE_BANKING = [
    {
        "cve_id": "CVE-2021-44228",
        "date": "2021-12-10",
        "severity": "Critical",
        "cvss_score": 10.0,
        "system_affected": "Apache Log4j 2 (Log4Shell)",
        "description": (
            "Critical remote code execution vulnerability in the Apache Log4j 2 Java logging library "
            "via JNDI injection. Exploitation requires no authentication and no special privileges. "
            "Affects any Java application using Log4j 2.0-beta9 through 2.14.1."
        ),
        "recommended_action": (
            "Immediately upgrade to Log4j 2.17.1 or later. Apply JNDI disabling workaround as interim "
            "measure (set log4j2.formatMsgNoLookups=true). Conduct full inventory of all Java applications "
            "using the affected library. Monitor for exploitation indicators in network and application logs."
        ),
        "banking_relevance": (
            "Log4j is embedded in hundreds of enterprise Java applications used in banking: trading platforms, "
            "SIEM solutions, regulatory reporting systems, and middleware. Financial institutions were primary "
            "targets in the weeks following disclosure. Rapid exploitation by nation-state actors and "
            "ransomware groups made this the most critical vulnerability of 2021-2022 for the sector."
        ),
    },
    {
        "cve_id": "CVE-2023-34362",
        "date": "2023-05-31",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Progress Software MOVEit Transfer",
        "description": (
            "SQL injection vulnerability in MOVEit Transfer web application allowing unauthenticated "
            "remote attackers to gain unauthorised access to databases, exfiltrate sensitive data, "
            "and potentially execute arbitrary code. Exploited at scale by Cl0p ransomware group."
        ),
        "recommended_action": (
            "Apply vendor patch immediately (versions 2021.0.7, 2021.1.5, 2022.0.5, 2022.1.9, 2023.0.2). "
            "Review MOVEit Transfer audit logs for signs of exploitation (SQLi patterns, unusual file access). "
            "Assess all data stored or transmitted through MOVEit; notify affected individuals if breach confirmed."
        ),
        "banking_relevance": (
            "MOVEit Transfer is widely used in financial services for secure file transfer between banks, "
            "regulators, auditors, and outsourced service providers. The Cl0p campaign compromised "
            "hundreds of organisations globally including multiple financial institutions, payroll processors "
            "(Zellis, Aon), and pension administrators. Client and employee data from major banks was exfiltrated."
        ),
    },
    {
        "cve_id": "CVE-2023-46604",
        "date": "2023-10-27",
        "severity": "Critical",
        "cvss_score": 10.0,
        "system_affected": "Apache ActiveMQ (messaging broker)",
        "description": (
            "Remote code execution vulnerability in Apache ActiveMQ allowing unauthenticated remote "
            "attackers to execute arbitrary shell commands by manipulating the ExceptionResponse "
            "and OpenWire protocol. Actively exploited by HelloKitty ransomware group."
        ),
        "recommended_action": (
            "Upgrade Apache ActiveMQ to versions 5.15.16, 5.16.7, 5.17.6, or 5.18.3 immediately. "
            "Network-isolate ActiveMQ brokers from internet-facing systems. Audit for signs of exploitation: "
            "unusual processes spawned by ActiveMQ, new admin accounts, outbound C2 connections."
        ),
        "banking_relevance": (
            "Apache ActiveMQ is used in financial messaging infrastructure including SWIFT integration "
            "layers, trading system event buses, and batch processing pipelines. Exploitation could "
            "allow attackers to intercept or manipulate financial messages, disrupt transaction processing, "
            "or use the broker as a pivot point into core banking networks."
        ),
    },
    {
        "cve_id": "CVE-2023-4966",
        "date": "2023-10-10",
        "severity": "Critical",
        "cvss_score": 9.4,
        "system_affected": "Citrix NetScaler ADC and Gateway (Citrix Bleed)",
        "description": (
            "Sensitive information disclosure vulnerability in Citrix NetScaler that allows unauthenticated "
            "attackers to retrieve session tokens from device memory, enabling full session hijacking "
            "and bypassing MFA. Exploited extensively by Lockbit ransomware affiliates in 2023-2024."
        ),
        "recommended_action": (
            "Update to NetScaler ADC and NetScaler Gateway 14.1-8.50, 13.1-49.15, 13.0-92.19 or later. "
            "Terminate all active sessions after patching. Investigate all authentication logs for "
            "session token theft indicators. Conduct forensic review if exploitation suspected."
        ),
        "banking_relevance": (
            "Citrix NetScaler is the dominant remote access and application delivery solution at financial "
            "institutions. Exploitation of CVE-2023-4966 allowed attackers to bypass MFA and access "
            "internal banking systems as authenticated users. Multiple financial institutions confirmed "
            "compromise via Citrix Bleed during Q4 2023, with Lockbit deploying ransomware post-access."
        ),
    },
    {
        "cve_id": "CVE-2023-27997",
        "date": "2023-06-12",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Fortinet FortiOS SSL-VPN",
        "description": (
            "Heap-based buffer overflow in FortiOS SSL-VPN web management interface allowing "
            "pre-authentication remote code execution. Impacts FortiOS 6.0 through 7.2.4 and "
            "FortiProxy 1.x through 7.2.3. Actively exploited by threat actors including APT groups."
        ),
        "recommended_action": (
            "Upgrade to FortiOS 6.0.17, 6.2.15, 6.4.13, 7.0.12, 7.2.5 or higher immediately. "
            "If immediate patching is not possible, disable SSL-VPN as an interim measure. "
            "Review VPN logs for anomalous authentication patterns and unusual connection sources."
        ),
        "banking_relevance": (
            "Fortinet FortiGate/FortiOS is widely deployed as the VPN gateway and perimeter firewall "
            "at financial institutions globally. This vulnerability enabled unauthenticated access to "
            "internal banking networks, bypassing all perimeter security. Several central banks and "
            "commercial banks in Asia and Europe confirmed exploitation in 2023."
        ),
    },
    {
        "cve_id": "CVE-2024-3400",
        "date": "2024-04-12",
        "severity": "Critical",
        "cvss_score": 10.0,
        "system_affected": "Palo Alto Networks PAN-OS (GlobalProtect VPN)",
        "description": (
            "Command injection vulnerability in the GlobalProtect gateway feature of PAN-OS allowing "
            "unauthenticated remote code execution with root privileges. Requires GlobalProtect gateway "
            "or GlobalProtect portal to be enabled. Exploited as a zero-day by threat group UTA0218."
        ),
        "recommended_action": (
            "Apply hotfix immediately: PAN-OS 10.2.9-h1, 11.0.4-h1, 11.1.2-h3. Enable Threat Prevention "
            "signature 95187 as interim mitigation if patching is delayed. Perform threat assessment "
            "to determine whether systems were compromised before patch application."
        ),
        "banking_relevance": (
            "PAN-OS is a leading enterprise firewall and VPN platform deployed at major financial "
            "institutions. Zero-day exploitation allowed attackers to establish backdoors in banking "
            "network perimeters, exfiltrate configuration data, and create persistent access. "
            "The financial sector was among the primary targets of UTA0218 exploitation campaign."
        ),
    },
    {
        "cve_id": "CVE-2022-41040",
        "date": "2022-10-03",
        "severity": "Critical",
        "cvss_score": 8.8,
        "system_affected": "Microsoft Exchange Server (ProxyNotShell)",
        "description": (
            "Server-side request forgery (SSRF) vulnerability in Microsoft Exchange Server that, "
            "chained with CVE-2022-41082 (remote code execution), allows authenticated attackers "
            "to execute arbitrary PowerShell commands with SYSTEM privileges on Exchange servers."
        ),
        "recommended_action": (
            "Apply November 2022 Cumulative Update for Exchange Server. As an interim measure, "
            "configure URL Rewrite rules to block exploitation patterns. Monitor Exchange logs "
            "for abnormal PowerShell activity and web shell deployments."
        ),
        "banking_relevance": (
            "Microsoft Exchange is the primary email platform at most financial institutions. "
            "Compromise of Exchange servers provides access to all corporate email — including "
            "payment instructions, client communications, and internal strategy documents. "
            "Banking-sector targets included custody banks and wealth management firms during the "
            "initial exploitation window before patches were available."
        ),
    },
    {
        "cve_id": "CVE-2022-40684",
        "date": "2022-10-10",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Fortinet FortiOS, FortiProxy, FortiSwitchManager",
        "description": (
            "Authentication bypass vulnerability using an alternate path or channel in Fortinet "
            "FortiOS, FortiProxy, and FortiSwitchManager allows an unauthenticated attacker to "
            "perform operations on the administrative interface via specially crafted HTTP requests."
        ),
        "recommended_action": (
            "Upgrade to FortiOS 7.0.7 or 7.2.2 and above, FortiProxy 7.0.7 or 7.2.1 and above. "
            "Disable HTTP/HTTPS management interface from internet-facing interfaces. "
            "Review admin account creation and configuration changes since vulnerability window."
        ),
        "banking_relevance": (
            "Immediately exploited after disclosure to create backdoor admin accounts on Fortinet "
            "devices at financial institutions. Attackers used access to reconfigure firewall rules, "
            "establish persistent VPN access, and conduct reconnaissance of internal banking networks. "
            "CISA issued emergency directive requiring federal agencies to patch within 3 days."
        ),
    },
    {
        "cve_id": "CVE-2022-26134",
        "date": "2022-06-03",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Atlassian Confluence Server and Data Center",
        "description": (
            "Object-Graph Navigation Language (OGNL) injection vulnerability in Confluence Server "
            "and Data Center allowing unauthenticated remote attackers to execute arbitrary code. "
            "Exploited as a zero-day; tens of thousands of servers were compromised within days."
        ),
        "recommended_action": (
            "Apply vendor patch immediately (versions 7.4.17, 7.13.7, 7.14.3, 7.15.2, 7.16.4, "
            "7.17.4, 7.18.1 and later). If immediate patching is not possible, restrict Confluence "
            "access to trusted networks. Review Confluence logs for web shell installation indicators."
        ),
        "banking_relevance": (
            "Confluence is widely used in financial institutions for internal knowledge management, "
            "audit documentation, procedure libraries, and regulatory tracking. Compromise allows "
            "access to sensitive internal documentation including audit programmes, risk assessments, "
            "and business continuity plans. Exploitation was followed by ransomware deployment in "
            "several confirmed financial sector cases."
        ),
    },
    {
        "cve_id": "CVE-2022-22965",
        "date": "2022-03-31",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "VMware Spring Framework (Spring4Shell)",
        "description": (
            "Remote code execution vulnerability in Spring MVC and Spring WebFlux applications "
            "running on JDK 9 and above. Allows unauthenticated attackers to execute arbitrary "
            "commands via data binding and class loader manipulation."
        ),
        "recommended_action": (
            "Upgrade to Spring Framework 5.3.18 or 5.2.20 and above. Set disallowedFields on "
            "DataBinder in WebMvcConfigurer as a temporary mitigation. Identify all Java applications "
            "using the vulnerable Spring version and prioritise patching for internet-facing services."
        ),
        "banking_relevance": (
            "Spring Framework is the dominant Java web application framework used in banking middleware, "
            "API gateways, and customer-facing digital banking platforms. Internet-facing banking "
            "applications built on Spring were immediately at risk. Rapid exploitation was observed "
            "for cryptomining and ransomware deployment targeting financial services infrastructure."
        ),
    },
    {
        "cve_id": "CVE-2022-22954",
        "date": "2022-04-11",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "VMware Workspace ONE Access and Identity Manager",
        "description": (
            "Server-side template injection vulnerability in VMware Workspace ONE Access and "
            "VMware Identity Manager allowing unauthenticated remote code execution as root. "
            "Exploited by Iranian state-sponsored threat groups targeting financial sector."
        ),
        "recommended_action": (
            "Apply VMware security advisory VMSA-2022-0011 patches immediately. Assess for indicators "
            "of compromise: new admin accounts, scheduled tasks, or processes spawned by Workspace ONE. "
            "Implement network monitoring for anomalous traffic from Workspace ONE servers."
        ),
        "banking_relevance": (
            "VMware Workspace ONE is used for mobile device management and single sign-on in financial "
            "institutions — compromise provides access to all SSO-integrated systems including email, "
            "trading platforms, and core banking portals. CISA confirmed exploitation of this "
            "vulnerability by Iranian APT targeting critical infrastructure including banking."
        ),
    },
    {
        "cve_id": "CVE-2023-20198",
        "date": "2023-10-16",
        "severity": "Critical",
        "cvss_score": 10.0,
        "system_affected": "Cisco IOS XE Web UI (network infrastructure)",
        "description": (
            "Privilege escalation vulnerability in the web UI feature of Cisco IOS XE Software "
            "allowing unauthenticated remote attackers to create an account with privilege level 15 "
            "(full admin access). Exploited at massive scale as a zero-day before patch availability."
        ),
        "recommended_action": (
            "Disable the HTTP Server feature on all internet-facing IOS XE devices immediately "
            "(no ip http server / no ip http secure-server). Apply Cisco patch as available. "
            "Review all IOS XE devices for unauthorised admin accounts created after the vulnerability window."
        ),
        "banking_relevance": (
            "Cisco IOS XE powers core network infrastructure at most large financial institutions: "
            "routers, switches, and WAN edge devices forming the backbone of banking networks. "
            "Exploitation created backdoor admin accounts allowing attackers full control of network "
            "devices — enabling traffic interception, route manipulation, and persistent access to "
            "internal banking network segments."
        ),
    },
    {
        "cve_id": "CVE-2023-29357",
        "date": "2023-06-13",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Microsoft SharePoint Server",
        "description": (
            "Authentication bypass vulnerability in Microsoft SharePoint Server allowing unauthenticated "
            "attackers to spoof JWT authentication tokens and gain administrator privileges without "
            "providing credentials. Chained with CVE-2023-24955 for remote code execution."
        ),
        "recommended_action": (
            "Apply June 2023 Patch Tuesday cumulative update for SharePoint. Monitor SharePoint audit "
            "logs for unusual administrator activity and unexpected file access by system accounts. "
            "Restrict SharePoint access to trusted networks where possible."
        ),
        "banking_relevance": (
            "SharePoint is the primary document management and intranet platform in financial institutions. "
            "It stores compliance documents, AML policies, audit reports, client onboarding files, and "
            "regulatory correspondence. Unauthorised admin access exposes highly sensitive regulatory "
            "and strategic information to theft or manipulation."
        ),
    },
    {
        "cve_id": "CVE-2024-21762",
        "date": "2024-02-09",
        "severity": "Critical",
        "cvss_score": 9.6,
        "system_affected": "Fortinet FortiOS and FortiProxy (SSL-VPN)",
        "description": (
            "Out-of-bounds write vulnerability in Fortinet FortiOS and FortiProxy SSL-VPN that "
            "allows unauthenticated remote attackers to execute arbitrary code or commands via "
            "specially crafted HTTP requests. Actively exploited in the wild at time of disclosure."
        ),
        "recommended_action": (
            "Upgrade to FortiOS 7.4.3, 7.2.7, 7.0.14, 6.4.15 or above, or disable SSL-VPN immediately. "
            "CISA listed this as a Known Exploited Vulnerability (KEV) within days of disclosure. "
            "Conduct forensic review of SSL-VPN logs for pre-patch exploitation indicators."
        ),
        "banking_relevance": (
            "The continued stream of critical vulnerabilities in Fortinet's SSL-VPN product — used for "
            "remote access by banking staff, third-party vendors, and IT administrators — highlights "
            "the persistent risk of VPN infrastructure. Financial institutions relying on Fortinet "
            "for remote access must maintain an aggressive patch schedule and monitor KEV status."
        ),
    },
    {
        "cve_id": "CVE-2023-48788",
        "date": "2024-03-13",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Fortinet FortiClientEMS",
        "description": (
            "SQL injection vulnerability in Fortinet FortiClientEMS allowing unauthenticated remote "
            "attackers to execute code or commands via specially crafted requests. Exploited "
            "against financial sector targets by cybercriminal groups in Q1-Q2 2024."
        ),
        "recommended_action": (
            "Upgrade to FortiClientEMS 7.0.11 or 7.2.4 and above. Review SQL server logs for "
            "unusual queries or command execution. Assess for new administrator accounts or "
            "scheduled tasks created during the vulnerability window."
        ),
        "banking_relevance": (
            "FortiClientEMS manages endpoint security clients across financial institution endpoints. "
            "Compromise of the management server enables attackers to push malicious configuration "
            "to all managed endpoints, disable security controls, or establish persistent access "
            "across the entire endpoint estate of a financial institution."
        ),
    },
    {
        "cve_id": "CVE-2024-1709",
        "date": "2024-02-21",
        "severity": "Critical",
        "cvss_score": 10.0,
        "system_affected": "ConnectWise ScreenConnect",
        "description": (
            "Authentication bypass vulnerability in ConnectWise ScreenConnect remote desktop and "
            "access software allowing unauthenticated attackers to bypass authentication and gain "
            "full control of systems. Chained with CVE-2024-1708 for remote code execution."
        ),
        "recommended_action": (
            "Update to ScreenConnect 23.9.8 or later immediately. Audit all recent remote sessions "
            "for unauthorised access. If compromise is suspected, isolate affected systems and conduct "
            "forensic investigation before reconnection to the network."
        ),
        "banking_relevance": (
            "ScreenConnect is used by IT support teams and managed service providers to access "
            "banking infrastructure remotely. Exploitation allows attackers to establish undetected "
            "remote access to financial institution endpoints and servers, bypassing traditional "
            "VPN and PAM controls. Ransomware groups rapidly weaponised this vulnerability against "
            "financial sector MSP clients."
        ),
    },
    {
        "cve_id": "CVE-2022-30190",
        "date": "2022-05-30",
        "severity": "High",
        "cvss_score": 7.8,
        "system_affected": "Microsoft Windows (Follina — MSDT)",
        "description": (
            "Remote code execution vulnerability in the Microsoft Support Diagnostic Tool (MSDT) "
            "triggered when Windows opens a specially crafted Microsoft Office document. "
            "No user interaction beyond opening the document required; macros do not need to be enabled."
        ),
        "recommended_action": (
            "Apply June 2022 Patch Tuesday update. As interim mitigation, disable MSDT URL protocol "
            "(reg delete HKEY_CLASSES_ROOT\\ms-msdt /f). Block delivery of Office documents from "
            "untrusted sources at email gateway. Train users to report unexpected document behaviour."
        ),
        "banking_relevance": (
            "Financial institutions routinely receive Office documents from clients, counterparties, "
            "and regulators. This vulnerability allows weaponised Word documents to execute code "
            "on the recipient's machine without any macro warning or special user action. "
            "Targeted phishing campaigns using Follina against banking staff were observed "
            "in multiple jurisdictions in H1 2022."
        ),
    },
    {
        "cve_id": "CVE-2023-23397",
        "date": "2023-03-14",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Microsoft Outlook",
        "description": (
            "Zero-click privilege escalation vulnerability in Microsoft Outlook triggered when Outlook "
            "receives and processes a specially crafted email — no user interaction required. "
            "Exploited by Russian APT28 (Fancy Bear) to steal NTLM hashes from European targets."
        ),
        "recommended_action": (
            "Apply March 2023 Patch Tuesday update immediately. Add well-known Microsoft accounts "
            "to the Protected Users Security Group. Block TCP 445 (SMB) at the perimeter to "
            "prevent outbound NTLM hash transmission. Monitor for NTLM authentication anomalies."
        ),
        "banking_relevance": (
            "Zero-click vulnerabilities in Outlook require no user action — receiving a malicious "
            "email is sufficient for compromise. APT28 exploited this against defence, energy, and "
            "financial sector organisations. NTLM hash theft enables lateral movement across banking "
            "networks using Pass-the-Hash attacks, bypassing multi-factor authentication in some configurations."
        ),
    },
    {
        "cve_id": "CVE-2022-3602",
        "date": "2022-11-01",
        "severity": "High",
        "cvss_score": 7.5,
        "system_affected": "OpenSSL 3.x (buffer overflow)",
        "description": (
            "Stack-based buffer overflow in OpenSSL 3.0.0 to 3.0.6 triggered during X.509 certificate "
            "verification. Exploitable when processing a specially crafted certificate chain, "
            "potentially allowing remote code execution. Initially rated Critical, downgraded to High "
            "following analysis of exploitation difficulty."
        ),
        "recommended_action": (
            "Upgrade to OpenSSL 3.0.7 or later on all systems using OpenSSL 3.x. Identify all "
            "applications and systems using OpenSSL 3.x via asset inventory. Prioritise internet-facing "
            "systems and those processing externally-provided certificates."
        ),
        "banking_relevance": (
            "OpenSSL underpins TLS encryption for virtually all internet-facing banking systems: "
            "online banking portals, APIs, SWIFT messaging, and interbank communications. "
            "The financial sector's wide adoption of TLS 1.3 (which requires OpenSSL 3.x) "
            "made this vulnerability particularly concerning. Financial institutions rushing to "
            "TLS 1.3 compliance were potentially exposing systems to this vulnerability."
        ),
    },
    {
        "cve_id": "CVE-2022-47966",
        "date": "2023-01-18",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Zoho ManageEngine (multiple products)",
        "description": (
            "Remote code execution vulnerability in multiple Zoho ManageEngine products via SAML "
            "authentication, allowing unauthenticated attackers to execute arbitrary code. Exploited "
            "by nation-state actors against critical infrastructure including financial services."
        ),
        "recommended_action": (
            "Upgrade all affected ManageEngine products to latest versions immediately. Review "
            "authentication logs for exploitation indicators (unusual SAML assertions, new admin "
            "accounts). Restrict ManageEngine administrative access to trusted internal networks."
        ),
        "banking_relevance": (
            "Zoho ManageEngine products (ServiceDesk, PAM360, ADManager) are widely deployed in "
            "financial institutions for IT service management, privileged access, and Active Directory "
            "management. Compromise of ManageEngine PAM360 specifically provides access to all "
            "managed privileged credentials — the keys to the entire banking IT infrastructure."
        ),
    },
    {
        "cve_id": "CVE-2023-44487",
        "date": "2023-10-10",
        "severity": "High",
        "cvss_score": 7.5,
        "system_affected": "HTTP/2 Protocol (Rapid Reset DDoS)",
        "description": (
            "HTTP/2 Rapid Reset Attack exploiting the stream cancellation feature to send a large "
            "number of HTTP/2 HEADERS followed by RST_STREAM frames, overwhelming web servers with "
            "unprecedented DDoS traffic. Attack volume of 398 million requests per second recorded."
        ),
        "recommended_action": (
            "Apply patches from web server vendors (nginx, Apache, IIS, H2O). Configure HTTP/2 "
            "connection limits and implement rate limiting at load balancers. Engage DDoS mitigation "
            "provider if not already in place; validate DDoS runbooks cover HTTP/2-based attacks."
        ),
        "banking_relevance": (
            "DDoS attacks targeting online banking portals, payment APIs, and trading platforms cause "
            "direct operational and reputational harm. The Rapid Reset technique defeated existing "
            "DDoS defences that were not prepared for HTTP/2-based floods. Financial institutions "
            "with high-traffic digital banking platforms were primary targets of campaigns "
            "following public disclosure of this technique."
        ),
    },
    {
        "cve_id": "CVE-2024-21893",
        "date": "2024-01-31",
        "severity": "High",
        "cvss_score": 8.2,
        "system_affected": "Ivanti Connect Secure and Policy Secure",
        "description": (
            "Server-side request forgery (SSRF) vulnerability in Ivanti Connect Secure and Policy "
            "Secure VPN appliances allowing authenticated attackers to access certain restricted "
            "resources. Chained with other Ivanti zero-days (CVE-2023-46805, CVE-2024-21887) for "
            "unauthenticated remote code execution. Exploited by Chinese APT groups."
        ),
        "recommended_action": (
            "Apply Ivanti patches as soon as available; perform factory reset before patching if "
            "compromise is suspected. Run Ivanti Integrity Checker Tool. Replace compromised "
            "device credentials and review all certificates issued through the compromised VPN. "
            "CISA advised agencies to disconnect affected Ivanti products pending patch availability."
        ),
        "banking_relevance": (
            "Ivanti Connect Secure is a major enterprise VPN solution at financial institutions. "
            "The combination of multiple zero-days exploited by Chinese APT (Volt Typhoon and UNC5221) "
            "in early 2024 caused CISA to issue emergency directives. Financial institutions using "
            "Ivanti VPN for staff and vendor remote access faced undetected compromise of their "
            "network perimeter by state-sponsored actors."
        ),
    },
    {
        "cve_id": "CVE-2023-35078",
        "date": "2023-07-24",
        "severity": "Critical",
        "cvss_score": 10.0,
        "system_affected": "Ivanti Endpoint Manager Mobile (EPMM / MobileIron Core)",
        "description": (
            "Authentication bypass vulnerability in Ivanti Endpoint Manager Mobile (formerly "
            "MobileIron Core) allowing unauthenticated remote attackers to access specific API "
            "endpoints and retrieve sensitive personal information including names, phone numbers, "
            "and mobile device details."
        ),
        "recommended_action": (
            "Apply Ivanti patch (11.10.0.2, 11.9.1.2, 11.8.1.2) immediately. Restrict EPMM admin "
            "portal access to trusted internal networks. Review API logs for unauthorised access. "
            "Norwegian government confirmed compromise of multiple ministries via this vulnerability."
        ),
        "banking_relevance": (
            "MobileIron/EPMM is deployed in financial institutions for mobile device management "
            "of staff smartphones and tablets, including those used for banking authentication "
            "apps and email. Compromise exposes mobile device inventory, user directories, and "
            "potentially mobile application configuration data used in digital banking."
        ),
    },
    {
        "cve_id": "CVE-2022-21587",
        "date": "2022-10-18",
        "severity": "Critical",
        "cvss_score": 9.8,
        "system_affected": "Oracle E-Business Suite (EBS)",
        "description": (
            "Remote code execution vulnerability in Oracle E-Business Suite allowing unauthenticated "
            "network access to execute arbitrary code on servers running Oracle EBS. Affects "
            "Oracle Web Applications Desktop Integrator (ADI) component in EBS versions 12.2."
        ),
        "recommended_action": (
            "Apply Oracle Critical Patch Update October 2022 immediately. Assess network exposure "
            "of Oracle EBS to untrusted networks. Review EBS system logs for unusual web service "
            "calls or newly created database accounts during the vulnerability window."
        ),
        "banking_relevance": (
            "Oracle E-Business Suite is used in financial institutions for general ledger, accounts "
            "payable, procurement, and human resources. Compromise of EBS provides access to "
            "financial records, payment processing configurations, and employee data. "
            "Banks using Oracle EBS for financial close and regulatory reporting face "
            "data integrity risk if EBS is compromised."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 5. PUBLIC_AUDIT_RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════════

PUBLIC_AUDIT_RECOMMENDATIONS = [

    # ── AML / KYC ──────────────────────────────────────────────────────────────
    {
        "source": "FATF",
        "year": "2023",
        "theme": "AML_KYC",
        "recommendation": (
            "Private banks must apply enhanced due diligence for all HNWI clients and implement "
            "proportionate verification — not merely declaration — of source of wealth. Documentation "
            "must be substantiated by independent evidence, not solely client-provided statements."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Directly applicable: FATF's 2023 guidance specifically targets private banking. "
            "Swiss, Singapore, and Hong Kong private banks are primary implementation targets."
        ),
    },
    {
        "source": "FATF",
        "year": "2023",
        "theme": "AML_KYC",
        "recommendation": (
            "Complex ownership structures used by HNWI clients — trusts, foundations, holding companies, "
            "and SPVs across multiple jurisdictions — must be analysed to identify the ultimate beneficial "
            "owner. Look-through must be applied regardless of the number of intermediary layers."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Fundamental requirement for private banks serving international HNWI clients. "
            "Manual look-through for multi-layer structures is frequently cited as inadequate by FATF."
        ),
    },
    {
        "source": "FATF",
        "year": "2022",
        "theme": "AML_KYC",
        "recommendation": (
            "Transaction monitoring systems must be regularly tuned and back-tested against known "
            "typologies. Alert thresholds must be calibrated to the risk profile of individual clients, "
            "not applied as a single universal threshold across the entire customer base."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Critical for private banks where HNWI transaction patterns differ significantly from retail. "
            "Universal thresholds create both excessive false positives and genuine detection gaps."
        ),
    },
    {
        "source": "FINMA",
        "year": "2023",
        "theme": "AML_KYC",
        "recommendation": (
            "Swiss banks must maintain a complete and current register of beneficial owners. "
            "FINMA enforcement reviews in 2023 found that Form A documentation was incomplete or "
            "outdated for a significant proportion of client relationships at several private banks."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Enforcement finding directly applicable to Swiss private banks. Form A compliance "
            "is a FINMA supervisory priority and key indicator in the annual audit."
        ),
    },
    {
        "source": "MAS",
        "year": "2022",
        "theme": "AML_KYC",
        "recommendation": (
            "Financial institutions should not rely exclusively on client declarations for PEP "
            "identification. Automated screening tools must be supplemented by RM-level intelligence "
            "and regular database updates. Domestic PEPs present a particular identification challenge "
            "requiring explicit procedural controls."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "MAS thematic inspection findings (2022) across private banks in Singapore. "
            "Domestic PEP identification failures were the most frequently cited AML weakness."
        ),
    },
    {
        "source": "FCA",
        "year": "2022",
        "theme": "AML_KYC",
        "recommendation": (
            "Banks must implement a risk-based approach to periodic review that ensures high-risk "
            "clients are reviewed at least annually. Reviews must be substantive — confirming continued "
            "KYC adequacy and re-assessing risk ratings — not merely administrative date-stamps."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FCA's Financial Crime Guide update (2022) specifically addressed private banking periodic "
            "review backlogs identified during supervisory visits."
        ),
    },
    {
        "source": "EBA",
        "year": "2022",
        "theme": "AML_KYC",
        "recommendation": (
            "AML/CFT compliance functions must be adequately staffed and resourced relative to the "
            "institution's risk profile. The ratio of compliance officers to total client-facing staff "
            "should be reviewed annually against the volume and complexity of relationships managed."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "EBA opinion on ML/TF risks highlighted systematic under-resourcing of AML compliance "
            "at mid-sized private banks as a key vulnerability."
        ),
    },
    {
        "source": "Basel Committee",
        "year": "2021",
        "theme": "AML_KYC",
        "recommendation": (
            "Correspondent banking relationships require a graduated due diligence approach. "
            "Shell bank relationships must be prohibited in policy and actively screened for "
            "in the onboarding and review processes for all respondent institutions."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "Relevant for Swiss and Bahamas private banks maintaining correspondent relationships "
            "to facilitate cross-border HNWI transactions in lower-regulation jurisdictions."
        ),
    },

    # ── CYBER RISK ─────────────────────────────────────────────────────────────
    {
        "source": "EBA",
        "year": "2023",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Financial institutions must implement DORA-aligned ICT risk management frameworks by "
            "January 2025. Boards and senior management must be able to demonstrate accountability "
            "for ICT risk and understanding of digital resilience obligations."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Mandatory for all EU financial entities. Swiss and UK private banks with EU operations "
            "face equivalent requirements. Board training on DORA obligations is specifically required."
        ),
    },
    {
        "source": "MAS",
        "year": "2023",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Cyber incident reporting capabilities must be capable of detecting and reporting "
            "significant incidents within 1 hour of detection. Financial institutions should conduct "
            "annual end-to-end testing of their cyber incident response and reporting pipelines "
            "to validate the 1-hour MAS reporting requirement."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "MAS TRM 2021 guidance. Banks relying on MSSPs for SOC services must contractually "
            "require 1-hour notification to enable compliance with MAS reporting timelines."
        ),
    },
    {
        "source": "HKMA",
        "year": "2023",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Authorised institutions should adopt a zero-trust architecture approach for network "
            "access, moving away from perimeter-based security models. All access requests must "
            "be authenticated, authorised, and continuously validated regardless of network location."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "HKMA CRAF 2021 recommendation. Remote working patterns post-COVID make perimeter "
            "security insufficient for private banks with distributed RM and client service models."
        ),
    },
    {
        "source": "FSB",
        "year": "2023",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Financial institutions should participate in sector-wide cyber threat intelligence "
            "sharing frameworks. Real-time threat intelligence reduces mean time to detect and "
            "enables pre-emptive defensive action for threats already observed in the sector."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "FS-ISAC membership and participation in HKMA CISP and MAS information sharing "
            "platforms provides private banks with early warning of sector-specific threats."
        ),
    },
    {
        "source": "FINMA",
        "year": "2023",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Banks must maintain a tested capability to restore critical systems from immutable "
            "backups within their defined RTO. Backup restoration must be tested end-to-end "
            "at least annually. Backups must be immutable and logically isolated from production."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FINMA risk monitor 2023 identified untested BCPs and non-isolated backups as "
            "significant vulnerabilities at Swiss financial institutions following ransomware incidents."
        ),
    },
    {
        "source": "FCA",
        "year": "2023",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Firms must assess and test their operational resilience against severe but plausible "
            "cyber attack scenarios, not merely technical failure. Impact tolerance testing must "
            "include scenarios where recovery systems themselves are compromised."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FCA PS21/3 compliance (March 2025 deadline). Private banks must demonstrate they "
            "remain within impact tolerances even in scenarios where cyber attacks target recovery "
            "infrastructure."
        ),
    },
    {
        "source": "Basel Committee",
        "year": "2021",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Third-party technology providers must be subject to cyber risk assessment throughout "
            "the vendor lifecycle — not only at onboarding. Banks must conduct ongoing monitoring "
            "of vendor security posture and require immediate notification of vendor-side incidents."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Highly relevant for private banks with extensive fintech and cloud vendor ecosystems. "
            "SolarWinds and MOVEit incidents demonstrated that single vendor breaches can cascade "
            "across hundreds of financial institutions."
        ),
    },
    {
        "source": "IIA",
        "year": "2022",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Internal audit should conduct annual assessments of the cyber risk management framework, "
            "including validation of SIEM coverage, privileged access controls, and patch management "
            "compliance. Technical cyber audit capability — including certified staff (CISA, CISSP) — "
            "must be available within or accessible to the internal audit function."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "IIA Global Technology Audit Guide. Many private banks rely on external co-sourcing "
            "for cyber audit capability — the independence and depth of such arrangements must "
            "be assessed."
        ),
    },

    # ── CREDIT RISK ────────────────────────────────────────────────────────────
    {
        "source": "Basel Committee",
        "year": "2023",
        "theme": "CREDIT_RISK",
        "recommendation": (
            "Banks using internal ratings-based approaches must validate their PD, LGD, and EAD "
            "models at least annually. Model performance during the 2022-2023 stress period must "
            "be reviewed; models that underperformed must be recalibrated before continued use."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Banks using IRBA for Lombard lending or real estate must validate models post-rate "
            "shock. CRR III output floor (2025) requires banks to compare internal model RWAs "
            "against standardised approach RWAs."
        ),
    },
    {
        "source": "FINMA",
        "year": "2023",
        "theme": "CREDIT_RISK",
        "recommendation": (
            "Swiss banks must review Lombard lending exposures for concentration risk following "
            "the 2022 market correction. Stress test scenarios must be updated to reflect rapid "
            "rate rises and equity market corrections of 30-40% in key markets."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Explicit FINMA 2023 supervisory priority. Private banks with large Lombard books "
            "were specifically reviewed for concentration risk and margin call process adequacy."
        ),
    },
    {
        "source": "EBA",
        "year": "2023",
        "theme": "CREDIT_RISK",
        "recommendation": (
            "IFRS 9 staging criteria and provisioning models must reflect forward-looking information "
            "current as of the reporting date. Banks must not apply 2021 macroeconomic scenarios in "
            "2023 provisions; rapid rate rises and commercial real estate corrections must be "
            "incorporated into ECL calculations."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "EBA supervisory convergence report 2023. Private banks with real estate and CRE "
            "exposures face the largest provisioning adjustments given CRE market corrections "
            "in CH, UK, and SG."
        ),
    },
    {
        "source": "IMF",
        "year": "2023",
        "theme": "CREDIT_RISK",
        "recommendation": (
            "Financial sector assessments have identified credit concentration risk in private "
            "banking as a systemic vulnerability. Banks should maintain concentration limits "
            "at the single-name, sector, and geographic levels and test these limits under "
            "correlated stress scenarios."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "IMF FSAP recommendations for Switzerland (2023) highlighted Lombard lending "
            "concentration as a key private banking risk requiring enhanced supervisory attention."
        ),
    },
    {
        "source": "FCA",
        "year": "2022",
        "theme": "CREDIT_RISK",
        "recommendation": (
            "Firms offering Lombard and securities-backed lending must ensure that margin call "
            "processes are clearly documented, tested under stress, and capable of execution "
            "within defined timeframes. Clients must be informed of margin call procedures "
            "at inception of the facility."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "FCA portfolio letter to wealth managers (2022). UK private banks must demonstrate "
            "that margin call processes have been tested under the 2022 market stress scenario."
        ),
    },

    # ── OPERATIONAL RISK ───────────────────────────────────────────────────────
    {
        "source": "EBA",
        "year": "2023",
        "theme": "OPERATIONAL_RISK",
        "recommendation": (
            "Operational risk frameworks must be updated to reflect DORA requirements. The ICT "
            "risk management framework required by DORA Article 6 must be integrated into the "
            "broader operational risk governance structure, not maintained as a separate parallel "
            "framework."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Mandatory DORA compliance by January 2025. Private banks with EU operations must "
            "integrate ICT risk management into their existing operational risk governance."
        ),
    },
    {
        "source": "Basel Committee",
        "year": "2021",
        "theme": "OPERATIONAL_RISK",
        "recommendation": (
            "Banks must maintain a comprehensive operational loss data collection process. "
            "Internal loss data, external loss data from industry databases, and scenario analysis "
            "must be combined to produce a complete picture of operational risk exposure. "
            "Near-miss capture is essential and must be incentivised culturally."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "BCBS operational risk principles directly applicable. Near-miss culture in private "
            "banking is particularly weak given the relationship-driven, high-discretion environment."
        ),
    },
    {
        "source": "FINMA",
        "year": "2022",
        "theme": "OPERATIONAL_RISK",
        "recommendation": (
            "Banks must conduct a formal business impact analysis annually to identify critical "
            "processes, maximum tolerable downtime, and key person dependencies. BIA findings "
            "must be reflected in tested BCP and, where key persons are identified, in documented "
            "succession and knowledge transfer plans."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FINMA circular on operational risk management. Swiss private banks with high "
            "concentration of AUM in a small number of senior RMs face acute key person risk."
        ),
    },
    {
        "source": "MAS",
        "year": "2022",
        "theme": "OPERATIONAL_RISK",
        "recommendation": (
            "Outsourcing oversight must include regular on-site or equivalent reviews of critical "
            "service providers. Monitoring of contractual SLAs alone is insufficient; independent "
            "assessment of the vendor's risk management and operational quality must be conducted."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "MAS Notice on Outsourcing (2022 update). Singapore private banks must demonstrate "
            "active oversight of custodian, fund administrator, and IT service provider arrangements."
        ),
    },
    {
        "source": "IIA",
        "year": "2023",
        "theme": "OPERATIONAL_RISK",
        "recommendation": (
            "Internal audit must assess the quality and independence of the RCSA process, not "
            "merely the outputs. Where RCSAs are business-led and unvalidated, internal audit "
            "must challenge the risk ratings through independent testing and external benchmarking."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "IIA Practice Guide on RCSA auditing. Particularly relevant for private banks where "
            "operational risk function is small and RCSA may be driven by business lines."
        ),
    },
    {
        "source": "FSB",
        "year": "2022",
        "theme": "OPERATIONAL_RISK",
        "recommendation": (
            "Financial institutions must develop and maintain exit strategies for all critical "
            "outsourcing arrangements. Exit strategies must be tested through dry-run exercises "
            "to validate feasibility; theoretical exit plans that have never been assessed for "
            "practical executability are insufficient."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FSB discussion paper on outsourcing and third-party risk (2022). Exit strategy "
            "for core banking platform is the most challenging requirement for private banks."
        ),
    },

    # ── DATA PRIVACY ───────────────────────────────────────────────────────────
    {
        "source": "EDPB",
        "year": "2023",
        "theme": "DATA_PRIVACY",
        "recommendation": (
            "Controllers must conduct transfer impact assessments for all data exports to third "
            "countries, even where SCCs are in place. The assessment must evaluate local law in "
            "the destination country and whether it impairs the effectiveness of the SCC safeguards."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Mandatory post-Schrems II. Private banks transferring client data to Singapore, "
            "Hong Kong, and US service providers must maintain documented transfer impact assessments."
        ),
    },
    {
        "source": "ICO",
        "year": "2023",
        "theme": "DATA_PRIVACY",
        "recommendation": (
            "Data Protection Impact Assessments must be conducted before implementing any new "
            "processing activity that is likely to result in high risk, including automated client "
            "profiling, large-scale processing of financial data, and new customer analytics tools."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "ICO guidance on DPIA requirements. Private banks adopting AI/ML for client "
            "investment profiling or fraud detection must complete DPIAs before deployment."
        ),
    },
    {
        "source": "FDPIC",
        "year": "2023",
        "theme": "DATA_PRIVACY",
        "recommendation": (
            "Under the revised nDSG effective September 2023, Swiss organisations must update "
            "their privacy notices, review processing activities for compliance, and implement "
            "DPIA processes. Existing consent mechanisms must be reviewed for alignment with "
            "the heightened nDSG requirements."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Mandatory for all Swiss private banks from September 2023. FDPIC has indicated "
            "that financial institutions processing HNWI data are a priority supervision category."
        ),
    },
    {
        "source": "EBA",
        "year": "2022",
        "theme": "DATA_PRIVACY",
        "recommendation": (
            "Financial institutions must operationalise data subject rights — particularly the "
            "right of access (DSAR) and the right to erasure. Manual, fragmented processes "
            "that cannot meet the 30-day response deadline must be replaced by systematic, "
            "documented workflows with ownership assigned at function level."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "Private banks holding extensive HNWI personal and financial data across legacy "
            "systems face significant challenges in executing DSARs and erasure requests "
            "within regulatory timelines."
        ),
    },
    {
        "source": "IMF",
        "year": "2022",
        "theme": "DATA_PRIVACY",
        "recommendation": (
            "Financial regulators and data protection authorities must coordinate their supervision "
            "of data privacy at financial institutions. Institutions should proactively engage with "
            "both regulatory frameworks and ensure that data protection obligations are integrated "
            "into the overall compliance framework."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "Relevant for private banks managing dual compliance obligations under banking "
            "regulators (FINMA, MAS) and data protection authorities (FDPIC, PDPC, ICO)."
        ),
    },

    # ── MARKET RISK ────────────────────────────────────────────────────────────
    {
        "source": "Basel Committee",
        "year": "2023",
        "theme": "MARKET_RISK",
        "recommendation": (
            "Banks must prepare for Fundamental Review of the Trading Book (FRTB) implementation "
            "under CRR III/CRD VI. Impact assessments on capital requirements must be completed "
            "and strategic decisions on standardised vs. internal model approach finalised. "
            "Data infrastructure for FRTB must be in place before the 2025 go-live date."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FRTB applies to banks with trading books above EUR 500m notional (EUR 1bn for SA-only). "
            "Swiss and UK private banks with active trading desks must assess FRTB impact on capital."
        ),
    },
    {
        "source": "FINMA",
        "year": "2023",
        "theme": "MARKET_RISK",
        "recommendation": (
            "Banks must update IRRBB stress scenarios to reflect the rate environment experienced "
            "in 2022-2023. Behavioural assumptions for non-maturity deposits must be recalibrated; "
            "deposit repricing betas derived from the 2010-2021 low-rate era are no longer valid."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FINMA risk monitor 2023. Swiss private banks with significant client cash balances "
            "face materially different IRRBB profiles than assumed by pre-2022 models."
        ),
    },
    {
        "source": "EBA",
        "year": "2022",
        "theme": "MARKET_RISK",
        "recommendation": (
            "VaR model backtesting results showing multiple exceptions must trigger formal model "
            "review rather than simply capital add-ons. Model limitations must be disclosed in "
            "Pillar 3 reports. Banks should migrate to Expected Shortfall measures alongside VaR."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "EBA guidelines on market risk model performance following 2022 volatility. "
            "Private banks relying on simple parametric VaR models face the highest model risk."
        ),
    },

    # ── THIRD PARTY RISK ───────────────────────────────────────────────────────
    {
        "source": "EBA",
        "year": "2023",
        "theme": "THIRD_PARTY_RISK",
        "recommendation": (
            "Financial institutions must maintain a complete register of all ICT third-party "
            "arrangements as required by DORA Article 28. The register must be reported to the "
            "competent authority on an annual basis and must identify all critical and important "
            "function providers."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "DORA mandate effective January 2025. Private banks with EU operations must build "
            "or update their vendor registers to meet the DORA Article 28 reporting standard."
        ),
    },
    {
        "source": "PRA",
        "year": "2021",
        "theme": "THIRD_PARTY_RISK",
        "recommendation": (
            "Material outsourcing arrangements must not only be notified to the PRA but must "
            "be actively managed with evidence of ongoing oversight. Firms must be able to "
            "demonstrate that they understand the risks inherent in their outsourcing arrangements "
            "and that contracts provide adequate protections."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "PRA SS2/21. UK private banks with extensive custody, IT, and back-office outsourcing "
            "must demonstrate active management, not merely contract execution."
        ),
    },
    {
        "source": "FINMA",
        "year": "2022",
        "theme": "THIRD_PARTY_RISK",
        "recommendation": (
            "Swiss banks outsourcing to non-Swiss entities must assess the legal and regulatory "
            "risks in the provider's jurisdiction, including data access by foreign authorities, "
            "and document compensating measures where Swiss banking secrecy could be compromised."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FINMA-RS 2018/3 implementation guidance. Swiss private banks using US cloud providers "
            "must address CLOUD Act risks and document their assessment of Swiss secrecy exposure."
        ),
    },
    {
        "source": "FSB",
        "year": "2023",
        "theme": "THIRD_PARTY_RISK",
        "recommendation": (
            "Regulators and financial institutions should develop standardised metrics to measure "
            "third-party concentration risk. Banks should regularly report their critical third-party "
            "dependencies to boards and regulators, including the percentage of critical functions "
            "delivered by each top-five provider."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "FSB report on financial stability implications of third-party dependencies (2023). "
            "Private banks relying on a single core banking vendor (e.g. Avaloq, Temenos) for "
            "all front-to-back operations represent the extreme concentration risk case."
        ),
    },

    # ── GOVERNANCE ─────────────────────────────────────────────────────────────
    {
        "source": "Basel Committee",
        "year": "2023",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Boards must receive risk reports that are sufficiently granular, timely, and accurate "
            "to enable effective oversight. The quality and adequacy of management information "
            "provided to the Board must itself be assessed in the ICAAP and SREP process."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "BCBS corporate governance principles for banks (2015, updated 2023). The Credit "
            "Suisse collapse renewed focus on whether boards received adequate, accurate risk "
            "information — directly relevant for Swiss private bank boards."
        ),
    },
    {
        "source": "FINMA",
        "year": "2023",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Following the Credit Suisse resolution, FINMA has signalled that governance and "
            "accountability requirements will be tightened across the Swiss banking sector. "
            "Private banks should proactively review board composition, senior management "
            "accountability frameworks, and risk culture."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Direct FINMA supervisory signal post-Credit Suisse. Governance is the single highest "
            "priority area for FINMA supervision in 2024-2025 across the Swiss banking sector."
        ),
    },
    {
        "source": "IIA",
        "year": "2024",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Under the 2024 Global Internal Audit Standards, internal audit functions must have "
            "a formally documented and Board-approved internal audit charter. The chief audit "
            "executive must report functionally to the Audit Committee and have unfettered access "
            "to all people, records, and properties relevant to engagements."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Mandatory under IIA Standards 2024. Private banks where the head of internal audit "
            "reports to the CEO rather than the Audit Committee are in breach of these standards."
        ),
    },
    {
        "source": "FCA",
        "year": "2023",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Under SMCR, firms must ensure that senior management functions are appropriately "
            "staffed with individuals who can demonstrate accountability for their allocated "
            "responsibilities. Responsibility maps must be kept current and reflect actual "
            "decision-making authority."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FCA SMCR in-scope private banks must review responsibility maps annually. "
            "Gaps between stated responsibility and actual authority are a primary FCA "
            "enforcement trigger."
        ),
    },
    {
        "source": "MAS",
        "year": "2022",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Risk appetite statements must be cascaded into business-unit-level limits and KRIs "
            "that are monitored and reported to risk committees regularly. A Board-level risk "
            "appetite statement that is not operationalised at the business unit level does not "
            "constitute effective risk governance."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "MAS thematic review findings on risk governance at Singapore banks (2022). "
            "Specifically highlighted that private banking risk appetite was frequently stated "
            "at enterprise level without meaningful cascade to portfolio or RM level."
        ),
    },
    {
        "source": "IMF",
        "year": "2023",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Financial Sector Assessment Programs have consistently identified weaknesses in the "
            "independence of internal audit and compliance at smaller financial institutions. "
            "Supervisory authorities should require a minimum level of independence for these "
            "functions regardless of firm size."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "IMF FSAP finding applicable across all jurisdictions. Smaller private banks must "
            "ensure that cost-efficiency measures do not compromise the functional independence "
            "of their second and third lines of defence."
        ),
    },
    {
        "source": "EBA",
        "year": "2022",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Remuneration policies must ensure that variable compensation is genuinely risk-adjusted "
            "and incorporates non-financial performance indicators including compliance, conduct, "
            "and risk management behaviour. Clawback provisions must be enforceable and applied "
            "in practice."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "EBA guidelines on sound remuneration (2022). Private banking RM compensation models "
            "driven purely by AUM and revenue growth create structural incentives misaligned "
            "with risk management and client interests."
        ),
    },
    {
        "source": "Basel Committee",
        "year": "2021",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Banks must implement a robust whistleblowing framework that enables staff to raise "
            "concerns without fear of retaliation. The effectiveness of whistleblowing mechanisms "
            "should be monitored through participation rates and benchmarked against peer institutions."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "BCBS corporate governance principles. Low whistleblowing report volumes in private "
            "banking — given the close-knit, relationship-driven culture — require careful "
            "assessment of channel accessibility and perceived safety."
        ),
    },

    # ── ESG / CLIMATE ──────────────────────────────────────────────────────────
    {
        "source": "FINMA",
        "year": "2023",
        "theme": "ESG",
        "recommendation": (
            "Systemically important banks must integrate climate and nature-related financial risks "
            "into their risk management frameworks in accordance with FINMA-RS 2023/1. Climate "
            "scenario analysis must be conducted annually and results disclosed under TCFD. "
            "Physical and transition risk must be assessed at portfolio level."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "FINMA RS 2023/1 applicable to SIBs immediately; proportional application expected "
            "for other banks. Private banks with large real estate and commodity-linked portfolios "
            "face material transition and physical risk exposures."
        ),
    },
    {
        "source": "EBA",
        "year": "2023",
        "theme": "ESG",
        "recommendation": (
            "ESG risks must be integrated into the Internal Capital Adequacy Assessment Process "
            "(ICAAP) and Pillar 2 assessments. Banks cannot treat ESG risks as a separate parallel "
            "framework; they must be embedded in credit, market, and operational risk methodologies."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "EBA discussion paper on ESG risk management (2022/2023). Swiss and EU private banks "
            "must demonstrate that green bond holdings, ESG advisory mandates, and sustainable "
            "investment products are subject to adequate risk assessment."
        ),
    },
    {
        "source": "MAS",
        "year": "2022",
        "theme": "ESG",
        "recommendation": (
            "Financial institutions in Singapore should implement TCFD-aligned disclosures and "
            "develop internal capabilities for climate risk assessment. MAS has signalled that "
            "mandatory climate disclosures for financial institutions will be phased in from 2024."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "MAS Environmental Risk Management Guidelines (2020, updated 2022). Singapore "
            "private banks managing ESG-labelled mandates must ensure product claims are "
            "substantiated by underlying risk analysis."
        ),
    },

    # ── ADDITIONAL — Big4 Public Thought Leadership ────────────────────────────
    {
        "source": "Deloitte (public)",
        "year": "2023",
        "theme": "CYBER_RISK",
        "recommendation": (
            "Financial institutions should adopt an 'assume breach' mentality, focusing investment "
            "on detection and response capabilities rather than purely on prevention. Mean time to "
            "detect (MTTD) and mean time to respond (MTTR) are the primary metrics that correlate "
            "with breach impact limitation."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Deloitte Global Financial Services Cyber Risk Report 2023. Particularly relevant "
            "for private banks where prevention-focused security investments dominate but "
            "detection capabilities lag industry benchmarks."
        ),
    },
    {
        "source": "PwC (public)",
        "year": "2023",
        "theme": "GOVERNANCE",
        "recommendation": (
            "The three lines of defence model requires updating to reflect modern risk frameworks. "
            "The 2LoD role should shift from pure oversight to collaborative risk partnership with "
            "the business, while maintaining the independence required for credible challenge. "
            "Internal audit should focus on systemic risks rather than transactional compliance."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "PwC Global Internal Audit Study 2023. Private banks with small 2LoD teams must "
            "prioritise where collaborative risk partnership adds most value — typically "
            "in new product approval, strategic transactions, and regulatory change."
        ),
    },
    {
        "source": "KPMG (public)",
        "year": "2023",
        "theme": "AML_KYC",
        "recommendation": (
            "Financial institutions should evaluate AI/ML-based transaction monitoring solutions "
            "to supplement rules-based systems. Hybrid approaches — combining rules for regulatory "
            "typologies with ML for anomaly detection — materially reduce false positive rates "
            "while improving suspicious activity detection."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "KPMG AML survey 2023. Private banks with relatively small transaction volumes may "
            "find ML-based monitoring more accessible and cost-effective than large-scale "
            "enterprise TM platforms."
        ),
    },
    {
        "source": "EY (public)",
        "year": "2023",
        "theme": "THIRD_PARTY_RISK",
        "recommendation": (
            "Organisations should develop a 'fourth-party risk management' capability to understand "
            "and monitor risks embedded in the supply chains of their critical third-party providers. "
            "Annual disclosure from critical vendors of their material sub-processors should be "
            "a contractual requirement."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "EY Third-Party Risk Management Survey 2023. Financial institutions using cloud-hosted "
            "fintech solutions must understand the sub-processor dependency chain that underpins "
            "their vendor's service delivery."
        ),
    },
    {
        "source": "Deloitte (public)",
        "year": "2022",
        "theme": "OPERATIONAL_RISK",
        "recommendation": (
            "Operational resilience programmes must move beyond compliance with regulatory "
            "requirements to genuinely test the ability to serve clients under stress. "
            "Scenario testing should include multi-hazard events — simultaneous cyber attack "
            "and key person unavailability — that test organisational resilience holistically."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "Deloitte Operational Resilience for Financial Services 2022. Private banks testing "
            "only physical disruption scenarios are likely unprepared for cyber-driven disruptions "
            "that affect systems, people, and vendors simultaneously."
        ),
    },
    {
        "source": "PwC (public)",
        "year": "2022",
        "theme": "CREDIT_RISK",
        "recommendation": (
            "Stress testing frameworks must be updated to reflect the new macroeconomic paradigm "
            "of higher rates, elevated inflation, and geopolitical fragmentation. Scenarios designed "
            "in 2015-2021 for a low-rate, high-growth environment no longer represent plausible "
            "severe but plausible adverse scenarios."
        ),
        "priority": "High",
        "private_banking_relevance": (
            "PwC Banking Perspectives 2022. Lombard lending stress tests that assume only mild "
            "equity corrections are no longer adequate. Private banks must test -40% equity and "
            "+400bp rate scenarios simultaneously."
        ),
    },
    {
        "source": "KPMG (public)",
        "year": "2022",
        "theme": "DATA_PRIVACY",
        "recommendation": (
            "Data lineage and inventory tools should be implemented to provide a complete and "
            "queryable map of personal data flows. Organisations that cannot locate all personal "
            "data cannot fulfil GDPR/nDSG rights obligations — notably erasure and portability — "
            "within statutory timelines."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "KPMG GDPR Health Check 2022. Private banks with 15-30 year old core banking systems "
            "and multiple data warehouses face significant data lineage challenges that expose "
            "them to regulatory risk for DSAR and erasure requests."
        ),
    },
    {
        "source": "EY (public)",
        "year": "2024",
        "theme": "GOVERNANCE",
        "recommendation": (
            "Boards should conduct periodic deep-dives on emerging risks including AI governance, "
            "quantum computing threats to encryption, and geopolitical risk. Board minutes should "
            "reflect substantive deliberation on emerging risks — not merely receipt of management "
            "presentations."
        ),
        "priority": "Medium",
        "private_banking_relevance": (
            "EY Board Effectiveness Survey 2024. AI adoption in private banking — for client "
            "profiling, trade recommendations, and compliance monitoring — requires explicit "
            "board-level AI governance that many private bank boards have not yet established."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 6. DATA_ANALYTICS_SCENARIOS
# ═══════════════════════════════════════════════════════════════════════════════

DATA_ANALYTICS_SCENARIOS = {

    "AML_KYC": [
        {
            "id": "DA001",
            "theme": "AML_KYC",
            "title": "Structuring / Smurfing Detection",
            "objective": "Detect transactions deliberately structured below reporting thresholds to avoid detection.",
            "data_sources": ["Core banking transaction ledger", "Wire transfer logs", "Cash transaction records"],
            "analysis_type": "Threshold",
            "anomaly_searched": "Multiple transactions just below CHF/SGD/HKD 10,000 reporting threshold by same client or group of related clients within a short time window.",
            "tools": ["SQL", "Python"],
            "complexity": "Medium",
        },
        {
            "id": "DA002",
            "theme": "AML_KYC",
            "title": "Round-Trip Transaction Detection",
            "objective": "Identify funds that leave and re-enter the bank within a short period, potentially indicating circular flow to disguise origin.",
            "data_sources": ["Wire transfer logs", "Correspondent bank transaction records", "Client account ledger"],
            "analysis_type": "Network",
            "anomaly_searched": "Funds transferred out and back to the same or related accounts within 30 days, particularly across jurisdictions.",
            "tools": ["Python", "SQL"],
            "complexity": "High",
        },
        {
            "id": "DA003",
            "theme": "AML_KYC",
            "title": "Dormant Account Activation",
            "objective": "Identify accounts that become suddenly active after extended dormancy with high-value or unusual transactions.",
            "data_sources": ["Account activity logs", "Transaction records", "Client onboarding date records"],
            "analysis_type": "Anomaly",
            "anomaly_searched": "Accounts with no transactions for >12 months that suddenly receive or send transfers above CHF 100,000 without prior client contact.",
            "tools": ["SQL", "Excel"],
            "complexity": "Low",
        },
        {
            "id": "DA004",
            "theme": "AML_KYC",
            "title": "Geographic Transaction Inconsistency",
            "objective": "Flag transactions to or from jurisdictions inconsistent with the client's declared source of wealth, residence, or business profile.",
            "data_sources": ["Wire transfer records", "Client KYC profile", "FATF risk country lists"],
            "analysis_type": "Anomaly",
            "anomaly_searched": "Transfers to/from FATF grey or black-listed jurisdictions, or jurisdictions not mentioned in client KYC documentation.",
            "tools": ["Python", "SQL"],
            "complexity": "Medium",
        },
        {
            "id": "DA005",
            "theme": "AML_KYC",
            "title": "PEP Portfolio Monitoring",
            "objective": "Monitor all transactions and portfolio changes for PEP-classified clients to detect unusual activity requiring EDD review.",
            "data_sources": ["PEP flag register", "Account transaction history", "Trade execution records", "Wire transfer logs"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Transactions exceeding 200% of the prior 12-month average for PEP clients; large incoming transfers without identified source.",
            "tools": ["SQL", "Python", "Tableau"],
            "complexity": "Medium",
        },
        {
            "id": "DA006",
            "theme": "AML_KYC",
            "title": "STR Filing Rate Analysis",
            "objective": "Analyse the rate and quality of STR/SAR filings relative to transaction volumes, risk profile, and peer benchmarks.",
            "data_sources": ["STR/SAR register", "Transaction monitoring alert log", "Client risk ratings", "Transaction volumes"],
            "analysis_type": "Statistical",
            "anomaly_searched": "STR filing rate disproportionately low vs. high-risk client proportion; jurisdictions with zero STRs in >12 months.",
            "tools": ["Excel", "Python"],
            "complexity": "Low",
        },
        {
            "id": "DA007",
            "theme": "AML_KYC",
            "title": "Beneficial Ownership Completeness",
            "objective": "Identify client accounts where UBO documentation is missing, outdated, or flagged as incomplete in the CRM/onboarding system.",
            "data_sources": ["CRM system", "KYC document repository", "Client onboarding records", "Periodic review logs"],
            "analysis_type": "Aging",
            "anomaly_searched": "Accounts with missing UBO form, Form A not signed, or UBO last verified >2 years ago — particularly for high-risk or trust/foundation structures.",
            "tools": ["SQL", "Excel"],
            "complexity": "Low",
        },
    ],

    "CYBER_RISK": [
        {
            "id": "DA008",
            "theme": "CYBER_RISK",
            "title": "Privileged Account Usage Outside Business Hours",
            "objective": "Detect privileged account logons and activity outside normal business hours that may indicate insider threat or credential compromise.",
            "data_sources": ["Active Directory / LDAP logs", "PAM solution session logs", "SIEM event data"],
            "analysis_type": "Anomaly",
            "anomaly_searched": "Privileged account logons between 22:00-06:00 local time or on weekends; admin actions on production systems outside change windows.",
            "tools": ["Python", "SQL"],
            "complexity": "Medium",
        },
        {
            "id": "DA009",
            "theme": "CYBER_RISK",
            "title": "Patch Compliance Dashboard",
            "objective": "Measure and report the proportion of systems with outstanding critical and high-severity patches beyond the defined SLA.",
            "data_sources": ["Vulnerability management platform (Qualys, Tenable, Rapid7)", "CMDB asset register", "Patch deployment logs"],
            "analysis_type": "Aging",
            "anomaly_searched": "Systems with critical patches outstanding >15 days or high patches >30 days; EOL systems with no compensating control documented.",
            "tools": ["Python", "Tableau", "SQL"],
            "complexity": "Low",
        },
        {
            "id": "DA010",
            "theme": "CYBER_RISK",
            "title": "Failed Authentication Spike Detection",
            "objective": "Identify potential brute-force attacks, credential stuffing, or account takeover attempts via anomalous failed logon patterns.",
            "data_sources": ["Active Directory event logs", "VPN authentication logs", "Application access logs", "SIEM"],
            "analysis_type": "Threshold",
            "anomaly_searched": "More than 10 failed logons in 5 minutes for a single account; geographically impossible logon pairs (same account logging in from two distant locations within minutes).",
            "tools": ["Python", "SQL"],
            "complexity": "Medium",
        },
        {
            "id": "DA011",
            "theme": "CYBER_RISK",
            "title": "Data Exfiltration Indicators",
            "objective": "Detect unusual outbound data transfers that may indicate exfiltration of client data or intellectual property.",
            "data_sources": ["DLP solution logs", "Proxy/web gateway logs", "Email gateway logs", "Cloud storage access logs"],
            "analysis_type": "Anomaly",
            "anomaly_searched": "Outbound email or upload volumes 3× standard deviation above the user's 90-day average; transfers to personal email or cloud storage (Dropbox, Google Drive) of files containing client data keywords.",
            "tools": ["Python", "SQL"],
            "complexity": "High",
        },
        {
            "id": "DA012",
            "theme": "CYBER_RISK",
            "title": "Third-Party Access Review",
            "objective": "Identify vendor and contractor accounts with active access that should have been revoked following contract termination.",
            "data_sources": ["Active Directory third-party OUs", "PAM vendor access logs", "HR/procurement system (contract termination dates)", "VPN logs"],
            "analysis_type": "Duplicate",
            "anomaly_searched": "Active vendor accounts where contract end date has passed; vendor accounts not used in >90 days; accounts with no matching active contract in the procurement system.",
            "tools": ["SQL", "Python"],
            "complexity": "Low",
        },
        {
            "id": "DA013",
            "theme": "CYBER_RISK",
            "title": "MFA Bypass or Downgrade Detection",
            "objective": "Identify authentication events where MFA was bypassed or a downgrade to single-factor authentication occurred.",
            "data_sources": ["Identity provider logs (Azure AD, Okta)", "VPN authentication logs", "Application access logs"],
            "analysis_type": "Anomaly",
            "anomaly_searched": "Successful logons to MFA-protected systems where MFA challenge was not recorded; legacy protocol authentications (NTLM, basic auth) on MFA-required systems.",
            "tools": ["Python", "SQL"],
            "complexity": "High",
        },
        {
            "id": "DA014",
            "theme": "CYBER_RISK",
            "title": "SIEM Alert SLA Compliance",
            "objective": "Monitor whether SOC team is meeting defined SLAs for alert triage and escalation.",
            "data_sources": ["SIEM platform (Splunk, Sentinel, QRadar)", "ITSM ticket system (ServiceNow)", "SOC shift logs"],
            "analysis_type": "Aging",
            "anomaly_searched": "High-severity alerts not triaged within 1 hour; medium alerts not reviewed within 4 hours; open alerts aged beyond SLA without documented investigation.",
            "tools": ["SQL", "Python", "Tableau"],
            "complexity": "Low",
        },
    ],

    "CREDIT_RISK": [
        {
            "id": "DA015",
            "theme": "CREDIT_RISK",
            "title": "Lombard Loan LTV Monitoring",
            "objective": "Identify Lombard loans where the current market value of collateral has deteriorated, causing LTV to breach the policy limit.",
            "data_sources": ["Core banking loan register", "Collateral management system", "Market data feed (Bloomberg, Reuters)"],
            "analysis_type": "Threshold",
            "anomaly_searched": "Loans with current LTV exceeding approved limit; loans within 5% of margin call trigger; concentrated collateral (>25% single name) approaching haircut threshold.",
            "tools": ["Python", "SQL", "Excel"],
            "complexity": "Medium",
        },
        {
            "id": "DA016",
            "theme": "CREDIT_RISK",
            "title": "Collateral Staleness Analysis",
            "objective": "Identify collateral positions that have not been revalued within the required frequency for their asset class.",
            "data_sources": ["Collateral management system", "Valuation history records", "Asset class classification register"],
            "analysis_type": "Aging",
            "anomaly_searched": "Listed securities not repriced in >1 business day; unlisted/private equity not revalued in >90 days; real estate not externally appraised in >12 months.",
            "tools": ["SQL", "Excel"],
            "complexity": "Low",
        },
        {
            "id": "DA017",
            "theme": "CREDIT_RISK",
            "title": "Credit Exception Rate Trending",
            "objective": "Track the volume and nature of credit policy exceptions over time to identify trend deterioration in underwriting standards.",
            "data_sources": ["Credit approval system", "Credit committee minutes", "Exception log", "Credit policy document"],
            "analysis_type": "Trend",
            "anomaly_searched": "Exception rate increasing quarter-over-quarter; repeat exceptions of the same type (policy not updated); exceptions approved by same senior without committee review.",
            "tools": ["Excel", "Python"],
            "complexity": "Low",
        },
        {
            "id": "DA018",
            "theme": "CREDIT_RISK",
            "title": "Covenant Breach Aging",
            "objective": "Identify covenant breaches that have not been escalated, remediated, or waived within the defined SLA.",
            "data_sources": ["Loan management system", "Covenant monitoring schedule", "Credit committee records", "Waiver log"],
            "analysis_type": "Aging",
            "anomaly_searched": "Covenant breaches outstanding >30 days without formal waiver or remediation plan; waivers granted without Credit Committee approval; recurring breach by same borrower.",
            "tools": ["SQL", "Excel"],
            "complexity": "Low",
        },
        {
            "id": "DA019",
            "theme": "CREDIT_RISK",
            "title": "IFRS 9 Stage Migration Analysis",
            "objective": "Analyse the movement of loans between IFRS 9 stages to identify potential under-staging and provisioning inadequacy.",
            "data_sources": ["Loan staging records (IFRS 9 system)", "Arrears history", "Credit risk grades", "Macroeconomic scenario inputs"],
            "analysis_type": "Statistical",
            "anomaly_searched": "High volume of Stage 3 loans migrating back to Stage 1 without genuine credit improvement; provision coverage ratio declining while NPL ratio is stable or increasing.",
            "tools": ["Python", "SQL"],
            "complexity": "High",
        },
        {
            "id": "DA020",
            "theme": "CREDIT_RISK",
            "title": "Single-Name Concentration Heat Map",
            "objective": "Map credit exposure concentration by obligor, sector, and geography to identify limit breaches or near-breaches.",
            "data_sources": ["Credit exposure register", "Collateral position data", "Industry/sector classification", "Country risk ratings"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Single obligor exposure exceeding 10% of Tier 1 capital; sector concentration exceeding policy limit; geographic concentration in FATF grey-listed jurisdiction.",
            "tools": ["Python", "Tableau", "SQL"],
            "complexity": "Medium",
        },
    ],

    "OPERATIONAL_RISK": [
        {
            "id": "DA021",
            "theme": "OPERATIONAL_RISK",
            "title": "Operational Loss Event Frequency Trending",
            "objective": "Monitor the frequency and severity of operational loss events over time to detect deterioration in the control environment.",
            "data_sources": ["Operational loss database", "Incident reporting system", "Insurance claim records"],
            "analysis_type": "Trend",
            "anomaly_searched": "Increasing frequency of losses in a specific risk category; single loss events exceeding materiality threshold not escalated to senior management; near-miss rate declining (possible under-reporting).",
            "tools": ["Python", "Excel", "Tableau"],
            "complexity": "Medium",
        },
        {
            "id": "DA022",
            "theme": "OPERATIONAL_RISK",
            "title": "KRI Threshold Breach Analysis",
            "objective": "Identify Key Risk Indicators that have breached amber or red thresholds and assess whether escalation occurred per policy.",
            "data_sources": ["KRI monitoring system", "Risk committee minutes", "KRI escalation log"],
            "analysis_type": "Threshold",
            "anomaly_searched": "KRIs in red zone for >30 days without documented escalation; same KRI breaching amber threshold in >3 consecutive months — indicative of unresolved root cause.",
            "tools": ["Excel", "SQL"],
            "complexity": "Low",
        },
        {
            "id": "DA023",
            "theme": "OPERATIONAL_RISK",
            "title": "Reconciliation Break Aging",
            "objective": "Track unreconciled items in cash and securities accounts by age to identify persistent breaks that may indicate errors or fraud.",
            "data_sources": ["Reconciliation system", "Nostro account statements", "Custody system position records"],
            "analysis_type": "Aging",
            "anomaly_searched": "Cash breaks aged >5 business days above materiality threshold; securities position breaks outstanding >1 business day; total aged break value exceeding defined tolerance.",
            "tools": ["SQL", "Excel"],
            "complexity": "Low",
        },
        {
            "id": "DA024",
            "theme": "OPERATIONAL_RISK",
            "title": "Emergency Change Overuse",
            "objective": "Identify whether the emergency change process is being overused as a workaround for standard change process controls.",
            "data_sources": ["IT change management system (ServiceNow, BMC Remedy)", "Change Advisory Board records", "Incident tickets linked to changes"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Emergency changes >15% of total change volume; emergency changes not reviewed post-implementation within 5 days; recurrent emergency changes by same team or system.",
            "tools": ["SQL", "Python"],
            "complexity": "Low",
        },
        {
            "id": "DA025",
            "theme": "OPERATIONAL_RISK",
            "title": "Segregation of Duties Conflict Detection",
            "objective": "Identify access rights conflicts where a single user holds permissions that should be segregated.",
            "data_sources": ["Identity and access management system", "Role-based access control matrix", "Application user access logs", "SoD conflict rule library"],
            "analysis_type": "Duplicate",
            "anomaly_searched": "Users with both trade input and trade approval access; users with both payment creation and payment release permissions; single user with access to modify transaction records and approve them.",
            "tools": ["SQL", "Python"],
            "complexity": "High",
        },
    ],

    "DATA_PRIVACY": [
        {
            "id": "DA026",
            "theme": "DATA_PRIVACY",
            "title": "Data Retention Compliance Scan",
            "objective": "Identify personal data held beyond its defined retention period in key systems.",
            "data_sources": ["Core banking system", "CRM", "Email archive", "Document management system", "Data retention schedule"],
            "analysis_type": "Aging",
            "anomaly_searched": "Former client records in active systems beyond retention period (e.g. >10 years post-relationship end); email archives containing personal data with no retention controls applied.",
            "tools": ["SQL", "Python"],
            "complexity": "Medium",
        },
        {
            "id": "DA027",
            "theme": "DATA_PRIVACY",
            "title": "DSAR Response Time Tracking",
            "objective": "Monitor the time taken to respond to data subject access requests and identify overdue responses.",
            "data_sources": ["DSAR log / privacy management platform", "Request intake records", "Response dispatch records"],
            "analysis_type": "Aging",
            "anomaly_searched": "DSARs not responded to within 30 calendar days of receipt; extension notices (up to 2 months) not sent within the initial 30-day period; DSAR backlog growing quarter-over-quarter.",
            "tools": ["Excel", "SQL"],
            "complexity": "Low",
        },
        {
            "id": "DA028",
            "theme": "DATA_PRIVACY",
            "title": "Cross-Border Transfer Mapping",
            "objective": "Identify all personal data transfers to third countries and validate that appropriate transfer mechanisms are in place.",
            "data_sources": ["Records of processing activities (RoPA)", "IT system inventory with hosting location", "Vendor contracts and DPAs", "SCC register"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Personal data hosted or processed in non-adequate countries without executed SCCs; data transfers not reflected in RoPA; vendor location changes not reassessed for transfer mechanism validity.",
            "tools": ["Excel", "Python"],
            "complexity": "Medium",
        },
        {
            "id": "DA029",
            "theme": "DATA_PRIVACY",
            "title": "Breach Log Completeness Analysis",
            "objective": "Assess whether the data breach log captures all security incidents and validates reportability assessment quality.",
            "data_sources": ["Data breach register", "IT security incident log", "SIEM incident records", "DLP alert log"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Security incidents in the IT log not reflected in the breach register; breaches classified as non-reportable without documented risk assessment; near-misses not recorded in breach log.",
            "tools": ["SQL", "Excel"],
            "complexity": "Medium",
        },
        {
            "id": "DA030",
            "theme": "DATA_PRIVACY",
            "title": "Consent Record Completeness",
            "objective": "Verify that consent records exist and are current for all marketing and profiling processing activities.",
            "data_sources": ["Consent management platform", "Marketing campaign system", "CRM client contact preferences", "Privacy preference centre logs"],
            "analysis_type": "Duplicate",
            "anomaly_searched": "Marketing emails sent to clients without a valid consent record; consent records with no timestamp or version; withdrawn consents not processed within 72 hours.",
            "tools": ["SQL", "Python"],
            "complexity": "Medium",
        },
    ],

    "MARKET_RISK": [
        {
            "id": "DA031",
            "theme": "MARKET_RISK",
            "title": "VaR Backtesting Exception Tracking",
            "objective": "Count and classify VaR backtesting exceptions to assess model performance and capital adequacy.",
            "data_sources": ["Risk system VaR output", "Daily P&L data", "Trading book positions", "Market data feed"],
            "analysis_type": "Statistical",
            "anomaly_searched": "More than 4 exceptions in a 250-day window (Yellow Zone) or more than 10 (Red Zone) per Basel II traffic light approach; clustering of exceptions in specific market conditions suggesting systematic model bias.",
            "tools": ["Python", "Excel"],
            "complexity": "High",
        },
        {
            "id": "DA032",
            "theme": "MARKET_RISK",
            "title": "Market Risk Limit Utilisation Trending",
            "objective": "Monitor risk limit utilisation over time to detect limit creep and assess headroom adequacy.",
            "data_sources": ["Risk management system limit utilisation reports", "Trading system positions", "Market data"],
            "analysis_type": "Trend",
            "anomaly_searched": "Limits consistently >90% utilised — insufficient headroom for normal business fluctuations; limits breached and waived repeatedly without policy amendment; new positions added without limit capacity.",
            "tools": ["Python", "Tableau", "Excel"],
            "complexity": "Medium",
        },
        {
            "id": "DA033",
            "theme": "MARKET_RISK",
            "title": "IRRBB Sensitivity Trend Analysis",
            "objective": "Track NII and EVE sensitivity to interest rate changes over time to assess IRRBB risk trend and compliance with appetite.",
            "data_sources": ["ALM system", "Balance sheet data", "Interest rate curves", "Behavioural assumption inputs"],
            "analysis_type": "Trend",
            "anomaly_searched": "EVE sensitivity under +200bp scenario increasing quarter-over-quarter; NII sensitivity exceeding risk appetite; behavioural assumptions not updated since prior year.",
            "tools": ["Python", "Excel"],
            "complexity": "High",
        },
        {
            "id": "DA034",
            "theme": "MARKET_RISK",
            "title": "P&L Attribution Unexplained Variance",
            "objective": "Identify unexplained variance between predicted P&L (based on risk sensitivities) and actual P&L to detect model weaknesses.",
            "data_sources": ["Trading P&L records", "Risk sensitivity report", "Market data moves", "Position data"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Unexplained P&L variance exceeding 10% of total daily P&L on more than 3 days per month; systematic bias in a specific risk factor suggesting missing sensitivity.",
            "tools": ["Python", "Excel"],
            "complexity": "High",
        },
        {
            "id": "DA035",
            "theme": "MARKET_RISK",
            "title": "Independent Price Verification Coverage",
            "objective": "Confirm that all positions in the trading and banking book are subject to independent price verification at the required frequency.",
            "data_sources": ["Position data", "IPV results log", "Asset class register", "Pricing sources (Bloomberg, third-party)"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Positions not included in IPV scope; Level 2/3 assets priced using internal models without external validation; IPV frequency below policy requirement for specific asset classes.",
            "tools": ["SQL", "Python"],
            "complexity": "Medium",
        },
    ],

    "THIRD_PARTY_RISK": [
        {
            "id": "DA036",
            "theme": "THIRD_PARTY_RISK",
            "title": "Vendor Due Diligence Completeness",
            "objective": "Identify vendors in the outsourcing register where due diligence documentation is missing, expired, or below the required standard for their risk tier.",
            "data_sources": ["Outsourcing / vendor register", "Due diligence document repository", "SOC 2 report tracker", "Vendor risk tier classification"],
            "analysis_type": "Aging",
            "anomaly_searched": "Critical vendors with SOC 2 reports >12 months old; high-risk vendors without completed security questionnaire; any vendor with no due diligence on file.",
            "tools": ["SQL", "Excel"],
            "complexity": "Low",
        },
        {
            "id": "DA037",
            "theme": "THIRD_PARTY_RISK",
            "title": "SLA Breach Monitoring",
            "objective": "Track vendor SLA performance against contractual commitments and identify chronic underperformers.",
            "data_sources": ["Vendor SLA monitoring reports", "Service performance records", "Incident tickets linked to vendor failures", "Contract terms extract"],
            "analysis_type": "Threshold",
            "anomaly_searched": "Vendors failing SLA in >2 consecutive months without formal notice; service credits not claimed despite SLA breach; SLA not defined or measurable in contract.",
            "tools": ["Excel", "SQL"],
            "complexity": "Low",
        },
        {
            "id": "DA038",
            "theme": "THIRD_PARTY_RISK",
            "title": "Concentration Risk Quantification",
            "objective": "Quantify the proportion of critical functions delivered by each top-five vendor to assess concentration risk.",
            "data_sources": ["Outsourcing register", "Critical function mapping", "Vendor spend data", "Business continuity dependency mapping"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Single vendor supporting >30% of critical business services; single cloud provider hosting >50% of production workloads; top-3 vendors collectively responsible for >80% of outsourced critical functions.",
            "tools": ["Python", "Tableau"],
            "complexity": "Medium",
        },
        {
            "id": "DA039",
            "theme": "THIRD_PARTY_RISK",
            "title": "Sub-Outsourcing Disclosure Tracking",
            "objective": "Monitor whether critical vendors have disclosed material sub-outsourcers as required by contract, and flag new or changed sub-outsourcers.",
            "data_sources": ["Vendor sub-outsourcing disclosure records", "Fourth-party register", "Vendor contracts sub-outsourcing clauses"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Critical vendors that have not provided annual sub-outsourcer disclosure; new sub-outsourcers disclosed in FATF-listed or sanctioned jurisdictions; sub-outsourcers not approved by the bank.",
            "tools": ["Excel", "SQL"],
            "complexity": "Low",
        },
        {
            "id": "DA040",
            "theme": "THIRD_PARTY_RISK",
            "title": "Contract Coverage Gap Analysis",
            "objective": "Identify gaps in vendor contracts relative to regulatory requirements (DORA, FINMA RS 2018/3, PRA SS2/21) for critical and material vendors.",
            "data_sources": ["Contract register", "Contract terms database", "Regulatory minimum clause checklist", "Vendor risk tier classification"],
            "analysis_type": "Duplicate",
            "anomaly_searched": "Critical vendor contracts missing audit rights clause; contracts without data portability obligation; contracts with no business continuity or exit provision; contracts not updated since 2020.",
            "tools": ["SQL", "Excel"],
            "complexity": "Medium",
        },
    ],

    "GOVERNANCE": [
        {
            "id": "DA041",
            "theme": "GOVERNANCE",
            "title": "Policy Review Cycle Compliance",
            "objective": "Identify policies that are overdue for their mandatory periodic review.",
            "data_sources": ["Policy management system", "Policy register with review dates", "Approval workflow records"],
            "analysis_type": "Aging",
            "anomaly_searched": "Policies overdue for review by >3 months; critical policies (AML, Cyber, Operational Risk) with review overdue; policies approved by individuals who have since left the organisation.",
            "tools": ["Excel", "SQL"],
            "complexity": "Low",
        },
        {
            "id": "DA042",
            "theme": "GOVERNANCE",
            "title": "Board Meeting Attendance Analysis",
            "objective": "Assess Board and Committee meeting attendance rates to identify potential governance concerns.",
            "data_sources": ["Board and committee meeting minutes", "Attendance registers", "Director profiles"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Directors attending <75% of Board or Committee meetings in a year; independent director missing >2 consecutive Risk Committee meetings; Audit Committee quorum not met.",
            "tools": ["Excel"],
            "complexity": "Low",
        },
        {
            "id": "DA043",
            "theme": "GOVERNANCE",
            "title": "Audit Finding Closure Aging",
            "objective": "Track the age of open internal audit findings and identify items overdue for remediation.",
            "data_sources": ["Internal audit tracking system", "Finding register with target dates", "Management response records"],
            "analysis_type": "Aging",
            "anomaly_searched": "Critical findings open >90 days past target remediation date; high findings with >2 deadline extensions; repeat findings from prior audit cycles (systemic control failure).",
            "tools": ["SQL", "Excel", "Tableau"],
            "complexity": "Low",
        },
        {
            "id": "DA044",
            "theme": "GOVERNANCE",
            "title": "Conflicts of Interest Disclosure Gap",
            "objective": "Identify staff who have not submitted their annual conflicts of interest declaration.",
            "data_sources": ["HR system", "Conflicts of interest register", "Declaration submission records", "In-scope staff list"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Staff in material functions (RM, compliance, risk, finance) who have not submitted annual CoI declaration; new hires >30 days without initial CoI disclosure.",
            "tools": ["SQL", "Excel"],
            "complexity": "Low",
        },
        {
            "id": "DA045",
            "theme": "GOVERNANCE",
            "title": "Mandatory Training Completion Rate",
            "objective": "Monitor completion rates for mandatory compliance training and identify non-compliant staff.",
            "data_sources": ["Learning management system (LMS)", "Training curriculum register", "Staff list by function and role", "Completion certificates"],
            "analysis_type": "Statistical",
            "anomaly_searched": "Staff with mandatory AML, data privacy, or cyber awareness training completion overdue >30 days past deadline; senior management with lower completion rates than general staff.",
            "tools": ["Excel", "SQL"],
            "complexity": "Low",
        },
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# 7. IIA_STANDARDS_2024
# ═══════════════════════════════════════════════════════════════════════════════

IIA_STANDARDS_2024 = [
    {
        "standard_id": "Overview",
        "domain": "Framework",
        "title": "Global Internal Audit Standards (GIAS) 2024",
        "description": "The GIAS 2024, effective January 9, 2024, replace the 2017 Standards. They establish mandatory requirements across five Domains, introduce Topical Requirements for specialised areas, and elevate the CAE's accountability to governing bodies. They apply to all internal audit functions globally.",
        "key_requirements": [
            "Mandatory for all IIA member functions globally from January 9, 2024",
            "Five Domains: Domain I — Purpose of Internal Auditing; Domain II — Ethics and Professionalism; Domain III — Governing the Internal Audit Function; Domain IV — Managing the Internal Audit Function; Domain V — Performing Internal Audit Services",
            "Topical Requirements for Fraud, Cyber, Culture, ESG, and Third-Party Risk",
            "Enhanced independence and objectivity requirements",
            "Stronger quality assurance and reporting to governing bodies",
        ],
        "banking_application": "Swiss private banks must align their internal audit charters, methodologies, and reporting frameworks with GIAS 2024 to satisfy FINMA Circular 2017/1 and IIA membership obligations.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    # Domain I
    {
        "standard_id": "Standard 1",
        "domain": "Domain I — Purpose of Internal Auditing",
        "title": "Purpose of Internal Auditing",
        "description": "Internal auditing strengthens the organization's ability to create, protect, and sustain value by providing the governing body and senior management with independent, risk-based, and objective assurance, advice, insight, and foresight.",
        "key_requirements": [
            "Internal audit must provide assurance, advice, insight, and foresight",
            "Activities must strengthen value creation and protection",
            "Scope covers governance, risk management, and internal controls",
            "Must serve both the governing body and senior management",
            "Independence is non-negotiable in all engagements",
        ],
        "banking_application": "In private banking, internal audit must cover all three lines of defence: front office (1L), risk and compliance (2L), and audit itself (3L). Value protection includes client assets, regulatory licence, and reputational capital.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 2",
        "domain": "Domain I — Purpose of Internal Auditing",
        "title": "Ethics and Professional Conduct",
        "description": "Internal auditors must demonstrate integrity, objectivity, and respect for others. They must comply with the IIA Code of Ethics and avoid conflicts of interest in all professional activities.",
        "key_requirements": [
            "Compliance with the IIA Code of Ethics at all times",
            "Integrity in all findings, reporting, and communications",
            "Objectivity: no subordination of judgement to others",
            "Confidentiality of information obtained during engagements",
            "Disclosure of actual and potential conflicts of interest",
        ],
        "banking_application": "Auditors reviewing private banking operations must maintain strict confidentiality regarding HNWI client data, declare conflicts if they hold accounts at the audited entity, and report findings without influence from senior management.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    # Domain II
    {
        "standard_id": "Standard 3",
        "domain": "Domain II — Ethics and Professionalism",
        "title": "Independence and Objectivity",
        "description": "The internal audit function must be independent of the activities it audits. Individual auditors must be objective in performing their work, ensuring that assessments are based on evidence rather than personal interest or external influence.",
        "key_requirements": [
            "Organizational independence: CAE reports functionally to the governing body",
            "No dual-hat arrangements between 1L/2L and 3L",
            "Individual objectivity: auditor free from bias and conflict",
            "Impairments to independence must be disclosed immediately",
            "Annual declaration of independence for CAE and audit staff",
        ],
        "banking_application": "The CAE of a Swiss private bank must report functionally to the Audit Committee (not the CEO or CFO). Auditors who previously worked in the front office cannot audit their former team without a 12-month cooling-off period.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 4",
        "domain": "Domain II — Ethics and Professionalism",
        "title": "Competency",
        "description": "Internal auditors must possess or develop the knowledge, skills, and other competencies needed to fulfil their responsibilities. The CAE must ensure the function collectively possesses the competencies required to cover the audit universe.",
        "key_requirements": [
            "Collective competency across all audit universe areas",
            "Professional qualifications: CIA, CPA, CISA, CFE as appropriate",
            "Continuous professional development (CPD) mandatory",
            "Use of specialists for technology, forensics, or actuarial work",
            "Competency gaps must be disclosed in the audit plan",
        ],
        "banking_application": "Private banking audit teams must include auditors with expertise in AML, wealth management products, credit risk (Lombard lending), technology/cybersecurity, and applicable regulations (FINMA, MAS, FCA). External specialists may be engaged for complex quantitative model reviews.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 5",
        "domain": "Domain II — Ethics and Professionalism",
        "title": "Due Professional Care",
        "description": "Internal auditors must apply the care and skill expected of a reasonably prudent and competent internal auditor. Due professional care does not imply infallibility.",
        "key_requirements": [
            "Reasonable assurance standard: not absolute certainty",
            "Adequate testing based on risk — sampling must be justified",
            "Professional scepticism in evaluating management representations",
            "Consideration of fraud risk in all engagements",
            "Documentation sufficient to support conclusions",
        ],
        "banking_application": "In private banking, due care means applying sufficient sample sizes for client file testing, not accepting management assertions without evidence, and maintaining working paper standards sufficient for FINMA regulatory examination.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    # Domain III
    {
        "standard_id": "Standard 6",
        "domain": "Domain III — Governing the Internal Audit Function",
        "title": "Chief Audit Executive Leadership",
        "description": "The CAE is responsible for directing the internal audit function, promoting a culture of integrity, and managing the function to meet its mandate. The CAE must be a senior leader who communicates effectively with the governing body.",
        "key_requirements": [
            "CAE accountable for the internal audit function's performance",
            "Direct access to the governing body without management interference",
            "Champion ethical culture across the organisation",
            "Manage function to deliver the approved audit plan",
            "Escalate significant risk and control issues without delay",
        ],
        "banking_application": "The CAE of a private bank must have direct access to the Board Audit Committee, receive invitations to all AC meetings, and be empowered to raise concerns about regulatory breaches or significant control failures directly to the AC Chair.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 7",
        "domain": "Domain III — Governing the Internal Audit Function",
        "title": "Organisational Independence",
        "description": "The internal audit function must be positioned within the organisation to enable it to fulfil its mandate with independence and objectivity. The CAE must report functionally to the governing body.",
        "key_requirements": [
            "Functional reporting to governing body (Audit Committee or Board)",
            "Administrative reporting may be to CEO — but must not impair independence",
            "CAE appointment and removal requires governing body approval",
            "Budget and resources approved by governing body",
            "Annual independence assessment reported to governing body",
        ],
        "banking_application": "Under FINMA Circular 2017/1, the CAE of a Swiss bank must report to the Board Audit Committee. The AC must approve the audit plan and budget independently of senior management.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 8",
        "domain": "Domain III — Governing the Internal Audit Function",
        "title": "Internal Audit Charter",
        "description": "The internal audit function must have a formal charter approved by the governing body that defines its purpose, authority, and responsibilities. The charter must be reviewed and reaffirmed annually.",
        "key_requirements": [
            "Charter approved by the governing body (not management)",
            "Defines purpose, authority, scope, and independence",
            "Unrestricted access to people, records, and systems",
            "Annual review and reaffirmation by the governing body",
            "Charter publicly disclosed or available on request",
        ],
        "banking_application": "The private banking audit charter must explicitly cover all legal entities, branches (CH, SG, HK, Bahamas), and material subsidiaries. It must grant access to client files, trading systems, and HR records without management gatekeeping.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 9",
        "domain": "Domain III — Governing the Internal Audit Function",
        "title": "Audit Strategy and Planning",
        "description": "The CAE must develop and maintain a risk-based audit strategy and annual plan that aligns with the organisation's risk profile and strategic priorities. The plan must be approved by the governing body.",
        "key_requirements": [
            "Risk-based audit universe covering all significant activities",
            "Annual plan approved by the Audit Committee",
            "Plan updated dynamically for emerging risks",
            "Resource allocation matched to risk and coverage",
            "Rationale for unaudited areas disclosed to governing body",
        ],
        "banking_application": "Private banking audit plans must prioritise AML/KYC, cyber risk, credit risk (Lombard lending), cross-border compliance, and ESG in line with FINMA and MAS supervisory priorities. Unaudited high-risk areas must be formally disclosed to the AC.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 10",
        "domain": "Domain III — Governing the Internal Audit Function",
        "title": "Resource Management",
        "description": "The CAE must ensure the internal audit function has adequate human, financial, and technological resources to fulfil its mandate. Resource gaps must be disclosed to the governing body.",
        "key_requirements": [
            "Budget sufficient to deliver the approved audit plan",
            "Staffing levels commensurate with audit universe complexity",
            "Technology tools for data analytics and workflow management",
            "Disclosure of resource constraints that limit plan delivery",
            "Use of co-sourcing or outsourcing where gaps exist",
        ],
        "banking_application": "Private banks with operations in multiple jurisdictions must ensure audit staffing in key locations (CH, SG, HK) or demonstrate alternative coverage through group audit. Co-sourcing with Big 4 or specialist firms is common for complex areas (model risk, cyber).",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 11",
        "domain": "Domain III — Governing the Internal Audit Function",
        "title": "Quality Assurance and Improvement Programme",
        "description": "The CAE must establish and maintain a quality assurance and improvement programme (QAIP) that covers all aspects of the internal audit function. Results must be communicated to the governing body.",
        "key_requirements": [
            "Internal assessments: ongoing monitoring and periodic self-assessment",
            "External quality assessment every 5 years by qualified independent assessor",
            "Conformance declaration in annual report to governing body",
            "Action plans to address identified deficiencies",
            "Disclosure of non-conformance with GIAS 2024",
        ],
        "banking_application": "FINMA expects Swiss bank audit functions to demonstrate GIAS conformance. External QAR every 5 years should be conducted by an IIA-certified assessor. Results must be reported to the Audit Committee, not just filed internally.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    # Domain IV
    {
        "standard_id": "Standard 12",
        "domain": "Domain IV — Managing the Internal Audit Function",
        "title": "Planning Engagements",
        "description": "Internal auditors must plan each engagement to assess the relevant risks, controls, and governance processes. A preliminary risk assessment must be performed and the engagement objectives, scope, and criteria must be defined before fieldwork begins.",
        "key_requirements": [
            "Preliminary risk assessment before each engagement",
            "Clear engagement objectives and scope defined upfront",
            "Criteria for evaluating controls established in advance",
            "Planning documented in engagement work programme",
            "Management briefed on objectives and timing before fieldwork",
        ],
        "banking_application": "For a private banking AML audit, engagement planning must include a preliminary risk assessment of jurisdiction, client risk profile mix, TMS alert volumes, and prior findings. The scope must cover all relevant legal entities, not just the Swiss parent.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 13",
        "domain": "Domain IV — Managing the Internal Audit Function",
        "title": "Performing Engagements",
        "description": "Internal auditors must identify sufficient, reliable, and relevant information to achieve the engagement objectives. Conclusions must be based on analysis and evaluation of evidence, not assumptions.",
        "key_requirements": [
            "Evidence must be sufficient, reliable, relevant, and useful",
            "Working papers must support conclusions and be properly retained",
            "Supervision by experienced auditor throughout fieldwork",
            "Identified issues communicated to management during fieldwork",
            "Anomalies and fraud indicators must be escalated promptly",
        ],
        "banking_application": "Sampling methodology must be risk-based (judgmental or statistical). Client file samples must cover the full risk spectrum (high, medium, low risk). Anomalies in TMS or credit data discovered during fieldwork must be escalated to the CAE before the report is issued.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 14",
        "domain": "Domain IV — Managing the Internal Audit Function",
        "title": "Communicating Results",
        "description": "Internal auditors must communicate the results of each engagement, including the opinion, findings, recommendations, and action plans, to appropriate parties. Reports must be accurate, objective, clear, concise, and timely.",
        "key_requirements": [
            "Written report for every assurance engagement",
            "Overall audit opinion (Satisfactory/Needs Improvement/Unsatisfactory)",
            "Each finding: criteria, condition, cause, consequence, recommendation",
            "Management action plans with owners and due dates",
            "Distribution to governing body for significant findings",
        ],
        "banking_application": "Private banking audit reports must include an overall rating, individual finding ratings (Critical/High/Moderate/Low), and be issued within 30 days of fieldwork completion. Significant findings (Critical/High) must be reported to the Audit Committee at the next meeting.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 15",
        "domain": "Domain IV — Managing the Internal Audit Function",
        "title": "Monitoring Actions",
        "description": "The CAE must establish and maintain a follow-up process to monitor and ensure that management actions have been effectively implemented. Open findings must be tracked and reported to the governing body.",
        "key_requirements": [
            "Formal tracking system for all open findings",
            "Verification that management actions are effectively implemented (not just attested)",
            "Past-due findings escalated to senior management and governing body",
            "Repeat findings identified and root cause analysis required",
            "Quarterly status report of open findings to Audit Committee",
        ],
        "banking_application": "In a private bank, the CAE must maintain a live findings register in a GRC system, evidence actual remediation (not just management attestation), escalate overdue Critical/High findings to the AC Chair, and identify repeat findings as an indicator of systemic control weakness.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    # Domain V
    {
        "standard_id": "Standard 16",
        "domain": "Domain V — Performing Internal Audit Services",
        "title": "Assurance Services",
        "description": "Assurance services provide an independent, objective assessment of the adequacy and effectiveness of governance, risk management, and internal control processes. The audit opinion must be based on sufficient evidence.",
        "key_requirements": [
            "Risk-based scope covering governance, risk, and control",
            "Independent opinion on control effectiveness",
            "Criteria (regulations, policies, best practice) clearly stated",
            "Findings include root cause and business impact",
            "Overall assurance opinion (not just individual findings)",
        ],
        "banking_application": "Assurance engagements in private banking typically cover AML/KYC controls, Lombard credit process, IT security controls, and compliance with FINMA/MAS/FCA regulations. The overall opinion must be risk-rated (Satisfactory, Needs Improvement, or Unsatisfactory).",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 17",
        "domain": "Domain V — Performing Internal Audit Services",
        "title": "Advisory Services",
        "description": "Advisory services are consulting activities designed to add value and improve the organisation's governance, risk management, and control processes. The nature and scope must be agreed with the client and must not impair independence.",
        "key_requirements": [
            "Scope and objectives agreed with the engagement client",
            "Independence must not be impaired by advisory work",
            "Advisory findings do not carry the same weight as assurance",
            "Significant risks identified during advisory must be communicated",
            "Advisory work documented to the same standard as assurance",
        ],
        "banking_application": "Private banking audit teams may advise on new product development controls, digital transformation programmes, or regulatory change implementations (e.g., DORA readiness). However, auditors must not assume ownership of the controls they advise on.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "Standard 18",
        "domain": "Domain V — Performing Internal Audit Services",
        "title": "Investigation Services",
        "description": "Investigation services involve examining allegations of fraud, misconduct, or regulatory violations. Investigations must be conducted with objectivity, appropriate expertise, and in compliance with legal requirements.",
        "key_requirements": [
            "Investigation mandate and scope approved by governing body",
            "Appropriate forensic and legal expertise engaged",
            "Chain of custody maintained for all evidence",
            "Findings communicated to appropriate parties including regulators if required",
            "Lessons learned fed back into audit plan risk assessment",
        ],
        "banking_application": "In private banking, investigations may cover suspected money laundering (client or employee), unauthorized trading, data theft, or senior management misconduct. FINMA must be notified of material fraud within regulatory timeframes. External forensic specialists are typically required.",
        "topical_requirement": False,
        "effective_date": "January 9, 2024",
    },
    # Topical Requirements
    {
        "standard_id": "TR-1",
        "domain": "Topical Requirements",
        "title": "Fraud and Misconduct",
        "description": "Internal auditors must incorporate fraud risk assessment into the audit universe and individual engagements. They must be alert to fraud indicators throughout all audit work and escalate suspicions promptly.",
        "key_requirements": [
            "Fraud risk assessment mandatory in all assurance engagements",
            "Auditors trained to recognise fraud red flags and indicators",
            "Imminent or suspected fraud escalated to CAE and governing body immediately",
            "Cooperation with legal, compliance, and law enforcement as required",
            "Lessons learned from fraud events incorporated into future audit plans",
        ],
        "banking_application": "Private banking fraud risks include: client impersonation (identity fraud), front-office misconduct (churning, unauthorised transactions), AML facilitation, and cyber-enabled fraud (BEC, CEO fraud). Each audit must assess relevant fraud scenarios, not just general controls.",
        "topical_requirement": True,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "TR-2",
        "domain": "Topical Requirements",
        "title": "Cybersecurity",
        "source_guide": "IIA User Guide, February 2025",
        "description": "Mandatory for all assurance engagements on cybersecurity. Internal auditors must evaluate cybersecurity governance, risk management, and control processes across the organisation. Specialist knowledge or co-sourced expertise is required. Structured across three sections: Governance (4), Risk Management (6), Control Processes (7).",
        "key_requirements": [
            "G-A: Formal cybersecurity strategy reviewed by Board (generally quarterly)",
            "RM-A/B: Cyber risk assessment covering all organisational functions",
            "RM-F: Annual tabletop exercise for incident response and recovery",
            "CP-D/E: IT asset lifecycle management, MFA, patch management, SDLC",
            "CP-F/G: Network segmentation, endpoint communication security",
        ],
        "sections": [
            {
                "section_id": "governance",
                "section_title": "Governance",
                "icon": "🏛️",
                "requirements": [
                    {
                        "id": "G-A",
                        "text": "Formal cybersecurity strategy and objectives established and periodically updated. Board reviews cybersecurity updates periodically (generally quarterly). Covers strategic objectives monitoring, budget, KPIs, and human resources for cyber personnel.",
                        "frameworks": ["NIST CSF 2.0 GV.OC-01, GV.OC-02", "COBIT 2019 APO02", "NIST 800-53 PM-2"],
                    },
                    {
                        "id": "G-B",
                        "text": "Policies and procedures established, periodically updated (at least annually). Reference frameworks: NIST, COBIT. Covers all cybersecurity processes.",
                        "frameworks": ["NIST CSF 2.0 GV.PO-01, GV.PO-02", "COBIT 2019 APO01", "NIST 800-53 PL-2"],
                    },
                    {
                        "id": "G-C",
                        "text": "Roles and responsibilities defined. CISO or equivalent reports at sufficient organisational level. Periodic assessment of knowledge, skills, and abilities of cybersecurity personnel.",
                        "frameworks": ["NIST CSF 2.0 GV.RR-01, GV.RR-02", "COBIT 2019 APO01.02", "NIST 800-53 PS-7"],
                    },
                    {
                        "id": "G-D",
                        "text": "Stakeholder engagement on vulnerabilities and emerging threats. Includes senior management, operations, risk, HR, legal, compliance, vendors. Evidence: meeting minutes, reports, emails.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-07", "COBIT 2019 EDM02", "NIST 800-53 PL-8"],
                    },
                ],
            },
            {
                "section_id": "risk_management",
                "section_title": "Risk Management",
                "icon": "⚠️",
                "requirements": [
                    {
                        "id": "RM-A",
                        "text": "Risk assessment and management process covers identification, analysis, mitigation, and monitoring of cyber threats and their effect on strategic objectives.",
                        "frameworks": ["NIST CSF 2.0 ID.RA-01, ID.RA-03", "COBIT 2019 APO12", "NIST 800-53 RA-3"],
                    },
                    {
                        "id": "RM-B",
                        "text": "Cyber risk management conducted across the organisation: IT, ERM, HR, legal, compliance, operations, supply chain, accounting, finance.",
                        "frameworks": ["NIST CSF 2.0 ID.RA-04", "COBIT 2019 APO12.01", "NIST 800-53 RA-3(1)"],
                    },
                    {
                        "id": "RM-C",
                        "text": "Accountability assigned to individual or team. Periodic reporting (quarterly/monthly) on cyber risk status including resource requirements.",
                        "frameworks": ["NIST CSF 2.0 GV.RR-03", "COBIT 2019 APO12.05", "NIST 800-53 PM-9"],
                    },
                    {
                        "id": "RM-D",
                        "text": "Escalation process for cyber risks reaching unacceptable levels. Covers risk levels definition, financial and non-financial impacts, regulatory compliance requirements.",
                        "frameworks": ["NIST CSF 2.0 GV.RM-07", "COBIT 2019 APO12.06", "NIST 800-53 RA-7"],
                    },
                    {
                        "id": "RM-E",
                        "text": "Communication process to management and employees. Annual phishing simulations. Remediation updates with completion dates. Board/senior management reporting on non-compliance.",
                        "frameworks": ["NIST CSF 2.0 PR.AT-01", "COBIT 2019 APO07", "NIST 800-53 AT-2"],
                    },
                    {
                        "id": "RM-F",
                        "text": "Incident response and recovery process: detection, containment, recovery, post-incident analysis. Annual tabletop exercise mandatory. Results reported to senior management.",
                        "frameworks": ["NIST CSF 2.0 RS.MA-01, RC.RP-01", "COBIT 2019 DSS02, DSS04", "NIST 800-53 IR-4, IR-6, IR-8"],
                    },
                ],
            },
            {
                "section_id": "control_processes",
                "section_title": "Control Processes",
                "icon": "🔒",
                "requirements": [
                    {
                        "id": "CP-A",
                        "text": "Internal controls and vendor-based controls protect confidentiality, integrity, availability. SOC reports reviewed for vendors. Periodic testing of controls effectiveness. Remediation process for deficiencies.",
                        "frameworks": ["NIST CSF 2.0 PR.AA-05, GV.SC-07", "COBIT 2019 APO10, DSS05", "NIST 800-53 CA-2, CA-7"],
                    },
                    {
                        "id": "CP-B",
                        "text": "Talent management for cybersecurity: recruitment, training, certifications (cyber-related). Knowledge sharing groups. Continuing education.",
                        "frameworks": ["NIST CSF 2.0 PR.AT-02", "COBIT 2019 APO07.03", "NIST 800-53 AT-3"],
                    },
                    {
                        "id": "CP-C",
                        "text": "Continuous monitoring of emerging threats and vulnerabilities including AI/new technologies. Prioritisation and implementation of improvements.",
                        "frameworks": ["NIST CSF 2.0 ID.RA-05, DE.AE-03", "COBIT 2019 APO12.02", "NIST 800-53 SI-5, RA-5"],
                    },
                    {
                        "id": "CP-D",
                        "text": "IT asset lifecycle management (selection, usage, maintenance, decommissioning) for hardware, software, vendor services. Includes encryption, antivirus, MDM, complex passwords, VPN/ZTN, firmware updates, database controls, SDLC, DevSecOps.",
                        "frameworks": ["NIST CSF 2.0 ID.AM-01 to 07", "COBIT 2019 BAI09, DSS05", "NIST 800-53 CM-8, SA-22"],
                    },
                    {
                        "id": "CP-E",
                        "text": "Cybersecurity processes: configuration, end-user device administration, encryption, patching, user-access management (MFA, unique IDs, complex passwords), monitoring availability/performance, DevSecOps integration.",
                        "frameworks": ["NIST CSF 2.0 PR.AA-01 to 06, PR.DS-01", "COBIT 2019 DSS05.03, DSS05.04", "NIST 800-53 AC-2, IA-2, SC-28"],
                    },
                    {
                        "id": "CP-F",
                        "text": "Network controls: network segmentation, firewalls, limited external/internal connections, VPN/ZTNA, IoT controls, IDS/IPS.",
                        "frameworks": ["NIST CSF 2.0 PR.IR-01, PR.IR-02", "COBIT 2019 DSS05.02", "NIST 800-53 SC-7, SC-20"],
                    },
                    {
                        "id": "CP-G",
                        "text": "Endpoint communication security: email, browsers, videoconferencing, messaging (Teams/Zoom), social media, cloud, file-sharing. Controls include file extension restrictions, MFA for file sharing.",
                        "frameworks": ["NIST CSF 2.0 PR.PS-04", "COBIT 2019 DSS05.07", "NIST 800-53 SC-8, SC-28"],
                    },
                ],
            },
        ],
        "framework_mapping": ["NIST CSF 2.0", "NIST SP 800-53 Rev.5", "COBIT 2019"],
        "banking_application": "DORA (EU, effective Jan 2025): TLPT mandatory, ICT risk management framework, major incident reporting within 4 hours, third-party ICT oversight (Art. 28–30). FINMA RS 2018/3: outsourcing IT controls for Swiss banks. MAS TRM 2021: annual ICT audit requirement (SG). Elevated threat profile: HNWI data and private banker social engineering are prime ransomware targets. Cloud migration across jurisdictions increases attack surface and cross-border data exposure.",
        "topical_requirement": True,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "TR-3",
        "domain": "Topical Requirements",
        "title": "Organisational Culture and Ethics",
        "description": "Internal auditors must evaluate whether the organisation's culture supports ethical behaviour, sound risk management, and compliance with laws and regulations. Tone at the top, middle management conduct, and speak-up mechanisms must be assessed.",
        "key_requirements": [
            "Culture assessment methodology defined in the audit plan",
            "Tone at the top: Board and senior management behaviours assessed",
            "Speak-up/whistleblowing mechanism tested for accessibility and independence",
            "Ethical failures and near-misses tracked and trended",
            "Culture findings reported to the Audit Committee",
        ],
        "banking_application": "Private banking culture assessments should cover: RM compensation incentives vs. suitability obligations, pressure on compliance team independence, treatment of whistleblowers, and Board effectiveness. Poor culture was a root cause in multiple private banking regulatory enforcement cases (2015-2023).",
        "topical_requirement": True,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "TR-4",
        "domain": "Topical Requirements",
        "title": "Environmental, Social and Governance (ESG)",
        "description": "Internal auditors must include ESG risks in the audit universe and assess the adequacy of ESG governance, data quality, and regulatory compliance. ESG risks are increasingly material for financial institutions.",
        "key_requirements": [
            "ESG risk universe defined and included in audit plan",
            "Climate risk assessment: physical and transition risk measurement",
            "ESG data quality and integrity (non-financial reporting accuracy)",
            "Regulatory compliance: CSRD (EU), TCFD, SFDR (for funds)",
            "Greenwashing risk in marketed ESG products assessed",
        ],
        "banking_application": "Swiss private banks managing ESG-labelled investment products must have internal audit cover: ESG product classification process, greenwashing risk controls, regulatory compliance with FINMA sustainability disclosures, and climate risk integration in credit assessments. FINMA circular on sustainability is expected in 2025.",
        "topical_requirement": True,
        "effective_date": "January 9, 2024",
    },
    {
        "standard_id": "TR-5",
        "domain": "Topical Requirements",
        "title": "Third-Party Relationships",
        "source_guide": "IIA User Guide, September 2025",
        "description": "Mandatory for all assurance engagements on third parties. Internal auditors must evaluate the organisation's governance, risk management, and control processes across the full third-party lifecycle: Selecting → Contracting → Onboarding → Monitoring → Offboarding. Risk categories: Strategic, Reputational, Ethical, Operational, Financial, Compliance, Cybersecurity/Data Protection, IT, Legal, Sustainability/ESG, Geopolitical. Structured across three sections: Governance (4), Risk Management (4), Control Processes (9).",
        "key_requirements": [
            "G-A/B: Risk-based approach and standardised policies for full lifecycle",
            "RM-B: Regular risk ranking and due diligence across all risk categories",
            "CP-A: Background checks including cybersecurity, financial, criminal, political",
            "CP-B: Contract clauses: right-to-audit, NDA, SLA, BCP, AI usage, whistleblowing",
            "CP-D: Centralised listing of all vendor relationships maintained",
            "CP-F: Ongoing KPI monitoring, SLA enforcement, quarterly business reviews",
            "CP-I: Formalised offboarding: access revocation, data return/destruction, asset recovery",
        ],
        "sections": [
            {
                "section_id": "governance",
                "section_title": "Governance",
                "icon": "🏛️",
                "requirements": [
                    {
                        "id": "G-A",
                        "text": "Formalised risk-based approach for determining whether to use a third party. Periodically reviewed. Includes cost-benefit analysis, risk/control evaluation, adequate resources, and stakeholder feedback.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-01", "COBIT 2019 APO10.01", "ISO 27001 A.15.1"],
                    },
                    {
                        "id": "G-B",
                        "text": "Policies and procedures for third-party lifecycle (all 5 stages). Standardised tools and templates. Periodic review. Criteria for each stage. Regulatory alignment and benchmarking exercises.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-02, GV.SC-03", "COBIT 2019 APO10.02", "ISO 27001 A.15.2"],
                    },
                    {
                        "id": "G-C",
                        "text": "Roles and responsibilities defined. Values/ethics alignment with third party. Regular training for third-party management roles. Three Lines Model alignment.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-04", "COBIT 2019 APO10.03", "NIST 800-53 SA-9"],
                    },
                    {
                        "id": "G-D",
                        "text": "Timely stakeholder communication throughout lifecycle. Includes board, senior management, procurement, operations, risk, compliance, legal, IT, HR. Cross-functional meetings on third-party management.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-07", "COBIT 2019 BAI08", "NIST 800-53 PM-9"],
                    },
                ],
            },
            {
                "section_id": "risk_management",
                "section_title": "Risk Management",
                "icon": "⚠️",
                "requirements": [
                    {
                        "id": "RM-A",
                        "text": "Standardised and comprehensive risk management processes: Identification → Analysis → Mitigation → Monitoring. Risk management committee with board oversight. Corrective actions for deviations.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-09", "COBIT 2019 APO12.01", "NIST 800-53 RA-3"],
                    },
                    {
                        "id": "RM-B",
                        "text": "Regular risk identification and assessment throughout lifecycle. Risk ranking and prioritisation. Due diligence process and vendor questionnaires. Factors: criticality, financial materiality, relationship duration, subcontracting.",
                        "frameworks": ["NIST CSF 2.0 ID.RA-09, GV.SC-06", "COBIT 2019 APO10.04", "NIST 800-53 SA-9(3)"],
                    },
                    {
                        "id": "RM-C",
                        "text": "Risk responses (mitigation, acceptance, elimination, sharing) commensurate with risk ranking. Documented responses including third-party control environment. Conflicts of interest addressed.",
                        "frameworks": ["NIST CSF 2.0 GV.RM-06", "COBIT 2019 APO10.05", "NIST 800-53 SA-9(1)"],
                    },
                    {
                        "id": "RM-D",
                        "text": "Escalation processes for third-party risks. Risk level definitions and escalation procedures. Financial and non-financial impact consideration. Periodic reassessment when risk appetite changes.",
                        "frameworks": ["NIST CSF 2.0 GV.RM-07, GV.SC-09", "COBIT 2019 APO12.06", "NIST 800-53 RA-7"],
                    },
                ],
            },
            {
                "section_id": "control_processes",
                "section_title": "Control Processes",
                "icon": "🔒",
                "requirements": [
                    {
                        "id": "CP-A",
                        "text": "Due diligence for sourcing and selecting: competitive bidding, RFPs, sole sourcing criteria. Background checks: cybersecurity, financial, criminal, legal records, political ties. Cross-functional review teams. SOC reports review. No advance to contracting without completed due diligence.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-06, ID.RA-09", "COBIT 2019 APO10.02", "NIST 800-53 SA-4"],
                    },
                    {
                        "id": "CP-B",
                        "text": "Contracting policies followed. Key risks in contract clauses. Essential elements: NDA, termination clauses, cybersecurity requirements, breach notification, SLAs, right-to-audit (including downstream subcontractors), AI usage, change management process, sustainability clauses, whistleblowing protocols, BCP requirements.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-10", "COBIT 2019 APO10.03", "NIST 800-53 SA-9(3), SA-12"],
                    },
                    {
                        "id": "CP-C",
                        "text": "Contracts reviewed/approved by legal and compliance. Signed by authorised individuals. Stored securely. Contract manager assigned.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-10", "COBIT 2019 APO10.03", "NIST 800-53 SA-9"],
                    },
                    {
                        "id": "CP-D",
                        "text": "Centralised listing of all third-party relationships maintained (contract management system). Processes for adding/removing contracts. Tracking system for issues with vendors.",
                        "frameworks": ["NIST CSF 2.0 ID.AM-07, GV.SC-03", "COBIT 2019 APO10.01", "NIST 800-53 SA-9(6)"],
                    },
                    {
                        "id": "CP-E",
                        "text": "Documented onboarding processes. System integration assessment. Technology compatibility and security. BCP assessment of third party. Complementary user entity controls (SOC reporting).",
                        "frameworks": ["NIST CSF 2.0 GV.SC-05", "COBIT 2019 BAI07", "NIST 800-53 SA-9(1)"],
                    },
                    {
                        "id": "CP-F",
                        "text": "Ongoing monitoring of vendor performance vs contract objectives. KPIs evaluation, payment controls, cost-benefit analysis, SLA penalty enforcement, periodic risk ranking reevaluation. Quarterly business reviews. Additional monitoring: financial stability, complaints, ISO certifications, media inquiries, AI/cybersecurity protocols, segregation of duties.",
                        "frameworks": ["NIST CSF 2.0 ID.RA-09, DE.CM-06", "COBIT 2019 APO10.05", "NIST 800-53 SA-9(4)"],
                    },
                    {
                        "id": "CP-G",
                        "text": "Corrective action protocols when third party fails to meet contract or increases risk. Escalation based on severity. Post-incident review with root cause analysis.",
                        "frameworks": ["NIST CSF 2.0 RS.CO-04", "COBIT 2019 APO10.05", "NIST 800-53 IR-4"],
                    },
                    {
                        "id": "CP-H",
                        "text": "Contract expiration and renewal monitoring. Auto-renewal review: performance, terms, risk factors.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-10", "COBIT 2019 APO10.04", "NIST 800-53 SA-9"],
                    },
                    {
                        "id": "CP-I",
                        "text": "Formalised offboarding plan. Termination process. Replacement if necessary. Data return or destruction. Access revocation (systems, tools, facilities). Asset return (devices, licenses, IP, documentation). Escalation to board when terminated for cause.",
                        "frameworks": ["NIST CSF 2.0 GV.SC-05, PR.AA-04", "COBIT 2019 APO10.06", "NIST 800-53 SA-9, PS-4"],
                    },
                ],
            },
        ],
        "framework_mapping": ["NIST CSF 2.0", "NIST SP 800-53 Rev.5", "COBIT 2019", "ISO 27001"],
        "banking_application": "FINMA RS 2018/3: outsourcing register mandatory for Swiss banks, right-to-audit clause required in all material contracts, FINMA notification for critical outsourcing. DORA Art. 28–44: ICT third-party risk management framework, Register of Information for all ICT providers, mandatory notification to EBA for concentration risk. MAS Notice 655 / SS2/21 (PRA): outsourcing requirements. Fourth-party risk is critical for custody, core banking (Temenos, Avaloq), portfolio management (Murex, Bloomberg), and cloud providers — concentration risk in private banking technology. Right-to-audit must flow down to sub-contractors in all material outsourcing contracts.",
        "topical_requirement": True,
        "effective_date": "January 9, 2024",
    },
]

# ── Audit Tests Library ───────────────────────────────────────────────────────
AUDIT_TESTS_LIBRARY = {
    "AML_KYC": [
        {
            "id": "T001", "level": "Critical", "category": "Standard",
            "objective": "Verify completeness of CDD/EDD files for all active clients",
            "procedure": "Extract full client list from CRM segmented by risk rating. Test (a) 100% of PEP-flagged clients and all High-risk clients (typically 30-100 files); (b) statistical sample of 60 Standard-risk files using random number generation. Review each file for: KYC form, government-issued ID copy, source of wealth narrative with supporting evidence, source of funds, risk rating rationale, and last periodic review date vs. required cycle.",
            "population": "All active client files (~1,200), segmented: High-risk/PEP (~50-100), Standard-risk (~1,100)",
            "sample_size": "100% of High-risk and PEP clients + statistical sample of 60 Standard-risk files (~10% coverage)",
            "failure_criteria": "Any High-risk or PEP file missing mandatory CDD document; any file overdue for periodic review by >3 months; Standard-risk deficiency rate >5%",
        },
        {
            "id": "T002", "level": "Critical", "category": "Standard",
            "objective": "Test adequacy of PEP screening and adverse media checks",
            "procedure": "For sampled clients, verify PEP status in system vs. external World-Check/Refinitiv database. Check adverse media search performed at onboarding and annually. Review EDD file completeness for all PEPs.",
            "population": "All PEP-flagged clients and new onboardings in the last 12 months",
            "sample_size": "100% of PEPs (full population, typically 10-30 clients)",
            "failure_criteria": "PEP not identified, EDD incomplete, or adverse media not checked",
        },
        {
            "id": "T003", "level": "High", "category": "Data Analytics",
            "objective": "Detect unusual transaction patterns indicative of structuring or layering",
            "procedure": "Extract all transactions > CHF 5,000 for 12 months. Run structuring detection algorithm (multiple sub-threshold transactions within 24h). Flag accounts with velocity anomalies (>3 SD from peer group). Review flagged transactions against SAR log.",
            "population": "All client transactions for 12-month period",
            "sample_size": "100% population (data analytics — full dataset)",
            "failure_criteria": "Flagged transactions not in SAR/STR log or not investigated within 5 business days",
        },
        {
            "id": "T004", "level": "High", "category": "Standard",
            "objective": "Verify STR/SAR filing timeliness and quality",
            "procedure": "Request STR register for the period. For each STR, verify: date of suspicion vs. date of filing (must be ≤30 days in CH). Review narrative quality checklist. Compare number of STRs vs. peer benchmark.",
            "population": "All STRs filed in the 12-month review period",
            "sample_size": "100% of STRs filed (typically 3-15)",
            "failure_criteria": "Filing delay >30 days, incomplete narrative, or missing client account detail",
        },
        {
            "id": "T005", "level": "Moderate", "category": "Standard",
            "objective": "Assess effectiveness of transaction monitoring rule calibration",
            "procedure": "Obtain TMS alert statistics for the period: total alerts, false positive rate, escalation rate, SAR conversion rate. Interview compliance team on rule review frequency. Compare alert thresholds against FINMA/MAS guidance.",
            "population": "All TMS alerts generated in 12-month period",
            "sample_size": "Analytical review (statistics) + 25 alerts (random sample)",
            "failure_criteria": "False positive rate >95%, no rule review in 12 months, or escalation backlog >30 days",
        },
    ],
    "CYBER_RISK": [
        {
            "id": "T011", "level": "Critical", "category": "Standard",
            "objective": "Verify MFA enforcement on all privileged and remote-access accounts",
            "procedure": "Extract list of all admin accounts from Active Directory / IAM system. Cross-reference with MFA enrollment logs. Verify MFA applied to VPN, cloud consoles, banking applications, and SWIFT. Test bypass scenarios with IT team.",
            "population": "All privileged accounts (IT admin, DB admin, SWIFT operators) — typically 50-150",
            "sample_size": "100% of privileged accounts (full population)",
            "failure_criteria": "Any admin or remote-access account without MFA enrolled and enforced",
            "tr_reference": "TR-Cyber CP-E",
        },
        {
            "id": "T012", "level": "Critical", "category": "Standard",
            "objective": "Test patch management — critical CVE remediation within SLA",
            "procedure": "Run vulnerability scan output (Qualys/Nessus) for 6-month period. Identify Critical/High CVEs by detection date. Cross-reference patch deployment date from CMDB/ITSM. Calculate remediation lead time vs. SLA (Critical: ≤15 calendar days, High: ≤30 calendar days). Note exceptions granted through formal change management.",
            "population": "All systems in scope: servers, network devices, endpoints (typically 200-500 assets)",
            "sample_size": "100% of Critical CVEs + random 25 High CVEs",
            "failure_criteria": "Any Critical CVE not patched within 15 calendar days or High CVE within 30 calendar days without documented exception and compensating control",
            "tr_reference": "TR-Cyber CP-D, CP-E",
        },
        {
            "id": "T013", "level": "High", "category": "Data Analytics",
            "objective": "Detect privileged access anomalies — logins outside business hours or from unusual locations",
            "procedure": "Extract 6 months of SIEM/PAM logs for privileged accounts. Identify logins outside 07:00-20:00 local time and logins from unusual geographies. Calculate baseline per user and flag deviations >2 SD. Review flagged events vs. approved change records.",
            "population": "All privileged account activity logs for 6-month period",
            "sample_size": "100% population (data analytics)",
            "failure_criteria": "Unexplained after-hours logins or foreign-IP logins without approved change record",
            "tr_reference": "TR-Cyber RM-C, CP-E",
        },
        {
            "id": "T014", "level": "High", "category": "Standard",
            "objective": "Assess incident response plan completeness and last test date",
            "procedure": "Review IRP documentation: scope, escalation tree, communication plan, DORA/FINMA notification timeline. Verify tabletop or live exercise conducted within last 12 months. Review lessons-learned log from last exercise.",
            "population": "IRP documentation set + last 3 incident records",
            "sample_size": "Full documentation review + interview IT Security and Compliance",
            "failure_criteria": "IRP not tested in 12 months, DORA notification timelines missing, or escalation list outdated",
            "tr_reference": "TR-Cyber RM-F",
        },
        {
            "id": "T015", "level": "Moderate", "category": "Standard",
            "objective": "Review third-party / vendor access — segregation and deprovisioning",
            "procedure": "Obtain list of all vendors with system access. For each, verify: access limited to required systems (least privilege), time-limited credentials, and formal termination process. Sample 10 terminated vendors — confirm access revoked within 24h.",
            "population": "All vendors with active system access (typically 20-80)",
            "sample_size": "100% active vendor review + 10 terminated vendor access checks",
            "failure_criteria": "Vendor with broader access than justified, or active credentials post-termination",
            "tr_reference": "TR-Cyber CP-A · TR-Third CP-E, CP-F",
        },
    ],
    "CREDIT_RISK": [
        {
            "id": "T021", "level": "Critical", "category": "Standard",
            "objective": "Verify Lombard loan LTV monitoring and margin call process",
            "procedure": "Extract all Lombard facilities with LTV > 60% at quarter-end. Verify daily LTV calculation methodology. For 20 sampled facilities, trace: LTV breach date → margin call issuance → response tracking → collateral top-up or liquidation. Review override log.",
            "population": "All Lombard facilities (typically 200-600)",
            "sample_size": "100% of facilities in breach + judgmental 20 standard facilities",
            "failure_criteria": "LTV breach without margin call within 24h, or override without senior approval",
        },
        {
            "id": "T022", "level": "High", "category": "Standard",
            "objective": "Test credit underwriting — completeness of credit file and dual approval",
            "procedure": "Request new credit approvals for 12-month period. Sample 25 credit files. Verify: financial analysis present, collateral valuation signed, dual approval (RM + Credit), credit limit within delegated authority, conditions precedent documented.",
            "population": "All new credit facilities approved in 12-month period",
            "sample_size": "25 files (judgmental — skewed to larger facilities > CHF 5M)",
            "failure_criteria": "Single approval for facility requiring dual sign-off, missing financial analysis, or breach of delegated authority",
        },
        {
            "id": "T023", "level": "High", "category": "Data Analytics",
            "objective": "Identify concentration risk — single-name and sector exposures vs. limits",
            "procedure": "Extract full credit portfolio from credit risk system. Calculate top-20 single-name exposures as % of tier-1 capital. Calculate sector concentrations (real estate, energy, private equity). Compare against approved concentration limits. Trend analysis vs. prior quarter.",
            "population": "Full credit portfolio — all outstanding facilities",
            "sample_size": "100% portfolio (data analytics)",
            "failure_criteria": "Any single-name exposure >10% Tier-1, or sector concentration breaching approved limit without escalation",
        },
        {
            "id": "T024", "level": "High", "category": "Standard",
            "objective": "Review adequacy of loan loss provisioning for watch-list credits",
            "procedure": "Obtain watch-list and non-performing loan register. For sample of 15 NPLs, verify: provisioning calculation methodology, collateral haircut applied, external valuation recency (< 12 months for real estate). Compare provisions vs. ECL model output.",
            "population": "All watch-list and NPL credits",
            "sample_size": "15 NPLs (judgmental — largest exposures)",
            "failure_criteria": "Provision below ECL model estimate by >10% without documented rationale, or outdated collateral valuation",
        },
        {
            "id": "T025", "level": "Moderate", "category": "Standard",
            "objective": "Verify annual credit review completeness and timeliness",
            "procedure": "Extract list of all credit facilities with scheduled annual review date in the period. Calculate % completed on time (≤30 days late). For 20 sampled reviews, check: updated financials, revised risk rating, RM sign-off, and credit committee approval where required.",
            "population": "All facilities with annual review due in 12-month period",
            "sample_size": "100% overdue reviews + 20 on-time reviews",
            "failure_criteria": "Annual review >30 days late without documented extension, or risk rating not updated",
        },
    ],
    "OPERATIONAL_RISK": [
        {
            "id": "T031", "level": "Critical", "category": "Standard",
            "objective": "Test BCP/DR plan — recovery time vs. RTO/RPO targets",
            "procedure": "Review most recent BCP/DR test report. Verify test scope covers critical systems (core banking, SWIFT, client portal). Extract actual recovery times vs. approved RTO/RPO. Interview IT for untested scenarios. Check FINMA/MAS notification plan for prolonged outages.",
            "population": "BCP/DR documentation set + last 2 test reports",
            "sample_size": "Full review + interviews with BCP coordinator and IT",
            "failure_criteria": "Recovery time exceeding RTO, critical system excluded from test, or test not conducted in 12 months",
        },
        {
            "id": "T032", "level": "High", "category": "Standard",
            "objective": "Verify outsourcing arrangements — oversight and sub-outsourcing controls",
            "procedure": "Obtain register of all outsourced activities classified as critical/important per FINMA Circ 2018/3. For 10 vendors, verify: annual performance review, right-to-audit clause exercised, sub-outsourcing approved by senior management, and concentration risk assessed.",
            "population": "All critical/important outsourcing arrangements (typically 5-20)",
            "sample_size": "100% critical outsourcing + 10 important arrangements",
            "failure_criteria": "Missing SLA review, right-to-audit not exercised in 24 months, or unapproved sub-outsourcing",
        },
        {
            "id": "T033", "level": "High", "category": "Data Analytics",
            "objective": "Analyse operational loss event database — frequency, severity, root cause trends",
            "procedure": "Extract 3-year loss event database. Segment by event type (BCBS 7 categories). Calculate frequency and severity by category and business unit. Identify recurring root causes (control failures). Compare actual losses vs. operational VaR model output.",
            "population": "Full loss event database for 3-year period",
            "sample_size": "100% population (data analytics)",
            "failure_criteria": "Undocumented losses, events not entered within 5 days, or recurring root cause with no remediation",
        },
        {
            "id": "T034", "level": "High", "category": "Standard",
            "objective": "Review RCSA completeness and control effectiveness ratings",
            "procedure": "Obtain latest RCSA for all business lines. Verify RCSA updated within 12 months. For 15 sampled controls rated 'Effective', review supporting evidence (test results, exception reports). Assess whether residual risk ratings are consistent with loss event data.",
            "population": "RCSA for all business lines (typically 3-5 BUs)",
            "sample_size": "Full RCSA review + 15 key controls tested for evidence",
            "failure_criteria": "RCSA not updated in 12 months, or 'Effective' control with no supporting test evidence",
        },
        {
            "id": "T035", "level": "Moderate", "category": "Standard",
            "objective": "Test key person dependency — succession planning and knowledge transfer",
            "procedure": "Identify roles with single-person dependency (no documented backup). Verify succession plans for top-10 revenue-generating RMs. Review holiday/absence coverage procedures. Assess concentration of client relationships per RM.",
            "population": "All client-facing and control-function roles",
            "sample_size": "Top-10 RMs by AuM + all control function heads",
            "failure_criteria": "Role with no documented successor, RM managing >20% of total AuM without backup, or coverage plan undocumented",
        },
    ],
    "DATA_PRIVACY": [
        {
            "id": "T041", "level": "Critical", "category": "Standard",
            "objective": "Verify data retention and deletion policy compliance",
            "procedure": "Obtain data inventory / records of processing activities (RoPA). For 5 data categories (client data, transaction data, HR data, marketing data, CCTV), verify: retention period defined, deletion process automated or documented, and last deletion run completed on schedule.",
            "population": "All data categories in RoPA (typically 15-30 categories)",
            "sample_size": "Full RoPA review + 5 key categories with evidence of deletion runs",
            "failure_criteria": "Data retained beyond defined retention period, deletion not automated for large datasets, or RoPA incomplete",
        },
        {
            "id": "T042", "level": "High", "category": "Standard",
            "objective": "Test data breach detection and notification process",
            "procedure": "Review last 3 data security incidents (if any). Verify: incident detected within 24h, notification to FDPIC/GDPR authority within 72h where required, client notification process documented. If no incidents, review tabletop exercise record.",
            "population": "All data incidents reported in 12-month period + incident response procedures",
            "sample_size": "100% incidents (typically 0-5) + procedure review",
            "failure_criteria": "Notification delay >72h without documented justification, or no incident response procedure",
        },
        {
            "id": "T043", "level": "High", "category": "Data Analytics",
            "objective": "Detect unauthorised access to sensitive client data — insider threat",
            "procedure": "Extract 6 months of DLP/SIEM logs for sensitive data access (client PII, account data). Identify access events outside normal role scope. Flag bulk downloads >500 records in single session. Cross-reference with HR database for employees under notice or PIP.",
            "population": "All sensitive data access logs for 6-month period",
            "sample_size": "100% population (data analytics)",
            "failure_criteria": "Bulk download without business justification, access by terminated employees, or role misalignment",
        },
        {
            "id": "T044", "level": "High", "category": "Standard",
            "objective": "Assess cross-border data transfer safeguards",
            "procedure": "Obtain list of all cross-border data transfers (CH → EU, CH → US, etc.). For each, verify legal basis: Standard Contractual Clauses (SCCs), adequacy decision, or binding corporate rules. Check SCCs are 2021 version (post-Schrems II). Verify transfer impact assessment (TIA) conducted.",
            "population": "All international data transfers identified in RoPA",
            "sample_size": "100% of transfers to non-adequate countries",
            "failure_criteria": "Transfer to non-adequate country without SCCs, outdated SCCs (pre-2021), or no TIA",
        },
        {
            "id": "T045", "level": "Moderate", "category": "Standard",
            "objective": "Review consent management and data subject rights fulfilment",
            "procedure": "Test data subject access request (DSAR) process: submit test DSAR and measure response time (must be ≤30 days). Review consent records for marketing communications. Verify right-to-erasure process is documented and tested.",
            "population": "All DSARs received in 12-month period + consent database sample",
            "sample_size": "100% DSARs (typically 5-20) + 50 consent records sampled",
            "failure_criteria": "DSAR response time >30 days, missing consent for marketing, or no erasure process documented",
        },
    ],
    "MARKET_RISK": [
        {
            "id": "T051", "level": "Critical", "category": "Standard",
            "objective": "Verify VaR model validation and back-testing results",
            "procedure": "Review latest model validation report (must be within 12 months). Check back-test results: count VaR exceptions over 250 trading days (>4 exceptions = amber, >10 = red per Basel traffic light). Verify exceptions investigated and documented.",
            "population": "250 trading days of daily VaR vs. P&L data",
            "sample_size": "100% population (all 250 trading days)",
            "failure_criteria": ">4 VaR exceptions without documented investigation, or model validation >12 months old",
        },
        {
            "id": "T052", "level": "High", "category": "Data Analytics",
            "objective": "Detect market risk limit breaches — intraday and end-of-day",
            "procedure": "Extract 12 months of risk limit monitoring data from risk system. Identify all intraday and EOD limit breaches by desk, trader, and instrument. Calculate breach frequency and average excess. Cross-reference with override approvals and escalation log.",
            "population": "All risk limit monitoring records for 12-month period",
            "sample_size": "100% population (data analytics)",
            "failure_criteria": "Limit breach without same-day escalation to senior management, or repeated breaches by same trader without remediation",
        },
        {
            "id": "T053", "level": "High", "category": "Standard",
            "objective": "Assess stress testing programme — scenarios and management review",
            "procedure": "Review stress testing framework document. Verify: scenarios include historical (2008, COVID-19) and hypothetical (rate shock ±200bp, credit spread widening). Check management review of results at least quarterly. Assess whether results feed into capital planning.",
            "population": "Stress testing documentation + last 4 quarterly reports",
            "sample_size": "Full review + interviews with Risk Management",
            "failure_criteria": "Scenarios not reviewed in 12 months, results not reported to ALCO/Board, or no capital planning linkage",
        },
        {
            "id": "T054", "level": "High", "category": "Standard",
            "objective": "Review IRRBB measurement and hedging effectiveness",
            "procedure": "Obtain NII and EVE sensitivity reports for latest quarter. Verify IRRBB limit compliance (EVE change < 15% Tier-1 per EBA). Review hedging instruments (IRS, caps, floors) — verify hedge accounting documentation and effectiveness tests.",
            "population": "IRRBB reports + hedging portfolio",
            "sample_size": "Full analytical review + 10 largest hedging positions",
            "failure_criteria": "EVE sensitivity exceeding 15% Tier-1 without remediation plan, or hedging not documented for accounting purposes",
        },
        {
            "id": "T055", "level": "Moderate", "category": "Standard",
            "objective": "Test front-office — compliance attestation and trade surveillance alerts",
            "procedure": "Review trade surveillance system (if any) alert log for 12 months. Identify market manipulation alerts (spoofing, wash trades) and front-running alerts. Verify all alerts investigated within 5 business days. Review annual compliance attestation completion rate for traders.",
            "population": "All trade surveillance alerts for 12-month period + attestation register",
            "sample_size": "100% of medium/high alerts + attestation register",
            "failure_criteria": "Alert unresolved >5 days, attestation completion <100%, or suppressed alerts without justification",
        },
    ],
    "THIRD_PARTY_RISK": [
        {
            "id": "T061", "level": "Critical", "category": "Standard",
            "objective": "Verify critical vendor due diligence — financial stability and security posture",
            "procedure": "For all critical vendors (Tier 1), verify: annual financial review (Dun & Bradstreet or equivalent), latest ISO 27001 / SOC 2 Type II report (< 12 months), and penetration test results. Verify vendor incident notification clause and SLA penalties enforced.",
            "population": "All Tier 1 (critical) vendors — typically 5-15",
            "sample_size": "100% of Tier 1 vendors",
            "failure_criteria": "Missing ISO 27001 / SOC 2 report, outdated financial review, or no incident notification clause",
            "tr_reference": "TR-Third CP-A",
        },
        {
            "id": "T062", "level": "High", "category": "Standard",
            "objective": "Test vendor access review — principle of least privilege and credential management",
            "procedure": "For 10 active vendors with system access, verify: access scoped to required functions only, shared credentials not used, access reviewed within last 6 months. Verify process for revoking access upon contract termination (check 5 terminated vendors).",
            "population": "All vendors with active system/network access",
            "sample_size": "10 active vendors + 5 terminated vendor access checks",
            "failure_criteria": "Vendor with access beyond contractual scope, shared/generic credentials, or active access post-termination",
            "tr_reference": "TR-Third CP-E, CP-F",
        },
        {
            "id": "T063", "level": "High", "category": "Data Analytics",
            "objective": "Map vendor concentration risk — single-vendor dependencies for critical functions",
            "procedure": "Extract vendor register and classify by function (IT infrastructure, custody, payments, data, etc.). Identify single-vendor dependencies for critical functions. Calculate % of critical operations dependent on top-3 vendors. Map sub-outsourcing chains for cloud providers.",
            "population": "Full vendor register (all active vendors)",
            "sample_size": "100% population (data analytics)",
            "failure_criteria": "Single-vendor dependency for a critical function with no documented contingency, or undisclosed sub-outsourcing",
            "tr_reference": "TR-Third RM-B, CP-F",
        },
        {
            "id": "T064", "level": "Moderate", "category": "Standard",
            "objective": "Review vendor contract terms — regulatory and exit provisions",
            "procedure": "For 10 critical/important vendor contracts, verify: governing law aligned with entity jurisdiction, right-to-audit clause, data protection provisions (GDPR/nDSG), exit plan documented and tested, and business continuity requirements defined in SLA.",
            "population": "All vendor contracts for critical/important services",
            "sample_size": "10 contracts (judgmental — highest value and criticality)",
            "failure_criteria": "Missing right-to-audit, no data protection clause, or exit plan not documented",
            "tr_reference": "TR-Third CP-B, CP-C",
        },
        {
            "id": "T065", "level": "Moderate", "category": "Standard",
            "objective": "Assess vendor performance monitoring — KPIs and SLA breach management",
            "procedure": "Review vendor performance scorecards for last 4 quarters. Verify KPIs cover availability, incident response time, and data quality. For any SLA breaches, confirm penalty calculation applied and formal vendor communication documented.",
            "population": "All critical/important vendor performance reports for 12-month period",
            "sample_size": "Full review + investigation of all SLA breaches",
            "failure_criteria": "No formal performance review in 12 months, SLA breach without penalty applied, or KPIs not aligned to contractual obligations",
            "tr_reference": "TR-Third CP-F",
        },
    ],
    "GOVERNANCE": [
        {
            "id": "T071", "level": "Critical", "category": "Standard",
            "objective": "Verify Three Lines of Defence — independence and reporting lines",
            "procedure": "Review organisational chart for 2L and 3L functions. Verify Risk and Compliance (2L) report to CRO/CCO independent of business. Verify Internal Audit (3L) reports functionally to Audit Committee. Check there is no dual-hat arrangement mixing 1L and 2L roles. Review charter documents.",
            "population": "Organisational structure documentation + Board/AC minutes",
            "sample_size": "Full review + interviews with CRO, CCO, CAE, and Audit Committee Chair",
            "failure_criteria": "2L or 3L head reporting to business line CEO, dual-hat arrangement, or Internal Audit charter not approved by Audit Committee",
        },
        {
            "id": "T072", "level": "High", "category": "Standard",
            "objective": "Review Board and Audit Committee meeting effectiveness — attendance and challenge",
            "procedure": "Review last 4 AC meeting minutes. Verify: quorum met, standing agenda covers risk reports, Internal Audit findings tracked, and external audit findings discussed. Assess quality of challenge documented in minutes. Check attendance record (target: >75%).",
            "population": "All Board and Audit Committee meetings for 12-month period",
            "sample_size": "100% of AC meetings (typically 4-6 per year)",
            "failure_criteria": "Quorum not met, no documented challenge of management, or material audit finding not escalated to AC",
        },
        {
            "id": "T073", "level": "High", "category": "Standard",
            "objective": "Test management action tracking — Internal Audit findings closure",
            "procedure": "Extract open findings register from GRC system. Verify: all past-due findings escalated to AC, evidence reviewed for 'closed' findings (actual fix, not just management attestation), repeat findings identified and root-cause addressed.",
            "population": "All open and recently closed Internal Audit findings",
            "sample_size": "100% of past-due findings + 20 closed findings for evidence review",
            "failure_criteria": "Past-due finding not escalated to AC, 'closed' finding without evidence, or repeat finding from prior year",
        },
        {
            "id": "T074", "level": "High", "category": "Data Analytics",
            "objective": "Analyse conflicts of interest declarations and approval trends",
            "procedure": "Extract conflicts of interest (COI) register for 12 months. Calculate declaration rate by seniority band. Identify approved conflicts with no review date. Flag any COI involving Board members not disclosed in annual report. Compare vs. prior year trend.",
            "population": "Full COI register for the period",
            "sample_size": "100% population (data analytics)",
            "failure_criteria": "Declaration rate <95% in senior management, approved COI with no review date, or undisclosed Board-level COI",
        },
        {
            "id": "T075", "level": "Moderate", "category": "Standard",
            "objective": "Review whistleblowing mechanism — accessibility, independence, and case resolution",
            "procedure": "Verify whistleblowing channel is accessible to all employees (including third parties). Confirm third-party management (not managed by same function being reported on). Review case log for the period: intake, investigation timeline (<60 days), and resolution. Check non-retaliation policy communicated.",
            "population": "Whistleblowing policy + case log for 12-month period",
            "sample_size": "Full policy review + 100% of cases (typically 0-10)",
            "failure_criteria": "Channel managed by HR without independent oversight, case unresolved >60 days, or no non-retaliation policy",
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# REGULATORY_CALENDAR
# 2025-2026 regulatory events relevant to Swiss private banks.
# Each entry is self-contained; used by app.py Tab 0 intelligence feeds.
# ══════════════════════════════════════════════════════════════════════════════
REGULATORY_CALENDAR = [

    {
        "reg_id": "RC001",
        "authority": "European Commission / ESAs",
        "regulation": "DORA — Digital Operational Resilience Act",
        "jurisdiction": "EU",
        "type": "Entry into force",
        "date": "2025-01-17",
        "description": (
            "Full application of DORA (Regulation (EU) 2022/2554). All financial entities "
            "in scope — including EU-licensed entities of Swiss private banking groups — "
            "must comply with ICT risk management framework, incident classification and "
            "reporting (major ICT incidents within 4 hours initial report, 72 hours "
            "intermediate, 1 month final), digital operational resilience testing (TLPT "
            "for significant institutions), and ICT third-party risk management requirements "
            "including mandatory contractual clauses and register of critical ICT providers."
        ),
        "impact_private_banking": (
            "Swiss private banks with EU entities (branches, subsidiaries) face full DORA "
            "obligations. FINMA circular 2023/1 aligns broadly for Swiss-only banks. "
            "Dual compliance required for cross-border structures. TLPT (threat-led "
            "penetration testing) mandatory for institutions above significance thresholds. "
            "ICT third-party register with risk assessments required for all vendors."
        ),
        "action_required": (
            "Complete ICT risk management framework gap assessment; establish incident "
            "classification and reporting workflows with <4 hour initial notification "
            "capability; finalise ICT third-party register with contractual clause review; "
            "schedule TLPT if in scope; board approval of DORA compliance programme."
        ),
        "audit_relevance": (
            "High priority audit topic: DORA readiness assessment, ICT incident management "
            "testing, third-party ICT risk register completeness, TLPT programme adequacy. "
            "Aligns with IIA TR-2 (Cybersecurity) and TR-5 (Third-Party Relationships)."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC002",
        "authority": "Basel Committee / FINMA / EU (CRR3)",
        "regulation": "Basel IV / CRR III — Output Floor and Revised Capital Framework",
        "jurisdiction": "CH / EU",
        "type": "Entry into force",
        "date": "2025-01-01",
        "description": (
            "EU CRR3 (Capital Requirements Regulation 3) implementing Basel IV enters "
            "application on 1 January 2025. Key changes: output floor at 50% of "
            "standardised approach RWAs (rising to 72.5% by 2030), revised credit risk "
            "standardised approach, new operational risk SMA replacing AMA, FRTB "
            "trading book capital framework, revised CVA framework. Switzerland is "
            "implementing through FINMA capital ordinance amendments on aligned timeline."
        ),
        "impact_private_banking": (
            "RWA increases expected across Lombard lending, structured products (market "
            "risk FRTB), and operational risk (SMA replaces internal models). Output "
            "floor creates capital pressure for banks with sophisticated internal models. "
            "CET1 ratio impact estimated at -0.5 to -2pp for mid-tier private banks. "
            "FRTB requires fundamental trading book reclassification and new capital "
            "model approval."
        ),
        "action_required": (
            "QIS (Quantitative Impact Study) on capital ratios under new framework; "
            "trading book boundary review; FRTB model development or SA adoption "
            "decision; capital planning update for output floor phase-in to 2030; "
            "ICAAP refresh reflecting new RWA densities."
        ),
        "audit_relevance": (
            "Audit of capital adequacy framework, RWA calculation accuracy, FRTB "
            "implementation readiness, output floor monitoring, ICAAP process quality. "
            "Relevant to credit risk, market risk, and operational risk audit programmes."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC003",
        "authority": "European Parliament / Council",
        "regulation": "MiCA Phase 2 — Crypto-Asset Service Providers (CASPs)",
        "jurisdiction": "EU",
        "type": "Entry into force",
        "date": "2024-12-30",
        "description": (
            "Markets in Crypto-Assets Regulation (MiCA) full application from "
            "30 December 2024 for crypto-asset service providers (CASPs). Requires "
            "CASP authorisation from national competent authorities, capital requirements, "
            "consumer protection measures, market abuse rules for crypto-assets, "
            "and disclosure requirements. Stablecoin provisions (ART/EMT) entered "
            "into force June 2024. EU passporting available only for MiCA-licensed entities."
        ),
        "impact_private_banking": (
            "Swiss private banks offering crypto custody, trading, or advisory services "
            "to EU clients via EU entities require CASP authorisation. Passporting "
            "creates competitive advantage for EU-licensed entities vs. Swiss-only banks. "
            "Product governance and disclosure requirements for crypto-asset instruments "
            "distributed to EU clients. AML/KYC requirements integrated with AMLD."
        ),
        "action_required": (
            "Map crypto-asset services offered to EU clients; determine CASP authorisation "
            "requirement for EU entities; prepare authorisation application if required; "
            "update product governance framework for crypto instruments; review "
            "client documentation and risk disclosure standards."
        ),
        "audit_relevance": (
            "Audit of CASP authorisation status, crypto custody controls, MiCA product "
            "governance compliance, client classification for crypto services, "
            "AML/KYC adequacy for crypto onboarding (FATF Travel Rule compliance)."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC004",
        "authority": "FINMA",
        "regulation": "FINMA Circular 2023/1 — Operational Risks and Resilience",
        "jurisdiction": "CH",
        "type": "Implementation deadline",
        "date": "2025-01-01",
        "description": (
            "FINMA Circular 2023/1 on operational risks and resilience became mandatory "
            "for all FINMA-supervised institutions from 1 January 2024, with a transition "
            "period for certain provisions extending to January 2025. The circular "
            "consolidates ICT risk, business continuity, crisis management, and "
            "outsourcing requirements. Key obligations: documented critical service "
            "mapping, board-approved impact tolerance definitions, annual resilience "
            "testing, and FINMA incident reporting timelines."
        ),
        "impact_private_banking": (
            "All Swiss private banks must have completed: critical services inventory, "
            "impact tolerance definitions (maximum tolerable disruption per service), "
            "BCP testing under realistic scenarios, and ICT incident reporting procedures "
            "aligned with FINMA expectations. Third-party outsourcing arrangements "
            "must be fully documented and risk-assessed."
        ),
        "action_required": (
            "Verify critical services mapping is complete and board-approved; confirm "
            "impact tolerance definitions are documented; schedule annual resilience "
            "test if not already completed; review outsourcing register for completeness; "
            "test FINMA incident reporting workflow."
        ),
        "audit_relevance": (
            "Core operational resilience audit: critical services mapping accuracy, "
            "impact tolerance definition adequacy, BCP test results, outsourcing "
            "governance completeness. High priority given FINMA supervisory focus."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC005",
        "authority": "European Parliament / EU Member States",
        "regulation": "AMLD6 — 6th Anti-Money Laundering Directive Transposition",
        "jurisdiction": "EU",
        "type": "Implementation deadline",
        "date": "2025-07-10",
        "description": (
            "EU Member States must transpose the 6th Anti-Money Laundering Directive "
            "(AMLD6) into national law by 10 July 2025. AMLD6 establishes: harmonised "
            "list of predicate offences for money laundering (22 categories including "
            "cybercrime and environmental crime), extended criminal liability to legal "
            "persons, minimum 4-year imprisonment for ML conviction, and enhanced "
            "cross-border cooperation provisions. Accompanied by AML Regulation "
            "(directly applicable without transposition) from 2027."
        ),
        "impact_private_banking": (
            "Swiss private banks with EU entities must update AML risk frameworks to "
            "reflect expanded predicate offence list (cybercrime and environmental "
            "crime as ML predicates require enhanced monitoring). Legal person "
            "liability increases institutional risk for compliance failures. "
            "Enhanced beneficial ownership transparency requirements."
        ),
        "action_required": (
            "Update AML risk typologies to include cybercrime and environmental crime "
            "as predicate offences; review transaction monitoring rules for new "
            "predicate categories; update legal person beneficial ownership procedures; "
            "brief compliance and front-office on enhanced obligations."
        ),
        "audit_relevance": (
            "AML audit scope expansion: predicate offence coverage in transaction "
            "monitoring, beneficial ownership procedures for legal entities, "
            "staff training adequacy on extended predicate offences."
        ),
        "priority": "Medium",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC006",
        "authority": "EU Anti-Money Laundering Authority (AMLA)",
        "regulation": "AMLA — Direct Supervision Launch",
        "jurisdiction": "EU",
        "type": "Entry into force",
        "date": "2025-07-01",
        "description": (
            "The EU Anti-Money Laundering Authority (AMLA) becomes operational, "
            "headquartered in Frankfurt. AMLA will directly supervise the highest-risk "
            "obliged entities across the EU — approximately 40 institutions selected "
            "based on cross-border presence, risk profile, and AUM. Full supervisory "
            "powers (inspections, sanctions, binding measures) operative from 2028. "
            "2025–2027: AMLA builds capabilities and coordinates with national supervisors "
            "through joint supervisory teams. Swiss banks with EU operations will be "
            "subject to AMLA coordination even if not directly supervised."
        ),
        "impact_private_banking": (
            "Swiss private banking groups with significant EU AML/CFT footprint face "
            "potential direct AMLA supervision. AMLA establishes common AML/CFT "
            "supervisory standards across EU — raising minimum expectations for "
            "all institutions serving EU clients. Enhanced cross-border enforcement "
            "coordination increases extraterritorial risk for AML failures."
        ),
        "action_required": (
            "Assess likelihood of direct AMLA supervision (cross-border presence, "
            "risk profile); strengthen AML/CFT framework to AMLA's expected standards; "
            "monitor AMLA guidance publications; ensure EU entity AML governance "
            "aligned with emerging AMLA supervisory expectations."
        ),
        "audit_relevance": (
            "AML governance audit: EU entity AML framework quality, cross-border "
            "AML coordination, preparation for potential AMLA inspection methodology."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC007",
        "authority": "FCA (UK)",
        "regulation": "FCA Consumer Duty — Annual Board Report Requirement",
        "jurisdiction": "UK",
        "type": "Implementation deadline",
        "date": "2025-07-31",
        "description": (
            "FCA Consumer Duty (PS22/9), effective July 2023, requires firms to produce "
            "annual Board reports assessing consumer outcomes. By 31 July 2025, all "
            "FCA-authorised firms must have completed their second annual Consumer Duty "
            "Board report, demonstrating evidence-based assessment of consumer outcomes "
            "across the four outcome areas: products/services, price/value, consumer "
            "understanding, and consumer support. FCA has signalled enhanced supervisory "
            "scrutiny of report quality in 2025."
        ),
        "impact_private_banking": (
            "Swiss private banks with UK FCA authorisation (wealth management, "
            "private banking licences) must produce compliant Board reports. "
            "Consumer Duty extends to distribution chain — banks distributing "
            "products through FCA-authorised intermediaries must evidence value "
            "assessment. Private banking 'professional clients' partially exempt "
            "but retail-classified HNWI clients fully in scope."
        ),
        "action_required": (
            "Complete Consumer Duty outcomes monitoring data collection by Q2 2025; "
            "draft Board report with evidence across four outcome areas; Board "
            "approval by 31 July 2025; FCA MI pack for regulatory review if requested. "
            "Update distribution chain assessments for third-party products."
        ),
        "audit_relevance": (
            "Consumer Duty audit: outcomes monitoring data quality, Board report "
            "completeness, value assessment methodology, distribution chain oversight, "
            "complaints and vulnerability data integration."
        ),
        "priority": "Medium",
        "status": "DEADLINE PASSED",
    },

    {
        "reg_id": "RC008",
        "authority": "MAS (Singapore)",
        "regulation": "MAS Technology Risk Management Guidelines — Revised Edition",
        "jurisdiction": "SG",
        "type": "Review",
        "date": "2025-Q2",
        "description": (
            "MAS is consulting on an updated Technology Risk Management (TRM) Guidelines "
            "framework in 2025, expected to publish final version H1 2025. Updates "
            "expected to cover: AI/ML model risk governance, cloud risk management "
            "(critical deployment scenarios), software supply chain security, "
            "and cyber resilience metrics. MAS Notice 655 (Technology Risk — "
            "Banks) will be updated in alignment. Singapore private banks must "
            "implement within 12 months of final publication."
        ),
        "impact_private_banking": (
            "Swiss private banks with Singapore operations must update TRM governance "
            "to incorporate AI/ML risk, enhanced cloud provider assessment, "
            "and software supply chain security. Overlap with DORA principles "
            "for EU-exposed institutions enables consolidated compliance approach."
        ),
        "action_required": (
            "Monitor MAS consultation response; gap assess current TRM against "
            "proposed revisions; plan AI/ML risk governance framework enhancements; "
            "review cloud provider contracts for new MAS requirements; "
            "update incident reporting procedures to MAS timelines."
        ),
        "audit_relevance": (
            "Technology risk audit for Singapore entities: TRM compliance gap, "
            "AI/ML model inventory, cloud risk assessment, cyber incident "
            "reporting capability."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC009",
        "authority": "FATF",
        "regulation": "FATF Mutual Evaluation — Switzerland 4th Round Follow-Up",
        "jurisdiction": "CH",
        "type": "Review",
        "date": "2025-Q3",
        "description": (
            "FATF's fourth round mutual evaluation of Switzerland (published 2016, "
            "follow-up reviews ongoing) continues with a 2025 enhanced follow-up "
            "assessment focusing on Switzerland's progress on key deficiencies: "
            "beneficial ownership transparency, STR filing rates, and effectiveness "
            "of AML supervision. FATF's updated methodology (2024) places greater "
            "emphasis on outcomes/effectiveness over technical compliance. "
            "Adverse ratings could impact Switzerland's standing and trigger "
            "enhanced due diligence by correspondent banks."
        ),
        "impact_private_banking": (
            "Adverse FATF finding on Switzerland would increase international "
            "correspondent banking friction, trigger enhanced due diligence "
            "requirements from EU and US banks, and could prompt FINMA enforcement "
            "of specific deficiencies. Beneficial ownership transparency requirements "
            "likely to be tightened following FATF feedback."
        ),
        "action_required": (
            "Benchmark STR filing rates against industry and FATF expectations; "
            "audit beneficial ownership identification completeness; review "
            "MROS reporting quality and timeliness; assess correspondent bank "
            "relationship risk if Swiss FATF rating deteriorates."
        ),
        "audit_relevance": (
            "AML effectiveness audit: STR quality and quantity, beneficial ownership "
            "coverage, high-risk jurisdiction controls — aligned with FATF effectiveness "
            "assessment methodology."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC010",
        "authority": "EBA",
        "regulation": "EBA EU-Wide Stress Test 2025",
        "jurisdiction": "EU",
        "type": "Review",
        "date": "2025-Q3",
        "description": (
            "EBA biennial EU-wide stress test exercise for significant institutions. "
            "2025 exercise will test bank resilience under adverse macroeconomic scenarios "
            "designed by the ESRB. Scenarios expected to incorporate: higher-for-longer "
            "interest rate environment, commercial real estate correction, geopolitical "
            "stress (trade fragmentation), and climate transition risks. "
            "Results publication expected Q3 2025. Swiss banks with EU subsidiaries "
            "above EUR 30B threshold participate; FINMA conducts parallel domestic stress test."
        ),
        "impact_private_banking": (
            "Swiss private banking groups with large EU entities participate directly. "
            "Stress test results influence Pillar 2 capital requirements and supervisory "
            "intensity. FINMA uses parallel exercise results for Swiss entities. "
            "Climate scenario inclusion raises bar for climate risk quantification."
        ),
        "action_required": (
            "Prepare stress test data submission infrastructure; model climate "
            "transition scenarios; validate credit, market, and operational risk "
            "stress models against EBA adverse scenario; engage with supervisors "
            "on model assumptions. Internal parallel run recommended Q1 2025."
        ),
        "audit_relevance": (
            "Stress testing audit: model documentation, data quality, scenario "
            "coverage, governance of stress test results, climate risk integration."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC011",
        "authority": "ECB / SSM",
        "regulation": "ECB Supervisory Priorities 2025–2027",
        "jurisdiction": "EU",
        "type": "Review",
        "date": "2025-Q1",
        "description": (
            "ECB Banking Supervision published its supervisory priorities for 2025–2027 "
            "covering three strategic themes: (1) resilience to macro-financial and "
            "geopolitical shocks — credit quality, IRRBB, capital adequacy; "
            "(2) timely remediation of deficiencies — governance, risk data aggregation "
            "(BCBS 239), and IT/cyber; (3) progress on digital transformation and "
            "climate risk. Banks under SSM supervision (including Swiss banking groups "
            "with significant EU subsidiaries) will receive supervisor-specific "
            "engagement letters based on these priorities."
        ),
        "impact_private_banking": (
            "ECB-supervised entities within Swiss banking groups face targeted "
            "on-site inspections and model investigations aligned with these priorities. "
            "Credit quality, IRRBB, governance, and cyber/IT are highest-probability "
            "inspection topics. BCBS 239 risk data aggregation deficiencies "
            "specifically targeted."
        ),
        "action_required": (
            "Gap assess credit portfolio quality against ECB expectations; "
            "test IRRBB models under ECB-specified scenarios; advance BCBS 239 "
            "data aggregation remediation; prepare for cyber inspection using "
            "TIBER-EU framework. Align internal audit plan with ECB priority areas."
        ),
        "audit_relevance": (
            "Direct alignment opportunity: Internal Audit can provide pre-inspection "
            "assurance on ECB priority areas — credit quality, IRRBB, governance, "
            "IT/cyber, and climate risk — creating regulatory value from audit planning."
        ),
        "priority": "High",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC012",
        "authority": "European Commission / EFRAG",
        "regulation": "CSRD — Corporate Sustainability Reporting Directive",
        "jurisdiction": "EU",
        "type": "Implementation deadline",
        "date": "2025-01-01",
        "description": (
            "CSRD reporting obligations expand in 2025: large EU companies (>500 employees "
            "OR >EUR 40M revenue OR >EUR 20M assets) report on FY2024 under ESRS standards, "
            "with first reports published 2025. Swiss companies with EU-listed securities "
            "or large EU subsidiaries included. ESRS (European Sustainability Reporting "
            "Standards) require double materiality assessment, TCFD-aligned climate "
            "disclosures, biodiversity, social, and governance reporting. "
            "Limited assurance from auditors required from first year."
        ),
        "impact_private_banking": (
            "Swiss private banking groups with EU-listed entities or large EU subsidiaries "
            "face CSRD reporting. Double materiality assessment requires new process. "
            "TCFD climate metrics (Scope 1/2/3 GHG, PCAF-based financed emissions) "
            "require data collection from client portfolios. Private bank as reporter "
            "AND as data provider to corporate clients subject to CSRD."
        ),
        "action_required": (
            "Complete double materiality assessment if not done; align ESRS data "
            "collection with reporting calendar; implement PCAF methodology for "
            "financed emissions; engage external assurance provider; integrate "
            "CSRD reporting into existing annual report process."
        ),
        "audit_relevance": (
            "Sustainability reporting audit: double materiality assessment quality, "
            "ESRS data completeness, financed emissions calculation methodology, "
            "assurance readiness, greenwashing risk in disclosures."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC013",
        "authority": "FCA (UK)",
        "regulation": "UK TCFD Mandatory Climate Disclosure — Annual Review",
        "jurisdiction": "UK",
        "type": "Review",
        "date": "2025-Q2",
        "description": (
            "UK TCFD-aligned climate disclosures became mandatory for premium-listed "
            "companies and large asset managers from 2022, with scope extended to "
            "additional categories in 2023–2024. FCA is conducting a 2025 review "
            "of disclosure quality across regulated firms, with particular focus on "
            "scenario analysis quality, Scope 3/financed emissions reporting, and "
            "transition plan credibility. FCA has indicated enforcement action "
            "for misleading climate disclosures under the Market Abuse framework."
        ),
        "impact_private_banking": (
            "Swiss private banks with UK FCA-regulated asset management entities "
            "face TCFD disclosure obligations and FCA quality review. Financed "
            "emissions reporting (Scope 3 Category 15) requires client portfolio "
            "data collection. Transition plan commitments must be credible and "
            "evidenced — vague net-zero pledges will attract FCA scrutiny."
        ),
        "action_required": (
            "Update TCFD disclosure with 2024 data; enhance scenario analysis "
            "(minimum 2 scenarios: Paris-aligned and 'current policies'); "
            "strengthen financed emissions methodology (PCAF alignment); "
            "document transition plan milestones with measurable targets."
        ),
        "audit_relevance": (
            "Climate risk and TCFD audit: scenario analysis methodology, financed "
            "emissions data quality, transition plan implementation, greenwashing "
            "risk in UK disclosures."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC014",
        "authority": "European Parliament / Council",
        "regulation": "EU AI Act — Financial Services Application",
        "jurisdiction": "EU",
        "type": "Entry into force",
        "date": "2025-08-01",
        "description": (
            "EU AI Act (Regulation 2024/1689) enters application progressively: "
            "prohibited AI practices banned from 2 February 2025; high-risk AI "
            "system requirements (Annex III) applying to financial services from "
            "August 2026; GPAI model obligations from August 2025. Financial services "
            "AI applications classified as high-risk include: creditworthiness assessment, "
            "insurance risk scoring, and AI in employment decisions. "
            "The European AI Office is developing sector-specific guidance for "
            "financial services institutions (expected 2025)."
        ),
        "impact_private_banking": (
            "AI models used in credit scoring (Lombard LTV assessment), client "
            "risk profiling (suitability), AML transaction monitoring, and "
            "fraud detection may be classified as high-risk under Annex III. "
            "High-risk classification requires: conformity assessment, registration "
            "in EU AI database, technical documentation, human oversight mechanisms, "
            "and post-market monitoring."
        ),
        "action_required": (
            "Inventory all AI/ML models in use; classify against EU AI Act risk "
            "categories; implement AI governance framework for high-risk systems; "
            "document model cards and technical documentation; plan conformity "
            "assessment process; monitor European AI Office sector guidance."
        ),
        "audit_relevance": (
            "AI governance audit: model inventory completeness, risk classification "
            "accuracy, high-risk system documentation, human oversight controls, "
            "explainability and bias testing for client-facing AI models."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC015",
        "authority": "OECD / SECO / Swiss Federal Tax Administration",
        "regulation": "CRS / FATCA Annual Reporting Deadline 2025",
        "jurisdiction": "CH",
        "type": "Implementation deadline",
        "date": "2025-06-30",
        "description": (
            "Annual CRS (Common Reporting Standard) and FATCA reporting deadline "
            "for Swiss Reporting Financial Institutions. CRS data for calendar year "
            "2024 must be submitted to the Swiss Federal Tax Administration (ESTV) "
            "by 30 June 2025 for transmission to 105+ partner jurisdictions. "
            "FATCA data (IDES submission) follows US IRS deadline of 31 July 2025. "
            "ESTV has increased audit activity on reporting quality, including "
            "self-certification staleness and account classification accuracy."
        ),
        "impact_private_banking": (
            "All Swiss private banks are Reporting Financial Institutions. "
            "Accuracy of account holder classification (tax residency, entity "
            "classification), self-certification currency, and reportable account "
            "identification are key compliance metrics. ESTV spot audits of "
            "classification methodology are increasing."
        ),
        "action_required": (
            "Complete self-certification refresh campaign for stale certifications "
            "(>3 years without update); validate account classification logic; "
            "run pre-submission data quality checks; confirm IDES registration "
            "and FATCA reporting infrastructure is operational; file by deadlines."
        ),
        "audit_relevance": (
            "Tax compliance audit: CRS/FATCA self-certification completeness and "
            "currency, account classification accuracy, reportable account "
            "identification, submission timeliness and data quality."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC016",
        "authority": "Basel Committee on Banking Supervision (BCBS)",
        "regulation": "FRTB — Fundamental Review of the Trading Book",
        "jurisdiction": "EU / CH",
        "type": "Entry into force",
        "date": "2025-01-01",
        "description": (
            "FRTB (BCBS 457) enters EU application via CRR3 on 1 January 2025 "
            "(with full capital requirements phased). Trading book boundary rules "
            "become mandatory: instruments must be assigned to trading or banking "
            "book with strict transfer limitations. Standardised Approach (SA-FRTB) "
            "mandatory as floor; IMA (Internal Model Approach) requires per-desk "
            "approval. Expected Shortfall replaces VaR; non-modellable risk factors "
            "(NMRFs) create capital add-ons for illiquid instruments. "
            "Switzerland aligns FINMA capital ordinance with EU CRR3 timeline."
        ),
        "impact_private_banking": (
            "Structured product hedging desks and FX/rates treasury operations "
            "face fundamental capital model changes. SA-FRTB increases capital "
            "for complex derivatives and illiquid positions common in private "
            "bank treasury. IMA approval requires per-desk backtesting and P&L "
            "attribution tests. NMRFs create capital charges for bespoke structured "
            "product components."
        ),
        "action_required": (
            "Complete trading book classification exercise; implement SA-FRTB "
            "calculation engine; submit IMA application for eligible desks "
            "if applicable; adapt risk systems to Expected Shortfall; establish "
            "NMRF identification and capital charge process; update ICAAP."
        ),
        "audit_relevance": (
            "Market risk audit: FRTB trading book boundary compliance, SA-FRTB "
            "calculation accuracy, IMA model adequacy (if applicable), NMRF "
            "identification completeness, capital reporting accuracy."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC017",
        "authority": "FINMA",
        "regulation": "FINMA Supervisory Priorities 2025",
        "jurisdiction": "CH",
        "type": "Review",
        "date": "2025-Q1",
        "description": (
            "FINMA published its supervisory priorities for 2025 focusing on: "
            "(1) credit and real estate risk — Lombard and mortgage concentration; "
            "(2) operational and cyber resilience — DORA/FINMA 2023/1 implementation; "
            "(3) AML/CFT — beneficial ownership quality and STR effectiveness; "
            "(4) sustainable finance — greenwashing risk and FinSA ESG integration; "
            "(5) digital assets — FINMA guidance on tokenisation and crypto custody. "
            "On-site inspections and document reviews will be concentrated in these areas."
        ),
        "impact_private_banking": (
            "All FINMA-supervised private banks should align internal audit plans "
            "with FINMA priorities to provide pre-inspection assurance. Credit "
            "risk, cyber resilience, and AML are highest-probability inspection "
            "topics. ESG and digital assets signal growing supervisory expectations "
            "in these areas."
        ),
        "action_required": (
            "Align internal audit plan 2025 with FINMA priority areas; ensure "
            "documentation readiness for potential FINMA on-site inspection; "
            "brief Board and senior management on supervisory focus areas; "
            "conduct self-assessment against FINMA inspection methodology."
        ),
        "audit_relevance": (
            "Direct audit planning input: FINMA priorities define the highest-value "
            "audit topics for 2025. Internal audit providing assurance on FINMA "
            "priority areas maximises regulatory value and manages inspection risk."
        ),
        "priority": "High",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC018",
        "authority": "SFC (Hong Kong)",
        "regulation": "SFC — Virtual Asset Regulatory Framework Expansion",
        "jurisdiction": "HK",
        "type": "Review",
        "date": "2025-Q2",
        "description": (
            "Hong Kong's SFC is expanding the virtual asset (VA) regulatory framework "
            "following VASP licensing regime implementation (June 2023). 2025 developments: "
            "VA OTC derivatives regulation (SFC-HKMA joint guidelines expected Q1 2025), "
            "enhanced stablecoin licensing regime (HKMA Bills progressing), "
            "tokenised securities framework updates, and retail VA product distribution "
            "requirements. SFC has signalled increased VA enforcement activity. "
            "Swiss banks with Hong Kong operations or SFC licences are affected."
        ),
        "impact_private_banking": (
            "Swiss private banks with HK entities offering VA custody, trading, "
            "or advisory services must maintain VASP licence compliance and "
            "adapt to OTC derivatives and stablecoin rule changes. "
            "Tokenised securities distribution requires SFC product authorisation. "
            "Retail distribution of VA products subject to enhanced suitability requirements."
        ),
        "action_required": (
            "Monitor SFC/HKMA VA regulatory updates; review VASP licence conditions "
            "for compliance with expanding requirements; assess stablecoin exposure "
            "against HKMA licensing regime; update VA product governance framework."
        ),
        "audit_relevance": (
            "HK entity VA audit: VASP licence compliance, VA custody controls, "
            "OTC VA derivatives risk management, stablecoin exposure assessment."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC019",
        "authority": "PRA (UK)",
        "regulation": "PRA Operational Resilience — Implementation Deadline",
        "jurisdiction": "UK",
        "type": "Implementation deadline",
        "date": "2025-03-31",
        "description": (
            "PRA/FCA Operational Resilience Policy (PS6/21) requires all PRA-regulated "
            "firms to be fully within impact tolerances for all important business "
            "services by 31 March 2025. From this date, firms must not only have "
            "defined impact tolerances but must demonstrate they can stay within them "
            "during severe but plausible disruption scenarios. Three-year build-out "
            "period (2022–2025) ends; supervisory intensity increases post-deadline. "
            "Firms failing to meet deadline must immediately notify supervisors."
        ),
        "impact_private_banking": (
            "Swiss private banks with PRA-regulated UK entities face the March 2025 "
            "deadline as a hard regulatory obligation. Important business service "
            "mapping, impact tolerance testing, and scenario testing must be "
            "complete. Post-March 2025, firms will be expected to demonstrate "
            "within-tolerance performance in live disruption events."
        ),
        "action_required": (
            "Complete important business service mapping and impact tolerance testing; "
            "document scenario test results demonstrating within-tolerance performance; "
            "ensure Board attestation of operational resilience compliance; "
            "establish continuous monitoring of important business services; "
            "prepare for PRA supervisory engagement on resilience evidence."
        ),
        "audit_relevance": (
            "Operational resilience audit (UK): important business service mapping "
            "completeness, impact tolerance test evidence, scenario testing rigour, "
            "Board attestation process, continuous monitoring capability."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC020",
        "authority": "FINMA",
        "regulation": "FINMA RS 2023/1 — Climate and Nature-Related Financial Risks",
        "jurisdiction": "CH",
        "type": "Implementation deadline",
        "date": "2025-01-01",
        "description": (
            "FINMA is developing climate risk supervisory expectations (building on "
            "TCFD and NGFS frameworks) to be published as guidance in 2025. "
            "Expectation: banks integrate physical and transition climate risks "
            "into ICAAP, risk appetite, and stress testing. FINMA's 2024 survey "
            "identified significant gaps in Swiss banks' climate risk quantification "
            "and scenario analysis capabilities. Formal circular expected 2025–2026; "
            "supervisory reviews of climate risk integration underway in 2025."
        ),
        "impact_private_banking": (
            "Private banks must demonstrate climate risk integration in credit "
            "portfolio assessment (physical risk on real estate collateral, "
            "transition risk on carbon-intensive sectors), IRRBB (green asset "
            "repricing), and operational risk (physical climate impacts on "
            "infrastructure). TCFD reporting aligned with FINMA expectations required."
        ),
        "action_required": (
            "Complete TCFD-aligned climate risk assessment; integrate physical risk "
            "into real estate collateral valuation; assess transition risk in "
            "credit portfolio (sector-level); run climate scenario analysis in "
            "ICAAP; establish climate risk data infrastructure for ongoing monitoring."
        ),
        "audit_relevance": (
            "Climate risk audit: TCFD disclosure quality, physical risk integration "
            "in credit assessment, transition risk scenario analysis, ICAAP climate "
            "risk chapter adequacy, financed emissions data quality."
        ),
        "priority": "Medium",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC021",
        "authority": "MAS (Singapore)",
        "regulation": "MAS Notice 626 — AML/CFT for Banks (Amendment) 2025",
        "jurisdiction": "SG",
        "type": "Review",
        "date": "2025-Q1",
        "description": (
            "MAS is reviewing and amending Notice 626 (Prevention of Money Laundering "
            "and Countering the Financing of Terrorism — Banks) in 2025. Expected "
            "amendments include: enhanced beneficial ownership requirements for "
            "legal arrangement clients (trusts, foundations), updated high-risk "
            "country lists, enhanced correspondent banking due diligence, and "
            "strengthened virtual asset-related AML provisions. Singapore's "
            "2024 FATF mutual evaluation results are driving specific amendments."
        ),
        "impact_private_banking": (
            "Singapore private banking entities of Swiss groups must update "
            "AML procedures for trust/foundation clients, high-risk jurisdictions, "
            "and crypto-related client activities. Correspondent banking relationships "
            "require enhanced due diligence documentation. Staff training update required."
        ),
        "action_required": (
            "Monitor MAS Notice 626 consultation outcome; gap assess procedures "
            "against expected amendments; update trust/foundation KYC procedures; "
            "review high-risk country list and exposure; update correspondent "
            "banking risk assessment. Implementation within MAS transition period."
        ),
        "audit_relevance": (
            "Singapore AML audit: Notice 626 compliance, trust/foundation KYC "
            "quality, correspondent banking due diligence, high-risk jurisdiction "
            "controls, virtual asset AML procedures."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC022",
        "authority": "EBA / European Commission",
        "regulation": "EBA AML/CFT Package — Single Rulebook",
        "jurisdiction": "EU",
        "type": "Consultation",
        "date": "2025-Q2",
        "description": (
            "The EU AML/CFT Single Rulebook — the AML Regulation (AMLR, directly "
            "applicable from 2027) complementing AMLD6 — is being developed through "
            "EBA Level 2 measures and guidelines throughout 2025. EBA will publish "
            "consultation papers on: customer due diligence standards, beneficial "
            "ownership verification methods, transaction monitoring calibration "
            "expectations, and PEP identification methodologies. These will become "
            "binding EU-wide standards from 2027."
        ),
        "impact_private_banking": (
            "EU AML regulation creates harmonised, directly applicable AML standards "
            "superseding national transpositions. Higher floor for beneficial ownership "
            "verification, CDD standards, and transaction monitoring will require "
            "framework updates by 2027. Early adoption of AMLR standards reduces "
            "transition risk. Swiss banks must align EU entities."
        ),
        "action_required": (
            "Engage with EBA consultations on key provisions; assess current AML "
            "framework against draft AMLR standards; identify gaps requiring "
            "remediation by 2027; consider early adoption for EU entities to "
            "reduce transition risk. Engage industry body responses."
        ),
        "audit_relevance": (
            "Future audit scope: AMLR compliance readiness, beneficial ownership "
            "verification quality, transaction monitoring calibration against "
            "EBA expectations, PEP programme adequacy."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC023",
        "authority": "HKMA",
        "regulation": "HKMA Stablecoin Regulation — Legislative Framework",
        "jurisdiction": "HK",
        "type": "Entry into force",
        "date": "2025-Q2",
        "description": (
            "Hong Kong's Stablecoins Ordinance is progressing through LegCo (expected "
            "enactment H1 2025). The HKMA will license fiat-referenced stablecoin (FRS) "
            "issuers. Banks wishing to issue or hold FRS as principal must comply with "
            "licensing requirements. Custody of licensed FRS for clients will be "
            "regulated. Unlicensed FRS will be prohibited for use in HK financial "
            "markets. HKMA sandbox participants (including bank-affiliated stablecoin "
            "projects) must transition to full licensing regime."
        ),
        "impact_private_banking": (
            "HK entities of Swiss banks holding stablecoins in client portfolios "
            "must assess licensing status of each stablecoin. Unlicensed stablecoin "
            "exposure must be managed. Banks considering stablecoin issuance "
            "partnerships must assess HKMA licensing requirements. Client "
            "stablecoin product offering requires product governance update."
        ),
        "action_required": (
            "Inventory client stablecoin holdings; assess licensing status under "
            "HK regime; update product governance for stablecoin instruments; "
            "review custody arrangements; monitor HKMA sandbox and licensing "
            "timeline; brief HK entity Board on regulatory change."
        ),
        "audit_relevance": (
            "Digital assets audit (HK): stablecoin client exposure assessment, "
            "product governance compliance, custody control adequacy, "
            "HKMA licensing compliance for any stablecoin activities."
        ),
        "priority": "Medium",
        "status": "IN FORCE",
    },

    {
        "reg_id": "RC024",
        "authority": "FSB (Financial Stability Board)",
        "regulation": "FSB Crypto-Asset Recommendations — Implementation Monitoring",
        "jurisdiction": "Global",
        "type": "Review",
        "date": "2025-Q3",
        "description": (
            "FSB published final high-level recommendations for crypto-asset "
            "activity regulation and global stablecoin oversight in October 2023. "
            "2025: FSB monitoring review of jurisdictional implementation progress. "
            "Recommendations cover: regulatory perimeter for crypto, cross-border "
            "cooperation, stablecoin reserve and governance standards, and "
            "DeFi risks. FSB report will assess gaps and may escalate to G20 "
            "for further policy action. MiCA (EU), FIT21 (US under consideration), "
            "and HK stablecoin framework are key jurisdictional responses."
        ),
        "impact_private_banking": (
            "FSB implementation review creates risk of additional regulatory "
            "requirements in key jurisdictions (US, Asia) beyond MiCA. Banks "
            "with global crypto-asset services should monitor FSB findings "
            "for advance indication of regulatory direction. Cross-border "
            "crypto supervision coordination implications for compliance frameworks."
        ),
        "action_required": (
            "Monitor FSB implementation review findings; assess regulatory "
            "landscape in all jurisdictions where crypto services are offered; "
            "scenario plan for US crypto regulation (FIT21 or alternative); "
            "maintain adaptable compliance framework for global crypto operations."
        ),
        "audit_relevance": (
            "Crypto risk audit: regulatory compliance across jurisdictions, "
            "cross-border crypto governance consistency, preparedness for "
            "regulatory change in non-MiCA jurisdictions."
        ),
        "priority": "Low",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC025",
        "authority": "Basel Committee on Banking Supervision (BCBS)",
        "regulation": "BCBS 239 — Risk Data Aggregation and Reporting (Supervisory Reviews)",
        "jurisdiction": "Global",
        "type": "Review",
        "date": "2025-Q2",
        "description": (
            "BCBS published its 10-year progress report on Principles for Effective "
            "Risk Data Aggregation and Risk Reporting (BCBS 239) in 2023, finding "
            "that G-SIBs remain substantially non-compliant. In 2025, supervisors "
            "(ECB, FINMA, PRA, BIS) are conducting targeted reviews of BCBS 239 "
            "implementation at significant institutions. Key deficiencies: "
            "data lineage documentation, aggregation accuracy for complex portfolios, "
            "timeliness of management reporting in stress conditions, and "
            "IT architecture supporting single authoritative data sources."
        ),
        "impact_private_banking": (
            "Swiss private banking groups designated as G-SIBs or D-SIBs face "
            "direct supervisory review. Mid-tier private banks face indirect "
            "pressure through correspondent bank reporting requirements and "
            "FINMA data reporting expectations. Data aggregation weakness is "
            "the most common finding in FINMA and ECB on-site inspections."
        ),
        "action_required": (
            "Conduct BCBS 239 gap assessment against all 11 principles; "
            "prioritise data lineage documentation and single-source-of-truth "
            "architecture for key risk metrics; establish board-approved BCBS 239 "
            "remediation roadmap; demonstrate stress-condition reporting capability."
        ),
        "audit_relevance": (
            "Risk data audit: BCBS 239 principles compliance, data lineage, "
            "aggregation accuracy, management information quality, IT architecture "
            "supporting authoritative data sources. High regulatory exposure topic."
        ),
        "priority": "High",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC026",
        "authority": "European AI Office / EBA",
        "regulation": "EU AI Act — Financial Services Sector Guidance",
        "jurisdiction": "EU",
        "type": "Consultation",
        "date": "2025-Q3",
        "description": (
            "The European AI Office (established under the AI Act) is developing "
            "sector-specific guidance for financial services, expected for consultation "
            "Q3 2025 and finalisation H1 2026. Guidance will clarify: classification "
            "of financial services AI use cases as high-risk, conformity assessment "
            "methodology for credit and AML models, human oversight requirements "
            "for automated client-facing decisions, and GPAI model obligations "
            "for large language model deployments in financial services."
        ),
        "impact_private_banking": (
            "Clarification of AI Act scope will determine which AI/ML models require "
            "full high-risk conformity assessment (potentially credit scoring, "
            "AML monitoring, suitability engines, fraud detection models). "
            "GPAI model obligations affect banks using large LLMs for internal "
            "productivity or client communication. Timeline and cost of compliance "
            "will crystallise from guidance."
        ),
        "action_required": (
            "Engage with consultation process; complete preliminary AI model "
            "inventory and risk classification; develop AI governance framework "
            "proportional to anticipated guidance; assess LLM use cases against "
            "GPAI model obligations. Do not wait for final guidance — "
            "draft governance framework now to reduce implementation timeline."
        ),
        "audit_relevance": (
            "AI governance pre-implementation audit: model inventory completeness, "
            "preliminary risk classification, governance framework adequacy, "
            "human oversight controls for automated decisions."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC027",
        "authority": "FATF",
        "regulation": "FATF Guidance on Virtual Assets and VASPs — 2025 Update",
        "jurisdiction": "Global",
        "type": "Review",
        "date": "2025-Q2",
        "description": (
            "FATF is updating its guidance on virtual assets and Virtual Asset Service "
            "Providers (VASPs) in 2025, following the 2023 targeted update. Focus areas: "
            "DeFi AML obligations, NFT regulatory perimeter, Travel Rule implementation "
            "progress review (only 50% of jurisdictions have implemented), "
            "and updated guidance on crypto-asset risk assessment methodologies. "
            "FATF will publish a Travel Rule implementation status report, "
            "potentially triggering enhanced due diligence requirements for "
            "institutions in non-compliant jurisdictions."
        ),
        "impact_private_banking": (
            "Swiss private banks with crypto services must comply with FATF Travel "
            "Rule (originator/beneficiary information for crypto transfers >USD/EUR 1,000). "
            "Updated guidance on DeFi and NFTs may expand AML perimeter. "
            "Travel Rule implementation assessment affects correspondent banking "
            "relationships with VASP counterparties in non-compliant jurisdictions."
        ),
        "action_required": (
            "Assess Travel Rule implementation completeness (SREA, OpenVASP, or "
            "proprietary solution); review DeFi exposure in client portfolios "
            "for AML implications; update VA AML procedures against updated FATF "
            "guidance; monitor non-compliant jurisdiction list for EDD implications."
        ),
        "audit_relevance": (
            "Crypto AML audit: Travel Rule compliance, VASP due diligence, "
            "chain analytics integration, DeFi exposure assessment, "
            "NFT AML procedures."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC028",
        "authority": "FINMA / Swiss Federal Council",
        "regulation": "Swiss FMIA — OTC Derivatives Reporting and Clearing Obligations",
        "jurisdiction": "CH",
        "type": "Review",
        "date": "2025-Q2",
        "description": (
            "The Swiss Financial Market Infrastructure Act (FMIA) derivatives framework "
            "is under review in 2025, with the Federal Council expected to propose "
            "amendments to align reporting requirements with EU EMIR Refit standards. "
            "Key changes under consideration: expanded reporting fields (ISO 20022 "
            "alignment), enhanced counterparty identifier requirements (LEI mandatory "
            "for all derivatives), and updated clearing thresholds. Current FMIA "
            "reporting obligations already cover FX, rates, equity, credit, and "
            "commodity derivatives for banks above thresholds."
        ),
        "impact_private_banking": (
            "Swiss private banks above FMIA clearing/reporting thresholds must "
            "maintain compliant trade reporting to registered trade repositories. "
            "EMIR Refit alignment changes require system updates (new fields, "
            "ISO 20022 message formats). LEI mandatory for all counterparties "
            "requires client LEI collection programme."
        ),
        "action_required": (
            "Monitor FMIA amendment consultation; assess reporting infrastructure "
            "against expected EMIR Refit-aligned changes; complete client LEI "
            "collection for derivatives counterparties; plan system updates "
            "for new reporting fields. Engage with trade repository on "
            "transition timeline."
        ),
        "audit_relevance": (
            "Derivatives reporting audit: FMIA reporting completeness, LEI "
            "coverage, reporting accuracy and timeliness, clearing threshold "
            "monitoring, trade repository reconciliation."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC029",
        "authority": "EBA",
        "regulation": "EBA Guidelines on Outsourcing Arrangements — 2025 Review",
        "jurisdiction": "EU",
        "type": "Review",
        "date": "2025-Q3",
        "description": (
            "EBA is reviewing its Guidelines on Outsourcing Arrangements (EBA/GL/2019/02) "
            "in 2025 to align with DORA's third-party ICT risk requirements and "
            "incorporate learnings from supervisory practice. Expected revisions: "
            "enhanced cloud outsourcing provisions (data location, exit strategy), "
            "strengthened intragroup outsourcing standards, updated concentration "
            "risk management expectations, and alignment of outsourcing register "
            "requirements with DORA ICT third-party register. "
            "Consultation expected Q2 2025, final guidelines Q4 2025."
        ),
        "impact_private_banking": (
            "EU entities of Swiss private banks must align outsourcing governance "
            "with updated EBA guidelines. DORA-EBA alignment reduces dual compliance "
            "burden for ICT outsourcing but may increase requirements for "
            "non-ICT outsourcing. Concentration risk management expectations "
            "for core banking platform providers are expected to tighten."
        ),
        "action_required": (
            "Monitor EBA consultation; gap assess current outsourcing register "
            "and governance against expected revisions; strengthen cloud "
            "outsourcing documentation; develop vendor concentration risk framework; "
            "update exit strategy documentation for critical vendors."
        ),
        "audit_relevance": (
            "Outsourcing governance audit: EBA guideline compliance, cloud "
            "outsourcing controls, exit strategy adequacy, concentration risk "
            "assessment, intragroup outsourcing documentation."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC030",
        "authority": "FINMA",
        "regulation": "FINMA — FinSA/FinIA Implementation Review 2025",
        "jurisdiction": "CH",
        "type": "Review",
        "date": "2025-Q2",
        "description": (
            "FINMA is conducting a structured review of Financial Services Act (FinSA) "
            "and Financial Institutions Act (FinIA) implementation quality across "
            "supervised institutions in 2025. Focus areas: client segmentation accuracy, "
            "suitability assessment process quality, documentation completeness for "
            "advisory mandates, inducement/retrocession disclosure, and ESG preference "
            "integration (mandatory since January 2024). The review may result in "
            "enforcement actions or enhanced supervisory requirements for institutions "
            "with material deficiencies."
        ),
        "impact_private_banking": (
            "All Swiss private banks providing investment services must demonstrate "
            "FinSA compliance across the full client lifecycle. Client segmentation, "
            "suitability documentation, and ESG preference integration are highest "
            "deficiency-rate areas based on FINMA pre-review indications. "
            "Retrocession disclosure completeness is a specific focus area."
        ),
        "action_required": (
            "Conduct internal FinSA compliance self-assessment; audit sample of "
            "advisory mandate documentation for completeness; verify ESG preference "
            "assessment is captured for all relevant client interactions since "
            "January 2024; review retrocession disclosure processes; "
            "correct identified deficiencies before FINMA review."
        ),
        "audit_relevance": (
            "Investment suitability audit: FinSA documentation quality, "
            "client segmentation accuracy, ESG preference integration, "
            "retrocession disclosure, mandate drift monitoring. "
            "High-value audit given FINMA supervisory focus."
        ),
        "priority": "High",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC031",
        "authority": "Swiss Federal Council / FINMA",
        "regulation": "Swiss 'Too Big to Fail' (TBTF) Framework — Post-CS Revision",
        "jurisdiction": "CH",
        "type": "Consultation",
        "date": "2025-Q2",
        "description": (
            "Following the Credit Suisse emergency rescue, the Swiss Federal Council "
            "commissioned a comprehensive review of the TBTF framework. Key proposals "
            "under consultation: enhanced gone-concern capital requirements for "
            "systemically important banks, strengthened FINMA early intervention powers, "
            "revised Emergency Liquidity Assistance (ELA) framework including Public "
            "Liquidity Backstop (PLB) legislation, and enhanced senior management "
            "accountability provisions. UBS — now the only Swiss G-SIB — faces "
            "potentially significant capital surcharges under revised framework."
        ),
        "impact_private_banking": (
            "Directly affects UBS and systemically important Swiss cantonal banks. "
            "Indirectly affects private banks: enhanced FINMA powers create "
            "potential for broader intervention authority; PLB framework may "
            "affect interbank funding costs; senior manager accountability "
            "provisions may be extended to non-TBTF institutions in revised "
            "FINMA governance guidelines."
        ),
        "action_required": (
            "Monitor consultation outcome; assess implications of enhanced FINMA "
            "powers for own supervisory relationship; review senior manager "
            "accountability framework in anticipation of broader application; "
            "brief Board on TBTF reform implications for sector."
        ),
        "audit_relevance": (
            "Governance and capital audit: senior manager accountability "
            "framework adequacy, capital planning under potential revised "
            "requirements, recovery plan adequacy, liquidity backstop arrangements."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC032",
        "authority": "Swiss Banking Act / FINMA",
        "regulation": "FINMA Beneficial Ownership Transparency Requirements",
        "jurisdiction": "CH",
        "type": "Review",
        "date": "2025-Q3",
        "description": (
            "Following FATF's 4th round Switzerland evaluation and EU AMLA pressure, "
            "Switzerland is enhancing beneficial ownership transparency requirements. "
            "Proposals under consultation: expanded shareholder register obligations "
            "for unlisted Swiss companies, enhanced beneficial owner identification "
            "for complex legal structures (foundations, collective investment schemes), "
            "and strengthened FINMA authority to verify beneficial ownership data "
            "quality. FINMA has made beneficial ownership a specific 2025 "
            "inspection priority for private banks."
        ),
        "impact_private_banking": (
            "Private banks onboarding clients through complex structures "
            "(Swiss and foreign foundations, trusts, SPVs) must demonstrate "
            "enhanced beneficial owner verification procedures. FINMA on-site "
            "inspections will specifically test quality of beneficial ownership "
            "evidence files. Remediation of legacy accounts with inadequate "
            "documentation is a time-sensitive priority."
        ),
        "action_required": (
            "Audit sample of complex structure accounts for beneficial ownership "
            "documentation quality; remediate gaps in legacy accounts; "
            "update procedures for foundation and trust onboarding; "
            "implement periodic beneficial ownership re-verification triggers; "
            "prepare for FINMA beneficial ownership inspection."
        ),
        "audit_relevance": (
            "AML beneficial ownership audit: documentation quality for complex "
            "structures, re-verification processes, foundation/trust KYC "
            "procedures, FATF FATF-aligned assessment methodology."
        ),
        "priority": "High",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC033",
        "authority": "European Commission / ESMA",
        "regulation": "ESMA MiFID II Suitability Guidelines — 2025 Review",
        "jurisdiction": "EU",
        "type": "Review",
        "date": "2025-Q3",
        "description": (
            "ESMA is reviewing its Guidelines on MiFID II Suitability Requirements "
            "(ESMA35-43-3172) in 2025, with particular focus on: AI and automation "
            "in suitability assessments, sustainability (ESG) preference integration "
            "quality, appropriateness testing for complex products, and "
            "portfolio management mandate suitability monitoring frequency. "
            "Updated guidelines expected Q4 2025 with 12-month implementation period. "
            "National supervisors (NCAs) are already conducting suitability "
            "reviews based on ESMA's 2023 supervisory briefing."
        ),
        "impact_private_banking": (
            "EU entities of Swiss private banks must update suitability frameworks "
            "to reflect revised ESMA guidelines. ESG preference integration — "
            "already mandatory but inconsistently implemented — will face enhanced "
            "scrutiny. AI-assisted suitability engines require human oversight "
            "and explainability documentation. Portfolio drift monitoring "
            "frequency standards may increase."
        ),
        "action_required": (
            "Monitor ESMA consultation; audit current suitability process against "
            "draft revised guidelines; assess AI/automation tools for "
            "explainability requirements; implement ESG preference recording "
            "audit trail; review portfolio monitoring frequency for mandates."
        ),
        "audit_relevance": (
            "MiFID suitability audit: ESG preference integration quality, "
            "AI model oversight documentation, portfolio drift monitoring, "
            "appropriateness test coverage for complex products."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC034",
        "authority": "BCBS",
        "regulation": "BCBS Climate Risk Principles — Supervisory Implementation Review",
        "jurisdiction": "Global",
        "type": "Review",
        "date": "2025-Q4",
        "description": (
            "BCBS published Principles for the Effective Management and Supervision "
            "of Climate-Related Financial Risks in June 2022. In 2025, BCBS is "
            "conducting a global supervisory implementation review to assess "
            "banks' progress across 18 principles. Areas of focus: "
            "climate risk integration in ICAAP, scenario analysis and stress testing, "
            "credit risk assessment (physical and transition), and disclosure quality. "
            "Review findings will inform potential BCBS capital treatment for "
            "climate risk (Pillar 1 or Pillar 2 add-on) — a key policy question "
            "expected to be resolved 2025–2026."
        ),
        "impact_private_banking": (
            "Swiss private banks with significant real estate lending (physical risk) "
            "or carbon-intensive sector exposure (transition risk) face material "
            "capital implications if BCBS moves to Pillar 1 climate capital charge. "
            "Supervisory review findings from peer banks will set the bar "
            "for expected practices, influencing FINMA and ECB expectations."
        ),
        "action_required": (
            "Assess compliance with all 18 BCBS climate risk principles; "
            "enhance ICAAP climate scenario analysis; develop physical risk "
            "assessment for real estate collateral portfolios; brief Board "
            "on potential capital implications of BCBS Pillar 1 climate charge."
        ),
        "audit_relevance": (
            "Climate risk audit: BCBS principles compliance, ICAAP climate "
            "integration, physical risk assessment methodology, transition risk "
            "framework, disclosure alignment."
        ),
        "priority": "Medium",
        "status": "COMPLETED",
    },

    {
        "reg_id": "RC035",
        "authority": "Swiss Federal Tax Administration (ESTV)",
        "regulation": "DAC8 Preparation — Crypto-Asset Reporting Framework",
        "jurisdiction": "CH / EU",
        "type": "Implementation deadline",
        "date": "2026-01-01",
        "description": (
            "EU DAC8 Directive (extending AEoI to crypto-assets) requires EU member "
            "states to collect and exchange data on crypto-asset accounts from 1 January 2026. "
            "Switzerland is implementing equivalent CARF (Crypto-Asset Reporting Framework, "
            "OECD) standards on aligned timeline. Financial institutions and CASPs "
            "holding or trading crypto-assets for clients must: identify reportable "
            "accounts, collect self-certifications for crypto holders, and report "
            "transaction data and account balances annually from 2026."
        ),
        "impact_private_banking": (
            "Swiss private banks offering crypto custody or trading services must "
            "implement CARF/DAC8 reporting infrastructure by end-2025 for first "
            "reporting cycle in 2026. Client self-certification collection for "
            "crypto-asset accounts required. Integration with existing CRS/FATCA "
            "reporting infrastructure. Significant data collection challenge for "
            "banks with legacy crypto service implementations."
        ),
        "action_required": (
            "Inventory crypto-asset accounts requiring CARF reporting; design "
            "self-certification workflow for crypto clients; build or procure "
            "CARF reporting capability; integrate with existing CRS reporting "
            "infrastructure; test reporting system ahead of January 2026 deadline; "
            "client communication programme."
        ),
        "audit_relevance": (
            "Tax compliance audit (forward-looking): CARF implementation readiness, "
            "crypto account inventory completeness, self-certification collection "
            "process, reporting infrastructure testing."
        ),
        "priority": "High",
        "status": "IN FORCE",
    },

]

# ══════════════════════════════════════════════════════════════════════════════
# THEMATIC_BACKGROUND
# Strategic market-context intelligence for each audit theme.
# Used by AuditIQ to prime report narratives and opening briefings.
# ══════════════════════════════════════════════════════════════════════════════

THEMATIC_BACKGROUND = {

    "AML_KYC": {
        "theme": "AML / KYC",
        "market_context": (
            "The Swiss anti-money laundering landscape has undergone a structural reset between 2023 and 2026. "
            "The revised Anti-Money Laundering Act (AMLA) introduced stricter beneficial ownership transparency "
            "requirements, mandatory registration of bearer shares, and enhanced due diligence obligations for "
            "high-risk client segments. FINMA's revised AML circular (2024 update to AMLA circular) raised the "
            "bar on transaction monitoring calibration and documentation of risk assessments, placing Swiss private "
            "banks squarely in the crosshairs of both domestic and international scrutiny.\n\n"
            "At the international level, the Financial Action Task Force (FATF) Mutual Evaluation of Switzerland "
            "highlighted persistent deficiencies in the effectiveness of suspicious transaction reporting (STR) "
            "and in the supervision of designated non-financial businesses. The FATF grey list continues to evolve, "
            "with several jurisdictions relevant to Swiss private banking client flows — including parts of the "
            "Middle East, Southeast Asia, and Sub-Saharan Africa — subject to enhanced monitoring. Private banks "
            "with concentrated geographic client books face disproportionate exposure.\n\n"
            "Compliance expenditure has risen materially across the sector. Industry surveys estimate that "
            "mid-tier Swiss private banks now allocate CHF 8–15 million annually to AML/KYC infrastructure, "
            "encompassing technology platforms, dedicated compliance headcount, and external advisory. Despite "
            "this investment, STR filing rates in Switzerland remain below the European peer average, prompting "
            "FINMA to signal heightened supervisory focus on transaction monitoring effectiveness and the quality "
            "— not merely quantity — of STRs submitted to MROS."
        ),
        "private_banking_issues": (
            "Private banking presents a structurally elevated AML/KYC risk profile relative to retail or "
            "commercial banking. The combination of complex client ownership structures (multi-layered trusts, "
            "foundations, and special purpose vehicles domiciled across multiple jurisdictions), opaque sources "
            "of wealth in emerging-market geographies, and the high transactional autonomy granted to relationship "
            "managers creates conditions in which illicit flows can be obscured. HNWI clients routinely transact "
            "across asset classes — cash, securities, real estate, and alternative investments — within a single "
            "relationship, amplifying the monitoring surface. The pressure on relationship managers to preserve "
            "client revenue can create implicit incentives to under-escalate CDD deficiencies, a dynamic "
            "repeatedly cited in FINMA enforcement proceedings."
        ),
        "regulatory_pressure": (
            "FINMA has materially intensified AML enforcement, accounting for more than 40% of formal enforcement "
            "proceedings initiated in 2023–2025. The regulator's willingness to impose personal accountability — "
            "including industry bans on senior compliance officers — has raised the stakes of AML governance "
            "failures. The revised AMLA framework requires enhanced documentation of periodic review cycles, "
            "risk re-classification triggers, and senior management sign-off on high-risk client continuations. "
            "Simultaneously, the FATF's 40 Recommendations update and the EU's AMLD6 transposition by member "
            "states are creating de facto compliance expectations for Swiss institutions with EU client flows "
            "or EU-domiciled entities, requiring alignment of Swiss KYC standards with evolving EU norms "
            "even where direct Swiss law does not yet mandate it."
        ),
        "industry_trends": (
            "Four structural trends are reshaping AML/KYC practice in Swiss private banking. First, the "
            "industrialisation of KYC through AI-assisted entity resolution and adverse media screening has "
            "reduced manual effort but introduced model risk — institutions must now validate algorithm outputs "
            "and demonstrate explainability to regulators. Second, the proliferation of digital onboarding "
            "channels (FINMA-RS 2016/7 compliant video identification) has increased onboarding volume while "
            "compressing the time available for qualitative risk judgment. Third, the shift toward perpetual "
            "KYC (pKYC) — continuous, event-driven re-assessment rather than fixed periodic review — is gaining "
            "traction among tier-one private banks, with technology vendors offering real-time UBO registry "
            "monitoring and transactional anomaly feeds. Fourth, regulatory convergence between FINMA, EBA, and "
            "FATF on the definition of 'adequate' transaction monitoring is narrowing the space for bespoke "
            "Swiss interpretations, pushing institutions toward documented, risk-based calibration methodologies."
        ),
        "peer_incidents": (
            "The Swiss private banking sector has been marked by several high-profile AML enforcement actions "
            "in recent years. UBS faced FINMA supervisory proceedings related to legacy AML control weaknesses "
            "inherited through the Credit Suisse acquisition, requiring significant remediation investment across "
            "the combined entity's private banking platform. Julius Bär received a FINMA enforcement action in "
            "2023 citing deficiencies in its Lombard lending AML controls and client risk classification framework, "
            "resulting in a CHF 26 million fine and mandated governance remediation. Beyond Switzerland, "
            "Pictet & Cie agreed to a USD 122.9 million settlement with the US Department of Justice in 2023 "
            "related to facilitation of US tax evasion, underscoring the intersection of AML and tax compliance "
            "risk. Internationally, Danske Bank's EUR 2 billion fine and the ongoing fallout from the Wirecard "
            "collapse continue to set the benchmark for what regulators consider systemic AML failure."
        ),
        "key_statistics": [
            "Swiss private banks spend an estimated CHF 8–15 million per year on AML/KYC compliance infrastructure",
            "Switzerland's STR filing rate to MROS remains below the EU peer average, at approximately 0.04% of transactions",
            "FATF grey-list jurisdictions account for a disproportionate share of high-risk client geographies in Swiss private banking",
            "FINMA AML-related enforcement proceedings represented over 40% of all formal regulatory actions in 2023–2025",
            "Julius Bär CHF 26 million FINMA fine (2023) and Pictet USD 122.9 million DOJ settlement (2023) are the sector's headline enforcement benchmarks",
        ],
        "mckinsey_angle": (
            "From a strategic perspective, AML/KYC has crossed the threshold from pure compliance cost to "
            "competitive differentiator. Institutions that have invested in scalable, technology-enabled KYC "
            "utilities — shared data infrastructure, AI-assisted screening, and pKYC event triggers — are "
            "demonstrating materially shorter onboarding cycle times and lower per-client compliance cost "
            "without sacrificing risk quality. The strategic imperative for Swiss private bank leadership is "
            "to reframe AML investment as a client experience and operational efficiency lever, not merely "
            "a regulatory obligation. Banks that fail to modernise risk both regulatory censure and a "
            "structural cost disadvantage as the compliance burden continues to escalate."
        ),
        "tone": "professional",
    },

    "CYBER_RISK": {
        "theme": "Cyber Risk",
        "market_context": (
            "The Digital Operational Resilience Act (DORA), which entered into force across the European Union "
            "in January 2025, has fundamentally recalibrated the cyber risk governance expectations for financial "
            "institutions with EU operations or EU-domiciled clients. While Swiss private banks are not directly "
            "subject to DORA, the regulation's extraterritorial reach through third-party ICT service providers "
            "and EU subsidiary entities means that materially all significant Swiss private banks must align "
            "their cyber governance frameworks with DORA's requirements. FINMA's own Technology Risk circular "
            "(FINMA-RS 2023/1) mirrors many DORA principles, including mandatory ICT risk management frameworks, "
            "incident classification and reporting obligations, and TLPT (Threat-Led Penetration Testing) "
            "for systemically important institutions.\n\n"
            "The threat landscape facing private banking has intensified sharply. The ION Trading ransomware "
            "attack of January 2023 demonstrated that a single third-party technology provider disruption could "
            "cascade across dozens of financial institutions simultaneously, impairing cleared derivatives "
            "processing for days. The Temenos core banking platform security incident highlighted that "
            "infrastructure shared across multiple private banks creates concentrated single-point-of-failure "
            "risk. IBM's 2024 Cost of a Data Breach report put the average financial services breach cost at "
            "USD 5.9 million, a figure that excludes regulatory fines, client remediation costs, and "
            "reputational damage — all of which are materially higher in a private banking context.\n\n"
            "The attack surface for private banking institutions has expanded with the adoption of digital "
            "client portals, mobile banking platforms, and API-based connectivity to external custodians and "
            "data aggregators. At the same time, the sophistication of threat actors targeting HNWI clients "
            "and their advisors — through spear-phishing, deepfake voice authentication bypass, and social "
            "engineering via family offices — has increased materially, requiring a shift from perimeter "
            "defence to identity-centric zero-trust architectures."
        ),
        "private_banking_issues": (
            "Private banking cyber risk is distinguished by the premium value of the data at stake. HNWI "
            "client records contain not merely financial account information but consolidated wealth pictures, "
            "tax positions, family structures, and geopolitical affiliations — intelligence of significant "
            "value to state actors, organised crime, and competitors. The high degree of personalised service "
            "delivery, including email-based client communication, verbal instruction acceptance, and "
            "relationship manager autonomy, creates vulnerability vectors that are absent in more standardised "
            "retail environments. The use of legacy core banking platforms across many mid-tier Swiss private "
            "banks further compounds the exposure, as unpatched systems and proprietary integrations resist "
            "modern security controls."
        ),
        "regulatory_pressure": (
            "FINMA-RS 2023/1 imposes mandatory ICT risk management, operational resilience testing, and "
            "cyber incident reporting obligations on all supervised Swiss financial institutions. The circular "
            "requires institutions to classify ICT incidents by severity, report significant incidents to "
            "FINMA within defined timeframes, and maintain a current ICT asset inventory. DORA's parallel "
            "framework introduces mandatory TLPT every three years for in-scope institutions, binding "
            "contractual requirements for ICT third-party providers, and cross-border supervisory cooperation "
            "on cyber resilience. The EBA's Guidelines on ICT and Security Risk Management provide an "
            "additional reference framework applicable to EU-connected entities, creating a multi-jurisdictional "
            "compliance matrix for internationally active Swiss private banks."
        ),
        "industry_trends": (
            "The cyber risk landscape for private banking is being reshaped by four converging trends. "
            "Zero-trust architecture adoption is accelerating, driven by regulatory expectations and the "
            "failure of perimeter-based models against insider threats and credential-based attacks. "
            "AI-powered threat detection is being deployed at the network, endpoint, and application layers, "
            "but is simultaneously being weaponised by adversaries to craft more convincing phishing lures "
            "and automate vulnerability scanning. Cloud migration — particularly to hyperscaler platforms "
            "such as AWS and Microsoft Azure — is increasing agility but introducing new third-party "
            "concentration risks and data residency questions under Swiss banking secrecy law. Finally, "
            "the emergence of quantum computing as a medium-term threat to current encryption standards "
            "is prompting forward-looking institutions to begin post-quantum cryptography migration planning."
        ),
        "peer_incidents": (
            "The ION Trading ransomware attack (January 2023) disrupted cleared derivatives processing for "
            "over 40 financial institutions globally, demonstrating the systemic risk embedded in shared "
            "financial infrastructure. The Temenos security incident exposed vulnerabilities in core banking "
            "platforms used across multiple Swiss and European private banks, prompting emergency patching "
            "cycles and FINMA supervisory inquiries. SWIFT's ongoing publication of cyber incident learnings "
            "through its CSCF (Customer Security Controls Framework) reveals persistent authentication "
            "weaknesses at correspondent banking nodes. Domestically, several Swiss private banks have "
            "experienced targeted spear-phishing campaigns against relationship managers, with at least "
            "two confirmed cases of fraudulent SWIFT transfer initiation through compromised RM credentials "
            "in 2023–2024."
        ),
        "key_statistics": [
            "Average cost of a financial services data breach: USD 5.9 million (IBM Cost of a Data Breach Report 2024)",
            "DORA entered into force January 2025, requiring mandatory ICT risk management and TLPT for EU in-scope entities",
            "ION Trading ransomware attack (Jan 2023) disrupted operations at 40+ financial institutions globally",
            "FINMA-RS 2023/1 mandates cyber incident reporting within defined timeframes for all supervised Swiss institutions",
            "Deepfake-enabled fraud attempts against financial institutions increased by over 700% between 2022 and 2023",
        ],
        "mckinsey_angle": (
            "Cyber risk in private banking has transitioned from an IT management issue to a board-level "
            "strategic risk. The McKinsey perspective is that leading institutions are investing in three "
            "capabilities simultaneously: a modern, zero-trust security architecture that assumes breach "
            "and limits lateral movement; a mature cyber crisis response capability with board-level "
            "simulation testing; and a supply-chain security programme that extends contractual and "
            "technical controls to the full ICT vendor ecosystem. The institutions that treat DORA and "
            "FINMA-RS 2023/1 compliance as a floor rather than a ceiling will emerge with structurally "
            "superior resilience and lower tail-risk exposure."
        ),
        "tone": "professional",
    },

    "CREDIT_RISK": {
        "theme": "Credit Risk",
        "market_context": (
            "Swiss private banking credit risk is dominated by Lombard lending — collateralised lending "
            "against diversified securities portfolios — which has grown to an estimated CHF 150–200 billion "
            "in aggregate exposure across the Swiss private banking sector. The SNB's interest rate cycle, "
            "which saw the policy rate rise from negative territory to 1.75% in 2023 before declining to "
            "1.0% by mid-2025, has created a complex environment for Lombard portfolio management. Rising "
            "rates initially compressed collateral values for fixed-income-heavy portfolios, triggering "
            "margin call events not seen since the 2020 COVID volatility. The subsequent rate reduction "
            "cycle has provided partial relief but has introduced IRRBB complexity for banks with "
            "fixed-rate Lombard books.\n\n"
            "FINMA's mortgage lending circular and supplementary guidance on Lombard credit risk have "
            "raised the bar on LTV stress-testing, concentration limit governance, and margin call "
            "procedures. Institutions are now expected to demonstrate that their Lombard credit frameworks "
            "can withstand simultaneous collateral value declines and liquidity demands — the 'double "
            "shock' scenario that materialised during the Archegos Capital Management collapse in 2021, "
            "which resulted in over USD 10 billion in losses across prime brokers including Credit Suisse.\n\n"
            "Beyond Lombard, Swiss private banks with integrated wealth management and investment banking "
            "capabilities face credit risk from structured product counterparty exposures, real estate "
            "lending to HNWI clients, and, increasingly, from direct lending mandates and private credit "
            "allocations within client portfolios — creating a blurring of the traditional boundary between "
            "wealth management and credit risk management."
        ),
        "private_banking_issues": (
            "The Lombard lending model creates credit risk characteristics unique to private banking. "
            "Collateral portfolios are often illiquid — concentrated in private equity, hedge funds, or "
            "single-stock positions — creating margin call execution risk during market stress. HNWI "
            "clients with significant leverage may also have Lombard facilities at multiple institutions "
            "simultaneously, creating cross-bank concentration risks invisible to any single lender. "
            "The relationship-driven culture of private banking can create pressure on credit officers "
            "to accommodate client requests for LTV exceptions or extended margin call timelines, "
            "potentially subordinating credit discipline to client retention objectives."
        ),
        "regulatory_pressure": (
            "FINMA's Lombard lending guidelines require documented LTV frameworks with defined stress "
            "haircuts by asset class, mandatory margin call procedures, and senior credit officer approval "
            "for LTV exceptions. The Basel III final rules, being transposed into Swiss capital adequacy "
            "ordinance, introduce revised standardised approach (SA-CCR) for counterparty credit risk and "
            "tighten the treatment of illiquid collateral. The EBA's Guidelines on Loan Origination and "
            "Monitoring (applicable to EU-regulated entities within Swiss banking groups) impose additional "
            "suitability, affordability, and monitoring standards for credit exposures to retail clients, "
            "including HNWI segments classified as retail for regulatory purposes."
        ),
        "industry_trends": (
            "Four trends are reshaping credit risk management in Swiss private banking. First, the growth "
            "of real-time collateral monitoring — integrating market data feeds directly into LTV "
            "calculation engines — is reducing the lag between collateral value decline and margin call "
            "initiation. Second, the expansion of private credit as an asset class within HNWI portfolios "
            "is creating new credit risk exposures for banks offering NAV-based Lombard lending against "
            "illiquid private credit fund holdings. Third, the concentration of Lombard books in "
            "technology and emerging-market equities during the 2021–2022 period, followed by sharp "
            "corrections, has prompted comprehensive back-testing of haircut adequacy. Fourth, "
            "ESG-linked Lombard facilities — where pricing is tied to portfolio sustainability scores "
            "— are introducing novel collateral valuation and monitoring challenges."
        ),
        "peer_incidents": (
            "The Archegos Capital Management collapse (March 2021) remains the defining credit risk event "
            "for private banking, with Credit Suisse sustaining a USD 5.5 billion loss from concentrated "
            "total return swap exposures that were inadequately stress-tested and poorly governed. The "
            "incident exposed the absence of cross-bank collateral visibility and the failure of prime "
            "brokerage credit risk frameworks to capture family office concentration risk. Separately, "
            "several Swiss private banks experienced Lombard margin call failures during the March 2020 "
            "COVID liquidity shock, when concentrated positions in investment-grade bonds — normally "
            "considered low-risk Lombard collateral — declined sharply in simultaneous selling. FINMA "
            "subsequently issued supervisory guidance requiring enhanced stress scenarios for bond "
            "collateral under liquidity-driven market dislocations."
        ),
        "key_statistics": [
            "Estimated Swiss private banking Lombard lending market: CHF 150–200 billion in aggregate exposure",
            "Archegos collapse (2021): Credit Suisse loss of USD 5.5 billion from inadequately governed prime brokerage exposure",
            "SNB policy rate cycle: from -0.75% (2022) to +1.75% (2023), declining to 1.0% by mid-2025",
            "FINMA Lombard guidelines require documented LTV stress haircuts by asset class and mandatory margin call procedures",
            "Basel III final rules (Swiss CAO transposition) tighten SA-CCR treatment of illiquid Lombard collateral",
        ],
        "mckinsey_angle": (
            "Credit risk in private banking is at an inflection point. The Lombard model, which has been "
            "a primary revenue driver, is facing structural stress from rate volatility, illiquid collateral "
            "growth, and regulatory tightening. Leading institutions are investing in three strategic "
            "capabilities: real-time, cross-asset collateral monitoring with automated stress simulation; "
            "disciplined credit culture reinforcement through independent credit officer authority; and "
            "a differentiated private credit offering that extends the lending value proposition while "
            "managing illiquidity risk through structural protections. The Archegos lessons must be "
            "institutionalised — not merely as process controls, but as cultural norms around credit "
            "discipline independent of client relationship pressure."
        ),
        "tone": "professional",
    },

    "OPERATIONAL_RISK": {
        "theme": "Operational Risk",
        "market_context": (
            "The collapse of Credit Suisse in March 2023 — the largest banking failure in Swiss history "
            "and the first resolution of a global systemically important bank (G-SIB) — fundamentally "
            "altered the operational risk landscape for Swiss private banking. The failure was not "
            "attributable to a single operational failure but to a compounding of governance weaknesses, "
            "risk culture deficiencies, key-person dependencies, and business continuity gaps that "
            "accumulated over years and were exposed by a confidence crisis. FINMA's post-crisis "
            "supervisory priorities have included mandatory operational resilience self-assessments, "
            "enhanced BCP testing requirements, and heightened scrutiny of key-person risk at senior "
            "management level.\n\n"
            "FINMA-RS 2023/1 represents the most significant overhaul of operational and technology risk "
            "regulation in Switzerland in over a decade. The circular introduces a principles-based "
            "resilience framework requiring institutions to identify critical business services, map "
            "dependencies on people, processes, technology, and third parties, and demonstrate the "
            "ability to maintain those services through severe but plausible disruption scenarios. "
            "This shifts operational risk management from a loss-event cataloguing exercise to a "
            "forward-looking resilience discipline.\n\n"
            "Process automation and digitalisation — including the deployment of robotic process "
            "automation (RPA) and AI-assisted client servicing tools — are simultaneously reducing "
            "some traditional operational risks (manual keying errors, reconciliation failures) while "
            "introducing new categories: algorithm failures, model drift, and cyber-operational "
            "hybrid events. The operational risk taxonomy is being redefined in real time."
        ),
        "private_banking_issues": (
            "Swiss private banking operational risk is characterised by a high degree of key-person "
            "dependency — individual relationship managers who carry client relationships, know client "
            "preferences, and hold institutional knowledge not formally documented. The departure or "
            "incapacitation of a senior RM can trigger client attrition, regulatory scrutiny, and "
            "operational disruption simultaneously. Additionally, the bespoke nature of private banking "
            "service delivery — customised reporting, tailored investment mandates, complex multi-asset "
            "portfolios — means that process standardisation is lower than in retail banking, increasing "
            "the error rate and audit trail gaps. Succession planning at the RM and management level "
            "remains a structural weakness across the sector."
        ),
        "regulatory_pressure": (
            "FINMA-RS 2023/1 mandates a comprehensive ICT and operational risk management framework, "
            "including critical business service identification, impact tolerance definition, and "
            "regular BCP testing with documented results reported to the Board. The circular aligns "
            "with DORA's operational resilience requirements, creating a consistent framework for "
            "Swiss and EU-connected institutions. FINMA's enforcement track record on operational "
            "risk weaknesses — including the Credit Suisse supervisory proceedings and the Julius "
            "Bär governance action — demonstrates willingness to impose public censure and mandatory "
            "remediation programmes for systemic operational control failures."
        ),
        "industry_trends": (
            "Operational risk management in private banking is evolving along four axes. Operational "
            "resilience — the ability to absorb disruption and recover critical services — is displacing "
            "the traditional loss-event focus of Pillar 2 operational risk capital models. Process "
            "mining tools are enabling real-time identification of control deviations and inefficiencies "
            "in client-facing operations. The outsourcing of operational functions — including fund "
            "administration, custody, and trade settlement — to specialist service providers is "
            "transferring operational execution but retaining regulatory accountability with the bank, "
            "creating a principal–agent governance challenge. Finally, the increasing integration of "
            "ESG and sustainability considerations into operational practices is creating new "
            "non-financial risk categories around data quality and reporting integrity."
        ),
        "peer_incidents": (
            "The Credit Suisse collapse (March 2023) stands as the defining operational risk event "
            "in Swiss banking history, demonstrating how governance failures, reputational erosion, "
            "and BCP inadequacies can interact catastrophically. The Greensill Capital collapse (2021) "
            "and associated Credit Suisse supply chain finance fund crisis exposed operational risk "
            "in fund structuring, due diligence, and conflicts of interest management. Separately, "
            "several Swiss private banks experienced significant operational disruptions during the "
            "2021 Suez Canal incident-related trade finance processing backlog — a reminder that "
            "operational risk is not confined to internal systems. The WannaCry and NotPetya cyber "
            "events continue to be referenced as benchmark scenarios in operational resilience "
            "stress-testing exercises across the sector."
        ),
        "key_statistics": [
            "Credit Suisse failure (March 2023): CHF 110 billion in client outflows in Q4 2022 preceded the collapse",
            "FINMA-RS 2023/1 (effective 2024): mandates critical business service mapping and impact tolerance for all supervised banks",
            "Key-person dependency: an estimated 60–70% of Swiss private bank client relationships are held by fewer than 20% of RMs",
            "Operational losses from process failures account for approximately 30% of total operational risk capital in Swiss private banking",
            "BCP testing frequency under FINMA-RS 2023/1: at minimum annual, with results documented and reported to the Board",
        ],
        "mckinsey_angle": (
            "Operational resilience has become the defining strategic operational risk imperative for "
            "Swiss private banking leadership post-Credit Suisse. The McKinsey perspective is that "
            "institutions must move beyond compliance-driven BCP exercises to embed genuine resilience "
            "thinking into strategic planning, technology investment, and people development. The "
            "institutions best positioned for the next market disruption will be those that have "
            "mapped their critical service dependencies with precision, stress-tested their recovery "
            "capabilities with genuine severity, and addressed key-person concentration through "
            "systematic knowledge transfer and succession planning. Operational resilience is not "
            "an IT project — it is a leadership and governance commitment."
        ),
        "tone": "professional",
    },

    "DATA_PRIVACY": {
        "theme": "Data Privacy",
        "market_context": (
            "Switzerland's revised Federal Act on Data Protection (nDSG / revFADP), which entered into "
            "force on 1 September 2023, represents the most significant overhaul of Swiss privacy law "
            "in three decades. The nDSG aligns Swiss data protection standards substantially with the "
            "EU General Data Protection Regulation (GDPR), introducing new requirements for data "
            "protection impact assessments (DPIAs), mandatory breach notification to the Federal Data "
            "Protection and Information Commissioner (FDPIC), data processing records, and enhanced "
            "individual rights including the right to data portability. For Swiss private banks serving "
            "EU-domiciled clients, dual compliance with nDSG and GDPR is now the operational baseline.\n\n"
            "The intersection of data privacy and banking secrecy — a cornerstone of Swiss financial "
            "law — creates a uniquely complex compliance environment. Swiss banking secrecy provisions "
            "under Article 47 of the Banking Act impose criminal penalties for unauthorised client data "
            "disclosure, while GDPR and nDSG impose obligations to respond to data subject requests, "
            "including subject access requests (SARs) and erasure requests, that can create tension "
            "with banking secrecy retention requirements. Managing this tension requires carefully "
            "documented legal basis analysis and client-specific data retention schedules.\n\n"
            "Cloud computing adoption — accelerating across the Swiss private banking sector as "
            "institutions seek to leverage hyperscaler infrastructure for cost efficiency and "
            "capability development — introduces data residency, cross-border transfer, and "
            "sub-processor management challenges that are intensifying FDPIC and FINMA scrutiny "
            "of data governance frameworks."
        ),
        "private_banking_issues": (
            "Private banking data is among the most sensitive in the financial services sector. "
            "HNWI client records encompass not merely account balances but consolidated family wealth "
            "structures, tax positions, health information (for insurance and succession planning "
            "purposes), geopolitical affiliations, and politically exposed person (PEP) status. "
            "A data breach in the private banking context can have consequences extending far beyond "
            "financial loss — reputational destruction, personal safety risk for clients, and "
            "criminal exposure under banking secrecy law. The high degree of data sharing across "
            "relationship managers, investment advisors, credit officers, and compliance teams "
            "within a private bank creates extensive internal access control challenges."
        ),
        "regulatory_pressure": (
            "The FDPIC has signalled a more assertive enforcement posture following the nDSG "
            "implementation, with preliminary investigations into several financial institutions "
            "regarding cookie practices, data retention, and cross-border transfer adequacy. "
            "FINMA's supervisory expectations on data management — articulated in FINMA-RS 2023/1 "
            "and the outsourcing circular — require documented data classification, access control "
            "frameworks, and third-party data processing agreements meeting minimum security and "
            "audit rights standards. The EU's planned adequacy decision review for Switzerland "
            "remains a background risk: any adequacy decision withdrawal would impose significant "
            "compliance costs on Swiss private banks with EU client data flows."
        ),
        "industry_trends": (
            "Data privacy management in private banking is evolving across three dimensions. The "
            "adoption of data governance platforms — centralised tools for data lineage mapping, "
            "access control management, and automated SAR response — is gaining momentum as manual "
            "compliance approaches prove insufficient at scale. Privacy-by-design principles are "
            "being embedded into technology development and product design processes, driven by "
            "both regulatory expectation and competitive differentiation in a trust-sensitive "
            "client segment. Finally, the use of AI and machine learning for client analytics "
            "is creating new privacy risks — including profiling, automated decision-making, "
            "and training data governance — that are pushing data privacy teams into the "
            "front end of technology development conversations."
        ),
        "peer_incidents": (
            "The DWS greenwashing investigation (2022–2023) highlighted the reputational and "
            "regulatory consequences of data integrity failures in client-facing reporting, with "
            "EUR 25 million in fines and significant management disruption. In the banking context, "
            "the Uber data breach enforcement by European data protection authorities — resulting "
            "in EUR 290 million in fines — demonstrated the severity of cross-border transfer "
            "violations. Within Swiss banking, several institutions have received FDPIC inquiries "
            "following client data exposure incidents linked to legacy system migrations and "
            "inadequate sub-processor oversight. The ongoing litigation around LinkedIn and "
            "other social media data scraping for client prospecting purposes is a live "
            "private banking exposure that has not yet been fully resolved by regulators."
        ),
        "key_statistics": [
            "nDSG (revFADP) entered into force 1 September 2023, introducing GDPR-aligned breach notification and DPIA requirements",
            "Swiss banking secrecy (Banking Act Art. 47) imposes criminal penalties for unauthorised client data disclosure",
            "GDPR fines in the financial services sector exceeded EUR 1 billion cumulatively across EU member states by end-2024",
            "Cloud adoption in Swiss private banking: estimated 60% of tier-one institutions have active hyperscaler migration programmes",
            "FDPIC enforcement activity increased materially post-nDSG, with multiple preliminary investigations in financial services",
        ],
        "mckinsey_angle": (
            "Data privacy has evolved from a compliance checkbox to a strategic client trust asset "
            "in private banking. HNWI clients — particularly those with complex cross-border profiles "
            "— are increasingly discriminating buyers of data privacy assurance, and leading private "
            "banks are leveraging their data governance credentials as a client acquisition and "
            "retention differentiator. The strategic imperative is to build a data governance "
            "capability that is simultaneously nDSG/GDPR compliant, operationally efficient, and "
            "capable of supporting the data-intensive analytics and personalisation that define "
            "the next-generation private banking value proposition."
        ),
        "tone": "professional",
    },

    "MARKET_RISK": {
        "theme": "Market Risk",
        "market_context": (
            "The Fundamental Review of the Trading Book (FRTB), adopted into EU regulation and "
            "effective from January 2025, represents the most significant structural change to "
            "market risk capital requirements since Basel 2.5. Swiss institutions with EU trading "
            "entities are directly subject to FRTB's revised Internal Models Approach (IMA) and "
            "Standardised Approach (SA), while FINMA is expected to transpose equivalent requirements "
            "into Swiss capital ordinance in the near term. For private banks with structured product "
            "manufacturing and distribution capabilities, FRTB significantly increases the capital "
            "intensity of trading book positions and tightens the boundary between banking book "
            "and trading book classification.\n\n"
            "Interest Rate Risk in the Banking Book (IRRBB) remains a primary market risk concern "
            "following the SNB rate cycle of 2022–2025 and the instructive failures of Silicon "
            "Valley Bank (SVB) in March 2023. SVB's USD 1.8 billion loss crystallisation on "
            "held-to-maturity bond sales — triggered by deposit outflows and inadequate IRRBB "
            "hedging — demonstrated that banking book interest rate risk can become an acute "
            "solvency threat under conditions of rapid rate movement and concentrated deposit "
            "bases. Swiss private banks with significant fixed-rate lending books and "
            "interest-sensitive deposit profiles face analogous structural vulnerabilities.\n\n"
            "The write-down of Credit Suisse Additional Tier 1 (AT1) capital instruments — CHF "
            "16 billion wiped out in the March 2023 resolution — created significant mark-to-market "
            "losses for private banking clients holding AT1 securities in discretionary mandates "
            "and advisory portfolios, triggering suitability challenges and client litigation."
        ),
        "private_banking_issues": (
            "Market risk in private banking manifests primarily through the client portfolio channel "
            "rather than the proprietary trading channel. Structured products — capital protected "
            "notes, barrier reverse convertibles, and leveraged certificates — expose both the "
            "issuing institution and the client to complex market risk payoffs that are frequently "
            "misunderstood by relationship managers and inadequately stress-tested at the portfolio "
            "level. The CS AT1 write-down crystallised the risk of recommending regulatory capital "
            "instruments to clients without adequate disclosure of bail-in risk. Additionally, "
            "discretionary mandate managers face market risk through benchmark tracking error, "
            "concentration in illiquid positions, and currency risk in multi-currency portfolios."
        ),
        "regulatory_pressure": (
            "FRTB (EU, January 2025) imposes mandatory IMA desk-level approval, daily P&L "
            "attribution testing, and risk factor eligibility assessment — all of which require "
            "significant technology investment and risk infrastructure upgrading. The EBA's "
            "IRRBB guidelines (effective 2023) impose standardised interest rate shock scenarios, "
            "supervisory outlier thresholds, and enhanced ICAAP integration requirements. FINMA's "
            "supervisory priorities for 2025–2026 include explicit focus on IRRBB governance "
            "and the adequacy of structured product risk disclosure under FinSA suitability "
            "requirements — creating a dual market risk and conduct risk exposure for private "
            "banks with active structured product businesses."
        ),
        "industry_trends": (
            "Four trends are defining market risk management evolution in Swiss private banking. "
            "FRTB implementation is driving a fundamental re-architecture of risk infrastructure, "
            "with many institutions opting for third-party risk calculation engines rather than "
            "in-house builds due to complexity and cost. IRRBB management is receiving board-level "
            "attention post-SVB, with enhanced scenario analysis and hedging programme governance "
            "becoming standard practice. The proliferation of alternative risk premia strategies "
            "and systematic overlay programmes in discretionary mandates is introducing new "
            "factor-based market risk exposures that require enhanced monitoring. Finally, "
            "the integration of climate-related financial risk into market risk scenarios — "
            "including transition risk impacts on equity and credit portfolios — is creating "
            "a nascent but growing dimension of market risk management."
        ),
        "peer_incidents": (
            "Silicon Valley Bank's collapse (March 2023) — driven by USD 1.8 billion in "
            "realised losses on a HTM bond portfolio under rising rate stress — became the "
            "defining IRRBB cautionary tale, prompting supervisory letters from FINMA and "
            "the EBA to banking institutions with comparable balance sheet structures. "
            "Credit Suisse's AT1 write-down (March 2023) of CHF 16 billion created direct "
            "market risk losses for private banking clients and triggered widespread litigation "
            "regarding suitability disclosures. The Archegos Capital collapse (2021) demonstrated "
            "that concentrated equity derivative positions can crystallise market and counterparty "
            "credit losses simultaneously with insufficient warning. The 2022 UK gilt market "
            "dislocation — triggered by the Truss budget — remains a reference stress scenario "
            "for IRRBB and structured product risk management."
        ),
        "key_statistics": [
            "FRTB effective in EU from January 2025; FINMA transposition into Swiss CAO anticipated in near term",
            "SVB: USD 1.8 billion HTM bond loss realisation triggered collapse — benchmark IRRBB stress scenario",
            "Credit Suisse AT1 write-down: CHF 16 billion wiped out in March 2023 resolution, creating client portfolio losses",
            "EBA IRRBB guidelines (2023) impose standardised shock scenarios and supervisory outlier NII thresholds",
            "Structured product volumes in Swiss private banking: estimated CHF 200+ billion in outstanding notional",
        ],
        "mckinsey_angle": (
            "Market risk management in private banking is undergoing a structural upgrade driven by "
            "regulatory complexity (FRTB, IRRBB) and client liability exposure (AT1, structured "
            "products). The strategic differentiation between leading and lagging institutions will "
            "be determined by the quality of their risk infrastructure investment and the depth "
            "of their client-level risk integration — the ability to aggregate market risk across "
            "Lombard collateral, discretionary mandates, and advisory portfolios at the client "
            "relationship level. Institutions that build this integrated view will be better "
            "positioned to manage suitability risk, optimise capital allocation, and defend "
            "against client litigation in stress scenarios."
        ),
        "tone": "professional",
    },

    "THIRD_PARTY_RISK": {
        "theme": "Third-Party Risk",
        "market_context": (
            "The third-party risk landscape for Swiss private banking has been transformed by the "
            "twin forces of accelerating technology outsourcing and escalating regulatory expectations. "
            "Industry surveys indicate that mid-to-large Swiss private banks now maintain relationships "
            "with 80–120 active technology and service vendors, encompassing core banking platforms, "
            "custody and settlement infrastructure, data analytics providers, cloud hosting, and "
            "regulatory reporting utilities. This vendor proliferation has created a complex dependency "
            "map that few institutions have fully mapped at the operational level, let alone stress-tested "
            "for concentration, substitutability, and cyber-resilience.\n\n"
            "DORA's third-party provisions, effective January 2025, introduce binding contractual "
            "requirements for ICT service providers to in-scope financial institutions, mandatory "
            "concentration risk assessment for critical third-party providers (CTPPs), and a new "
            "EU-level oversight framework for systemically important ICT providers. While Swiss "
            "private banks are not directly subject to DORA, the regulation's reach through EU "
            "subsidiaries, EU-regulated correspondent banks, and EU-domiciled ICT providers "
            "creates de facto compliance pressure. FINMA's outsourcing circular (FINMA-RS 2018/3) "
            "and FINMA-RS 2023/1 impose parallel requirements under Swiss law.\n\n"
            "The concentration of Swiss private banking on a small number of core banking platforms "
            "— including Temenos, Avaloq, and FIS — creates systemic single-point-of-failure risk "
            "that is visible to FINMA and increasingly cited in supervisory discussions about "
            "sector-wide operational resilience."
        ),
        "private_banking_issues": (
            "Private banking third-party risk is amplified by the customisation-intensive nature "
            "of the service model. Bespoke integrations between core banking platforms, portfolio "
            "management systems, client reporting tools, and custody interfaces create complex, "
            "poorly documented dependency chains that are expensive to replace and difficult to "
            "monitor. The reliance on a small number of external custodians for HNWI asset "
            "safekeeping creates counterparty concentration risk, while the use of third-party "
            "introduced clients through external asset managers (EAMs) creates additional "
            "outsourced relationship management dependencies with associated conduct risk."
        ),
        "regulatory_pressure": (
            "DORA (EU, January 2025) requires mandatory mapping of ICT third-party dependencies, "
            "concentration risk assessment for CTPPs, and contractual provisions ensuring audit "
            "rights, incident notification, and service continuity. FINMA-RS 2018/3 imposes "
            "prior notification requirements for material outsourcing, minimum contractual "
            "standards, and periodic due diligence on service providers. FINMA-RS 2023/1 "
            "extends these requirements to the ICT-specific domain, requiring institutions "
            "to assess the substitutability of critical ICT providers and maintain documented "
            "exit strategies. The EBA's Guidelines on Outsourcing provide a parallel framework "
            "applicable to EU-regulated subsidiaries of Swiss banking groups."
        ),
        "industry_trends": (
            "Third-party risk management is professionalising rapidly across four dimensions. "
            "Dedicated vendor risk management platforms — offering automated due diligence, "
            "contract obligation tracking, and continuous security rating monitoring — are "
            "replacing spreadsheet-based vendor registers at leading institutions. The "
            "concentration of shared financial infrastructure on a small number of hyperscaler "
            "cloud providers (AWS, Azure, Google Cloud) is creating a new category of systemic "
            "concentration risk that regulators are monitoring with increasing concern. Exit "
            "strategy testing — actually simulating the replacement of a critical vendor — "
            "is moving from aspirational to mandatory in supervisory expectations. Finally, "
            "the integration of third-party cyber risk ratings (BitSight, SecurityScorecard) "
            "into ongoing vendor monitoring is providing a continuous signal of vendor "
            "security posture between formal due diligence cycles."
        ),
        "peer_incidents": (
            "The ION Trading ransomware attack (January 2023) disrupted cleared derivatives "
            "processing for over 40 financial institutions simultaneously, demonstrating that a "
            "single shared infrastructure provider failure can have systemic consequences. The "
            "Temenos core banking platform security incident prompted emergency patching across "
            "multiple private banks sharing the same platform version, exposing the operational "
            "risk embedded in shared technology stacks. The collapse of the third-party fund "
            "administrator Citco's operational disruptions during COVID-19 impacted NAV reporting "
            "for private banking clients with hedge fund allocations. The SolarWinds supply "
            "chain attack (2020) remains a reference scenario for assessing software supply "
            "chain risk management adequacy in vendor due diligence frameworks."
        ),
        "key_statistics": [
            "Average number of active technology and service vendors per mid-to-large Swiss private bank: 80–120",
            "DORA third-party provisions effective January 2025: mandatory CTPP mapping and concentration risk assessment",
            "ION Trading ransomware (Jan 2023): 40+ financial institutions disrupted through a single shared infrastructure failure",
            "FINMA-RS 2018/3: material outsourcing requires prior FINMA notification and documented exit strategies",
            "Swiss private banking core banking platform concentration: Temenos, Avaloq, and FIS collectively serve the majority of the sector",
        ],
        "mckinsey_angle": (
            "Third-party risk management has become a board-level strategic imperative, not merely "
            "a procurement compliance function. The McKinsey view is that leading institutions are "
            "building a differentiated capability in three areas: a comprehensive, living vendor "
            "dependency map integrated with operational resilience planning; a tiered due diligence "
            "model that applies proportionate scrutiny to critical versus non-critical vendors; and "
            "a genuine exit strategy capability tested against realistic timelines. The institutions "
            "that treat DORA and FINMA-RS 2023/1 as an opportunity to professionalise their vendor "
            "ecosystem management will build a structural resilience advantage over peers who approach "
            "third-party risk as a documentation exercise."
        ),
        "tone": "professional",
    },

    "GOVERNANCE": {
        "theme": "Governance",
        "market_context": (
            "The collapse of Credit Suisse in March 2023 produced the most consequential governance "
            "post-mortem in Swiss banking history. FINMA's public enforcement communication and the "
            "subsequent Parliamentary Investigation Commission (PUK) report identified systemic "
            "governance failures — including Board risk oversight inadequacies, management culture "
            "that suppressed escalation, serial restructuring without strategic coherence, and the "
            "marginalisation of the Chief Risk Officer function — as root causes of the bank's "
            "vulnerability. The findings have catalysed a sector-wide reassessment of governance "
            "frameworks, with FINMA increasing supervisory intensity on Board effectiveness, "
            "management culture, and the independence of control functions.\n\n"
            "FINMA's 2023–2026 supervisory strategy explicitly identifies governance and risk culture "
            "as priority themes, signalling a shift from document-based compliance assessment to "
            "qualitative evaluation of Board competency, management behaviour, and tone-from-the-top. "
            "The proportion of formal FINMA enforcement proceedings attributable to governance "
            "failures — estimated at 40% of all proceedings in 2023–2025 — underscores the "
            "regulator's willingness to hold institutions and individuals accountable for control "
            "environment deficiencies that cannot be attributed to a single rule breach.\n\n"
            "Internationally, the Senior Managers and Certification Regime (SMCR) in the UK and "
            "the EU's fit-and-proper requirements for significant institution managers are "
            "influencing Swiss supervisory expectations, particularly for institutions with "
            "UK or EU-regulated entities within their group structures."
        ),
        "private_banking_issues": (
            "Private banking governance presents specific structural vulnerabilities. The "
            "concentration of commercial power in senior relationship managers — who control "
            "client revenues and can resist compliance challenges with implicit management "
            "support — creates a governance dynamic in which the second line of defence is "
            "structurally subordinated to first-line commercial priorities. The Three Lines "
            "of Defence model, while formally adopted across the sector, frequently operates "
            "as a compliance documentation exercise rather than a genuine risk governance "
            "mechanism. Board-level expertise gaps in private banking-specific risks — including "
            "Lombard credit risk, structured product suitability, and AML — further undermine "
            "the effectiveness of Board risk oversight."
        ),
        "regulatory_pressure": (
            "FINMA-RS 2017/1 (Corporate Governance — Banks) requires Board independence, "
            "separation of Chair and CEO roles, and formal governance of conflicts of interest. "
            "FINMA's enforcement posture post-Credit Suisse has elevated personal accountability, "
            "with industry bans imposed on senior managers and compliance officers for governance "
            "failures previously treated as institutional rather than individual liability. The "
            "EBA's Guidelines on Internal Governance (applicable to EU-regulated subsidiaries) "
            "impose additional requirements on management body composition, risk committee "
            "functioning, and remuneration governance. Swiss corporate law reforms (effective "
            "2023) have also tightened shareholder rights and management accountability "
            "obligations for financial institution boards."
        ),
        "industry_trends": (
            "Four governance trends are reshaping Swiss private banking. Board risk education "
            "programmes — bringing external expertise into board discussions on cyber, AML, and "
            "credit risk — are becoming standard at tier-one institutions. The Three Lines model "
            "is being critically revisited, with several institutions restructuring their second "
            "line to give risk and compliance functions genuine veto authority over significant "
            "business decisions. Remuneration governance is under enhanced scrutiny, with "
            "FINMA requiring documented linkage between variable compensation and non-financial "
            "risk outcomes. Finally, ESG governance — board-level sustainability oversight, "
            "climate risk integration into risk appetite, and ESG committee structures — "
            "is rapidly professionalising across the sector."
        ),
        "peer_incidents": (
            "The Credit Suisse collapse (2023) is the defining governance failure case for "
            "Swiss private banking, with the FINMA enforcement communication citing serial "
            "governance weaknesses over multiple years. Julius Bär's FINMA action (2023) "
            "included governance findings related to the inadequacy of Board oversight of "
            "compliance risk and the failure of the Three Lines model to surface AML "
            "deficiencies. Internationally, the Wells Fargo fake accounts scandal and the "
            "subsequent USD 3 billion regulatory settlement remain reference cases for "
            "the consequences of governance cultures that prioritise commercial metrics "
            "over conduct standards. The Wirecard collapse (2020) — involving auditor, "
            "regulator, and board failures simultaneously — set the benchmark for multi-layer "
            "governance breakdown in a financial services context."
        ),
        "key_statistics": [
            "FINMA governance-related enforcement proceedings: estimated 40% of all formal actions in 2023–2025",
            "Credit Suisse CHF 110 billion client outflows in Q4 2022 preceded collapse — governance failures identified as root cause",
            "FINMA-RS 2017/1: mandates Board independence, Chair/CEO separation, and formal conflict of interest governance",
            "Swiss corporate law reform (effective 2023): enhanced shareholder rights and management accountability for financial institutions",
            "Julius Bär CHF 26 million FINMA action (2023) included Board-level governance findings on compliance oversight adequacy",
        ],
        "mckinsey_angle": (
            "Governance effectiveness in private banking is the meta-risk that determines whether "
            "all other risk management investments produce their intended outcomes. The McKinsey "
            "perspective is that governance transformation requires three sequential interventions: "
            "a rigorous Board effectiveness assessment that goes beyond compliance self-certification "
            "to evaluate actual risk oversight quality; a cultural diagnostic that surfaces the "
            "informal norms and incentive structures that govern real decision-making; and a "
            "structural empowerment of the control functions — compliance, risk, and internal audit "
            "— with genuine authority, adequate resources, and direct Board access. Without these "
            "foundations, process and technology investments in other risk domains will consistently "
            "underperform their potential."
        ),
        "tone": "professional",
    },

    "CROSS_BORDER": {
        "theme": "Cross-Border Compliance",
        "market_context": (
            "Cross-border tax and regulatory compliance remains one of the most complex and "
            "institutionally consequential risk dimensions in Swiss private banking. The global "
            "automatic exchange of information (AEOI) architecture — built on the OECD Common "
            "Reporting Standard (CRS) and the US Foreign Account Tax Compliance Act (FATCA) — "
            "has fundamentally altered the Swiss banking secrecy model, replacing selective "
            "disclosure with systematic, annual data exchange covering financial account "
            "information for non-resident clients. Over 100 jurisdictions now participate in "
            "CRS exchange, creating a near-universal information reporting framework that leaves "
            "limited scope for undisclosed offshore accounts.\n\n"
            "The EU's DAC8 Directive, expected to enter into force in 2026, extends automatic "
            "exchange obligations to crypto-asset reporting, closing a significant perceived "
            "gap in the AEOI framework. Swiss private banks with crypto-asset service offerings "
            "must prepare CARF (Crypto-Asset Reporting Framework) implementation alongside "
            "existing CRS/FATCA infrastructure, representing a material technology and data "
            "management investment.\n\n"
            "The United States DOJ Swiss Bank Program — which resulted in over USD 5 billion in "
            "settlements from Swiss banks for facilitating US tax evasion — has left a permanent "
            "mark on compliance culture and resourcing across the sector. The residual tail risk "
            "from legacy US client relationships, combined with ongoing DOJ investigative activity, "
            "means that US cross-border compliance remains a live risk management priority."
        ),
        "private_banking_issues": (
            "Cross-border risk in private banking is inherently elevated by the international "
            "client profile of the sector. Swiss private banks typically serve clients from "
            "20–50 jurisdictions simultaneously, each with distinct tax reporting, investment "
            "restriction, and market access requirements. The management of these multi-jurisdictional "
            "obligations at the client relationship level — ensuring that CRS self-certifications "
            "are current, that tax residency changes are identified and acted upon, and that "
            "investment recommendations comply with the regulatory requirements of the client's "
            "home jurisdiction — requires sophisticated compliance infrastructure and trained "
            "relationship management teams. The departure of senior RMs with cross-border client "
            "books creates acute compliance continuity risk."
        ),
        "regulatory_pressure": (
            "FINMA's expectations on cross-border compliance are articulated through the FINMA "
            "cross-border services policy and supervisory guidance on CRS/FATCA implementation. "
            "The US QI (Qualified Intermediary) programme imposes specific documentation, "
            "withholding, and reporting obligations on Swiss banks acting as QIs for US "
            "securities transactions. The DOJ's continued investigative activity — including "
            "the Pictet USD 122.9 million settlement in 2023 and the UBS EUR 1.8 billion French "
            "tax settlement — demonstrates that historical cross-border facilitation exposures "
            "remain prosecutable. DAC8's 2026 implementation will require new CARF reporting "
            "infrastructure integrated with existing CRS/FATCA systems."
        ),
        "industry_trends": (
            "Cross-border compliance is evolving along three dimensions. The maturation of CRS "
            "and FATCA has shifted the compliance challenge from implementation to quality "
            "assurance — ensuring that self-certification data is accurate, current, and "
            "consistent with client transaction patterns, and that reportable accounts are "
            "correctly identified. DAC8 and CARF are introducing a new crypto-asset reporting "
            "layer that requires significant data infrastructure investment. The proliferation "
            "of digital nomad clients — HNWI individuals with fluid tax residency, multiple "
            "citizenships, and cross-border asset structures — is creating a new category of "
            "cross-border complexity that existing CRS frameworks were not designed to handle "
            "elegantly. Finally, country-specific market access restrictions — including EU "
            "MiFID II third-country equivalence, SEC registration requirements, and Asian "
            "regulatory restrictions on offshore services — are reshaping which Swiss private "
            "banks can credibly serve which jurisdictions."
        ),
        "peer_incidents": (
            "Pictet & Cie agreed to a USD 122.9 million DOJ settlement in 2023 for facilitating "
            "US tax evasion through offshore accounts — the largest such settlement by a Swiss "
            "private bank in the post-Swiss Bank Program era. UBS agreed to a EUR 1.8 billion "
            "settlement with French authorities in 2023 for cross-border tax evasion facilitation, "
            "following a decade-long investigation into Swiss-based relationship managers "
            "soliciting French clients. The DOJ Swiss Bank Program (2013–2016) resulted in "
            "over USD 5 billion in settlements from more than 80 Swiss banks. Separately, "
            "German tax authority Cum-Ex investigations have implicated several Swiss-connected "
            "entities, with ongoing criminal proceedings against individual bankers demonstrating "
            "that personal criminal liability for cross-border tax facilitation is a live risk."
        ),
        "key_statistics": [
            "DOJ Swiss Bank Program total settlements: over USD 5 billion from 80+ Swiss banks",
            "Pictet & Cie USD 122.9 million DOJ settlement (2023) — largest post-Program Swiss private bank tax evasion settlement",
            "UBS EUR 1.8 billion French tax settlement (2023) — decade-long cross-border investigation",
            "CRS: over 100 jurisdictions participating in automatic exchange of financial account information",
            "DAC8 / CARF: crypto-asset reporting framework targeted for implementation from 2026, requiring new infrastructure",
        ],
        "mckinsey_angle": (
            "Cross-border compliance is a permanent strategic cost of the Swiss private banking "
            "model, not a transitional regulatory challenge. The McKinsey perspective is that "
            "the institutions best positioned for the next decade will be those that have "
            "invested in a genuinely integrated cross-border compliance capability — one that "
            "covers CRS/FATCA quality, QI programme management, CARF readiness, and "
            "jurisdiction-by-jurisdiction market access governance within a single, client-centric "
            "compliance framework. The alternative — managing cross-border compliance as a "
            "fragmented set of regulatory workstreams — creates both regulatory risk and a "
            "client experience penalty that sophisticated HNWI clients will increasingly notice."
        ),
        "tone": "professional",
    },

    "INVESTMENT_SUITABILITY": {
        "theme": "Investment Suitability",
        "market_context": (
            "Switzerland's Financial Services Act (FinSA), which entered into force in January 2020 "
            "with a transitional period expiring in 2022, has fundamentally restructured the legal "
            "framework for investment advice and portfolio management in Swiss private banking. FinSA "
            "introduces a tiered client classification system (retail, professional, institutional), "
            "mandatory suitability and appropriateness assessments for investment recommendations, "
            "written client agreement requirements, and enhanced conflict of interest disclosure "
            "obligations. For private banks accustomed to a lighter regulatory touch than their "
            "EU MiFID II-regulated counterparts, FinSA represents a material compliance uplift.\n\n"
            "The parallel application of EU MiFID II requirements — applicable to Swiss private banks "
            "with EU clients, EU-regulated subsidiaries, or cross-border service activities into EU "
            "member states — creates a dual regulatory framework that must be navigated simultaneously. "
            "MiFID II's product governance requirements, ex-ante cost disclosure obligations, and "
            "target market definition standards are de facto applicable to a significant portion of "
            "Swiss private banking AUM. The interaction between FinSA's Swiss suitability framework "
            "and MiFID II's EU requirements creates compliance complexity, particularly for "
            "cross-border mandates and structured product distribution.\n\n"
            "The prohibition on retrocessions — third-party inducements paid to relationship managers "
            "or portfolio managers in return for recommending specific products — under FinSA's "
            "independence provisions has reshaped the economics of Swiss private banking product "
            "distribution and aligned Swiss practice more closely with MiFID II's inducement rules."
        ),
        "private_banking_issues": (
            "Investment suitability risk in private banking is structurally elevated by the "
            "sophistication gap between product complexity and client understanding. Structured "
            "products — barrier reverse convertibles, auto-callables, leveraged certificates — "
            "are distributed widely in the Swiss private banking market but are frequently "
            "inadequately explained, with suitability assessments that document process compliance "
            "rather than genuine client comprehension. The discretionary mandate model introduces "
            "a different suitability risk: portfolio managers making investment decisions that "
            "deviate from client risk profiles without client awareness, creating latent "
            "suitability breaches visible only during performance attribution review or market "
            "stress events."
        ),
        "regulatory_pressure": (
            "FINMA's enforcement action against Julius Bär in 2023 — including a CHF 26 million "
            "fine and mandatory governance remediation — cited suitability control failures in "
            "Lombard lending and investment advisory as core findings. FINMA has signalled "
            "continuing supervisory focus on FinSA implementation quality, including the "
            "adequacy of suitability documentation, the frequency of client profile updates, "
            "and the robustness of structured product suitability assessments. ESG suitability "
            "preferences — mandatory under FinSA as of January 2024 — add a further dimension "
            "to the suitability assessment framework, requiring integration of sustainability "
            "preferences into investment recommendation processes."
        ),
        "industry_trends": (
            "Four trends are reshaping investment suitability management. The digitisation of "
            "suitability assessment — moving from paper-based questionnaires to dynamic, "
            "algorithm-assisted profiling tools — is improving data quality but introducing "
            "model risk and regulatory uncertainty about algorithm explainability. ESG preference "
            "integration is creating a new axis of suitability complexity, requiring systems that "
            "can match client sustainability preferences against product ESG classifications that "
            "are themselves contested. The growth of alternative investments in HNWI portfolios "
            "— private equity, hedge funds, real assets — requires suitability frameworks "
            "calibrated for illiquidity, valuation uncertainty, and concentration risk. Finally, "
            "the vulnerable client agenda — addressing the needs of elderly, cognitively impaired, "
            "or recently bereaved clients — is receiving growing regulatory and reputational "
            "attention across the sector."
        ),
        "peer_incidents": (
            "Julius Bär received a CHF 26 million FINMA fine in 2023, with suitability control "
            "failures cited as a core finding alongside AML deficiencies — one of the largest "
            "Swiss private banking regulatory penalties for conduct-related failures. The CS "
            "AT1 write-down (2023) triggered widespread client litigation against private banks "
            "that had recommended AT1 securities to clients whose risk profiles did not "
            "accommodate full capital loss scenarios, creating a systemic suitability exposure "
            "across the sector. Internationally, Deutsche Bank's EUR 400 million settlement "
            "with US investors over structured product mis-selling set a benchmark for "
            "institutional liability in structured product distribution. The UK FCA's Consumer "
            "Duty (effective July 2023) is reshaping client outcome expectations in a manner "
            "that is influencing Swiss supervisory thinking about suitability culture."
        ),
        "key_statistics": [
            "FinSA entered into force January 2020; mandatory suitability and appropriateness assessments for all investment services",
            "Julius Bär CHF 26 million FINMA fine (2023): suitability and AML control failures cited",
            "ESG suitability preferences mandatory under FinSA from January 2024",
            "CS AT1 write-down CHF 16 billion (2023): triggered sector-wide suitability litigation review",
            "MiFID II inducement / retrocession rules: de facto applicable to Swiss banks with EU clients or subsidiaries",
        ],
        "mckinsey_angle": (
            "Investment suitability is simultaneously a regulatory obligation and a client value "
            "proposition in private banking. Leading institutions are recognising that a genuinely "
            "robust suitability framework — one that integrates FinSA, MiFID II, and ESG preference "
            "requirements in a seamless client profiling and product matching process — creates "
            "commercial as well as compliance value. Clients who receive recommendations that "
            "transparently reflect their objectives, constraints, and sustainability preferences "
            "demonstrate higher satisfaction, lower litigation propensity, and stronger AUM "
            "retention. The strategic investment in suitability infrastructure is thus "
            "simultaneously a risk mitigation and a client franchise protection measure."
        ),
        "tone": "professional",
    },

    "TAX_COMPLIANCE": {
        "theme": "Tax Compliance",
        "market_context": (
            "Tax compliance in Swiss private banking has undergone a structural transformation "
            "over the past decade, driven by the global AEOI architecture, US DOJ enforcement, "
            "and the collapse of offshore banking secrecy as a viable business model. The "
            "OECD Common Reporting Standard (CRS) — now covering over 100 jurisdictions — "
            "and FATCA together create a near-comprehensive automatic information exchange "
            "framework that has rendered undisclosed offshore accounts an unacceptable risk "
            "for compliant institutions. Swiss private banks have collectively invested "
            "hundreds of millions of CHF in tax compliance infrastructure, client re-documentation "
            "programmes, and legacy portfolio remediation.\n\n"
            "The US Qualified Intermediary (QI) programme imposes specific withholding, "
            "documentation, and reporting obligations on Swiss banks transacting in US "
            "securities, with periodic QI audits by IRS-approved external reviewers creating "
            "a regular compliance verification cycle. The programme's complexity — particularly "
            "in the treatment of partnerships, trusts, and entity account holders — requires "
            "dedicated QI compliance infrastructure and specialist expertise.\n\n"
            "The EU's DAC8 Directive, extending AEOI to crypto-assets through the OECD's "
            "Crypto-Asset Reporting Framework (CARF), targets implementation from 2026. "
            "Swiss private banks with crypto service offerings must build parallel CARF "
            "reporting infrastructure, collect new client self-certifications, and integrate "
            "crypto reporting with existing CRS/FATCA frameworks — representing a significant "
            "compliance investment horizon."
        ),
        "private_banking_issues": (
            "Tax compliance risk in private banking is heightened by the complexity of HNWI "
            "tax structures. Ultra-high-net-worth clients typically hold assets through multiple "
            "legal entities — trusts, foundations, holding companies, and special purpose vehicles "
            "— across several jurisdictions, each with distinct tax treatment and reporting "
            "requirements. Determining the correct CRS/FATCA classification for complex entity "
            "structures, identifying ultimate controlling persons, and ensuring that "
            "self-certifications remain current across multiple account holders and jurisdictions "
            "requires specialist expertise that is unevenly distributed across relationship "
            "management teams. The risk of CRS under-reporting through classification errors "
            "is a live exposure at most Swiss private banks."
        ),
        "regulatory_pressure": (
            "FINMA expects Swiss private banks to maintain robust tax compliance frameworks "
            "encompassing CRS/FATCA implementation quality, QI programme compliance, and "
            "client documentation currency. The DOJ's continued investigative activity — "
            "most recently the Pictet USD 122.9 million settlement in 2023 — demonstrates "
            "that historical tax evasion facilitation exposures remain prosecutable, and that "
            "cooperation with DOJ and IRS investigations is a determinant of settlement terms. "
            "The OECD Pillar Two global minimum tax (15% effective tax rate) is creating new "
            "compliance complexity for Swiss-domiciled holding structures used by HNWI clients, "
            "with Swiss Federal Council implementation of qualifying domestic minimum top-up "
            "tax (QDMTT) adding a domestic dimension to an international framework."
        ),
        "industry_trends": (
            "Tax compliance in private banking is evolving along three dimensions. CARF/DAC8 "
            "implementation is the sector's most pressing near-term investment priority, "
            "requiring crypto-asset account identification, client self-certification collection, "
            "and reporting infrastructure build. The quality assurance of existing CRS/FATCA "
            "reporting — ensuring that entity classifications are correct, that controlling "
            "person identification is complete, and that reportable accounts are not "
            "erroneously excluded — is receiving increased supervisory and internal audit "
            "scrutiny. Finally, the Pillar Two global minimum tax is creating new advisory "
            "opportunities for private banks assisting HNWI clients with corporate structure "
            "reviews, while also creating new compliance complexity in the treatment of "
            "Swiss holding structures."
        ),
        "peer_incidents": (
            "Pictet & Cie's USD 122.9 million DOJ settlement (2023) for facilitating US tax "
            "evasion — through Swiss-based RMs soliciting undisclosed offshore accounts for "
            "US persons — is the defining recent enforcement case for Swiss private banking "
            "tax compliance. The DOJ Swiss Bank Program (2013–2016) resulted in USD 5 billion+ "
            "in settlements from over 80 Swiss banks, permanently reshaping the sector's "
            "approach to US client tax compliance. UBS's EUR 1.8 billion French settlement "
            "(2023) for facilitating French client tax evasion through cross-border solicitation "
            "demonstrates that the enforcement risk extends beyond the US to European tax "
            "authorities. The ongoing German Cum-Ex dividend stripping investigations have "
            "implicated Swiss-connected entities, with individual criminal prosecutions "
            "demonstrating personal liability exposure."
        ),
        "key_statistics": [
            "DOJ Swiss Bank Program: USD 5 billion+ in settlements from 80+ Swiss banks for US tax evasion facilitation",
            "Pictet & Cie USD 122.9 million DOJ settlement (2023) — largest post-Program Swiss private bank tax enforcement action",
            "CRS AEOI: 100+ jurisdictions exchanging financial account information annually",
            "DAC8 / CARF: crypto-asset automatic reporting targeted for 2026, requiring new self-certification and infrastructure",
            "OECD Pillar Two: 15% global minimum effective tax rate, with Swiss QDMTT implementation impacting HNWI holding structures",
        ],
        "mckinsey_angle": (
            "Tax compliance has transitioned from a reactive, enforcement-driven function to a "
            "proactive client advisory and institutional risk management capability. The "
            "McKinsey perspective is that Swiss private banks that invest in high-quality "
            "tax compliance infrastructure — including automated CRS/FATCA classification "
            "engines, CARF-ready reporting platforms, and QI programme quality assurance "
            "processes — will reduce their regulatory tail risk while simultaneously "
            "providing a differentiating client advisory capability in an environment where "
            "HNWI clients face unprecedented global tax transparency. Tax compliance "
            "excellence is no longer a defensive capability — it is a client service imperative."
        ),
        "tone": "professional",
    },

    "CRYPTO_ASSETS": {
        "theme": "Crypto Assets",
        "market_context": (
            "Switzerland has positioned itself as a leading crypto-asset and blockchain jurisdiction "
            "through the Swiss DLT Act (Distributed Ledger Technology Act, effective 2021), which "
            "created a dedicated legal framework for DLT-based securities, digital asset trading "
            "facilities, and crypto custody. Swiss private banks operating crypto custody or "
            "trading services benefit from one of the world's most developed regulatory frameworks "
            "for digital assets, but simultaneously face the challenge of aligning with the EU's "
            "Markets in Crypto-Assets Regulation (MiCA), which entered into force in December "
            "2024 and applies extraterritorially to Swiss banks serving EU-resident clients.\n\n"
            "The collapse of FTX in November 2022 — the most significant crypto exchange failure "
            "in history, resulting in USD 8 billion in customer losses — crystallised operational, "
            "custody, and counterparty risk concerns for institutional crypto participants. Swiss "
            "private banks that had developed crypto product offerings faced immediate client "
            "inquiries, regulatory scrutiny, and reputational management challenges. The FTX "
            "fallout accelerated regulatory reform globally, contributing to MiCA's final text "
            "and prompting FINMA to issue additional guidance on crypto custody safekeeping "
            "obligations.\n\n"
            "Beyond speculative crypto assets, the tokenisation of traditional financial assets — "
            "private equity interests, real estate, bonds — is gaining institutional momentum, "
            "with Swiss DLT infrastructure (SIX Digital Exchange, Taurus) enabling regulated "
            "tokenised security issuance and settlement. Private banks are evaluating tokenised "
            "asset custody and distribution as a near-term product development priority."
        ),
        "private_banking_issues": (
            "Crypto asset risk in private banking is characterised by the combination of "
            "client demand, regulatory uncertainty, and operational immaturity. HNWI clients "
            "increasingly request crypto asset exposure — either through direct custody, "
            "structured product wrappers, or discretionary mandate allocations — while the "
            "AML/KYC risk associated with crypto assets (pseudonymous transactions, mixer "
            "usage, DeFi interactions) is materially higher than for traditional assets. "
            "The suitability framework for crypto assets remains underdeveloped, with limited "
            "historical data for stress testing and valuation models that are contested even "
            "among practitioners. Custody risk — the safekeeping of private keys and the "
            "management of crypto asset operational processes — requires specialist "
            "infrastructure absent from most traditional private banking platforms."
        ),
        "regulatory_pressure": (
            "MiCA (EU, December 2024) requires authorisation for crypto-asset service providers "
            "serving EU clients, imposes mandatory white paper disclosures, and establishes "
            "conduct and operational requirements for crypto intermediaries. Swiss private "
            "banks serving EU-resident clients through crypto services must assess MiCA "
            "applicability and either seek EU authorisation or restructure their service model. "
            "FINMA's expectations on crypto AML — including travel rule compliance for "
            "crypto transfers under the revised AMLA — are among the world's most stringent. "
            "DAC8/CARF requires crypto-asset reporting from 2026, imposing new client "
            "self-certification and data collection obligations on Swiss private banks "
            "offering crypto services."
        ),
        "industry_trends": (
            "Four trends are defining crypto asset development in Swiss private banking. "
            "Institutional custody infrastructure — dedicated crypto custody platforms with "
            "multi-signature key management, insurance coverage, and regulatory-grade "
            "AML controls — is becoming a prerequisite for private bank crypto offerings. "
            "Tokenisation of traditional assets is moving from proof-of-concept to initial "
            "commercial deployment on Swiss DLT infrastructure. Stablecoin regulation — "
            "including HKMA's stablecoin framework and MiCA's e-money token requirements "
            "— is creating a regulated stablecoin layer that private banks may leverage "
            "for settlement and liquidity management. Finally, DeFi risk management is "
            "emerging as a new competency requirement for institutions whose clients "
            "are actively engaging with decentralised protocols, creating AML and "
            "suitability monitoring challenges without centralised counterparty visibility."
        ),
        "peer_incidents": (
            "The FTX collapse (November 2022) resulted in USD 8 billion in customer losses "
            "and triggered global regulatory acceleration on crypto exchange regulation, "
            "custody requirements, and client asset segregation. Swiss private banks with "
            "FTX-related product exposure faced immediate client claims and reputational "
            "management challenges. The Celsius Network collapse (2022) — a crypto lending "
            "platform with institutional private banking clients — similarly crystallised "
            "counterparty and liquidity risk in crypto lending structures. The OneCoin "
            "fraud — a multi-billion-dollar crypto Ponzi scheme whose proceeds flowed "
            "through Swiss financial institutions — resulted in FINMA inquiries and "
            "demonstrated the AML risk of accepting crypto-origin funds without adequate "
            "source of funds documentation."
        ),
        "key_statistics": [
            "Swiss DLT Act (effective 2021): world-leading regulatory framework for DLT-based securities and crypto custody",
            "MiCA (EU, December 2024): mandatory authorisation and conduct requirements for crypto-asset services to EU clients",
            "FTX collapse (November 2022): USD 8 billion in customer losses — defining crypto counterparty risk event",
            "DAC8 / CARF: crypto-asset reporting from 2026, requiring client self-certification and new reporting infrastructure",
            "FINMA crypto AML: travel rule compliance for crypto transfers among the world's most stringent requirements",
        ],
        "mckinsey_angle": (
            "Crypto assets represent both the highest-risk and potentially highest-reward "
            "product development frontier for Swiss private banking. The McKinsey view is "
            "that the institutions best positioned to capture the HNWI crypto opportunity "
            "are those that have built a genuinely institutional-grade capability: regulated "
            "custody infrastructure, robust AML/travel rule compliance, MiCA-ready service "
            "architecture, and suitability frameworks calibrated for crypto's unique risk "
            "profile. Rushing to market with inadequate infrastructure — as several "
            "institutions did in the 2021 crypto bull market — creates regulatory, "
            "reputational, and client liability exposure that far outweighs first-mover "
            "revenue benefits."
        ),
        "tone": "professional",
    },

    "ESG": {
        "theme": "ESG & Sustainable Finance",
        "market_context": (
            "Sustainable finance has moved from a niche client preference to a mainstream "
            "regulatory and commercial imperative in Swiss private banking. The mandatory "
            "integration of client ESG preferences into investment advice under FinSA "
            "(effective January 2024) has transformed ESG from a product development "
            "question into a core suitability compliance obligation. Swiss Asset Managers "
            "Association (AMAS) sustainable finance guidelines and the Swiss Financial "
            "Centre's sustainability roadmap have created a self-regulatory framework "
            "that supplements — and in some areas exceeds — EU regulatory requirements.\n\n"
            "The EU's Sustainable Finance Disclosure Regulation (SFDR) — directly applicable "
            "to Swiss private banks distributing SFDR-classified funds to EU investors or "
            "operating EU AIFMs within their group structures — has introduced a complex "
            "product classification system (Article 6, 8, and 9 funds) and entity-level "
            "principal adverse impact (PAI) disclosure requirements. The CSRD (Corporate "
            "Sustainability Reporting Directive), effective for large EU companies from 2025, "
            "is creating a step-change in sustainability data availability from corporate "
            "issuers, which will in turn improve the quality of portfolio-level ESG metrics "
            "available to private banking investment teams.\n\n"
            "Greenwashing risk — the misrepresentation of sustainability credentials in "
            "client communications, fund marketing materials, and discretionary mandate "
            "reporting — is the defining ESG conduct risk for private banking, combining "
            "regulatory, reputational, and litigation exposure in a single vulnerability."
        ),
        "private_banking_issues": (
            "ESG risk in private banking is shaped by the tension between client demand, "
            "product availability, and data quality. HNWI clients have widely divergent "
            "sustainability preferences — from impact-first philanthropic mandates to "
            "pure ESG-exclusion strategies to clients who resist any sustainability "
            "integration — requiring a segmented advisory capability. The quality and "
            "consistency of ESG data across asset classes remains uneven, with private "
            "market assets, real estate, and alternative investments presenting particular "
            "data gaps. The risk of suitability mis-match — recommending products with "
            "inadequate sustainability credentials to clients who have expressed strong "
            "ESG preferences — is an emerging FINMA conduct focus."
        ),
        "regulatory_pressure": (
            "FinSA ESG preference integration (mandatory January 2024) requires Swiss "
            "private banks to collect, document, and act upon client sustainability "
            "preferences in investment advice. SFDR PAI disclosures and CSRD supply "
            "chain data obligations are progressively improving the sustainability data "
            "inputs available to portfolio managers. FINMA has signalled greenwashing "
            "as a supervisory priority for 2025–2026, with expectations that marketing "
            "materials, fund prospectuses, and client reporting accurately represent "
            "sustainability characteristics and are not misleading. The EU Taxonomy "
            "Regulation — classifying economic activities as environmentally sustainable "
            "— is progressively creating a reference framework for sustainable product "
            "classification applicable to Swiss institutions distributing EU-classified products."
        ),
        "industry_trends": (
            "ESG practice in private banking is maturing rapidly along four dimensions. "
            "Client ESG preference elicitation is being systematised through structured "
            "profiling tools that map client values to product universe segments. "
            "Impact measurement — going beyond ESG scores to quantify real-world "
            "sustainability outcomes from portfolio holdings — is becoming a differentiating "
            "capability for leading private banks. Transition finance — supporting "
            "brown-to-green economic transition through blended finance structures "
            "and sustainability-linked instruments — is emerging as a significant "
            "product innovation domain. Climate risk integration into investment "
            "mandates — including TCFD-aligned scenario analysis at the portfolio level "
            "— is transitioning from best practice to regulatory expectation."
        ),
        "peer_incidents": (
            "DWS received a EUR 25 million fine from BaFin in 2023 for greenwashing in "
            "its fund marketing materials — the largest financial sector greenwashing "
            "regulatory penalty to date, setting the benchmark for the severity of "
            "ESG conduct enforcement. Goldman Sachs Asset Management settled SEC "
            "greenwashing charges for USD 4 million related to inadequate ESG policy "
            "implementation in marketed ESG funds. Several Swiss private banks received "
            "FINMA inquiries in 2024 regarding the consistency between ESG credentials "
            "claimed in marketing materials and actual portfolio construction methodology. "
            "The broader 'SFDR reclassification wave' — in which numerous fund managers "
            "downgraded funds from Article 9 to Article 8 status — created client trust "
            "damage and regulatory scrutiny across the European private banking distribution "
            "network."
        ),
        "key_statistics": [
            "FinSA ESG preference integration: mandatory from January 2024 for all Swiss investment advisory services",
            "DWS greenwashing fine: EUR 25 million (BaFin, 2023) — largest ESG conduct penalty in financial services to date",
            "SFDR: Article 8 and 9 fund reclassification wave eroded sustainable fund AUM credibility across European distribution",
            "CSRD (effective 2025): mandatory sustainability reporting for large EU companies, improving ESG data availability",
            "Swiss private banking ESG AUM: estimated 35–45% of total managed assets incorporate some form of ESG criteria",
        ],
        "mckinsey_angle": (
            "ESG in private banking has reached the maturity threshold at which it can no longer "
            "be managed as a product overlay — it must be embedded in the core investment process, "
            "client advisory model, and risk management framework. The McKinsey perspective is "
            "that leading institutions are building three structural capabilities: a segmented "
            "client ESG profiling model that goes beyond checkbox questionnaires; a product "
            "architecture that maps transparently to client preferences with auditable methodology; "
            "and a greenwashing prevention framework spanning marketing review, product validation, "
            "and client reporting integrity. The institutions that build these capabilities will "
            "capture the growing share of ESG-committed HNWI AUM; those that rely on marketing "
            "narrative without substance face accelerating regulatory and reputational risk."
        ),
        "tone": "professional",
    },

    "FRAUD": {
        "theme": "Fraud",
        "market_context": (
            "Fraud risk in Swiss private banking is undergoing a structural escalation driven "
            "by the intersection of sophisticated cyber-enabled attack vectors, the high-value "
            "targets represented by HNWI client relationships, and the trust-intensive, "
            "relationship-driven service model that characterises the sector. Switzerland "
            "recorded approximately CHF 180 million in reported fraud losses in 2023, with "
            "authorised push payment (APP) fraud — in which victims are socially engineered "
            "into authorising fraudulent transfers — representing the fastest-growing category. "
            "The HNWI private banking segment is disproportionately targeted due to the "
            "size of individual transactions and the relatively lower transaction monitoring "
            "scrutiny applied to large, infrequent wire transfers by high-value clients.\n\n"
            "Deepfake technology has emerged as a material fraud vector, with reported "
            "incidents of AI-generated voice and video impersonation of clients to authorise "
            "fraudulent instructions increasing by over 700% between 2022 and 2023. The "
            "attack surface extends beyond client impersonation to advisor impersonation — "
            "fraudsters using deepfake audio to mimic relationship manager voices in calls "
            "to client family members or operations staff. A Hong Kong finance firm suffered "
            "a USD 25 million loss in 2024 from a multi-person deepfake video conference "
            "in which all participants were AI-generated.\n\n"
            "Internal fraud — misappropriation of client assets, unauthorised trading, and "
            "expense fraud by bank employees — accounts for an estimated 35% of total "
            "private banking fraud losses, reflecting the access, trust, and autonomy "
            "afforded to relationship managers and senior advisors in the private banking model."
        ),
        "private_banking_issues": (
            "Private banking fraud risk is structurally amplified by the service model. "
            "The high degree of relationship manager autonomy — including discretion over "
            "client communication, transaction initiation, and documentation management — "
            "creates conditions in which internal fraud can be sustained for extended periods "
            "before detection. Client deference to trusted advisors can delay the reporting "
            "of suspected unauthorised activity. The complexity of HNWI portfolio structures "
            "— spanning multiple accounts, asset classes, and jurisdictions — makes routine "
            "reconciliation and anomaly detection more challenging than in retail environments. "
            "Family office structures, which aggregate decision-making authority over large "
            "wealth pools in a small number of individuals, create high-value social "
            "engineering targets."
        ),
        "regulatory_pressure": (
            "FINMA expects Swiss private banks to maintain robust fraud prevention and detection "
            "frameworks, encompassing transaction monitoring calibrated for HNWI behaviour "
            "patterns, operational controls over wire transfer authorisation, and client "
            "identity verification procedures for high-value instruction acceptance. The "
            "revised AMLA and FINMA AML circular impose enhanced due diligence obligations "
            "for unusual transaction patterns that may indicate fraud or money laundering. "
            "DORA's operational resilience requirements include incident classification and "
            "reporting obligations for fraud-related operational events. Swiss criminal law "
            "(Articles 138–148 SCC) provides the prosecutorial framework for banking fraud, "
            "with civil liability for insufficient controls being an additional exposure "
            "under the Swiss Code of Obligations."
        ),
        "industry_trends": (
            "Four fraud trends are defining the private banking risk landscape. Deepfake "
            "and AI-enabled social engineering attacks are escalating in sophistication and "
            "frequency, requiring liveness detection, callback verification, and multi-factor "
            "authentication for high-value instruction authorisation. APP fraud prevention "
            "— including enhanced payee verification, transaction delay mechanisms, and "
            "client education programmes — is becoming an operational priority. Internal "
            "fraud prevention is being strengthened through enhanced four-eyes principle "
            "enforcement, exception reporting on RM transaction patterns, and surprise "
            "audit programmes targeting high-access individuals. Behavioural analytics "
            "— applying machine learning to detect anomalous advisor or client behaviour "
            "patterns before losses crystallise — is emerging as a leading detection "
            "capability at tier-one institutions."
        ),
        "peer_incidents": (
            "A Hong Kong finance firm suffered a USD 25 million loss in early 2024 from "
            "a deepfake video conference fraud in which all counterparties were AI-generated, "
            "demonstrating the operational reality of multi-person deepfake attacks. Several "
            "Swiss private banks experienced internal fraud incidents in 2022–2024 involving "
            "relationship managers who misappropriated client assets over multi-year periods, "
            "concealed through falsified portfolio statements — echoing the Kweku Adoboli "
            "UBS rogue trader case pattern in a private banking context. The Bernie Madoff "
            "Ponzi scheme — in which several Swiss private banks had placed client assets "
            "with BMIS without adequate due diligence — remains a defining third-party fraud "
            "risk reference case. Internationally, the Société Générale Jérôme Kerviel "
            "case and the recent Morgan Stanley internal trading fraud cases illustrate "
            "the persistent internal fraud risk at sophisticated financial institutions."
        ),
        "key_statistics": [
            "Switzerland APP and wire fraud losses: approximately CHF 180 million reported in 2023",
            "Deepfake fraud attempts against financial institutions: +700% increase between 2022 and 2023",
            "Internal fraud share of total private banking fraud losses: estimated 35%",
            "Hong Kong deepfake video conference fraud (2024): USD 25 million single-event loss",
            "HNWI fraud targeting: average loss per successful HNWI fraud event estimated at CHF 2–5 million in Switzerland",
        ],
        "mckinsey_angle": (
            "Fraud risk management in private banking requires a fundamental rethink of the "
            "trust model that underpins the service relationship. The McKinsey perspective "
            "is that the institutions best positioned to manage emerging fraud threats will "
            "be those that have invested in three capabilities: a zero-trust verification "
            "framework for high-value instruction authorisation that does not compromise "
            "client experience; a behavioural analytics capability that detects internal "
            "and external fraud signals before losses crystallise; and a client education "
            "programme that empowers HNWI clients to identify and report social engineering "
            "attempts. Fraud prevention in private banking is not in conflict with the "
            "relationship model — it is a prerequisite for sustaining client trust."
        ),
        "tone": "professional",
    },

    "LIQUIDITY_RISK": {
        "theme": "Liquidity Risk",
        "market_context": (
            "The liquidity risk landscape for Swiss private banking was fundamentally "
            "reset by two events in rapid succession: the SVB collapse (March 2023) — "
            "in which USD 42 billion in deposits were withdrawn in a single day, precipitating "
            "a bank run driven by social media amplification — and the Credit Suisse crisis, "
            "in which CHF 110 billion in client outflows across Q4 2022 and Q1 2023 "
            "overwhelmed the bank's liquidity buffers despite its HQLA position appearing "
            "adequate on standard LCR metrics. These events demonstrated that traditional "
            "liquidity risk models — calibrated on historical deposit behaviour and regulatory "
            "stress scenarios — systematically underestimate outflow velocity in confidence "
            "crises amplified by digital communication.\n\n"
            "The Swiss National Bank's Public Liquidity Backstop (PLB) mechanism, "
            "legislated following the Credit Suisse emergency merger, provides a new "
            "emergency liquidity instrument for systemically important Swiss banks, but "
            "does not eliminate the need for robust internal liquidity risk management. "
            "FINMA's post-CS supervisory priorities explicitly include intraday liquidity "
            "monitoring, stress scenario calibration, and funding concentration risk "
            "assessment as areas requiring enhanced management attention.\n\n"
            "Private banks with concentrated HNWI deposit bases face distinctive liquidity "
            "risk characteristics. A small number of large depositors can drive material "
            "outflow events — particularly in a confidence crisis — creating lumpiness in "
            "liquidity that standard LCR and NSFR frameworks do not fully capture."
        ),
        "private_banking_issues": (
            "Liquidity risk in private banking is structurally shaped by the high concentration "
            "of deposits among a small number of HNWI clients. A single large client departing "
            "— or a cluster of clients responding simultaneously to adverse news — can drive "
            "outflows that exceed LCR stress scenario assumptions calibrated on diversified "
            "retail deposit bases. The investment of HNWI deposits in long-duration or "
            "illiquid assets to generate yield creates a maturity transformation mismatch "
            "that is particularly acute when client deposits are remunerated at floating "
            "rates but invested in illiquid alternatives or Lombard loan books. The "
            "relationship manager as a single point of client contact means that RM "
            "departure — or RM misconduct exposure — can serve as a liquidity trigger."
        ),
        "regulatory_pressure": (
            "FINMA's post-CS supervisory guidance requires enhanced intraday liquidity "
            "monitoring, granular deposit concentration reporting, and stress scenario "
            "testing that explicitly includes social-media-amplified confidence crisis "
            "scenarios. The LCR and NSFR frameworks, transposed into Swiss liquidity "
            "ordinance, remain the regulatory baseline, but FINMA expects institutions "
            "to supplement these with bespoke internal liquidity stress tests calibrated "
            "to their specific client base and funding structure. The PLB mechanism "
            "requires systemically important Swiss banks to maintain the pre-conditions "
            "for PLB access — eligible collateral, operational readiness — as a "
            "standing liquidity contingency measure."
        ),
        "industry_trends": (
            "Four liquidity risk trends are shaping Swiss private banking practice. "
            "Real-time intraday liquidity monitoring — moving from end-of-day reporting "
            "to continuous intraday position visibility — is becoming a supervisory "
            "expectation for all but the smallest institutions. Social-media-aware "
            "stress scenarios — calibrated on the SVB and CS outflow velocities — are "
            "being incorporated into ILAAP stress testing frameworks. Deposit "
            "concentration limits — formalised thresholds on the share of total deposits "
            "held by a single client or client group — are being embedded into liquidity "
            "risk appetite statements. Finally, the liquidity implications of the growth "
            "in illiquid alternative investments within discretionary mandates — which "
            "cannot be liquidated to meet client redemptions on short notice — are "
            "receiving enhanced management and regulatory attention."
        ),
        "peer_incidents": (
            "Credit Suisse experienced CHF 110 billion in client outflows across Q4 2022 "
            "and Q1 2023, overwhelming its liquidity buffers and precipitating the "
            "emergency UBS merger — the defining liquidity event in Swiss banking history. "
            "Silicon Valley Bank's collapse (March 2023) was triggered by USD 42 billion "
            "in single-day deposit outflows following social media amplification of "
            "concerns about HTM bond losses — establishing the benchmark for digital-era "
            "bank run velocity. First Republic Bank (May 2023) experienced USD 100 billion "
            "in deposit outflows in Q1 2023 despite appearing adequately liquid on LCR "
            "metrics — demonstrating that regulatory liquidity ratios do not prevent "
            "confidence-driven runs. The SNB's CHF 50 billion emergency liquidity "
            "assistance to Credit Suisse — exhausted within weeks — underscored the "
            "inadequacy of traditional ELA mechanisms for modern confidence crises."
        ),
        "key_statistics": [
            "Credit Suisse: CHF 110 billion client outflows in Q4 2022–Q1 2023 preceding emergency UBS merger",
            "SVB: USD 42 billion in single-day deposit withdrawals (March 2023) — benchmark social-media-amplified bank run",
            "Swiss PLB mechanism: legislated following CS emergency merger to provide backstop liquidity for SIBs",
            "First Republic Bank: USD 100 billion in Q1 2023 deposit outflows despite adequate LCR metrics",
            "Private banking deposit concentration: top 10 HNWI clients represent an estimated 20–40% of total deposits at mid-tier Swiss private banks",
        ],
        "mckinsey_angle": (
            "Liquidity risk management in private banking must be recalibrated for the "
            "digital-era confidence crisis — a qualitatively different threat from the "
            "historical bank run that LCR and NSFR frameworks were designed to address. "
            "The McKinsey perspective is that leading institutions must invest in three "
            "capabilities: real-time intraday liquidity visibility that enables minutes-level "
            "response to emerging outflow signals; stress scenarios explicitly calibrated "
            "for social-media-amplified confidence events with CS and SVB-level outflow "
            "velocities; and a deposit concentration management framework that prevents "
            "the build-up of individual client liquidity cliff-edges. Liquidity risk in "
            "private banking is ultimately a function of client trust — and the institutions "
            "that manage it most effectively are those that combine technical liquidity "
            "infrastructure with a relentless focus on client relationship quality."
        ),
        "tone": "professional",
    },

}

# ══════════════════════════════════════════════════════════════════════════════
# HNWI_RED_FLAGS
# 45 structured red flags for HNWI / private banking audit and compliance use.
# ══════════════════════════════════════════════════════════════════════════════

HNWI_RED_FLAGS = [

    # ── AML (RF001–RF015) ──────────────────────────────────────────────────────

    {
        "rf_id": "RF001",
        "category": "AML",
        "title": "Recurring round-number transactions",
        "description": (
            "The client repeatedly initiates or receives transfers in exact round-number amounts "
            "(e.g., CHF 50,000, CHF 100,000, USD 500,000) without plausible commercial justification. "
            "Round-number structuring is a classical indicator of deliberate transaction fragmentation "
            "designed to evade monitoring thresholds or conceal the true amount being transferred."
        ),
        "risk_level": "High",
        "detection_method": (
            "Run automated transaction monitoring rules flagging outgoing and incoming transfers "
            "in round denominations (multiples of CHF/USD/EUR 10,000) above a defined frequency "
            "threshold. Cross-reference flagged transactions against client business profile to "
            "assess economic plausibility."
        ),
        "regulatory_reference": "FATF Recommendation 20; AMLA Art. 9; FINMA AML Circular",
        "private_banking_context": (
            "HNWI clients frequently transact in large round amounts for legitimate purposes "
            "(property purchases, investment subscriptions), making contextual analysis essential. "
            "The pattern is most significant when combined with an unclear source of funds or "
            "a history of fragmented cross-border transfers."
        ),
        "examples": [
            "Client transfers CHF 100,000 to a counterparty in Dubai on the same date each month with no stated purpose",
            "Twelve incoming wires of exactly USD 50,000 from three different offshore entities over 60 days",
            "Client requests 15 separate payments of EUR 9,900 to the same beneficiary within a single quarter",
        ],
    },

    {
        "rf_id": "RF002",
        "category": "AML",
        "title": "Inflows from FATF grey-list jurisdictions",
        "description": (
            "The client receives significant fund inflows originating from jurisdictions currently "
            "subject to FATF enhanced monitoring or identified as having strategic AML/CFT deficiencies. "
            "Such flows carry elevated risk of laundered proceeds and require enhanced source-of-funds "
            "verification beyond the standard CDD process."
        ),
        "risk_level": "High",
        "detection_method": (
            "Configure transaction monitoring to flag all inflows above a defined materiality threshold "
            "from FATF grey-list and black-list jurisdictions. Validate against the client's documented "
            "business activities, source of wealth narrative, and known counterparty network."
        ),
        "regulatory_reference": "FATF Recommendations 10, 19; AMLA Art. 6; FINMA AML Circular 2011/1",
        "private_banking_context": (
            "Private banking clients often maintain legitimate business or family ties to higher-risk "
            "jurisdictions, but relationship managers may under-escalate FATF geography flags to avoid "
            "client friction. Enhanced due diligence documentation and senior compliance sign-off are "
            "required for all material flows from grey-list jurisdictions."
        ),
        "examples": [
            "USD 2 million wire received from a corporate entity registered in Myanmar (FATF grey list)",
            "Recurring inflows from a trust domiciled in a jurisdiction with known beneficial ownership opacity",
            "Client's primary wealth source is a business operating in a jurisdiction recently added to the FATF grey list",
        ],
    },

    {
        "rf_id": "RF003",
        "category": "AML",
        "title": "Opaque nested structures (trusts, foundations)",
        "description": (
            "The client's assets are held through layered legal structures — such as a trust owning "
            "a foundation which in turn owns an operating company — with no clear economic rationale "
            "for the complexity beyond asset concealment. Identifying the ultimate beneficial owner "
            "through the nested layers requires disproportionate effort and yields uncertain results."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Conduct a structured UBO mapping exercise for all clients with multi-layer ownership "
            "structures, documenting each legal entity layer with registered address, jurisdiction, "
            "and ownership percentage. Escalate to compliance for senior review where UBO cannot "
            "be identified with confidence after reasonable investigation."
        ),
        "regulatory_reference": "FATF Recommendation 24, 25; AMLA Art. 4; FINMA AML Circular",
        "private_banking_context": (
            "Complex trust and foundation structures are prevalent and often legitimate in HNWI "
            "wealth planning, making genuine concealment difficult to distinguish from estate "
            "planning sophistication. The key risk indicators are jurisdictional opacity, "
            "professional nominee trustees with no relationship to the settlor, and resistance "
            "to providing underlying corporate documentation."
        ),
        "examples": [
            "Client assets held in a BVI trust whose trustee is a Panamanian professional nominee firm, with no identified beneficiaries",
            "Foundation registered in Liechtenstein owns a Cayman Islands holding company which holds Swiss bank accounts — no economic purpose documented",
            "Four-layer ownership structure identified; RM unable to name the natural person controlling the structure",
        ],
    },

    {
        "rf_id": "RF004",
        "category": "AML",
        "title": "Frequent beneficial owner changes",
        "description": (
            "The declared beneficial owner of a client account or associated legal entity changes "
            "repeatedly and without clear justification — such as succession events, corporate "
            "restructuring, or documented ownership transactions. Frequent UBO substitution is "
            "a classical technique for dissociating illicit funds from their origin."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Implement systematic tracking of UBO declaration changes in the client management "
            "system, with automated alerts triggered when a UBO is changed more than once within "
            "a 12-month period. Each change must be accompanied by documented justification and "
            "compliance officer review."
        ),
        "regulatory_reference": "FATF Recommendations 10, 24; AMLA Art. 3–4; FINMA AML Circular",
        "private_banking_context": (
            "HNWI estates and family offices may legitimately change UBO registrations following "
            "inheritance, divorce, or corporate reorganisation. The red flag arises when changes "
            "occur without accompanying legal documentation, when the new UBO has no discernible "
            "connection to the original client relationship, or when changes correlate with "
            "significant inbound fund flows."
        ),
        "examples": [
            "Beneficial owner of a holding company changes three times in 18 months with no disclosed corporate transaction",
            "New UBO declared immediately prior to a large inbound wire transfer from a high-risk jurisdiction",
            "Original client dies; assets transferred to an entity with an entirely new UBO without probate documentation",
        ],
    },

    {
        "rf_id": "RF005",
        "category": "AML",
        "title": "Source of wealth inconsistent with profile",
        "description": (
            "The client's documented or claimed source of wealth is materially inconsistent with "
            "their professional background, business activities, or the jurisdictions in which they "
            "operate. The discrepancy between the asserted wealth origin and verifiable evidence "
            "raises the possibility that a false or misleading wealth narrative has been constructed."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "During onboarding and periodic review, cross-reference the client's source of wealth "
            "declaration against independent verification sources: corporate registry filings, "
            "property records, news searches, and professional background databases. Document "
            "the evidence base and escalate where inconsistencies cannot be resolved."
        ),
        "regulatory_reference": "FATF Recommendation 10; AMLA Art. 6; FINMA AML Circular 2011/1",
        "private_banking_context": (
            "Private banking onboarding frequently relies on RM-provided source of wealth "
            "narratives that are not independently verified beyond a plausibility check. The "
            "HNWI context amplifies this risk: the larger the claimed wealth, the more "
            "difficult it can be to verify through publicly available sources, and the "
            "greater the potential AML consequence of an inaccurate narrative."
        ),
        "examples": [
            "Client declares CHF 50 million from salary as a government official in a jurisdiction where maximum salary is CHF 80,000 annually",
            "Claimed business sale proceeds cannot be traced to any identified company or transaction in the relevant jurisdiction",
            "Client asserts inheritance from a deceased relative, but no probate documentation or estate record is obtainable",
        ],
    },

    {
        "rf_id": "RF006",
        "category": "AML",
        "title": "Transactions with no economic rationale",
        "description": (
            "The client initiates transactions — transfers, securities purchases, currency conversions "
            "— that have no identifiable commercial, investment, or personal purpose consistent with "
            "their known profile and stated objectives. Transactions lacking economic rationale may "
            "indicate layering activity within a money laundering scheme."
        ),
        "risk_level": "High",
        "detection_method": (
            "Review transactions flagged by monitoring systems for absence of a documented business "
            "purpose. Request client explanation for all non-routine transactions above defined "
            "materiality thresholds. Where explanation is not provided or is implausible, escalate "
            "to compliance for STR assessment."
        ),
        "regulatory_reference": "FATF Recommendation 20; AMLA Art. 9; FINMA AML Circular",
        "private_banking_context": (
            "In private banking, the breadth of legitimate HNWI transaction types — cross-border "
            "investments, philanthropy, real estate purchases, art acquisitions — creates a wide "
            "plausibility zone that can be exploited to conceal transactions lacking genuine purpose. "
            "RM judgment plays a critical role in distinguishing legitimate complexity from "
            "genuine absence of economic rationale."
        ),
        "examples": [
            "Client repeatedly purchases and immediately sells the same securities position with no price movement — apparent wash trading",
            "Large wire to an unrelated third party with no loan agreement, invoice, or relationship documentation",
            "Currency conversion of CHF 5 million followed within 24 hours by reconversion to CHF at a loss, with no stated hedging purpose",
        ],
    },

    {
        "rf_id": "RF007",
        "category": "AML",
        "title": "Client reluctance to provide documentation",
        "description": (
            "The client consistently delays, refuses, or provides incomplete responses to requests "
            "for KYC documentation — including identity documents, source of wealth evidence, "
            "UBO declarations, or transaction purpose explanations. Persistent documentation "
            "reluctance is a primary indicator of a client seeking to obscure relevant information."
        ),
        "risk_level": "High",
        "detection_method": (
            "Track all outstanding KYC documentation requests in the client management system "
            "with escalation triggers for requests outstanding beyond defined timeframes (e.g., "
            "30 days for periodic review, 5 days for urgent transaction-related requests). "
            "Compliance must review all cases where documentation has been outstanding beyond "
            "threshold and assess account restriction or exit."
        ),
        "regulatory_reference": "AMLA Art. 3–7; FINMA AML Circular; FATF Recommendation 10",
        "private_banking_context": (
            "HNWI clients and their advisors frequently cite complexity or advisor availability "
            "as justification for documentation delays. While some delays are legitimate, "
            "a pattern of consistent resistance — particularly correlated with pending "
            "transactions or periodic review milestones — requires compliance escalation "
            "regardless of client commercial importance."
        ),
        "examples": [
            "Client has not provided updated source of wealth documentation despite three requests over six months",
            "Trust deed requested for UBO mapping has not been provided for 90 days; RM has not escalated",
            "Client's legal representative repeatedly claims documents are 'in preparation' without producing them",
        ],
    },

    {
        "rf_id": "RF008",
        "category": "AML",
        "title": "Undisclosed PEP discovered mid-relationship",
        "description": (
            "A client who was not identified as a Politically Exposed Person (PEP) at onboarding "
            "is subsequently found — through screening, adverse media, or client disclosure — to "
            "hold or have recently held a prominent public function. The failure to identify PEP "
            "status at onboarding, or the client's active concealment, requires immediate "
            "re-assessment of the entire relationship."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Conduct continuous PEP screening using real-time screening platforms that cover "
            "domestic and foreign PEP lists across all relevant jurisdictions. Adverse media "
            "monitoring should run in parallel to detect PEP-related news not yet reflected "
            "in structured databases. Any PEP identification mid-relationship triggers "
            "mandatory compliance escalation and enhanced due diligence review."
        ),
        "regulatory_reference": "FATF Recommendations 12, 22; AMLA Art. 6; FINMA AML Circular",
        "private_banking_context": (
            "In private banking, PEP status may be deliberately concealed through the use of "
            "nominees, family member account holders, or complex ownership structures that "
            "distance the PEP from the account. Relationship managers focused on commercial "
            "relationship management may have limited incentive to conduct proactive PEP "
            "identification beyond the onboarding screen."
        ),
        "examples": [
            "Client identified post-onboarding as a senior minister in their home country; enhanced due diligence not performed at account opening",
            "Client's spouse, listed as beneficial owner of a holding company, is revealed to be a state-owned enterprise executive",
            "Adverse media search reveals client received a government infrastructure contract worth USD 500 million — not disclosed in onboarding",
        ],
    },

    {
        "rf_id": "RF009",
        "category": "AML",
        "title": "Flows toward sanctioned jurisdictions",
        "description": (
            "Client transactions involve fund flows to, from, or through jurisdictions subject to "
            "international sanctions regimes — including OFAC, EU, UN, or Swiss SECO sanctions. "
            "Even indirect exposure, such as correspondent bank routing through a sanctioned "
            "country or a beneficial owner with sanctions-linked nationality, may create "
            "regulatory and criminal liability."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Deploy real-time sanctions screening at transaction initiation covering beneficiary "
            "name, beneficiary bank, intermediary bank, and payment routing. Cross-reference "
            "client UBO structures against sanctions lists and SECO/OFAC designations. "
            "Escalate all potential matches to compliance before transaction execution."
        ),
        "regulatory_reference": "SECO Embargo Ordinance; EU Sanctions Regulation; OFAC SDN List; FATF Recommendation 6",
        "private_banking_context": (
            "Private banking clients with business activities in geopolitically complex regions "
            "may have legitimate relationships that inadvertently create sanctions exposure — "
            "for example, a company operating in a partially sanctioned sector or a counterparty "
            "owned by a newly designated individual. The complexity of HNWI structures increases "
            "the risk of indirect sanctions exposure not visible in straightforward name screening."
        ),
        "examples": [
            "Wire transfer routed through a correspondent bank with a branch in a comprehensively sanctioned jurisdiction",
            "Client's business partner is identified as a designated person under EU Russia sanctions",
            "Investment in a company with a 40%+ ownership stake held by a sanctioned Russian oligarch",
        ],
    },

    {
        "rf_id": "RF010",
        "category": "AML",
        "title": "Cash-intensive activity in wealth management",
        "description": (
            "The client requests cash withdrawals, deposits, or currency exchanges at a volume "
            "or frequency inconsistent with their wealth profile and the expected service model "
            "of private banking. Significant cash activity in a relationship primarily managed "
            "through book-entry transfers is anomalous and requires enhanced scrutiny."
        ),
        "risk_level": "High",
        "detection_method": (
            "Monitor all cash transactions above CHF 15,000 (AMLA threshold) and cumulative "
            "monthly cash activity above a defined client-specific threshold. Require documented "
            "purpose for all material cash transactions and escalate where cash usage is "
            "disproportionate to the client's documented lifestyle and business activities."
        ),
        "regulatory_reference": "AMLA Art. 3, 9; FINMA AML Circular; FATF Recommendation 10",
        "private_banking_context": (
            "While private banking clients may legitimately request cash for real estate, art, "
            "or personal expenditure, cash-intensive patterns in a relationship that is otherwise "
            "digital are a significant red flag. The risk is amplified when cash is used in "
            "conjunction with cross-border transfers or when cash is deposited immediately "
            "prior to international wires."
        ),
        "examples": [
            "Client withdraws CHF 200,000 in cash on four occasions over three months with no documented purpose",
            "Multiple large cash deposits by a client who describes their wealth as arising from a professional consulting business",
            "Client requests foreign currency cash in multiple denominations for 'travel purposes' at a combined annual amount of CHF 500,000",
        ],
    },

    {
        "rf_id": "RF011",
        "category": "AML",
        "title": "Unusual correspondent banking flows",
        "description": (
            "Transactions routed through correspondent banking channels display patterns "
            "inconsistent with the client's known counterparty network — including "
            "unexpected originating jurisdictions, unfamiliar correspondent banks, "
            "or multi-hop routing through intermediary accounts. Such patterns may "
            "indicate deliberate layering through the correspondent banking system."
        ),
        "risk_level": "High",
        "detection_method": (
            "Analyse the routing headers of incoming SWIFT messages to identify originating "
            "banks and jurisdictions not consistent with client's documented business geography. "
            "Flag all transactions routed through jurisdictions with poor AML supervision "
            "ratings for enhanced review."
        ),
        "regulatory_reference": "FATF Recommendation 13; AMLA Art. 6; FINMA AML Circular",
        "private_banking_context": (
            "HNWI clients with international business networks may legitimately receive funds "
            "through multiple correspondent banking chains. The red flag is most significant "
            "when correspondent routing involves jurisdictions with no connection to the "
            "client's declared business geography, or when the originating bank operates "
            "in a jurisdiction with identified AML deficiencies."
        ),
        "examples": [
            "Inbound wire for a client whose business is in the UAE routed through a Moldovan correspondent bank",
            "Payment from a Luxembourg investment fund routed through three intermediary banks across jurisdictions with poor FATF ratings",
            "Client's regular counterparty suddenly begins routing payments through a new correspondent bank in a high-risk jurisdiction",
        ],
    },

    {
        "rf_id": "RF012",
        "category": "AML",
        "title": "Urgent international transfer requests",
        "description": (
            "The client makes repeated requests for same-day or urgent international transfers, "
            "typically for large amounts, with pressure on operations staff to bypass standard "
            "authorisation and verification procedures. Urgency-driven requests that circumvent "
            "controls are a common precursor to fraud and money laundering transaction execution."
        ),
        "risk_level": "High",
        "detection_method": (
            "Log all urgent transfer requests with timestamps, client-stated rationale, "
            "and authorisation chain documentation. Identify patterns of urgency through "
            "monitoring exception reports. Compliance review is mandatory before same-day "
            "execution for any transfer above a defined threshold where standard verification "
            "cannot be completed."
        ),
        "regulatory_reference": "FATF Recommendation 16 (Wire Transfers); AMLA Art. 9; FINMA AML Circular",
        "private_banking_context": (
            "Private banking clients may legitimately require urgent transfers for time-sensitive "
            "transactions such as property closings or investment subscriptions. The red flag "
            "arises when urgency is used systematically to suppress compliance checks, when "
            "the stated purpose cannot be verified, or when the beneficiary has not previously "
            "featured in the client's transaction history."
        ),
        "examples": [
            "Client calls RM demanding immediate CHF 3 million transfer for a 'deal closing today' to an account never previously used",
            "Operations receives pressure to waive compliance callback for urgent USD 5 million wire with a beneficiary in a high-risk jurisdiction",
            "Recurring urgent transfer requests to different beneficiaries over a 30-day period, each accompanied by a different stated purpose",
        ],
    },

    {
        "rf_id": "RF013",
        "category": "AML",
        "title": "Sudden refusal of re-profiling",
        "description": (
            "A client who previously cooperated with KYC and periodic review processes "
            "abruptly refuses to participate in a scheduled or triggered re-profiling "
            "exercise — including updating source of wealth, providing current documentation, "
            "or confirming UBO information. Sudden refusal after prior cooperation is a "
            "significant behavioural change requiring immediate compliance assessment."
        ),
        "risk_level": "High",
        "detection_method": (
            "Track compliance with periodic review requests in the client management system. "
            "Flag all accounts where a re-profiling request has been outstanding beyond 30 "
            "days without client engagement. Compliance must assess all refusal cases for "
            "STR filing obligation and account restriction necessity."
        ),
        "regulatory_reference": "AMLA Art. 7; FINMA AML Circular; FATF Recommendation 10",
        "private_banking_context": (
            "In private banking, periodic review can be postponed for relationship management "
            "reasons — client travelling, advisor gap, documentation complexity — creating "
            "opportunities for compliance timelines to lapse without genuine escalation. "
            "A sudden refusal following a change in the client's personal or business "
            "circumstances (e.g., media exposure, criminal investigation in home country) "
            "is particularly significant."
        ),
        "examples": [
            "Client who completed full KYC at onboarding refuses to provide updated UBO documentation at triennial review",
            "Previously cooperative client declines to answer source of wealth questions following news reports linking them to a corruption investigation",
            "Client instructs RM 'not to send any more compliance questionnaires' and threatens to transfer assets if review proceeds",
        ],
    },

    {
        "rf_id": "RF014",
        "category": "AML",
        "title": "Sudden change in transactional behaviour",
        "description": (
            "A client's transaction pattern undergoes a material and unexplained shift — such "
            "as a dramatic increase in transfer volume, a change in counterparty geography, "
            "or a shift from investment to high-frequency cash-like transactions — without "
            "a corresponding change in documented business activities or personal circumstances. "
            "Sudden behavioural changes are among the most reliable indicators of emerging "
            "AML or financial crime risk."
        ),
        "risk_level": "High",
        "detection_method": (
            "Deploy behavioural analytics to establish normalised transaction baselines per "
            "client and generate automated alerts for deviations exceeding defined thresholds "
            "(e.g., volume increase >200%, new geography >3 new jurisdictions in 30 days). "
            "RM review is mandatory for all material behavioural shift alerts within 5 business days."
        ),
        "regulatory_reference": "FATF Recommendation 20; AMLA Art. 9; FINMA AML Circular",
        "private_banking_context": (
            "Private banking relationship managers are well-positioned to detect behavioural "
            "changes through client interaction, but this detection depends on active monitoring "
            "rather than reactive documentation. Automated behavioural analytics are increasingly "
            "required to complement RM judgment, particularly for dormant accounts that reactivate "
            "with high-volume activity."
        ),
        "examples": [
            "Client who had maintained a stable equity portfolio for five years suddenly initiates 40 outbound wires over 30 days",
            "Dormant account reactivates with CHF 8 million inflow followed by immediate fragmented outbound transfers",
            "Client transitions from primarily CHF-denominated transactions to a mix of USD, AED, and HKD without business rationale",
        ],
    },

    {
        "rf_id": "RF015",
        "category": "AML",
        "title": "Multiple accounts without justification",
        "description": (
            "The client maintains multiple accounts at the same institution — across different "
            "booking centres, legal entities, or currency books — without a documented business "
            "rationale for the structural separation. Multiple accounts with overlapping "
            "beneficiary patterns may be used to fragment transaction volumes and evade "
            "monitoring thresholds."
        ),
        "risk_level": "Medium",
        "detection_method": (
            "Conduct periodic cross-account analysis to identify clients with three or more "
            "accounts and assess whether the structural separation is documented and justified. "
            "Aggregate transaction monitoring across all accounts held by the same UBO "
            "to prevent fragmentation-based threshold evasion."
        ),
        "regulatory_reference": "FATF Recommendation 10; AMLA Art. 3; FINMA AML Circular",
        "private_banking_context": (
            "HNWI clients legitimately maintain multiple accounts for currency management, "
            "entity-specific booking, or discretionary mandate segregation. The red flag "
            "arises where account multiplication is unexplained, where transfers between "
            "own accounts are used to obscure fund flows, or where different accounts "
            "are managed through different RMs with no consolidated oversight."
        ),
        "examples": [
            "Client holds seven accounts across three booking centres with no documented business reason for the structural separation",
            "Transfers between client's own accounts aggregate to CHF 15 million over a month, each individually below the reporting threshold",
            "Different family members hold nominally separate accounts that are effectively controlled by a single UBO without disclosure",
        ],
    },

    # ── Fraud (RF016–RF025) ────────────────────────────────────────────────────

    {
        "rf_id": "RF016",
        "category": "Fraud",
        "title": "Rogue advisor — unauthorised trades",
        "description": (
            "A relationship manager or portfolio manager executes transactions in a client's "
            "account without explicit client authorisation or in excess of the authority granted "
            "under the client's mandate. Unauthorised trading may be motivated by fee generation, "
            "position unwinding, or personal financial gain, and can result in significant client "
            "losses and institutional liability."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Implement systematic comparison of executed transactions against client-signed "
            "instruction records or discretionary mandate parameters. Generate exception reports "
            "for all trades executed without a corresponding client instruction record in advisory "
            "mandates. Surprise trade reconciliation audits should be conducted for high-activity "
            "advisory portfolios quarterly."
        ),
        "regulatory_reference": "FinSA Art. 9–10; MiFID II Art. 25; Swiss Code of Obligations Art. 398",
        "private_banking_context": (
            "The trust-based private banking relationship model, in which clients often defer "
            "to advisor judgment without reviewing individual trade confirmations, creates "
            "conditions in which unauthorised trading can persist for extended periods. "
            "The risk is highest where a single RM has exclusive client contact and controls "
            "both the advisory relationship and transaction initiation."
        ),
        "examples": [
            "RM executes 30 equity purchases in a client's advisory account over six months with no documented client instructions on file",
            "Portfolio manager invests client's capital in illiquid structured products not permitted under the agreed mandate parameters",
            "Advisor transfers client assets between own accounts and client account without authorisation, concealed through falsified confirmations",
        ],
    },

    {
        "rf_id": "RF017",
        "category": "Fraud",
        "title": "Churning — excessive portfolio turnover",
        "description": (
            "A relationship manager or portfolio manager generates excessive trading activity "
            "in a client account — measured by turnover ratio relative to portfolio size — "
            "primarily to generate commission or transaction fee income rather than to serve "
            "the client's investment objectives. Churning results in direct client cost and "
            "potential underperformance relative to a buy-and-hold benchmark."
        ),
        "risk_level": "High",
        "detection_method": (
            "Calculate annualised portfolio turnover ratios for all advisory and discretionary "
            "accounts and flag accounts where turnover exceeds a defined threshold (e.g., 200% "
            "annually for equity mandates). Cross-reference against the investment objective "
            "and compare transaction costs paid against peer benchmarks. Management review "
            "required for outlier accounts."
        ),
        "regulatory_reference": "FinSA Art. 9; MiFID II Art. 25; ESMA Guidelines on MiFID II Suitability",
        "private_banking_context": (
            "In retrocession-based compensation models (where permitted), churning incentives "
            "are structurally embedded. Even in advisory fee models, excessive trading can "
            "arise from RM incentives tied to transaction volume. Private banking clients "
            "who trust their advisors implicitly may not scrutinise trade confirmations "
            "closely enough to detect churning before significant costs accumulate."
        ),
        "examples": [
            "Advisory account with CHF 5 million in assets generates CHF 250,000 in transaction costs annually — 5% cost drag",
            "Portfolio manager executes 120 trades per year in a conservative balanced mandate, resulting in 350% annual turnover",
            "Client's equity portfolio is fully liquidated and reinvested three times in 18 months with no documented strategic rationale",
        ],
    },

    {
        "rf_id": "RF018",
        "category": "Fraud",
        "title": "Front-running on client orders",
        "description": (
            "A bank employee — typically a trader or RM — trades for their own account or "
            "a related party's account in the same securities as a pending client order, "
            "exploiting advance knowledge of the client order to profit from the anticipated "
            "price movement. Front-running constitutes market abuse and is a criminal offence "
            "in Switzerland and across EU jurisdictions."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Monitor personal trading accounts of client-facing employees and traders for "
            "transactions in the same securities as client orders placed within a defined "
            "time window (e.g., 24 hours before client order execution). Flag all matches "
            "for compliance investigation. Require pre-clearance for personal trades in "
            "securities within research or client order pipelines."
        ),
        "regulatory_reference": "Swiss FMIA Art. 142–143; MiFID II Art. 16; MAR Art. 8",
        "private_banking_context": (
            "Front-running risk in private banking arises primarily from RMs or investment "
            "advisors who receive large client orders in concentrated positions and can "
            "anticipate the price impact. The risk is heightened in illiquid securities "
            "or structured products where a single large client order is sufficient "
            "to move the market."
        ),
        "examples": [
            "Trader buys 50,000 shares of a small-cap equity 10 minutes before executing a client purchase order of 500,000 shares",
            "RM purchases call options on a stock the day before executing a large discretionary buy order for client portfolios",
            "Investment desk employee shorts a bond on personal account before distributing a sell recommendation to client portfolios",
        ],
    },

    {
        "rf_id": "RF019",
        "category": "Fraud",
        "title": "Misappropriation of client assets",
        "description": (
            "A bank employee — typically a relationship manager or back-office staff member "
            "— diverts client funds or securities to their own account or a related party's "
            "account, concealing the diversion through falsified records, false statements "
            "to the client, or manipulation of the client management system. "
            "Misappropriation is a criminal offence under Swiss law and invariably triggers "
            "FINMA notification obligations."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Conduct surprise reconciliations of client asset holdings against custodian "
            "records independently of the RM relationship. Implement system access controls "
            "preventing individual employees from both initiating and approving transactions. "
            "Independent client statement confirmation exercises — contacting clients directly "
            "to verify portfolio values — should be conducted annually for all advisory accounts."
        ),
        "regulatory_reference": "Swiss SCC Art. 138; Banking Act Art. 3; FINMA notification obligation",
        "private_banking_context": (
            "Misappropriation in private banking is particularly insidious because HNWI "
            "clients typically review their portfolios infrequently and trust their "
            "relationship manager completely. The absence of independent custodian "
            "confirmation and the reliance on RM-produced portfolio reporting creates "
            "an environment in which small-scale misappropriation can compound over "
            "years before detection."
        ),
        "examples": [
            "RM transfers CHF 500,000 from client account to a personal account over 18 months through a series of small transfers disguised as advisory fees",
            "Back-office employee creates fictitious redemption instructions to divert fund proceeds to a controlled account",
            "RM provides client with falsified portfolio statements showing full asset values while having sold positions for personal gain",
        ],
    },

    {
        "rf_id": "RF020",
        "category": "Fraud",
        "title": "Client document falsification",
        "description": (
            "KYC or account documentation submitted by or on behalf of a client is found "
            "to be falsified, altered, or fabricated — including identity documents, "
            "source of wealth certificates, corporate registration documents, or "
            "financial statements. Document falsification may be client-initiated or "
            "facilitated by bank employees or external intermediaries."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Implement document authentication procedures including biometric passport "
            "NFC chip verification, third-party corporate registry cross-referencing, "
            "and reverse image search for identity document fraud detection. Flag "
            "documents with inconsistent formatting, unusual metadata, or discrepancies "
            "against independent sources for specialist review."
        ),
        "regulatory_reference": "Swiss SCC Art. 251 (forgery); AMLA Art. 3; FINMA AML Circular",
        "private_banking_context": (
            "The complexity of HNWI documentation — including foreign corporate records, "
            "trust deeds from less transparent jurisdictions, and wealth certificates "
            "from private accountants — creates more opportunities for falsification "
            "than in standardised retail onboarding. External asset managers introducing "
            "clients may inadvertently or deliberately facilitate document fraud."
        ),
        "examples": [
            "Passport submitted during onboarding found to have altered date of birth when cross-referenced against INTERPOL database",
            "Source of wealth certificate from a private accountant in a high-risk jurisdiction cannot be verified and shows formatting inconsistencies",
            "Corporate registration documents provided for a Cayman Islands holding company are fabricated — the company does not appear in registry records",
        ],
    },

    {
        "rf_id": "RF021",
        "category": "Fraud",
        "title": "Identity fraud during onboarding",
        "description": (
            "A fraudster assumes the identity of another individual — including through "
            "stolen identity documents, deepfake video presentation, or proxy use — "
            "to open or take over a private banking account. Identity fraud during "
            "onboarding bypasses the legitimate client's risk profile and creates "
            "accounts under false identities for subsequent illicit use."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Deploy liveness detection and biometric matching in digital onboarding flows "
            "per FINMA-RS 2016/7 requirements. For high-value accounts, require in-person "
            "identity verification or certified notary confirmation. Cross-reference "
            "document metadata, IP address geolocation, and device fingerprint for "
            "digital onboarding sessions."
        ),
        "regulatory_reference": "FINMA-RS 2016/7; AMLA Art. 3; FATF Recommendation 10",
        "private_banking_context": (
            "Private banking digital onboarding — increasingly adopted for efficiency — "
            "creates identity fraud vulnerability where high account values provide "
            "strong criminal motivation. The HNWI context is particularly exposed "
            "to deepfake-enabled identity impersonation, as HNWI individuals' facial "
            "and voice data is often available through public media."
        ),
        "examples": [
            "Fraudster presents a high-quality deepfake video during online onboarding, passing standard liveness checks",
            "Stolen passport of a prominent businessperson used to open an account by a third party presenting similar physical characteristics",
            "Account opened in the name of a recently deceased individual using their authentic identity documents before death registration",
        ],
    },

    {
        "rf_id": "RF022",
        "category": "Fraud",
        "title": "Targeted phishing against HNWI clients",
        "description": (
            "HNWI clients are targeted by highly personalised spear-phishing attacks — "
            "crafted using publicly available or previously stolen information about "
            "the client's relationships, investments, and lifestyle — designed to "
            "obtain login credentials, authorise fraudulent transactions, or extract "
            "sensitive personal information. Spear-phishing against HNWI clients "
            "is a growing and sophisticated fraud vector."
        ),
        "risk_level": "High",
        "detection_method": (
            "Monitor for anomalous client portal login activity — unusual geolocation, "
            "device, or time-of-day patterns. Implement out-of-band transaction "
            "confirmation for high-value transfers. Client education programme on "
            "spear-phishing recognition should be delivered annually with incident "
            "reporting mechanisms."
        ),
        "regulatory_reference": "FINMA-RS 2023/1; DORA Art. 17; Swiss SCC Art. 147",
        "private_banking_context": (
            "HNWI clients are high-value targets whose public profiles — on corporate "
            "websites, social media, and press releases — provide attackers with "
            "the raw material for highly credible impersonation. The private banking "
            "relationship's personalised communication style makes it easier for "
            "fraudsters to craft convincing mimicry of legitimate bank communications."
        ),
        "examples": [
            "Client receives a phishing email mimicking the bank's domain, with the RM's name and the client's correct account number, requesting login credentials",
            "HNWI targeted with a spear-phishing SMS claiming urgent action is required to prevent account closure, linking to a credential-harvesting site",
            "Attacker uses LinkedIn data to craft a phishing email referencing the client's recent board appointment and investment activity",
        ],
    },

    {
        "rf_id": "RF023",
        "category": "Fraud",
        "title": "Social engineering via family office",
        "description": (
            "Fraudsters target the family office structure — employees, advisors, or "
            "family members involved in wealth management — to gain access to client "
            "accounts, authorise transactions, or extract sensitive information. "
            "Family offices are attractive targets due to their significant financial "
            "authority, smaller compliance teams, and less robust cybersecurity "
            "infrastructure than institutional banks."
        ),
        "risk_level": "High",
        "detection_method": (
            "Maintain a current register of all authorised family office representatives "
            "for each client relationship, with documented authority levels. Implement "
            "callback verification for all transaction instructions received from family "
            "office contacts above a defined threshold. Monitor for new or changed "
            "contact information purportedly from family offices."
        ),
        "regulatory_reference": "FINMA-RS 2023/1; Swiss SCC Art. 147; FATF Recommendation 10",
        "private_banking_context": (
            "Family offices managing HNWI wealth often operate with substantial discretionary "
            "authority over client accounts, creating an extended attack surface beyond the "
            "directly identified client. Social engineering through family office staff "
            "can be more effective than direct client targeting due to lower awareness "
            "and weaker security protocols."
        ),
        "examples": [
            "Fraudster impersonates the family office CFO by email and requests an urgent CHF 2 million wire to a new beneficiary",
            "Social engineer builds a long-term relationship with a family office junior employee, eventually obtaining account access credentials",
            "Deepfake audio call simulating the family patriarch's voice instructs the private bank to change wire transfer authorisation contacts",
        ],
    },

    {
        "rf_id": "RF024",
        "category": "Fraud",
        "title": "Unauthorised third-party instructions",
        "description": (
            "Instructions for account actions — transfers, investment changes, beneficiary "
            "amendments — are received from a third party who has not been formally authorised "
            "by the client through documented power of attorney or mandate arrangements. "
            "Acting on unauthorised third-party instructions exposes the bank to civil "
            "liability and may facilitate fraud against the client."
        ),
        "risk_level": "High",
        "detection_method": (
            "Maintain a current, signed register of authorised third-party representatives "
            "for each client account, with clearly defined authority scope and validity period. "
            "Reject all instructions from unregistered third parties and require the client "
            "to confirm authority in writing before any action is taken."
        ),
        "regulatory_reference": "Swiss Code of Obligations Art. 32; FinSA Art. 9; FINMA AML Circular",
        "private_banking_context": (
            "In private banking, instructions from lawyers, accountants, family members, "
            "and external asset managers are common and often legitimate — but the "
            "informal culture of trusting known advisors creates risk where authority "
            "is assumed rather than verified. Elderly or incapacitated clients are "
            "particularly vulnerable to third-party instruction fraud."
        ),
        "examples": [
            "Client's accountant calls the bank requesting a CHF 1 million transfer, citing client approval 'already given verbally' — no written authority on file",
            "Person claiming to be the client's son instructs the bank to change the beneficiary address for recurring transfers",
            "External asset manager exceeds their documented mandate scope by requesting redemption of assets outside the agreed investment universe",
        ],
    },

    {
        "rf_id": "RF025",
        "category": "Fraud",
        "title": "Fake inheritance / windfall scams",
        "description": (
            "A client is approached by fraudsters — sometimes through the bank's communication "
            "channels — with a fraudulent inheritance, lottery, or windfall opportunity requiring "
            "an advance payment or account access to release a large sum. The client is persuaded "
            "to transfer funds or provide account details, resulting in direct financial loss "
            "and potential account compromise."
        ),
        "risk_level": "High",
        "detection_method": (
            "Monitor outgoing transfers to previously unknown beneficiaries accompanied by "
            "client-stated justifications consistent with advance-fee fraud patterns. "
            "Train RMs to recognise behavioural indicators of client victimisation — "
            "urgency, secrecy, unusual counterparty profile — and to initiate a welfare "
            "check and compliance escalation."
        ),
        "regulatory_reference": "Swiss SCC Art. 146; FINMA AML Circular; FCA Consumer Duty (reference)",
        "private_banking_context": (
            "Advance-fee and windfall fraud disproportionately targets elderly HNWI clients "
            "who may be socially isolated and less familiar with digital fraud vectors. "
            "The private banking relationship manager is often the first institutional "
            "contact who can identify victimisation before it results in significant loss — "
            "but only if trained and empowered to intervene."
        ),
        "examples": [
            "78-year-old client requests an urgent CHF 500,000 transfer to release an inheritance from a deceased Nigerian diplomat — a classic advance-fee pattern",
            "Client received an email purportedly from the bank's wealth management team announcing a prize draw win requiring an administrative deposit",
            "Recently widowed client persuaded by a new 'romantic interest' to transfer CHF 300,000 as an 'investment in their joint future'",
        ],
    },

    # ── Suitability (RF026–RF033) ──────────────────────────────────────────────

    {
        "rf_id": "RF026",
        "category": "Suitability",
        "title": "Complex products sold to unsophisticated clients",
        "description": (
            "Structured products — including barrier reverse convertibles, auto-callables, "
            "leveraged certificates, or capital-at-risk notes — are recommended to or held "
            "by clients whose documented risk profile, financial knowledge, or investment "
            "experience does not meet the product's complexity and risk threshold. This "
            "represents a core FinSA suitability failure with significant conduct liability."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Conduct systematic product-to-client suitability mapping for all structured "
            "product holdings, cross-referencing product risk rating and complexity score "
            "against client knowledge assessment and risk profile. Generate an exception "
            "report for all mismatches and require documented compliance review before "
            "any new structured product recommendation to sub-threshold clients."
        ),
        "regulatory_reference": "FinSA Art. 10–12; MiFID II Art. 25; PRIIPs KID Regulation",
        "private_banking_context": (
            "Structured products are a significant revenue generator in Swiss private banking, "
            "and the commercial pressure to distribute complex instruments can result in "
            "suitability documentation that reflects post-hoc justification rather than "
            "genuine pre-sale assessment. The CS AT1 write-down (2023) crystallised the "
            "litigation exposure from selling regulatory capital instruments without "
            "adequate bail-in risk disclosure."
        ),
        "examples": [
            "Client classified as 'balanced' with no derivatives experience holds a portfolio comprising 40% barrier reverse convertibles",
            "Auto-callable structured note with 50% capital protection barrier sold to a 75-year-old client with a 'capital preservation' objective",
            "Leveraged commodity certificate recommended to a client who indicated on their knowledge assessment that they had no understanding of leverage mechanics",
        ],
    },

    {
        "rf_id": "RF027",
        "category": "Suitability",
        "title": "Excessive concentration in single asset",
        "description": (
            "A client's portfolio is concentrated in a single issuer, sector, or asset class "
            "at a level materially exceeding the diversification parameters implied by their "
            "risk profile and investment objective. Excessive concentration creates "
            "idiosyncratic risk that is inconsistent with the stated mandate and exposes "
            "the bank to suitability liability if the concentrated position suffers losses."
        ),
        "risk_level": "High",
        "detection_method": (
            "Run quarterly portfolio concentration analysis for all managed and advisory "
            "mandates, flagging portfolios where a single issuer exceeds 20% of NAV or "
            "a single sector exceeds 40% unless explicitly documented as client instruction "
            "and suitability-assessed. Senior investment oversight review required for "
            "all flagged portfolios."
        ),
        "regulatory_reference": "FinSA Art. 10; MiFID II Art. 25; ESMA Suitability Guidelines",
        "private_banking_context": (
            "HNWI clients frequently have legitimate concentrated positions — founder equity "
            "stakes, inherited shareholdings, or strategic investments — that are not managed "
            "by the private bank. The suitability risk arises when the bank's managed or "
            "advisory portfolio adds further concentration on top of known external "
            "concentrations, without consolidating the full client wealth picture."
        ),
        "examples": [
            "Discretionary mandate portfolio holds 45% in a single technology stock, with no documented client instruction to deviate from diversification parameters",
            "Client's advisory portfolio concentrates 70% in Swiss real estate investment trusts, inconsistent with their documented 'globally diversified equity' objective",
            "Portfolio manager adds a 30% position in an emerging market bond fund to a client profile whose knowledge assessment excludes emerging market fixed income",
        ],
    },

    {
        "rf_id": "RF028",
        "category": "Suitability",
        "title": "Risk profile not updated >24 months",
        "description": (
            "A client's investment risk profile, financial situation assessment, or investment "
            "objective documentation has not been reviewed or updated within the past 24 months, "
            "or has not been updated following a known material change in the client's "
            "circumstances (retirement, inheritance, divorce, health event). Stale profiles "
            "create suitability exposure where portfolio positioning continues to be based "
            "on outdated client information."
        ),
        "risk_level": "High",
        "detection_method": (
            "Generate automated alerts for all client accounts where the risk profile "
            "documentation date exceeds 24 months or where the bank is aware of a material "
            "life event that has not been reflected in an updated profile. Compliance review "
            "is required before any new product recommendation for clients with stale profiles."
        ),
        "regulatory_reference": "FinSA Art. 12; MiFID II Art. 25; ESMA Suitability Guidelines",
        "private_banking_context": (
            "In private banking, periodic risk profile updates are frequently deferred "
            "by relationship managers to avoid client friction — particularly for older "
            "clients who resist being asked to complete questionnaires. The regulatory "
            "expectation is unambiguous: profiles must be current to support ongoing "
            "suitability assessments, regardless of client preference."
        ),
        "examples": [
            "Client turns 70 and retires — risk profile still documents 'growth-oriented' objective based on assessment conducted at age 65",
            "Client inherited EUR 20 million following a parent's death 18 months ago; risk profile has not been updated to reflect changed financial situation",
            "Risk profile last updated in 2022; client has since disclosed a terminal health diagnosis that materially affects investment time horizon",
        ],
    },

    {
        "rf_id": "RF029",
        "category": "Suitability",
        "title": "Divergence between client instructions and transactions",
        "description": (
            "Executed transactions in a client's account materially diverge from the "
            "instructions recorded in the client's mandate, the most recent client "
            "communication, or the agreed investment strategy. Systematic divergence "
            "between instructions and execution may indicate unauthorised trading, "
            "system error, or suitability failure."
        ),
        "risk_level": "High",
        "detection_method": (
            "Implement systematic instruction-to-execution matching for advisory accounts, "
            "with exception reports generated for all transactions where no corresponding "
            "client instruction is recorded within a defined time window. Quarterly "
            "portfolio reviews should include a reconciliation of portfolio positioning "
            "against the agreed investment strategy."
        ),
        "regulatory_reference": "FinSA Art. 9; MiFID II Art. 25; Swiss Code of Obligations Art. 398",
        "private_banking_context": (
            "The personalised, relationship-driven nature of private banking means that "
            "verbal instructions are frequently acted upon without contemporaneous written "
            "confirmation. This creates an instruction record gap that makes divergence "
            "between intent and execution difficult to detect and document."
        ),
        "examples": [
            "Client gives verbal instruction to maintain defensive positioning; RM executes significant equity increase the following week with no recorded client confirmation",
            "Discretionary mandate positioned as 60% equity / 40% bonds drifts to 85% equity without rebalancing or client notification",
            "Client instructs sale of all positions in a specific sector on ethical grounds; RM fails to execute the instruction and positions remain",
        ],
    },

    {
        "rf_id": "RF030",
        "category": "Suitability",
        "title": "Absent suitability documentation for structured products",
        "description": (
            "Structured product recommendations or transactions are executed without the "
            "required pre-sale suitability assessment documentation — including client "
            "knowledge assessment, risk profile confirmation, and product-specific "
            "risk disclosure acknowledgement. The absence of suitability documentation "
            "creates unmitigated regulatory and civil liability in the event of loss."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Conduct a retrospective audit of all structured product transactions in the "
            "past 24 months to verify that pre-sale suitability documentation is complete "
            "and on file for each transaction. Implement a system control requiring "
            "suitability assessment sign-off before structured product orders can be "
            "entered in the order management system."
        ),
        "regulatory_reference": "FinSA Art. 10–12; PRIIPs KID Regulation; MiFID II Art. 25",
        "private_banking_context": (
            "Structured product documentation gaps are endemic in Swiss private banking "
            "due to the pace of distribution, reliance on verbal client agreement, and "
            "the volume of products transacted. The CS AT1 litigation post-2023 write-down "
            "demonstrated that documentation gaps convert regulatory risk into client "
            "litigation exposure at scale."
        ),
        "examples": [
            "Barrier reverse convertible transaction executed in 2024 with no pre-sale KID acknowledgement on file",
            "Client's holding of EUR 1 million in auto-callable notes has no corresponding suitability assessment in the client file",
            "Structured note recommended via WhatsApp message from RM — no written suitability documentation, risk profile confirmation, or KID provision on record",
        ],
    },

    {
        "rf_id": "RF031",
        "category": "Suitability",
        "title": "Recommendations without written justification",
        "description": (
            "Investment recommendations — whether for specific securities, asset allocation "
            "changes, or structured products — are made to clients without a contemporaneous "
            "written record of the suitability rationale. FinSA and MiFID II require that "
            "the basis for suitability assessments be documented and retainable for regulatory "
            "review."
        ),
        "risk_level": "High",
        "detection_method": (
            "Sample advisory client files and verify that each material investment recommendation "
            "in the past 12 months has a corresponding written suitability note explaining why "
            "the recommendation meets the client's investment objective, risk profile, and "
            "financial situation. Flag accounts where recommendations exceed documented "
            "advisory interactions."
        ),
        "regulatory_reference": "FinSA Art. 15; MiFID II Art. 25(6); FINMA AML Circular (documentation)",
        "private_banking_context": (
            "The relationship-driven advisory model in private banking — characterised by "
            "verbal conversations, informal emails, and WhatsApp messages — creates a "
            "structural documentation deficit. Senior RMs often make investment recommendations "
            "in the course of client lunches or informal calls without generating written "
            "suitability records, creating latent compliance exposure."
        ),
        "examples": [
            "RM recommends a CHF 500,000 reallocation to emerging market equities during a client dinner — no written suitability note generated",
            "Client file contains 15 trade confirmations for the past year but only three written investment recommendations with suitability rationale",
            "Advisory account review conducted by email with no documented suitability assessment — only a portfolio performance summary",
        ],
    },

    {
        "rf_id": "RF032",
        "category": "Suitability",
        "title": "Vulnerable client (age/health) without safeguards",
        "description": (
            "A client who is elderly, cognitively impaired, recently bereaved, or otherwise "
            "in a vulnerable condition continues to be managed without enhanced safeguards — "
            "such as designated trusted contact persons, restricted product access, enhanced "
            "instruction verification, or periodic welfare checks. Vulnerable client management "
            "is an emerging regulatory priority with significant conduct and civil liability implications."
        ),
        "risk_level": "High",
        "detection_method": (
            "Maintain a vulnerable client register identifying clients who have been assessed "
            "as potentially vulnerable based on age, disclosed health conditions, behavioural "
            "observations, or life events. Conduct periodic welfare-oriented review calls "
            "for all clients on the register and document outcomes. Compliance sign-off "
            "required for all significant transactions initiated by registered vulnerable clients."
        ),
        "regulatory_reference": "FinSA Art. 10; FCA Consumer Duty (reference); Swiss Civil Code on capacity",
        "private_banking_context": (
            "Private banking serves a disproportionately older HNWI client population, "
            "and cognitive decline among long-standing clients is a structural challenge "
            "that the sector has historically addressed insufficiently. The combination "
            "of significant wealth, reduced financial literacy capacity, and social isolation "
            "creates acute third-party exploitation risk."
        ),
        "examples": [
            "85-year-old client with documented early-stage dementia continues to have a high-risk discretionary mandate with no documented safeguard review",
            "Recently widowed client displaying significant emotional distress is approached by the RM with a complex restructuring proposal within weeks of bereavement",
            "Client's family members raise concerns about cognitive capacity with the bank — RM documents the concern but takes no action pending relationship management considerations",
        ],
    },

    {
        "rf_id": "RF033",
        "category": "Suitability",
        "title": "Undisclosed conflict of interest on in-house products",
        "description": (
            "A relationship manager or investment advisor recommends in-house investment "
            "products — proprietary funds, structured products manufactured by the bank's "
            "own desks, or products generating retrocessions — without disclosing the "
            "material conflict of interest arising from the bank's financial interest "
            "in the recommendation. Non-disclosure of conflicts violates FinSA's "
            "transparency requirements and MiFID II's inducement rules."
        ),
        "risk_level": "High",
        "detection_method": (
            "Audit a sample of advisory recommendations for in-house product concentration "
            "and cross-reference against disclosed conflicts of interest in client "
            "documentation. Verify that all retrocession arrangements are disclosed "
            "in the client agreement and that in-house product recommendations include "
            "a specific conflict disclosure note."
        ),
        "regulatory_reference": "FinSA Art. 25–26; MiFID II Art. 23; FINMA-RS 2017/1",
        "private_banking_context": (
            "In-house product recommendations are a significant source of private banking "
            "revenue, and the commercial pressure to place proprietary products can "
            "compromise advisory independence. The prohibition on undisclosed retrocessions "
            "under FinSA and MiFID II has not eliminated the underlying conflict — it "
            "has shifted it to disclosures that are technically compliant but practically "
            "ineffective in communicating the conflict to clients."
        ),
        "examples": [
            "RM recommends that 60% of client AUM be allocated to the bank's proprietary multi-asset fund range without disclosing the bank's fund management fee income",
            "Structured note manufactured by the bank's own desk recommended to client without disclosure that the issuing desk receives a distribution margin",
            "Client's discretionary mandate is systematically overweight in the bank's own funds relative to peer benchmarks — conflict disclosed in boilerplate but not specifically highlighted",
        ],
    },

    # ── Tax (RF034–RF040) ──────────────────────────────────────────────────────

    {
        "rf_id": "RF034",
        "category": "Tax",
        "title": "Offshore structures with no economic substance",
        "description": (
            "A client maintains offshore legal entities — holding companies, trusts, "
            "or investment vehicles — in low-tax jurisdictions that lack genuine "
            "economic substance: no real employees, no management decisions made locally, "
            "no physical presence, and no commercial purpose beyond asset holding or "
            "tax minimisation. Substance-less offshore structures are a primary OECD "
            "BEPS and CRS compliance risk."
        ),
        "risk_level": "High",
        "detection_method": (
            "During CDD reviews, assess documented economic substance for all offshore "
            "entities held by the client. Request evidence of local management, "
            "employees, and genuine economic activity. Flag entities registered in "
            "known zero-substance jurisdictions (BVI, Cayman, Panama, Seychelles) "
            "without corresponding substance documentation for compliance tax review."
        ),
        "regulatory_reference": "OECD BEPS Action 5; CRS; EU Anti-Tax Avoidance Directive",
        "private_banking_context": (
            "HNWI clients frequently use offshore holding structures for legitimate "
            "investment and estate planning purposes, but the line between legitimate "
            "tax efficiency and artificial arrangement lacking substance is increasingly "
            "scrutinised by OECD member states and CRS information recipients. "
            "The bank's CRS reporting obligations make it a de facto participant "
            "in the automatic disclosure of these structures."
        ),
        "examples": [
            "Client holds CHF 30 million through a BVI company with a professional nominee director, no employees, and no documented business purpose",
            "Cayman Islands limited partnership holds a portfolio of Swiss equities with no identifiable investment management function in the Cayman jurisdiction",
            "Client's holding structure includes four layered companies across three zero-tax jurisdictions — none with documented management or operational activity",
        ],
    },

    {
        "rf_id": "RF035",
        "category": "Tax",
        "title": "Beneficial owner in FATF/OECD-monitored jurisdiction",
        "description": (
            "The beneficial owner of a client account resides in or is a national of a "
            "jurisdiction subject to heightened FATF or OECD tax transparency scrutiny, "
            "including jurisdictions on the EU non-cooperative jurisdictions list or "
            "with limited CRS exchange relationships. This combination elevates both "
            "AML and tax compliance risk simultaneously."
        ),
        "risk_level": "High",
        "detection_method": (
            "Cross-reference client UBO residency and nationality against current FATF "
            "grey/black lists, EU non-cooperative jurisdictions list, and OECD Global "
            "Forum peer review outcomes. Flag all matches for enhanced CRS classification "
            "review and compliance tax assessment."
        ),
        "regulatory_reference": "CRS; FATF Recommendation 10; EU Directive on Administrative Cooperation",
        "private_banking_context": (
            "The Swiss private banking client base includes significant representation "
            "from jurisdictions with evolving or limited AEOI participation, creating "
            "complex CRS classification challenges and elevated tax facilitation risk "
            "for accounts held by beneficial owners in such jurisdictions."
        ),
        "examples": [
            "Beneficial owner is a national and resident of a jurisdiction that joined CRS only in 2024, with no exchange with Switzerland yet operational",
            "Client's UBO is resident in a jurisdiction on the EU's list of non-cooperative jurisdictions for tax purposes",
            "Account held through a trust whose settlor and beneficiaries are nationals of a jurisdiction with identified tax transparency deficiencies",
        ],
    },

    {
        "rf_id": "RF036",
        "category": "Tax",
        "title": "Refusal to sign FATCA/CRS self-certification",
        "description": (
            "A client refuses or persistently delays signing the FATCA and/or CRS "
            "self-certification form required for account maintenance and regulatory "
            "reporting compliance. Refusal to self-certify is a significant indicator "
            "of potential undisclosed tax status and triggers specific regulatory "
            "obligations for the bank."
        ),
        "risk_level": "High",
        "detection_method": (
            "Track all outstanding self-certification requests in the tax compliance "
            "management system with escalation alerts at 30 and 60 days. Compliance "
            "must assess all refusal cases for account restriction necessity and, "
            "where applicable, FATCA presumption rules (treat account as US reportable "
            "absent valid certification) or CRS undocumented account treatment."
        ),
        "regulatory_reference": "FATCA (IRS 1471–1474); CRS OECD Standard; AMLA Art. 7",
        "private_banking_context": (
            "In private banking, self-certification requests for complex entity structures "
            "or clients with multi-jurisdictional tax exposure can face genuine legal and "
            "tax advisory complexity. However, systematic refusal — particularly correlated "
            "with jurisdictions where CRS reporting would result in disclosure to tax "
            "authorities — is a significant tax facilitation risk indicator."
        ),
        "examples": [
            "Client with apparent US indicia (address, telephone number, birthplace) refuses to complete W-9 or W-8 self-certification for three consecutive years",
            "Entity account holder declines to identify its controlling persons for CRS purposes, citing 'confidentiality' — no legal basis provided",
            "Client annually requests extension of self-certification deadline without engaging substantively with the documentation requirement",
        ],
    },

    {
        "rf_id": "RF037",
        "category": "Tax",
        "title": "Sudden change of tax residency",
        "description": (
            "A client declares a sudden change of tax residency — particularly to a "
            "jurisdiction with favourable tax treatment, limited CRS exchange with "
            "their apparent home country, or recent removal from the OECD's list "
            "of cooperative jurisdictions — without a plausible personal or business "
            "rationale for the relocation. Tax residency changes may be genuine but "
            "require enhanced verification in the private banking context."
        ),
        "risk_level": "High",
        "detection_method": (
            "Flag all self-certification updates reflecting a change of tax residency "
            "for compliance review. Request supporting evidence of genuine relocation "
            "(proof of address, utility bills, residency permit) and cross-reference "
            "against the client's known lifestyle, business activities, and travel patterns. "
            "Enhanced due diligence required where the new jurisdiction has materially "
            "different CRS obligations."
        ),
        "regulatory_reference": "CRS Section VI; FATCA IGA; FINMA AML Circular",
        "private_banking_context": (
            "HNWI clients are genuinely geographically mobile and may legitimately "
            "relocate for personal, professional, or family reasons. The red flag "
            "arises when the declared new tax residency correlates with an imminent "
            "CRS reporting cycle, when the client has no apparent personal connection "
            "to the new jurisdiction, or when the relocation is to a jurisdiction "
            "with known tax information exchange limitations."
        ),
        "examples": [
            "Client declares Portuguese tax residency under NHR regime weeks before the first CRS reporting deadline, having shown no prior connection to Portugal",
            "Long-standing French-resident client declares UAE tax residency coincident with French CRS exchange effective date",
            "Client claims to have relocated to a jurisdiction that does not participate in CRS exchange with their apparent home country — no supporting documentation provided",
        ],
    },

    {
        "rf_id": "RF038",
        "category": "Tax",
        "title": "Declarations inconsistent with lifestyle",
        "description": (
            "The client's declared tax and financial profile — including declared income, "
            "wealth sources, and tax residency — is materially inconsistent with their "
            "observable lifestyle indicators: property holdings, travel patterns, "
            "consumer expenditure, and social profile. The inconsistency raises the "
            "possibility of undeclared income or assets."
        ),
        "risk_level": "High",
        "detection_method": (
            "Conduct lifestyle cross-referencing during onboarding and periodic review "
            "by comparing declared income and wealth against observable indicators "
            "accessible through open-source research (property registries, press coverage, "
            "social media). Significant unexplained discrepancies require documented "
            "RM and compliance assessment."
        ),
        "regulatory_reference": "AMLA Art. 6; FINMA AML Circular; CRS Commentaries on Due Diligence",
        "private_banking_context": (
            "Private banking clients' lifestyles — luxury real estate, private aviation, "
            "superyachts, art collections — are often publicly visible and provide "
            "a valuable cross-reference for the plausibility of declared financial profiles. "
            "Relationship managers who are embedded in client social networks are "
            "well-positioned to identify lifestyle-declaration inconsistencies but "
            "may have limited incentive to escalate them."
        ),
        "examples": [
            "Client declares annual income of EUR 150,000 while maintaining three Swiss properties, a private jet subscription, and a CHF 25 million portfolio",
            "Tax certificate from client's home country shows modest declared assets — inconsistent with known spending patterns observed by RM",
            "Client describes themselves as a 'retired teacher' but funds appear to support a lifestyle consistent with significantly higher wealth levels",
        ],
    },

    {
        "rf_id": "RF039",
        "category": "Tax",
        "title": "Use of nominee directors/shareholders",
        "description": (
            "The client's legal structures employ nominee directors or shareholders — "
            "professional service providers who appear in corporate records as directors "
            "or shareholders but have no genuine management authority or economic interest — "
            "to conceal the true beneficial owner from company registries and due diligence "
            "processes. Nominee arrangements are a primary vehicle for beneficial ownership "
            "opacity."
        ),
        "risk_level": "High",
        "detection_method": (
            "Identify nominee arrangements during UBO mapping through the use of corporate "
            "registry searches, industry-specific nominee provider databases, and director "
            "network analysis tools. Require signed nominee declarations confirming the "
            "identity of the true principal and the scope of the nominee arrangement "
            "for all entities with identified nominees."
        ),
        "regulatory_reference": "FATF Recommendations 24–25; AMLA Art. 4; EU AMLD6",
        "private_banking_context": (
            "Nominee arrangements are endemic in offshore wealth structures and are "
            "frequently encountered in Swiss private banking client onboarding. While "
            "some nominee arrangements are legitimate (estate planning, privacy), "
            "they systematically impede UBO identification and are a primary vehicle "
            "for tax avoidance and AML risk. Enhanced diligence must pierce the "
            "nominee layer to identify the genuine controlling person."
        ),
        "examples": [
            "All five directors of a BVI holding company are employees of a professional nominee services firm with no independent relationship to the client",
            "Corporate shareholder appears in five unrelated client structures as a registered shareholder — a classic nominee company pattern",
            "Nominee director signs all corporate documentation but is unable to describe the company's business activities when contacted independently",
        ],
    },

    {
        "rf_id": "RF040",
        "category": "Tax",
        "title": "Absent Tax Identification Number (TIN)",
        "description": (
            "A client or beneficial owner is unable or unwilling to provide a valid Tax "
            "Identification Number (TIN) for their declared tax residency jurisdiction "
            "as required for CRS and FATCA self-certification. Absence of a TIN may "
            "indicate undisclosed tax residency, use of a false residency declaration, "
            "or registration in a jurisdiction that does not issue TINs."
        ),
        "risk_level": "Medium",
        "detection_method": (
            "Verify TIN format against OECD TIN format databases for each declared "
            "jurisdiction. Flag accounts where TIN is absent, cannot be validated, "
            "or where the stated justification for absence does not correspond to "
            "the jurisdiction's actual TIN issuance practice. Compliance review "
            "required for all TIN-absent accounts above defined materiality threshold."
        ),
        "regulatory_reference": "CRS Standard Section VI; FATCA IRS Form W-8/W-9; OECD TIN Guidance",
        "private_banking_context": (
            "In private banking, TIN absence is frequently encountered for clients "
            "from jurisdictions with non-standard TIN systems, elderly clients "
            "who have not received a TIN, or clients who have recently relocated. "
            "The risk arises where TIN absence is not explained by a legitimate "
            "jurisdiction-specific reason but may reflect deliberate residency "
            "misrepresentation."
        ),
        "examples": [
            "Client declares UK tax residency but cannot provide a UTR (Unique Taxpayer Reference) — states they have 'never received one'",
            "Entity self-certifies as resident in Switzerland but cannot provide a UID (Unternehmens-Identifikationsnummer) — entity is not registered in Swiss commercial registry",
            "Client provides a TIN format inconsistent with the format issued by their declared tax residency jurisdiction according to OECD guidance",
        ],
    },

    # ── Conduct (RF041–RF045) ──────────────────────────────────────────────────

    {
        "rf_id": "RF041",
        "category": "Conduct",
        "title": "Abnormal personal advisor–client relationship",
        "description": (
            "The relationship between a relationship manager and a client displays "
            "characteristics that extend beyond professional norms — including personal "
            "financial entanglement, social dependency, gifts of significant value, "
            "joint personal investments, or cohabitation. Abnormal personal relationships "
            "create conflicts of interest, impair professional judgment, and create "
            "conditions for exploitation or misconduct."
        ),
        "risk_level": "High",
        "detection_method": (
            "Conduct periodic review of RM–client relationship disclosures and personal "
            "conflict of interest declarations. Implement annual self-certification "
            "requiring RMs to disclose personal financial relationships with clients. "
            "Supervisory oversight of client relationships managed by RMs with flagged "
            "personal connections should include independent transaction review."
        ),
        "regulatory_reference": "FINMA-RS 2017/1; FinSA Art. 25; Swiss Code of Obligations Art. 398",
        "private_banking_context": (
            "The long-term, intimate nature of private banking relationships — spanning "
            "decades, involving shared family milestones, and extending to multiple "
            "family generations — creates conditions in which personal and professional "
            "boundaries can erode. The risk is that an RM's personal dependency on a "
            "client relationship impairs their ability to exercise independent "
            "professional judgment or to escalate concerning client behaviours."
        ),
        "examples": [
            "RM accepts a 10% stake in a client's privately held company as a 'thank you' for years of service — undisclosed to the bank",
            "Relationship manager regularly attends client's private family events and holidays — personal relationship has effectively replaced professional distance",
            "RM has loaned personal funds to a client experiencing a liquidity shortfall while simultaneously managing their CHF 20 million portfolio",
        ],
    },

    {
        "rf_id": "RF042",
        "category": "Conduct",
        "title": "Undisclosed gifts or benefits",
        "description": (
            "A bank employee — typically a relationship manager or investment advisor — "
            "receives gifts, hospitality, or other benefits from clients, third-party "
            "product providers, or external asset managers without disclosing them "
            "in accordance with the bank's gifts and entertainment policy. Undisclosed "
            "benefits create conflicts of interest that may impair professional objectivity "
            "and violate FinSA's inducement provisions."
        ),
        "risk_level": "High",
        "detection_method": (
            "Require annual gifts and entertainment register self-certification from all "
            "client-facing employees. Conduct periodic spot-checks of employee social "
            "media and expense records for indicators of undisclosed hospitality. "
            "Compliance review of all declared gifts above the bank's materiality "
            "threshold for acceptance approval."
        ),
        "regulatory_reference": "FinSA Art. 25–26; FINMA-RS 2017/1; Swiss Criminal Code Art. 322",
        "private_banking_context": (
            "The private banking culture of client entertainment — dinners, sporting events, "
            "private travel — normalises the receipt of benefits that may, at higher "
            "values or frequencies, constitute undisclosed inducements. The risk is "
            "highest where product providers (structured product desks, fund managers) "
            "provide benefits to RMs who distribute their products, creating undisclosed "
            "distribution incentives."
        ),
        "examples": [
            "RM accepts a CHF 10,000 watch from a client following a large investment transaction — gift not declared in compliance register",
            "Product provider hosting an RM and guests at a private event estimated at CHF 5,000 per person — not declared as a potential inducement",
            "RM regularly receives case lots of wine from a client — cumulative annual value exceeds CHF 3,000 policy threshold without disclosure",
        ],
    },

    {
        "rf_id": "RF043",
        "category": "Conduct",
        "title": "Transactions outside business hours without authorisation",
        "description": (
            "Significant client transactions — particularly large wire transfers, "
            "portfolio restructurings, or security sales — are initiated outside "
            "normal business hours without documented emergency authorisation, "
            "senior management approval, or client-instructed urgency. Out-of-hours "
            "transaction initiation outside approved procedures is a conduct and "
            "fraud risk indicator."
        ),
        "risk_level": "High",
        "detection_method": (
            "Generate exception reports for all transactions initiated outside defined "
            "business hours (e.g., before 07:00 or after 20:00 local time) above a "
            "defined materiality threshold. Require documented authorisation chain for "
            "all out-of-hours transactions, including client instruction timestamp "
            "and approving officer identity."
        ),
        "regulatory_reference": "FINMA-RS 2023/1; FINMA-RS 2008/21; Internal Control Framework",
        "private_banking_context": (
            "Private banking's culture of client responsiveness — including the expectation "
            "that senior RMs are available outside business hours for high-value client "
            "needs — creates a grey zone in which out-of-hours transaction processing "
            "can be normalised without adequate control. The risk is heightened for "
            "remote access transactions initiated from personal devices or home systems."
        ),
        "examples": [
            "CHF 3 million wire transfer initiated at 02:00 on a Saturday with no documented client instruction or management approval",
            "RM remotely executes a large portfolio liquidation on a Sunday evening — documented rationale references a 'client phone call' with no callback verification",
            "Pattern of transactions consistently initiated outside business hours by a single RM for a specific client cluster — not authorised through exception process",
        ],
    },

    {
        "rf_id": "RF044",
        "category": "Conduct",
        "title": "Circumvention of four-eyes principle",
        "description": (
            "A material transaction, client instruction, or operational action is processed "
            "by a single employee without the required secondary authorisation (four-eyes "
            "control). Circumvention may occur through procedural override, shared login "
            "credentials, retrospective approval, or manipulation of the authorisation "
            "workflow. Four-eyes circumvention is a primary internal fraud enabler."
        ),
        "risk_level": "Critical",
        "detection_method": (
            "Implement system-enforced four-eyes controls in the transaction management "
            "system, preventing single-employee authorisation above defined thresholds. "
            "Conduct quarterly audit sampling of high-value transactions to verify "
            "that both authorisers were independently active in the system at the "
            "time of approval. Investigate all shared login or credential delegation instances."
        ),
        "regulatory_reference": "FINMA-RS 2008/21; FINMA-RS 2017/1; Basel Committee on Banking Supervision Principles",
        "private_banking_context": (
            "In private banking, the four-eyes principle can be undermined by the "
            "hierarchical deference afforded to senior relationship managers — "
            "junior colleagues may provide nominal secondary authorisation without "
            "genuinely reviewing the transaction. System controls must be designed "
            "to make genuine independent review a prerequisite, not merely a "
            "documentation exercise."
        ),
        "examples": [
            "Senior RM uses a junior colleague's login credentials to process a self-authorised transaction while the junior employee is on leave",
            "Four-eyes approval workflow bypassed for an 'urgent' CHF 2 million transfer through a manual override not subsequently reviewed by compliance",
            "Audit trail shows both authorisers approved a transaction within 30 seconds of each other — implying rubber-stamp approval without genuine review",
        ],
    },

    {
        "rf_id": "RF045",
        "category": "Conduct",
        "title": "Verbal instructions not confirmed in writing",
        "description": (
            "Material client instructions — investment transactions, beneficiary changes, "
            "mandate modifications, or risk profile updates — are acted upon based "
            "on verbal communication without subsequent written confirmation from the "
            "client. Acting on unconfirmed verbal instructions creates an evidentiary "
            "gap that exposes the bank to client disputes, regulatory scrutiny, and "
            "potential fraud facilitation."
        ),
        "risk_level": "High",
        "detection_method": (
            "Implement a policy requiring written confirmation — email, signed letter, "
            "or secure digital channel — for all material transactions and account "
            "changes above defined thresholds, with a mandatory confirmation window "
            "before execution. Audit a sample of transaction records quarterly "
            "to verify that written instruction documentation exists for all "
            "material actions."
        ),
        "regulatory_reference": "FinSA Art. 15; MiFID II Art. 25(6); FINMA AML Circular",
        "private_banking_context": (
            "The reliance on verbal instruction in private banking is deeply embedded "
            "in the relationship model — clients expect their advisor to act on a "
            "phone call or meeting instruction without bureaucratic confirmation "
            "requirements. This cultural expectation must be balanced against "
            "the documented regulatory obligation to maintain a contemporaneous "
            "record of client instructions, which verbal-only execution systematically fails to meet."
        ),
        "examples": [
            "RM executes a CHF 5 million portfolio reallocation based on a verbal instruction given during a client lunch — no written confirmation obtained",
            "Beneficiary change processed following a telephone call with the client — no written confirmation secured before account update",
            "Client claims they never authorised a series of trades — RM has no written instruction on file, only a personal note from a telephone call",
        ],
    },

]

# ═══════════════════════════════════════════════════════════════════════════════
# MANAGEMENT_ACTION_TEMPLATES
# Suggested management actions per audit theme — Swiss private banking context
# ═══════════════════════════════════════════════════════════════════════════════

MANAGEMENT_ACTION_TEMPLATES = {
    "AML_KYC": [
        {
            "action": "Deploy automated PEP and sanctions screening tool integrated with real-time watchlists (e.g. World-Check, Dow Jones) and configure daily refresh cycles",
            "owner": "Chief Compliance Officer",
            "due": "3 months",
        },
        {
            "action": "Review and update the AML/KYC policy framework to ensure full alignment with FATF 40 Recommendations, FINMA-RS 2011/1 and the revised Anti-Money Laundering Act (AMLA)",
            "owner": "Compliance / Legal",
            "due": "2 months",
        },
        {
            "action": "Design and deliver mandatory Enhanced Due Diligence (EDD) training for all Relationship Managers, covering red-flag identification, source-of-wealth documentation and escalation procedures",
            "owner": "HR / Compliance",
            "due": "1 month",
        },
        {
            "action": "Initiate a 100% retrospective KYC file review for all High-Risk and PEP client relationships, documenting remediation actions and escalating unresolved gaps to the MLRO within 10 business days",
            "owner": "Compliance / Business Lines",
            "due": "3 months",
        },
        {
            "action": "Establish a formalised Suspicious Transaction Report (STR) escalation workflow with documented decision trees, mandatory senior Compliance sign-off and Board-level reporting metrics",
            "owner": "MLRO",
            "due": "2 months",
        },
    ],
    "CYBER_RISK": [
        {
            "action": "Commission an independent penetration test of all internet-facing systems and critical internal infrastructure, with findings tracked to closure in the risk register within agreed remediation SLAs",
            "owner": "Chief Information Security Officer",
            "due": "3 months",
        },
        {
            "action": "Implement privileged access management (PAM) controls including just-in-time access provisioning, session recording and quarterly recertification of all privileged accounts",
            "owner": "IT Security / IT Operations",
            "due": "3 months",
        },
        {
            "action": "Develop and test a cyber incident response playbook covering ransomware, data exfiltration and DDoS scenarios, with defined FINMA notification timelines in line with DORA Article 19",
            "owner": "CISO / Business Continuity",
            "due": "2 months",
        },
        {
            "action": "Roll out mandatory phishing-simulation training for all staff on a quarterly basis, with targeted awareness sessions for employees who fail simulations",
            "owner": "HR / Information Security",
            "due": "1 month",
        },
        {
            "action": "Establish a third-party cyber risk assessment process requiring all critical technology vendors to complete an annual security questionnaire aligned to ISO/IEC 27001 and FINMA ICT outsourcing guidelines",
            "owner": "CISO / Procurement",
            "due": "3 months",
        },
    ],
    "CREDIT_RISK": [
        {
            "action": "Introduce an automated Lombard lending margin-call workflow with real-time collateral valuation feeds, mandatory RM notification within 24 hours and escalation triggers to the Credit Risk Committee",
            "owner": "Chief Risk Officer / Credit Risk",
            "due": "3 months",
        },
        {
            "action": "Conduct a full review of the credit concentration framework, setting single-name, sector and asset-class limits consistent with FINMA-RS 2019/1 large-exposure rules and Board-approved risk appetite",
            "owner": "Credit Risk / Finance",
            "due": "2 months",
        },
        {
            "action": "Implement an independent annual review cycle for all credit facilities exceeding CHF 5 million, with mandatory reassessment of client financial position, collateral adequacy and covenant compliance",
            "owner": "Credit Risk Committee",
            "due": "6 months",
        },
        {
            "action": "Update loan-loss provisioning methodology to align with IFRS 9 expected credit loss (ECL) requirements, including model validation by an independent internal or external reviewer",
            "owner": "Finance / Risk Management",
            "due": "3 months",
        },
        {
            "action": "Design and execute stress-test scenarios for the Lombard and mortgage portfolios assuming equity drawdowns of 30%, interest rate rises of 200 bps and currency shocks of 15%, with results reported to the Board Risk Committee",
            "owner": "CRO / Treasury",
            "due": "2 months",
        },
    ],
    "OPERATIONAL_RISK": [
        {
            "action": "Complete a comprehensive Risk and Control Self-Assessment (RCSA) across all business lines, with risk owners formally attesting to residual risk ratings and control effectiveness on a semi-annual basis",
            "owner": "Operational Risk / Business Lines",
            "due": "3 months",
        },
        {
            "action": "Update the Business Continuity Plan (BCP) and IT Disaster Recovery (DR) procedures to reflect current infrastructure, with a full end-to-end simulation exercise validated by senior management",
            "owner": "Business Continuity Management",
            "due": "3 months",
        },
        {
            "action": "Establish a centralised operational loss-event database with mandatory reporting thresholds, root-cause analysis requirements and escalation protocols to the Operational Risk Committee",
            "owner": "Operational Risk",
            "due": "2 months",
        },
        {
            "action": "Review all material outsourcing arrangements against FINMA-RS 2017/6 requirements, ensuring written contracts include audit rights, business-continuity obligations and exit strategies",
            "owner": "Compliance / Procurement / Legal",
            "due": "3 months",
        },
        {
            "action": "Implement an end-to-end process for capturing, assessing and tracking Key Risk Indicators (KRIs) with breach-reporting workflows feeding into quarterly Board Risk Committee reporting",
            "owner": "CRO / Operational Risk",
            "due": "2 months",
        },
    ],
    "DATA_PRIVACY": [
        {
            "action": "Conduct a gap analysis between current data handling practices and the Swiss nDSG (Federal Act on Data Protection, revised 2023) requirements, producing a remediation roadmap with ownership and target dates",
            "owner": "Data Protection Officer / Legal",
            "due": "2 months",
        },
        {
            "action": "Implement a data-subject rights management platform to handle access, rectification and erasure requests within statutory 30-day response deadlines, with audit trails for every request",
            "owner": "DPO / IT",
            "due": "3 months",
        },
        {
            "action": "Establish a comprehensive Records of Processing Activities (RoPA) register covering all personal data flows, with annual review and mandatory sign-off by business process owners",
            "owner": "DPO / Business Lines",
            "due": "3 months",
        },
        {
            "action": "Embed Privacy by Design review checkpoints into the project delivery lifecycle, requiring a Data Protection Impact Assessment (DPIA) for all new systems processing client personal data",
            "owner": "DPO / Project Management",
            "due": "2 months",
        },
        {
            "action": "Review and update all cross-border data transfer agreements (including Standard Contractual Clauses) to ensure compliance with nDSG adequacy requirements and FINMA cross-border data transfer guidance",
            "owner": "Legal / Compliance",
            "due": "3 months",
        },
    ],
    "MARKET_RISK": [
        {
            "action": "Calibrate and independently validate the Value-at-Risk (VaR) model using a minimum three-year historical data set, with backtesting results reported monthly to the Market Risk Committee",
            "owner": "Market Risk / Model Validation",
            "due": "3 months",
        },
        {
            "action": "Define and implement Interest Rate Risk in the Banking Book (IRRBB) limits aligned with BIS Standards (April 2016) and FINMA-RS 2019/2, with sensitivity analysis reviewed quarterly by ALCO",
            "owner": "Treasury / ALCO",
            "due": "3 months",
        },
        {
            "action": "Develop a stressed market scenario library covering equity crashes, FX dislocations and credit spread widening, and integrate results into the ICAAP capital planning process",
            "owner": "Risk Management / Finance",
            "due": "2 months",
        },
        {
            "action": "Establish real-time trading-desk limit monitoring with automated breach alerts, mandatory RM and desk-head sign-off on breaches and next-day reporting to senior management",
            "owner": "Market Risk / Front Office",
            "due": "2 months",
        },
        {
            "action": "Prepare the bank for FRTB (Fundamental Review of the Trading Book) Standardised Approach reporting, including a data-quality remediation programme and parallel-run timeline agreed with the CFO",
            "owner": "CRO / Finance / IT",
            "due": "6 months",
        },
    ],
    "THIRD_PARTY_RISK": [
        {
            "action": "Develop and implement a Third-Party Risk Management (TPRM) framework covering initial due diligence, ongoing monitoring and annual re-assessment of all critical and non-critical vendors",
            "owner": "Procurement / Risk Management",
            "due": "3 months",
        },
        {
            "action": "Ensure all material outsourcing contracts include mandatory audit-rights clauses, data-security requirements, business-continuity obligations and termination/exit strategies in line with FINMA-RS 2017/6",
            "owner": "Legal / Procurement",
            "due": "3 months",
        },
        {
            "action": "Establish a vendor concentration risk register identifying single points of failure in critical service supply chains, and define contingency plans for the top-five highest-risk vendors",
            "owner": "CRO / Procurement",
            "due": "2 months",
        },
        {
            "action": "Implement a continuous performance and compliance monitoring programme for Tier-1 vendors, including quarterly SLA reporting, on-site review rights and escalation procedures for material breaches",
            "owner": "Vendor Management / Compliance",
            "due": "3 months",
        },
        {
            "action": "Conduct an immediate review of fourth-party (sub-contractor) exposure across all critical outsourced functions, documenting concentration risk and presenting findings to the Board Audit Committee",
            "owner": "Risk Management / Procurement",
            "due": "2 months",
        },
    ],
    "GOVERNANCE": [
        {
            "action": "Formalise a Three Lines of Defence model with clearly documented mandates, escalation paths and accountability matrices, approved by the Board and reviewed annually",
            "owner": "Board / Chief Risk Officer",
            "due": "2 months",
        },
        {
            "action": "Strengthen the Internal Audit Charter to reflect IIA International Standards (2024 edition), ensuring organisational independence, unrestricted access and direct reporting line to the Board Audit Committee",
            "owner": "Chief Audit Executive",
            "due": "1 month",
        },
        {
            "action": "Implement a Board-level Risk Appetite Statement (RAS) with quantitative thresholds for each material risk category, reviewed and formally approved at least annually and cascaded to business-line risk limits",
            "owner": "Board / CRO",
            "due": "3 months",
        },
        {
            "action": "Establish a formal Management Action tracking system for all internal audit, regulatory and external review findings, with mandatory evidence submission, escalation of overdue items and quarterly BAC reporting",
            "owner": "Internal Audit / Compliance",
            "due": "2 months",
        },
        {
            "action": "Design and deliver a Board-level financial crime and governance training programme, covering directors' personal liability, FINMA supervisory expectations and the bank's internal risk culture framework",
            "owner": "Legal / Compliance / HR",
            "due": "3 months",
        },
    ],
    "CROSS_BORDER": [
        {
            "action": "Conduct a jurisdiction-by-jurisdiction mapping of all client bookings to identify markets where the bank lacks a valid licence or local law exemption, and escalate findings to Legal and senior management within 30 days",
            "owner": "Legal / Compliance",
            "due": "1 month",
        },
        {
            "action": "Establish a Cross-Border Services Committee with documented approval procedures, country-specific risk assessments and annual renewal of the permitted-activities register for each target market",
            "owner": "Compliance / Legal / Business",
            "due": "3 months",
        },
        {
            "action": "Implement mandatory pre-travel compliance clearance for all Relationship Managers undertaking client visits abroad, with documented country risk assessments and records retained for regulatory inspection",
            "owner": "Compliance / HR",
            "due": "2 months",
        },
        {
            "action": "Review marketing materials and digital communications sent to foreign clients to ensure compliance with local solicitation rules, with legal sign-off required before dissemination in restricted jurisdictions",
            "owner": "Legal / Marketing",
            "due": "2 months",
        },
        {
            "action": "Engage external local counsel in the top-five cross-border booking markets to obtain written opinions on the bank's permitted activities, and incorporate findings into the annual compliance risk assessment",
            "owner": "Legal / Compliance",
            "due": "3 months",
        },
    ],
    "INVESTMENT_SUITABILITY": [
        {
            "action": "Implement system-level suitability pre-trade checks that block or flag transactions inconsistent with the client's documented risk profile, investment horizon and MiFID II / LSFin appropriateness criteria before order execution",
            "owner": "Chief Investment Officer / IT",
            "due": "3 months",
        },
        {
            "action": "Conduct a retrospective review of discretionary mandates over the past 12 months to identify concentration breaches, style drift and undocumented deviations from mandate guidelines, with findings reported to the Investment Committee",
            "owner": "Investment Risk / Compliance",
            "due": "2 months",
        },
        {
            "action": "Revise the client risk-profiling questionnaire to capture liquidity needs, sustainability preferences and capacity for loss, with mandatory annual re-assessment and event-driven updates for material life changes",
            "owner": "Compliance / Business Lines",
            "due": "2 months",
        },
        {
            "action": "Establish a product-governance framework requiring formal approval of all new investment products through an in-house Product Approval Committee before distribution, incorporating target-market analysis and stress-testing",
            "owner": "Product Management / Compliance",
            "due": "3 months",
        },
        {
            "action": "Implement a complaints management and root-cause analysis process for all suitability-related client complaints, with monthly reporting to senior management and regulatory notifications where required under LSFin",
            "owner": "Compliance / Client Relations",
            "due": "2 months",
        },
    ],
    "TAX_COMPLIANCE": [
        {
            "action": "Conduct a comprehensive review of all client accounts subject to CRS and FATCA reporting to identify gaps in self-certifications, TIN collection and reportable account classification, and remediate prior to the next annual submission deadline",
            "owner": "Tax / Compliance",
            "due": "3 months",
        },
        {
            "action": "Implement a systematic QI (Qualified Intermediary) compliance monitoring programme, including annual testing of withholding procedures, Form 1042-S reconciliation and periodic review of the bank's QI agreement obligations",
            "owner": "Tax / Finance",
            "due": "3 months",
        },
        {
            "action": "Update the bank's tax-risk policy to explicitly prohibit assistance with tax evasion structures, with mandatory legal and tax sign-off on all complex cross-border arrangements involving onshore/offshore fund flows",
            "owner": "Legal / Tax / Compliance",
            "due": "2 months",
        },
        {
            "action": "Design and deliver annual tax-compliance training for all Relationship Managers covering CRS/FATCA self-certification requirements, the prohibition on facilitating tax evasion and escalation procedures for suspicious client requests",
            "owner": "HR / Tax / Compliance",
            "due": "1 month",
        },
        {
            "action": "Engage external tax counsel to assess exposure under the OECD Pillar Two global minimum tax rules and DAC6 mandatory disclosure requirements, presenting a remediation plan to the CFO and Board Audit Committee",
            "owner": "CFO / Tax / Legal",
            "due": "3 months",
        },
    ],
    "FRAUD": [
        {
            "action": "Deploy a real-time transaction fraud-detection engine with machine-learning-based anomaly scoring, integrated with the core banking system and configured to generate alerts for same-day review by the Fraud Operations team",
            "owner": "Head of Fraud / IT Security",
            "due": "3 months",
        },
        {
            "action": "Establish a formal fraud-incident response playbook covering internal fraud, payment fraud, identity theft and social engineering, with defined escalation paths, regulatory notification timelines and client communication protocols",
            "owner": "Compliance / Operations / Legal",
            "due": "2 months",
        },
        {
            "action": "Implement mandatory dual-authorisation controls for all high-value payments above CHF 500,000 and all changes to beneficiary account details, with system-enforced segregation of duties between initiation and approval",
            "owner": "Operations / IT",
            "due": "2 months",
        },
        {
            "action": "Conduct a fraud-risk assessment across all client-facing digital channels, identifying social-engineering vulnerabilities, weak authentication controls and gaps in call-back verification for sensitive account changes",
            "owner": "Fraud Risk / CISO",
            "due": "2 months",
        },
        {
            "action": "Introduce an anonymous whistleblowing channel (compliant with nDSG and Swiss employment law) with an independent investigation process, formal non-retaliation policy and quarterly reporting of cases to the Board Audit Committee",
            "owner": "HR / Legal / Internal Audit",
            "due": "3 months",
        },
    ],
    "LIQUIDITY_RISK": [
        {
            "action": "Strengthen the Liquidity Coverage Ratio (LCR) monitoring framework to produce intraday liquidity positions for all material currencies, with automated breach alerts and same-day reporting to ALCO in stress conditions",
            "owner": "Treasury / Risk Management",
            "due": "2 months",
        },
        {
            "action": "Develop a comprehensive Internal Liquidity Adequacy Assessment Process (ILAAP) aligned with FINMA expectations, incorporating multiple stress scenarios including name-specific, market-wide and combined shocks",
            "owner": "CRO / Treasury / Finance",
            "due": "3 months",
        },
        {
            "action": "Review and formalise the Contingency Funding Plan (CFP), including identification of contingent liquidity sources, activation triggers, decision-making authorities and communication protocols with FINMA and counterparties",
            "owner": "Treasury / ALCO",
            "due": "2 months",
        },
        {
            "action": "Implement funds-transfer pricing (FTP) framework that correctly attributes liquidity costs and benefits to business lines, ensuring incentive alignment and accurate product profitability measurement",
            "owner": "Finance / Treasury",
            "due": "6 months",
        },
        {
            "action": "Conduct quarterly liquidity stress tests covering a 30-day severe stress horizon and a 12-month moderate stress scenario, with results reviewed by ALCO and summary reporting to the Board Risk Committee",
            "owner": "Risk Management / Treasury",
            "due": "3 months",
        },
    ],
    "ESG": [
        {
            "action": "Develop and publish a TCFD-aligned Climate Risk Disclosure report covering physical and transition risk exposures across the investment portfolio and lending book, reviewed by an independent third party before publication",
            "owner": "CRO / Sustainability / Finance",
            "due": "6 months",
        },
        {
            "action": "Establish ESG suitability assessment procedures for all discretionary and advisory mandates, integrating client sustainability preferences into the investment proposal process in line with LSFin Article 12 and Swiss Sustainable Finance guidelines",
            "owner": "Compliance / Investment Management",
            "due": "3 months",
        },
        {
            "action": "Implement a greenwashing risk framework with pre-publication review of all ESG-labelled product marketing materials, fund fact-sheets and client communications, requiring sign-off by Compliance and the Sustainability team",
            "owner": "Compliance / Sustainability / Marketing",
            "due": "2 months",
        },
        {
            "action": "Embed ESG and climate risk factors into the credit risk assessment framework for Lombard and mortgage portfolios, with Relationship Manager guidance on collateral haircuts for stranded-asset exposures",
            "owner": "Credit Risk / Sustainability",
            "due": "6 months",
        },
        {
            "action": "Define the bank's net-zero commitment pathway including scope 1, 2 and 3 emissions baseline, interim reduction targets and Board-approved governance structure for annual progress reporting",
            "owner": "Board / Sustainability / Finance",
            "due": "12 months",
        },
    ],
    "CRYPTO": [
        {
            "action": "Conduct a regulatory classification analysis for each crypto-asset type offered or held in custody, mapping instruments to applicable FINMA guidance (FINMA ICO Guidelines 2018, DLT Act 2021) and identifying any unlicensed activities",
            "owner": "Legal / Compliance",
            "due": "2 months",
        },
        {
            "action": "Implement enhanced AML/KYC controls for crypto-asset transactions, including Travel Rule compliance (FATF Recommendation 16) and automated blockchain analytics tools to screen wallet addresses for illicit-fund exposure",
            "owner": "Compliance / MLRO",
            "due": "3 months",
        },
        {
            "action": "Establish a crypto-asset custody risk framework covering private key management, cold/hot wallet segregation, multi-signature authorisation, insurance coverage and annual third-party security audit requirements",
            "owner": "Operations / CISO / Risk Management",
            "due": "3 months",
        },
        {
            "action": "Develop a crypto-asset market-risk stress-testing methodology reflecting the asset class's extreme volatility (e.g. 80% drawdown scenarios), with results integrated into the ICAAP and reported to the Board Risk Committee",
            "owner": "Market Risk / CRO",
            "due": "3 months",
        },
        {
            "action": "Produce a comprehensive client suitability and product-governance framework for crypto-asset services, ensuring appropriateness assessments, risk disclosures and execution-only safeguards comply with LSFin and FINMA expectations",
            "owner": "Compliance / Product Management",
            "due": "2 months",
        },
    ],
}

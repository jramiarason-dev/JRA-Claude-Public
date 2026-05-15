"""
AuditIQ — Static reference data library.
All data is hardcoded; zero API calls required.
"""

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
            "scope": "Banks subject to FINMA supervision; references Basel II/III operational risk framework",
            "key_requirements": [
                "Banks must maintain an operational risk management framework aligned with Basel II Pillar 2",
                "All material operational risk events must be captured in a loss database",
                "Risk and Control Self-Assessment (RCSA) must be performed at least annually",
                "Business continuity plans must be tested regularly and kept up to date",
                "Capital allocation for operational risk must use approved approach (BIA, TSA, or AMA)",
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
                "PEP screening mandatory; domestic and foreign PEPs require senior management approval",
                "Transaction monitoring must detect unusual patterns; SAR must be filed with MROS promptly",
                "AML risk assessment must be reviewed annually; high-risk clients reviewed at least annually",
            ],
            "applies_to": ["AML", "KYC", "Compliance"],
        },
        {
            "reference": "FINMA-RS 2023/1",
            "title": "Climate and Nature-Related Financial Risks",
            "authority": "FINMA",
            "year": 2023,
            "scope": "Systemically important banks; other banks on proportional basis",
            "key_requirements": [
                "Governance framework must explicitly assign responsibility for climate risk to Board and senior management",
                "Physical and transition risks must be integrated into credit, market, and operational risk frameworks",
                "Climate scenario analysis and stress testing must be performed at least annually",
                "Climate-related disclosures must align with TCFD framework; mandatory for SIBs from 2024",
                "Portfolio alignment metrics must be developed to assess transition risk exposure",
            ],
            "applies_to": ["Operational Risk", "Credit Risk", "Governance", "ESG"],
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
                "ICT-related incidents above defined thresholds must be reported to competent authority within 4 hours (major), 24 hours (significant), and 1 month final report (Art. 17-23)",
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
                "Output floor of 72.5% applied to RWA calculated using internal models vs. standardised approach",
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
                "R.12-13: Politically Exposed Persons — enhanced measures for PEPs and their family members/close associates",
                "R.16: Wire transfers — full originator and beneficiary information must accompany wire transfers",
                "R.20: Reporting of suspicious transactions — prompt filing with national FIU required",
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
        "key_risks": ["R001", "R002", "R003", "R004", "R005"],
        "recommended_tests": [
            "T001", "T002", "T003", "T004", "T005", "T006", "T007", "T008", "T009", "T010",
        ],
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
        "key_risks": ["R006", "R007", "R008", "R009", "R010"],
        "recommended_tests": [
            "T026", "T027", "T028", "T029", "T030", "T031", "T032", "T033", "T034", "T035",
        ],
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
        "key_risks": ["R011", "R012", "R013", "R014", "R015"],
        "recommended_tests": [
            "T046", "T047", "T048", "T049", "T050", "T051", "T052", "T053", "T054", "T055",
        ],
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
        "key_risks": ["R016", "R017", "R018", "R019", "R020"],
        "recommended_tests": [
            "T066", "T067", "T068", "T069", "T070", "T071", "T072", "T073", "T074", "T075",
        ],
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
        "key_risks": ["R021", "R022", "R023", "R024", "R025"],
        "recommended_tests": [
            "T086", "T087", "T088", "T089", "T090", "T091", "T092", "T093", "T094", "T095",
        ],
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
        "key_risks": ["R026", "R027", "R028", "R029", "R030"],
        "recommended_tests": [
            "T101", "T102", "T103", "T104", "T105", "T106", "T107", "T108", "T109", "T110",
        ],
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
        "key_risks": ["R031", "R032", "R033", "R034", "R035"],
        "recommended_tests": [
            "T116", "T117", "T118", "T119", "T120", "T121", "T122", "T123", "T124", "T125",
        ],
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
        "key_risks": ["R036", "R037", "R038", "R039", "R040"],
        "recommended_tests": [
            "T131", "T132", "T133", "T134", "T135", "T136", "T137", "T138", "T139", "T140",
        ],
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

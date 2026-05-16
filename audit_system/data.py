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
            "level": "Critical",
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
            "level": "Moderate",
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
            "level": "High",
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

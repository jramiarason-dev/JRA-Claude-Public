"""Pre-populate the database with realistic private banking EA content."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime, timedelta
import database as db


def seed():
    db.init_db()
    conn = db.get_connection()

    # ── EA Team ───────────────────────────────────────────────────────────────
    users = [
        ("Head of EA",                      "EA Lead",     None,        "Strategy & Governance"),
        ("Sr EA 1 — PWM / Application",     "EA Reviewer", "PWM",       "Application/Integration"),
        ("Sr EA 2 — PAS / Data & Security", "EA Reviewer", "PAS",       "Data/API/Security"),
        ("Sr EA 3 — Ops / Process",         "EA Reviewer", "Ops",       "Business Process/Workflow"),
        ("Risk & Compliance EA",            "EA Reviewer", "Cross-BL",  "Governance/Controls"),
        ("Cloud Architect EA",              "EA Reviewer", "PTech",     "Cloud/Infrastructure"),
    ]
    for name, role, bl, tech in users:
        conn.execute(
            "INSERT OR IGNORE INTO users (name, role, bl_domain, tech_domain) VALUES (?,?,?,?)",
            (name, role, bl, tech)
        )

    # ── Standards ─────────────────────────────────────────────────────────────
    standards = [
        ("STD-001", "API Gateway Pattern",
         "Integration", "Active",
         "All internal and external API calls must route through the approved API Gateway. "
         "Direct service-to-service HTTP calls are prohibited in production environments.",
         "Centralises authentication, rate-limiting, observability, and versioning.",
         ["PWM","PAS","Ops","PTech","Cross-BL"], "Mandatory",
         "Sr EA 1 — PWM / Application",
         ["ADR-2024-001"], ["PAT-001"]),

        ("STD-002", "Data Classification & Handling",
         "Security", "Active",
         "All data assets must be classified into one of four tiers: Public, Internal, "
         "Confidential, Restricted. Handling rules (encryption, access, retention) differ per tier.",
         "Regulatory requirement (FINMA, GDPR). Client financial data is Restricted by default.",
         ["PWM","PAS","Ops","PTech","Cross-BL"], "Mandatory",
         "Sr EA 2 — PAS / Data & Security",
         ["ADR-2024-002"], ["PAT-002"]),

        ("STD-003", "Cloud Landing Zone",
         "Cloud", "Active",
         "All cloud workloads must be provisioned within the approved AWS Landing Zone. "
         "Accounts outside the Landing Zone hierarchy are non-compliant.",
         "Ensures consistent security baseline, cost governance, and network segmentation.",
         ["PTech","PWM","PAS","Ops"], "Mandatory",
         "Cloud Architect EA",
         ["ADR-2024-003"], ["PAT-004"]),

        ("STD-004", "Event-Driven Architecture",
         "Integration", "Active",
         "Where asynchronous communication is required, prefer event-driven patterns "
         "using the approved event bus. Point-to-point messaging queues are discouraged.",
         "Decouples producers from consumers; improves resilience and scalability.",
         ["PWM","PAS","Ops"], "Recommended",
         "Sr EA 1 — PWM / Application",
         [], ["PAT-004"]),

        ("STD-005", "Microservices Decomposition Principles",
         "Application", "Active",
         "Services must be bounded by a single business capability. "
         "Shared databases across service boundaries are prohibited.",
         "Enables independent deployment, scaling, and team ownership.",
         ["PWM","PAS","Ops","PTech"], "Recommended",
         "Sr EA 1 — PWM / Application",
         [], ["PAT-005"]),

        ("STD-006", "Zero Trust Network Access",
         "Security", "Active",
         "No implicit trust based on network location. All access must be authenticated, "
         "authorised, and continuously validated. VPN-only access models are non-compliant.",
         "Aligns with FINMA cyber-resilience guidance and modern threat landscape.",
         ["PWM","PAS","Ops","PTech","Cross-BL"], "Mandatory",
         "Sr EA 2 — PAS / Data & Security",
         ["ADR-2024-004"], []),

        ("STD-007", "Data Residency — Switzerland",
         "Data", "Active",
         "Client personal and financial data must reside on infrastructure physically located "
         "in Switzerland. Cross-border replication requires explicit DPO approval.",
         "Swiss Banking Act and FINMA Circular 2023/01 requirements.",
         ["PWM","PAS","Ops","PTech","Cross-BL"], "Mandatory",
         "Sr EA 2 — PAS / Data & Security",
         [], []),

        ("STD-008", "Legacy Integration Wrapper Pattern",
         "Integration", "Active",
         "When integrating with legacy core banking systems, a dedicated anti-corruption "
         "layer (wrapper service) must be introduced. Direct coupling to legacy APIs is deprecated.",
         "Isolates modern services from legacy volatility and enables incremental migration.",
         ["PWM","PAS","Ops"], "Optional",
         "Sr EA 3 — Ops / Process",
         [], ["PAT-003"]),

        ("STD-009", "Observability & Logging Standards",
         "Cross-cutting", "Active",
         "All production services must emit structured logs (JSON), metrics (Prometheus format), "
         "and distributed traces (OpenTelemetry). Log retention minimum 13 months.",
         "Operational excellence and audit trail for regulatory examinations.",
         ["PWM","PAS","Ops","PTech","Cross-BL"], "Mandatory",
         "Cloud Architect EA",
         [], []),

        ("STD-010", "Third-Party Risk Assessment",
         "Security", "Active",
         "Any new third-party software or SaaS integration must complete a Technology Risk "
         "Assessment (TRA) before production use. TRA covers security, data privacy, "
         "operational resilience, and vendor concentration.",
         "Regulatory obligation; protects bank from supply chain and vendor risk.",
         ["PWM","PAS","Ops","PTech","Cross-BL"], "Mandatory",
         "Risk & Compliance EA",
         [], []),
    ]

    for row in standards:
        conn.execute("""
            INSERT OR IGNORE INTO standards
            (std_id, title, category, status, description, rationale, scope,
             compliance_level, owner, related_adrs, related_patterns)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (row[0], row[1], row[2], row[3], row[4], row[5],
              json.dumps(row[6]), row[7], row[8],
              json.dumps(row[9]), json.dumps(row[10])))

    # ── Patterns ──────────────────────────────────────────────────────────────
    patterns = [
        ("PAT-001", "API Gateway",
         "Integration",
         "Multiple clients need to access multiple backend services with varying auth, "
         "rate-limiting, and protocol requirements.",
         "Route all external and internal API traffic through a single API Gateway that handles "
         "auth, rate-limiting, routing, SSL termination, and request transformation.",
         "When you have multiple clients (mobile, web, partner) consuming multiple services.",
         "For internal service-to-service calls where overhead is unjustified (use service mesh instead).",
         "Client → API Gateway → [Auth Service, Rate Limiter] → Backend Microservices",
         "Approved", "Sr EA 1 — PWM / Application", ["STD-001"]),

        ("PAT-002", "CQRS for Wealth Data",
         "Data",
         "Read patterns for portfolio reporting differ vastly from write patterns for "
         "trade execution; combined model causes contention.",
         "Separate Command (write) and Query (read) models. Write side uses event sourcing; "
         "read side maintains materialised views optimised for reporting.",
         "High read:write ratio; complex reporting requirements; audit trail needed.",
         "Simple CRUD applications; teams without event sourcing experience.",
         "TradeCommand → EventStore → Projection → PortfolioReadModel → ReportingAPI",
         "Approved", "Sr EA 2 — PAS / Data & Security", ["STD-002","STD-004"]),

        ("PAT-003", "Strangler Fig for Legacy Migration",
         "Application",
         "Need to modernise a legacy monolith without a big-bang rewrite.",
         "Incrementally replace legacy functionality by routing new requests to new services "
         "while the legacy system handles remaining traffic. Retire legacy components progressively.",
         "Migrating core banking modules; replacing legacy reporting engines.",
         "Greenfield applications; when legacy cannot be wrapped without excessive complexity.",
         "Load Balancer → [New Service (new traffic), Legacy (remaining)] → Shared DB (transitional)",
         "Approved", "Sr EA 3 — Ops / Process", ["STD-008"]),

        ("PAT-004", "Cloud-Native Event Bus",
         "Cloud",
         "Services need to communicate asynchronously in a cloud-native, scalable way.",
         "Use Amazon EventBridge as the enterprise event bus. Producers publish domain events; "
         "consumers subscribe via event rules. Schema registry enforces event contracts.",
         "Asynchronous workflows; event-driven microservices; audit trail requirements.",
         "Synchronous request-reply patterns; low-latency trading systems.",
         "Producer → EventBridge Bus → Event Rules → [Consumer A, Consumer B, Archive]",
         "Approved", "Cloud Architect EA", ["STD-003","STD-004","STD-009"]),

        ("PAT-005", "Shared Nothing Multi-Tenant",
         "Application",
         "Multiple business lines need isolated data and processing with shared platform cost.",
         "Each tenant (BL) has dedicated data stores and compute; shared only at platform/control-plane level. "
         "No cross-tenant data access at application layer.",
         "SaaS-style platforms serving multiple BLs; regulatory data isolation requirements.",
         "Single-tenant deployments; where cross-BL reporting requires data joins.",
         "Platform Control Plane → [PWM Shard, PAS Shard, Ops Shard] (isolated DB + compute per shard)",
         "Approved", "Sr EA 1 — PWM / Application", ["STD-002","STD-005","STD-007"]),

        ("PAT-006", "Circuit Breaker",
         "Integration",
         "Cascading failures when downstream services are slow or unavailable.",
         "Wrap calls to downstream services with a circuit breaker. After N failures, "
         "the circuit opens and fast-fails for a configured period before attempting recovery.",
         "Any synchronous service dependency in production; especially external APIs.",
         "Asynchronous messaging (use dead-letter queues instead).",
         "ServiceA → CircuitBreaker(CLOSED→OPEN→HALF-OPEN) → ServiceB",
         "Approved", "Sr EA 1 — PWM / Application", ["STD-001"]),
    ]

    for row in patterns:
        conn.execute("""
            INSERT OR IGNORE INTO patterns
            (pat_id, title, category, problem, solution, when_to_use,
             when_not_to_use, example, status, owner, related_standards)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, row[:10] + (json.dumps(row[10]),))

    # ── ADRs ──────────────────────────────────────────────────────────────────
    adrs = [
        ("ADR-2024-001", "Adopt Kong API Gateway as Enterprise API Gateway",
         "Accepted",
         "The bank requires a centralised API gateway to enforce security policies, "
         "rate-limiting, and observability across all BL APIs. Multiple teams had "
         "implemented ad-hoc reverse proxy solutions.",
         "Adopt Kong Gateway (OSS) deployed on the AWS Landing Zone as the single "
         "enterprise API Gateway for all production APIs.",
         "Kong provides native integration with our AWS infrastructure, supports our "
         "authentication standards (OAuth2/JWT), and has an active enterprise support "
         "contract. Evaluated against AWS API Gateway, Apigee, and Traefik.",
         "Centralised observability and policy enforcement; reduced duplicated infrastructure.",
         "Operational complexity of managing Kong cluster; requires Kong-specific expertise.",
         "AWS API Gateway (rejected: limited on-prem support), Apigee (rejected: cost), "
         "Traefik (rejected: limited enterprise features)",
         "PWM", "Application/Integration",
         "Sr EA 1 — PWM / Application",
         ["Sr EA 2 — PAS / Data & Security", "Cloud Architect EA"],
         ["STD-001"], []),

        ("ADR-2024-002", "Adopt AWS Macie for Automated Data Classification",
         "Accepted",
         "Manual data classification is error-prone and does not scale with growing "
         "data volumes. STD-002 mandates classification of all data assets.",
         "Use AWS Macie integrated with S3 and our data catalogue to automate "
         "sensitive data discovery and classification tagging.",
         "Macie is native to our AWS Landing Zone, supports GDPR-relevant PII detection, "
         "and integrates with our existing Security Hub workflow.",
         "Automated enforcement of STD-002; reduced manual classification burden.",
         "Macie has limited coverage outside S3; databases require separate tooling.",
         "Varonis (rejected: cost), manual classification only (rejected: not scalable)",
         "PAS", "Data/API/Security",
         "Sr EA 2 — PAS / Data & Security",
         ["Risk & Compliance EA", "Cloud Architect EA"],
         ["STD-002"], []),

        ("ADR-2024-003", "AWS Control Tower as Cloud Landing Zone Foundation",
         "Accepted",
         "Cloud adoption was proceeding without consistent governance guardrails, "
         "leading to security and cost inconsistencies across accounts.",
         "Standardise on AWS Control Tower with customised SCPs and guardrails as "
         "the foundation for all cloud accounts.",
         "Control Tower provides out-of-the-box governance aligned with STD-003; "
         "AWS-native; aligns with our existing AWS Enterprise Support agreement.",
         "Consistent security baseline; automated account vending; cost governance.",
         "Control Tower version upgrades can be disruptive; limited multi-cloud support.",
         "Custom Terraform-only approach (rejected: governance overhead), "
         "Prisma Cloud (considered for CSPM overlay — retained)",
         "PTech", "Cloud/Infrastructure",
         "Cloud Architect EA",
         ["Head of EA", "Sr EA 2 — PAS / Data & Security"],
         ["STD-003"], []),

        ("ADR-2024-004", "Zero Trust with Zscaler Private Access",
         "Proposed",
         "Legacy VPN infrastructure does not meet STD-006 Zero Trust requirements. "
         "Remote access has expanded post-COVID and VPN has become a bottleneck.",
         "Replace VPN with Zscaler Private Access (ZPA) for all remote access. "
         "Integrate ZPA with our IdP (Azure AD) for identity-based access policies.",
         "ZPA aligns with Zero Trust principles; integrates with Azure AD; "
         "reduces attack surface by eliminating network-level access.",
         "Eliminates VPN; enables identity-based micro-segmentation; better UX.",
         "Significant migration effort; Zscaler dependency; higher licensing cost.",
         "Cloudflare Access (shortlisted), Palo Alto Prisma Access (shortlisted), "
         "Cisco Duo (rejected: limited ZTNA features)",
         "Cross-BL", "Governance/Controls",
         "Risk & Compliance EA",
         ["Cloud Architect EA", "Head of EA"],
         ["STD-006"], []),
    ]

    for row in adrs:
        conn.execute("""
            INSERT OR IGNORE INTO adrs
            (adr_number, title, status, context, decision, rationale,
             consequences_positive, consequences_negative, alternatives,
             bl_domain, tech_domain, author, reviewers, related_standards,
             related_requests, superseded_by, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
              row[9], row[10], row[11], json.dumps(row[12]),
              json.dumps(row[13]), json.dumps(row[14]), "", datetime.now().isoformat()))

    # ── Sample Arch Reviews ───────────────────────────────────────────────────
    now = datetime.now()
    arch_reviews = [
        {
            "reference": "AR-2025-001",
            "title": "PWM Client Portal — API Layer Redesign",
            "submitter_name": "Alexandre Martin",
            "submitter_role": "Solution Architect",
            "submitter_bl": "PWM",
            "description": "Complete redesign of the PWM client-facing API layer to adopt RESTful patterns, "
                           "introduce versioning, and integrate with the Kong API Gateway. "
                           "Current spaghetti of direct service calls will be replaced.",
            "arch_type": "Significant change",
            "affected_bls": ["PWM"],
            "complexity": "High",
            "urgency": "Standard",
            "standard_violation": "Suspected",
            "attachment_path": "",
            "routing_score": 5,
            "routing_tier": "Standard Review",
            "assigned_ea": "Sr EA 1 — PWM / Application",
            "status": "Under Review",
            "sla_deadline": (now + timedelta(days=8)).isoformat(),
        },
        {
            "reference": "AR-2025-002",
            "title": "PAS Trade Settlement — Event-Driven Refactor",
            "submitter_name": "Sarah Chen",
            "submitter_role": "Product Owner",
            "submitter_bl": "PAS",
            "description": "Migrate the trade settlement confirmation flow from synchronous RPC calls "
                           "to an event-driven architecture using Amazon EventBridge. "
                           "Estimated 40% latency reduction. Affects reconciliation pipeline.",
            "arch_type": "New solution",
            "affected_bls": ["PAS", "Ops"],
            "complexity": "High",
            "urgency": "Standard",
            "standard_violation": "No",
            "attachment_path": "",
            "routing_score": 6,
            "routing_tier": "Standard Review",
            "assigned_ea": "Head of EA",
            "status": "Submitted",
            "sla_deadline": (now + timedelta(days=12)).isoformat(),
        },
        {
            "reference": "AR-2025-003",
            "title": "Cross-BL Data Warehouse — Single Pane of Glass",
            "submitter_name": "Marcus Weber",
            "submitter_role": "Solution Architect",
            "submitter_bl": "Cross-BL",
            "description": "Proposal to build a unified data warehouse aggregating data from PWM, PAS, "
                           "and Ops for executive reporting. Uses Snowflake on AWS. "
                           "Raises data residency and cross-BL governance concerns.",
            "arch_type": "New solution",
            "affected_bls": ["PWM", "PAS", "Ops", "PTech"],
            "complexity": "High",
            "urgency": "Urgent",
            "standard_violation": "Suspected",
            "attachment_path": "",
            "routing_score": 10,
            "routing_tier": "SAB Escalation",
            "assigned_ea": "Head of EA",
            "status": "Escalated",
            "sla_deadline": None,
        },
    ]

    for ar in arch_reviews:
        ar["affected_bls"] = json.dumps(ar["affected_bls"])
        existing = conn.execute("SELECT id FROM arch_reviews WHERE reference=?", (ar["reference"],)).fetchone()
        if not existing:
            conn.execute("""
                INSERT INTO arch_reviews
                (reference, title, submitter_name, submitter_role, submitter_bl,
                 description, arch_type, affected_bls, complexity, urgency,
                 standard_violation, attachment_path, routing_score, routing_tier,
                 assigned_ea, status, sla_deadline, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                ar["reference"], ar["title"], ar["submitter_name"], ar["submitter_role"],
                ar["submitter_bl"], ar["description"], ar["arch_type"], ar["affected_bls"],
                ar["complexity"], ar["urgency"], ar["standard_violation"], ar["attachment_path"],
                ar["routing_score"], ar["routing_tier"], ar["assigned_ea"], ar["status"],
                ar["sla_deadline"], datetime.now().isoformat()
            ))

    # ── Sample Exception Requests ─────────────────────────────────────────────
    exceptions = [
        {
            "reference": "EX-2025-001",
            "title": "Temporary Exception: Direct DB Access for Legacy Reporting",
            "submitter_name": "François Dupont",
            "submitter_bl": "Ops",
            "standard_id": "STD-005",
            "justification": "The legacy reporting engine requires direct database access to generate "
                             "regulatory reports. Refactoring to API-based access will take 6 months. "
                             "Requesting temporary exception for Q2 regulatory submission.",
            "duration": "Temporary",
            "end_date": (now + timedelta(days=180)).strftime("%Y-%m-%d"),
            "risk_acknowledged": True,
            "compensating_controls": "Read-only database user; access logging enabled; "
                                      "quarterly review by Risk & Compliance EA.",
            "routing_tier": "Standard Review",
            "assigned_ea": "Sr EA 3 — Ops / Process + Risk & Compliance EA",
            "status": "Under Review",
            "sla_deadline": (now + timedelta(days=10)).isoformat(),
        },
        {
            "reference": "EX-2025-002",
            "title": "Permanent Exception: On-Premise Message Queue for Trading",
            "submitter_name": "Isabella Romano",
            "submitter_bl": "PAS",
            "standard_id": "STD-004",
            "justification": "Ultra-low latency requirements for FX trading cannot be met "
                             "by cloud event bus. Requesting permanent exception to use on-prem "
                             "Solace message broker for trading workflows.",
            "duration": "Permanent",
            "end_date": None,
            "risk_acknowledged": True,
            "compensating_controls": "Solace cluster HA configuration; monitoring via STD-009 tooling; "
                                      "annual architecture review.",
            "routing_tier": "SAB Escalation",
            "assigned_ea": "Sr EA 2 — PAS / Data & Security + Risk & Compliance EA",
            "status": "Submitted",
            "sla_deadline": None,
        },
        {
            "reference": "EX-2025-003",
            "title": "Data Residency Exception: US-based Backup for DR",
            "submitter_name": "Thomas Keller",
            "submitter_bl": "PTech",
            "standard_id": "STD-007",
            "justification": "Disaster recovery scenario requires geographically distributed backups. "
                             "Proposing encrypted backup replication to AWS us-east-1 for DR only. "
                             "No active processing outside Switzerland.",
            "duration": "Permanent",
            "end_date": None,
            "risk_acknowledged": True,
            "compensating_controls": "AES-256 encryption; DPO approval obtained; data classified "
                                      "as non-personal aggregates only; annual DPO review.",
            "routing_tier": "SAB Escalation",
            "assigned_ea": "Cloud Architect EA + Risk & Compliance EA",
            "status": "Draft",
            "sla_deadline": None,
        },
    ]

    for ex in exceptions:
        existing = conn.execute("SELECT id FROM std_exceptions WHERE reference=?", (ex["reference"],)).fetchone()
        if not existing:
            conn.execute("""
                INSERT INTO std_exceptions
                (reference, title, submitter_name, submitter_bl, standard_id,
                 justification, duration, end_date, risk_acknowledged,
                 compensating_controls, routing_tier, assigned_ea, status, sla_deadline, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                ex["reference"], ex["title"], ex["submitter_name"], ex["submitter_bl"],
                ex["standard_id"], ex["justification"], ex["duration"], ex.get("end_date"),
                ex["risk_acknowledged"], ex["compensating_controls"], ex["routing_tier"],
                ex["assigned_ea"], ex["status"], ex.get("sla_deadline"),
                datetime.now().isoformat()
            ))

    # ── Activity log ──────────────────────────────────────────────────────────
    activities = [
        ("Sr EA 1 — PWM / Application", "Started review", "arch_review", "AR-2025-001",
         "Review commenced — assessing API gateway compliance"),
        ("Head of EA", "Routed to SAB", "arch_review", "AR-2025-003",
         "Score 10/12 — escalated to SAB agenda"),
        ("Risk & Compliance EA", "Assigned as co-reviewer", "std_exception", "EX-2025-001",
         "Co-review assigned per exception policy"),
        ("System", "Seed data loaded", "system", "SEED", "Initial demo data loaded"),
    ]
    for actor, action, etype, eref, details in activities:
        conn.execute(
            "INSERT INTO activity_log (actor, action, entity_type, entity_ref, details) VALUES (?,?,?,?,?)",
            (actor, action, etype, eref, details)
        )

    conn.commit()
    conn.close()
    print("Seed data loaded successfully.")


if __name__ == "__main__":
    seed()

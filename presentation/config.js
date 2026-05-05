// ═══════════════════════════════════════════════════════════════
//  config.js — Personnalisez votre rapport ici
//  Modifiez uniquement ce fichier pour adapter la présentation
// ═══════════════════════════════════════════════════════════════

const RAPPORT = {

  // ── Informations générales ────────────────────────────────────
  meta: {
    titre:     "Audit de Sécurité Informatique",
    sousTitre: "Rapport d'Analyse & Recommandations",
    client:    "Entreprise ABC",
    date:      "Mai 2024",
    auditeur:  "Équipe Cybersécurité",
    version:   "v1.0",
  },

  // ── Score global (0 à 100) ────────────────────────────────────
  // niveau : "bon" (≥70) | "moyen" (≥40) | "critique" (<40)
  scoreGlobal: {
    valeur:         68,
    label:          "Score de Maturité",
    interpretation: "Niveau Intermédiaire",
    niveau:         "moyen",
  },

  // ── KPIs (4 recommandés) ──────────────────────────────────────
  kpis: [
    { icone: "🔴", label: "Risques Critiques", valeur: 3  },
    { icone: "🟠", label: "Risques Élevés",    valeur: 7  },
    { icone: "✅", label: "Points Conformes",  valeur: 24 },
    { icone: "📋", label: "Recommandations",   valeur: 15 },
  ],

  // ── Répartition des risques ───────────────────────────────────
  repartition: [
    { niveau: "Critique", count: 3,  couleur: "#ef4444" },
    { niveau: "Élevé",    count: 7,  couleur: "#f97316" },
    { niveau: "Moyen",    count: 11, couleur: "#eab308" },
    { niveau: "Faible",   count: 9,  couleur: "#22c55e" },
    { niveau: "Info",     count: 4,  couleur: "#60a5fa" },
  ],

  // ── Constats ──────────────────────────────────────────────────
  // severite : "critique" | "eleve" | "moyen" | "faible" | "info"
  constats: [
    {
      id:             "C-01",
      severite:       "critique",
      titre:          "Absence d'authentification multi-facteurs",
      description:    "Aucun mécanisme MFA n'est en place sur les accès sensibles (VPN, admin, messagerie).",
      recommandation: "Déployer une solution MFA (TOTP ou clé hardware) sur l'ensemble des accès privilégiés.",
    },
    {
      id:             "C-02",
      severite:       "critique",
      titre:          "Mots de passe administrateurs non renouvelés",
      description:    "Les comptes administrateurs partagent des mots de passe datant de plus de 2 ans.",
      recommandation: "Implémenter une politique de rotation et un gestionnaire de mots de passe.",
    },
    {
      id:             "C-03",
      severite:       "critique",
      titre:          "Sauvegardes non testées",
      description:    "Aucun test de restauration n'a été réalisé depuis 18 mois.",
      recommandation: "Planifier des tests de restauration trimestriels et documenter les procédures.",
    },
    {
      id:             "C-04",
      severite:       "eleve",
      titre:          "Absence de gestion des correctifs",
      description:    "Plusieurs serveurs présentent des vulnérabilités connues faute de mises à jour.",
      recommandation: "Mettre en place un processus de patch management avec suivi mensuel.",
    },
    {
      id:             "C-05",
      severite:       "eleve",
      titre:          "Journalisation insuffisante",
      description:    "Les logs de sécurité sont incomplets et non centralisés.",
      recommandation: "Déployer un SIEM ou une solution de centralisation des logs avec alerting.",
    },
    {
      id:             "C-06",
      severite:       "moyen",
      titre:          "Formation sécurité absente",
      description:    "Aucune sensibilisation à la cybersécurité n'est dispensée aux collaborateurs.",
      recommandation: "Mettre en place un programme annuel de formation et des exercices de phishing simulé.",
    },
  ],

  // ── Recommandations prioritaires ─────────────────────────────
  // priorite : "immediat" | "court" | "moyen"
  recommandations: [
    {
      priorite: "immediat",
      titre:    "Activer le MFA sur tous les accès",
      impact:   "Critique",
      effort:   "Moyen",
      delai:    "< 2 semaines",
    },
    {
      priorite: "immediat",
      titre:    "Renouveler les mots de passe administrateurs",
      impact:   "Critique",
      effort:   "Faible",
      delai:    "< 1 semaine",
    },
    {
      priorite: "court",
      titre:    "Tester et documenter les sauvegardes",
      impact:   "Critique",
      effort:   "Moyen",
      delai:    "1 mois",
    },
    {
      priorite: "court",
      titre:    "Appliquer les correctifs de sécurité",
      impact:   "Élevé",
      effort:   "Moyen",
      delai:    "1 mois",
    },
    {
      priorite: "moyen",
      titre:    "Centraliser les journaux (SIEM)",
      impact:   "Élevé",
      effort:   "Élevé",
      delai:    "3 mois",
    },
    {
      priorite: "moyen",
      titre:    "Former les collaborateurs à la cybersécurité",
      impact:   "Moyen",
      effort:   "Moyen",
      delai:    "3 mois",
    },
  ],

  // ── Feuille de route ──────────────────────────────────────────
  roadmap: [
    {
      phase:   "Phase 1",
      periode: "Mois 1",
      couleur: "#ef4444",
      actions: [
        "Activation MFA tous comptes",
        "Rotation mots de passe admin",
        "Inventaire des accès",
      ],
    },
    {
      phase:   "Phase 2",
      periode: "Mois 2–3",
      couleur: "#f97316",
      actions: [
        "Tests de restauration sauvegardes",
        "Plan de patch management",
        "Audit des droits d'accès",
      ],
    },
    {
      phase:   "Phase 3",
      periode: "Mois 4–6",
      couleur: "#eab308",
      actions: [
        "Déploiement SIEM",
        "Programme de formation",
        "Procédures de réponse aux incidents",
      ],
    },
    {
      phase:   "Phase 4",
      periode: "Mois 7–12",
      couleur: "#22c55e",
      actions: [
        "Audit de suivi",
        "Certification ISO 27001",
        "Amélioration continue",
      ],
    },
  ],

  // ── Conclusion ────────────────────────────────────────────────
  conclusion: {
    message: "Des efforts significatifs sont nécessaires dans l'immédiat pour sécuriser les accès et garantir la continuité d'activité. En suivant la feuille de route proposée, votre organisation atteindra un niveau de maturité satisfaisant d'ici 12 mois.",
    contact: "audit@example.com",
  },
};

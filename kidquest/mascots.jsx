// mascots.jsx — Three original SVG mascots, one per hub
// Owl (English) "Lumi", Turtle (Geo) "Globi", Fox (Math) "Pixel"
//
// Props:
//   size      — display size in px (default 120)
//   mood      — "happy" | "wave" | "wow" | "think"
//   accent    — override main color
//
// Each is drawn around viewBox 0 0 200 200, centered.

const OwlMascot = ({ size = 120, mood = "happy", accent = "#4ECDC4" }) => {
  const eyeRadius = mood === "wow" ? 18 : 14;
  const pupilOffsetY = mood === "wow" ? -2 : 2;
  return (
    <svg viewBox="0 0 200 200" width={size} height={size} className="kq-mascot">
      {/* Branch */}
      <path d="M 30 175 Q 100 165 170 175" stroke="#8B6F47" strokeWidth="6" fill="none" strokeLinecap="round" />
      {/* Body */}
      <ellipse cx="100" cy="120" rx="56" ry="62" fill={accent} stroke="#2A1F1F" strokeWidth="4" />
      {/* Belly */}
      <ellipse cx="100" cy="135" rx="36" ry="42" fill="#FEFCEC" stroke="#2A1F1F" strokeWidth="3" />
      {/* Belly speckles */}
      <ellipse cx="92"  cy="125" rx="3" ry="4" fill="#E0B783" opacity="0.5" />
      <ellipse cx="110" cy="135" rx="3" ry="4" fill="#E0B783" opacity="0.5" />
      <ellipse cx="98"  cy="150" rx="3" ry="4" fill="#E0B783" opacity="0.5" />
      {/* Wings */}
      <path d={mood === "wave"
        ? "M 50 100 Q 30 80 28 60 Q 36 75 50 95 Z"
        : "M 50 110 Q 32 120 38 150 Q 50 130 58 120 Z"}
        fill={accent} stroke="#2A1F1F" strokeWidth="3" />
      <path d="M 150 110 Q 168 120 162 150 Q 150 130 142 120 Z"
            fill={accent} stroke="#2A1F1F" strokeWidth="3" />
      {/* Feet */}
      <path d="M 86 175 L 86 168 M 92 175 L 92 168 M 80 175 L 80 168" stroke="#FFB84D" strokeWidth="3" strokeLinecap="round" />
      <path d="M 114 175 L 114 168 M 120 175 L 120 168 M 108 175 L 108 168" stroke="#FFB84D" strokeWidth="3" strokeLinecap="round" />
      {/* Head tufts (horns) */}
      <path d="M 65 65 L 72 45 L 80 65 Z" fill={accent} stroke="#2A1F1F" strokeWidth="3" />
      <path d="M 135 65 L 128 45 L 120 65 Z" fill={accent} stroke="#2A1F1F" strokeWidth="3" />
      {/* Face base */}
      <circle cx="100" cy="80" r="44" fill={accent} stroke="#2A1F1F" strokeWidth="4" />
      {/* Eye disks */}
      <circle cx="80" cy="80" r={eyeRadius + 6} fill="#FEFCEC" stroke="#2A1F1F" strokeWidth="3" />
      <circle cx="120" cy="80" r={eyeRadius + 6} fill="#FEFCEC" stroke="#2A1F1F" strokeWidth="3" />
      {/* Eyes */}
      <circle cx="80" cy="80" r={eyeRadius} fill="#2A1F1F" />
      <circle cx="120" cy="80" r={eyeRadius} fill="#2A1F1F" />
      {/* Pupils glints */}
      <circle cx={82} cy={78 + pupilOffsetY} r="4" fill="#fff" />
      <circle cx={122} cy={78 + pupilOffsetY} r="4" fill="#fff" />
      {/* Beak */}
      <path d="M 92 96 L 100 108 L 108 96 Z" fill="#FFB84D" stroke="#2A1F1F" strokeWidth="3" />
      {/* Glasses arms — only owl has these (English teacher vibe) */}
      <path d="M 64 80 L 56 78 M 136 80 L 144 78" stroke="#2A1F1F" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
};

const TurtleMascot = ({ size = 120, mood = "happy", accent = "#FF8E53" }) => {
  return (
    <svg viewBox="0 0 200 200" width={size} height={size} className="kq-mascot">
      {/* Ground shadow */}
      <ellipse cx="100" cy="178" rx="68" ry="6" fill="#2A1F1F" opacity="0.12" />
      {/* Back leg */}
      <ellipse cx="148" cy="155" rx="14" ry="10" fill="#56C596" stroke="#2A1F1F" strokeWidth="3" />
      {/* Front leg */}
      <ellipse cx="52" cy="155" rx="16" ry="11" fill="#56C596" stroke="#2A1F1F" strokeWidth="3" />
      {/* Tail */}
      <path d="M 160 145 L 175 142 L 168 152 Z" fill="#56C596" stroke="#2A1F1F" strokeWidth="2.5" />
      {/* Head & neck */}
      <ellipse cx="48" cy="118" rx="22" ry="20" fill="#56C596" stroke="#2A1F1F" strokeWidth="3.5" />
      {/* Cheeks */}
      <ellipse cx="36" cy="124" rx="5" ry="4" fill="#FFB6C1" opacity="0.7" />
      {/* Shell — main dome */}
      <path d="M 50 125 Q 100 60 150 125 Z" fill={accent} stroke="#2A1F1F" strokeWidth="4" />
      <path d="M 50 125 L 150 125" stroke="#2A1F1F" strokeWidth="3" />
      {/* Shell scutes pattern (hexagons) */}
      <g stroke="#2A1F1F" strokeWidth="2.5" fill="#FFD93D">
        <polygon points="100,80 115,90 115,108 100,118 85,108 85,90" />
        <polygon points="74,98 86,108 86,120 74,124 64,118 64,108" />
        <polygon points="126,98 136,108 136,118 126,124 114,120 114,108" />
      </g>
      <path d="M 100 80 L 100 60 M 100 118 L 100 125" stroke="#2A1F1F" strokeWidth="2.5" />
      {/* Eye */}
      <circle cx="40" cy="112" r="6" fill="#FEFCEC" stroke="#2A1F1F" strokeWidth="2.5" />
      <circle cx="40" cy="112" r="3" fill="#2A1F1F" />
      <circle cx="41" cy="111" r="1" fill="#fff" />
      {/* Smile */}
      <path d={mood === "wow" ? "M 32 128 Q 38 134 44 128" : "M 32 128 Q 40 134 48 128"}
            stroke="#2A1F1F" strokeWidth="2.5" fill="none" strokeLinecap="round" />
      {/* Tiny explorer hat */}
      <ellipse cx="48" cy="98" rx="22" ry="4" fill="#8B6F47" stroke="#2A1F1F" strokeWidth="2.5" />
      <path d="M 36 98 Q 48 84 60 98" fill="#A0794F" stroke="#2A1F1F" strokeWidth="2.5" />
      <path d="M 44 96 Q 48 92 52 96" stroke="#FF6B6B" strokeWidth="2.5" fill="none" />
    </svg>
  );
};

const FoxMascot = ({ size = 120, mood = "happy", accent = "#A78BFA" }) => {
  return (
    <svg viewBox="0 0 200 200" width={size} height={size} className="kq-mascot">
      {/* Tail */}
      <path d="M 160 130 Q 188 110 178 80 Q 170 100 158 120 Z" fill={accent} stroke="#2A1F1F" strokeWidth="3.5" />
      <path d="M 178 80 Q 186 85 182 92" fill="#FEFCEC" stroke="#2A1F1F" strokeWidth="2.5" />
      {/* Body */}
      <ellipse cx="100" cy="135" rx="52" ry="44" fill={accent} stroke="#2A1F1F" strokeWidth="4" />
      {/* Belly */}
      <ellipse cx="100" cy="148" rx="32" ry="28" fill="#FEFCEC" stroke="#2A1F1F" strokeWidth="3" />
      {/* Legs */}
      <ellipse cx="74"  cy="172" rx="11" ry="9" fill={accent} stroke="#2A1F1F" strokeWidth="3" />
      <ellipse cx="126" cy="172" rx="11" ry="9" fill={accent} stroke="#2A1F1F" strokeWidth="3" />
      {/* Head */}
      <path d="M 60 90 L 50 50 L 80 70 Z" fill={accent} stroke="#2A1F1F" strokeWidth="3.5" />
      <path d="M 140 90 L 150 50 L 120 70 Z" fill={accent} stroke="#2A1F1F" strokeWidth="3.5" />
      <path d="M 64 56 L 60 70 L 73 60 Z" fill="#FFB6C1" />
      <path d="M 136 56 L 140 70 L 127 60 Z" fill="#FFB6C1" />
      <ellipse cx="100" cy="92" rx="44" ry="38" fill={accent} stroke="#2A1F1F" strokeWidth="4" />
      {/* Face mask */}
      <ellipse cx="100" cy="100" rx="28" ry="22" fill="#FEFCEC" stroke="#2A1F1F" strokeWidth="3" />
      {/* Eyes */}
      <ellipse cx="86" cy="92" rx={mood === "wow" ? 6 : 4} ry={mood === "wow" ? 6 : 5} fill="#2A1F1F" />
      <ellipse cx="114" cy="92" rx={mood === "wow" ? 6 : 4} ry={mood === "wow" ? 6 : 5} fill="#2A1F1F" />
      <circle cx="87" cy="90" r="1.5" fill="#fff" />
      <circle cx="115" cy="90" r="1.5" fill="#fff" />
      {/* Nose */}
      <path d="M 94 104 L 106 104 L 100 112 Z" fill="#2A1F1F" />
      {/* Smile */}
      <path d={mood === "wow"
        ? "M 92 116 Q 100 122 108 116"
        : "M 92 114 Q 100 122 108 114"}
        stroke="#2A1F1F" strokeWidth="2.5" fill="#FF99B6" />
      {/* Math accessory: tiny calculator hint or glasses */}
      <rect x="78" y="72" width="44" height="14" rx="6" fill="none" stroke="#2A1F1F" strokeWidth="2" opacity="0.4" />
    </svg>
  );
};

// Pick mascot for a hub
const HubMascot = ({ hubId, ...rest }) => {
  if (hubId === "english") return <OwlMascot {...rest} />;
  if (hubId === "geo") return <TurtleMascot {...rest} />;
  return <FoxMascot {...rest} />;
};

window.OwlMascot = OwlMascot;
window.TurtleMascot = TurtleMascot;
window.FoxMascot = FoxMascot;
window.HubMascot = HubMascot;

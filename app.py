import streamlit as st
from constraint import Problem, AllDifferentConstraint

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Parking CSP Solver",
    page_icon="🚗",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0f1117; color: #e8e8e8; }
#MainMenu, footer, header { visibility: hidden; }

.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #1e3a5f; border-radius: 16px;
    padding: 2rem 2rem 1.6rem; margin-bottom: 1.8rem;
    text-align: center; position: relative; overflow: hidden;
}
.hero h1 { font-size: 2rem; font-weight: 700; color: #fff; margin: 0 0 0.4rem; }
.hero p  { color: #8b9ab3; font-size: 0.9rem; margin: 0; }
.hero-badge {
    display: inline-block; background: rgba(56,139,253,0.15);
    border: 1px solid rgba(56,139,253,0.4); color: #79b8ff;
    font-size: 0.7rem; font-weight: 600; padding: 3px 12px;
    border-radius: 999px; margin-bottom: 0.8rem; letter-spacing: 1px; text-transform: uppercase;
}
.section-card {
    background: #161b27; border: 1px solid #1e2d45;
    border-radius: 14px; padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.section-title {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #4a7fb5; margin-bottom: 0.8rem;
}
.slot-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin: 0.4rem 0; }
.slot-box  { border-radius: 10px; padding: 10px 12px; border: 1px solid; font-family: 'JetBrains Mono',monospace; }
.slot-large    { background: rgba(186,117,23,0.12); border-color: rgba(186,117,23,0.4); }
.slot-regular  { background: rgba(56,139,253,0.08); border-color: rgba(56,139,253,0.25); }
.slot-bikeonly { background: rgba(46,160,67,0.10);  border-color: rgba(46,160,67,0.35); }
.slot-id   { font-size: 1rem; font-weight: 700; }
.slot-type { font-size: 0.65rem; margin-top: 2px; opacity: 0.7; }
.slot-large .slot-id    { color: #e3b341; }
.slot-large .slot-type  { color: #b08020; }
.slot-regular .slot-id  { color: #79b8ff; }
.slot-regular .slot-type{ color: #4a7fb5; }
.slot-bikeonly .slot-id { color: #56d364; }
.slot-bikeonly .slot-type{ color: #2ea043; }

.vehicle-pills { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.4rem; }
.pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 12px; border-radius: 999px; font-size: 0.75rem;
    font-weight: 600; font-family: 'JetBrains Mono',monospace; border: 1px solid;
}
.pill-car     { background: rgba(56,139,253,0.12);  border-color: rgba(56,139,253,0.4);  color: #79b8ff; }
.pill-bike    { background: rgba(46,160,67,0.12);   border-color: rgba(46,160,67,0.4);   color: #56d364; }
.pill-truck   { background: rgba(186,117,23,0.15);  border-color: rgba(186,117,23,0.4);  color: #e3b341; }
.pill-tractor { background: rgba(139,92,246,0.12);  border-color: rgba(139,92,246,0.4);  color: #c084fc; }
.pill-van     { background: rgba(236,72,153,0.12);  border-color: rgba(236,72,153,0.4);  color: #f472b6; }
.pill-scooter { background: rgba(20,184,166,0.12);  border-color: rgba(20,184,166,0.4);  color: #2dd4bf; }
.pill-bus     { background: rgba(249,115,22,0.12);  border-color: rgba(249,115,22,0.4);  color: #fb923c; }
.pill-other   { background: rgba(100,116,139,0.12); border-color: rgba(100,116,139,0.4); color: #94a3b8; }

.constraint-list { list-style: none; padding: 0; margin: 0; }
.constraint-list li {
    padding: 7px 0; border-bottom: 1px solid #1e2d45;
    font-size: 0.82rem; color: #8b9ab3; display: flex; align-items: flex-start; gap: 9px;
}
.constraint-list li:last-child { border-bottom: none; }
.c-dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }

.sol-header {
    display: flex; justify-content: space-between; align-items: center;
    background: #1a2332; border: 1px solid #1e3a5f;
    border-radius: 10px 10px 0 0; padding: 8px 14px;
    font-size: 0.75rem; font-weight: 600; color: #79b8ff; font-family: 'JetBrains Mono',monospace;
}
.sol-body {
    background: #11161f; border: 1px solid #1e2d45; border-top: none;
    border-radius: 0 0 10px 10px; padding: 10px 14px; margin-bottom: 10px;
}
.sol-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 4px 0; border-bottom: 1px solid #1a2332;
    font-size: 0.82rem; font-family: 'JetBrains Mono',monospace;
}
.sol-row:last-child { border-bottom: none; }
.sol-slot    { color: #4a7fb5; font-weight: 600; min-width: 30px; }
.sol-arrow   { color: #30363d; }
.sol-veh     { font-weight: 600; flex: 1; text-align: center; }
.sol-car     { color: #79b8ff; }
.sol-bike    { color: #56d364; }
.sol-truck   { color: #e3b341; }
.sol-tractor { color: #c084fc; }
.sol-van     { color: #f472b6; }
.sol-scooter { color: #2dd4bf; }
.sol-bus     { color: #fb923c; }
.sol-empty   { color: #3d4450; font-style: italic; }

.stats-bar { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 1.2rem; }
.stat-box  { background: #161b27; border: 1px solid #1e2d45; border-radius: 10px; padding: 0.9rem; text-align: center; }
.stat-num  { font-size: 1.6rem; font-weight: 700; font-family: 'JetBrains Mono',monospace; color: #79b8ff; }
.stat-label{ font-size: 0.68rem; color: #4a7fb5; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

.stButton > button {
    background: linear-gradient(135deg,#1a4a8a,#0f3460) !important;
    color: #fff !important; border: 1px solid #2563b0 !important;
    border-radius: 10px !important; font-family: 'Space Grotesk',sans-serif !important;
    font-weight: 600 !important; font-size: 0.9rem !important;
    width: 100% !important; transition: all 0.2s !important;
}
.stButton > button:hover { background: linear-gradient(135deg,#2563b0,#1a4a8a) !important; border-color: #388bfd !important; }

.solutions-scroll { max-height: 560px; overflow-y: auto; padding-right: 4px; }
.solutions-scroll::-webkit-scrollbar { width: 4px; }
.solutions-scroll::-webkit-scrollbar-track { background: #0f1117; }
.solutions-scroll::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 4px; }

.add-form { background: #111827; border: 1px solid #1e3a5f; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 1rem; }
.add-form-title { font-size: 0.65rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #388bfd; margin-bottom: 0.8rem; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   SLOT & VEHICLE TYPE CONFIG
# ══════════════════════════════════════════════════════════════

ALL_SLOTS   = ["S1", "S2", "S3", "S4", "S5", "S6"]
LARGE_SLOTS = ["S1", "S2"]
CAR_SLOTS   = ["S1", "S2", "S3", "S4"]
BIKE_SLOTS  = ALL_SLOTS

SLOT_META = {
    "S1": ("Large",     "slot-large"),
    "S2": ("Large",     "slot-large"),
    "S3": ("Regular",   "slot-regular"),
    "S4": ("Regular",   "slot-regular"),
    "S5": ("Bike-only", "slot-bikeonly"),
    "S6": ("Bike-only", "slot-bikeonly"),
}

# emoji, allowed_slots, pill_css_class, solution_css_class
TYPE_CONFIG = {
    "Car":     ("🚗", CAR_SLOTS,   "pill-car",     "sol-car"),
    "Bike":    ("🏍️", BIKE_SLOTS,  "pill-bike",    "sol-bike"),
    "Truck":   ("🚛", LARGE_SLOTS, "pill-truck",   "sol-truck"),
    "Tractor": ("🚜", LARGE_SLOTS, "pill-tractor", "sol-tractor"),
    "Van":     ("🚐", CAR_SLOTS,   "pill-van",     "sol-van"),
    "Scooter": ("🛵", BIKE_SLOTS,  "pill-scooter", "sol-scooter"),
    "Bus":     ("🚌", LARGE_SLOTS, "pill-bus",     "sol-bus"),
    "Other":   ("🚙", CAR_SLOTS,   "pill-other",   "sol-car"),
}


# ══════════════════════════════════════════════════════════════
#   SESSION STATE
# ══════════════════════════════════════════════════════════════

if "vehicles" not in st.session_state:
    st.session_state.vehicles = [
        {"name": "Car1",   "type": "Car"},
        {"name": "Car2",   "type": "Car"},
        {"name": "Car3",   "type": "Car"},
        {"name": "Bike1",  "type": "Bike"},
        {"name": "Bike2",  "type": "Bike"},
        {"name": "Truck1", "type": "Truck"},
    ]


# ══════════════════════════════════════════════════════════════
#   CSP SOLVER
# ══════════════════════════════════════════════════════════════

def solve_parking_csp(vehicle_list):
    if not vehicle_list:
        return []
    names = [v["name"] for v in vehicle_list]
    if len(names) > len(ALL_SLOTS):
        return []
    problem = Problem()
    for v in vehicle_list:
        allowed = TYPE_CONFIG[v["type"]][1]
        problem.addVariable(v["name"], allowed)
    problem.addConstraint(AllDifferentConstraint(), names)
    return problem.getSolutions()


# ══════════════════════════════════════════════════════════════
#   HERO
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <div class="hero-badge">CSP · Constraint Satisfaction Problem</div>
  <h1>🚗 Vehicle Parking Allocator</h1>
  <p>Manually vehicles add karo aur CSP se sare valid parking assignments dhundo</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   TWO-COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════

left, right = st.columns([1, 1.6], gap="large")

# ────────────────────────────────────────────────────────────
# LEFT COLUMN
# ────────────────────────────────────────────────────────────
with left:

    # Slot legend
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Parking Slots</div>', unsafe_allow_html=True)
    s_html = '<div class="slot-grid">'
    for sid in ALL_SLOTS:
        lbl, cls = SLOT_META[sid]
        s_html += f'<div class="slot-box {cls}"><div class="slot-id">{sid}</div><div class="slot-type">{lbl}</div></div>'
    s_html += '</div>'
    st.markdown(s_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Add vehicle form
    st.markdown('<div class="add-form">', unsafe_allow_html=True)
    st.markdown('<div class="add-form-title">➕ Vehicle Add Karo</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        v_name = st.text_input("Naam", placeholder="e.g. Car4, MyBike…", label_visibility="collapsed")
    with c2:
        v_type = st.selectbox("Qisam chunein", list(TYPE_CONFIG.keys()), label_visibility="collapsed")

    if st.button("➕  Add Vehicle"):
        name = v_name.strip()
        if not name:
            st.error("Naam khali nahi ho sakta.")
        elif any(v["name"].lower() == name.lower() for v in st.session_state.vehicles):
            st.error(f'"{name}" pehle se list mein hai.')
        elif len(st.session_state.vehicles) >= len(ALL_SLOTS):
            st.error(f"Maximum {len(ALL_SLOTS)} vehicles allowed.")
        else:
            st.session_state.vehicles.append({"name": name, "type": v_type})
            st.session_state.pop("solutions", None)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Vehicle list + remove
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Current Vehicles</div>', unsafe_allow_html=True)

    if not st.session_state.vehicles:
        st.markdown('<p style="color:#3d4450;font-size:0.85rem;">Koi vehicle nahi — upar se add karo</p>', unsafe_allow_html=True)
    else:
        p_html = '<div class="vehicle-pills">'
        for v in st.session_state.vehicles:
            emoji, _, pcls, _ = TYPE_CONFIG[v["type"]]
            p_html += f'<span class="pill {pcls}">{emoji} {v["name"]}</span>'
        p_html += '</div>'
        st.markdown(p_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        remove_name = st.selectbox(
            "Vehicle hatao",
            ["— Select —"] + [v["name"] for v in st.session_state.vehicles]
        )
        if st.button("🗑️  Remove Selected"):
            if remove_name != "— Select —":
                st.session_state.vehicles = [v for v in st.session_state.vehicles if v["name"] != remove_name]
                st.session_state.pop("solutions", None)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Constraints reference
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Constraints</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="constraint-list">
      <li><span class="c-dot" style="background:#79b8ff"></span>Ek slot par sirf ek vehicle park ho sakti hai</li>
      <li><span class="c-dot" style="background:#56d364"></span>Bike / Scooter → koi bhi slot (S1–S6)</li>
      <li><span class="c-dot" style="background:#79b8ff"></span>Car / Van / Other → S1–S4 only</li>
      <li><span class="c-dot" style="background:#e3b341"></span>Truck / Tractor / Bus → sirf S1–S2 (Large)</li>
      <li><span class="c-dot" style="background:#f78166"></span>Har vehicle ko alag unique slot milna chahiye</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_r, col_s = st.columns(2)
    with col_r:
        if st.button("🔄 Reset All"):
            st.session_state.vehicles = []
            st.session_state.pop("solutions", None)
            st.rerun()
    with col_s:
        solve_clicked = st.button("⚡ Solve CSP")


# ────────────────────────────────────────────────────────────
# RIGHT COLUMN
# ────────────────────────────────────────────────────────────
with right:

    if solve_clicked:
        if not st.session_state.vehicles:
            st.warning("Pehle koi vehicle add karo.")
        else:
            with st.spinner("CSP solve ho raha hai..."):
                solutions = solve_parking_csp(st.session_state.vehicles)
                st.session_state["solutions"] = solutions
                st.session_state["solved_vehicles"] = list(st.session_state.vehicles)

    if "solutions" in st.session_state:
        solutions    = st.session_state["solutions"]
        solved_veh   = st.session_state.get("solved_vehicles", st.session_state.vehicles)
        type_map     = {v["name"]: v["type"] for v in solved_veh}
        total        = len(solutions)

        st.markdown(f"""
        <div class="stats-bar">
          <div class="stat-box"><div class="stat-num">{total}</div><div class="stat-label">Valid Solutions</div></div>
          <div class="stat-box"><div class="stat-num">{len(solved_veh)}</div><div class="stat-label">Vehicles</div></div>
          <div class="stat-box"><div class="stat-num">{len(ALL_SLOTS)}</div><div class="stat-label">Total Slots</div></div>
        </div>
        """, unsafe_allow_html=True)

        if total == 0:
            st.markdown("""
            <div style="background:#1f1215;border:1px solid #4a1e1e;border-radius:12px;padding:2rem;text-align:center;margin-top:1rem;">
              <div style="font-size:2rem;margin-bottom:0.5rem;">❌</div>
              <div style="color:#f87171;font-weight:600;">Koi valid solution nahi mila</div>
              <div style="color:#6b3a3a;font-size:0.82rem;margin-top:0.4rem;">
                Vehicles zyada hain ya slots se match nahi karta — list check karo
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            fa, fb = st.columns(2)
            with fa:
                search = st.text_input("🔍 Filter", placeholder="vehicle ya slot naam…")
            with fb:
                show_n = st.slider("Solutions dikhao", 1, min(total, 100), min(10, total))

            filtered = [
                s for s in solutions
                if not search or any(
                    search.lower() in k.lower() or search.lower() in str(v).lower()
                    for k, v in s.items()
                )
            ][:show_n]

            if not filtered:
                st.warning("Is filter ke sath koi result nahi.")
            else:
                st.markdown(f'<div class="section-title">{len(filtered)} solutions dikh rahe hain</div>', unsafe_allow_html=True)

                html = '<div class="solutions-scroll">'
                for idx, sol in enumerate(filtered, 1):
                    slot_to_veh = {v: k for k, v in sol.items()}
                    html += f'<div class="sol-header"><span>Solution #{idx}</span><span style="color:#4a7fb5;font-size:0.7rem;">{len(sol)} placements</span></div>'
                    html += '<div class="sol-body">'
                    for sid in ALL_SLOTS:
                        veh   = slot_to_veh.get(sid, "")
                        vtype = type_map.get(veh, "").lower()
                        vcls  = f"sol-{vtype}" if vtype else "sol-empty"
                        emoji = TYPE_CONFIG.get(type_map.get(veh, ""), ("",))[0] if veh else ""
                        lbl, _ = SLOT_META[sid]
                        disp  = f"{emoji} {veh}" if veh else "— khali —"
                        html += f"""<div class="sol-row">
                          <span class="sol-slot">{sid}</span>
                          <span class="sol-arrow"> ──▶ </span>
                          <span class="sol-veh {vcls}">{disp}</span>
                          <span style="font-size:0.68rem;color:#30363d;">{lbl}</span>
                        </div>"""
                    html += '</div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#161b27;border:1px dashed #1e3a5f;border-radius:14px;
                    padding:4rem 2rem;text-align:center;margin-top:1rem;">
          <div style="font-size:2.5rem;margin-bottom:1rem;">⚡</div>
          <div style="color:#4a7fb5;font-size:1rem;font-weight:600;">Vehicles add karo, phir "Solve CSP" dabao</div>
          <div style="color:#30363d;font-size:0.82rem;margin-top:0.5rem;">Sare valid parking assignments yahan dikhenge</div>
        </div>
        """, unsafe_allow_html=True)

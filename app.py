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

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0f1117;
    color: #e8e8e8;
}

/* ── Hide default streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 70% 30%, rgba(56,139,253,0.08) 0%, transparent 60%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.5rem;
    letter-spacing: -0.5px;
}
.hero p {
    color: #8b9ab3;
    font-size: 1rem;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(56,139,253,0.15);
    border: 1px solid rgba(56,139,253,0.4);
    color: #79b8ff;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 1rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Section cards ── */
.section-card {
    background: #161b27;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a7fb5;
    margin-bottom: 1rem;
}

/* ── Slot grid ── */
.slot-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 0.5rem 0;
}
.slot-box {
    border-radius: 10px;
    padding: 12px 14px;
    border: 1px solid;
    font-family: 'JetBrains Mono', monospace;
}
.slot-large    { background: rgba(186,117,23,0.12); border-color: rgba(186,117,23,0.4); }
.slot-regular  { background: rgba(56,139,253,0.08); border-color: rgba(56,139,253,0.25); }
.slot-bikeonly { background: rgba(46,160,67,0.1);  border-color: rgba(46,160,67,0.35); }
.slot-id   { font-size: 1.1rem; font-weight: 700; }
.slot-type { font-size: 0.7rem; margin-top: 2px; opacity: 0.7; }
.slot-large .slot-id    { color: #e3b341; }
.slot-large .slot-type  { color: #b08020; }
.slot-regular .slot-id  { color: #79b8ff; }
.slot-regular .slot-type{ color: #4a7fb5; }
.slot-bikeonly .slot-id { color: #56d364; }
.slot-bikeonly .slot-type{color: #2ea043; }

/* ── Vehicle pills ── */
.vehicle-pills { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.5rem; }
.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    border: 1px solid;
}
.pill-car   { background: rgba(56,139,253,0.12); border-color: rgba(56,139,253,0.4); color: #79b8ff; }
.pill-bike  { background: rgba(46,160,67,0.12);  border-color: rgba(46,160,67,0.4);  color: #56d364; }
.pill-truck { background: rgba(186,117,23,0.15); border-color: rgba(186,117,23,0.4); color: #e3b341; }

/* ── Constraint chips ── */
.constraint-list { list-style: none; padding: 0; margin: 0; }
.constraint-list li {
    padding: 8px 0;
    border-bottom: 1px solid #1e2d45;
    font-size: 0.88rem;
    color: #8b9ab3;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
.constraint-list li:last-child { border-bottom: none; }
.c-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}

/* ── Solution cards ── */
.sol-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1a2332;
    border: 1px solid #1e3a5f;
    border-radius: 10px 10px 0 0;
    padding: 10px 16px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #79b8ff;
    font-family: 'JetBrains Mono', monospace;
}
.sol-body {
    background: #11161f;
    border: 1px solid #1e2d45;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 12px 16px;
    margin-bottom: 12px;
}
.sol-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid #1a2332;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
}
.sol-row:last-child { border-bottom: none; }
.sol-slot  { color: #4a7fb5; font-weight: 600; }
.sol-arrow { color: #30363d; }
.sol-veh   { font-weight: 600; }
.sol-veh-car   { color: #79b8ff; }
.sol-veh-bike  { color: #56d364; }
.sol-veh-truck { color: #e3b341; }
.sol-veh-empty { color: #3d4450; font-style: italic; }

/* ── Stats bar ── */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 1.5rem;
}
.stat-box {
    background: #161b27;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.stat-num {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #79b8ff;
}
.stat-label {
    font-size: 0.72rem;
    color: #4a7fb5;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Solve button ── */
.stButton > button {
    background: linear-gradient(135deg, #1a4a8a, #0f3460) !important;
    color: #ffffff !important;
    border: 1px solid #2563b0 !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563b0, #1a4a8a) !important;
    border-color: #388bfd !important;
    transform: translateY(-1px) !important;
}

/* ── Scrollable solutions area ── */
.solutions-scroll {
    max-height: 520px;
    overflow-y: auto;
    padding-right: 4px;
}
.solutions-scroll::-webkit-scrollbar { width: 4px; }
.solutions-scroll::-webkit-scrollbar-track { background: #0f1117; }
.solutions-scroll::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   CSP SOLVER
# ══════════════════════════════════════════════════════════════

def solve_parking_csp(vehicles, slots, car_slots, large_slots, bike_slots):
    """
    Build and solve the CSP.
    Returns a list of solution dicts: { vehicle: slot }
    """
    problem = Problem()

    # Define variables and their domains
    cars   = [v for v in vehicles if v.startswith("Car")]
    bikes  = [v for v in vehicles if v.startswith("Bike")]
    trucks = [v for v in vehicles if v.startswith("Truck")]

    for c in cars:
        problem.addVariable(c, car_slots)    # Cars: no bike-only slots

    for b in bikes:
        problem.addVariable(b, bike_slots)   # Bikes: any slot

    for t in trucks:
        problem.addVariable(t, large_slots)  # Trucks: large slots only

    # No two vehicles can share the same slot
    problem.addConstraint(AllDifferentConstraint(), vehicles)

    return problem.getSolutions()


# ══════════════════════════════════════════════════════════════
#   DATA
# ══════════════════════════════════════════════════════════════

ALL_SLOTS    = ["S1", "S2", "S3", "S4", "S5", "S6"]
LARGE_SLOTS  = ["S1", "S2"]
CAR_SLOTS    = ["S1", "S2", "S3", "S4"]
BIKE_SLOTS   = ALL_SLOTS
VEHICLES     = ["Car1", "Car2", "Car3", "Bike1", "Bike2", "Truck1"]

SLOT_META = {
    "S1": ("Large",     "slot-large"),
    "S2": ("Large",     "slot-large"),
    "S3": ("Regular",   "slot-regular"),
    "S4": ("Regular",   "slot-regular"),
    "S5": ("Bike-only", "slot-bikeonly"),
    "S6": ("Bike-only", "slot-bikeonly"),
}


# ══════════════════════════════════════════════════════════════
#   HERO
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <div class="hero-badge">CSP · Constraint Satisfaction Problem</div>
  <h1>🚗 Vehicle Parking Allocator</h1>
  <p>Automatically find all valid parking assignments using python-constraint</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   LEFT / RIGHT COLUMNS
# ══════════════════════════════════════════════════════════════

left, right = st.columns([1, 1.6], gap="large")

# ── LEFT: Problem Definition ──────────────────────────────────
with left:

    # Parking Slots
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Parking Slots</div>', unsafe_allow_html=True)
    slots_html = '<div class="slot-grid">'
    for sid in ALL_SLOTS:
        label, cls = SLOT_META[sid]
        slots_html += f"""
        <div class="slot-box {cls}">
            <div class="slot-id">{sid}</div>
            <div class="slot-type">{label}</div>
        </div>"""
    slots_html += '</div>'
    st.markdown(slots_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Vehicles
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Vehicles</div>', unsafe_allow_html=True)
    pills_html = '<div class="vehicle-pills">'
    for v in VEHICLES:
        if v.startswith("Car"):
            pills_html += f'<span class="pill pill-car">🚗 {v}</span>'
        elif v.startswith("Bike"):
            pills_html += f'<span class="pill pill-bike">🏍️ {v}</span>'
        else:
            pills_html += f'<span class="pill pill-truck">🚛 {v}</span>'
    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Constraints
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Constraints</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="constraint-list">
      <li><span class="c-dot" style="background:#79b8ff"></span>One vehicle per slot — no double parking</li>
      <li><span class="c-dot" style="background:#56d364"></span>Bikes can park in any slot (S1–S6)</li>
      <li><span class="c-dot" style="background:#79b8ff"></span>Cars cannot use bike-only slots (S5, S6)</li>
      <li><span class="c-dot" style="background:#e3b341"></span>Truck can only use large slots (S1, S2)</li>
      <li><span class="c-dot" style="background:#f78166"></span>All vehicles must get a unique slot</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Solve button
    solve_clicked = st.button("⚡  Solve — Find All Valid Assignments")


# ── RIGHT: Solutions ──────────────────────────────────────────
with right:

    if solve_clicked or "solutions" in st.session_state:

        if solve_clicked:
            with st.spinner("Solving CSP..."):
                solutions = solve_parking_csp(
                    VEHICLES, ALL_SLOTS, CAR_SLOTS, LARGE_SLOTS, BIKE_SLOTS
                )
                st.session_state["solutions"] = solutions
        else:
            solutions = st.session_state["solutions"]

        total = len(solutions)

        # Stats bar
        trucks_in = sum(1 for s in solutions if s.get("Truck1") in LARGE_SLOTS)
        st.markdown(f"""
        <div class="stats-bar">
          <div class="stat-box">
            <div class="stat-num">{total}</div>
            <div class="stat-label">Valid Solutions</div>
          </div>
          <div class="stat-box">
            <div class="stat-num">{len(VEHICLES)}</div>
            <div class="stat-label">Vehicles Placed</div>
          </div>
          <div class="stat-box">
            <div class="stat-num">{len(ALL_SLOTS)}</div>
            <div class="stat-label">Total Slots</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Filter / sort controls
        col_a, col_b = st.columns(2)
        with col_a:
            search = st.text_input("🔍 Filter by vehicle or slot", placeholder="e.g. Truck1 or S1")
        with col_b:
            show_n = st.slider("Solutions to display", 1, min(total, 100), min(10, total))

        # Apply filter
        filtered = []
        for sol in solutions:
            if search:
                match = any(
                    search.upper() in k.upper() or search.upper() in v.upper()
                    for k, v in sol.items()
                )
                if match:
                    filtered.append(sol)
            else:
                filtered.append(sol)

        filtered = filtered[:show_n]

        if not filtered:
            st.warning("Koi solution nahi mila is filter ke sath.")
        else:
            st.markdown(f'<div class="section-title" style="margin-top:0.5rem;">{len(filtered)} Solutions shown</div>', unsafe_allow_html=True)

            scroll_html = '<div class="solutions-scroll">'
            for idx, sol in enumerate(filtered, 1):
                slot_to_veh = {v: k for k, v in sol.items()}
                scroll_html += f'<div class="sol-header"><span>Solution #{idx}</span><span style="color:#4a7fb5;font-size:0.72rem;">{len(sol)} assignments</span></div>'
                scroll_html += '<div class="sol-body">'
                for sid in ALL_SLOTS:
                    veh = slot_to_veh.get(sid, "")
                    if veh.startswith("Car"):
                        vcls = "sol-veh-car"
                    elif veh.startswith("Bike"):
                        vcls = "sol-veh-bike"
                    elif veh.startswith("Truck"):
                        vcls = "sol-veh-truck"
                    else:
                        vcls = "sol-veh-empty"
                    label, _ = SLOT_META[sid]
                    disp = veh if veh else "empty"
                    scroll_html += f"""
                    <div class="sol-row">
                      <span class="sol-slot">{sid}</span>
                      <span class="sol-arrow">──▶</span>
                      <span class="sol-veh {vcls}">{disp}</span>
                      <span style="font-size:0.7rem;color:#30363d;">{label}</span>
                    </div>"""
                scroll_html += '</div>'
            scroll_html += '</div>'
            st.markdown(scroll_html, unsafe_allow_html=True)

    else:
        # Placeholder before solving
        st.markdown("""
        <div style="background:#161b27; border:1px dashed #1e3a5f; border-radius:14px;
                    padding:3rem 2rem; text-align:center; margin-top:1rem;">
          <div style="font-size:2.5rem; margin-bottom:1rem;">⚡</div>
          <div style="color:#4a7fb5; font-size:1rem; font-weight:600;">"Solve" button dabao</div>
          <div style="color:#30363d; font-size:0.85rem; margin-top:0.5rem;">
            Sare valid parking assignments yahan dikhenge
          </div>
        </div>
        """, unsafe_allow_html=True)

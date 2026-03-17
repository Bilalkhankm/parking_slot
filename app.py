# ============================================================
#   Vehicle Parking Allocator — Interactive (Google Colab)
#   Uses ipywidgets for a live UI inside the notebook
# ============================================================

# ── Step 1: Install required library ────────────────────────
!pip install ipywidgets --quiet

# ── Step 2: Imports ─────────────────────────────────────────
import ipywidgets as widgets
from IPython.display import display, clear_output

# ── Step 3: Define parking slots and their rules ────────────
# Each slot has:
#   label   : human-readable type name
#   allows  : which vehicle types can use this slot
SLOTS = {
    "S1": {"label": "Large",     "allows": ["car", "bike", "truck"]},
    "S2": {"label": "Large",     "allows": ["car", "bike", "truck"]},
    "S3": {"label": "Regular",   "allows": ["car", "bike"]},
    "S4": {"label": "Regular",   "allows": ["car", "bike"]},
    "S5": {"label": "Bike-only", "allows": ["bike"]},
    "S6": {"label": "Bike-only", "allows": ["bike"]},
}

# occupied dict  →  { "S1": "Car1", "S3": "Bike2", ... }
occupied = {}

# ── Step 4: Helper — print the current parking lot status ───
def print_status():
    print("=" * 45)
    print(f"{'SLOT':<6} {'TYPE':<12} {'VEHICLE'}")
    print("-" * 45)
    for slot_id, info in SLOTS.items():
        vehicle = occupied.get(slot_id, "— Khali —")
        print(f"{slot_id:<6} {info['label']:<12} {vehicle}")
    print("=" * 45)

# ── Step 5: Core allocation logic ───────────────────────────
def suggest_slot(vehicle_name, vehicle_type):
    """
    Finds the first available slot for the given vehicle type,
    assigns it, and returns a result message.
    """
    vehicle_name = vehicle_name.strip()

    # Validation checks
    if not vehicle_name:
        return ("error", "Vehicle ka naam khali nahi ho sakta.")
    if vehicle_type == "-- Select --":
        return ("error", "Pehle vehicle ki qisam chunein.")
    if vehicle_name in occupied.values():
        return ("error", f'"{vehicle_name}" pehle se park hai.')

    vehicle_type_lower = vehicle_type.lower()

    # Find all eligible empty slots
    eligible = [
        sid for sid, info in SLOTS.items()
        if vehicle_type_lower in info["allows"] and sid not in occupied
    ]

    if not eligible:
        return ("error",
                f'Koi available slot nahi hai "{vehicle_name}" ({vehicle_type}) ke liye.')

    # Assign to the first eligible slot
    best_slot = eligible[0]
    occupied[best_slot] = vehicle_name
    return ("success",
            f'"{vehicle_name}" ({vehicle_type}) → {best_slot} ({SLOTS[best_slot]["label"]}) ✔')

# ── Step 6: Build the UI widgets ────────────────────────────

title = widgets.HTML(
    value="<h3 style='margin-bottom:8px;'>🚗 Vehicle Parking Allocator</h3>"
)

name_input = widgets.Text(
    placeholder="e.g. Car4, Bike3, Truck2",
    description="Naam:",
    layout=widgets.Layout(width="280px"),
)

type_dropdown = widgets.Dropdown(
    options=["-- Select --", "Car", "Bike", "Truck"],
    description="Qisam:",
    layout=widgets.Layout(width="200px"),
)

add_btn   = widgets.Button(description="Slot Suggest Karo",
                            button_style="primary",
                            layout=widgets.Layout(width="160px"))
reset_btn = widgets.Button(description="Reset",
                            button_style="warning",
                            layout=widgets.Layout(width="100px"))

msg_out    = widgets.Output()   # shows success / error message
status_out = widgets.Output()   # shows the parking lot table

# ── Step 7: Render the parking lot table ────────────────────
def render_status():
    with status_out:
        clear_output(wait=True)
        print_status()

# ── Step 8: Button click handlers ───────────────────────────
def on_add_clicked(_):
    result_type, message = suggest_slot(name_input.value, type_dropdown.value)
    with msg_out:
        clear_output(wait=True)
        if result_type == "success":
            print(f"✅  {message}")
        else:
            print(f"❌  {message}")
    # Clear inputs after successful add
    if result_type == "success":
        name_input.value = ""
        type_dropdown.value = "-- Select --"
    render_status()

def on_reset_clicked(_):
    occupied.clear()
    name_input.value = ""
    type_dropdown.value = "-- Select --"
    with msg_out:
        clear_output(wait=True)
        print("🔄  Parking slot reset ho gaya.")
    render_status()

add_btn.on_click(on_add_clicked)
reset_btn.on_click(on_reset_clicked)

# ── Step 9: Assemble and display the full UI ────────────────
form_row    = widgets.HBox([name_input, type_dropdown, add_btn, reset_btn],
                            layout=widgets.Layout(gap="12px", align_items="center"))
legend_html = widgets.HTML("""
<small>
  <b>Legend:</b>
  &nbsp;🟠 S1–S2 = Large (Car/Bike/Truck)
  &nbsp;⬜ S3–S4 = Regular (Car/Bike)
  &nbsp;🟢 S5–S6 = Bike-only
</small>
""")

ui = widgets.VBox(
    [title, form_row, legend_html, msg_out, status_out],
    layout=widgets.Layout(padding="12px", gap="8px"),
)

display(ui)
render_status()   # show initial empty lot
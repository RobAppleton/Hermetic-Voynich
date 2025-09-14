#!/usr/bin/env python3
"""
translate.py

Reads operator-sequence JSON and pictorial counts produced by decode_f1r_runner.py,
then emits a plain-English translation in a 12-step allegorical frame (and optionally
a 7-step frame if the decision says so). The prose is assembled from templates and
lightly tailored by observed counts and operator histograms.

Inputs (defaults):
  - /mnt/data/f1r_operator_sequence.json
  - /mnt/data/pictorial_counts_f1r_template.csv
  - /mnt/data/f1r_decision_note.txt

Outputs:
  - /mnt/data/f1r_translation_12key.txt
  - /mnt/data/f1r_translation_7step.txt  (if applicable)
"""

from pathlib import Path
import json
import csv
from collections import Counter

SEQ_PATH   = Path("/mnt/data/extendedset_v15.json")
PICT_PATH  = Path("/mnt/data/extendedset_v15.csv")
DEC_PATH   = Path("/mnt/data/f1r_decision_note.txt")

# Output path for 12-key translation variant
OUT_12     = Path("/mnt/data/f1r_translation_12key.txt")
# Output path for 7-step translation variant
OUT_7      = Path("/mnt/data/f1r_translation_7step.txt")
# Output path for 12-key translation variant
OUT_12_LAB  = Path("/mnt/data/f1r_translation_12key_lab.txt")
# Output path for 12-key translation variant
OUT_12_SPIR = Path("/mnt/data/f1r_translation_12key_spirit.txt")
# Output path for 12-key translation variant
OUT_12_MERGE = Path("/mnt/data/f1r_translation_12key_merged.txt")
# Output path for 12-key translation variant
OUT_12_TRANSL = Path("/mnt/data/f1r_translation_12key_translation.txt")

# Output path for 7-step translation variant
OUT_7_LAB  = Path("/mnt/data/f1r_translation_7step_lab.txt")
# Output path for 7-step translation variant
OUT_7_SPIR = Path("/mnt/data/f1r_translation_7step_spirit.txt")
# Output path for 7-step translation variant
OUT_7_MERGE = Path("/mnt/data/f1r_translation_7step_merged.txt")
# Output path for 7-step translation variant
OUT_7_TRANSL = Path("/mnt/data/f1r_translation_7step_translation.txt")



# Load operator sequence data from JSON
def load_seq(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load pictorial/visual cues from CSV
def load_pict(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        return rows[0] if rows else {}


# Load decoding decision note (e.g., 7-step or 12-key strategy)
def load_decision(path):
    if not path.exists():
        return "UNKNOWN", []
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    dec = "UNKNOWN"
    rationale = []
    if lines:
        head = lines[0].strip()
        if head.lower().startswith("decision:"):
            dec = head.split(":",1)[1].strip()
        for ln in lines[1:]:
            ln = ln.strip("- ").strip()
            if ln:
                rationale.append(ln)
    return dec, rationale

def phrase_counts(pict):
    roots = pict.get("roots_count", "?")
    leaves = pict.get("leaf_groups_count") or pict.get("leaf_pairs_count") or "?"
    buds = pict.get("bud_count", "?")
    bud_state = pict.get("bud_state","?")
    bud_color = pict.get("bud_colour","?")
    return roots, leaves, buds, bud_state, bud_color

def top_ops_hist(seq_data, k=6):
    hist = seq_data.get("operator_histogram", [])
    return [f"{op}×{ct}" for op, ct in hist[:k]]


# Write lines to output file
def write_lines(path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# Generate 12-key translation with both operational and spiritual interpretations
def make_12key(seq_data, pict, decision, rationale):
    roots, leaves, buds, bud_state, bud_color = phrase_counts(pict)
    ops = ", ".join(top_ops_hist(seq_data))

    # Templates: lightly parameterized with counts and histogram
    t = []
    t.append("Translation of f1r — Twelve Keys (Allegorical)")
    t.append("—")
    t.append(f"Snapshot: roots={roots}, leaves≈{leaves}, buds={buds} ({bud_state}/{bud_color}); frequent ops: {ops}")
    if rationale:
        t.append("Decision rationale: " + "; ".join(rationale))
    t.append("")

    t.extend([
        "Step 1 — Vessel & Naming"
        "",
        "Dual Reading:",
        "The vessel is both the physical flask and the soul’s container. Invocation awakens both the material and the self to the alchemical journey.",
        "",
        "The division marks not only chemical partition but the mystical separation of ego and essence.",
        "",
        "Dissolution serves to cleanse material and purify the inner self through surrender.",
        "",
        "Distillation echoes the ascent of spirit; impurities fall away in both lab and life.",
        "",
        "Conjunction reflects union: Sulphur and Mercury, masculine and feminine, body and soul.",
        "",
        "Nigredo symbolizes the dark night of the soul; the blackening before rebirth.",
        "",
        "Albedo washes the psyche clean; Luna’s light reveals the purified spirit.",
        "",
        "Citrinitas is the dawning awareness; Mars forges willpower in transformation.",
        "",
        "Rubedo completes the cycle: the alchemist becomes the Stone.",
        "",
        "Planetary forces don’t just guide reactions—they govern stages of inner development.",
        "",
        "Circulation mirrors breath, prayer, and meditation: the Work is not linear.",
        "",
        "The seal closes not only a flask, but also a rite. Completion blesses both craft and soul."
,
        "The matter is named and bound in its vessel. The root marks the body (Salt), fixed under Saturn’s weight. "
        "Invocation is repeated in glyphs (e.g., daiin) and leaf pairing, sealing the beginning of the work.",
        "",
        "Step 2 — Division",
        "The one is divided into twain and thrice: leaf pairs show duality, triplets imply the tria prima. "
        "Repetitions (daiin/aiin) and fixatives (chedy) portion the matter.",
        "",
        "Step 3 — Dissolution",
        "Stems and loops mark circulation and washing. Tokens like shol/chor indicate solve in water; the matter is softened and set apart.",
        "",
        "Step 4 — Distillation",
        "Droplet-like signs and repeated shody/qokedy patterns suggest distillation. Vapour rises and returns as dew; the subtle is separated from the gross.",
        "",
        "Step 5 — Conjunction",
        "Two buds appear, closed then opening: Sulphur unites with Mercury. Conjunction signs (cfhol) and daiin repetitions confirm the aim.",
        "",
        "Step 6 — Black Phase (Nigredo)",
        "Darkness of the root signals nigredo. The body putrefies; successive shody seals fix the stage.",
        "",
        "Step 7 — White Phase (Albedo)",
        "Leaves pale; east–west orientation encodes invocation and washing. Luna presides; the spirit clarifies.",
        "",
        "Step 8 — Yellow Phase (Citrinitas)",
        "Intermediate yellowing under Mars’s heat prepares perfection. Iterative forms (chedy, cthar) track cycles.",
        "",
        "Step 9 — Red Phase (Rubedo)",
        "The two red buds are the clearest cipher: open and red = Rubedo, the crown of the Work. Sol governs completion.",
        "",
        "Step 10 — Planetary Governance",
        "Saturn delays, Mars heats, Luna moistens, Sol perfects; leaf direction hints Air and Water. Planetary order binds the phases.",
        "",
        "Step 11 — Circulation & Return",
        "Cycles of daiin, shol, chor command: solve → coagula → fix. Vapours rise and fall; leaf pairs confirm counts (2, 3, 7).",
        "",
        "Step 12 — Seal & Completion",
        "Final y-terminations act as seals. With buds now red/open, the final conjunction is declared: the Work is closed and fixed."
    ])
    return t


# Generate 7-step translation with dual-layer format
def make_7step(seq_data, pict, decision, rationale):
    roots, leaves, buds, bud_state, bud_color = phrase_counts(pict)
    ops = ", ".join(top_ops_hist(seq_data))
    t = []
    t.append("Translation of f1r — Seven-Step Operator Cycle")
    t.append("—")
    t.append(f"Snapshot: roots={roots}, leaves≈{leaves}, buds={buds} ({bud_state}/{bud_color}); frequent ops: {ops}")
    if rationale:
        t.append("Decision rationale: " + "; ".join(rationale))
    t.append("")
    t.extend([
        "1) Name & Bind — Identify the matter, bind in the vessel, open the cycle with invocations (daiin)."
        "",
        "Spiritual Parallel:",
        "1) The name calls the soul to action; the vessel holds intent.",
        "2) Separation defines inner conflict; parts must know themselves.",
        "3) Washing purifies ego; flow liberates spirit.",
        "4) Distilling refines insight; vapor rises, truth condenses.",
        "5) Union heals duality; opposites embrace.",
        "6) Fixing grounds the Self; realization stabilizes the soul.",
        "7) Rubedo crowns the seeker; the Work completes with wisdom."
,
        "2) Divide & Portion — Split into halves/thirds; assign portions; chedy marks fixation points.",
        "3) Solve — Wash/circulate (shol/chor); soften and separate.",
        "4) Distil — Raise and return the subtle (shody/qokedy); condense as dew.",
        "5) Conjoin — Recombine fractions (cfhol) under measured heat.",
        "6) Fix — Seal interim results (y endings), weigh against root heaviness (Saturn).",
        "7) Perfect — Advance through colours to red; crown under Sol; close with a final seal."
    ])
    return t


# === Main translation workflow ===
def main():
    seq = load_seq(SEQ_PATH)

# Load pictorial/visual cues from CSV
    pict = load_pict(PICT_PATH) if PICT_PATH.exists() else {}

# Load decoding decision note (e.g., 7-step or 12-key strategy)
    decision, rationale = load_decision(DEC_PATH)


# Generate 12-key translation with both operational and spiritual interpretations
    txt12 = make_12key(seq, pict, decision, rationale)
# Output path for 12-key translation variant
    OUT_12.write_text("\n".join(txt12) + "\n", encoding="utf-8")

    if decision == "7_STEPS_OPERATOR":

# Generate 7-step translation with dual-layer format
        txt7 = make_7step(seq, pict, decision, rationale)
    else:
        # Still produce a 7-step for comparison

# Generate 7-step translation with dual-layer format
        txt7 = make_7step(seq, pict, "7_STEPS_OPERATOR (comparative)", [])
# Output path for 7-step translation variant
    OUT_7.write_text("\n".join(txt7) + "\n", encoding="utf-8")
    # Split and write 12-key files
    dual_start_12 = txt12.index("Dual Reading:")
    OUT_12_LAB.write_text("\n".join(txt12[:dual_start_12]).strip() + "\n")
    OUT_12_SPIR.write_text("\n".join(txt12[dual_start_12+1:]).strip() + "\n")
    merged_12 = []
    for op, sp in zip(txt12[:dual_start_12], txt12[dual_start_12+1:]):
        if op.strip() and sp.strip():
            merged_12.append(op.strip() + " / " + sp.strip())
        elif op.strip():
            merged_12.append(op.strip())
    OUT_12_MERGE.write_text("\n".join(merged_12) + "\n")
    OUT_12_TRANSL.write_text("\n".join(txt12) + "\n")

    # Split and write 7-step files
    dual_start_7 = txt7.index("Spiritual Parallel:")
    OUT_7_LAB.write_text("\n".join(txt7[:dual_start_7]).strip() + "\n")
    OUT_7_SPIR.write_text("\n".join(txt7[dual_start_7+1:]).strip() + "\n")
    merged_7 = []
    for op, sp in zip(txt7[:dual_start_7], txt7[dual_start_7+1:]):
        if op.strip() and sp.strip():
            merged_7.append(op.strip() + " / " + sp.strip())
        elif op.strip():
            merged_7.append(op.strip())
    OUT_7_MERGE.write_text("\n".join(merged_7) + "\n")
    OUT_7_TRANSL.write_text("\n".join(txt7) + "\n")


    print("Wrote:", OUT_12)
    print("Wrote:", OUT_7)


# Run script if called directly
if __name__ == "__main__":
    main()

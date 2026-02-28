"""
LeadVision Pro - Enterprise Lead Intelligence & Reporting System
Created by: Anuj
Version: 1.0.0
Copyright (c) 2024 Anuj. All rights reserved.

GitHub Repository: https://github.com/Anujh23/Lead-Vision-Pro.git
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import math


# ═══════════════════════════════════════════════════════════════════════════
# APPLICATION METADATA (Not visible in UI)
# ═══════════════════════════════════════════════════════════════════════════
__author__ = "Anuj"
__copyright__ = "Copyright (c) 2024 Anuj. All rights reserved."
__version__ = "1.0.0"
__license__ = "Proprietary"
__created_by__ = "Anuj"
__developer__ = "Anuj"


class LeadsAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("LeadVision Pro — Enterprise Lead Intelligence")
        self.root.geometry("1440x900")
        self.root.minsize(1200, 780)

        self.original_df  = None
        self.df           = None
        self.filtered_df  = None
        self.current_view = None
        self.detail_mode  = False

        # ── Glassmorphism Light Palette ──────────────────────────────────────
        self.C = {
            # Backgrounds
            'bg':         "#dce8f5",   # Soft periwinkle-blue background
            'glass':      "#ffffff", # White glass card (simulated)
            'glass_dark': "#f0f6ffee", # Slightly tinted glass
            'sidebar':    "#e8f0fa",   # Sidebar frosted
            'header':     "#ffffff",   # Header white
            # Borders / Shadow simulation
            'border':     "#c8d8ee",
            'border_hi':  "#4f8ef7",
            'shadow':     "#b8cce0",
            # Text
            'text':       "#1a2744",   # Deep navy text
            'text2':      "#5a6e8a",   # Secondary muted
            'text3':      "#2563eb",   # Accent text
            # Accent colors (vivid, saturated)
            'accent':     "#3b82f6",
            'accent2':    "#1d4ed8",
            'success':    "#10b981",
            'warning':    "#f59e0b",
            'danger':     "#ef4444",
            'info':       "#06b6d4",
            'purple':     "#8b5cf6",
            'pink':       "#ec4899",
            'teal':       "#14b8a6",
            'orange':     "#f97316",
            'indigo':     "#6366f1",
            'cyan':       "#0ea5e9",
            'lime':       "#84cc16",
            'rose':       "#f43f5e",
        }

        # Dynamic color pool for KPI cards
        self.DYN_COLORS = [
            self.C['accent'],  self.C['success'], self.C['info'],
            self.C['warning'], self.C['danger'],  self.C['purple'],
            self.C['pink'],    self.C['teal'],    self.C['orange'],
            self.C['cyan'],    self.C['lime'],    self.C['rose'],
            self.C['indigo'],  "#a855f7",         "#22d3ee",
            "#fb923c",         "#4ade80",         "#f472b6",
        ]

        self._configure_styles()
        self.create_widgets()

    # ─────────────────────────────────────────────────────────────────────────
    # STYLES
    # ─────────────────────────────────────────────────────────────────────────
    def _configure_styles(self):
        s = ttk.Style()
        s.theme_use('clam')

        s.configure("Treeview",
            background="#f8fbff", foreground=self.C['text'],
            fieldbackground="#f8fbff", rowheight=30,
            borderwidth=0, font=('Segoe UI', 10))
        s.map("Treeview",
            background=[('selected', '#dbeafe')],
            foreground=[('selected', self.C['accent2'])])
        s.configure("Treeview.Heading",
            background="#e8f0fa", foreground=self.C['text2'],
            font=('Segoe UI', 9, 'bold'), relief="flat", padding=10)
        s.map("Treeview.Heading",
            background=[('active', '#d4e4f7')],
            foreground=[('active', self.C['accent'])])

        for o in ("Vertical", "Horizontal"):
            s.configure(f"{o}.TScrollbar",
                background="#c8d8ee", troughcolor="#e8f0fa",
                bordercolor="#e8f0fa", arrowcolor=self.C['text2'],
                gripcount=0, relief="flat")

    # ─────────────────────────────────────────────────────────────────────────
    # MAIN WIDGET BUILDER
    # ─────────────────────────────────────────────────────────────────────────
    def create_widgets(self):
        self.root.configure(bg=self.C['bg'])
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        outer = tk.Frame(self.root, bg=self.C['bg'])
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_rowconfigure(1, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        self._build_header(outer)

        body = tk.Frame(outer, bg=self.C['bg'])
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        self._build_sidebar(body)
        self._build_right(body)

    # ─────────────────────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────────────────────
    def _build_header(self, parent):
        hdr = tk.Frame(parent, bg=self.C['header'], height=62)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)

        # Bottom shadow line
        tk.Frame(parent, bg=self.C['border'], height=1).grid(
            row=0, column=0, sticky="sew")

        # Diamond logo
        lc = tk.Canvas(hdr, width=34, height=34, bg=self.C['header'],
                        highlightthickness=0)
        lc.place(x=18, y=14)
        lc.create_polygon(17, 1, 33, 17, 17, 33, 1, 17,
                          fill=self.C['accent'], outline="")
        lc.create_polygon(17, 8, 26, 17, 17, 26, 8, 17,
                          fill=self.C['header'], outline="")

        # Title
        tf = tk.Frame(hdr, bg=self.C['header'])
        tf.place(x=60, y=9)
        tk.Label(tf, text="LeadVision Pro",
                 bg=self.C['header'], fg=self.C['text'],
                 font=("Segoe UI", 17, "bold")).pack(anchor="w")

        # Right controls
        rf = tk.Frame(hdr, bg=self.C['header'])
        rf.place(relx=1.0, x=-16, y=0, anchor="ne", height=62)
        rf.grid_rowconfigure(0, weight=1)

        self.file_label = tk.Label(rf, text="No dataset loaded",
            bg=self.C['header'], fg=self.C['text2'],
            font=("Segoe UI", 9, "italic"))
        self.file_label.pack(side="left", padx=(0, 18), pady=0, anchor="center")

        self.load_btn = tk.Button(rf, text="  ⬆  Import Dataset",
            command=self.load_file,
            bg=self.C['accent'], fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0, padx=16, pady=0, cursor="hand2",
            activebackground=self.C['accent2'], activeforeground="white",
            relief="flat", height=2)
        self.load_btn.pack(side="left", pady=10)

    # ─────────────────────────────────────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=self.C['sidebar'], width=215)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        # Right border
        tk.Frame(sb, bg=self.C['border'], width=1).pack(side="right", fill="y")

        inner = tk.Frame(sb, bg=self.C['sidebar'])
        inner.pack(fill="both", expand=True)

        # ── TIME PERIOD CARD ─────────────────────────────────────────────────
        tp_card = tk.Frame(inner,
            bg=self.C['glass'], highlightthickness=1,
            highlightbackground=self.C['border'])
        tp_card.pack(fill="x", padx=12, pady=(16, 10))

        # Card header strip
        tp_hdr = tk.Frame(tp_card, bg=self.C['accent'], height=3)
        tp_hdr.pack(fill="x", side="top")

        tp_body = tk.Frame(tp_card, bg=self.C['glass'])
        tp_body.pack(fill="x", padx=12, pady=10)

        # Icon + label row
        icon_row = tk.Frame(tp_body, bg=self.C['glass'])
        icon_row.pack(fill="x", pady=(0, 8))

        ic = tk.Canvas(icon_row, width=18, height=18, bg=self.C['glass'],
                        highlightthickness=0)
        ic.pack(side="left")
        # Calendar icon
        ic.create_rectangle(1, 3, 17, 17, outline=self.C['accent'],
                             fill="#eff6ff", width=2)
        ic.create_line(5, 1, 5, 5, fill=self.C['accent'], width=2)
        ic.create_line(13, 1, 13, 5, fill=self.C['accent'], width=2)
        ic.create_line(1, 7, 17, 7, fill=self.C['accent'], width=1)
        ic.create_rectangle(4, 9, 7, 12, fill=self.C['accent'], outline="")
        ic.create_rectangle(8, 9, 11, 12, fill=self.C['accent'], outline="")

        tk.Label(icon_row, text=" TIME PERIOD", bg=self.C['glass'],
                 fg=self.C['text'], font=("Segoe UI", 9, "bold")).pack(
            side="left")

        # Year row
        yr = tk.Frame(tp_body, bg=self.C['glass'])
        yr.pack(fill="x", pady=(0, 6))
        tk.Label(yr, text="Year", bg=self.C['glass'], fg=self.C['text2'],
                 font=("Segoe UI", 8)).pack(side="left")

        self.year_var = tk.StringVar(value="All Years")
        self.year_combo = ttk.Combobox(yr, textvariable=self.year_var,
            state="readonly", width=10, font=("Segoe UI", 9))
        self.year_combo.pack(side="right")
        self.year_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_date_filter())

        # Month row
        mr = tk.Frame(tp_body, bg=self.C['glass'])
        mr.pack(fill="x")
        tk.Label(mr, text="Month", bg=self.C['glass'], fg=self.C['text2'],
                 font=("Segoe UI", 8)).pack(side="left")

        self.month_var = tk.StringVar(value="All Months")
        self.month_combo = ttk.Combobox(mr, textvariable=self.month_var,
            state="readonly", width=10, font=("Segoe UI", 9))
        self.month_combo.pack(side="right")
        self.month_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_date_filter())

        # ── CATEGORIES LABEL ─────────────────────────────────────────────────
        cat_row = tk.Frame(inner, bg=self.C['sidebar'])
        cat_row.pack(fill="x", padx=12, pady=(6, 4))
        tk.Label(cat_row, text="CATEGORIES", bg=self.C['sidebar'],
                 fg=self.C['text2'], font=("Segoe UI", 8, "bold")).pack(side="left")

        # ── NAV BUTTONS ──────────────────────────────────────────────────────
        self.filter_buttons = {}
        filters = [
            ("Lead Status",    self.filter_status,         self.C['accent'],   "◈"),
            ("UTM Source",     self.filter_utm,            self.C['info'],     "◉"),
            ("Income Range",   self.filter_salary,         self.C['success'],  "◈"),
            ("Branch (City)",  self.filter_branch,         self.C['warning'],  "◈"),
            ("Credit Manager", self.filter_credit_manager, self.C['purple'],   "◈"),
            ("State",          self.filter_state,          self.C['cyan'],     "◈"),
            ("Duplicates",     self.filter_duplicates,     self.C['danger'],   "⚠"),
        ]
        for (text, cmd, color, icon) in filters:
            self._make_nav_btn(inner, text, cmd, text, color, icon)

        # Divider
        tk.Frame(inner, bg=self.C['border'], height=1).pack(
            fill="x", padx=12, pady=10)

        # All Leads button
        all_btn = tk.Button(inner, text="  ↩  Show All Leads",
            command=self.show_all,
            bg=self.C['sidebar'], fg=self.C['text2'],
            font=("Segoe UI", 9), bd=0, padx=12, pady=7,
            anchor="w", cursor="hand2", relief="flat",
            activebackground=self.C['border'])
        all_btn.pack(fill="x", padx=8, pady=2)

    def _make_nav_btn(self, parent, text, cmd, key, color, icon="◈"):
        frm = tk.Frame(parent, bg=self.C['sidebar'], cursor="hand2")
        frm.pack(fill="x", padx=8, pady=2)

        sw = tk.Canvas(frm, width=4, height=36, bg=self.C['sidebar'],
                        highlightthickness=0)
        sw.pack(side="left")

        btn = tk.Button(frm, text=f"  {icon}  {text}",
            command=lambda: self._apply_filter(cmd, key),
            bg=self.C['sidebar'], fg=self.C['text2'],
            font=("Segoe UI", 10), bd=0, padx=8, pady=7,
            anchor="w", cursor="hand2", relief="flat",
            activebackground=self.C['glass'],
            activeforeground=self.C['text'])
        btn.pack(fill="x", side="left", expand=True)

        def on_enter(e):
            if not self.filter_buttons.get(key, (None,)*5)[2]:
                frm.config(bg=self.C['glass'])
                btn.config(bg=self.C['glass'], fg=self.C['text'])
                sw.config(bg=self.C['glass'])
                sw.delete("all")
                sw.create_rectangle(0, 6, 4, 30, fill=color, outline="")

        def on_leave(e):
            if not self.filter_buttons.get(key, (None,)*5)[2]:
                frm.config(bg=self.C['sidebar'])
                btn.config(bg=self.C['sidebar'], fg=self.C['text2'])
                sw.config(bg=self.C['sidebar'])
                sw.delete("all")

        for w in (frm, btn, sw):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

        self.filter_buttons[key] = (btn, color, False, frm, sw)

    def _apply_filter(self, cmd, key):
        for k, (btn, color, _, frm, sw) in self.filter_buttons.items():
            btn.config(bg=self.C['sidebar'], fg=self.C['text2'])
            frm.config(bg=self.C['sidebar'])
            sw.config(bg=self.C['sidebar'])
            sw.delete("all")
            self.filter_buttons[k] = (btn, color, False, frm, sw)

        if key in self.filter_buttons:
            btn, color, _, frm, sw = self.filter_buttons[key]
            btn.config(bg=self.C['glass'], fg=color)
            frm.config(bg=self.C['glass'])
            sw.config(bg=self.C['glass'])
            sw.delete("all")
            sw.create_rectangle(0, 4, 4, 32, fill=color, outline="")
            self.filter_buttons[key] = (btn, color, True, frm, sw)
        cmd()

    # ─────────────────────────────────────────────────────────────────────────
    # RIGHT PANEL
    # ─────────────────────────────────────────────────────────────────────────
    def _build_right(self, parent):
        right = tk.Frame(parent, bg=self.C['bg'])
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # ── KPI STRIP ────────────────────────────────────────────────────────
        # Outer frame — NO fixed height, let cards define it
        kpi_outer = tk.Frame(right, bg=self.C['bg'])
        kpi_outer.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 10))
        kpi_outer.grid_columnconfigure(0, weight=1)

        self.kpi_canvas = tk.Canvas(kpi_outer, bg=self.C['bg'],
                                     highlightthickness=0, height=132)
        # Scrollbar — packed BELOW canvas with zero gap
        kpi_scroll = ttk.Scrollbar(kpi_outer, orient="horizontal",
                                    command=self.kpi_canvas.xview)
        self.kpi_canvas.grid(row=0, column=0, sticky="ew")
        kpi_scroll.grid(row=1, column=0, sticky="ew")
        self.kpi_canvas.configure(xscrollcommand=kpi_scroll.set)

        self.kpi_frame = tk.Frame(self.kpi_canvas, bg=self.C['bg'])
        self._kpi_win = self.kpi_canvas.create_window(
            (0, 0), window=self.kpi_frame, anchor="nw")

        self.kpi_frame.bind("<Configure>", lambda e:
            self.kpi_canvas.configure(
                scrollregion=self.kpi_canvas.bbox("all")))
        self.kpi_canvas.bind("<Configure>", lambda e:
            self.kpi_canvas.itemconfig(self._kpi_win, height=e.height))
        self.kpi_canvas.bind("<MouseWheel>", lambda e:
            self.kpi_canvas.xview_scroll(int(-1*(e.delta/120)), "units"))

        # ── CHART GRID ───────────────────────────────────────────────────────
        cg = tk.Frame(right, bg=self.C['bg'])
        cg.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        cg.grid_rowconfigure(0, weight=1)
        cg.grid_rowconfigure(1, weight=1)
        for i in range(3):
            cg.grid_columnconfigure(i, weight=1)

        self.status_chart    = self._chart_canvas(cg, 0, 0)
        self.utm_chart       = self._chart_canvas(cg, 0, 1)
        self.income_chart    = self._chart_canvas(cg, 0, 2)
        self.india_map_chart = self._chart_canvas(cg, 1, 0, colspan=2)
        self.duplicate_chart = self._chart_canvas(cg, 1, 2)

        # Hidden widgets for compatibility
        self.summary_label = tk.Label(right, text="", bg=self.C['bg'])
        self.tree = ttk.Treeview(right)
        self.tree.tag_configure('odd',  background="#f8fbff")
        self.tree.tag_configure('even', background="#eef5ff")

        self.kpi_frame = tk.Frame(self.kpi_canvas, bg=self.C['bg'])
        self._kpi_win = self.kpi_canvas.create_window(
            (0, 0), window=self.kpi_frame, anchor="nw")

    def _chart_canvas(self, parent, row, col, colspan=1):
        """Create a chart canvas with glass effect"""
        frm = tk.Frame(parent, bg=self.C['bg'])
        frm.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=6, pady=6)
        frm.grid_rowconfigure(0, weight=1)
        frm.grid_columnconfigure(0, weight=1)
        
        c = tk.Canvas(frm, bg=self.C['glass'],
                        highlightthickness=0, height=188)
        c.pack(fill="both", expand=True)
        return c

    # ─────────────────────────────────────────────────────────────────────────
    # KPI CARD BUILDER — fully dynamic
    # ─────────────────────────────────────────────────────────────────────────
    def _make_kpi_card(self, parent, title, value, subtitle, color, col):
        W, H = 178, 118

        card = tk.Frame(parent,
            bg=self.C['glass'], width=W, height=H,
            highlightthickness=1,
            highlightbackground=self.C['border'])
        card.grid(row=0, column=col, padx=(0, 8), pady=0, sticky="nsew")
        card.grid_propagate(False)

        # Top colored accent stripe
        tk.Frame(card, bg=color, height=4).pack(fill="x", side="top")

        body = tk.Frame(card, bg=self.C['glass'])
        body.pack(fill="both", expand=True, padx=12, pady=(8, 6))

        # Title row with dot
        tr = tk.Frame(body, bg=self.C['glass'])
        tr.pack(fill="x")
        dc = tk.Canvas(tr, width=8, height=8, bg=self.C['glass'],
                        highlightthickness=0)
        dc.pack(side="left", pady=2)
        dc.create_oval(1, 1, 7, 7, fill=color, outline="")
        tk.Label(tr, text=title.upper(), bg=self.C['glass'],
                 fg=self.C['text2'], font=("Segoe UI", 7, "bold")).pack(
            side="left", padx=(5, 0))

        # Big value
        tk.Label(body, text=str(value), bg=self.C['glass'],
                 fg=self.C['text'], font=("Segoe UI", 24, "bold")).pack(
            anchor="w", pady=(2, 0))

        # Subtitle
        tk.Label(body, text=str(subtitle), bg=self.C['glass'],
                 fg=self.C['text2'], font=("Segoe UI", 8)).pack(anchor="w")

    def _rebuild_kpi_cards(self, cards):
        """Destroy old cards and rebuild with exactly len(cards) columns."""
        for w in self.kpi_frame.winfo_children():
            w.destroy()

        n = len(cards)
        for i in range(n):
            self.kpi_frame.grid_columnconfigure(i, weight=0, minsize=178)

        for i, (title, value, sub, color) in enumerate(cards):
            self._make_kpi_card(self.kpi_frame, title, value, sub, color, i)

        # Dynamically size the canvas height to card height
        self.kpi_frame.update_idletasks()
        self.kpi_canvas.configure(
            scrollregion=self.kpi_canvas.bbox("all"),
            height=122)

    # ─────────────────────────────────────────────────────────────────────────
    # CHART DRAWING
    # ─────────────────────────────────────────────────────────────────────────
    def _draw_bar_chart(self, canvas, title, labels, values, color):
        canvas.delete("all")
        canvas.update_idletasks()
        w = max(canvas.winfo_width(), 10)
        h = max(canvas.winfo_height(), 10)
        PL, PR, PT, PB = 12, 12, 36, 10

        # Glass card bg gradient simulation
        canvas.create_rectangle(0, 0, w, h, fill=self.C['glass'], outline="")

        # Title
        canvas.create_text(PL, 13, text=title, anchor="nw",
                           fill=self.C['text'], font=("Segoe UI", 10, "bold"))
        # Underline
        canvas.create_line(PL, 30, w - PR, 30,
                           fill=self.C['border'], width=1)

        if not values:
            canvas.create_text(w//2, h//2, text="No Data Available",
                               fill=self.C['text2'], font=("Segoe UI", 9))
            return

        max_v   = max(values) or 1
        n       = min(len(values), 8)
        avail_h = h - PT - PB
        bar_h   = max(14, min(22, avail_h // n - 6))
        gap     = max(4, (avail_h - n * bar_h) // max(n, 1))
        label_w = 115

        for i in range(n):
            y = PT + i * (bar_h + gap)
            if y + bar_h > h - PB:
                break
            v   = values[i]
            lbl = str(labels[i])
            if len(lbl) > 19: lbl = lbl[:18] + "…"
            pct   = v / max_v
            bar_x = PL + label_w
            max_bw = w - bar_x - PR - 52
            bw    = int(max_bw * pct)

            # Track
            canvas.create_rectangle(bar_x, y, bar_x + max_bw, y + bar_h,
                fill=self.C['border'], outline="")
            # Fill
            if bw > 2:
                canvas.create_rectangle(bar_x, y, bar_x + bw, y + bar_h,
                    fill=color, outline="")
                # Shine
                canvas.create_rectangle(bar_x, y, bar_x + bw, y + max(3, bar_h//5),
                    fill=self._lighten(color, 0.35), outline="")

            canvas.create_text(PL, y + bar_h//2, text=lbl, anchor="w",
                               fill=self.C['text2'], font=("Segoe UI", 9))
            canvas.create_text(bar_x + max_bw + 6, y + bar_h//2,
                               text=f"{v:,}", anchor="w",
                               fill=self.C['text'], font=("Segoe UI", 9, "bold"))

    def _draw_donut(self, canvas, title, labels, values, colors):
        canvas.delete("all")
        canvas.update_idletasks()
        w = max(canvas.winfo_width(), 10)
        h = max(canvas.winfo_height(), 10)
        P = 12

        canvas.create_rectangle(0, 0, w, h, fill=self.C['glass'], outline="")
        canvas.create_text(P, 13, text=title, anchor="nw",
                           fill=self.C['text'], font=("Segoe UI", 10, "bold"))
        canvas.create_line(P, 30, w - P, 30, fill=self.C['border'], width=1)

        total = sum(values) if values else 0
        if total <= 0:
            canvas.create_text(w//2, h//2, text="No Data Available",
                               fill=self.C['text2'], font=("Segoe UI", 9))
            return

        r  = min(w // 2 - 90, (h - 45) // 2)
        r  = max(r, 35)
        cx = P + r + 8
        cy = 38 + r
        bbox = (cx - r, cy - r, cx + r, cy + r)

        start = 90
        for i, v in enumerate(values[:7]):
            extent = -(v / total) * 360
            c = colors[i % len(colors)]
            canvas.create_arc(bbox, start=start, extent=extent,
                              fill=c, outline="white", width=2)
            start += extent

        # Hole
        hr = r * 0.54
        canvas.create_oval(cx-hr, cy-hr, cx+hr, cy+hr,
                           fill=self.C['glass'], outline=self.C['glass'])
        canvas.create_text(cx, cy - 8, text=f"{total:,}",
                           fill=self.C['text'], font=("Segoe UI", 11, "bold"))
        canvas.create_text(cx, cy + 10, text="Total",
                           fill=self.C['text2'], font=("Segoe UI", 8))

        # Legend
        lx = cx + r + 16
        ly = 38
        for i, (lbl, v) in enumerate(list(zip(labels, values))[:7]):
            c   = colors[i % len(colors)]
            row_y = ly + i * 21
            if row_y + 16 > h - 6:
                break
            canvas.create_rectangle(lx, row_y + 2, lx + 10, row_y + 12,
                                    fill=c, outline="")
            short = str(lbl)[:15] + ("…" if len(str(lbl)) > 15 else "")
            canvas.create_text(lx + 14, row_y + 7, text=short, anchor="w",
                               fill=self.C['text2'], font=("Segoe UI", 8))
            canvas.create_text(w - P, row_y + 7, text=f"{v:,}", anchor="e",
                               fill=self.C['text'], font=("Segoe UI", 8, "bold"))

    def _lighten(self, hex_color, f=0.25):
        h = hex_color.lstrip('#')
        r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r + (255-r)*f))
        g = min(255, int(g + (255-g)*f))
        b = min(255, int(b + (255-b)*f))
        return f"#{r:02x}{g:02x}{b:02x}"

    # ─────────────────────────────────────────────────────────────────────────
    # DASHBOARD UPDATE — DYNAMIC CARDS
    # ─────────────────────────────────────────────────────────────────────────
    def update_dashboard(self):
        if self.df is None:
            return

        total  = len(self.df)
        cards  = []
        colors = self.DYN_COLORS

        col_map = {
            'status':         'Status',
            'utm':            'Utm Source',
            'branch':         'City',
            'credit_manager': 'Leads Assign',
            'state':          'State',
        }

        # ── CATEGORY VIEWS: show exactly as many cards as there are values ──
        if self.current_view in col_map or self.current_view == 'salary':
            cards.append(("Total Leads", f"{total:,}",
                          "All filtered data", self.C['indigo']))

            if self.current_view == 'salary':
                df_t = self.df.copy()
                df_t['Monthly Income'] = pd.to_numeric(
                    df_t['Monthly Income'], errors='coerce')
                bins   = [0, 50000, 80000, 100000, 150000, float('inf')]
                lbls   = ['0–50K', '51–80K', '81K–1L', '1L–1.5L', '>1.5L']
                counts = pd.cut(df_t['Monthly Income'], bins=bins,
                                labels=lbls, include_lowest=True).value_counts()
                # Reindex so all 5 buckets always appear
                counts = counts.reindex(lbls, fill_value=0)
            else:
                cname  = col_map[self.current_view]
                counts = self.df[cname].value_counts() \
                         if cname in self.df.columns else pd.Series(dtype=int)

            # ALL values — no cap, fully dynamic
            for i, (name, val) in enumerate(counts.items()):
                short = str(name)
                if len(short) > 14: short = short[:13] + "…"
                pct = f"{val/total*100:.1f}%" if total else "0%"
                cards.append((short, f"{val:,}", pct,
                              colors[(i + 1) % len(colors)]))

        # ── DUPLICATES VIEW ──────────────────────────────────────────────────
        elif self.current_view == 'duplicates':
            def _dc(col):
                if col not in self.df.columns: return 0
                d = self.df[self.df.duplicated(subset=[col], keep=False)]
                return len(d) - d[col].nunique() if len(d) > 0 else 0

            dm, de, dp = _dc('Mobile'), _dc('Email'), _dc('Pancard')
            cards.append(("Total Leads",  f"{total:,}", "All data",     self.C['indigo']))
            cards.append(("Mobile Dupes", f"{dm:,}",    "By mobile",    self.C['danger']))
            cards.append(("Email Dupes",  f"{de:,}",    "By email",     self.C['warning']))
            cards.append(("PAN Dupes",    f"{dp:,}",    "By PAN",       self.C['info']))

        # ── DEFAULT / ALL VIEW ───────────────────────────────────────────────
        else:
            top3 = [("—", 0)] * 3
            if 'Status' in self.df.columns:
                sc   = self.df['Status'].value_counts()
                top3 = [(s, c) for s, c in sc.head(3).items()]
            while len(top3) < 3: top3.append(("—", 0))

            dm = 0
            if 'Mobile' in self.df.columns:
                md = self.df[self.df.duplicated(subset=['Mobile'], keep=False)]
                dm = len(md) - md['Mobile'].nunique() if len(md) > 0 else 0
            dup_rate = f"{dm/total*100:.1f}%" if total else "0%"

            utm_src, utm_cnt, utm_uniq = "N/A", 0, 0
            if 'Utm Source' in self.df.columns:
                uc       = self.df['Utm Source'].value_counts()
                utm_uniq = uc.shape[0]
                if len(uc):
                    utm_src = str(uc.index[0])
                    utm_cnt = int(uc.iloc[0])

            uniq_cities  = self.df['City'].nunique()  if 'City'  in self.df.columns else 0
            uniq_states  = self.df['State'].nunique() if 'State' in self.df.columns else 0

            high_income = 0
            if 'Monthly Income' in self.df.columns:
                inc = pd.to_numeric(self.df['Monthly Income'], errors='coerce')
                high_income = int((inc >= 100000).sum())

            share_sub = "All Data"
            if isinstance(self.original_df, pd.DataFrame) and len(self.original_df) > 0:
                pct = total / len(self.original_df) * 100
                share_sub = f"{pct:.1f}% of {len(self.original_df):,}"

            utm_lbl = utm_src[:13] + "…" if len(utm_src) > 13 else utm_src

            def pct3(idx):
                return f"{top3[idx][1]/total*100:.1f}%" if total else "0%"

            cards = [
                ("Total Leads",   f"{total:,}",         share_sub,             self.C['accent']),
                (top3[0][0][:14], f"{top3[0][1]:,}",   pct3(0),               self.C['success']),
                (top3[1][0][:14], f"{top3[1][1]:,}",   pct3(1),               self.C['info']),
                (top3[2][0][:14], f"{top3[2][1]:,}",   pct3(2),               self.C['rose']),
                ("Duplicates",    f"{dm:,}",            "Mobile dupes",        self.C['warning']),
                ("Dup. Rate",     dup_rate,             "of total leads",      self.C['danger']),
                ("UTM Sources",   f"{utm_uniq:,}",      "Unique sources",      self.C['teal']),
                ("Top UTM",       utm_lbl,              f"{utm_cnt:,} leads",  self.C['purple']),
                ("Cities",        f"{uniq_cities:,}",   "Active cities",       self.C['pink']),
                ("States",        f"{uniq_states:,}",   "Active states",       self.C['cyan']),
                ("High Income",   f"{high_income:,}",   "Income ≥ 1L",        self.C['lime']),
            ]

        # Rebuild KPI cards dynamically
        self._rebuild_kpi_cards(cards)

        # ── CHARTS ───────────────────────────────────────────────────────────
        def after_draw():
            # Status bar chart
            if 'Status' in self.df.columns:
                sc = self.df['Status'].value_counts().head(8)
                self._draw_bar_chart(self.status_chart, "Top Status",
                    sc.index.tolist(), sc.values.tolist(), self.C['accent'])
            else:
                self._draw_bar_chart(self.status_chart, "Top Status",
                    [], [], self.C['accent'])

            # UTM donut
            if 'Utm Source' in self.df.columns:
                uc = self.df['Utm Source'].value_counts().head(7)
                dc = [self.C['purple'], self.C['info'], self.C['success'],
                      self.C['warning'], self.C['pink'], self.C['teal'],
                      self.C['orange']]
                self._draw_donut(self.utm_chart, "Top UTM Sources",
                    uc.index.tolist(), uc.values.tolist(), dc)
            else:
                self._draw_donut(self.utm_chart, "Top UTM Sources",
                    [], [], [self.C['accent']])

            # Income buckets
            if 'Monthly Income' in self.df.columns:
                df_i = self.df.copy()
                df_i['Monthly Income'] = pd.to_numeric(
                    df_i['Monthly Income'], errors='coerce')
                bins  = [0, 50000, 80000, 100000, 150000, float('inf')]
                lblsi = ['0–50K', '51–80K', '81K–1L', '1–1.5L', '1.5L+']
                df_i['IB'] = pd.cut(df_i['Monthly Income'], bins=bins,
                                    labels=lblsi, include_lowest=True)
                ic = df_i['IB'].value_counts().reindex(lblsi, fill_value=0)
                self._draw_bar_chart(self.income_chart, "Income Buckets",
                    ic.index.tolist(), ic.values.tolist(), self.C['success'])

            # India map with state-wise leads
            if 'State' in self.df.columns:
                state_counts = self.df['State'].value_counts()
                self._draw_india_map(self.india_map_chart, state_counts)
            else:
                self._draw_india_map(self.india_map_chart, {})

            # Duplicates overview with vertical bars
            dup_l = []; dup_v = []
            for col, lbl in [('Mobile', 'Mobile'), ('Email', 'Email'), ('Pancard', 'Pancard')]:
                if col in self.df.columns:
                    d = self.df[self.df.duplicated(subset=[col], keep=False)]
                    cnt = len(d) - d[col].nunique() if len(d) > 0 else 0
                    if cnt > 0:
                        dup_l.append(lbl); dup_v.append(cnt)
            self._draw_vertical_bar_chart(self.duplicate_chart, "Duplicates Overview",
                dup_l, dup_v, self.C['danger'])

        self.root.after(30, after_draw)

    def _draw_india_map(self, canvas: tk.Canvas, state_counts: dict):
        """Draw top states as clean horizontal bar chart - LARGER SIZE"""
        canvas.delete("all")
        w = 520  # Increased width
        h = 240  # Increased height
        pad = 20  # Increased padding
        
        # Clean white background
        canvas.create_rectangle(0, 0, w, h, fill="#ffffff", outline="")
        
        # Title - larger font
        canvas.create_text(pad, pad, text="Top States by Lead Count", anchor="nw", 
                         fill="#1e293b", font=("Arial", 13, "bold"))
        
        if len(state_counts) == 0:
            canvas.create_text(w//2, h//2, text="No state data available", 
                             fill="#94a3b8", font=("Arial", 11))
            return
        
        # Get top 7 states
        if hasattr(state_counts, 'head'):
            top_states = state_counts.head(7)
        else:
            top_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)[:7]
        
        max_count = max(top_states.values) if hasattr(top_states, 'values') else max([v for _, v in top_states])
        total_leads = sum(state_counts.values) if hasattr(state_counts, 'values') else sum(state_counts.values())
        
        # Chart area - adjusted for larger size
        chart_top = pad + 35
        chart_bottom = h - pad - 25
        bar_height = 16  # Increased bar height
        gap = 8  # Increased gap
        
        # Draw bars
        for i, (state, count) in enumerate(top_states.items() if hasattr(top_states, 'items') else top_states):
            y = chart_top + i * (bar_height + gap)
            if y + bar_height > chart_bottom:
                break
            
            # Calculate bar width
            bar_max_width = w - pad * 2 - 130
            bar_width = (count / max_count) * bar_max_width if max_count > 0 else 0
            
            # State label - larger font
            canvas.create_text(pad, y + bar_height//2, text=state[:20], anchor="w", 
                             fill="#374151", font=("Arial", 10))
            
            # Bar background (light gray)
            canvas.create_rectangle(pad + 110, y, pad + 110 + bar_max_width, y + bar_height, 
                                  fill="#f1f5f9", outline="", width=0)
            
            # Colored bar
            intensity = count / max_count if max_count > 0 else 0
            if intensity > 0.6:
                bar_color = "#2563eb"  # Strong blue
            elif intensity > 0.3:
                bar_color = "#3b82f6"  # Medium blue
            else:
                bar_color = "#60a5fa"  # Light blue
            
            canvas.create_rectangle(pad + 110, y, pad + 110 + bar_width, y + bar_height, 
                                  fill=bar_color, outline="", width=0)
            
            # Value label at end of bar - larger font
            canvas.create_text(pad + 110 + bar_width + 6, y + bar_height//2, 
                             text=f"{count:,}", anchor="w", 
                             fill="#1e40af", font=("Arial", 10, "bold"))
        
        # Summary at bottom - larger font
        active_states = len([s for s in (state_counts.index if hasattr(state_counts, 'index') else state_counts) 
                            if (state_counts[s] if hasattr(state_counts, '__getitem__') else state_counts.get(s, 0)) > 0])
        canvas.create_text(w//2, h - 14, text=f"{total_leads:,} total leads across {active_states} states", 
                         fill="#6b7280", font=("Arial", 10))

    def _draw_vertical_bar_chart(self, canvas: tk.Canvas, title: str, labels, values, color: str):
        """Draw clean gauge-style duplicate metrics"""
        canvas.delete("all")
        w = 400
        h = 180
        pad = 20
        
        # Clean white background
        canvas.create_rectangle(0, 0, w, h, fill="#ffffff", outline="")
        
        # Title
        canvas.create_text(w//2, pad, text=title, anchor="n", 
                         fill="#1e293b", font=("Arial", 12, "bold"))
        
        if not values:
            canvas.create_text(w//2, h//2, text="No Duplicates Found", 
                             fill="#22c55e", font=("Arial", 11))
            return
        
        max_val = max(values) if max(values) > 0 else 1
        total = sum(values)
        
        # Create gauge-style cards for each duplicate type
        card_width = 100
        card_height = 80
        start_x = (w - (len(values) * card_width + (len(values) - 1) * 15)) // 2
        y_pos = 100  # Shifted down from 50 to 65
        
        for i, (lbl, val) in enumerate(zip(labels, values)):
            x = start_x + i * (card_width + 15)
            
            # Card shadow
            canvas.create_rectangle(x + 2, y_pos + 2, x + card_width + 2, y_pos + card_height + 2, 
                                  fill="#e5e7eb", outline="")
            
            # Card background
            canvas.create_rectangle(x, y_pos, x + card_width, y_pos + card_height, 
                                  fill="#f9fafb", outline="#d1d5db", width=1)
            
            # Gauge arc background
            arc_center_x = x + card_width // 2
            arc_center_y = y_pos + 35
            arc_radius = 25
            
            # Background arc (gray)
            canvas.create_arc(arc_center_x - arc_radius, arc_center_y - arc_radius,
                            arc_center_x + arc_radius, arc_center_y + arc_radius,
                            start=0, extent=180, fill="#e5e7eb", outline="")
            
            # Calculate fill extent based on value
            fill_extent = (val / max_val) * 180 if max_val > 0 else 0
            
            # Choose color based on severity
            if val / max_val > 0.7:
                fill_color = "#dc2626"  # Red (high)
            elif val / max_val > 0.4:
                fill_color = "#f59e0b"  # Orange (medium)
            else:
                fill_color = "#3b82f6"  # Blue (low)
            
            # Fill arc
            if fill_extent > 0:
                canvas.create_arc(arc_center_x - arc_radius, arc_center_y - arc_radius,
                                arc_center_x + arc_radius, arc_center_y + arc_radius,
                                start=180 - fill_extent, extent=fill_extent, fill=fill_color, outline="")
            
            # Center value
            canvas.create_text(arc_center_x, arc_center_y + 5, text=f"{val:,}", 
                             fill="#1f2937", font=("Arial", 12, "bold"))
            
            # Label below
            canvas.create_text(x + card_width//2, y_pos + card_height - 12, text=lbl, 
                             fill="#4b5563", font=("Arial", 9))
    
    def _adjust_brightness(self, hex_color, factor):
        """Adjust brightness of a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, max(0, int(c * factor))) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    # ─────────────────────────────────────────────────────────────────────────
    # DATA LOAD & FILTER
    # ─────────────────────────────────────────────────────────────────────────
    def _find_date_column(self, df):
        possible = ['created at', 'date', 'created_on', 'timestamp', 'lead_date']
        for col in df.columns:
            if str(col).lower().strip() in possible:
                return col
        return None

    def _setup_date_filters(self):
        if self.original_df is None: return
        dc = self._find_date_column(self.original_df)
        if not dc:
            self.year_combo['values']  = ["All Years"]
            self.month_combo['values'] = ["All Months"]
            self.year_combo.set("All Years")
            self.month_combo.set("All Months")
            self.year_combo.config(state="disabled")
            self.month_combo.config(state="disabled")
            return
        try:
            dates  = pd.to_datetime(self.original_df[dc], errors='coerce').dropna()
            years  = sorted(dates.dt.year.unique().astype(int).tolist(), reverse=True)
            months = ['Jan','Feb','Mar','Apr','May','Jun',
                      'Jul','Aug','Sep','Oct','Nov','Dec']
            self.year_combo['values']  = ["All Years"] + [str(y) for y in years]
            self.month_combo['values'] = ["All Months"] + months
            self.year_combo.set("All Years");   self.year_combo.config(state="readonly")
            self.month_combo.set("All Months"); self.month_combo.config(state="readonly")
            self.original_df['_parsed_date'] = pd.to_datetime(
                self.original_df[dc], errors='coerce')
        except Exception as e:
            print(f"Date error: {e}")

    def apply_date_filter(self):
        if self.original_df is None: return
        ys = self.year_var.get()
        ms = self.month_var.get()
        if '_parsed_date' not in self.original_df.columns:
            self.df = self.original_df.copy()
        else:
            mask = pd.Series(True, index=self.original_df.index)
            if ys != "All Years":
                mask &= (self.original_df['_parsed_date'].dt.year == int(ys))
            if ms != "All Months":
                mlist = ['Jan','Feb','Mar','Apr','May','Jun',
                         'Jul','Aug','Sep','Oct','Nov','Dec']
                mask &= (self.original_df['_parsed_date'].dt.month ==
                         mlist.index(ms) + 1)
            self.df = self.original_df[mask].copy()
        self.filtered_df = self.df.copy()
        for k, (btn, color, _, frm, sw) in self.filter_buttons.items():
            btn.config(bg=self.C['sidebar'], fg=self.C['text2'])
            frm.config(bg=self.C['sidebar']); sw.config(bg=self.C['sidebar'])
            sw.delete("all")
            self.filter_buttons[k] = (btn, color, False, frm, sw)
        self.detail_mode  = False
        self.current_view = "all"
        self.update_dashboard()
        self.show_all()

    def load_file(self):
        fp = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if fp:
            try:
                self.original_df  = pd.read_csv(fp, low_memory=False)
                self.df           = self.original_df.copy()
                self.filtered_df  = self.df.copy()
                self.file_label.config(
                    text=f"{fp.split('/')[-1]}  ·  {len(self.df):,} records")
                self.detail_mode  = False
                self.current_view = "all"
                self._setup_date_filters()
                self.update_dashboard()
                self.show_all()
                messagebox.showinfo("Success",
                    f"Loaded {len(self.df):,} records successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")

    # ─────────────────────────────────────────────────────────────────────────
    # FILTER METHODS
    # ─────────────────────────────────────────────────────────────────────────
    def display_data(self, data):
        if data is None: return
        self.filtered_df = data.copy()
        self.update_dashboard()

    def show_all(self):
        if self.df is None: return
        self.filtered_df = self.df.copy()
        self.current_view = "all"
        self.detail_mode  = False
        self.display_data(self.df)

    def filter_status(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV first!"); return
        self.current_view = "status"; self.detail_mode = False
        self._set_tree_from_counts(self.df['Status'].value_counts(),
            ['Status', 'Count', 'Percentage'])
        self.update_dashboard()

    def filter_utm(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV first!"); return
        self.current_view = "utm"; self.detail_mode = False
        self._set_tree_from_counts(self.df['Utm Source'].value_counts(),
            ['UTM Source', 'Count', 'Percentage'])
        self.update_dashboard()

    def filter_branch(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV first!"); return
        self.current_view = "branch"; self.detail_mode = False
        self._set_tree_from_counts(self.df['City'].value_counts(),
            ['Branch (City)', 'Count', 'Percentage'])
        self.update_dashboard()

    def filter_credit_manager(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV first!"); return
        if 'Leads Assign' not in self.df.columns:
            messagebox.showinfo("Info", "Leads Assign column not found!"); return
        self.current_view = "credit_manager"; self.detail_mode = False
        self._set_tree_from_counts(self.df['Leads Assign'].value_counts(),
            ['Credit Manager', 'Count', 'Percentage'])
        self.update_dashboard()

    def filter_state(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV first!"); return
        if 'State' not in self.df.columns:
            messagebox.showinfo("Info", "State column not found!"); return
        self.current_view = "state"; self.detail_mode = False
        self._set_tree_from_counts(self.df['State'].value_counts(),
            ['State', 'Count', 'Percentage'])
        self.update_dashboard()

    def filter_salary(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV first!"); return
        self.current_view = "salary"; self.detail_mode = False
        df = self.df.copy()
        df['Monthly Income'] = pd.to_numeric(df['Monthly Income'], errors='coerce')
        bins  = [0, 50000, 80000, 100000, 150000, float('inf')]
        lbls  = ['0–50K', '51–80K', '81K–1Lakh', '1L–1.5Lakh', '>1.5L']
        df['SR'] = pd.cut(df['Monthly Income'], bins=bins,
                          labels=lbls, include_lowest=True)
        self._set_tree_from_counts(df['SR'].value_counts(),
            ['Salary Range', 'Count', 'Percentage'])
        self.update_dashboard()

    def filter_duplicates(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV first!"); return
        self.current_view = "duplicates"; self.detail_mode = False

        def _dc(col):
            if col not in self.df.columns: return 0
            d = self.df[self.df.duplicated(subset=[col], keep=False)]
            return len(d) - d[col].nunique() if len(d) > 0 else 0

        dm, de, dp = _dc('Mobile'), _dc('Email'), _dc('Pancard')
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ['Type', 'Count']
        self.tree["show"]    = "headings"
        for col in ['Type', 'Count']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300, anchor="center")
        for row in [('Mobile Dupes', dm), ('Email Dupes', de), ('PAN Dupes', dp)]:
            self.tree.insert("", "end", values=row)
        self.filtered_df = pd.DataFrame(
            {'Type': ['Mobile','Email','PAN'], 'Count': [dm, de, dp]})
        self.update_dashboard()

    def _set_tree_from_counts(self, counts, cols):
        total  = len(self.df)
        df_out = counts.reset_index()
        df_out.columns = [cols[0], cols[1]]
        df_out[cols[2]] = (df_out[cols[1]] / total * 100).round(1).astype(str)+'%'
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols
        self.tree["show"]    = "headings"
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")
        for _, row in df_out.iterrows():
            self.tree.insert("", "end", values=list(row))
        self.filtered_df = df_out

    def show_detail_view(self, data, title):
        self.detail_mode  = True
        self.filtered_df  = data
        self.display_data(data)
        self.summary_label.config(text=f"{title} — {len(data):,} records")

    def back_to_summary(self):
        self.detail_mode = False
        self.search_var.set("")
        fn = {
            "status": self.filter_status, "utm": self.filter_utm,
            "salary": self.filter_salary, "branch": self.filter_branch,
            "credit_manager": self.filter_credit_manager,
            "duplicates": self.filter_duplicates, "state": self.filter_state,
        }.get(self.current_view, self.show_all)
        fn()

    def search_data(self):
        if self.df is None: return
        query = self.search_var.get().strip()
        if not query or query == self._search_placeholder: return
        src  = self.filtered_df if (isinstance(self.filtered_df, pd.DataFrame)
               and self.detail_mode) else self.df
        mask = src.astype(str).apply(
            lambda x: x.str.lower().str.contains(query.lower(), na=False)).any(axis=1)
        result = src[mask]
        self.filtered_df = result
        self.detail_mode = True
        self.display_data(result)

    def clear_search(self):
        if self.df is None: return
        self.search_var.set("")
        self._set_search_placeholder()
        self.back_to_summary()

    def _set_search_placeholder(self):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, self._search_placeholder)

    def _on_search_focus_in(self, e):
        if self.search_entry.get() == self._search_placeholder:
            self.search_entry.delete(0, 'end')

    def _on_search_focus_out(self, e):
        if not self.search_entry.get().strip():
            self._set_search_placeholder()

    def export_data(self):
        data = self.filtered_df \
               if (isinstance(self.filtered_df, pd.DataFrame)
                   and len(self.filtered_df) > 0) else self.df
        if data is None or len(data) == 0:
            messagebox.showwarning("Warning", "No data to export!"); return
        fp = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
            initialfile=f"leads_export_{datetime.now():%Y%m%d_%H%M%S}.csv")
        if fp:
            try:
                data.to_csv(fp, index=False)
                messagebox.showinfo("Success", f"Exported {len(data):,} records.")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    # Stubs
    def update_quick_stats(self): pass
    def on_tree_double_click(self, event): pass
    def _get_state_counts(self): return {}
    def create_progress_bar(self, *a, **kw): pass
    def create_clickable_progress_bar(self, *a, **kw): pass
    def filter_salary_detail(self, sr): return self.df
    def filter_duplicate_detail(self, t): return self.df


if __name__ == "__main__":
    root = tk.Tk()
    app  = LeadsAnalyzer(root)
    root.mainloop()
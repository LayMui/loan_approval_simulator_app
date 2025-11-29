import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LoanApprovalSimulator(ttk.Window):
    def __init__(self):
        super().__init__(title="💰 Loan Approval Probability Simulator", themename="superhero")
        self.geometry("950x700")
        self.resizable(False, False)

        self.entries = {}
        self.error_labels = {}
        self._build_ui()

    # ---------------------------------------------------------
    # UI SETUP
    # ---------------------------------------------------------
    def _build_ui(self):
        ttk.Label(self, text="Loan Approval Probability Simulator",
                  font=("Segoe UI", 20, "bold")).pack(pady=15)

        # Input Section
        form = ttk.Labelframe(self, text="Loan Application Details", padding=15)
        form.pack(fill="x", padx=20, pady=10)

        fields = [
            ("Annual Income (SGD)", "income"),
            ("Credit Score (300 - 850)", "credit"),
            ("Monthly Debt (SGD)", "debt"),
            ("Loan Amount Requested (SGD)", "loan")
        ]

        # Each field: Label | Entry | Inline Error BELOW entry
        for i, (label, key) in enumerate(fields):
            row = i * 2  # double the row index to leave space for error below
            ttk.Label(form, text=label, font=("Segoe UI", 11)).grid(row=row, column=0, sticky="w", pady=(5, 0), padx=5)

            entry = ttk.Entry(form, width=25, bootstyle=INFO)
            entry.grid(row=row, column=1, sticky="w", pady=(5, 0))
            self.entries[key] = entry

            # Inline error label BELOW entry
            error_label = ttk.Label(form, text="", font=("Segoe UI", 9, "italic"), foreground="red")
            error_label.grid(row=row + 1, column=1, sticky="w", padx=5, pady=(0, 5))
            self.error_labels[key] = error_label

        # Info button beside Credit Score field
        # ttk.Button(form, text="❓", width=3, bootstyle=(INFO, OUTLINE),
        #            command=self.show_credit_info).grid(row=1, column=2, padx=8, sticky="w")

        # Info button beside Credit Score field (aligned with its entry on row=2)
        info_btn = ttk.Button(
            form,
            text="❓",
            width=3,
            bootstyle=(INFO, OUTLINE),
            command=self.show_credit_info
        )
        info_btn.grid(row=2, column=2, padx=(8, 0), pady=(5, 0), sticky="w")


        # Action Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Calculate", bootstyle=SUCCESS, width=18,
                   command=self.run_simulation).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Reset", bootstyle=SECONDARY, width=18,
                   command=self.reset_form).grid(row=0, column=1, padx=10)

        # Result Section
        self.progress_label = ttk.Label(self, text="", font=("Segoe UI", 13, "bold"))
        self.progress_label.pack(pady=(5, 3))

        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate", bootstyle=SUCCESS)
        self.progress.pack(pady=(0, 10))

        self.result_label = ttk.Label(self, text="", font=("Segoe UI", 14, "bold"))
        self.result_label.pack(pady=(5, 10))

        self.chart_frame = ttk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Label(self, text="Developed by Team 7 MH6803 Python Project November 2025",
                  font=("Segoe UI", 9, "italic"), foreground="#9ab").pack(pady=5)

    # ---------------------------------------------------------
    # CREDIT SCORE INFO
    # ---------------------------------------------------------
    def show_credit_info(self):
        messagebox.showinfo(
            "Credit Score Guide",
            "Credit Score ranges between 300 and 850:\n\n"
            "800–850  ⭐⭐⭐⭐⭐  Excellent — Very high approval chance\n"
            "740–799  ⭐⭐⭐⭐   Very Good — Good interest rates\n"
            "670–739  ⭐⭐⭐    Fair — Average approval odds\n"
            "580–669  ⭐⭐     Poor — Low approval chance\n"
            "300–579  ⭐      Very Poor — Unlikely to be approved"
        )

    # ---------------------------------------------------------
    # INLINE FIELD ERROR
    # ---------------------------------------------------------
    def show_field_error(self, field, message):
        """Show inline error below specific field, auto-clears after 4s."""
        self.error_labels[field].config(text=message)
        self.after(4000, lambda: self.error_labels[field].config(text=""))

    def clear_all_errors(self):
        for lbl in self.error_labels.values():
            lbl.config(text="")

    # ---------------------------------------------------------
    # MAIN LOGIC
    # ---------------------------------------------------------
    def run_simulation(self):
        """Validate inputs and simulate loan approval."""
        self.clear_all_errors()
        valid = True

        # --- Validation per field ---
        try:
            income = float(self.entries["income"].get())
            if income <= 0:
                self.show_field_error("income", "Must be > 0")
                valid = False
        except ValueError:
            self.show_field_error("income", "Enter number")
            valid = False

        try:
            credit = float(self.entries["credit"].get())
            if not (300 <= credit <= 850):
                self.show_field_error("credit", "300–850 only")
                valid = False
        except ValueError:
            self.show_field_error("credit", "Enter number")
            valid = False

        try:
            debt = float(self.entries["debt"].get())
        except ValueError:
            self.show_field_error("debt", "Enter number")
            valid = False

        try:
            loan = float(self.entries["loan"].get())
            if loan <= 0:
                self.show_field_error("loan", "Must be > 0")
                valid = False
        except ValueError:
            self.show_field_error("loan", "Enter number")
            valid = False

        if not valid:
            return  # Stop if any validation fails

        # --- Compute normalized factors ---
        income_factor = min(income / (loan * 0.5), 1)
        credit_factor = (credit - 300) / (850 - 300)
        debt_factor = max(1 - (debt / (income * 0.4)), 0)

        approval_prob = 0.4 * income_factor + 0.4 * credit_factor + 0.2 * debt_factor
        approval_pct = round(approval_prob * 100, 2)

        # --- Update UI ---
        self.progress["value"] = approval_pct
        self.progress_label.config(text=f"Predicted Loan Approval Probability: {approval_pct}%")

        # Result summary
        if approval_pct >= 70:
            msg = f"✅ Approved — Excellent financial standing ({approval_pct}%)"
            color = "green"
        elif 50 <= approval_pct < 70:
            msg = f"⚖️ Borderline — Consider reducing debt or applying for a smaller loan ({approval_pct}%)"
            color = "#f1c40f"
        else:
            msg = f"❌ Not Approved — Improve credit or income ({approval_pct}%)"
            color = "red"

        self.result_label.config(text=msg, foreground=color)
        self.display_chart(income_factor, credit_factor, debt_factor)

    # ---------------------------------------------------------
    # VISUALIZATION
    # ---------------------------------------------------------
    def display_chart(self, income_factor, credit_factor, debt_factor):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        labels = ["Income Strength", "Credit Score", "Debt Burden"]
        values = [income_factor, credit_factor, debt_factor]
        colors = ["#1abc9c", "#3498db", "#f39c12"]

        fig, ax = plt.subplots(figsize=(7.5, 4), dpi=100)
        bars = ax.bar(labels, values, color=colors)
        ax.bar_label(bars, fmt="%.2f", padding=3)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Normalized Score (0–1)", fontsize=11)
        ax.set_title("Loan Approval Factors Contribution", fontsize=13, weight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.6)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # RESET FORM
    # ---------------------------------------------------------
    def reset_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.progress["value"] = 0
        self.progress_label.config(text="")
        self.result_label.config(text="")
        self.clear_all_errors()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()


# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------
if __name__ == "__main__":
    app = LoanApprovalSimulator()
    app.mainloop()

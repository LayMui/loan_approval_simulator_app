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

        for i, (label, key) in enumerate(fields):
            ttk.Label(form, text=label, font=("Segoe UI", 11)).grid(row=i, column=0, sticky="w", pady=8, padx=5)
            entry = ttk.Entry(form, width=25, bootstyle=INFO)
            entry.grid(row=i, column=1, pady=8)
            self.entries[key] = entry

        ttk.Button(form, text="❓", width=3, bootstyle=(INFO, OUTLINE),
                   command=self.show_credit_info).grid(row=1, column=2, padx=8)

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

        self.chart_frame = ttk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Label(self, text="Developed by Team of 5 — Demonstrating Algorithm Design, UI Creativity, and Robustness",
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
    # MAIN LOGIC
    # ---------------------------------------------------------
    def run_simulation(self):
        # Validate Inputs
        try:
            income = float(self.entries["income"].get())
            credit = float(self.entries["credit"].get())
            debt = float(self.entries["debt"].get())
            loan = float(self.entries["loan"].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numeric values for all fields.")
            return

        if any(v <= 0 for v in [income, loan]) or not (300 <= credit <= 850):
            messagebox.showerror("Invalid Values",
                                 "Ensure income and loan > 0 and credit score between 300 and 850.")
            return

        # Compute normalized factors
        income_factor = min(income / (loan * 0.5), 1)
        credit_factor = (credit - 300) / (850 - 300)
        debt_factor = max(1 - (debt / (income * 0.4)), 0)

        # Weighted model
        approval_prob = 0.4 * income_factor + 0.4 * credit_factor + 0.2 * debt_factor
        approval_pct = round(approval_prob * 100, 2)

        # Update UI
        self.progress["value"] = approval_pct
        self.progress_label.config(text=f"Predicted Loan Approval Probability: {approval_pct}%")

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
        for widget in self.chart_frame.winfo_children():
            widget.destroy()


# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------
if __name__ == "__main__":
    app = LoanApprovalSimulator()
    app.mainloop()  # Start event loop (keeps window open)

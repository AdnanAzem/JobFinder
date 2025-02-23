import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from nlp.resume_parser import parse_resume
from api.job_fetcher import fetch_jobs
from nlp.job_matcher import rank_jobs
from database.models import session, Resume
from cli.commands.upload_resume import check_and_truncate_resumes 

class JobFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Finder")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Custom Fonts
        self.title_font = ("Helvetica", 16, "bold")
        self.label_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")

        # Main Frame
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(pady=20)

        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="Job Finder",
            font=self.title_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Upload Resume Section
        self.upload_label = tk.Label(
            self.main_frame,
            text="Upload Resume (PDF):",
            font=self.label_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        self.upload_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.upload_button = tk.Button(
            self.main_frame,
            text="Browse",
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            relief="flat",
            command=self.upload_resume
        )
        self.upload_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.resume_id_label = tk.Label(
            self.main_frame,
            text="Resume ID: None",
            font=self.label_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        self.resume_id_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Search Jobs Section
        self.job_title_label = tk.Label(
            self.main_frame,
            text="Job Title:",
            font=self.label_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        self.job_title_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.job_title_entry = tk.Entry(
            self.main_frame,
            width=40,
            font=self.label_font,
            relief="flat",
            bg="white"
        )
        self.job_title_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.location_label = tk.Label(
            self.main_frame,
            text="Location:",
            font=self.label_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        self.location_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.location_entry = tk.Entry(
            self.main_frame,
            width=40,
            font=self.label_font,
            relief="flat",
            bg="white"
        )
        self.location_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)

        self.search_button = tk.Button(
            self.buttons_frame,
            text="Search Jobs",
            font=self.button_font,
            bg="#2196F3",
            fg="white",
            relief="flat",
            command=self.search_jobs
        )
        self.search_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(
            self.buttons_frame,
            text="Reset",
            font=self.button_font,
            bg="#FF5722",
            fg="white",
            relief="flat",
            command=self.reset_fields
        )
        self.reset_button.pack(side="left", padx=10)

        # Results Display Section
        self.results_label = tk.Label(
            self.main_frame,
            text="Job Recommendations:",
            font=self.label_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        self.results_label.grid(row=6, column=0, columnspan=2, pady=10)

        self.results_text = scrolledtext.ScrolledText(
            self.main_frame,
            width=70,
            height=10,
            font=self.label_font,
            relief="flat",
            bg="white"
        )
        self.results_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def upload_resume(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                check_and_truncate_resumes()
                parsed_resume = parse_resume(file_path)
                resume = Resume(
                    file_path=file_path,
                    content=parsed_resume["content"],
                    skills=", ".join(parsed_resume["skills"])
                )
                session.add(resume)
                session.commit()
                self.resume_id_label.config(text=f"Resume ID: {resume.id}")
                messagebox.showinfo("Success", "Resume uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload resume: {e}")

    def search_jobs(self):
        resume_id = self.resume_id_label.cget("text").split(": ")[1]
        if resume_id == "None":
            messagebox.showerror("Error", "Please upload a resume first.")
            return

        query = self.job_title_entry.get()
        location = self.location_entry.get()
        if not query or not location:
            messagebox.showerror("Error", "Please enter a job title and location.")
            return

        try:
            resume = session.query(Resume).filter_by(id=resume_id).first()
            if not resume:
                messagebox.showerror("Error", "Resume not found!")
                return

            jobs = fetch_jobs(query, location)
            ranked_jobs = rank_jobs(resume.skills, jobs)

            # Display results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Top Job Recommendations:\n\n")
            for job, score in ranked_jobs[:5]:
                self.results_text.insert(tk.END, f"Title: {job['job_title']}\n")
                self.results_text.insert(tk.END, f"Company: {job['employer_name']}\n")
                self.results_text.insert(tk.END, f"Location: {job['job_location']}\n")
                self.results_text.insert(tk.END, f"Score: {score:.2f}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search jobs: {e}")

    def reset_fields(self):
        # Clear Resume ID
        self.resume_id_label.config(text="Resume ID: None")

        # Clear Job Title and Location fields
        self.job_title_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)

        # Clear Job Recommendations
        self.results_text.delete(1.0, tk.END)

        messagebox.showinfo("Reset", "All fields have been reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JobFinderApp(root)
    root.mainloop()
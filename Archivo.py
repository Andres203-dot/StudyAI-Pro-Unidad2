import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from datetime import date

class StudyAIPro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" StudyAI Pro")
        self.root.geometry("900x600")
        self.root.configure(bg="#1E1E2E")
        
        self.db = sqlite3.connect('studyai.db')
        self.user_id = None
        self.setup_db()
        self.show_login()
    
    def setup_db(self):
        c = self.db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            subject TEXT,
            duration INTEGER,
            score INTEGER,
            date TEXT
        )''')
        self.db.commit()
    
    def hash_pwd(self, pwd):
        return hashlib.md5(pwd.encode()).hexdigest()
    
    def show_login(self):
        # Limpiar
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        frame = tk.Frame(self.root, bg="#252535", bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Título
        title = tk.Label(frame, text=" StudyAI Pro", font=("Arial", 40, "bold"), 
                        fg="#00d4ff", bg="#252535")
        title.pack(pady=80)
        
        # Usuario
        tk.Label(frame, text="Usuario:", font=("Arial", 16), fg="white", bg="#252535").pack(pady=20)
        self.entry_user = tk.Entry(frame, font=("Arial", 14), width=30, justify="center")
        self.entry_user.pack(pady=10)
        self.entry_user.insert(0, "prueba")
        
        # Contraseña
        tk.Label(frame, text="Contraseña:", font=("Arial", 16), fg="white", bg="#252535").pack(pady=20)
        self.entry_pwd = tk.Entry(frame, font=("Arial", 14), show="*", width=30, justify="center")
        self.entry_pwd.pack(pady=10)
        self.entry_pwd.insert(0, "1234")
        
        # Botones
        btn_frame = tk.Frame(frame, bg="#252535")
        btn_frame.pack(pady=50)
        
        # Helper para crear botones animados
        def create_btn(text, bg, hover, cmd):
            btn = tk.Button(btn_frame, text=text, font=("Arial", 16, "bold"),
                           bg=bg, fg="white", width=15, height=2,
                           relief="flat", cursor="hand2", command=cmd,
                           activebackground=hover, activeforeground="white")
            btn.bind("<Enter>", lambda e: btn.config(bg=hover))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg))
            return btn

        create_btn(" LOGIN", "#00d4ff", "#0099cc", self.login).pack(side="left", padx=20)
        create_btn("➕ REGISTRAR", "#00cc88", "#00aa66", self.register).pack(side="right", padx=20)
    
    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pwd.get()
        
        c = self.db.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", 
                 (user, self.hash_pwd(pwd)))
        result = c.fetchone()
        
        if result:
            self.user_id = result[0]
            self.show_main()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta")
    
    def register(self):
        user = self.entry_user.get()
        pwd = self.entry_pwd.get()
        
        if len(user) < 3 or len(pwd) < 3:
            messagebox.showerror("Error", "Mínimo 3 caracteres")
            return
        
        try:
            c = self.db.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (user, self.hash_pwd(pwd)))
            self.db.commit()
            messagebox.showinfo("Éxito", "Usuario creado!")
        except:
            messagebox.showerror("Error", "Usuario ya existe")
    
    def show_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Sidebar
        sidebar = tk.Frame(self.root, width=250, bg="#252535", bd=2, relief="ridge")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="StudyAI Pro", font=("Arial", 24, "bold"), 
                fg="#00d4ff", bg="#252535").pack(pady=40)
        
        tk.Button(sidebar, text=" Dashboard", font=("Arial", 16), 
                 bg="#3E3E4E", fg="white", width=18, height=2,
                 command=self.show_dashboard).pack(pady=15, padx=20, fill="x")
        
        tk.Button(sidebar, text="➕ Nueva Sesión", font=("Arial", 16), 
                 bg="#3E3E4E", fg="white", width=18, height=2,
                 command=self.show_new_session).pack(pady=15, padx=20, fill="x")
        
        tk.Button(sidebar, text=" Estadísticas", font=("Arial", 16), 
                 bg="#3E3E4E", fg="white", width=18, height=2,
                 command=self.show_stats).pack(pady=15, padx=20, fill="x")
        
        tk.Button(sidebar, text="🧹 Resetear Datos", font=("Arial", 16), 
                 bg="#C75C00", fg="white", width=18, height=2,
                 command=self.reset_data).pack(pady=15, padx=20, fill="x")
        
        tk.Button(sidebar, text="🗑️ Borrar Cuenta", font=("Arial", 16), 
                 bg="#8B0000", fg="white", width=18, height=2,
                 command=self.delete_account).pack(pady=15, padx=20, fill="x")
        
        tk.Button(sidebar, text=" Salir", font=("Arial", 16), 
                 bg="#ff4444", fg="white", width=18, height=2,
                 command=self.show_login).pack(pady=(40,30), padx=20, fill="x")
        
        # Contenido
        self.content = tk.Frame(self.root, bg="#1E1E2E")
        self.content.pack(side="right", fill="both", expand=True, padx=(15, 30))
        self.show_dashboard()
    
    def show_dashboard(self):
        for w in self.content.winfo_children(): w.destroy()
        
        tk.Label(self.content, text=" Dashboard", font=("Arial", 32, "bold"), 
                fg="white", bg="#1E1E2E").pack(pady=50)
        
        # Estadísticas
        c = self.db.cursor()
        c.execute("SELECT COUNT(*), SUM(duration), AVG(score) FROM sessions WHERE user_id=?", (self.user_id,))
        stats = c.fetchone()
        
        stats_frame = tk.Frame(self.content, bg="#252535", relief="groove", bd=2)
        stats_frame.pack(pady=30, padx=50, fill="x")
        
        tk.Label(stats_frame, text=f"Sesiones: {stats[0] or 0}", 
                font=("Arial", 24, "bold"), fg="#00d4ff", bg="#252535").pack(pady=20)
        tk.Label(stats_frame, text=f"Horas: {(stats[1] or 0)/60:.1f}", 
                font=("Arial", 24, "bold"), fg="#ffaa00", bg="#252535").pack(pady=10)
        tk.Label(stats_frame, text=f"Promedio: {(stats[2] or 0):.1f}/10", 
                font=("Arial", 24, "bold"), fg="#00ff88", bg="#252535").pack(pady=20)
        
        tk.Label(self.content, text=" Tips: Haz sesiones de 25 min", 
                font=("Arial", 18), fg="#a0a0a0", bg="#1E1E2E").pack(pady=30)
    
    def show_new_session(self):
        for w in self.content.winfo_children(): w.destroy()
        
        tk.Label(self.content, text="➕ Nueva Sesión", 
                font=("Arial", 32, "bold"), fg="white", bg="#1E1E2E").pack(pady=60)
        
        frame = tk.Frame(self.content, bg="#252535", bd=2, relief="groove")
        frame.pack(pady=40, padx=50, fill="x")
        
        tk.Label(frame, text="Materia:", font=("Arial", 18), fg="white", bg="#252535").pack(pady=20)
        self.new_subject = tk.Entry(frame, font=("Arial", 16), width=40)
        self.new_subject.pack(pady=10)
        
        tk.Label(frame, text="Minutos:", font=("Arial", 18), fg="white", bg="#252535").pack(pady=20)
        self.new_duration = tk.Entry(frame, font=("Arial", 16), width=40)
        self.new_duration.insert(0, "25")
        self.new_duration.pack(pady=10)
        
        tk.Label(frame, text="Puntuación (1-10):", font=("Arial", 18), fg="white", bg="#252535").pack(pady=20)
        self.new_score = tk.Entry(frame, font=("Arial", 16), width=40)
        self.new_score.insert(0, "8")
        self.new_score.pack(pady=10)
        
        btn = tk.Button(frame, text="💾 GUARDAR SESIÓN", font=("Arial", 18, "bold"), 
                       bg="#00cc88", fg="white", width=25, height=2,
                       relief="flat", cursor="hand2", command=self.save_session,
                       activebackground="#00aa66", activeforeground="white")
        btn.bind("<Enter>", lambda e: btn.config(bg="#00aa66"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#00cc88"))
        btn.pack(pady=40)
    
    def save_session(self):
        try:
            subj = self.new_subject.get()
            dur = int(self.new_duration.get())
            score = int(self.new_score.get())
            
            c = self.db.cursor()
            c.execute("INSERT INTO sessions(user_id, subject, duration, score, date) VALUES(?, ?, ?, ?, ?)",
                     (self.user_id, subj, dur, score, str(date.today())))
            self.db.commit()
            messagebox.showinfo("¡Listo!", f"Sesión guardada:\n{subj} - {dur}min - {score}/10")
            self.show_dashboard()
        except:
            messagebox.showerror("Error", "Verifica los datos")
    
    def show_stats(self):
        for w in self.content.winfo_children(): w.destroy()
        
        tk.Label(self.content, text=" Estadísticas", 
                font=("Arial", 32, "bold"), fg="white", bg="#1E1E2E").pack(pady=60)
        
        c = self.db.cursor()
        c.execute("SELECT subject, SUM(duration), COUNT(*), AVG(score) FROM sessions WHERE user_id=? GROUP BY subject", 
                 (self.user_id,))
        
        frame = tk.Frame(self.content, bg="#1E1E2E")
        frame.pack(fill="both", expand=True, padx=60, pady=30)
        
        for subj, hours, count, avg in c.fetchall():
            text = f"{subj}: {hours/60:.1f}h ({count} sesiones, {avg:.1f}/10)"
            tk.Label(frame, text=text, font=("Arial", 16), fg="white", bg="#252535",
                    relief="ridge", bd=2, padx=20, pady=15).pack(fill="x", pady=10)
    
    def reset_data(self):
        confirm = messagebox.askyesno("⚠️ Confirmar", "¿Estás seguro de BORRAR todo tu historial de estudio?\n\nSe eliminarán todas las sesiones, pero tu usuario se mantendrá.")
        if confirm:
            c = self.db.cursor()
            c.execute("DELETE FROM sessions WHERE user_id=?", (self.user_id,))
            self.db.commit()
            messagebox.showinfo("Limpieza", "Tu historial ha sido borrado exitosamente.")
            self.show_dashboard()
    
    def delete_account(self):
        confirm = messagebox.askyesno("⚠️ PELIGRO", "¿Estás seguro de BORRAR TU CUENTA y todos tus datos?\n\nEsta acción NO se puede deshacer.")
        if confirm:
            c = self.db.cursor()
            c.execute("DELETE FROM sessions WHERE user_id=?", (self.user_id,))
            c.execute("DELETE FROM users WHERE id=?", (self.user_id,))
            self.db.commit()
            messagebox.showinfo("Eliminado", "Tu cuenta y datos han sido borrados permanentemente.")
            self.show_login()
    
    def run(self):
        self.root.mainloop()

# EJECUTAR
if __name__ == "__main__":
    app = StudyAIPro()
    app.run()

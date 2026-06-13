import customtkinter as ctk
import threading
import psutil
import datetime
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#070714"
BG2 = "#0a0a1e"
BG3 = "#0d0d28"
BG4 = "#080818"
BORDER = "#1a1a3e"
GREEN = "#00ff88"
RED = "#ff3355"
BLUE = "#4499ff"
YELLOW = "#ffaa00"
PURPLE = "#aa44ff"
TEXT = "#8899cc"
DIM = "#444466"
WHITE = "#ffffff"

class HexaDashboard:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Hexa - AI Desktop Assistant")
        self.root.geometry("1150x680")
        self.root.configure(fg_color=BG)
        self.is_listening = False
        self.command_count = 0
        self.setup_ui()
        self.update_stats()
        self.update_time()

    def get_avatar(self):
        photo_path = Path.home() / ".hexa-agent" / "profile.png"
        try:
            if photo_path.exists():
                img = Image.open(photo_path).convert("RGB")
            else:
                img = Image.new("RGB", (80, 80), "#0a0a2a")
                draw = ImageDraw.Draw(img)
                draw.ellipse([2, 2, 78, 78], fill="#0055cc")
                draw.text((24, 20), "H", fill="white")
            mask = Image.new("L", (80, 80), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, 80, 80], fill=255)
            out = Image.new("RGBA", (80, 80), (0,0,0,0))
            out.paste(img, mask=mask)
            return out
        except:
            return None

    def setup_ui(self):
        hdr = ctk.CTkFrame(self.root, height=62, corner_radius=0, fg_color=BG2)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        try:
            av = self.get_avatar()
            if av:
                av_ctk = ctk.CTkImage(av, size=(38, 38))
                ctk.CTkLabel(hdr, image=av_ctk, text="").pack(side="left", padx=(14,8), pady=12)
        except:
            pass

        brand = ctk.CTkFrame(hdr, fg_color="transparent")
        brand.pack(side="left", pady=12)
        ctk.CTkLabel(brand, text="HEXA", font=ctk.CTkFont(size=18, weight="bold"), text_color=BLUE).pack(anchor="w")
        ctk.CTkLabel(brand, text="AI DESKTOP ASSISTANT", font=ctk.CTkFont(size=8), text_color=DIM).pack(anchor="w")

        ctk.CTkButton(hdr, text="Photo", width=80, height=28, corner_radius=6,
            font=ctk.CTkFont(size=10), fg_color=BG3, hover_color="#2a2a5e",
            border_color=BORDER, border_width=1, text_color=TEXT,
            command=self.change_photo).pack(side="right", padx=12)

        self.time_lbl = ctk.CTkLabel(hdr, text="", font=ctk.CTkFont(size=11), text_color=DIM)
        self.time_lbl.pack(side="right", padx=12)

        body = ctk.CTkFrame(self.root, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=10, pady=(8,0))

        sb = ctk.CTkFrame(body, width=220, corner_radius=10, fg_color=BG4, border_color=BORDER, border_width=1)
        sb.pack(side="left", fill="y", padx=(0,8))
        sb.pack_propagate(False)

        mic_card = ctk.CTkFrame(sb, corner_radius=8, fg_color=BG3, border_color=BORDER, border_width=1)
        mic_card.pack(fill="x", padx=10, pady=(12,6))
        ctk.CTkLabel(mic_card, text="MICROPHONE STATUS", font=ctk.CTkFont(size=8), text_color=DIM).pack(anchor="w", padx=10, pady=(8,2))
        self.mic_dot = ctk.CTkLabel(mic_card, text="INACTIVE", font=ctk.CTkFont(size=12, weight="bold"), text_color=RED)
        self.mic_dot.pack(anchor="w", padx=10, pady=(0,8))

        ctk.CTkButton(sb, text="Start Listening", height=40, corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#001a0d", hover_color="#002a15",
            border_color=GREEN, border_width=1, text_color=GREEN,
            command=self.start_listening).pack(fill="x", padx=10, pady=3)

        ctk.CTkButton(sb, text="Stop Listening", height=40, corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1a0008", hover_color="#2a0010",
            border_color=RED, border_width=1, text_color=RED,
            command=self.stop_listening).pack(fill="x", padx=10, pady=3)

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(sb, text="QUICK COMMANDS", font=ctk.CTkFont(size=8), text_color=DIM).pack(anchor="w", padx=12, pady=(0,4))

        for label, cmd in [
            ("Chrome", "open chrome"),
            ("VS Code", "open vs code"),
            ("Files", "open file manager"),
            ("Screenshot", "take screenshot"),
            ("Volume Up", "increase volume"),
            ("Mute", "mute volume"),
            ("System Info", "check ram"),
            ("Desktop", "show desktop"),
        ]:
            ctk.CTkButton(sb, text=label, height=30, corner_radius=6,
                font=ctk.CTkFont(size=11), fg_color=BG3, hover_color="#1a1a3e",
                border_color=BORDER, border_width=1, anchor="w", text_color=TEXT,
                command=lambda c=cmd: self.run_cmd(c)).pack(fill="x", padx=10, pady=2)

        ctr = ctk.CTkFrame(body, corner_radius=10, fg_color=BG4, border_color=BORDER, border_width=1)
        ctr.pack(side="left", fill="both", expand=True, padx=(0,8))

        lh = ctk.CTkFrame(ctr, fg_color="transparent")
        lh.pack(fill="x", padx=12, pady=(10,4))
        ctk.CTkLabel(lh, text="COMMAND HISTORY", font=ctk.CTkFont(size=8), text_color=DIM).pack(side="left")
        ctk.CTkButton(lh, text="Clear", width=50, height=22, corner_radius=5,
            font=ctk.CTkFont(size=10), fg_color=BG3, hover_color="#1a1a3e",
            border_color=BORDER, border_width=1, text_color=DIM,
            command=self.clear).pack(side="right")

        log_wrap = tk.Frame(ctr, bg="#030310", highlightthickness=1, highlightbackground=BORDER)
        log_wrap.pack(fill="both", expand=True, padx=12, pady=(0,6))

        self.log_widget = tk.Text(log_wrap, bg="#030310", fg=TEXT,
            font=("Consolas", 11), bd=0, relief="flat", wrap="word",
            state="disabled", cursor="arrow", selectbackground="#1a1a3e")
        self.log_widget.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        scroll = tk.Scrollbar(log_wrap, command=self.log_widget.yview, bg=BG3, troughcolor=BG)
        scroll.pack(side="right", fill="y")
        self.log_widget.configure(yscrollcommand=scroll.set)

        self.log_widget.tag_configure("s", foreground=GREEN)
        self.log_widget.tag_configure("e", foreground=RED)
        self.log_widget.tag_configure("i", foreground=BLUE)
        self.log_widget.tag_configure("w", foreground=YELLOW)
        self.log_widget.tag_configure("u", foreground=WHITE)
        self.log_widget.tag_configure("t", foreground=DIM)
        self.log_widget.tag_configure("n", foreground=TEXT)

        inp = ctk.CTkFrame(ctr, fg_color=BG3, corner_radius=8, border_color=BORDER, border_width=1)
        inp.pack(fill="x", padx=12, pady=(0,10))
        self.cmd_in = ctk.CTkEntry(inp, placeholder_text="Type a command...",
            border_width=0, fg_color="transparent",
            font=ctk.CTkFont(size=12), text_color=WHITE)
        self.cmd_in.pack(side="left", fill="x", expand=True, pady=7, padx=10)
        self.cmd_in.bind("<Return>", lambda e: self.exec_typed())
        ctk.CTkButton(inp, text="Run", width=70, height=28, corner_radius=6,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#003388", hover_color="#0044aa",
            command=self.exec_typed).pack(side="right", padx=8, pady=6)

        rt = ctk.CTkFrame(body, width=195, corner_radius=10, fg_color=BG4, border_color=BORDER, border_width=1)
        rt.pack(side="right", fill="y")
        rt.pack_propagate(False)

        ctk.CTkLabel(rt, text="SYSTEM STATS", font=ctk.CTkFont(size=8), text_color=DIM).pack(anchor="w", padx=12, pady=(12,6))
        self.cpu_w = self.mk_stat(rt, "CPU", BLUE)
        self.ram_w = self.mk_stat(rt, "RAM", PURPLE)
        self.dsk_w = self.mk_stat(rt, "Disk", YELLOW)
        self.bat_w = self.mk_stat(rt, "Battery", GREEN)

        ctk.CTkFrame(rt, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(rt, text="COMMANDS RUN", font=ctk.CTkFont(size=8), text_color=DIM).pack()
        self.cnt_lbl = ctk.CTkLabel(rt, text="0", font=ctk.CTkFont(size=34, weight="bold"), text_color=BLUE)
        self.cnt_lbl.pack()
        ctk.CTkFrame(rt, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=8)
        self.ag_lbl = ctk.CTkLabel(rt, text="HEXA READY", font=ctk.CTkFont(size=11, weight="bold"), text_color=GREEN)
        self.ag_lbl.pack()

        sbar = ctk.CTkFrame(self.root, height=26, corner_radius=0, fg_color="#030310")
        sbar.pack(fill="x", side="bottom")
        sbar.pack_propagate(False)
        self.st_lbl = ctk.CTkLabel(sbar, text="Ready", font=ctk.CTkFont(size=10), text_color=DIM)
        self.st_lbl.pack(side="left", padx=14, pady=4)
        ctk.CTkLabel(sbar, text="Hexa v1.0.0  |  AI Desktop Assistant",
            font=ctk.CTkFont(size=10), text_color="#1a1a3e").pack(side="right", padx=14, pady=4)

        self.add_log("Hexa dashboard loaded successfully.", "s")
        self.add_log("Click start listening or type a command.", "i")

    def mk_stat(self, parent, title, color):
        card = ctk.CTkFrame(parent, corner_radius=8, fg_color=BG3, border_color=BORDER, border_width=1)
        card.pack(fill="x", padx=10, pady=3)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=(6,2))
        ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=10), text_color=DIM).pack(side="left")
        val = ctk.CTkLabel(row, text="0%", font=ctk.CTkFont(size=10, weight="bold"), text_color=color)
        val.pack(side="right")
        bar = ctk.CTkProgressBar(card, height=4, corner_radius=2, progress_color=color)
        bar.pack(fill="x", padx=10, pady=(0,6))
        bar.set(0)
        return val, bar

    def add_log(self, msg, tag="n"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_widget.configure(state="normal")
        self.log_widget.insert("end", f"[{ts}]  ", "t")
        self.log_widget.insert("end", f"{msg}\n", tag)
        self.log_widget.configure(state="disabled")
        self.log_widget.see("end")

    def set_status(self, text, color=None):
        self.st_lbl.configure(text=text, text_color=color or DIM)

    def update_stats(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            dsk = psutil.disk_usage("C:/")
            bat = psutil.sensors_battery()
            self.cpu_w[0].configure(text=f"{cpu}%")
            self.cpu_w[1].set(cpu/100)
            self.ram_w[0].configure(text=f"{ram.percent}%")
            self.ram_w[1].set(ram.percent/100)
            self.dsk_w[0].configure(text=f"{dsk.percent}%")
            self.dsk_w[1].set(dsk.percent/100)
            if bat:
                self.bat_w[0].configure(text=f"{bat.percent}%")
                self.bat_w[1].set(bat.percent/100)
        except:
            pass
        self.root.after(3000, self.update_stats)

    def update_time(self):
        now = datetime.datetime.now()
        self.time_lbl.configure(text=now.strftime("%a %b %d  |  %I:%M:%S %p"))
        self.root.after(1000, self.update_time)

    def change_photo(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(title="Select Profile Photo",
            filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            try:
                dest = Path.home() / ".hexa-agent"
                dest.mkdir(exist_ok=True)
                Image.open(path).convert("RGB").resize((80,80)).save(dest / "profile.png")
                self.add_log("Profile photo updated. Restart to see changes.", "s")
            except Exception as e:
                self.add_log(f"Could not update photo: {e}", "e")

    def start_listening(self):
        if self.is_listening:
            return
        self.is_listening = True
        self.mic_dot.configure(text="ACTIVE", text_color=GREEN)
        self.ag_lbl.configure(text="LISTENING...", text_color=BLUE)
        self.set_status("Listening for voice commands...", BLUE)
        self.add_log("Voice listening started.", "i")
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def stop_listening(self):
        self.is_listening = False
        self.mic_dot.configure(text="INACTIVE", text_color=RED)
        self.ag_lbl.configure(text="HEXA READY", text_color=GREEN)
        self.set_status("Ready", DIM)
        self.add_log("Voice listening stopped.", "w")

    def listen_loop(self):
        from voice.speech_to_text import transcribe
        from voice.text_to_speech import speak
        from agent.langgraph_brain import process_command
        from memory.memory_manager import save_command
        while self.is_listening:
            try:
                text = transcribe()
                if not text or len(text.strip()) < 3:
                    continue
                self.add_log(f"You said: {text}", "u")
                if "stop agent" in text.lower():
                    self.stop_listening()
                    break
                self.set_status("Processing...", YELLOW)
                result = process_command(text)
                save_command(text, result)
                self.command_count += 1
                self.cnt_lbl.configure(text=str(self.command_count))
                self.add_log(f"Hexa: {result}", "s")
                self.set_status("Done", GREEN)
                speak(result)
            except Exception as e:
                self.add_log(f"Error: {e}", "e")

    def exec_typed(self):
        cmd = self.cmd_in.get().strip()
        if not cmd:
            return
        self.cmd_in.delete(0, "end")
        self.add_log(f"Typed: {cmd}", "u")
        threading.Thread(target=self.run_cmd, args=(cmd,), daemon=True).start()

    def run_cmd(self, cmd):
        try:
            from agent.langgraph_brain import process_command
            from voice.text_to_speech import speak
            from memory.memory_manager import save_command
            self.set_status("Processing...", YELLOW)
            result = process_command(cmd)
            save_command(cmd, result)
            self.command_count += 1
            self.cnt_lbl.configure(text=str(self.command_count))
            self.add_log(f"Hexa: {result}", "s")
            self.set_status("Done", GREEN)
            speak(result)
        except Exception as e:
            self.add_log(f"Error: {e}", "e")
            self.set_status("Error", RED)

    def clear(self):
        self.log_widget.configure(state="normal")
        self.log_widget.delete("1.0", "end")
        self.log_widget.configure(state="disabled")
        self.add_log("Logs cleared.", "i")

    def run(self):
        self.root.mainloop()

def launch_dashboard():
    app = HexaDashboard()
    app.run()

if __name__ == "__main__":
    launch_dashboard()
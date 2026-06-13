import customtkinter as ctk
import threading
import psutil
import datetime
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#06060f"
BG2 = "#0c0c1e"
BG3 = "#0d1117"
BG4 = "#080816"
BORDER = "#1e1e3a"
GREEN = "#00e676"
RED = "#f44336"
BLUE = "#42a5f5"
YELLOW = "#ffa726"
PURPLE = "#ab47bc"
TEXT = "#546e7a"
DIM = "#263238"
WHITE = "#ffffff"
ACCENT = "#1565c0"

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
                img = Image.new("RGB", (80, 80), "#0d1b2a")
                draw = ImageDraw.Draw(img)
                draw.ellipse([2, 2, 78, 78], fill="#0d47a1")
                draw.text((24, 20), "H", fill="#90caf9")
            mask = Image.new("L", (80, 80), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, 80, 80], fill=255)
            out = Image.new("RGBA", (80, 80), (0,0,0,0))
            out.paste(img, mask=mask)
            return out
        except:
            return None

    def setup_ui(self):
        hdr = ctk.CTkFrame(self.root, height=65, corner_radius=0, fg_color=BG2)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        try:
            av = self.get_avatar()
            if av:
                av_ctk = ctk.CTkImage(av, size=(40, 40))
                ctk.CTkLabel(hdr, image=av_ctk, text="").pack(side="left", padx=(14,8), pady=12)
        except:
            pass

        brand = ctk.CTkFrame(hdr, fg_color="transparent")
        brand.pack(side="left", pady=12)
        ctk.CTkLabel(brand, text="HEXA", font=ctk.CTkFont(size=19, weight="bold"), text_color=BLUE).pack(anchor="w")
        ctk.CTkLabel(brand, text="AI DESKTOP ASSISTANT", font=ctk.CTkFont(size=8), text_color=DIM).pack(anchor="w")

        pills = ctk.CTkFrame(hdr, fg_color="transparent")
        pills.pack(side="right", padx=12)

        ctk.CTkButton(pills, text="Photo", width=75, height=28, corner_radius=20,
            font=ctk.CTkFont(size=10), fg_color=BG3, hover_color="#1a2a3a",
            border_color=BORDER, border_width=1, text_color=TEXT,
            command=self.change_photo).pack(side="right", padx=4)

        self.time_lbl = ctk.CTkLabel(pills, text="", font=ctk.CTkFont(size=11),
            text_color=TEXT, fg_color=BG3, corner_radius=20, padx=10)
        self.time_lbl.pack(side="right", padx=4)

        body = ctk.CTkFrame(self.root, fg_color="transparent")
        body.pack(fill="both", expand=True)

        sb = ctk.CTkFrame(body, width=205, corner_radius=0, fg_color=BG4)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        ctk.CTkFrame(sb, width=1, fg_color=BORDER).pack(side="right", fill="y")

        sb_inner = ctk.CTkFrame(sb, fg_color="transparent")
        sb_inner.pack(fill="both", expand=True, padx=12, pady=12)

        mic_card = ctk.CTkFrame(sb_inner, corner_radius=10, fg_color=BG3,
            border_color=BORDER, border_width=1)
        mic_card.pack(fill="x", pady=(0,8))

        ctk.CTkLabel(mic_card, text="MICROPHONE", font=ctk.CTkFont(size=8),
            text_color=DIM).pack(anchor="w", padx=10, pady=(8,4))

        mic_row = ctk.CTkFrame(mic_card, fg_color="transparent")
        mic_row.pack(fill="x", padx=10, pady=(0,8))

        self.mic_dot = ctk.CTkLabel(mic_row, text="", width=8, height=8,
            corner_radius=4, fg_color=RED)
        self.mic_dot.pack(side="left")

        self.mic_text = ctk.CTkLabel(mic_row, text=" Inactive",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=RED)
        self.mic_text.pack(side="left")

        ctk.CTkButton(sb_inner, text="Start listening", height=42, corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0a2a1a", hover_color="#0f3a22",
            border_color=GREEN, border_width=1, text_color=GREEN,
            command=self.start_listening).pack(fill="x", pady=3)

        ctk.CTkButton(sb_inner, text="Stop listening", height=42, corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2a0a0a", hover_color="#3a0f0f",
            border_color=RED, border_width=1, text_color=RED,
            command=self.stop_listening).pack(fill="x", pady=3)

        ctk.CTkFrame(sb_inner, height=1, fg_color=BORDER).pack(fill="x", pady=8)
        ctk.CTkLabel(sb_inner, text="QUICK COMMANDS", font=ctk.CTkFont(size=8),
            text_color=DIM).pack(anchor="w", pady=(0,4))

        for label, cmd in [
            ("Chrome", "open chrome"),
            ("VS Code", "open vs code"),
            ("Files", "open file manager"),
            ("Screenshot", "take screenshot"),
            ("Volume up", "increase volume"),
            ("Mute", "mute volume"),
            ("YouTube", "open youtube"),
            ("Battery", "check battery"),
        ]:
            ctk.CTkButton(sb_inner, text=label, height=32, corner_radius=7,
                font=ctk.CTkFont(size=11), fg_color=BG3, hover_color="#0d1b2a",
                border_color=BORDER, border_width=1, anchor="w", text_color=TEXT,
                command=lambda c=cmd: self.run_cmd(c)).pack(fill="x", pady=2)

        ctr = ctk.CTkFrame(body, corner_radius=0, fg_color=BG)
        ctr.pack(side="left", fill="both", expand=True)

        lh = ctk.CTkFrame(ctr, fg_color="transparent")
        lh.pack(fill="x", padx=14, pady=(10,4))
        ctk.CTkLabel(lh, text="COMMAND HISTORY", font=ctk.CTkFont(size=8),
            text_color=DIM).pack(side="left")
        ctk.CTkButton(lh, text="Clear", width=50, height=22, corner_radius=5,
            font=ctk.CTkFont(size=10), fg_color=BG3, hover_color="#0d1b2a",
            border_color=BORDER, border_width=1, text_color=DIM,
            command=self.clear).pack(side="right")

        log_wrap = tk.Frame(ctr, bg="#030309", highlightthickness=1,
            highlightbackground=BORDER)
        log_wrap.pack(fill="both", expand=True, padx=12, pady=(0,6))

        self.log_widget = tk.Text(log_wrap, bg="#030309", fg=TEXT,
            font=("Consolas", 11), bd=0, relief="flat", wrap="word",
            state="disabled", cursor="arrow", selectbackground="#1e1e3a")
        self.log_widget.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        scroll = tk.Scrollbar(log_wrap, command=self.log_widget.yview,
            bg=BG3, troughcolor=BG)
        scroll.pack(side="right", fill="y")
        self.log_widget.configure(yscrollcommand=scroll.set)

        self.log_widget.tag_configure("s", foreground=GREEN)
        self.log_widget.tag_configure("e", foreground=RED)
        self.log_widget.tag_configure("i", foreground=BLUE)
        self.log_widget.tag_configure("w", foreground=YELLOW)
        self.log_widget.tag_configure("u", foreground=WHITE)
        self.log_widget.tag_configure("t", foreground=DIM)
        self.log_widget.tag_configure("n", foreground=TEXT)

        inp = ctk.CTkFrame(ctr, fg_color=BG3, corner_radius=10,
            border_color=BORDER, border_width=1)
        inp.pack(fill="x", padx=12, pady=(0,10))

        ctk.CTkLabel(inp, text="Type a command...", font=ctk.CTkFont(size=12),
            text_color=DIM).pack(side="left", padx=10)

        self.cmd_in = ctk.CTkEntry(inp, placeholder_text="",
            border_width=0, fg_color="transparent",
            font=ctk.CTkFont(size=12), text_color=WHITE)
        self.cmd_in.pack(side="left", fill="x", expand=True, pady=8)
        self.cmd_in.bind("<Return>", lambda e: self.exec_typed())

        ctk.CTkButton(inp, text="Run", width=65, height=28, corner_radius=7,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0d2855", hover_color="#1a3a6e",
            border_color=ACCENT, border_width=1, text_color=BLUE,
            command=self.exec_typed).pack(side="right", padx=8, pady=6)

        rt = ctk.CTkFrame(body, width=185, corner_radius=0, fg_color=BG4)
        rt.pack(side="right", fill="y")
        rt.pack_propagate(False)

        ctk.CTkFrame(rt, width=1, fg_color=BORDER).pack(side="left", fill="y")

        rt_inner = ctk.CTkFrame(rt, fg_color="transparent")
        rt_inner.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(rt_inner, text="SYSTEM STATS", font=ctk.CTkFont(size=8),
            text_color=DIM).pack(anchor="w", pady=(0,6))

        self.cpu_w = self.mk_stat(rt_inner, "CPU", BLUE)
        self.ram_w = self.mk_stat(rt_inner, "RAM", PURPLE)
        self.dsk_w = self.mk_stat(rt_inner, "Disk", YELLOW)
        self.bat_w = self.mk_stat(rt_inner, "Battery", GREEN)

        ctk.CTkFrame(rt_inner, height=1, fg_color=BORDER).pack(fill="x", pady=8)
        ctk.CTkLabel(rt_inner, text="COMMANDS RUN", font=ctk.CTkFont(size=8),
            text_color=DIM).pack()
        self.cnt_lbl = ctk.CTkLabel(rt_inner, text="0",
            font=ctk.CTkFont(size=34, weight="bold"), text_color=BLUE)
        self.cnt_lbl.pack()
        ctk.CTkFrame(rt_inner, height=1, fg_color=BORDER).pack(fill="x", pady=8)
        self.ag_lbl = ctk.CTkLabel(rt_inner, text="HEXA READY",
            font=ctk.CTkFont(size=11, weight="bold"), text_color=GREEN)
        self.ag_lbl.pack()

        sbar = ctk.CTkFrame(self.root, height=26, corner_radius=0, fg_color="#030309")
        sbar.pack(fill="x", side="bottom")
        sbar.pack_propagate(False)
        self.st_lbl = ctk.CTkLabel(sbar, text="Ready",
            font=ctk.CTkFont(size=10), text_color=DIM)
        self.st_lbl.pack(side="left", padx=14, pady=4)
        ctk.CTkLabel(sbar, text="Hexa v1.0.2  |  AI Desktop Assistant",
            font=ctk.CTkFont(size=10), text_color="#1e1e3a").pack(side="right", padx=14, pady=4)

        self.add_log("Hexa dashboard loaded successfully.", "s")
        self.add_log("Click start listening or type a command.", "i")

    def mk_stat(self, parent, title, color):
        card = ctk.CTkFrame(parent, corner_radius=8, fg_color=BG3,
            border_color=BORDER, border_width=1)
        card.pack(fill="x", pady=3)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=(6,2))
        ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=10),
            text_color=DIM).pack(side="left")
        val = ctk.CTkLabel(row, text="0%",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=color)
        val.pack(side="right")
        bar = ctk.CTkProgressBar(card, height=4, corner_radius=2, progress_color=color)
        bar.pack(fill="x", padx=10, pady=(0,6))
        bar.set(0)
        return val, bar

    def add_log(self, msg, tag="n"):
        ts = datetime.datetime.now().strftime("%H:%M")
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
        self.time_lbl.configure(text=now.strftime("%I:%M:%S %p"))
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
        self.mic_dot.configure(fg_color=GREEN)
        self.mic_text.configure(text=" Active", text_color=GREEN)
        self.ag_lbl.configure(text="LISTENING...", text_color=BLUE)
        self.set_status("Listening for voice commands...", BLUE)
        self.add_log("Voice listening started.", "i")
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def stop_listening(self):
        self.is_listening = False
        self.mic_dot.configure(fg_color=RED)
        self.mic_text.configure(text=" Inactive", text_color=RED)
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
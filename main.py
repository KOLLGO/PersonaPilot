import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
from tkfontawesome import icon_to_image
import os
import pyperclip
import csv
from gen import *


class Tooltip:  # info on hover over elements
    def __init__(self, widget, text):  # init, hidden
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):  # hover, shown
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20  # positioning
        y = self.widget.winfo_rooty() + 20
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(  # styling
            self.tip,
            text=self.text,
            justify="left",
            background="#222",
            foreground="white",
            highlightthickness=1,
            highlightcolor="white",
            padx=6,
            pady=4,
            font=("Segoe UI", 10),
        )
        label.pack()

    def hide(self, _=None):  # leave, hide
        if self.tip:
            self.tip.destroy()
            self.tip = None


class PersonaManager:
    def __init__(self, root):  # init main window
        # window setup
        self.root = root
        icon = tk.PhotoImage(file="./assets/icon.png")
        self.root.iconphoto(True, icon)
        self.root.title("Persona Pilot")
        self.root.state("zoomed")

        # tab setup
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self.add_new_tab_button()
        self.notebook.bind("<Button-2>", self.on_tab_close)  # close on MMB

        # theme
        style = Style()
        style.theme_use("darkly")
        bg = style.lookup("TFrame", "background")
        fg = style.lookup("TLabel", "foreground")
        card_bg = style.lookup("TLabelframe", "background")
        card_fg = style.lookup("TLabelframe.Label", "foreground")
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 14))
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 14))
        style.configure("TFrame", background=bg, relief="flat")
        style.configure("Card.TFrame", background=card_bg, relief="flat", borderwidth=1)
        style.configure(
            "TLabelframe",
            background=card_bg,
            foreground=fg,
            relief="flat",
            borderwidth=1,
            font=("Segoe UI", 14, "bold"),
        )
        style.configure("TLabelframe.Label", background=card_bg, foreground=card_fg)
        style.configure("Modern.TButton", font=("Segoe UI", 14))
        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 14),
            foreground="#ffffff",
            background="#6c757d",
            bordercolor="#6c757d",
        )

    def add_new_tab_button(self):  # add "+" tab
        new_tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(new_tab_frame, text=" + ")
        self.notebook.bind(
            "<<NotebookTabChanged>>", self.on_tab_changed
        )  # bind tab change logic to on_tab_changed

    def on_tab_changed(self, event):
        selected_tab = event.widget.select()  # get selected tab
        tab_text = event.widget.tab(selected_tab, "text")  # get tab text
        if tab_text.strip() == "+":  # add tab logic
            self.add_start_tab()
            self.notebook.select(len(self.notebook.tabs()) - 2)

    def on_tab_close(self, event):  # tab close logic
        clicked_tab = self.notebook.tk.call(
            self.notebook._w, "identify", "tab", event.x, event.y
        )  # identify clicked tab
        if clicked_tab != "":  # if tab clicked
            tab_index = int(clicked_tab)
            tab_text = self.notebook.tab(tab_index, "text")
            if tab_text.strip() != "+":  # exclude "+" tab from closing
                if len(self.notebook.tabs()) > 2:  # >= 1 tab
                    self.notebook.forget(tab_index)  # close tab

    def add_start_tab(self):  # add start tab
        tab_frame = ttk.Frame(self.notebook, style="TFrame")
        num_tabs = len(self.notebook.tabs())
        if num_tabs > 0:  # insert before "+" tab
            tab_index = num_tabs - 1
            tab_name = "Neuer Tab"
            self.notebook.insert(tab_index, tab_frame, text=tab_name)
        else:  # first tab
            tab_name = "Neuer Tab"
            self.notebook.add(tab_frame, text=tab_name)
        self.create_start_screen(tab_frame)

    def create_start_screen(self, parent):

        # center
        container_outer = ttk.Frame(parent, style="TFrame")
        container_outer.pack(fill="both", expand=True)
        container = ttk.Frame(container_outer, style="TFrame")
        container.place(relx=0.5, rely=0.5, anchor="center")
        logo_frame = ttk.Frame(container, style="TFrame", height=80)
        logo_frame.pack(pady=(0, 20))

        # h1
        title_label = ttk.Label(container, text="PERSONA PILOT", style="Title.TLabel")
        title_label.pack(pady=(0, 10))

        subtitle_label = ttk.Label(
            container,
            text="Erstellen und verwalten Sie Ihre Personas",
            style="Subtitle.TLabel",
        )
        subtitle_label.pack(pady=(0, 50))

        # button container
        button_frame = ttk.Frame(container, style="TFrame")
        button_frame.pack()

        # create
        plus_icon = icon_to_image("plus", fill="white", scale_to_width=18)
        create_btn = ttk.Button(
            button_frame,
            text="Persona erstellen",
            image=plus_icon,
            compound="left",
            command=lambda: self.show_persona_type_selection(
                parent
            ),  # call type selection
            style="Modern.TButton",
            width=20,
        )
        create_btn.image = plus_icon
        create_btn.pack(side="left", padx=10)

        # load
        folder_icon = icon_to_image("folder-open", fill="white", scale_to_width=18)
        load_btn = ttk.Button(
            button_frame,
            text="Persona laden",
            image=folder_icon,
            compound="left",
            command=lambda: self.open_load_persona(parent),  # call csv import
            style="Modern.TButton",
            width=20,
        )
        load_btn.image = folder_icon
        load_btn.pack(side="left", padx=10)

    def show_persona_type_selection(self, parent):  # type selection
        # clear screen
        for widget in parent.winfo_children():
            widget.destroy()

        # parent container
        container = ttk.Frame(parent, style="TFrame")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # h1
        title_label = ttk.Label(
            container, text="Persona-Typ wählen", style="Title.TLabel"
        )
        title_label.pack(pady=(0, 30))

        # selection frame
        selection_frame = ttk.Frame(container, style="TFrame")
        selection_frame.pack(pady=20)

        # professional
        prof_frame = ttk.Frame(selection_frame, style="Card.TFrame", padding=30)
        prof_frame.pack(side="left", padx=20)

        tie_icon = icon_to_image("user-tie", fill="white", scale_to_width=18)

        prof_btn = ttk.Button(
            prof_frame,
            text="Professionell",
            command=lambda: self.open_create_persona(parent, "professional"),
            style="Modern.TButton",
            image=tie_icon,
            compound="left",
            width=15,
        )
        prof_btn.pack()
        prof_btn.image = tie_icon

        # personal
        pers_frame = ttk.Frame(selection_frame, style="Card.TFrame", padding=30)
        pers_frame.pack(side="left", padx=20)

        user_icon = icon_to_image("user", fill="white", scale_to_width=18)

        pers_btn = ttk.Button(
            pers_frame,
            text="Persönlich",
            command=lambda: self.open_create_persona(parent, "personal"),
            style="Modern.TButton",
            image=user_icon,
            compound="left",
            width=15,
        )
        pers_btn.pack()
        pers_btn.image = user_icon

        # back btn
        arrow_icon = icon_to_image("arrow-left", fill="white", scale_to_width=18)
        back_btn = ttk.Button(
            container,
            text="Zurück",
            image=arrow_icon,
            compound="left",
            command=lambda: self.create_start_screen(parent),
            style="Secondary.TButton",
        )
        back_btn.image = arrow_icon
        back_btn.pack(pady=30)

    def open_create_persona(
        self, parent, persona_type="professional", loaded_data=None
    ):
        for widget in parent.winfo_children():
            widget.destroy()

        # initialize fields storage
        self.fields = {}

        # main container
        main_container = ttk.Frame(parent, style="TFrame")
        main_container.pack(fill="both", expand=True)

        # header
        header_frame = ttk.Frame(main_container, style="Card.TFrame")
        header_frame.pack(fill="x", padx=0, pady=(0, 10), side="top")

        header_content = ttk.Frame(header_frame, style="Card.TFrame")
        header_content.pack(fill="x", pady=15, padx=30)

        # title
        title_text = (
            "Professionelle Persona"
            if persona_type == "professional"
            else "Persönliche Persona"
        )
        title_label = ttk.Label(
            header_content, text=title_text, font=("Segoe UI", 18, "bold")
        )
        title_label.pack(side="left")

        # save btn
        save_icon = icon_to_image("save", fill="white", scale_to_width=18)
        save_all_btn = ttk.Button(
            header_content,
            text="Als CSV speichern",
            image=save_icon,
            compound="left",
            command=self.save_persona_to_csv,
            style="Modern.TButton",
        )
        save_all_btn.image = save_icon
        save_all_btn.pack(side="left", padx=10)

        # clip btn
        clipboard_icon = icon_to_image("clipboard", fill="white", scale_to_width=18)
        copy_btn = ttk.Button(
            header_content,
            text="AI Kontext",
            image=clipboard_icon,
            compound="left",
            command=lambda: self.copy_AI_context(persona_type),
            style="Modern.TButton",
        )
        copy_btn.image = clipboard_icon
        copy_btn.pack(side="left", padx=10)

        # back btn
        arrow_icon = icon_to_image("arrow-left", fill="white", scale_to_width=18)
        back_btn = ttk.Button(
            header_content,
            text="Zurück",
            image=arrow_icon,
            compound="left",
            command=lambda: self.show_persona_type_selection(parent),
            style="Secondary.TButton",
        )
        back_btn.image = arrow_icon
        back_btn.pack(side="right", padx=(20, 0))

        # scrollable container
        canvas = tk.Canvas(main_container, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            main_container, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # columns
        content_frame = ttk.Frame(scrollable_frame, style="TFrame")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        left_column = ttk.Frame(content_frame, style="TFrame")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_column = ttk.Frame(content_frame, style="TFrame")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # MBTI + DA frame
        traits_frame = ttk.LabelFrame(
            right_column,
            text="Persönlichkeitsmerkmale",
            padding=12,
            style="TLabelframe",
        )
        traits_frame.pack(fill="x", pady=(0, 10))

        # DA slider
        da_default = 0.5
        if loaded_data and "Digitalaffinität" in loaded_data:
            try:
                da_default = float(loaded_data["Digitalaffinität"])
            except:
                da_default = 0.5
        da_var = tk.DoubleVar(value=da_default)
        da_label = ttk.Label(traits_frame, text=f"Digitalaffinität: {da_var.get():.1f}")
        da_label.pack(anchor="w")
        da_scale = ttk.Scale(
            traits_frame,
            from_=0.1,
            to=1.0,
            orient="horizontal",
            variable=da_var,
            command=lambda e: da_label.configure(
                text=f"Digitalaffinität: {float(da_var.get()):.1f}"
            ),
        )
        da_scale.pack(fill="x", pady=4)
        self.fields["Digitalaffinität"] = {
            "entry": da_var,
            "saved_value": "",
            "is_saved": False,
            "width_type": "trait",
        }

        # extroversion slider
        ex_default = 0.5
        if loaded_data and "Extroversion" in loaded_data:
            try:
                ex_default = float(loaded_data["Extroversion"])
            except:
                ex_default = 0.5
        ext_var = tk.DoubleVar(value=ex_default)
        ext_label = ttk.Label(traits_frame, text=f"Extroversion: {ext_var.get():.1f}")
        ext_label.pack(anchor="w", pady=(8, 0))
        ext_scale = ttk.Scale(
            traits_frame,
            from_=0.1,
            to=1.0,
            orient="horizontal",
            variable=ext_var,
            command=lambda e: ext_label.configure(
                text=f"Extroversion: {float(ext_var.get()):.1f}"
            ),
        )
        ext_scale.pack(fill="x", pady=4)
        self.fields["Extroversion"] = {
            "entry": ext_var,
            "saved_value": "",
            "is_saved": False,
            "width_type": "trait",
        }

        # perception switch
        perc_var = tk.StringVar(
            value=(
                loaded_data.get("Wahrnehmung")
                if loaded_data and "Wahrnehmung" in loaded_data
                else "Intuition"
            )
        )
        perc_frame = ttk.Frame(traits_frame)
        perc_frame.pack(fill="x", pady=(8, 0))
        ttk.Label(perc_frame, text="Wahrnehmung:").pack(side="left")
        ttk.Radiobutton(
            perc_frame, text="Intuition", value="Intuition", variable=perc_var
        ).pack(side="left", padx=6)
        ttk.Radiobutton(
            perc_frame, text="Sensorik", value="Sensorik", variable=perc_var
        ).pack(side="left", padx=6)
        Tooltip(
            perc_frame,
            "Intuition: basierend auf internen Quellen wie Bauchgefühl\nSensorik: basierend auf externen Quellen wie Sinnen",
        )  # tooltip info
        self.fields["Wahrnehmung"] = {
            "entry": perc_var,
            "saved_value": "",
            "is_saved": False,
            "width_type": "trait",
        }

        # information switch
        info_var = tk.StringVar(
            value=(
                loaded_data.get("Informationsverarbeitung")
                if loaded_data and "Informationsverarbeitung" in loaded_data
                else "Denken"
            )
        )
        info_frame = ttk.Frame(traits_frame)
        info_frame.pack(fill="x", pady=(6, 0))
        ttk.Label(info_frame, text="Informationsverarbeitung:").pack(side="left")
        ttk.Radiobutton(
            info_frame, text="Denken", value="Denken", variable=info_var
        ).pack(side="left", padx=6)
        ttk.Radiobutton(
            info_frame, text="Fühlen", value="Fühlen", variable=info_var
        ).pack(side="left", padx=6)
        Tooltip(
            info_frame,
            "Denken: rationales, logisches Denken\nFühlen: basierend auf Emotionen",
        )  # tooltip info
        self.fields["Informationsverarbeitung"] = {
            "entry": info_var,
            "saved_value": "",
            "is_saved": False,
            "width_type": "trait",
        }

        # lifestyle switch
        life_var = tk.StringVar(
            value=(
                loaded_data.get("Lebensstil")
                if loaded_data and "Lebensstil" in loaded_data
                else "Wahrnehmung"
            )
        )
        life_frame = ttk.Frame(traits_frame)
        life_frame.pack(fill="x", pady=(6, 0))
        ttk.Label(life_frame, text="Lebensstil:").pack(side="left")
        ttk.Radiobutton(
            life_frame, text="Wahrnehmung", value="Wahrnehmung", variable=life_var
        ).pack(side="left", padx=6)
        ttk.Radiobutton(
            life_frame, text="Beurteilung", value="Beurteilung", variable=life_var
        ).pack(side="left", padx=6)
        Tooltip(
            life_frame, "Wahrnehmung: explorativ\nBeurteilung: erfahrungsbasiert"
        )  # tooltip info
        self.fields["Lebensstil"] = {
            "entry": life_var,
            "saved_value": "",
            "is_saved": False,
            "width_type": "trait",
        }

        # full width (in layout) fields container
        full_width_frame = ttk.Frame(content_frame, style="TFrame")
        full_width_frame.pack(side="bottom", fill="x", pady=(20, 0), padx=(10, 0))

        # field definitions + placeholders
        if persona_type == "professional":  # professional persona
            field_definitions = [
                ("Name", "Max Mustermann", left_column, "normal"),
                ("Alter", "30", left_column, "normal"),
                ("Geschlecht", "Männlich", left_column, "normal"),
                ("Geburtsort", "Musterstadt", left_column, "normal"),
                ("Wohnort", "Musterstadt", left_column, "normal"),
                ("Familienstand", "Verheiratet", left_column, "normal"),
                ("Position", "Softwareentwickler", left_column, "normal"),
                ("Lebenslauf", "Lebenslauf", right_column, "wide"),
                ("Fähigkeiten", "Python, Java, C++", right_column, "wide"),
                ("Ziele", "Karrierefortschritt", right_column, "wide"),
                (
                    "Persönliche Stärken",
                    "Teamarbeit, Problemlösung",
                    right_column,
                    "wide",
                ),
                ("Persönliche Schwächen", "Ungeduld", right_column, "wide"),
                ("Softskills", "Kommunikation, Führung", right_column, "wide"),
                ("Hobbies", "Lesen, Reisen", right_column, "wide"),
                ("Notizen", "Notizen", right_column, "wide"),
            ]
        else:  # personal
            field_definitions = [
                ("Name", "Max Mustermann", left_column, "normal"),
                ("Nutzername", "maxmustermann", left_column, "normal"),
                ("Alter", "30", left_column, "normal"),
                ("Geschlecht", "Männlich", left_column, "normal"),
                ("Geburtsort", "Musterstadt", left_column, "normal"),
                ("Wohnort", "Musterstadt", left_column, "normal"),
                ("Wohnsituation", "Eigenheim", left_column, "normal"),
                ("Familienstand", "Verheiratet", left_column, "normal"),
                ("Beruf", "Softwareentwickler", left_column, "normal"),
                ("Bildungsstand", "Masterabschluss", left_column, "normal"),
                ("Ziele", "Finanzielle Sicherheit", right_column, "wide"),
                (
                    "Persönliche Stärken",
                    "Disziplin, Organisation",
                    right_column,
                    "wide",
                ),
                ("Persönliche Schwächen", "Perfektionismus", right_column, "wide"),
                (
                    "Charaktereigenschaften",
                    "Zuverlässig, Kreativ",
                    right_column,
                    "wide",
                ),
                ("Werte", "Ehrlichkeit, Loyalität", right_column, "wide"),
                ("Lebensstil", "Aktiv, Sozial", right_column, "wide"),
                ("Hobbies", "Lesen, Reisen", right_column, "wide"),
                ("Interessen", "Technologie, Musik", right_column, "wide"),
                ("Mediennutzung", "Soziale Medien, Podcasts", right_column, "wide"),
                (
                    "Konsumverhalten",
                    "Online-Shopping, Qualitätsbewusst",
                    right_column,
                    "wide",
                ),
                ("Lebensziele", "Familie gründen, Weltreise", right_column, "wide"),
                (
                    "Hintergrundgeschichte",
                    "Hintergrundgeschichte",
                    right_column,
                    "wide",
                ),
                ("Notizen", "Notizen", right_column, "wide"),
            ]

        for field_name, placeholder, column, width_type in field_definitions:
            initial_value = (
                loaded_data.get(field_name, placeholder) if loaded_data else placeholder
            )  # if loaded data exists: use, else: placeholder

            if width_type == "wide":  # more text space
                self.create_field(
                    full_width_frame, field_name, initial_value, width_type
                )
            else:  # normal field
                self.create_field(column, field_name, initial_value, width_type)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # update tab title to loaded name
        if loaded_data and "Name" in loaded_data:
            self.update_tab_title_with_name(loaded_data["Name"])

        # mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_field(
        self, parent, field_name, placeholder, width_type="normal"
    ):  # create input field logic
        field_frame = ttk.LabelFrame(
            parent, text=field_name, padding=15, style="TLabelframe"
        )  # container for field
        field_frame.pack(pady=10, fill="x")
        input_container = ttk.Frame(field_frame, style="TFrame")  # container for input
        input_container.pack(fill="x")
        if width_type == "wide":  # more text space
            entry = tk.Text(
                input_container, font=("Segoe UI", 11), height=4, wrap="word"
            )
            entry.insert("1.0", placeholder)
            entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        else:  # normal field
            entry = ttk.Entry(input_container, font=("Segoe UI", 11), style="TEntry")
            entry.insert(0, placeholder)
            entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # field data storage
        self.fields[field_name] = {
            "entry": entry,
            "saved_value": "",
            "is_saved": False,
            "width_type": width_type,
        }
        # button container
        button_container = ttk.Frame(input_container, style="TFrame")
        button_container.pack(side="right")
        save_icon = icon_to_image("save", fill="white", scale_to_width=16)
        edit_icon = icon_to_image("pen", fill="white", scale_to_width=19)
        refresh_icon = icon_to_image("sync", fill="white", scale_to_width=19)

        save_edit_btn = ttk.Button(
            button_container,
            text="Speichern",
            image=save_icon,
            compound="left",
            width=13,
        )  # save button
        save_edit_btn.image = save_icon
        save_edit_btn.pack(side="left", padx=2)

        def toggle_save_edit():  # save/edit toggle switch logic
            field_data = self.fields[field_name]  # get field data
            if field_data["is_saved"]:  # currently saved -> switch to edit
                if width_type == "wide":  # wide field
                    field_data["entry"].configure(state="normal")
                else:  # normal field
                    field_data["entry"].configure(state="normal")
                save_edit_btn.configure(text="Speichern", image=save_icon)
                save_edit_btn.image = save_icon
                field_data["is_saved"] = False
            else:  # currently editing -> switch to saved
                if width_type == "wide":  # wide field
                    field_data["saved_value"] = field_data["entry"].get("1.0", "end-1c")
                    field_data["entry"].configure(state="disabled")
                else:  # normal field
                    field_data["saved_value"] = field_data["entry"].get()
                    field_data["entry"].configure(state="readonly")
                save_edit_btn.configure(text="", image=edit_icon)
                save_edit_btn.image = edit_icon
                field_data["is_saved"] = True
                if field_name == "Name":  # update tab title on saved name
                    self.update_tab_title_with_name(field_data["saved_value"])

        # bind toggle function
        save_edit_btn.configure(command=toggle_save_edit)
        # generate btn
        generate_btn = ttk.Button(
            button_container,
            text="Generieren",
            image=refresh_icon,
            compound="left",
            width=13,
        )
        generate_btn.image = refresh_icon
        generate_btn.pack(side="left", padx=2)

        def generate_field():  # bind generation functions
            self.generate_field_value(field_name)

        generate_btn.configure(command=generate_field)

    def update_tab_title_with_name(self, name):
        # locate Tab
        current_tab = self.notebook.select()
        # update title
        if current_tab:
            tab_title = name.strip() if name.strip() else "Neuer Tab"
            self.notebook.tab(current_tab, text=tab_title)

    def generate_field_value(self, field_name):  # generate field value logic
        if field_name in self.fields:  # should always be true
            field_data = self.fields[field_name]  # get field data
            width_type = field_data.get("width_type", "normal")
            # switch to edit mode if saved
            if field_data["is_saved"]:
                if width_type == "wide":
                    field_data["entry"].configure(state="normal")
                else:
                    field_data["entry"].configure(state="normal")
                field_data["is_saved"] = False
                for widget in field_data["entry"].master.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for btn in widget.winfo_children():
                            if (
                                isinstance(btn, ttk.Button)
                                and "Speichern" in btn["text"]
                            ):
                                btn.configure(text="\U0001f4be Speichern")
                                break
            generated_value = self.get_generated_value(
                field_name
            )  # call generator selection
            # insert
            if width_type == "wide":
                field_data["entry"].delete("1.0", "end")
                field_data["entry"].insert("1.0", generated_value)
            else:
                field_data["entry"].delete(0, tk.END)
                field_data["entry"].insert(0, generated_value)

    def get_generated_value(self, field_name):
        # action call from gen.py based on field name
        generators = {
            # professional
            "Position": lambda: genJob(
                round(self.fields.get("Digitalaffinität", {}).get("entry").get(), 2)
            ),
            "Lebenslauf": lambda: professionalCV(),
            "Fähigkeiten": lambda: professionalSkills(),
            "Ziele": lambda: professionalGoals(),
            "Persönliche Stärken": lambda: professionalStrengths(),
            "Persönliche Schwächen": lambda: professionalWeaknesses(),
            "Softskills": lambda: professionalSoftskills(),
            # personal
            "Nutzername": lambda: personalUsername(
                name=(
                    self.fields.get("Name", {}).get("entry").get()
                    if self.fields.get("Name")
                    else "Max Mustermann"
                )
            ),
            "Wohnsituation": lambda: personalLivingSituation(),
            "Beruf": lambda: genJob(
                round(self.fields.get("Digitalaffinität", {}).get("entry").get(), 2)
            ),
            "Bildungsstand": lambda: personalEducation(),
            "Ziele": lambda: personalGoals(),
            "Persönliche Stärken": lambda: personalStrengths(),
            "Persönliche Schwächen": lambda: personalWeaknesses(),
            "Charaktereigenschaften": lambda: personalCharacterTraits(),
            "Werte": lambda: personalValues(),
            "Lebensstil": lambda: personalLifestyle(),
            "Interessen": lambda: personalInterests(),
            "Mediennutzung": lambda: personalMediaUsage(),
            "Konsumverhalten": lambda: personalConsumptionBehavior(),
            "Lebensziele": lambda: personalLifeGoals(),
            "Hintergrundgeschichte": lambda: personalBackgroundStory(),
            # both
            "Name": lambda: genName(
                gender=(
                    self.fields.get("Geschlecht", {}).get("entry").get()
                    if self.fields.get("Geschlecht")
                    else "Männlich"
                )
            ),
            "Alter": lambda: genAge(),
            "Geschlecht": lambda: genGender(
                name=(
                    self.fields.get("Name", {}).get("entry").get()
                    if self.fields.get("Name")
                    else "Max Mustermann"
                )
            ),
            "Geburtsort": lambda: genBirthplace(),
            "Wohnort": lambda: genResidence(),
            "Familienstand": lambda: genMaritalStatus(
                age=(
                    self.fields.get("Alter", {}).get("entry").get()
                    if self.fields.get("Alter")
                    else 30
                )
            ),
            "Hobbies": lambda: genHobbies(),
        }

        if field_name in generators:  # should always be true
            return generators[field_name]()
        else:
            return "N/A"

    def open_load_persona(self, parent):
        # file selection dialog
        file_path = filedialog.askopenfilename(
            title="Persona CSV laden",
            filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")],
        )

        if not file_path:  # empty path, should never happen
            return

        try:
            # read csv
            with open(file_path, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)  # reader object
                headers = next(reader)  # key (header) row
                values = next(reader)  # value row

                loaded_data = dict(zip(headers, values))  # join keys + values

                persona_type = self.detect_persona_type(loaded_data)  # detect type

                self.open_create_persona(
                    parent, persona_type, loaded_data
                )  # open screen with loaded data
                # alert success
                messagebox.showinfo(
                    "Datei geladen",
                    f"Persona wurde erfolgreich geladen aus:\n{os.path.basename(file_path)}",
                )

        except Exception as e:  # error handling
            messagebox.showerror(
                "Fehler beim Laden", f"Die Datei konnte nicht geladen werden:\n{str(e)}"
            )

    def detect_persona_type(self, data):
        professional_fields = {
            "Position",
            "Lebenslauf",
            "Fähigkeiten",
            "Softskills",
        }  # professional exclusives
        personal_fields = {
            "Nutzername",
            "Wohnsituation",
            "Bildungsstand",
            "Charaktereigenschaften",
            "Werte",
            "Lebensstil",
            "Interessen",
            "Mediennutzung",
            "Konsumverhalten",
            "Lebensziele",
            "Hintergrundgeschichte",
        }  # personal exclusives

        data_fields = set(data.keys())  # available fields

        prof_matches = len(
            data_fields.intersection(professional_fields)
        )  # count matches
        pers_matches = len(data_fields.intersection(personal_fields))  # count matches

        return (
            "personal" if pers_matches > prof_matches else "professional"
        )  # decide type

    def copy_AI_context(self, persona_type):
        text = ""
        if persona_type == "professional":  # fields for professional
            text += "Du bist eine Person im Berufsleben. Passe deinen  Schreibstil und deine Persönlichkeit den folgenden Angaben an und sei dabei so menschlich und natürlich wie möglich. Hier sind die Details der Persona:\n\n"
            fields_to_use = [
                "Name",
                "Alter",
                "Geschlecht",
                "Geburtsort",
                "Wohnort",
                "Familienstand",
                "Position",
                "Lebenslauf",
                "Fähigkeiten",
                "Ziele",
                "Persönliche Stärken",
                "Persönliche Schwächen",
                "Softskills",
                "Hobbies",
                "Notizen",
                "Digitalaffinität",
            ]
        else:  # fields for personal
            text += "Du bist eine Privatperson. Passe deinen  Schreibstil und deine Persönlichkeit den folgenden Angaben an und sei dabei so menschlich und natürlich wie möglich. Hier sind die Details der Persona:\n\n"
            fields_to_use = [
                "Name",
                "Nutzername",
                "Alter",
                "Geschlecht",
                "Geburtsort",
                "Wohnort",
                "Wohnsituation",
                "Familienstand",
                "Beruf",
                "Bildungsstand",
                "Ziele",
                "Persönliche Stärken",
                "Persönliche Schwächen",
                "Charaktereigenschaften",
                "Werte",
                "Lebensstil",
                "Hobbies",
                "Interessen",
                "Mediennutzung",
                "Konsumverhalten",
                "Lebensziele",
                "Hintergrundgeschichte",
                "Notizen",
                "Digitalaffinität",
            ]

        for field in fields_to_use:
            if field not in self.fields:  # should not happen
                continue
            field_data = self.fields[field]
            if field_data.get("width_type", "normal") == "wide":  # field width
                value = field_data["entry"].get("1.0", "end-1c")  # get value
            else:
                try:
                    value = field_data["entry"].get()  # get value
                except:
                    value = str(field_data.get("saved_value", ""))  # numbers to str
            text += f"{field}: {value}\n"
        text += "Persönlichkeitstyp nach MBTI: "  # parse MBTI params
        text += (
            "E"
            if self.fields.get("Extroversion", {}).get("entry").get() >= 0.5
            else "I"
        )
        text += (
            "S"
            if self.fields.get("Wahrnehmung", {}).get("entry").get() == "Sensorik"
            else "N"
        )
        text += (
            "T"
            if self.fields.get("Informationsverarbeitung", {}).get("entry").get()
            == "Denken"
            else "F"
        )
        text += (
            "J"
            if self.fields.get("Lebensstil", {}).get("entry").get() == "Beurteilung"
            else "P"
        )
        pyperclip.copy(text)  # to clipboard

    def save_persona_to_csv(self):  # serialization
        if (
            not hasattr(self, "fields") or not self.fields
        ):  # no fields, should not happen
            messagebox.showwarning(
                "Keine Daten", "Bitte erstellen Sie zuerst eine Persona."
            )
            return
        # save all non-saved
        for field_name, field_data in self.fields.items():
            if not field_data.get("is_saved", False):
                wt = field_data.get("width_type", "normal")
                entry = field_data.get("entry")
                if wt == "wide":  # entry type
                    field_data["saved_value"] = entry.get("1.0", "end-1c")
                else:
                    try:
                        field_data["saved_value"] = entry.get()  # get value
                    except:
                        field_data["saved_value"] = ""  # empty on error
        # file selection dialog
        file_path = filedialog.asksaveasfilename(
            title="Persona als CSV speichern",
            defaultextension=".csv",
            filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")],
        )
        if file_path:  # path selected
            # write csv
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)  # writer object
                # header (keys)
                headers = list(self.fields.keys())
                writer.writerow(headers)
                # values
                values = []
                for field_name in headers:
                    fd = self.fields[field_name]  # field data (width etc.)
                    sval = fd.get("saved_value")  # get saved value
                    if not sval:
                        wt = fd.get("width_type", "normal")
                        entry = fd.get("entry")
                        if wt == "wide":
                            sval = entry.get("1.0", "end-1c")
                        else:
                            try:
                                sval = entry.get()
                            except:
                                sval = ""
                    values.append(sval)
                writer.writerow(values)
            # alert success
            messagebox.showinfo(
                "Gespeichert",
                f"Persona wurde gespeichert als:\n{os.path.basename(file_path)}",
            )


def main():
    root = tk.Tk()
    app = PersonaManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()

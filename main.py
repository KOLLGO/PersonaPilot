import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
from tkfontawesome import icon_to_image 
import os
from gen import *

class PersonaManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Persona Pilot")
        self.root.state('zoomed')
        
        # Tab Container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        self.add_new_tab_button()
        # Tab-Close Binding
        self.notebook.bind('<Button-2>', self.on_tab_close)  # MMB

        # Theme
        style = Style()
        style.theme_use('darkly')
        bg = style.lookup('TFrame', 'background')
        fg = style.lookup('TLabel', 'foreground')
        card_bg = style.lookup('TLabelframe', 'background')
        card_fg = style.lookup('TLabelframe.Label', 'foreground')
        style.configure('TLabel', background=bg, foreground=fg, font=('Segoe UI', 14))
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', font=('Segoe UI', 14))
        style.configure('TFrame', background=bg, relief='flat')
        style.configure('Card.TFrame', background=card_bg, relief='flat', borderwidth=1)
        style.configure('TLabelframe', background=card_bg, foreground=fg, relief='flat', borderwidth=1, font=('Segoe UI', 14, 'bold'))
        style.configure('TLabelframe.Label', background=card_bg, foreground=card_fg)
        style.configure('Modern.TButton', font=('Segoe UI', 14))
        style.configure('Secondary.TButton', font=('Segoe UI', 14), foreground='#ffffff', background='#6c757d', bordercolor='#6c757d')

    def add_new_tab_button(self):
        new_tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(new_tab_frame, text=' + ')
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
    
    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text.strip() == '+':
            self.add_start_tab()
            self.notebook.select(len(self.notebook.tabs()) - 2)
    
    def on_tab_close(self, event):
        clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        if clicked_tab != '':
            tab_index = int(clicked_tab)
            tab_text = self.notebook.tab(tab_index, "text")
            if tab_text.strip() != '+':
                if len(self.notebook.tabs()) > 2:  # >= 1 Tab
                    self.notebook.forget(tab_index)
    
    def add_start_tab(self):
        tab_frame = ttk.Frame(self.notebook, style='TFrame')
        num_tabs = len(self.notebook.tabs())
        if num_tabs > 0:
            tab_index = num_tabs - 1
            tab_name = "Neuer Tab"
            self.notebook.insert(tab_index, tab_frame, text=tab_name)
        else:
            tab_name = "Neuer Tab"
            self.notebook.add(tab_frame, text=tab_name)
        self.create_start_screen(tab_frame)
    
    def create_start_screen(self, parent):

        # Center
        container_outer = ttk.Frame(parent, style='TFrame')
        container_outer.pack(fill='both', expand=True)
        container = ttk.Frame(container_outer, style='TFrame')
        container.place(relx=0.5, rely=0.5, anchor='center')
        logo_frame = ttk.Frame(container, style='TFrame', height=80)
        logo_frame.pack(pady=(0, 20))
        
        # H1
        title_label = ttk.Label(container, text="PERSONA PILOT", style='Title.TLabel')
        title_label.pack(pady=(0, 10))

        subtitle_label = ttk.Label(container, text="Erstellen und verwalten Sie Ihre Personas",
                                   style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 50))
        
        # Button Container
        button_frame = ttk.Frame(container, style='TFrame')
        button_frame.pack()
        
        # Create
        plus_icon = icon_to_image("plus", fill="white", scale_to_width=18)
        create_btn = ttk.Button(
            button_frame,
            text="Persona erstellen",
            image=plus_icon,
            compound="left",
            command=lambda: self.show_persona_type_selection(parent),
            style='Modern.TButton',
            width=20
        )
        create_btn.image = plus_icon
        create_btn.pack(side='left', padx=10)

        # Load
        folder_icon = icon_to_image("folder-open", fill="white", scale_to_width=18)
        load_btn = ttk.Button(
            button_frame,
            text="Persona laden",
            image=folder_icon,
            compound="left",
            command=lambda: self.open_load_persona(parent),
            style='Modern.TButton',
            width=20
        )
        load_btn.image = folder_icon
        load_btn.pack(side='left', padx=10)
    
    def show_persona_type_selection(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

        # Container
        container = ttk.Frame(parent, style='TFrame')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # H1
        title_label = ttk.Label(container, text="Persona-Typ wählen",
                                style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Container
        selection_frame = ttk.Frame(container, style='TFrame')
        selection_frame.pack(pady=20)
        
        # Professional
        prof_frame = ttk.Frame(selection_frame, style='Card.TFrame', padding=30)
        prof_frame.pack(side='left', padx=20)
        
        tie_icon = icon_to_image("user-tie", fill="white", scale_to_width=18)
        
        prof_btn = ttk.Button(prof_frame, text="Professionell",
                             command=lambda: self.open_create_persona(parent, "professional"),
                             style='Modern.TButton',
                             image=tie_icon, compound="left", width=15)
        prof_btn.pack()
        prof_btn.image = tie_icon
        
        # Personal
        pers_frame = ttk.Frame(selection_frame, style='Card.TFrame', padding=30)
        pers_frame.pack(side='left', padx=20)
        
        user_icon = icon_to_image("user", fill="white", scale_to_width=18)

        pers_btn = ttk.Button(pers_frame, text="Persönlich",
                             command=lambda: self.open_create_persona(parent, "personal"),
                             style='Modern.TButton',
                             image=user_icon, compound="left", width=15)
        pers_btn.pack()
        pers_btn.image = user_icon
        
        # Back
        arrow_icon = icon_to_image("arrow-left", fill="white", scale_to_width=18)
        back_btn = ttk.Button(
            container,
            text="Zurück",
            image=arrow_icon,
            compound="left",
            command=lambda: self.create_start_screen(parent),
            style='Secondary.TButton'
        )
        back_btn.image = arrow_icon
        back_btn.pack(pady=30)
    
    def open_create_persona(self, parent, persona_type="professional"):
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Main Container
        main_container = ttk.Frame(parent, style='TFrame')
        main_container.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(main_container, style='Card.TFrame')
        header_frame.pack(fill='x', padx=0, pady=(0, 10), side='top')
        
        header_content = ttk.Frame(header_frame, style='Card.TFrame')
        header_content.pack(fill='x', pady=15, padx=30)
        
        title_text = "Professionelle Persona" if persona_type == "professional" else "Persönliche Persona"
        title_label = ttk.Label(header_content, text=title_text,
                                font=('Segoe UI', 18, 'bold'))
        title_label.pack(side='left')
        
        save_icon = icon_to_image("save", fill="white", scale_to_width=18)
        save_all_btn = ttk.Button(
            header_content,
            text="Als CSV speichern",
            image=save_icon,
            compound="left",
            command=self.save_persona_to_csv,
            style='Modern.TButton',
        )
        save_all_btn.image = save_icon
        save_all_btn.pack(side='left', padx=10)

        arrow_icon = icon_to_image("arrow-left", fill="white", scale_to_width=18)
        back_btn = ttk.Button(
            header_content,
            text="Zurück",
            image=arrow_icon,
            compound="left",
            command=lambda: self.show_persona_type_selection(parent),
            style='Secondary.TButton'
        )
        back_btn.image = arrow_icon
        back_btn.pack(side='right', padx=(20, 0))

        # Scrollable Container
        canvas = tk.Canvas(main_container, bg='#1e1e1e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Columns
        content_frame = ttk.Frame(scrollable_frame, style='TFrame')
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        left_column = ttk.Frame(content_frame, style='TFrame')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_column = ttk.Frame(content_frame, style='TFrame')
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Type variables
        self.fields = {}
        
        if persona_type == "professional":
            field_definitions = [
                ("Name", "Max Mustermann", left_column),
                ("Example 1", "Placeholder", left_column),
                ("Example 2", "Placeholder", right_column),
            ]
        else:
            field_definitions = [
                ("Name", "Max Mustermann", left_column),
                ("Example 3", "Placeholder", left_column),
                ("Example 4", "Placeholder", right_column),
            ]
        
        for field_name, placeholder, column in field_definitions:
            self.create_field(column, field_name, placeholder)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_field(self, parent, field_name, placeholder):
        field_frame = ttk.LabelFrame(parent, text=field_name, padding=15, style='TLabelframe')
        field_frame.pack(pady=10, fill='x')
        input_container = ttk.Frame(field_frame, style='TFrame')
        input_container.pack(fill='x')
        entry = ttk.Entry(input_container, font=('Segoe UI', 11), style='TEntry')
        entry.insert(0, placeholder)
        entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.fields[field_name] = {
            'entry': entry,
            'saved_value': '',
            'is_saved': False
        }
        button_container = ttk.Frame(input_container, style='TFrame')
        button_container.pack(side='right')
        save_icon = icon_to_image("save", fill="white", scale_to_width=16)
        edit_icon = icon_to_image("pen", fill="white", scale_to_width=16)
        refresh_icon = icon_to_image("sync", fill="white", scale_to_width=16)

        save_edit_btn = ttk.Button(
            button_container,
            text="Speichern",
            image=save_icon,
            compound="left",
            width=13
        )
        save_edit_btn.image = save_icon
        save_edit_btn.pack(side='left', padx=2)

        def toggle_save_edit():
            field_data = self.fields[field_name]
            if field_data['is_saved']:
                field_data['entry'].configure(state='normal')
                save_edit_btn.configure(text="Speichern", image=save_icon)
                save_edit_btn.image = save_icon
                field_data['is_saved'] = False
            else:
                field_data['saved_value'] = field_data['entry'].get()
                field_data['entry'].configure(state='readonly')
                save_edit_btn.configure(text="Bearbeiten", image=edit_icon)
                save_edit_btn.image = edit_icon
                field_data['is_saved'] = True
                if field_name == "Name":
                    self.update_tab_title_with_name(field_data['saved_value'])

        save_edit_btn.configure(command=toggle_save_edit)

        generate_btn = ttk.Button(
            button_container,
            text="Generieren",
            image=refresh_icon,
            compound="left",
            width=13
        )
        generate_btn.image = refresh_icon
        generate_btn.pack(side='left', padx=2)

        def generate_field():
            self.generate_field_value(field_name)
        generate_btn.configure(command=generate_field)

    def update_tab_title_with_name(self, name):
        # Locate Tab
        current_tab = self.notebook.select()
        if current_tab:
            tab_title = name.strip() if name.strip() else "Neuer Tab"
            self.notebook.tab(current_tab, text=tab_title)

    def generate_field_value(self, field_name):
        if field_name in self.fields:
            field_data = self.fields[field_name]
            
            # Edit Switch
            if field_data['is_saved']:
                field_data['entry'].configure(state='normal')
                field_data['is_saved'] = False
                for widget in field_data['entry'].master.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for btn in widget.winfo_children():
                            if isinstance(btn, ttk.Button) and "Speichern" in btn['text']:
                                btn.configure(text="\U0001F4BE Speichern")
                                break
            generated_value = self.get_generated_value(field_name)
            
            # Insert
            field_data['entry'].delete(0, tk.END)
            field_data['entry'].insert(0, generated_value)
    
    def get_generated_value(self, field_name):
        # Action Call -> Field Name
        generators = {
            # Professional
            "Example 1": lambda: professionalEg1(),
            "Example 2": lambda: professionalEg2(),

            # Personal
            
            "Example 3": lambda: personalEg3(),
            "Example 4": lambda: personalEg4(),

            # Both
            "Name": lambda: genName(),
        }
        
        if field_name in generators:
            return generators[field_name]()
        else:
            return "N/A"
    
    def open_load_persona(self, parent):

        # Select Dialog
        file_path = filedialog.askopenfilename(
            title="Persona CSV laden",
            filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        )
        
        if file_path:
            messagebox.showinfo("Datei geladen", 
                              f"Persona wurde geladen aus:\n{os.path.basename(file_path)}")
            # ToDo: Deserialization logic
            self.show_persona_type_selection(parent)
    
    def save_persona_to_csv(self):
        if not hasattr(self, 'fields') or not self.fields:
            messagebox.showwarning("Keine Daten", 
                                 "Bitte erstellen Sie zuerst eine Persona.")
            return
        
        # Save All Non-Saved
        for field_name, field_data in self.fields.items():
            if not field_data['is_saved']:
                field_data['saved_value'] = field_data['entry'].get()
        
        # Save Dialog
        file_path = filedialog.asksaveasfilename(
            title="Persona als CSV speichern",
            defaultextension=".csv",
            filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        )
        
        if file_path:
            # write CSV
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Header
                writer.writerow(self.fields.keys())
                # Werte
                values = [field_data['entry'].get() for field_data in self.fields.values()]
                writer.writerow(values)
            
            messagebox.showinfo("Gespeichert", 
                              f"Persona wurde gespeichert als:\n{os.path.basename(file_path)}")

def main():
    root = tk.Tk()
    app = PersonaManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
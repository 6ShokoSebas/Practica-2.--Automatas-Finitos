import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import xml.etree.ElementTree as ET
import json

#OPERACIONES BÁSICAS
def obtener_prefijos(w):
    return list({w[:i] if w[:i] else "λ" for i in range(len(w) + 1)})

def obtener_sufijos(w):
    return list({w[i:] if w[i:] else "λ" for i in range(len(w) + 1)})

def obtener_subcadenas(w):
    return list({w[i:j] if w[i:j] else "λ" for i in range(len(w) + 1) for j in range(i, len(w) + 1)})

def obtener_positiva(alfabeto, max_longitud):
    resultado = set(alfabeto)
    actual = set(alfabeto)
    while True:
        siguiente = {s1 + s2 for s1 in actual for s2 in alfabeto if len(s1 + s2) <= max_longitud}
        if not siguiente: break
        resultado.update(siguiente)
        actual = siguiente
    return list(resultado)

def obtener_kleene(alfabeto, max_longitud):
    resultado = set(obtener_positiva(alfabeto, max_longitud))
    resultado.add("λ")
    return list(resultado)

# CLASE DEL AUTÓMATA 
class Automata:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.inicial = None
        self.aceptacion = set()
        self.transiciones = {}

    def cargar_jff(self, ruta):
        """Lee la estructura XML que usan los archivos .jff y .xml"""
        tree = ET.parse(ruta)
        root = tree.getroot()
        automaton = root.find('automaton')
        
        self.estados.clear()
        self.aceptacion.clear()
        self.transiciones.clear()
        self.alfabeto.clear()

        for state in automaton.findall('state'):
            s_id = state.get('id')
            self.estados.add(s_id)
            self.transiciones[s_id] = {}
            if state.find('initial') is not None:
                self.inicial = s_id
            if state.find('final') is not None:
                self.aceptacion.add(s_id)

        for trans in automaton.findall('transition'):
            origen = trans.find('from').text
            destino = trans.find('to').text
            simbolo_node = trans.find('read')
            simbolo = simbolo_node.text if (simbolo_node is not None and simbolo_node.text) else "λ"
            
            if simbolo != "λ":
                self.alfabeto.add(simbolo)
            self.transiciones[origen][simbolo] = destino

    def procesar_cadena(self, cadena):
        if self.inicial is None: return False, []
        estado_actual = self.inicial
        traza = [estado_actual]
        for simbolo in cadena:
            if simbolo not in self.alfabeto or simbolo not in self.transiciones.get(estado_actual, {}):
                return False, traza 
            estado_actual = self.transiciones[estado_actual][simbolo]
            traza.append(estado_actual)
        return str(estado_actual) in [str(x) for x in self.aceptacion], traza

# INTERFAZ GRÁFICA (GUI)
class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de AFD - ESCOM")
        self.root.geometry("680x600")
        self.automata = Automata()
        
        tk.Label(root, text="Simulador de Autómatas Finitos Deterministas", font=("Arial", 14, "bold")).pack(pady=10)
        
        # --- SECCIÓN ARCHIVOS Y EDICIÓN ---
        frame_archivos = tk.Frame(root)
        frame_archivos.pack(pady=5)
        tk.Button(frame_archivos, text="Crear Manualmente", command=self.editor_manual, bg="#fffacd", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_archivos, text="Cargar AFD", command=self.cargar_archivo, bg="lightblue", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_archivos, text="Exportar AFD", command=self.exportar_automata, bg="plum", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.lbl_info = tk.Label(root, text="Ningún autómata cargado.", fg="red", justify=tk.CENTER)
        self.lbl_info.pack(pady=5)

        # --- SECCIÓN VISUALIZACIÓN ---
        frame_visual = tk.Frame(root)
        frame_visual.pack(pady=5)
        tk.Button(frame_visual, text="Ver Tabla de Transiciones", command=self.mostrar_tabla, bg="#f0e68c").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_visual, text="Ver Grafo Visual", command=self.mostrar_grafo, bg="#ffb6c1").pack(side=tk.LEFT, padx=5)
        
        # --- SECCIÓN VALIDACIÓN ---
        tk.Label(root, text="Ingresa una cadena a evaluar:", font=("Arial", 10, "bold")).pack(pady=5)
        self.txt_cadena = tk.Entry(root, width=50, font=("Arial", 12))
        self.txt_cadena.pack()
        
        frame_validar = tk.Frame(root)
        frame_validar.pack(pady=10)
        tk.Button(frame_validar, text="Validar Rápido", command=self.validar_cadena).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_validar, text="Simulación Paso a Paso", command=self.paso_a_paso, bg="lightgreen").pack(side=tk.LEFT, padx=5)
        
        # --- SECCIÓN EXTRAS ---
        tk.Label(root, text="Operaciones de Lenguaje (Funcionalidades Adicionales):", font=("Arial", 12, "bold")).pack(pady=15)
        frame_extras = tk.Frame(root)
        frame_extras.pack()
        tk.Button(frame_extras, text="Prefijos/Sufijos/Subcadenas", command=self.mostrar_partes_cadena).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_extras, text="Cerradura Kleene (*) y Positiva (+)", command=self.mostrar_kleene).pack(side=tk.LEFT, padx=5)

    def editor_manual(self):
        alf = simpledialog.askstring("Definir Alfabeto", "Ingresa los símbolos separados por coma (ej: 0,1,2):")
        if not alf: return
        self.automata.alfabeto = set([x.strip() for x in alf.split(",")])
        
        est = simpledialog.askstring("Definir Estados", "Ingresa los IDs de estados separados por coma (ej: 0,1,2):")
        if not est: return
        self.automata.estados = set([x.strip() for x in est.split(",")])
        
        ini = simpledialog.askstring("Estado Inicial", f"Ingresa el estado inicial (debe estar en {self.automata.estados}):")
        if ini not in self.automata.estados: return messagebox.showerror("Error", "Estado inicial inválido.")
        self.automata.inicial = ini
        
        acep = simpledialog.askstring("Estados de Aceptación", "Ingresa los estados de aceptación separados por coma:")
        self.automata.aceptacion = set([x.strip() for x in acep.split(",") if x.strip() in self.automata.estados]) if acep else set()
        
        self.automata.transiciones = {e: {} for e in self.automata.estados}
        for estado in self.automata.estados:
            for sim in self.automata.alfabeto:
                dest = simpledialog.askstring("Transiciones", f"Desde q{estado} leyendo '{sim}', ¿a qué estado va?\n(Dejar vacío para rechazar/λ):")
                if dest and dest in self.automata.estados:
                    self.automata.transiciones[estado][sim] = dest
                    
        self.actualizar_info()

    def cargar_archivo(self):
        filepath = filedialog.askopenfilename(filetypes=[("Archivos soportados", "*.jff *.json *.xml"), ("JFLAP", "*.jff"), ("JSON", "*.json"), ("XML", "*.xml")])
        if not filepath: return
        
        try:
            if filepath.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.automata.alfabeto = set(data["alfabeto"])
                    self.automata.estados = set(data["estados"])
                    self.automata.inicial = str(data["inicial"])
                    self.automata.aceptacion = set([str(x) for x in data["aceptacion"]])
                    self.automata.transiciones = data["transiciones"]
            else:
                self.automata.cargar_jff(filepath)
            self.actualizar_info()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def exportar_automata(self):
        if not self.automata.estados:
            return messagebox.showwarning("Aviso", "Carga o crea un autómata primero.")
            
        filepath = filedialog.asksaveasfilename(title="Exportar Autómata", defaultextension=".jff", filetypes=[("JFLAP", "*.jff"), ("JSON", "*.json"), ("XML", "*.xml")])
        if not filepath: return

        try:
            if filepath.endswith('.json'):
                data = {
                    "alfabeto": list(self.automata.alfabeto),
                    "estados": list(self.automata.estados),
                    "inicial": self.automata.inicial,
                    "aceptacion": list(self.automata.aceptacion),
                    "transiciones": self.automata.transiciones
                }
                with open(filepath, 'w', encoding='utf-8') as f: 
                    json.dump(data, f, indent=4)
            else:
                root = ET.Element("structure")
                ET.SubElement(root, "type").text = "fa"
                automaton_node = ET.SubElement(root, "automaton")
                
                for estado in self.automata.estados:
                    state_node = ET.SubElement(automaton_node, "state", id=str(estado), name=f"q{estado}")
                    if str(estado) == str(self.automata.inicial): 
                        ET.SubElement(state_node, "initial")
                    if str(estado) in [str(x) for x in self.automata.aceptacion]: 
                        ET.SubElement(state_node, "final")
                
                for origen, trans in self.automata.transiciones.items():
                    for simbolo, destino in trans.items():
                        trans_node = ET.SubElement(automaton_node, "transition")
                        ET.SubElement(trans_node, "from").text = str(origen)
                        ET.SubElement(trans_node, "to").text = str(destino)
                        ET.SubElement(trans_node, "read").text = simbolo if simbolo != "λ" else ""
                
                tree = ET.ElementTree(root)
                tree.write(filepath, encoding="utf-8", xml_declaration=True)
                
            messagebox.showinfo("Éxito", f"Autómata exportado correctamente a:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Hubo un problema al guardar:\n{e}")

    def actualizar_info(self):
        info = f"Autómata Activo\nEstados: {len(self.automata.estados)} | Alfabeto: {self.automata.alfabeto}\nInicial: q{self.automata.inicial} | Aceptación: {[f'q{s}' for s in self.automata.aceptacion]}"
        self.lbl_info.config(text=info, fg="green")

    def mostrar_tabla(self):
        if not self.automata.estados: return messagebox.showwarning("Aviso", "No hay autómata cargado.")
        top = tk.Toplevel(self.root)
        top.title("Tabla de Transiciones")
        top.geometry("450x300")
        
        alfabeto_ordenado = sorted(list(self.automata.alfabeto))
        columnas = ["Estado"] + alfabeto_ordenado
        tree = ttk.Treeview(top, columns=columnas, show="headings")
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=80)
            
        for estado in sorted(list(self.automata.estados)):
            prefijo = "-> " if str(estado) == str(self.automata.inicial) else ""
            prefijo += "* " if str(estado) in [str(x) for x in self.automata.aceptacion] else ""
            fila = [f"{prefijo}q{estado}"]
            for sim in alfabeto_ordenado:
                destino = self.automata.transiciones.get(str(estado), {}).get(sim, "-")
                fila.append(f"q{destino}" if destino != "-" else "-")
            tree.insert("", tk.END, values=fila)
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def mostrar_grafo(self):
        if not self.automata.estados: return messagebox.showwarning("Aviso", "No hay autómata cargado.")
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            
            G = nx.DiGraph()
            for origen, trans in self.automata.transiciones.items():
                for simbolo, destino in trans.items():
                    if G.has_edge(f"q{origen}", f"q{destino}"):
                        G[f"q{origen}"][f"q{destino}"]['label'] += f", {simbolo}"
                    else:
                        G.add_edge(f"q{origen}", f"q{destino}", label=simbolo)
                        
            pos = nx.spring_layout(G, seed=42)
            plt.figure(figsize=(7, 5))
            
            node_colors = []
            for n in G.nodes():
                raw_node = n.replace("q","")
                if raw_node == str(self.automata.inicial): node_colors.append("lightgreen")
                elif raw_node in [str(x) for x in self.automata.aceptacion]: node_colors.append("gold")
                else: node_colors.append("lightblue")
                
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1800, font_size=10, font_weight="bold", arrows=True)
            edge_labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
            plt.title("Grafo del Autómata (Verde=Inicial, Oro=Final)")
            plt.axis('off')
            plt.show()
        except ImportError:
            messagebox.showerror("Librería faltante", "No se pudo dibujar el grafo porque falta NetworkX o Matplotlib.\nInstálalas ejecutando:\npip install networkx matplotlib")

    def validar_cadena(self):
        cadena = self.txt_cadena.get()
        if not self.automata.estados: return
        aceptada, traza = self.automata.procesar_cadena(cadena)
        estado_txt = "ACEPTADA" if aceptada else "RECHAZADA"
        traza_txt = " -> ".join([f"q{s}" for s in traza])
        messagebox.showinfo("Resultado Rápido", f"Cadena: '{cadena}'\nResultado: {estado_txt}\nRecorrido: {traza_txt}")

    def paso_a_paso(self):
        cadena = self.txt_cadena.get()
        if not self.automata.estados: return
        aceptada, traza = self.automata.procesar_cadena(cadena)
        recorrido = ""
        for i in range(len(cadena)):
            if i+1 < len(traza):
                recorrido += f"Paso {i+1}: Leyendo '{cadena[i]}' -> q{traza[i+1]}\n"
            else:
                recorrido += f"Paso {i+1}: FALLO al leer '{cadena[i]}'\n"
                break
        recorrido += f"\nEstado final: q{traza[-1]}\nResultado Final: {'ACEPTADA' if aceptada else 'RECHAZADA'}"
        messagebox.showinfo("Paso a Paso", recorrido)

    def mostrar_partes_cadena(self):
        cadena = self.txt_cadena.get()
        if not cadena: return
        pref, suf, sub = obtener_prefijos(cadena), obtener_sufijos(cadena), obtener_subcadenas(cadena)
        msg = f"Cadena original: '{cadena}'\n\nPREFIJOS:\n{pref}\n\nSUFIJOS:\n{suf}\n\nSUBCADENAS:\n{sub}"
        self.crear_ventana_resultados("Subcadenas, Prefijos y Sufijos", msg)

    def mostrar_kleene(self):
        if not self.automata.alfabeto: return messagebox.showwarning("Aviso", "Carga un autómata para obtener su alfabeto.")
        n = simpledialog.askinteger("Cerradura", "Longitud máxima (n):", minvalue=1, maxvalue=8)
        if n:
            pos, kle = obtener_positiva(self.automata.alfabeto, n), obtener_kleene(self.automata.alfabeto, n)
            pos.sort(key=len); kle.sort(key=len)
            msg = f"Alfabeto: {self.automata.alfabeto}\n\nCERRADURA POSITIVA (+):\n{pos}\n\nCERRADURA DE KLEENE (*):\n{kle}"
            self.crear_ventana_resultados("Cerraduras", msg)
            
    def crear_ventana_resultados(self, titulo, contenido):
        top = tk.Toplevel(self.root)
        top.title(titulo)
        top.geometry("500x400")
        txt_area = tk.Text(top, wrap=tk.WORD, font=("Consolas", 10))
        txt_area.insert(tk.END, contenido)
        txt_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        tk.Button(top, text="Guardar resultados en .txt", command=lambda: self.guardar_txt(contenido), bg="lightgray").pack(pady=5)

    def guardar_txt(self, contenido):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f: f.write(contenido)
            messagebox.showinfo("Éxito", "Archivo .txt guardado correctamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
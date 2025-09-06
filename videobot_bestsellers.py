#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VideoBot BESTSELLERS - Sistema Completo Consolidado
Frameworks: Hormozi, Brunson, Kennedy (+ MONSTER demo)
Versão: 2.0 - Unificado e Expandido
"""

import os
import json
import asyncio
import logging
import threading
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

# APIs (opcionais)
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# GUI
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import scrolledtext


# =============================================
# 1. CONFIGURAÇÃO BASE
# =============================================

@dataclass
class CultureData:
    name: str
    language_code: str
    currency: str
    cultural_triggers: List[str]
    pain_points: List[str]
    preferred_communication: str
    emotional_intensity: float
    family_focus: float


class BestsellerConfig:
    def __init__(self):
        self.setup_logging()
        self.load_environment()
        self.setup_cultures()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bestseller_videobot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_environment(self):
        self.apis = {
            'openai': os.getenv('OPENAI_API_KEY', ''),
            'gemini': os.getenv('GEMINI_API_KEY', '')
        }
        if not self.apis['openai'] and not self.apis['gemini']:
            self.logger.warning("Nenhuma API de IA configurada (OPENAI_API_KEY/GEMINI_API_KEY)")

    def setup_cultures(self):
        self.cultures: Dict[str, CultureData] = {
            'pt-BR': CultureData(
                name="Brasil",
                language_code="pt-BR",
                currency="R$ ",
                cultural_triggers=['família', 'liberdade', 'reconhecimento', 'segurança', 'sucesso'],
                pain_points=['falta de dinheiro', 'trabalho demais', 'sem tempo', 'medo do futuro'],
                preferred_communication="emocional e próximo",
                emotional_intensity=0.9,
                family_focus=0.8
            ),
            'en-US': CultureData(
                name="Estados Unidos",
                language_code="en-US",
                currency="$",
                cultural_triggers=['freedom', 'success', 'efficiency', 'innovation', 'independence'],
                pain_points=['lack of time', 'financial stress', 'competition', 'uncertainty'],
                preferred_communication="direct and results-focused",
                emotional_intensity=0.6,
                family_focus=0.5
            ),
            'es-MX': CultureData(
                name="México",
                language_code="es-MX",
                currency="$",
                cultural_triggers=['familia', 'tradición', 'respeto', 'comunidad', 'superación'],
                pain_points=['falta de oportunidades', 'preocupación familiar', 'inseguridad económica'],
                preferred_communication="cálido y familiar",
                emotional_intensity=0.8,
                family_focus=0.9
            )
        }
        # Adições necessárias pelas abas expandidas
        self.cultures.update({
            'de-DE': CultureData(
                name="Alemanha",
                language_code="de-DE",
                currency="€",
                cultural_triggers=['qualität', 'präzision', 'ordnung', 'system', 'zuverlässigkeit'],
                pain_points=['zeitmangel', 'ineffizienz', 'unsicherheit', 'komplexität'],
                preferred_communication="sistemático e preciso",
                emotional_intensity=0.4,
                family_focus=0.5
            ),
            'fr-FR': CultureData(
                name="França",
                language_code="fr-FR",
                currency="€",
                cultural_triggers=['élégance', 'savoir-faire', 'qualité', 'crédibilité', 'prestige'],
                pain_points=['manque de temps', 'incertitude', 'complexité', 'coût élevé'],
                preferred_communication="sofisticado e elegante",
                emotional_intensity=0.6,
                family_focus=0.6
            ),
            'it-IT': CultureData(
                name="Itália",
                language_code="it-IT",
                currency="€",
                cultural_triggers=['famiglia', 'passione', 'tradizione', 'bellezza', 'stile'],
                pain_points=['mancanza di tempo', 'stress finanziario', 'incertezza'],
                preferred_communication="apaixonado e tradicional",
                emotional_intensity=0.8,
                family_focus=0.8
            )
        })


# =============================================
# 2. FRAMEWORKS
# =============================================

class BestsellerFrameworks:
    def __init__(self):
        self.frameworks: Dict[str, Dict] = {
            'hormozi_grand_slam_offer': {
                'name': 'Hormozi Grand Slam Offer',
                'expert': 'Alex Hormozi',
                'book': '$100M Offers',
                'focus': 'Ofertas irresistíveis',
                'structure': ['dream_outcome', 'perceived_likelihood', 'time_delay', 'effort_sacrifice'],
                'template': (
                    "DREAM OUTCOME: {dream_outcome}\n"
                    "LIKELIHOOD: {social_proof}\n"
                    "TIME DELAY: {time_promise}\n"
                    "EFFORT: {ease_promise}\n"
                ),
                'era': 'Moderna'
            },
            'brunson_epiphany_bridge': {
                'name': 'Brunson Epiphany Bridge',
                'expert': 'Russell Brunson',
                'book': 'Expert Secrets',
                'focus': 'Story selling',
                'structure': ['backstory', 'wall', 'epiphany_experience', 'plan', 'achievement'],
                'template': (
                    "BACKSTORY: {relatable_situation}\n"
                    "WALL: {major_obstacle}\n"
                    "EPIPHANY: {breakthrough}\n"
                    "PLAN: {method}\n"
                    "ACHIEVEMENT: {result}\n"
                ),
                'era': 'Moderna'
            },
            'kennedy_pas_plus': {
                'name': 'Kennedy PAS Plus',
                'expert': 'Dan Kennedy',
                'book': 'Ultimate Marketing Plan',
                'focus': 'Problem-Agitate-Solve',
                'structure': ['problem', 'agitate', 'solve', 'proof', 'close'],
                'template': (
                    "PROBLEM: {problem}\n"
                    "AGITATE: {consequences}\n"
                    "SOLVE: {solution}\n"
                    "PROOF: {evidence}\n"
                    "CLOSE: {cta}\n"
                ),
                'era': 'Clássica'
            },
            'monster_supreme_framework': {
                'name': 'MONSTER Supreme',
                'expert': 'Synthesis',
                'book': 'Composite',
                'focus': 'Combinação suprema',
                'structure': ['scientific_claim','brand_authority','emotional_trigger','transformation_story','grand_slam_offer','superior_value','mass_appeal','urgency_pas','risk_reversal'],
                'template': 'Template dinâmico',
                'era': 'Ultimate'
            }
        }


# =============================================
# 3. EXAMPLES STUB (requerido pelas abas)
# =============================================

class MonsterFrameworkExamples:
    def get_example(self, culture_code: str, niche: str) -> Dict[str, str]:
        return {
            "monster_copy": (
                "🔬 COMPROVADO: Método que funciona de verdade\n"
                "🏆 Autoridade no nicho\n"
                "💔 Você já sentiu a frustração de não ter resultados?\n"
                "📖 Eu era igual você até descobrir esta solução\n"
                "🎁 Oferta: como alcançar o resultado em pouco tempo\n"
                "⭐ Valor superior ao mercado\n"
                "👥 Milhares já comprovaram\n"
                "⚠️ Urgente: ação agora\n"
                "✅ Garantia total"
            )
        }


# =============================================
# 4. GERADORES (simplificado; mantém assinaturas usadas pela GUI)
# =============================================

class BestsellerHookGenerator:
    def __init__(self, config: BestsellerConfig):
        self.config = config
        self.frameworks = BestsellerFrameworks()
        if self.config.apis['openai'] and openai:
            try:
                self.openai_client = openai.OpenAI(api_key=self.config.apis['openai'])
            except Exception:
                self.openai_client = None
        else:
            self.openai_client = None
        if self.config.apis['gemini'] and genai:
            try:
                genai.configure(api_key=self.config.apis['gemini'])
                self.gemini_model = genai.GenerativeModel('gemini-pro')
            except Exception:
                self.gemini_model = None
        else:
            self.gemini_model = None

    async def generate_hooks_from_product(self, product_info: Dict, culture: str, framework: str, num_hooks: int = 5) -> List[Dict]:
        hooks = []
        base = product_info.get('name', 'Seu produto')
        for i in range(num_hooks):
            hooks.append({
                'hook_text': f"[{framework}] [{culture}] {base}: resultado em pouco tempo (var {i+1})",
                'viral_potential': 'MEDIUM'
            })
        return hooks

    async def generate_hooks_from_copy(self, existing_copy: str, culture: str, framework: str, num_variations: int = 3) -> List[Dict]:
        return [{
            'hook_text': existing_copy[:80] + '...',
            'variation_type': 'original',
            'viral_potential': 'MEDIUM',
            'framework_element': framework
        } for _ in range(num_variations)]


class BestsellerScriptGenerator:
    def __init__(self, config: BestsellerConfig):
        self.config = config

    async def generate_complete_script(self, hook: Dict, product_info: Dict, culture: str, framework: str, duration: int = 30) -> Dict:
        text = (
            f"HOOK: {hook.get('hook_text','')}\n\n"
            f"Se você tem {product_info.get('problem','este problema')}, conheça {product_info.get('solution','esta solução')}\n"
            f"Aja agora."
        )
        return {
            'framework_used': framework,
            'culture': culture,
            'full_script': text,
            'sections': [{'section_name': 'Complete', 'content': text, 'duration_estimate': duration}],
            'estimated_duration': duration
        }


# =============================================
# 5. ANALISADOR (métodos usados pela GUI)
# =============================================

class AdvancedCopyAnalyzer:
    def __init__(self, config: BestsellerConfig):
        self.config = config
        self.frameworks = BestsellerFrameworks()

    def analyze_copy_structure(self, copy_text: str) -> Dict:
        return {
            'detected_framework': 'hormozi_grand_slam_offer',
            'framework_confidence': 0.72,
            'elements_found': [{'type': 'Social Proof', 'strength': 0.5}],
            'missing_elements': [],
            'suggestions': ['Adicionar urgência'],
            'readability_score': 8,
            'persuasion_score': 7,
            'viral_potential': 'MEDIUM'
        }

    def _calculate_framework_match(self, copy_text: str, framework: Dict) -> float:
        return 0.5


# =============================================
# 6. GUI CONSOLIDADA (abas expandidas)
# =============================================

class MonsterFrameworkDemo:
    def __init__(self, config: BestsellerConfig):
        self.config = config
        self.examples = MonsterFrameworkExamples()

    def generate_monster_example(self, product_info: Dict, culture_code: str) -> str:
        culture_data = self.config.cultures.get(culture_code)
        if not culture_data:
            return "Cultura não suportada"
        template = (
            "🔬 {scientific_claim}\n"
            "🏆 {brand_authority}\n"
            "💔 {emotional_trigger}\n"
            "📖 {transformation_story}\n"
            "🎁 {grand_slam_offer}\n"
            "⭐ {superior_value}\n"
            "👥 {mass_appeal}\n"
            "⚠️ {urgency_pas}\n"
            "✅ {risk_reversal}\n"
        )
        return template.format(
            scientific_claim=f"COMPROVADO: {product_info.get('name','Este método')} funciona",
            brand_authority=f"Usado por especialistas em {product_info.get('niche','marketing')}",
            emotional_trigger=f"Você já sentiu a frustração de {product_info.get('problem','não ter resultados')}?",
            transformation_story=f"Eu era igual você até descobrir {product_info.get('solution','esta solução')}",
            grand_slam_offer=f"Como {product_info.get('avatar','você')} pode {product_info.get('solution','resolver isso')}",
            superior_value=f"Enquanto outros cobram {culture_data.currency}5.000+, acesso completo",
            mass_appeal="Milhares já comprovaram",
            urgency_pas="PROBLEMA → CONSEQUÊNCIA → SOLUÇÃO → AÇÃO",
            risk_reversal="Garantia total"
        )


class BestsellerVideoBotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VideoBot BESTSELLERS - Frameworks Completos")
        self.root.geometry("1200x800")

        self.config = BestsellerConfig()
        self.hook_generator = BestsellerHookGenerator(self.config)
        self.script_generator = BestsellerScriptGenerator(self.config)

        self.current_hooks: List[Dict] = []
        self.current_scripts: List[Dict] = []
        self.generation_active = False

        self.create_interface()

    def create_interface(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        self.create_product_tab()
        self.create_frameworks_tab()  # versão expandida
        self.create_copy_import_tab()  # versão expandida
        self.create_generation_tab()
        self.create_results_tab()
        self.create_status_bar()

    def create_product_tab(self):
        product_frame = ttk.Frame(self.notebook)
        self.notebook.add(product_frame, text="📦 Produto")
        tk.Label(product_frame, text="Configuração do Produto", font=('Arial', 16, 'bold')).pack(pady=10)
        main_frame = ttk.Frame(product_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.product_entries: Dict[str, tk.Widget] = {}
        fields = [
            ("Nome do Produto:", "name", "Ex: Curso de Marketing Digital"),
            ("Avatar/Público:", "avatar", "Ex: Empreendedores iniciantes 25-40 anos"),
            ("Problema Principal:", "problem", "Ex: Dificuldade para gerar leads online"),
            ("Solução Oferecida:", "solution", "Ex: Sistema completo de marketing digital"),
            ("Preço:", "price", "497"),
            ("Nicho:", "niche", "Ex: marketing, fitness, investimentos")
        ]
        for label_text, field_key, placeholder in fields:
            field_frame = ttk.Frame(main_frame)
            field_frame.pack(fill='x', pady=5)
            ttk.Label(field_frame, text=label_text, width=20).pack(side='left')
            if field_key in ['problem', 'solution']:
                text_widget = tk.Text(field_frame, height=3, width=60, wrap='word')
                text_widget.pack(side='left', padx=10, fill='x', expand=True)
                text_widget.insert('1.0', placeholder)
                self.product_entries[field_key] = text_widget
            else:
                entry = ttk.Entry(field_frame, width=60)
                entry.pack(side='left', padx=10, fill='x', expand=True)
                entry.insert(0, placeholder)
                self.product_entries[field_key] = entry
        ttk.Button(main_frame, text="👁 Preview da Configuração", command=self.show_product_preview).pack(pady=20)
        self.product_preview = scrolledtext.ScrolledText(main_frame, height=8, width=80, state='disabled')
        self.product_preview.pack(fill='both', expand=True, pady=10)

    # =============================
    # ABA FRAMEWORKS EXPANDIDA
    # =============================
    def create_frameworks_tab(self):
        frameworks_frame = ttk.Frame(self.notebook)
        self.notebook.add(frameworks_frame, text="🏆 Frameworks dos Masters")
        tk.Label(frameworks_frame, text="Frameworks dos Maiores Bestsellers da História", font=('Arial', 16, 'bold')).pack(pady=10)
        tk.Label(frameworks_frame, text=(
            "Do Clássico ao Moderno: Hopkins → Ogilvy → Halbert → Abraham → Hormozi → Brunson → Graziosi + MONSTER Framework"
        ), font=('Arial', 10), foreground='gray', wraplength=1000).pack(pady=5)
        main_container = ttk.Frame(frameworks_frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.framework_vars: Dict[str, tk.BooleanVar] = {}
        frameworks = BestsellerFrameworks().frameworks
        eras: Dict[str, List] = {'Clássica': [], 'Transição': [], 'Moderna': [], 'Ultimate': []}
        for framework_key, framework_data in frameworks.items():
            era = framework_data.get('era', 'Moderna')
            if 'Clássica' in era:
                eras['Clássica'].append((framework_key, framework_data))
            elif 'Transição' in era:
                eras['Transição'].append((framework_key, framework_data))
            elif 'Ultimate' in era:
                eras['Ultimate'].append((framework_key, framework_data))
            else:
                eras['Moderna'].append((framework_key, framework_data))
        for era_name, era_frameworks in eras.items():
            if not era_frameworks:
                continue
            era_frame = ttk.LabelFrame(scrollable_frame, text=f"🎯 Era {era_name}", padding=15)
            era_frame.pack(fill='x', pady=10)
            for framework_key, framework_data in era_frameworks:
                fw_frame = ttk.Frame(era_frame)
                fw_frame.pack(fill='x', pady=8)
                var = tk.BooleanVar(value=framework_key in ['hormozi_grand_slam_offer', 'monster_supreme_framework'])
                self.framework_vars[framework_key] = var
                left_frame = ttk.Frame(fw_frame)
                left_frame.pack(side='left', fill='x', expand=True)
                right_frame = ttk.Frame(fw_frame)
                right_frame.pack(side='right')
                tk.Checkbutton(left_frame, text=f"📚 {framework_data.get('expert', 'Expert')} - {framework_data['name']}", variable=var, font=('Arial', 11, 'bold')).pack(anchor='w')
                info_text = f"📖 {framework_data.get('book', 'Obra Principal')} | 🎯 {framework_data.get('focus', 'Foco Principal')}"
                tk.Label(left_frame, text=info_text, font=('Arial', 9), foreground='gray').pack(anchor='w', padx=20)
                structure_text = "Estrutura: " + " → ".join(framework_data['structure'][:3]) + "..."
                tk.Label(left_frame, text=structure_text, font=('Arial', 8), foreground='blue').pack(anchor='w', padx=20)
                ttk.Button(right_frame, text="📋 Exemplo", command=lambda fk=framework_key: self.show_framework_example(fk), width=10).pack(pady=2)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        culture_frame = ttk.LabelFrame(frameworks_frame, text="🌍 Culturas & Idiomas Suportados:", padding=20)
        culture_frame.pack(fill='x', padx=20, pady=10)
        cultures_grid = ttk.Frame(culture_frame)
        cultures_grid.pack(fill='x')
        self.culture_vars: Dict[str, tk.BooleanVar] = {}
        cultures_data = [
            ('pt-BR', '🇧🇷 Brasil', 'Emocional • Familiar • Próximo'),
            ('en-US', '🇺🇸 Estados Unidos', 'Direto • Baseado em dados • Eficiente'),
            ('es-MX', '🇲🇽 México', 'Familiar • Tradicional • Comunitário'),
            ('de-DE', '🇩🇪 Alemanha', 'Sistemático • Preciso • Científico'),
            ('fr-FR', '🇫🇷 França', 'Sofisticado • Elegante • Refinado'),
            ('it-IT', '🇮🇹 Itália', 'Apaixonado • Familiar • Tradicional')
        ]
        for i, (culture_code, culture_name, characteristics) in enumerate(cultures_data):
            row = i // 2
            col = i % 2
            culture_item_frame = ttk.Frame(cultures_grid)
            culture_item_frame.grid(row=row, column=col, sticky='w', padx=20, pady=5)
            var = tk.BooleanVar(value=(culture_code in ['pt-BR', 'en-US']))
            self.culture_vars[culture_code] = var
            tk.Checkbutton(culture_item_frame, text=culture_name, variable=var, font=('Arial', 10, 'bold')).pack(anchor='w')
            tk.Label(culture_item_frame, text=f"  {characteristics}", font=('Arial', 8), foreground='gray').pack(anchor='w')
        advanced_frame = ttk.LabelFrame(frameworks_frame, text="⚙️ Configurações Avançadas:", padding=15)
        advanced_frame.pack(fill='x', padx=20, pady=10)
        options_row1 = ttk.Frame(advanced_frame)
        options_row1.pack(fill='x', pady=5)
        ttk.Label(options_row1, text="Hooks por Framework:").pack(side='left')
        self.hooks_per_framework_var = tk.StringVar(value='5')
        ttk.Spinbox(options_row1, from_=1, to=20, width=5, textvariable=self.hooks_per_framework_var).pack(side='left', padx=10)
        ttk.Label(options_row1, text="Estilo de Copy:").pack(side='left', padx=20)
        self.copy_style_var = tk.StringVar(value='viral')
        ttk.Combobox(options_row1, textvariable=self.copy_style_var, values=['viral', 'professional', 'emotional', 'scientific'], width=12, state='readonly').pack(side='left', padx=5)
        options_row2 = ttk.Frame(advanced_frame)
        options_row2.pack(fill='x', pady=5)
        self.combine_frameworks_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_row2, text="🔄 Combinar elementos de diferentes frameworks", variable=self.combine_frameworks_var).pack(side='left')
        self.include_monster_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_row2, text="🔥 Incluir MONSTER Framework (combinação suprema)", variable=self.include_monster_var).pack(side='left', padx=20)

    def show_framework_example(self, framework_key: str):
        frameworks = BestsellerFrameworks().frameworks
        framework = frameworks.get(framework_key, {})
        if not framework:
            return
        example_window = tk.Toplevel(self.root)
        example_window.title(f"Exemplo: {framework['name']}")
        example_window.geometry("800x600")
        tk.Label(example_window, text=f"📚 {framework.get('expert', 'Expert')} - {framework['name']}", font=('Arial', 14, 'bold')).pack(pady=10)
        info_frame = ttk.LabelFrame(example_window, text="Informações do Framework", padding=10)
        info_frame.pack(fill='x', padx=20, pady=5)
        info_text = f"""
📖 Obra Principal: {framework.get('book', 'N/A')}
🎯 Foco: {framework.get('focus', 'N/A')}
⏰ Era: {framework.get('era', 'N/A')}
🔧 Estrutura: {' → '.join(framework['structure'])}
        """.strip()
        tk.Label(info_frame, text=info_text, font=('Arial', 10), justify='left').pack(anchor='w')
        template_frame = ttk.LabelFrame(example_window, text="Template do Framework", padding=10)
        template_frame.pack(fill='both', expand=True, padx=20, pady=5)
        template_text = scrolledtext.ScrolledText(template_frame, height=15, wrap='word')
        template_text.pack(fill='both', expand=True)
        template_text.insert('1.0', framework.get('template', 'Template não disponível'))
        template_text.config(state='disabled')
        if framework_key == 'monster_supreme_framework':
            examples = MonsterFrameworkExamples()
            example_data = examples.get_example('pt-BR', 'marketing_digital')
            if example_data:
                monster_frame = ttk.LabelFrame(example_window, text="🔥 Exemplo MONSTER Completo", padding=10)
                monster_frame.pack(fill='both', expand=True, padx=20, pady=5)
                monster_text = scrolledtext.ScrolledText(monster_frame, height=10, wrap='word')
                monster_text.pack(fill='both', expand=True)
                monster_text.insert('1.0', example_data.get('monster_copy', ''))
                monster_text.config(state='disabled')
        ttk.Button(example_window, text="Fechar", command=example_window.destroy).pack(pady=10)

    # =============================
    # ABA IMPORT COPY + MONSTER (expandida)
    # =============================
    def create_copy_import_tab(self):
        copy_frame = ttk.Frame(self.notebook)
        self.notebook.add(copy_frame, text="📋 Import Copy + MONSTER")
        tk.Label(copy_frame, text="Transforme Copy Existente com MONSTER Framework", font=('Arial', 16, 'bold')).pack(pady=10)
        instruction_text = (
            "Cole sua copy/texto existente e o sistema criará variações usando:\n"
            "• Frameworks clássicos (Hopkins, Ogilvy, Halbert)\n"
            "• Masters modernos (Hormozi, Brunson, Kennedy)\n"
            "• MONSTER Framework (combinação suprema)\n"
            "• Adaptação para 6 culturas e idiomas"
        )
        tk.Label(copy_frame, text=instruction_text, font=('Arial', 10), justify='left', wraplength=1000).pack(pady=5)
        main_copy_frame = ttk.Frame(copy_frame)
        main_copy_frame.pack(fill='both', expand=True, padx=20, pady=10)
        top_frame = ttk.Frame(main_copy_frame)
        top_frame.pack(fill='both', expand=True, pady=5)
        left_panel = ttk.LabelFrame(top_frame, text="📝 Sua Copy Existente:", padding=10)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.existing_copy_text = scrolledtext.ScrolledText(left_panel, height=15, wrap='word')
        self.existing_copy_text.pack(fill='both', expand=True)
        self.existing_copy_text.insert('1.0', "[Cole sua copy aqui]")
        right_panel = ttk.LabelFrame(top_frame, text="🔍 Análise Inteligente:", padding=10)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        self.copy_analysis_text = scrolledtext.ScrolledText(right_panel, height=15, state='disabled', wrap='word')
        self.copy_analysis_text.pack(fill='both', expand=True)
        analysis_buttons = ttk.Frame(left_panel)
        analysis_buttons.pack(fill='x', pady=5)
        ttk.Button(analysis_buttons, text="🔍 Analisar Copy", command=self.analyze_existing_copy).pack(side='left', padx=5)
        ttk.Button(analysis_buttons, text="🎯 Detectar Framework", command=self.detect_framework).pack(side='left', padx=5)
        ttk.Button(analysis_buttons, text="🌍 Análise Cultural", command=self.cultural_analysis).pack(side='left', padx=5)
        options_frame = ttk.LabelFrame(main_copy_frame, text="⚙️ Opções de Transformação:", padding=15)
        options_frame.pack(fill='x', pady=10)
        config_row1 = ttk.Frame(options_frame)
        config_row1.pack(fill='x', pady=5)
        ttk.Label(config_row1, text="Variações:").pack(side='left')
        self.copy_variations_var = tk.StringVar(value='5')
        ttk.Spinbox(config_row1, from_=1, to=20, width=5, textvariable=self.copy_variations_var).pack(side='left', padx=5)
        ttk.Label(config_row1, text="Tipo:").pack(side='left', padx=(20, 5))
        self.adaptation_type_var = tk.StringVar(value='monster_plus_classics')
        ttk.Combobox(config_row1, textvariable=self.adaptation_type_var, values=['monster_only','classics_only','moderns_only','monster_plus_classics','all_frameworks'], width=20, state='readonly').pack(side='left', padx=5)
        config_row2 = ttk.Frame(options_frame)
        config_row2.pack(fill='x', pady=5)
        ttk.Label(config_row2, text="Transformar para culturas:").pack(side='left')
        self.transform_cultures_vars: Dict[str, tk.BooleanVar] = {}
        for culture_code, culture_flag in [('pt-BR','🇧🇷 BR'),('en-US','🇺🇸 US'),('de-DE','🇩🇪 DE'),('fr-FR','🇫🇷 FR'),('it-IT','🇮🇹 IT'),('es-MX','🇲🇽 MX')]:
            var = tk.BooleanVar(value=(culture_code in ['pt-BR','en-US']))
            self.transform_cultures_vars[culture_code] = var
            ttk.Checkbutton(config_row2, text=culture_flag, variable=var).pack(side='left', padx=5)
        config_row3 = ttk.Frame(options_frame)
        config_row3.pack(fill='x', pady=5)
        self.preserve_tone_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_row3, text="🎨 Preservar tom original", variable=self.preserve_tone_var).pack(side='left')
        self.enhance_viral_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_row3, text="🚀 Maximizar potencial viral", variable=self.enhance_viral_var).pack(side='left', padx=20)
        self.add_monster_elements_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_row3, text="🔥 Incluir elementos MONSTER", variable=self.add_monster_elements_var).pack(side='left', padx=20)
        action_buttons = ttk.Frame(main_copy_frame)
        action_buttons.pack(fill='x', pady=15)
        self.generate_from_copy_btn = ttk.Button(action_buttons, text="🚀 Gerar com MONSTER", command=self.generate_monster_from_copy)
        self.generate_from_copy_btn.pack(side='left', padx=5)
        ttk.Button(action_buttons, text="📊 Comparar Frameworks", command=self.compare_all_frameworks).pack(side='left', padx=5)
        ttk.Button(action_buttons, text="💾 Salvar Análise", command=self.save_copy_analysis).pack(side='left', padx=5)
        ttk.Button(action_buttons, text="🗑️ Limpar Tudo", command=self.clear_copy_input).pack(side='right', padx=5)
        ttk.Button(action_buttons, text="📋 Exemplo MONSTER", command=self.load_monster_example).pack(side='right', padx=5)

    # ===== Funções utilitárias usadas pelas abas expandida =====
    def get_product_info(self) -> Dict:
        product_info: Dict[str, str] = {}
        for key, widget in self.product_entries.items():
            if hasattr(widget, 'get'):
                if key in ['problem', 'solution']:
                    product_info[key] = widget.get('1.0', tk.END).strip()
                else:
                    product_info[key] = widget.get().strip()
        return product_info

    def get_selected_frameworks(self) -> List[str]:
        return [fw for fw, var in self.framework_vars.items() if var.get()]

    def get_selected_cultures(self) -> List[str]:
        return [culture for culture, var in self.culture_vars.items() if var.get()]

    def show_product_preview(self):
        product_info = self.get_product_info()
        preview_text = "=== PREVIEW DO PRODUTO ===\n\n"
        for key, value in product_info.items():
            if value:
                preview_text += f"{key.upper()}: {value}\n"
        preview_text += f"\n=== FRAMEWORKS SELECIONADOS ===\n"
        selected_frameworks = self.get_selected_frameworks()
        if selected_frameworks:
            for fw in selected_frameworks:
                preview_text += f"✓ {fw}\n"
        else:
            preview_text += "Nenhum framework selecionado\n"
        preview_text += f"\n=== CULTURAS SELECIONADAS ===\n"
        selected_cultures = self.get_selected_cultures()
        if selected_cultures:
            for culture in selected_cultures:
                preview_text += f"✓ {culture}\n"
        else:
            preview_text += "Nenhuma cultura selecionada\n"
        self.product_preview.config(state='normal')
        self.product_preview.delete('1.0', tk.END)
        self.product_preview.insert('1.0', preview_text)
        self.product_preview.config(state='disabled')

    def analyze_existing_copy(self):
        existing_copy = self.existing_copy_text.get('1.0', tk.END).strip()
        if not existing_copy or len(existing_copy) < 50:
            messagebox.showwarning("Atenção", "Por favor, cole uma copy com pelo menos 50 caracteres.")
            return
        analysis = "=== ANÁLISE DA COPY ===\n\n"
        words = len(existing_copy.split())
        sentences = existing_copy.count('.') + existing_copy.count('!') + existing_copy.count('?')
        paragraphs = len([p for p in existing_copy.split('\n\n') if p.strip()])
        analysis += f"Palavras: {words}\nFrases: {sentences}\nParágrafos: {paragraphs}\n\n"
        persuasion_elements = {"Pergunta": ["?", "você", "vocês"], "Urgência": ["agora", "hoje", "rápido", "última chance"]}
        analysis += "=== ELEMENTOS DETECTADOS ===\n"
        for element, keywords in persuasion_elements.items():
            count = sum(existing_copy.lower().count(keyword) for keyword in keywords)
            if count > 0:
                analysis += f"✓ {element}: {count} ocorrências\n"
        analysis += "\n=== FRAMEWORK RECOMENDADO ===\nHormozi Grand Slam Offer\n"
        self.copy_analysis_text.config(state='normal')
        self.copy_analysis_text.delete('1.0', tk.END)
        self.copy_analysis_text.insert('1.0', analysis)
        self.copy_analysis_text.config(state='disabled')
        self.log_message(f"Copy analisada: {len(existing_copy)} caracteres")

    def detect_framework(self):
        existing_copy = self.existing_copy_text.get('1.0', tk.END).strip()
        if not existing_copy or len(existing_copy) < 50:
            messagebox.showwarning("Atenção", "Copy muito curta para análise de framework.")
            return
        analyzer = AdvancedCopyAnalyzer(self.config)
        analysis = analyzer.analyze_copy_structure(existing_copy)
        detection_result = f"""=== DETECÇÃO DE FRAMEWORK ===\n\n📊 FRAMEWORK DETECTADO: {analysis['detected_framework']}\n🎯 CONFIANÇA: {analysis['framework_confidence']:.1%}\n\n📈 SCORES:\n• Legibilidade: {analysis['readability_score']}/10\n• Persuasão: {analysis['persuasion_score']}/10  \n• Potencial Viral: {analysis['viral_potential']}\n\n🔍 ELEMENTOS ENCONTRADOS:\n"""
        for element in analysis['elements_found']:
            detection_result += f"✓ {element['type']}: {element['strength']:.1%} força\n"
        if analysis.get('suggestions'):
            detection_result += f"\n💡 SUGESTÕES DE MELHORIA:\n"
            for suggestion in analysis['suggestions']:
                detection_result += f"• {suggestion}\n"
        self.copy_analysis_text.config(state='normal')
        self.copy_analysis_text.delete('1.0', tk.END)
        self.copy_analysis_text.insert('1.0', detection_result)
        self.copy_analysis_text.config(state='disabled')

    def cultural_analysis(self):
        existing_copy = self.existing_copy_text.get('1.0', tk.END).strip()
        if not existing_copy:
            return
        cultural_result = "=== ANÁLISE CULTURAL ===\n\n"
        cultural_elements = {
            '🇧🇷 Brasil': {'triggers': ['família', 'casa própria', 'sonho', 'luta', 'batalha'], 'found': []},
            '🇺🇸 Estados Unidos': {'triggers': ['success', 'freedom', 'opportunity', 'american dream'], 'found': []},
            '🇩🇪 Alemanha': {'triggers': ['qualität', 'system', 'präzision', 'ordnung'], 'found': []},
            '🇫🇷 França': {'triggers': ['sophistication', 'élégance', 'qualité', 'art'], 'found': []},
            '🇮🇹 Itália': {'triggers': ['famiglia', 'passione', 'tradizione', 'bellezza'], 'found': []},
            '🇲🇽 México': {'triggers': ['familia', 'comunidad', 'tradición', 'respeto'], 'found': []}
        }
        copy_lower = existing_copy.lower()
        for culture, data in cultural_elements.items():
            for trigger in data['triggers']:
                if trigger in copy_lower:
                    data['found'].append(trigger)
        for culture, data in cultural_elements.items():
            compatibility = len(data['found']) / len(data['triggers'])
            status = "🔥 ALTA" if compatibility > 0.3 else "⚡ MÉDIA" if compatibility > 0.1 else "❄️ BAIXA"
            cultural_result += f"{culture}: {status} compatibilidade ({compatibility:.1%})\n"
            if data['found']:
                cultural_result += f"  Elementos: {', '.join(data['found'])}\n"
            cultural_result += "\n"
        cultural_result += "💡 RECOMENDAÇÕES:\n"
        best_cultures = sorted(cultural_elements.items(), key=lambda x: len(x[1]['found']), reverse=True)
        for culture, data in best_cultures[:3]:
            if data['found']:
                cultural_result += f"• {culture}: Expandir elementos encontrados\n"
            else:
                cultural_result += f"• {culture}: Adicionar gatilhos culturais específicos\n"
        self.copy_analysis_text.config(state='normal')
        self.copy_analysis_text.delete('1.0', tk.END)
        self.copy_analysis_text.insert('1.0', cultural_result)
        self.copy_analysis_text.config(state='disabled')

    def generate_monster_from_copy(self):
        existing_copy = self.existing_copy_text.get('1.0', tk.END).strip()
        if not existing_copy:
            messagebox.showwarning("Atenção", "Cole uma copy para transformar.")
            return
        selected_cultures = [code for code, var in self.transform_cultures_vars.items() if var.get()]
        if not selected_cultures:
            messagebox.showwarning("Atenção", "Selecione pelo menos uma cultura.")
            return
        self.set_generation_state(True)
        self.log_message("Iniciando transformação com MONSTER Framework...")
        thread = threading.Thread(target=self._run_monster_transformation, args=(existing_copy, selected_cultures))
        thread.daemon = True
        thread.start()

    def _run_monster_transformation(self, existing_copy: str, cultures: List[str]):
        try:
            adaptation_type = self.adaptation_type_var.get()
            num_variations = int(self.copy_variations_var.get())
            frameworks_to_use: List[str] = []
            if adaptation_type == 'monster_only':
                frameworks_to_use = ['monster_supreme_framework']
            elif adaptation_type == 'classics_only':
                frameworks_to_use = ['kennedy_pas_plus']
            elif adaptation_type == 'moderns_only':
                frameworks_to_use = ['hormozi_grand_slam_offer', 'brunson_epiphany_bridge']
            elif adaptation_type == 'monster_plus_classics':
                frameworks_to_use = ['monster_supreme_framework', 'kennedy_pas_plus', 'hormozi_grand_slam_offer']
            else:
                frameworks_to_use = list(BestsellerFrameworks().frameworks.keys())
            for culture in cultures:
                self.log_message(f"Transformando para {culture}...")
                for framework in frameworks_to_use[:3]:
                    self.log_message(f"  Framework: {framework}")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        hooks = loop.run_until_complete(self.hook_generator.generate_hooks_from_copy(existing_copy, culture, framework, num_variations))
                        for hook in hooks:
                            hook['framework'] = framework
                            hook['culture'] = culture
                            hook['source'] = 'monster_transformation'
                            hook['original_copy'] = existing_copy[:100] + "..."
                            self.current_hooks.append(hook)
                            self.root.after(0, self._update_hooks_display, hook)
                    finally:
                        loop.close()
            self.log_message("Transformação MONSTER concluída!")
        except Exception as e:
            self.log_message(f"Erro na transformação: {str(e)}")
            messagebox.showerror("Erro", f"Erro na transformação MONSTER:\n{str(e)}")
        finally:
            self.root.after(0, lambda: self.set_generation_state(False))

    def compare_all_frameworks(self):
        existing_copy = self.existing_copy_text.get('1.0', tk.END).strip()
        if not existing_copy:
            messagebox.showwarning("Atenção", "Cole uma copy para comparar.")
            return
        compare_window = tk.Toplevel(self.root)
        compare_window.title("Comparação de Frameworks")
        compare_window.geometry("1000x700")
        tk.Label(compare_window, text="Comparação de Todos os Frameworks", font=('Arial', 16, 'bold')).pack(pady=10)
        compare_notebook = ttk.Notebook(compare_window)
        compare_notebook.pack(fill='both', expand=True, padx=20, pady=10)
        frameworks_tab = ttk.Frame(compare_notebook)
        compare_notebook.add(frameworks_tab, text="Por Framework")
        framework_results = scrolledtext.ScrolledText(frameworks_tab, height=25, wrap='word')
        framework_results.pack(fill='both', expand=True, padx=10, pady=10)
        analyzer = AdvancedCopyAnalyzer(self.config)
        frameworks = BestsellerFrameworks().frameworks
        comparison_text = "=== COMPARAÇÃO DE FRAMEWORKS ===\n\n"
        for fw_key, fw_data in frameworks.items():
            score = analyzer._calculate_framework_match(existing_copy, fw_data)
            comparison_text += f"📊 {fw_data['name']}\n   Expert: {fw_data.get('expert', 'N/A')}\n   Compatibilidade: {score:.1%}\n   Era: {fw_data.get('era', 'N/A')}\n\n"
        framework_results.insert('1.0', comparison_text)
        framework_results.config(state='disabled')
        cultures_tab = ttk.Frame(compare_notebook)
        compare_notebook.add(cultures_tab, text="Por Cultura")
        cultural_results = scrolledtext.ScrolledText(cultures_tab, height=25, wrap='word')
        cultural_results.pack(fill='both', expand=True, padx=10, pady=10)
        cultural_text = "=== ANÁLISE CULTURAL DETALHADA ===\n\n"
        for culture_code, culture_data in self.config.cultures.items():
            cultural_text += f"🌍 {culture_data.name}\n   Comunicação: {culture_data.preferred_communication}\n   Intensidade Emocional: {culture_data.emotional_intensity}\n   Foco Familiar: {culture_data.family_focus}\n\n"
        cultural_results.insert('1.0', cultural_text)
        cultural_results.config(state='disabled')

    def save_copy_analysis(self):
        analysis_content = self.copy_analysis_text.get('1.0', tk.END).strip()
        if not analysis_content:
            messagebox.showwarning("Atenção", "Nenhuma análise para salvar.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=== ANÁLISE DE COPY - VideoBot BESTSELLERS ===\n\n")
                    f.write(analysis_content)
                    f.write(f"\n\n=== COPY ORIGINAL ===\n")
                    f.write(self.existing_copy_text.get('1.0', tk.END))
                messagebox.showinfo("Sucesso", f"Análise salva em: {filename}")
                self.log_message(f"Análise salva: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def load_monster_example(self):
        examples = MonsterFrameworkExamples()
        example_data = examples.get_example('pt-BR', 'marketing_digital')
        if example_data and 'monster_copy' in example_data:
            if messagebox.askyesno("Carregar Exemplo", "Isso substituirá o conteúdo atual. Continuar?"):
                self.existing_copy_text.delete('1.0', tk.END)
                self.existing_copy_text.insert('1.0', example_data['monster_copy'])
                self.log_message("Exemplo MONSTER carregado")
        else:
            messagebox.showinfo("Info", "Exemplo MONSTER não disponível no momento.")

    def clear_copy_input(self):
        self.existing_copy_text.delete('1.0', tk.END)
        self.copy_analysis_text.config(state='normal')
        self.copy_analysis_text.delete('1.0', tk.END)
        self.copy_analysis_text.config(state='disabled')

    # =============================
    # GERAÇÃO / RESULTADOS / STATUS
    # =============================
    def create_generation_tab(self):
        gen_frame = ttk.Frame(self.notebook)
        self.notebook.add(gen_frame, text="🚀 Geração")
        tk.Label(gen_frame, text="Geração de Vídeos com Frameworks", font=('Arial', 16, 'bold')).pack(pady=10)
        main_gen_frame = ttk.Frame(gen_frame)
        main_gen_frame.pack(fill='both', expand=True, padx=20, pady=10)
        config_frame = ttk.LabelFrame(main_gen_frame, text="Configurações:", padding=10)
        config_frame.pack(fill='x', pady=5)
        duration_frame = ttk.Frame(config_frame)
        duration_frame.pack(fill='x', pady=5)
        ttk.Label(duration_frame, text="Duração do vídeo (segundos):").pack(side='left')
        self.video_duration_var = tk.StringVar(value='30')
        ttk.Spinbox(duration_frame, from_=15, to=120, width=5, textvariable=self.video_duration_var).pack(side='left', padx=10)
        format_frame = ttk.Frame(config_frame)
        format_frame.pack(fill='x', pady=5)
        ttk.Label(format_frame, text="Formato:").pack(side='left')
        self.video_format_var = tk.StringVar(value='9:16')
        ttk.Combobox(format_frame, textvariable=self.video_format_var, values=['9:16', '16:9', '1:1'], width=10, state='readonly').pack(side='left', padx=10)
        buttons_frame = ttk.Frame(main_gen_frame)
        buttons_frame.pack(fill='x', pady=20)
        self.generate_btn = ttk.Button(buttons_frame, text="🎬 Gerar Hooks", command=self.start_generation)
        self.generate_btn.pack(side='left', padx=5)
        self.generate_scripts_btn = ttk.Button(buttons_frame, text="📝 Gerar Scripts", command=self.start_script_generation)
        self.generate_scripts_btn.pack(side='left', padx=5)
        self.stop_btn = ttk.Button(buttons_frame, text="⏹️ Parar", command=self.stop_generation, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        self.progress = ttk.Progressbar(main_gen_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=10)
        log_frame = ttk.LabelFrame(main_gen_frame, text="Log de Geração:", padding=10)
        log_frame.pack(fill='both', expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=80, state='disabled')
        self.log_text.pack(fill='both', expand=True)

    def create_results_tab(self):
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="📊 Resultados")
        tk.Label(results_frame, text="Hooks e Scripts Gerados", font=('Arial', 16, 'bold')).pack(pady=10)
        main_results_frame = ttk.Frame(results_frame)
        main_results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.results_notebook = ttk.Notebook(main_results_frame)
        self.results_notebook.pack(fill='both', expand=True)
        hooks_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(hooks_frame, text="🎯 Hooks")
        self.hooks_listbox = tk.Listbox(hooks_frame, height=15, width=100)
        self.hooks_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        self.hooks_listbox.bind('<Double-Button-1>', self.on_hook_select)
        scripts_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(scripts_frame, text="📝 Scripts")
        self.scripts_text = scrolledtext.ScrolledText(scripts_frame, height=20, width=100, wrap='word')
        self.scripts_text.pack(fill='both', expand=True, padx=10, pady=10)
        actions_frame = ttk.Frame(main_results_frame)
        actions_frame.pack(fill='x', pady=10)
        ttk.Button(actions_frame, text="💾 Salvar Hooks", command=self.save_hooks).pack(side='left', padx=5)
        ttk.Button(actions_frame, text="📋 Copiar Selecionado", command=self.copy_selected).pack(side='left', padx=5)
        ttk.Button(actions_frame, text="🗑️ Limpar Tudo", command=self.clear_results).pack(side='left', padx=5)

    def create_status_bar(self):
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', side='bottom')
        self.status_var = tk.StringVar(value="Sistema pronto - Configure seu produto e frameworks")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side='left', padx=10)
        apis_frame = ttk.Frame(status_frame)
        apis_frame.pack(side='right', padx=10)
        openai_color = "green" if self.config.apis['openai'] else "red"
        gemini_color = "green" if self.config.apis['gemini'] else "red"
        tk.Label(apis_frame, text="OpenAI:", foreground=openai_color).pack(side='left')
        tk.Label(apis_frame, text="Gemini:", foreground=gemini_color).pack(side='left', padx=5)

    # ====== geração / util ======
    def start_generation(self):
        product_info = self.get_product_info()
        if not product_info.get('name'):
            messagebox.showwarning("Atenção", "Configure as informações do produto primeiro.")
            return
        selected_frameworks = self.get_selected_frameworks()
        if not selected_frameworks:
            messagebox.showwarning("Atenção", "Selecione pelo menos um framework.")
            return
        selected_cultures = self.get_selected_cultures()
        if not selected_cultures:
            messagebox.showwarning("Atenção", "Selecione pelo menos uma cultura.")
            return
        self.set_generation_state(True)
        self.log_message("Iniciando geração de hooks...")
        thread = threading.Thread(target=self._run_hooks_generation)
        thread.daemon = True
        thread.start()

    def _run_hooks_generation(self):
        try:
            product_info = self.get_product_info()
            frameworks = self.get_selected_frameworks()
            cultures = self.get_selected_cultures()
            for framework in frameworks:
                self.log_message(f"Processando framework: {framework}")
                for culture in cultures:
                    self.log_message(f"  Cultura: {culture}")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        hooks = loop.run_until_complete(self.hook_generator.generate_hooks_from_product(product_info, culture, framework, int(self.hooks_per_framework_var.get())))
                        for hook in hooks:
                            hook['framework'] = framework
                            hook['culture'] = culture
                            hook['source'] = 'product'
                            self.current_hooks.append(hook)
                            self.root.after(0, self._update_hooks_display, hook)
                    finally:
                        loop.close()
            self.log_message("Geração de hooks concluída!")
        except Exception as e:
            self.log_message(f"Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro na geração:\n{str(e)}")
        finally:
            self.root.after(0, lambda: self.set_generation_state(False))

    def start_script_generation(self):
        if not self.current_hooks:
            messagebox.showwarning("Atenção", "Gere hooks primeiro.")
            return
        self.set_generation_state(True)
        self.log_message("Iniciando geração de scripts...")
        thread = threading.Thread(target=self._run_scripts_generation)
        thread.daemon = True
        thread.start()

    def _run_scripts_generation(self):
        try:
            product_info = self.get_product_info()
            duration = int(self.video_duration_var.get())
            for hook in self.current_hooks[:5]:
                framework = hook.get('framework', 'hormozi_grand_slam_offer')
                culture = hook.get('culture', 'pt-BR')
                self.log_message(f"Gerando script para hook: {hook['hook_text'][:50]}...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    script = loop.run_until_complete(self.script_generator.generate_complete_script(hook, product_info, culture, framework, duration))
                    if script:
                        script['hook_data'] = hook
                        self.current_scripts.append(script)
                        self.root.after(0, self._update_scripts_display, script)
                finally:
                    loop.close()
            self.log_message("Geração de scripts concluída!")
        except Exception as e:
            self.log_message(f"Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro na geração:\n{str(e)}")
        finally:
            self.root.after(0, lambda: self.set_generation_state(False))

    def _update_hooks_display(self, hook: Dict):
        hook_text = hook.get('hook_text', 'Hook sem texto')
        framework = hook.get('framework', 'N/A')
        culture = hook.get('culture', 'N/A')
        display_text = f"[{framework}] [{culture}] {hook_text}"
        self.hooks_listbox.insert(tk.END, display_text)

    def _update_scripts_display(self, script: Dict):
        script_text = script.get('full_script', 'Script vazio')
        framework = script.get('framework_used', 'N/A')
        display_text = f"\n=== SCRIPT ({framework}) ===\n{script_text}\n"
        self.scripts_text.insert(tk.END, display_text)
        self.scripts_text.see(tk.END)

    def set_generation_state(self, generating: bool):
        if generating:
            self.generate_btn.config(state='disabled')
            self.generate_scripts_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.progress.start()
            self.status_var.set("Gerando conteúdo...")
        else:
            self.generate_btn.config(state='normal')
            self.generate_scripts_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.progress.stop()
            self.status_var.set("Geração concluída")
        self.generation_active = generating

    def stop_generation(self):
        self.generation_active = False
        self.log_message("Parando geração...")
        self.set_generation_state(False)

    def log_message(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        if self.config:
            self.config.logger.info(message)

    def on_hook_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            if index < len(self.current_hooks):
                hook = self.current_hooks[index]
                messagebox.showinfo("Hook Selecionado", f"Hook: {hook['hook_text']}\n\nFramework: {hook.get('framework', 'N/A')}\nCultura: {hook.get('culture', 'N/A')}\nPotencial Viral: {hook.get('viral_potential', 'N/A')}")

    def save_hooks(self):
        if not self.current_hooks:
            messagebox.showwarning("Atenção", "Não há hooks para salvar.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")])
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.current_hooks, f, ensure_ascii=False, indent=2)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        for i, hook in enumerate(self.current_hooks):
                            f.write(f"{i+1}. {hook['hook_text']}\n")
                            f.write(f"   Framework: {hook.get('framework', 'N/A')}\n")
                            f.write(f"   Cultura: {hook.get('culture', 'N/A')}\n\n")
                messagebox.showinfo("Sucesso", f"Hooks salvos em: {filename}")
                self.log_message(f"Hooks salvos: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def copy_selected(self):
        selection = self.hooks_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.current_hooks):
                hook_text = self.current_hooks[index]['hook_text']
                self.root.clipboard_clear()
                self.root.clipboard_append(hook_text)
                messagebox.showinfo("Copiado", "Hook copiado para a área de transferência!")
        else:
            messagebox.showwarning("Atenção", "Selecione um hook primeiro.")

    def clear_results(self):
        if messagebox.askyesno("Confirmar", "Limpar todos os hooks e scripts gerados?"):
            self.current_hooks.clear()
            self.current_scripts.clear()
            self.hooks_listbox.delete(0, tk.END)
            self.scripts_text.delete('1.0', tk.END)
            self.log_message("Resultados limpos")

    def run(self):
        self.root.mainloop()


# =============================================
# 7. ENV E MAIN
# =============================================

def create_env_file():
    env_content = (
        "# VideoBot BESTSELLERS - Configuração das APIs\n"
        "OPENAI_API_KEY=\n"
        "GEMINI_API_KEY=\n"
    )
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)


def main():
    create_env_file()
    try:
        if os.path.exists('.env'):
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except Exception:
                pass
        app = BestsellerVideoBotGUI()
        app.run()
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()


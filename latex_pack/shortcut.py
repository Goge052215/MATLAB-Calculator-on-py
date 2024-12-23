import re

class ExpressionShortcuts:
    """
    A class containing mappings for mathematical expression shortcuts to their LaTeX equivalents.
    """
    
    # Derivative shortcuts
    DERIVATIVE_SHORTCUTS = {
        'd/dx': r'\frac{d}{dx}',
        'd/dy': r'\frac{d}{dy}',
        'd/dt': r'\frac{d}{dt}',
        'd2/dx2': r'\frac{d^2}{dx^2}',
        'd3/dx3': r'\frac{d^3}{dx^3}',
        'd4/dx4': r'\frac{d^4}{dx^4}',
        'd5/dx5': r'\frac{d^5}{dx^5}'
    }
    
    # Integral shortcuts
    INTEGRAL_SHORTCUTS = {
        'int': r'\int',
        'integral': r'\int',
        'iint': r'\iint',  # Double integral
        'iiint': r'\iiint',  # Triple integral
        'oint': r'\oint',  # Contour integral
    }
    
    # Function shortcuts
    FUNCTION_SHORTCUTS = {
        'sqrt': r'\sqrt',
        'root': r'\sqrt',
        'abs': r'\left|#\right|',  # # will be replaced with the argument
        'sin': r'\sin',
        'cos': r'\cos',
        'tan': r'\tan',
        'csc': r'\csc',
        'sec': r'\sec',
        'cot': r'\cot',
        'arcsin': r'\arcsin',
        'arccos': r'\arccos',
        'arctan': r'\arctan',
        'ln': r'\ln',
        'lg': r'\log',
        'log': r'\log',
        'log10': r'\log_{10}',  # Added for explicit base-10 log
        'log2': r'\log_{2}'     # Added for base-2 log
    }
    
    # Fraction shortcuts
    FRACTION_SHORTCUTS = {
        '//': r'\frac{#}{#}',  # #'s will be replaced with numerator and denominator
    }
    
    # Greek letters
    GREEK_SHORTCUTS = {
        'alpha': r'\alpha',
        'beta': r'\beta',
        'gamma': r'\gamma',
        'delta': r'\delta',
        'epsilon': r'\epsilon',
        'zeta': r'\zeta',
        'eta': r'\eta',
        'theta': r'\theta',
        'iota': r'\iota',
        'kappa': r'\kappa',
        'lambda': r'\lambda',
        'mu': r'\mu',
        'nu': r'\nu',
        'xi': r'\xi',
        'pi': r'\pi',
        'rho': r'\rho',
        'sigma': r'\sigma',
        'tau': r'\tau',
        'upsilon': r'\upsilon',
        'phi': r'\phi',
        'chi': r'\chi',
        'psi': r'\psi',
        'omega': r'\omega',
    }
    
    # Operator shortcuts
    OPERATOR_SHORTCUTS = {
        'sum': r'\sum',
        'prod': r'\prod',
        'lim': r'\lim',
        'to': r'\to',
        'rightarrow': r'\rightarrow',
        'leftarrow': r'\leftarrow',
        'infty': r'\infty',
        'infinity': r'\infty',
    }
    
    @classmethod
    def get_all_shortcuts(cls):
        """
        Get all shortcuts combined into a single dictionary.
        
        Returns:
            dict: Combined dictionary of all shortcuts
        """
        all_shortcuts = {}
        all_shortcuts.update(cls.DERIVATIVE_SHORTCUTS)
        all_shortcuts.update(cls.INTEGRAL_SHORTCUTS)
        all_shortcuts.update(cls.FUNCTION_SHORTCUTS)
        all_shortcuts.update(cls.FRACTION_SHORTCUTS)
        all_shortcuts.update(cls.GREEK_SHORTCUTS)
        all_shortcuts.update(cls.OPERATOR_SHORTCUTS)
        return all_shortcuts
    
    @classmethod
    def convert_shortcut(cls, text):
        """
        Convert shortcuts in text to their LaTeX equivalents.
        
        Args:
            text (str): Input text containing shortcuts
            
        Returns:
            str: Text with shortcuts converted to LaTeX
        """
        result = text
        
        # Handle higher-order derivative notation (e.g., "d2/dx2 x^2")
        if text.startswith('d') and ('/' in text or text[1:2].isdigit()):
            parts = text.split(' ', 1)
            if len(parts) == 2:
                derivative_part, function_part = parts
                
                # Handle different derivative notations
                if '/' in derivative_part:
                    # Handle d/dx or d2/dx2 notation
                    order_match = re.match(r'd(\d*)/d([xyz])(\d*)', derivative_part)
                    if order_match:
                        order = order_match.group(1) or '1'
                        var = order_match.group(2)
                        result = f"\\frac{{d^{order}}}{{d{var}^{order}}} {function_part}"
                else:
                    # Handle d2x or dx notation
                    order_match = re.match(r'd(\d*)([xyz])', derivative_part)
                    if order_match:
                        order = order_match.group(1) or '1'
                        var = order_match.group(2)
                        result = f"\\frac{{d^{order}}}{{d{var}^{order}}} {function_part}"
                
                return result
        
        # Handle other shortcuts
        shortcuts = cls.get_all_shortcuts()
        for shortcut, latex in shortcuts.items():
            if shortcut in result and '#' not in latex:
                result = result.replace(shortcut, latex)
        
        return result

import re
import sympy as sy

class SympyToMatlab:
    def __init__(self):
        import logging
        self.logger = logging.getLogger(__name__)

    def sympy_to_matlab(self, expr):
        """Convert SymPy expression to MATLAB format."""
        self.logger.debug(f"Converting SymPy expression to MATLAB: {expr}")
        
        try:
            # Handle list expressions
            expr = self._handle_list_expression(expr)
            
            # Handle special expression types
            if isinstance(expr, sy.Integral):
                result = self._handle_integral(expr)
                self.logger.debug(f"Handled Integral expression. Result: {result}")
                return result
            elif isinstance(expr, sy.Derivative):
                result = self._handle_derivative(expr)
                self.logger.debug(f"Handled Derivative expression. Result: {result}")
                return result
            elif isinstance(expr, sy.Eq):
                result = self._handle_equation(expr)
                self.logger.debug(f"Handled Eq expression. Result: {result}")
                return result
            elif isinstance(expr, sy.Function):
                result = self._handle_function(expr)
                self.logger.debug(f"Handled Function expression. Result: {result}")
                return result
            
            # For other expressions, convert to string and process
            result = self._process_expression_string(expr)
            self.logger.debug(f"Processed expression string. Result: {result}")
            return str(result)  # Ensure the result is a string
        
        except Exception as e:
            self.logger.error(f"Error in sympy_to_matlab conversion: {e}", exc_info=True)
            raise

    def _handle_list_expression(self, expr):
        """Handle list expressions."""
        if isinstance(expr, list):
            if not expr:
                raise ValueError("Empty expression list")
            return expr[0]
        return expr
        
    def _handle_integral(self, expr):
        """Handle integral expressions."""
        self.logger.debug(f"Handling integral expression: {expr}")
        
        # Get the expression being integrated
        integrand = expr.args[0]
        
        # Recursively handle nested integrals
        if isinstance(integrand, sy.Integral):
            integrand_str = self.sympy_to_matlab(integrand)
        else:
            integrand_str = self.sympy_to_str(integrand)
        
        # Get the integration variable and limits
        var_info = expr.limits[0]
        
        if len(var_info) == 1:
            # Indefinite integral
            var = var_info[0]
            matlab_integral = f"int({integrand_str}, '{var}')"
        else:
            # Definite integral
            var, lower, upper = var_info
            matlab_integral = f"int({integrand_str}, '{var}', {lower}, {upper})"
        
        self.logger.debug(f"Converted integral to MATLAB syntax: {matlab_integral}")
        return matlab_integral

    def _handle_derivative(self, expr):
        """Handle derivative expressions."""
        self.logger.debug(f"Handling derivative expression: {expr}")
        
        # Get the expression being differentiated
        func_expr = expr.expr
        
        # Extract the variable and order of differentiation
        var_info = expr.variables[0]
        
        # Check if var_info is a tuple (indicating higher-order derivative)
        if isinstance(var_info, tuple):
            var, order = var_info
        else:
            var = var_info
            order = expr.derivative_count  # Use derivative_count for the order
        
        # Convert the function part
        func_str = self.sympy_to_matlab(func_expr)
        
        # Create MATLAB derivative expression
        if order == 1:
            matlab_derivative = f"diff({func_str}, '{var}')"
        else:
            matlab_derivative = f"diff({func_str}, '{var}', {order})"
        
        self.logger.debug(f"Converted derivative to MATLAB syntax: {matlab_derivative}")
        return matlab_derivative

    def _handle_equation(self, expr):
        """Handle equation expressions."""
        self.logger.debug(f"Handling equation expression: {expr}")
        # Implement equation handling if necessary
        # For example: lhs = rhs
        lhs, rhs = expr.lhs, expr.rhs
        matlab_eq = f"{self.sympy_to_matlab(lhs)} == {self.sympy_to_matlab(rhs)}"
        return matlab_eq

    def _handle_function(self, expr):
        """Handle function expressions like sin, cos, etc."""
        self.logger.debug(f"Handling function expression: {expr}")
        
        func_name = expr.func.__name__
        args = expr.args
        
        # Handle special functions if necessary
        function_mappings = {
            'sin': 'sin',
            'cos': 'cos',
            'tan': 'tan',
            'csc': 'csc',
            'sec': 'sec',
            'cot': 'cot',
            'arcsin': 'asin',
            'arccos': 'acos',
            'arctan': 'atan',
            'ln': 'log',      # MATLAB uses log for natural logarithm
            'log10': 'log10',
            'log2': 'log2',
            # Add more mappings as needed
        }
        
        matlab_func = function_mappings.get(func_name, func_name)
        matlab_args = ', '.join([self.sympy_to_matlab(arg) for arg in args])
        
        # Handle absolute value separately if needed
        if func_name == 'abs':
            matlab_expression = f"abs({matlab_args})"
        else:
            matlab_expression = f"{matlab_func}({matlab_args})"
        
        self.logger.debug(f"Converted function to MATLAB syntax: {matlab_expression}")
        return matlab_expression

    def sympy_to_str(self, expr):
        """Convert SymPy expression to string."""
        return str(expr)

    def _process_expression_string(self, expr):
        """Process a general expression string."""
        self.logger.debug(f"Processing general expression: {expr}")
        
        # Convert the SymPy expression to a string
        expr_str = str(expr)
        
        # Define a dictionary for replacements
        replacements = {
            '**': '^',  # Replace exponentiation for symbolic expressions
            # Do NOT replace '*' or '/' to avoid issues with symbolic expressions
        }
        
        # Apply replacements
        for sympy_op, matlab_op in replacements.items():
            expr_str = expr_str.replace(sympy_op, matlab_op)
        
        self.logger.debug(f"After replacements: {expr_str}")
        return expr_str
        
    def _is_degree_mode(self):
        """Determine if the calculator is in degree mode."""
        # This method should determine if the calculator is set to degree mode
        # For now, we'll assume radian mode. You can modify this based on your application state.
        return False
        
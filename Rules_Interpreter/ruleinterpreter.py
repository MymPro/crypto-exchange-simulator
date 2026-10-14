class RuleInterpreter():

    def evaluate(self, node, context):
        if isinstance(node, tuple):
            tipo = node[0]

            if tipo == "instruccion":
                return self.evaluate(node[1], context)
            elif tipo == "statement_rule":
                # Evaluamos la condición y luego ejecutamos la acción asociada
                condicion = self.evaluate(node[1], context)
                #accion = self.evaluate(node[2], context)
                return (condicion, node[2])
            elif tipo == 'number':
                return float(node[1])
            elif tipo == "AND":
                return min(self.evaluate(node[1], context), self.evaluate(node[2], context))
            elif tipo == "OR":
                return max(self.evaluate(node[1], context), self.evaluate(node[2], context))

            elif tipo == "grafico":
                history = context.get("price_history", [])
                if len(history) < 2:
                    return 0.0
                lookback = max(1, int(node[1]))
                initial_index = max(0, len(history) - lookback - 1)
                initial_price = history[initial_index]
                if initial_price == 0:
                    return 0.0
                return (history[-1] - initial_price) / initial_price * 100

            elif tipo == "*":
                return self.evaluate(node[1], context) * self.evaluate(node[2], context)

            elif tipo == 'es':
                return 0.9 if self.evaluate(node[1], context) == self.evaluate(node[2], context) else 0.1

            elif tipo == 'no es':
                return 0.9 if self.evaluate(node[1], context) != self.evaluate(node[2], context) else 0.1

            elif tipo == 'menor o igual que':
                return 0.9 if self.evaluate(node[1], context) <= self.evaluate(node[2], context) else 0.1

            elif tipo == 'menor que':
                return 0.9 if self.evaluate(node[1], context) < self.evaluate(node[2], context) else 0.1

            elif tipo == 'mayor o igual que':
                return 0.9 if self.evaluate(node[1], context) >= self.evaluate(node[2], context) else 0.1

            elif tipo == 'mayor que':
                return 0.9 if self.evaluate(node[1], context) > self.evaluate(node[2], context) else 0.1

            elif tipo == "accion":
                return node
            elif tipo == "creencia":
                # Aquí accedemos a la creencia en el diccionario `beliefs`
                creencia_name = node[1]
                if creencia_name in context["beliefs"]:
                    return context["beliefs"][creencia_name]
                else:
                    print(f"Creencia {creencia_name} no encontrada.")
                    return None
            elif tipo == "variable":
                # Las categorías (alto, positivo, etc.) se representan por su
                # propio texto cuando no son una variable presente en contexto.
                var_name = node[1]
                return context.get(var_name, var_name)

            else:
                print(f"Tipo desconocido: {tipo}")
                return None
        else:
            return node

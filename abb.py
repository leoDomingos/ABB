# Aluno: Leonardo Domingos
# DRE: 120168324





class Registro:
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str = ""):

        self.cpf = cpf  # primary key
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.deletado = False  # flag
    

    def __lt__(self, outro):
        """Comparação para ordenação na ABB baseada no CPF"""
        return self.cpf < outro.cpf
    def __eq__(self, outro):
        """Comparação de igualdade baseada no CPF"""
        return self.cpf == outro.cpf

    def __str__(self):

        return f"CPF: {self.cpf}, Nome: {self.nome}, Nascimento: {self.data_nascimento}, Endereço: {self.endereco}"
    
    def marcar_como_deletado(self):
        self.deletado = True

    
    def esta_deletado(self):
        return self.deletado



class NoABB:
    def __init__(self, registro: Registro, indice_edl: int):
        self.registro = registro
        self.indice_edl = indice_edl #
        self.esquerda = None
        self.direita = None



class ABB:
    def __init__(self):
        self.raiz = None
    

    def __init__(self, iterador=None):

        """construtor que pode receber um iterador para inicialização"""
        self.raiz = None
        if iterador is not None:
            for item in iterador:
                self.inserir(item['registro'], item['indice'])
    

    def inserir(self, registro: Registro, indice_edl: int) -> bool:
        """coloca um novo nó na árvore com o registro e índice na EDL"""
        novo_no = NoABB(registro, indice_edl)
        
        if self.raiz is None:
            self.raiz = novo_no
            return True
        
        atual = self.raiz

        while True:
            if registro == atual.registro:
                return False  # registro ja existe
            
            elif registro < atual.registro:
                if atual.esquerda is None:
                    atual.esquerda = novo_no
                    return True
                atual = atual.esquerda

            else:
                if atual.direita is None:
                    atual.direita = novo_no
                    return True
                atual = atual.direita
    



    def buscar(self, cpf: str) -> tuple:
        """busca um registro pelo cpf e retorna o no e o índice na EDL"""
        atual = self.raiz
        while atual is not None:
            if cpf == atual.registro.cpf:
                return atual.registro, atual.indice_edl
            elif cpf < atual.registro.cpf:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None, -1
    
    def remover(self, cpf: str) -> bool:
        """remove um no da árvore pelo cpf"""

        pai = None
        atual = self.raiz
        
        # encontrando o nó a ser removido
        while atual is not None and atual.registro.cpf != cpf:
            pai = atual
            if cpf < atual.registro.cpf:
                atual = atual.esquerda
            else:
                atual = atual.direita
        
        if atual is None:
            return False  # no nao existe
        

        # Caso 1: não tem filhos
        if atual.esquerda is None and atual.direita is None:
            if pai is None:
                self.raiz = None
            elif pai.esquerda == atual:
                pai.esquerda = None
            else:
                pai.direita = None
        

        # Caso 2: filho único
        elif atual.esquerda is None or atual.direita is None:
            filho = atual.esquerda if atual.esquerda is not None else atual.direita
            if pai is None:
                self.raiz = filho
            elif pai.esquerda == atual:
                pai.esquerda = filho
            else:
                pai.direita = filho
        

        # Caso 3: casal de filhos
        else:
            sucessor_pai = atual
            sucessor = atual.direita
            
            while sucessor.esquerda is not None:

                sucessor_pai = sucessor
                sucessor = sucessor.esquerda
            
            # trocar os valores do nó atual com o sucessor
            atual.registro, sucessor.registro = sucessor.registro, atual.registro
            atual.indice_edl, sucessor.indice_edl = sucessor.indice_edl, atual.indice_edl
            
            # retirar o sucessor
            if sucessor_pai.esquerda == sucessor:
                sucessor_pai.esquerda = sucessor.direita
            else:
                sucessor_pai.direita = sucessor.direita
        
        return True
    
    def percurso_em_ordem(self, no=None, resultado=None):
        """retorna os registros em ordem crescente de CPF"""

        if resultado is None:
            resultado = []
        if no is None:
            no = self.raiz
            if no is None:
                return resultado
        
        if no.esquerda is not None:
            self.percurso_em_ordem(no.esquerda, resultado)
        
        resultado.append((no.registro, no.indice_edl))
        
        if no.direita is not None:
            self.percurso_em_ordem(no.direita, resultado)
        
        return resultado
    


    def percurso_pre_ordem(self, no=None, resultado=None):
        """Retorna os registros em pre-ordem"""
        if resultado is None:
            resultado = []
        if no is None:
            no = self.raiz
            if no is None:
                return resultado
        

        resultado.append((no.registro, no.indice_edl))
        
        if no.esquerda is not None:
            self.percurso_pre_ordem(no.esquerda, resultado)
        
        if no.direita is not None:
            self.percurso_pre_ordem(no.direita, resultado)
        
        return resultado
    


    def percurso_pos_ordem(self, no=None, resultado=None):

        """retorna os registros em pos ordem"""
        if resultado is None:
            resultado = []

        if no is None:
            no = self.raiz
            if no is None:

                return resultado
        
        if no.esquerda is not None:
            self.percurso_pos_ordem(no.esquerda, resultado)

        
        if no.direita is not None:
            self.percurso_pos_ordem(no.direita, resultado)
        
        resultado.append((no.registro, no.indice_edl))
        
        return resultado
    

    def percurso_em_largura(self):
        """retorna os registros em nível (largura)"""
        if self.raiz is None:
            return []
        
        resultado = []
        fila = [self.raiz]
        
        while fila:
            no = fila.pop(0)
            resultado.append((no.registro, no.indice_edl))
            
            if no.esquerda is not None:
                fila.append(no.esquerda)
            

            if no.direita is not None:
                fila.append(no.direita)
        
        return resultado
    


    def __deepcopy__(self, memo=None):
        """deep copy da ab"""
        if memo is None:
            memo = {}
        
        nova_abb = ABB()
        if self.raiz is not None:
            nova_abb.raiz = self._copiar_no(self.raiz, memo)
        return nova_abb

    def _copiar_no(self, no, memo):
        """Método auxiliar para copiar um nó e seus filhos"""
        if no is None:
            return None
        
        
        # verifcia se o nó já foi copiado
        if id(no) in memo:
            return memo[id(no)]
        

        novo_no = NoABB(no.registro, no.indice_edl)
        memo[id(no)] = novo_no  # armazena na memoização antes de copiar os filhos
        
        novo_no.esquerda = self._copiar_no(no.esquerda, memo)
        novo_no.direita = self._copiar_no(no.direita, memo)
        
        return novo_no



class EDL:
    """EDL para simular o arquivo de registros"""
    def __init__(self):
        self.registros = []
    

    def inserir(self, registro: Registro) -> int:
        """Insere um registro na EDL e retorna seu índice"""
        self.registros.append(registro)
        return len(self.registros) - 1
    

    def buscar_por_indice(self, indice: int) -> Registro:
        """Retorna o registro no índice especificado"""
        if 0 <= indice < len(self.registros):
            return self.registros[indice]
        return None
    

    def remover_por_indice(self, indice: int) -> bool:
        """Marca um registro como deletado pelo índice"""
        if 0 <= indice < len(self.registros):
            self.registros[indice].marcar_como_deletado()
            return True
        return False
    

    def criar_edl_ordenada(self, abb: ABB):
        """Cria uma nova EDL ordenada com base na ABB"""
        registros_ordenados = abb.percurso_em_ordem()
        nova_edl = EDL()
        
        for registro, _ in registros_ordenados:
            nova_edl.inserir(registro)
        
        return nova_edl
    

    def __str__(self):
        return "\n".join(f"{i}: {str(reg)} {'(deletado)' if reg.esta_deletado() else ''}" 
                         for i, reg in enumerate(self.registros))



class SGBD:
    """SGBD simplificado"""
    def __init__(self):
        self.edl = EDL()  # Arquivo de registros
        self.abb = ABB()   # Índice para busca eficiente
    

    def inserir_registro(self, registro: Registro) -> bool:
        """insere um novo registro no sistema"""
        # Verificar se o CPF já existe
        _, indice = self.abb.buscar(registro.cpf)
        if indice != -1:
            return False  # CPF já cadastrado
        
        # Inserir na EDL e depois na ABB
        indice_edl = self.edl.inserir(registro)
        return self.abb.inserir(registro, indice_edl)
    


    def buscar_registro(self, cpf: str) -> Registro:
        """busca um registro pelo CPF"""
        registro, indice = self.abb.buscar(cpf)
        if indice == -1:
            return None
        

        registro_edl = self.edl.buscar_por_indice(indice)
        if registro_edl.esta_deletado():
            return None
        
        return registro_edl



    def remover_registro(self, cpf: str) -> bool:
        """remove um registro pelo CPF (marcação lógica)"""
        registro, indice = self.abb.buscar(cpf)
        if indice == -1:
            return False
        
        # Marcar como deletado na EDL e remover da ABB
        self.edl.remover_por_indice(indice)
        return self.abb.remover(cpf)
    


    def listar_registros_ordenados(self):
        """lista todos os registros ordenados por CPF"""
        registros_ordenados = self.abb.percurso_em_ordem()
        for registro, indice in registros_ordenados:
            reg_edl = self.edl.buscar_por_indice(indice)
            if not reg_edl.esta_deletado():
                print(reg_edl)
    

    def criar_edl_ordenada(self):
        """cria uma nova EDL com registros ordenados por CPF"""
        return self.edl.criar_edl_ordenada(self.abb)
    
    def __str__(self):
        return f"=== EDL ===\n{self.edl}\n\n=== ABB ===\n{self.abb.percurso_em_ordem()}"


def testar_todas_funcionalidades():
    """
    Função que testa todas as funcionalidades exigidas no projeto:
    - Operações básicas da ABB (inserção, busca, remoção)
    - Todos os tipos de percurso (pré-ordem, em ordem, pós-ordem, largura)
    - Construtores especiais (cópia, inicialização com iterador)
    - Integração com a EDL
    - Operações do SGBD completo
    """
    




    print("="*60)
    print("INÍCIO DOS TESTES - VERIFICAÇÃO DE TODAS AS FUNCIONALIDADES")
    print("="*60)
    



    # --------------------------------------------
    # 1. Teste da classe Registro e operador <
    # --------------------------------------------



    print("\n1. TESTANDO CLASSE REGISTRO E OPERADOR DE COMPARAÇÃO")
    reg1 = Registro("111", "João", "01/01/2000")
    reg2 = Registro("222", "Maria", "02/02/2001")
    reg3 = Registro("111", "João Clone", "01/01/2000")  # Mesmo CPF
    
    print(f"- Comparação: 111 < 222? {reg1 < reg2} (Esperado: True)")
    print(f"- Comparação: 222 < 111? {reg2 < reg1} (Esperado: False)")
    print(f"- Igualdade: 111 == 111? {reg1 == reg3} (Esperado: True)")
    print(f"- Igualdade: 111 == 222? {reg1 == reg2} (Esperado: False)")
    



    # --------------------------------------------
    # 2. Teste dos construtores da ABB
    # --------------------------------------------




    print("\n2. TESTANDO CONSTRUTORES DA ABB")
    
    # consturotr vazio
    abb_vazia = ABB()
    print("- ABB vazia criada com sucesso" if abb_vazia.raiz is None 
          else "ERRO: ABB vazia deveria ter raiz None")
    
    # construtor com iterador
    dados = [
        {'registro': Registro("333", "Carlos", "03/03/2002"), 'indice': 0},
        {'registro': Registro("111", "Ana", "04/04/2003"), 'indice': 1},
        {'registro': Registro("222", "Pedro", "05/05/2004"), 'indice': 2}
    ]
    abb_com_iterador = ABB((item for item in dados))  # Usando generator como iterador
    
    # verificar se inseriu todos os elementos
    percurso = abb_com_iterador.percurso_em_ordem()
    print(f"- ABB com iterador tem {len(percurso)} elementos (Esperado: 3)")
    print(f"- Primeiro elemento: {percurso[0][0].cpf} (Esperado: 111)")
    print(f"- Ordem correta: {percurso[0][0].cpf < percurso[1][0].cpf < percurso[2][0].cpf} (Esperado: True)")
    


    import copy
    abb_copia = copy.deepcopy(abb_com_iterador)
    print("- Cópia da ABB criada com sucesso" if abb_copia.raiz is not None 
        else "ERRO: Cópia não deveria ser vazia")


    abb_copia.remover("222")
    print(f"- Original ainda tem o 222? {'222' in [r[0].cpf for r in abb_com_iterador.percurso_em_ordem()]} (Esperado: True)")
    print(f"- Cópia ainda tem o 222? {'222' in [r[0].cpf for r in abb_copia.percurso_em_ordem()]} (Esperado: False)")
    



    # --------------------------------------------
    # 3. Teste das operações básicas da ABB
    # --------------------------------------------



    print("\n3. TESTANDO OPERAÇÕES BÁSICAS DA ABB")
    abb_teste = ABB()
    

    # Inserção
    abb_teste.inserir(Registro("555", "Luiza", "06/06/2005"), 0)
    abb_teste.inserir(Registro("333", "Marcos", "07/07/2006"), 1)
    abb_teste.inserir(Registro("777", "Julia", "08/08/2007"), 2)
    

    percurso = abb_teste.percurso_em_ordem()
    print(f"- ABB após inserções tem {len(percurso)} elementos (Esperado: 3)")
    print(f"- Ordem correta após inserções: {percurso[0][0].cpf}, {percurso[1][0].cpf}, {percurso[2][0].cpf} (Esperado: 333, 555, 777)")
    
    
    # Busca
    registro, indice = abb_teste.buscar("555")
    print(f"- Busca por CPF existente: {registro.nome if registro else 'Não encontrado'} (Esperado: Luiza)")
    registro, indice = abb_teste.buscar("999")
    print(f"- Busca por CPF inexistente: {'Não encontrado' if registro is None else 'ERRO'} (Esperado: Não encontrado)")
    

    # Remoção
    abb_teste.remover("555")
    registro, _ = abb_teste.buscar("555")
    print(f"- Após remoção, CPF 555 existe? {registro is not None} (Esperado: False)")
    percurso = abb_teste.percurso_em_ordem()
    print(f"- Elementos após remoção: {len(percurso)} (Esperado: 2)")
    


    # --------------------------------------------
    # 4. Teste dos percursos da ABB
    # --------------------------------------------



    print("\n4. TESTANDO PERCURSOS DA ABB")
    abb_percursos = ABB()
    registros = [
        ("444", "Davi", "09/09/2008"),
        ("222", "Eva", "10/10/2009"),
        ("666", "Caim", "11/11/2010"),
        ("111", "Abel", "12/12/2011"),
        ("333", "Beto", "13/13/2012"),
        ("555", "Fiona", "14/14/2013"),
        ("777", "Gina", "15/15/2014")
    ]
    

    for i, (cpf, nome, data) in enumerate(registros):
        abb_percursos.inserir(Registro(cpf, nome, data), i)
    
    print("\n- Pré-ordem:")
    pre_ordem = [r[0].cpf for r in abb_percursos.percurso_pre_ordem()]
    print(" ".join(pre_ordem) + " (Raiz -> Esquerda -> Direita)")
    
    print("\n- Em ordem:")
    em_ordem = [r[0].cpf for r in abb_percursos.percurso_em_ordem()]
    print(" ".join(em_ordem) + " (Ordenado crescente)")
    
    print("\n- Pós-ordem:")
    pos_ordem = [r[0].cpf for r in abb_percursos.percurso_pos_ordem()]
    print(" ".join(pos_ordem) + " (Esquerda -> Direita -> Raiz)")
    
    print("\n- Em largura:")
    largura = [r[0].cpf for r in abb_percursos.percurso_em_largura()]
    print(" ".join(largura) + " (Nível a nível)")
    



    # --------------------------------------------
    # 5. Teste da EDL (Estrutura de Dados Linear)
    # --------------------------------------------




    print("\n5. TESTANDO ESTRUTURA DE DADOS LINEAR (EDL)")
    edl = EDL()
    


    # Inserção
    indices = []
    for cpf, nome, data in registros[:3]:  # Inserir 3 registros
        indices.append(edl.inserir(Registro(cpf, nome, data)))
    
    print(f"- EDL tem {len(edl.registros)} registros (Esperado: 3)")
    print(f"- Primeiro registro: {edl.registros[0].nome} (Esperado: Davi)")
    

    # Busca por índice
    reg = edl.buscar_por_indice(1)
    print(f"- Registro no índice 1: {reg.nome if reg else 'ERRO'} (Esperado: Eva)")
    

    # Remoção (marcação lógica)
    edl.remover_por_indice(1)
    reg = edl.buscar_por_indice(1)
    print(f"- Registro 1 após remoção: {'Deletado' if reg.esta_deletado() else 'ERRO'} (Esperado: Deletado)")
    



    # --------------------------------------------
    # 6. Teste do SGBD completo (integração ABB + EDL)
    # --------------------------------------------



    print("\n6. TESTANDO SGBD COMPLETO (ABB + EDL)")
    sgbd = SGBD()
    
    # Inserção


    for cpf, nome, data in registros:
        sgbd.inserir_registro(Registro(cpf, nome, data))
    
    print(f"- Total de registros no SGBD: {len(sgbd.edl.registros)} (Esperado: 7)")
    print(f"- Total de índices na ABB: {len(sgbd.abb.percurso_em_ordem())} (Esperado: 7)")
    



    # Busca eficiente
    print("\n- Busca por CPF 222:")
    reg = sgbd.buscar_registro("222")
    print(f"  Resultado: {reg.nome if reg else 'Não encontrado'} (Esperado: Eva)")
    
    print("\n- Busca por CPF 999 (inexistente):")
    reg = sgbd.buscar_registro("999")
    print(f"  Resultado: {'Não encontrado' if reg is None else 'ERRO'}")
    

    # Remoção
    print("\n- Removendo CPF 333:")
    sgbd.remover_registro("333")
    reg = sgbd.buscar_registro("333")
    print(f"  Após remoção: {'Não encontrado' if reg is None else 'ERRO'}")
    
    # Listagem ordenada
    print("\n- Listagem ordenada por CPF:")
    sgbd.listar_registros_ordenados()
    

    # EDL ordenada
    print("\n- Criando EDL ordenada:")
    edl_ordenada = sgbd.criar_edl_ordenada()
    print("\n".join(f"{i}: {r.cpf}" for i, r in enumerate(edl_ordenada.registros)))
    




    # --------------------------------------------
    # Resultado final dos testes
    # --------------------------------------------



    print("\n" + "="*60)
    print("- Todos os testes foram executados")
    print("="*60)




if __name__ == "__main__":
    # sgbd = SGBD()
    
    # registros = [
    #     Registro("11111111111", "João Silva", "01/01/1990", "Rua A, 123"),
    #     Registro("33333333333", "Maria Souza", "15/05/1985", "Av. B, 456"),
    #     Registro("22222222222", "Carlos Oliveira", "20/10/1978", "Travessa C, 789"),
    #     Registro("55555555555", "Ana Santos", "03/03/1995", "Rua D, 321"),
    #     Registro("44444444444", "Pedro Costa", "12/12/2000", "Av. E, 654"),
    # ]

    
    # for registro in registros:
    #     sgbd.inserir_registro(registro)
    


    # sgbd.listar_registros_ordenados()
    # cpf_busca = "22222222222"
    # registro = sgbd.buscar_registro(cpf_busca)
    # if registro:
    #     print(f"Registro encontrado: {registro}")
    # else:
    #     print(f"Registro com CPF {cpf_busca} não encontrado.")
    # print("\n=== Removendo um registro ===")
    # cpf_remover = "33333333333"
    # if sgbd.remover_rgistro(cpf_remover):
    #     # else:
    # print("\n=== Tentando buscar registro removido ===")
    # reistro = sgbd.buscar_registro(cpf_remover)
    # if registro:
    #     print(f"Registro encontrado: {registro}")
    # else:
    #     print(f"Registro com CPF {cpf_remover} não encontrado.")
    # edl_ordenada = sgbd.criar_edl_ordenada()
    # print(edl_ordenada)
    testar_todas_funcionalidades()
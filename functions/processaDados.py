import math
def processaDados(empregados, fopagMinima, salarioMinimo):
    
    try:
        # Inicializando variáveis
        salario = 0.0
        proLabore = 0.0
        qtdSocios = 0.0
        listaSocios = []
        listaObjetosSocios = []

        # Iterando sobre o dicionário de empregados
        for nome, info in empregados.items():
            profissao = info["profissão"].upper()
            if profissao == "SÓCIO" \
            or profissao == "SOCIO" \
            or profissao == "SÓCIA" \
            or profissao == "SOCIA":
                proLabore += info["salário"]
                qtdSocios += 1.0
                listaSocios.append(nome)
            else:
                salario += info["salário"]

        fgts = salario * 0.08

        novoProLabore = float(fopagMinima) - (salario + fgts)

        proLaboreSocio = novoProLabore / qtdSocios

        if float(proLaboreSocio) < float(salarioMinimo):
            proLaboreSocio = salarioMinimo
        else:
            proLaboreSocio = novoProLabore / qtdSocios

        proLaboreSocio = math.ceil(proLaboreSocio)

        # Iterando sobre a lista de sócios
        for socio in listaSocios:
            # Criando um dicionário para cada sócio e adicionando à lista
            listaObjetosSocios.append({"nomeSocio": socio, "proLabore": proLaboreSocio, "anterior": empregados[socio]['salário']})

        if len(listaObjetosSocios) < 1:
            return {'dados': listaObjetosSocios, 'erro': True}

        return {'dados': listaObjetosSocios, 'erro': False}
    
    except Exception as e:
    
        return {'erro': True, 'mesagem': f"{e} - Tipo do objeto causador do erro: {type(e).__name__}", 'dados': []}
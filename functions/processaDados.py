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
            if info["profissão"] == "Sócio" \
            or info["profissão"] == "Socio" \
            or info["profissão"] == "SÓCIO" \
            or info["profissão"] == "SOCIO" \
            or info["profissão"] == "Sócia" \
            or info["profissão"] == "Socia" \
            or info["profissão"] == "SÓCIA" \
            or info["profissão"] == "SOCIA":
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

        # Iterando sobre a lista de sócios
        for socio in listaSocios:
            # Criando um dicionário para cada sócio e adicionando à lista
            listaObjetosSocios.append({"nomeSocio": socio, "proLabore": proLaboreSocio, "anterior": empregados[socio]['salário']})

        if len(listaObjetosSocios) < 1:
            return {'dados': listaObjetosSocios, 'erro': True}

        return {'dados': listaObjetosSocios, 'erro': False}
    
    except Exception as e:
    
        return {'erro': True, 'mesagem': f"{e} - Tipo do objeto causador do erro: {type(e).__name__}"}
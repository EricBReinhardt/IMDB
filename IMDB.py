import csv

def carregar_filmes(arquivo):
    movies = []
    with open(arquivo, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movies.append(row)
    return movies

movies = carregar_filmes('imdb_top_1000.csv')



def mostrar_titulo(texto):
    print(f"\n{texto}\n" + "-" * 40)

def formatar_dinheiro(valor):
    return f"${float(valor.replace(',', '')):,.0f}"

def buscar_filme_por_titulo(titulo):
    return [movie for movie in movies if titulo.lower() in movie['Series_Title'].lower()]

def buscar_filme_por_genero(generos):
    generos = [g.strip().lower() for g in generos.replace(',', '|').split('|') if g.strip()]
    return [movie for movie in movies 
            if all(g in movie['Genre'].lower().split(', ') for g in generos)]

def exibir_detalhes_filme(movie):
    print(f"{movie['Series_Title']} ({movie['Released_Year']}) - Gênero: {movie['Genre']}")



def top_10_filmes():
    mostrar_titulo("Top 10 Filmes Com Maior Rating")
    for movie in sorted(movies, key=lambda x: float(x['IMDB_Rating']), reverse=True)[:10]:
        exibir_detalhes_filme(movie)
        print(f"Nota: {movie['IMDB_Rating']}\n")

def filmes_100_milhoes():
    mostrar_titulo("Filmes Que Fizeram Mais de 100 Milhões de Dólares")
    for movie in movies:
        if movie['Gross'] and float(movie['Gross'].replace(',', '')) > 100000000:
            exibir_detalhes_filme(movie)
            print(f"Lucro: {formatar_dinheiro(movie['Gross'])}\n")

def comparar_lucro():
    mostrar_titulo("Comparar Lucro de Dois Filmes")
    filme1 = input("Digite o título do primeiro filme: ").strip()
    filme2 = input("Digite o título do segundo filme: ").strip()
    
    resultados1 = buscar_filme_por_titulo(filme1)
    resultados2 = buscar_filme_por_titulo(filme2)
    
    if not resultados1:
        print(f"\nFilme '{filme1}' não encontrado.")
        return
    if not resultados2:
        print(f"\nFilme '{filme2}' não encontrado.")
        return
    
    movie1, movie2 = resultados1[0], resultados2[0]
    
    try:
        lucro1 = float(movie1['Gross'].replace(',', '')) if movie1.get('Gross') else 0
        lucro2 = float(movie2['Gross'].replace(',', '')) if movie2.get('Gross') else 0
    except (ValueError, AttributeError):
        print("\nErro ao ler os valores de lucro. Verifique os dados dos filmes.")
        return
    
    print(f"\nComparação entre:")
    print(f"1. {movie1['Series_Title']} ({movie1['Released_Year']})")
    print(f"   Lucro: {formatar_dinheiro(str(lucro1)) if lucro1 else 'Dado indisponível'}")
    print(f"2. {movie2['Series_Title']} ({movie2['Released_Year']})")
    print(f"   Lucro: {formatar_dinheiro(str(lucro2)) if lucro2 else 'Dado indisponível'}")
    
    if lucro1 and lucro2:
        if lucro1 > lucro2:
            diferenca = formatar_dinheiro(str(lucro1 - lucro2))
            print(f"\n{movie1['Series_Title']} teve lucro maior em {diferenca}")
        elif lucro2 > lucro1:
            diferenca = formatar_dinheiro(str(lucro2 - lucro1))
            print(f"\n{movie2['Series_Title']} teve lucro maior em {diferenca}")
        else:
            print("\nOs filmes tiveram o mesmo lucro.")
    else:
        print("\nNão é possível comparar - dados de lucro incompletos.")

def pesquisar_filme():
    mostrar_titulo("Pesquisa Filme Por Título e Gênero")
    print("1. Pesquisar por título\n2. Pesquisar por gênero\n3. Pesquisar por ambos")
    escolha = input("Escolha uma opção: ")
    
    if escolha == '1':
        titulo = input("Digite o título do filme (ou parte dele): ")
        for movie in buscar_filme_por_titulo(titulo):
            exibir_detalhes_filme(movie)
    elif escolha == '2':
        genero = input("Digite um ou mais gêneros (separados por vírgula ou barra): ")
        for movie in buscar_filme_por_genero(genero):
            exibir_detalhes_filme(movie)
    elif escolha == '3':
        titulo = input("Digite o título do filme (ou parte dele): ")
        genero = input("Digite um ou mais gêneros (separados por vírgula ou barra): ")
        resultados_titulo = buscar_filme_por_titulo(titulo)
        resultados_genero = buscar_filme_por_genero(genero)
        for movie in [m for m in resultados_titulo if m in resultados_genero]:
            exibir_detalhes_filme(movie)

def realizar_operacao_generos(operacao, ano1, ano2):
    generos_ano1 = set()
    generos_ano2 = set()
    
    for movie in movies:
        if movie['Released_Year'] == ano1:
            generos_ano1.update(movie['Genre'].split(', '))
        elif movie['Released_Year'] == ano2:
            generos_ano2.update(movie['Genre'].split(', '))
    
    if operacao == 'união':
        resultado = generos_ano1.union(generos_ano2)
    elif operacao == 'intersecção':
        resultado = generos_ano1.intersection(generos_ano2)
    elif operacao == 'diferença':
        resultado = generos_ano1.difference(generos_ano2)
    else:
        print("Operação inválida.")
        return
    
    print(f"\nResultado da {operacao} de gêneros entre {ano1} e {ano2}:")
    for genero in sorted(resultado):
        print(genero)

def menu_principal():
    while True:
        mostrar_titulo("Menu Principal")
        print("1. Top 10 Filmes Com Maior Rating")
        print("2. Filmes Que Fizeram Mais de 100 Milhões de Dólares")
        print("3. Comparar Lucro de Dois Filmes")
        print("4. Pesquisa Filme Por Título e Gênero")
        print("5. Escolha 2 Anos Para Realizar União, Intersecção ou Diferença De Gêneros")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            top_10_filmes()
        elif opcao == '2':
            filmes_100_milhoes()
        elif opcao == '3':
            comparar_lucro()
        elif opcao == '4':
            pesquisar_filme()
        elif opcao == '5':
            realizar_operacao_generos(
                input("Escolha a operação (união, intersecção, diferença): ").strip().lower(),
                input("Digite o primeiro ano: ").strip(),
                input("Digite o segundo ano: ").strip()
            )
        elif opcao == '6':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
    
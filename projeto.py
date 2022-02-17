"""
autor: Afonso Carraça Azaruja
data: 26/10/2021
email: afonso.azaruja@tecnico.ulisboa.pt / afonso.azaruja@gmail.com
"""


def corrigir_palavra(cad_car):  # 1.2.1
    """ corrigir_palavra : str --> str
    Esta função recebe uma cadeia de carateres que representam uma palavra (potencialmente
    modificada por um ssurto de letras) e devolve a cadeia de carateres que corresponde à
    aplicação da sequência de reduções, da seguinte forma, são removidas duas letras caso
    estejam juntas e sejam a mesma letra, uma maiúscula e outra minúscula vice-versa (ex: aA, Bb) 
    """
    i = 0
    while i < len(cad_car) - 1:
        letra1 = cad_car[i]
        letra2 = cad_car[i + 1]
        i += 1
        if abs(ord(letra1) - ord(letra2)) == 32:  # ex ord('X') - ord('x') = 32   x, X = [a,z], [A-Z]
            cad_car = cad_car[:i - 1] + cad_car[i + 1:]  # concatenar parte esq a parte dir, em relacao aos car a del
            if i != 1:
                i -= 2  # ao remover os dois car e necessario começar a contar dois indices atras
            else:
                i = 0  # caso as primeiras letras sao removidas
    return cad_car


def eh_anagrama(f1, f2):  # 1.2.2 TUDO CERTO
    """ eh_anagrama : str, str --> bool
    Esta função recebe duas cadeias de carateres correspondentes a duas palavras e devolve
    True se e só se uma é anagrama da outra.
    """
    if len(f1) != len(f2):
        return False
    else:
        f1_p, f2_p = f1.lower(), f2.lower()  # tornar car minusculos para a soma ord() ser igual
        res_f1, res_f2 = 0, 0
        for i in f1_p:
            res_f1 += ord(i)  # soma da ord() de cada car
        for j in f2_p:
            res_f2 += ord(j)
        if res_f1 == res_f2:
            return True
        return False


def corrigir_doc(car_err):  # 1.2.3
    """ corrigir_doc : str --> str
    Esta função recebe uma cadeia de carateres que representa o texto com erros e devolve a
    cadeia de carateres filtrada com as palavras corrigidas (corrigir_palavra) e os anagramas
    retirados (eh_anagrama), ficando apenas a sua primeira ocorrência.
    """ 
    if type(car_err) != str or '  ' in car_err or len(car_err) == 0 or not (''.join(car_err.split()).isalpha()) \
            or car_err[0] == ' ' or car_err[len(car_err)-1] == ' ':
        raise ValueError('corrigir_doc: argumento invalido')
    car_cor = corrigir_palavra(car_err)
    lst_del, i = [], -1
    car_cor = car_cor.split()
    while i < len(car_cor):
        i += 1
        j = i + 1
        while j < len(car_cor):
            if eh_anagrama(car_cor[i], car_cor[j]) is True:
                if car_cor[i] not in lst_del and car_cor[i].lower() != car_cor[j].lower():
                    lst_del.append(car_cor[j])  # lista com os anagramas a remover da string
                j += 1
            else:
                j += 1
    for x in lst_del:
        car_cor.remove(x)  # remove as palavras da string que estao na lista
    return ' '.join(car_cor)  # junta as palavras que estao na lista numa string


def obter_posicao(c, p):  # 2.2.1
    """ obter_posicao : str, int --> int
    Esta função recebe uma cadeia de carateres contendo apenas um caráter que representa
    a direção de um único movimento ('C', 'B', 'E', 'D') e um inteiro representando a
    posição atual (1, 2, 3, 4, 5, 6, 7, 8 ou 9), e devolve o inteiro que corresponde á
    nova posição.
    """
    if c == 'C' and p != 1 and p != 2 and p != 3:
        p -= 3
    if c == 'B' and p != 7 and p != 8 and p != 9:
        p += 3
    if c == 'D' and p != 3 and p != 6 and p != 9:
        p += 1
    if c == 'E' and p != 1 and p != 4 and p != 7:
        p -= 1
    return p


def obter_digito(cad_car, pos):  # 2.2.2
    """ obter_digito : str, int --> int
    Esta função recebe uma cadeia de carateres contendo uma sequência de um ou mais
    movimentos e um inteiro representando a posição inicial. Devolvendo o inteiro que
    corresponde ao dígito a marcar após finalizar todos os movimentos.
    """
    ult_pos = obter_posicao(cad_car[0], pos)
    i = 1
    while i < len(cad_car):
        ult_pos = obter_posicao(cad_car[i], ult_pos)
        i += 1
    return ult_pos


def obter_pin(t):  # 2.2.3
    """ obter_pin : tuple --> tuple
    Esta função recebe um tuplo contendo entre 4 a 10 sequências de movimentos e devolve
    o tuplo de inteiro que contêm o pin codificado de acordo com o tuplo de movimentos.
    """
    lst = ['C', 'D', 'E', 'B']
    if not isinstance(t, tuple) or not 4 <= len(t) <= 10 or '' in t:
        raise ValueError('obter_pin: argumento invalido')
    for j in t:
        if not isinstance(j, str) or ' ' in j:
            raise ValueError('obter_pin: argumento invalido')
        for k in j:
            if k not in lst:
                raise ValueError('obter_pin: argumento invalido')
    else:
        pin, ult_pos, i = (), 5, 0
        while i < len(t):
            ult_pos = obter_digito(t[i], ult_pos)  # recebe a ultima posicao
            pin += (ult_pos,)  # insere a posicao num tuplo
            i += 1
    return pin


def eh_entrada(t):  # 3.2.1 / 4.2.1
    """ eh_entrada : universal --> bool
    Esta função recebe um argumento de qualquer tipo e devolte True se e só se o seu
    argumento corresponde a uma entrada válida da BDB. Isto é um tuplo com 3 campos:
    uma cifra, uma sequência de controlo e uma sequência de segurança.
    """
    def eh_cifra(c):  # AUXILIAR
        """ eh_cifra : str --> bool
        Função auxiliar de eh_entrada que deteta se a cifra corresponde a uma entrada válida da bdb.
        """
        if not isinstance(c, str):
            return False
        letras = ''.join(c.split('-'))  # c.split('-') remove '-' e transforma em lista e volta a transformar em str
        
        lst_cifra = c.split('-')
        while '' in lst_cifra:
            lst_cifra.remove('')  # caso hajam varias ocorrencias de '-'
        
        if letras.isalpha() and letras.islower() and c == '-'.join(lst_cifra) and not c.isspace():
            return True
        return False

    def eh_checksum(seq):  # AUXILIAR
        """ eh_checksum : str --> bool
        Função auxiliar de eh_entrada, que deteta se a sequência é uma entrada válida da bdb.
        """
        if not isinstance(seq, str):
            return False
        if len(seq) != 7:
            return False
        if not (seq[0] == '[' and seq[6] == ']' and seq[1:6].isalpha() and seq[1:6].islower()):
            return False
        return True

    def eh_tuplo(tp):  # AUXILIAR
        if not (isinstance(tp, tuple) and len(tp) > 1):
            return False
        count = 0
        for i in tp:
            if isinstance(i, int) and i > 0:
                count += 1  # contador de inteiros positivos

        if count == len(tp):
            return True
        return False

    if not (isinstance(t, tuple) and len(t) == 3):
        return False

    return eh_cifra(t[0]) and eh_checksum(t[1]) and eh_tuplo(t[2])


def validar_cifra(c, seq):  # 3.2.2
    """ validar_cifra : str, str --> bool
    Esta função recebe uma cadeia de carateres contendo uma cifra e uma outra cadeia de
    carateres contendo uma sequência de controlo, e devolve True se e só se a sequência
    de controlo é coerente com a cifra.
    """
    d, lst, lst_k, maior, j = {}, [], [], 0, 0
    for i in ''.join(c.split('-')):
        if i not in d:  # cilco for para criar dict com keys dos carateres e com os valores de quantas vezes aparecem
            d[i] = 1
        else:
            d[i] += 1

    while len(lst) < 5:
        for j in d.values():  # detetar o maior valor atual no dict
            if j > maior:
                maior = j
        for k, v in d.items():  # detetar todas as keys com o maior valor detetado anteriormente
            if v == maior:
                lst_k.append(k)  # adicionar as respetivas keys com esse valor
                maior = v
        
        if len(lst_k) == 1:  # caso seja apenas 1 key com esse valor, adicionar a lista para criar seq certa
            lst.append(lst_k[0])
            d.pop(lst_k[0])  # e remover do dict
        
        else:
            lst_k.sort()  # caso, keys > 1, entao ordenar car por ordem alfabetica
            while len(lst_k) != 0 and len(lst) < 5:
                lst.append(lst_k[0])
                d.pop(lst_k[0])
                lst_k.remove(lst_k[0])
        lst_k, maior = [], 0  # iniciar loop com lista vazia e variavel 'maior' a 0
        j += 1
    x = ''.join(lst)
    res = '[' + x + ']'  # de forma a criar a seq que estaria correta, se nao for igual a original, return False
    if res == seq:
        return True
    return False


def filtrar_bdb(lst):  # 3.2.3
    """ filtrar_bdb : list --> list
    Esta função recebe uma lista contendo uma ou mais entradas da BDB e devolve apenas
    a lista contendo as entradas em que o checksum não é coerente com a cifra correspondente.
    """
    if not (isinstance(lst, list) and len(lst) > 0):
        raise ValueError('filtrar_bdb: argumento invalido')
    for i in lst:
        if eh_entrada(i) is False:
            raise ValueError('filtrar_bdb: argumento invalido')

    lst_res = []
    for j in lst:
        if validar_cifra(j[0], j[1]) is False:
            lst_res.append(j)

    return lst_res


def obter_num_seguranca(t):  # 4.2.2
    """ obter_num_segurança : tuple --> int
    Esta função recebe um tuplo de número inteiros positivos e devolve o número de segurança.
    A menor diferença entre todos os números contidos na sequência de segurança.
    """
    dif = max(t)  # obter n. maximo do tuplo, apenas serve para ter uma variavel que garante que vai ser substituida
    for i in t:
        j = 0
        while j < len(t):
            res = i - t[j]  # subtrair n. i com todos os outros
            if res <= 0:  # se resultado <= 0 então subtraiu-se o msm n. ou t[j] > que i
                j += 1
            elif res < dif:  # se a diferença entre esses 2 n. e menor que dif entao substitui-se
                dif = res  # substituicao
                j += 1
            else:
                j += 1
    return dif


def decifrar_texto(cifra, n_seg):  # 4.2.3
    """ decifrar_texto : str, int --> str
    Esta função recebe uma cadeia de carateres contendo uma cifra e um número de segurança,
    e devolve o texto decifrado. Cada caratere move o número de espaços, indicados no nº de
    segurança, no alfabeto, caso se encontre em um índice par, move +1, caso contrário -1.
    """
    txt = ''
    if n_seg > 26:
        n_seg %= 26  # reduzir o n. para limites dentro do n. de letras no alfabeto
    for i in range(len(cifra)):
        if ord(cifra[i]) == 45:  # ao encontrar "-", substituir por espaço em branco
            txt += ' '
        else:
            if i % 2 == 0:  # se o indice da letra e par
                res = ord(cifra[i]) + n_seg + 1
            else:  # se o idnice da letra e impar
                res = ord(cifra[i]) + n_seg - 1
            if res > 122:  # caso o n. de espaços a avançar ultrapasse a letra z
                res -= 122  # subtrair a ord(z), fim do alfabeto
                res += 96  # adicionar a ord(a), inicio do alfabeto
                txt += chr(res)
            else:
                txt += chr(res)
            i += 1
    return txt


def decifrar_bdb(lst):  # 4.2.4
    """ decifrar_bdb : list --> list
    Esta função recebe uma lista contendo uma ou mais entradas da BDB e devolve uma lista
    de igual tamanho, contendo as entradas decifradas na mesma ordem.
    """
    if not (isinstance(lst, list) and len(lst) > 0):
        raise ValueError('decifrar_bdb: argumento invalido')
    lst_decifrada = []
    for i in range(len(lst)):
        if eh_entrada(lst[i]) is False:
            raise ValueError('decifrar_bdb: argumento invalido')
        lst_decifrada.append(decifrar_texto(lst[i][0], obter_num_seguranca(lst[i][2])))
    return lst_decifrada


def eh_utilizador(x):  # 5.2.1
    """ eh_utilizador : universal --> bool
    Esta função recebe um argumento de qualquer tipo e devolve True se e só se o seu argumento
    corresponde a um dicionário contendo informação relevante da BDB.
    """
    if not (isinstance(x, dict) and len(x) == 3):
        return False
    if 'name' not in x or 'pass' not in x or 'rule' not in x or 'vals' not in x['rule'] or 'char' not in x['rule']:
        return False
    if not (isinstance(x['name'], str) and isinstance(x['pass'], str) and isinstance(x['rule'], dict)):
        return False
    if not (isinstance(x['rule']['vals'], tuple) and isinstance(x['rule']['char'], str)):
        return False
    if len(x['name']) < 1 or len(x['pass']) < 1 or len(x['rule']['vals']) != 2 or len(x['rule']['char']) != 1:
        return False
    lst = []
    for i in x['rule']['vals']:
        lst.append(i)
        if i < 0:
            return False
    if lst[0] > lst[1]:
        return False
    else:
        return True


def eh_senha_valida(pl, dc):  # 5.2.2
    """ eh_senha_valida : str, dict --> bool
    Esta função receb uma cadeia de carateres correspondente a uma senha e um dicionário
    contendo a regra individual de criação de senha, e devovle True se e só se a senha
    cumpre com todas as regras de definição.
    """
    def regras_gerais(letras):  # AUXILIAR
        """ regras_gerais : str --> bool
        Função auxiliar de eh_senha_valida, valida as regras gerais. 
        """
        l_vog = ['a', 'e', 'i', 'o', 'u']
        count_vog, count_occ = 0, 0
        for i in range(len(letras)):
            if letras[i] in l_vog:  # contador do n. de vogais
                count_vog += 1
            if i < len(letras) - 1:
                if letras[i] == letras[i + 1]:  # contador de letras iguais seguidas
                    count_occ += 1
        if count_vog >= 3 and count_occ > 0:
            return True
        return False

    def regras_ind(p, v, c):  # AUXILIAR
        """ regras_ind : str, tuple, str --> bool
        Função auxiliar de eh_entrada, valida as regras individuais.
        """
        count = 0
        for i in p:
            if i == c:
                count += 1  # contador de instancias da letra
        if v[0] <= count <= v[1]:
            return True
        return False
    if regras_gerais(pl) and regras_ind(pl, dc['vals'], dc['char']) is True:
        return True
    return False


def filtrar_senhas(lst):  # 5.2.3
    """ filtrar_senhas : lst --> lst
    Esta função recebe uma lista contendo um ou mais dicionários correspondetes às entradas
    das da BDB como descritas anteriormente, e devolve a lista ordenada alfabeticamente com
    os nomes dos utilizadores com senhas erradas.
    """
    if not (isinstance(lst, list) and len(lst) > 0):
        raise ValueError('filtrar_senhas: argumento invalido')

    for i in lst:
        if not isinstance(i, dict):
            raise ValueError('filtrar_senhas: argumento invalido')
    
    lst_nomes = []
    for j in lst:
        if eh_utilizador(j) is False:
            raise ValueError('filtrar_senhas: argumento invalido') 

        if eh_senha_valida(j['pass'], j['rule']) is False:
            lst_nomes.append(j['name'])
    lst_nomes.sort()
    return lst_nomes

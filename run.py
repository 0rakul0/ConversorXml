import pandas as pd
import xmltodict
import glob

def processamento(pasta):
    """
    essa função tem como obejetivo ler a pasta raiz dos arquivos,
    ler > formatar em forma de discionario
    :param pasta:
    :return:
    """
    dados = []
    dir = fr"./{pasta}/"
    for arq in glob.iglob(dir+'*.xml',recursive=False):
        meu_arquivo = open(arq, "r", encoding="utf8")
        conteudo = meu_arquivo.read()
        conteudo_dict = xmltodict.parse(conteudo)
        dados.append(conteudo_dict)
        meu_arquivo.close()
    return dados

def filtro(dados_dict):
    """
    :param dados_dict: dados estruturados
    :return: dados filtrados
    """
    conteudo_dict = dados_dict
    ## filtro ###
    if "NFe" in conteudo_dict:
        infos_nf = conteudo_dict["NFe"]["infNFe"]
    else:
        infos_nf = conteudo_dict["nfeProc"]["NFe"]["infNFe"]
    numero_nf = infos_nf["@Id"]
    empresa_em = infos_nf["emit"]["xNome"]
    nome_cliente = infos_nf["dest"]["xNome"]
    end = infos_nf["dest"]["enderDest"]
    if "vol" in infos_nf["transp"]:
        peso_bruto = infos_nf["transp"]["vol"]
    else:
        peso_bruto = "peso não informado"
    dic_pandas = numero_nf, empresa_em, nome_cliente, end, peso_bruto
    return dic_pandas
def saida(dados):
    """
    monta o dataframe recebendo um json estruturado e convertendo para dataframe
    :param dados: recebe uma lista de json
    """
    colunas = ["numero_nota", "empresa_emissora", "nome_cliente", "endereco", "peso_bruto"]
    valores = [filtro(val) for val in dados]
    tabela = pd.DataFrame(columns=colunas, data=valores)
    tabela.to_excel(r"./outputs/notas_fiscais.xlsx", index=False)
    tabela.to_csv(r"./outputs/notas_fiscais.csv", index=False, header=True)

def run():
    """
    roda o script.
    input dos arquivos > processa os arquivos > filtra > saida
    gera um arquivo csv e xlsx
    """
    path = "inputs"
    dados = processamento(path)
    saida(dados)

if __name__=="__main__":
    run()
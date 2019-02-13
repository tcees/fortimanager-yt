import argparse
import urllib3

from .manager import Manager, ErroDeOperacao
from .youtube import YouTube

# Desliga a exibição de alertas do tipo warning lançados pelo urllib
urllib3.disable_warnings()

# Tratamento de parametros
parser = argparse.ArgumentParser(
    prog="fortimanager_yt",
    description="Automatizador de liberação "+
        "de videos do youtube, sem a necessidade de liberar o domínio "+
        "youtube inteiro no firewall fortigate, usando o fortimanager."+
        "Para usar é necessário ter configurado uma conta no google api "+
        "e ter acesso a api do YouTube. Para este uso, a versão gratuita "+
        "atende muito bem. E o fortimanager configurado para permitir "+
        "configurações via api.")

parser.add_argument("perfis", 
    help="Lista de perfis de webfilter para aplicação das alterações.",
    nargs="+")
parser.add_argument("playlist_id",
    help="Especifica a playlist do YouTube.",
    nargs=1)
parser.add_argument("--todos", 
    help="Executa a operação para TODOS os vídeos da playlist especificada (max 10000). "+
        "Caso este parâmetro seja omitido, será utilizado o valor do parâmetro `qtd`.", 
    action="store_true")
parser.add_argument("--nao_instalar", 
    help="Realiza as alterações mas não manda instalar as alterações.", 
    action="store_true")
parser.add_argument("--config", "-c",
    help="Caminho para o arquivo de configuração, necessário após intalar."+
        "Caso não seja especificado, buscará o arquivo com nome: fortimanagerYTconfig.yaml "+
        "na pasta atual."
)
parser.add_argument("--qtd", "-q", type=int, default=50,
    help="Quantidade de videos a liberar da playlist especificada."
)
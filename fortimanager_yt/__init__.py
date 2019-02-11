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
    help="Perfis de webfilter a qual serão aplicadas as alterações",
    nargs="+")
parser.add_argument("playlist_id",
    help="Playlist a qual deverá ser verificada se existem videos não "+
        "liberados no manager."
    )
parser.add_argument("--todos", 
    help="Libera todos os videos de uma playlist que ainda não estão "+
        "liberados no manager", 
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
import argparse
import urllib3

from manager import Manager, YouTube, ErroDeOperacao
from manager.confs import MANAGER, YOUTUBE

urllib3.disable_warnings()

parser = argparse.ArgumentParser(
    description="Manager-YT é um automatizador de liberação "+
    "de videos do youtube, sem a necessidade de liberar o domínio "+
    "youtube inteiro no firewall fortigate, usando o fortimanager."+
    "Para usar é necessário ter configurado uma conta no google api "+
    "e ter acesso a api do YouTube. Para este uso, a versão gratuita "+
    "atende muito bem.")

parser.add_argument("perfis", nargs="+")
parser.add_argument("--sync", action="store_true")
parser.add_argument("--playlist_id", "-p")
parser.add_argument("--todos", action="store_true")
parser.add_argument("--nao_instalar", action="store_true")
args = parser.parse_args()

youtube = YouTube(YOUTUBE["chave"], YOUTUBE["verificar_ssl"])
manager = Manager(MANAGER["url"], MANAGER["pasta_cache"], 
    MANAGER["pasta_templates"], MANAGER["verificar_ssl"], youtube)

try:
    manager.iniciar(MANAGER["usuario"], MANAGER["senha"])
except ErroDeOperacao as erro:
    print("Não foi possivel logar no Manager, verifique os dados de usuario e senha")

try:
    if args.sync:
        manager.sincronizarCache(args.perfis)

    else:
        if not args.playlist_id:
            print("Para liberar videos de uma playlist YouTube é necessário"+
                " passar o id da Playlist a ser liberada")
        
        else:
            manager.liberarVideosYouTubePlaylist(args.perfis, args.playlist_id, todos=args.todos)
            if not args.nao_instalar: 
                print(manager.instalar())

except ErroDeOperacao as erro:
    print(erro)

finally:
    if manager.token:
        manager.destruir()

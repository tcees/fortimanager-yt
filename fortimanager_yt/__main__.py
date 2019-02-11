import yaml
import os

from .__init__ import *

args = parser.parse_args()

# Carrega arquivo de configurações
if args.config:

    if os.path.isfile(args.config):
        cfg = yaml.load(open(args.config).read())

    else:
        print("Arquivo de configuração especificado não existe.")
        exit(0)

elif os.path.isfile("fortimanagerYTconfig.yaml"):
        cfg = yaml.load(open("fortimanagerYTconfig.yaml").read())

else:
    print("É necessário especificar um arquivo de configuração!")
    exit(0)

youtube = YouTube(cfg["youtube"]["api_key"], cfg["youtube"]["ssl"])

manager = Manager(cfg["manager"]["url"], cfg["manager"]["adom"], 
                    cfg["manager"]["ssl"], 
                    youtube
                )

try:
    # Inicia a sessão com o manager
    manager.iniciar(cfg["manager"]["usuario"], cfg["manager"]["senha"])
    
    print("[*] Logado no fortimanager")

except ErroDeOperacao as erro:
    print("[-] Não foi possivel logar no Manager, verifique os ")
    print("    dados de usuario e senha")
    exit(2)

try:
    
    # Caso nenhuma playlist seja passada não é possivel realizar a verificação
    if not args.playlist_id:

        print("[-] Para liberar videos de uma playlist YouTube é")
        print("    necessário passar o id da Playlist a ser liberada.")

    else:
        
        print("[+] PlayList ID:", args.playlist_id)
        print("    Perfis:", args.perfis)
        print("    Instalar?", (not args.nao_instalar))
        if args.todos:
            print("    Todos videos?", args.todos)
        else:
            print("    Quantidade:", args.qtd)

        print("[*] Iniciando liberação...")
        
        # Tenta realizar a liberação dos videos que ainda não foram liberados
        resp = manager.liberarVideosYouTubePlaylist(
                args.perfis, 
                args.playlist_id, 
                todos=args.todos,
                quantidade=args.qtd
            )
        
        if resp:
            print("[*] Liberação feita com sucesso.")

            if not args.nao_instalar:
                
                print("[*] Instalando...")
                
                manager.instalar()
                
                print("[*] Instalação concluida!")
                
        else:
            print("[+] Nenhum video encontrado para liberação")

except ErroDeOperacao as erro:
    
    print(erro)

finally:
    
    # Destrói a sessão que foi iniciada
    if manager.token:
        
        print("[*] Destruindo sessão...")
        
        manager.destruir()
        
        print("[*] Sessão destruída com sucesso!")

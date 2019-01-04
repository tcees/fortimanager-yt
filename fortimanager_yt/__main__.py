from .__init__ import ErroDeOperacao, Manager, YouTube, cfg, parser

args = parser.parse_args()

youtube = YouTube(
        cfg["youtube"]["chave"], 
        cfg["youtube"]["verificar_ssl"]
    )

manager = Manager(
        cfg["manager"]["url"], 
        cfg["manager"]["adom"],
        cfg["manager"]["pasta_cache"], 
        cfg["manager"]["pasta_templates"], 
        cfg["manager"]["verificar_ssl"], 
        youtube
    )

try:
    # Inicia a sessão com o manager
    manager.iniciar(
            cfg["manager"]["usuario"], 
            cfg["manager"]["senha"]
        )
except ErroDeOperacao as erro:
    print("Não foi possivel logar no Manager, verifique os dados de usuario e senha")

try:
    # Se a operação a ser realizada é somente de sincronia de cache
    if args.sync:
        manager.sincronizarCache(args.perfis)
    else:
        # Caso nenhuma playlist seja passada não é possivel realizar a verificação
        if not args.playlist_id:
            print("Para liberar videos de uma playlist YouTube é necessário"+
                " passar o id da Playlist a ser liberada")
        else:
            # Tenta realizar a liberação dos videos que ainda não foram liberados
            manager.liberarVideosYouTubePlaylist(
                    args.perfis, 
                    args.playlist_id, 
                    todos=args.todos
                )
    
            if not args.nao_instalar:
                print(manager.instalar())

except ErroDeOperacao as erro:
    print(erro)

finally:
    # Destroi a sessão que foi iniciada
    if manager.token:
        manager.destruir()

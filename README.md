# FortiMananager-YouTube
Aplicativo para automatizar liberação de videos do YouTube no FortiManager (FortiGate) de forma fácil, que pode ser colocado em um automatizador de tarefas como o cron ou no agendador de tarefas do windows.

## Pré-requisitos
* [Uma chave de api do YouTube](https://developers.google.com/youtube/registering_an_application?hl=pt-br)

* Uma conta configurada no FortiManager com acesso a api e permissões para escrita nos perfis de webfilters

## Como usar
Configure o arquivo `fortimanagerYTconfig.yaml` com os valores necessários

Rode o módulo da seguinte forma:

`python3 -m fortimanager_yt perfis [perfis ...] [-h] [--sync] [--playlist_id PLAYLIST_ID] [--todos] [--nao_instalar]`

Exemplo: 
`python3 -m fortimanager_yt perfil1 perfil2 --playlist_id xxxxxxxxxxxxxxx --todos`

Este comando iria liberar todos os videos encontrados na playlist `xxxxxxxxxxxxxxx` do youtube que ainda não estão liberados no FortiManager para os perfis: `perfil1` e `perfil2`.

### Lista de parâmetros linha de comando
* perfis

Perfis de webfilter a qual serão aplicadas as alterações.
Pode ser passado varios perfis

* sync

Modo de sincronização do cache. Quando este parâmetro é especificado, o programa atualizará o cache local somente.

* playlist_id

Especifica uma playlist do YouTube como alvoda operação a ser realizada.

* todos

Executa a operação para TODOS os videos da playlist especificada. Caso este parâmetro seja omitido, a operação utilizará aos 50 ultimos videos postados na playlist.

* nao_instalar

Ao fim dos procedimentos não realizar a instalação no Manager. Caso seja omitido, o programa instalará as alterações no FortiManager, fazendo a configuração valer no firewall associado a ele.

### Arquivo de configuração
Antes de usar o programa é importante configura-lo dentro do arquivo de configuração `fortimanagerYTconfig.yaml`.
Este arquivo tem a seguinte forma:
```
# Informações sobre o fortimanager
manager:

  # Url de acesso a api do manager
  # Exemplo: 192.168.1.200:8080
  url: ""

  # Usuário com permissões de escrita no 
  # fortimanager e com acesso a api
  usuario: ""
  senha: ""

  # Se o fortimanager usa ssl ou não
  ssl: True

  # Pasta onde devem ser armazenados os
  # arquivos de cache gerados pelo programa
  pasta_cache: ""

  # Pasta onde estão armazenados os templates
  # de requisição a api
  pasta_templates: "requests/"

  # Adom que será alterado
  adom: ""

# Configurações do youtube para se obter informações 
# sobre videos
youtube:
  
  # Chave de acesso a api do youtube do google
  api_key: ""

  # Se deseja verificar o certificado para a conexão
  ssl: True
```

## Limitações e problemas
O programa tem algumas limitações e pode gerar problemas com a integridade do FortiManager.

* A instalação sobe TODAS as configurações pendentes

Como a instalação no FortiManager sobe todas as configurações pendentes, se mais de uma pessoa configura o manager há o risco de, ao mesmo tempo que alguém estiver fazendo alguma alteração nas configurações haver uma execução deste programa com instalação. O que instalaria, além da configuração gerada pelo programa, a configuração inacabada pela pessoa trabalhando. Portanto, prudência ao usar este programa ajuda.

* A playlist é a unica forma de se encontrar videos para liberação

É uma limitação de projeto, mas que pode ser superada com mais algum tempo de trabalho, se houver demanda para isso.

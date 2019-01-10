# FortiMananager-YouTube
O FortiMananager-YouTube é um aplicativo desenvolvido em Python para realizar a liberação de vídeos de uma playlist do YouTube no Fortinet FortiManager.

## Pré-requisitos
* [Chave de api do YouTube](https://developers.google.com/youtube/registering_an_application?hl=pt-br);
* Conta configurada no FortiManager com permissão para escrita nos perfis de webfilters;
* Python 3.

## Instalação
* Após clonar o repositório, acesse a pasta e execute o comando abaixo:
```bash
pip3 install .
```
* Configure o arquivo `fortimanagerYTconfig.yaml`, disponível na pasta do módulo, com os valores necessários;
* Rode o módulo conforme parâmetros abaixo:
```bash
python3 -m fortimanager_yt perfis [perfis ...] [-h] [--sync] [--playlist_id PLAYLIST_ID] [--todos] [--nao_instalar]
```

## Exemplos 
Para realizar a liberação de todos os vídeos encontrados na playlist `xxxxxxxxxxxxxxx` para os perfis `perfil1` e `perfil2`, rode o comando abaixo:
```bash
python3 -m fortimanager_yt perfil1 perfil2 --playlist_id xxxxxxxxxxxxxxx --todos
```

## Lista de parâmetros
* perfis

Lista de perfis de webfilter para aplicação das alterações.

* sync

Modo de sincronização do cache. Quando este parâmetro é especificado, será atualizado o cache local somente.

* playlist_id

Especifica a playlist do YouTube.

* todos

Executa a operação para TODOS os vídeos da playlist especificada. Caso este parâmetro seja omitido, serão liberados apenas os 50 últimos vídeos postados na playlist.

* nao_instalar

Ao fim dos procedimentos, não realizar a instalação no FortiManager. Caso seja omitido, o programa instalará as alterações.

## Arquivo de configuração
Antes de usar o programa é importante configurá-lo dentro do arquivo de configuração `fortimanagerYTconfig.yaml`.
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

## Limitações
O programa possui algumas limitações que devem ser observadas.

* A instalação utiliza TODAS as configurações pendentes no FortiManager, mesmo aquelas que foram feitas ou possam estar sendo feitas por outro usuário.
* A playlist é a única forma de se encontrar vídeos para liberação.


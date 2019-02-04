# FortiManager-YouTube
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
Para realizar a liberação de todos os vídeos encontrados na playlist com id `<id>` para os perfis `<perfil1>` e `<perfil2>`, rode o comando abaixo:
```bash
python3 -m fortimanager_yt <perfil1> <perfil2> --playlist_id <id> --todos
```

## Lista de parâmetros
* perfis

Lista de perfis de webfilter para aplicação das alterações.

* playlist_id

Especifica a playlist do YouTube.

* todos

Executa a operação para TODOS os vídeos da playlist especificada. Caso este parâmetro seja omitido, serão liberados apenas os 50 últimos vídeos postados na playlist.

* nao_instalar

Ao fim dos procedimentos, não realizar a instalação no FortiManager. Caso seja omitido, o programa instalará as alterações.

## Arquivo de configuração
Antes de usar o programa é importante configurá-lo, editando o arquivo `fortimanagerYTconfig.yaml`.
Este arquivo possui o seguinte formato:
```
manager:
  # Url de acesso a api do manager
  # Exemplo: 192.168.1.200:8080
  url: ""
  # Usuário com permissões de escrita no fortimanager e com acesso a api
  usuario: ""
  senha: ""
  # Se o fortimanager usa ssl ou não
  ssl: True
  # Pasta onde estão armazenados os templates de requisição a api
  # O caminho relativo só irá funcionar caso rode o programa na pasta atual
  pasta_templates: "requests/"
  # Adom que será alterado
  adom: ""

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


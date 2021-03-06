from os import path
from time import sleep

from bs4 import BeautifulSoup
from jinja2 import Template
from requests import Session
from fortimanager_yt import requests


class Manager:
    """Simboliza uma instância do FortiManager

    Note:
        É importante que o FortiManager especificado esteja configurado
        para o uso da API de configuração e que o usuario passado tenha
        as devidas permições.
    """

    def __init__(self, endereco, adom, verify=True, youtube=None):
        """Construtor

        Args:
            endereco(str): Endereço de rede do FortiManager
            verify(bool, optional): Verificar ou não certificados SSL ao
                conectar com o FortiManager
            youtube(:obj:manager.YouTube, optional): Se tiver a intenção de
                usar recursos do YouTube, deverá especificar um objeto do
                tipo YouTube
        """
        self.adom = adom
        self.endereco = endereco
        self.token = None
        self.perfis = {}
        self.sessao = Session()
        self.sessao.headers["content-type"] = "text/xml;charset=UTF-8"
        self.sessao.headers["SOAPAction"] = ""
        self.sessao.verify = verify

        if youtube:
            self.youtube = youtube
            self.youtube_regex = r"(www\.youtube\.com|youtu\.be)/(watch\?v=|embed/)?"

    def enviar(self, corpo):
        """Envia uma requisição para o FortiManager
        Caso a requisição retorne algum código diferente
        de 0 (sucesso), é lançada uma excessão `ErroDeOperacao`

        Args:
            corpo(str): Corpo da requisição http, deve estar no formato SOAP
                reconhecível pela API do Managar

        Returns:
            `BeautifulSoup` resultado da requisição
        """
        resposta = self.sessao.post(self.endereco+"/FortiManagerWSxml", data=corpo)
        sopa = BeautifulSoup(resposta.text, "html.parser")
        if sopa.find("errorcode"):
            errorcode = sopa.find("errorcode").string
            errormsg = sopa.find("errormsg").string

            if errorcode != "0":
                raise ErroDeOperacao(errorcode, errormsg)

            return sopa
        else:
            print(resposta.text)
            return None

    def iniciar(self, usuario, senha):
        """Inicia uma sessão com o FortiManager

        Note: O `usuario` utilizado deve ter permissões para logar
            através da API

        Args:
            usuario(str): Usuário do Manager
            senha(str): Senha do usuário

        Returns:
            `BeautifulSoup` resultado da requisição
        """
        corpo = Template(requests.login).render(
                                    usuario=usuario,
                                    senha=senha)
        sopa = self.enviar(corpo)

        if sopa:
            self.token = sopa.find("session").string
            return sopa

    def destruir(self):
        """Destrói a sessão atual no Manager

        Returns:
            `BeautifulSoup` resultado da requisição
        """
        if not self.token: raise NaoLogado()

        corpo = Template(requests.logout).render(sessao=self.token)
        return self.enviar(corpo)

    def obterUrlsLiberadosPerfil(self, perfil):
        """Obtem urls que já estão liberadas pelo perfil

        Returns:
            `dict` com todas as urls liberadas para cada `perfil`
        """
        if not self.token:
            raise NaoLogado()

        corpo = Template(requests.getwebfilters).render(
                                    adom=self.adom,
                                    sessao=self.token,
                                    perfil_id=self.idUrlFilter(perfil),
                                    loadsub=True
                                )
        sopa = self.enviar(corpo)
        entradas = sopa.find("data").findAll("entries")
        urls = [entrada.url.string for entrada in entradas]

        return urls

    def idUrlFilter(self, perfil):
        """Obtém o id de um perfil de usuário de WebUrlFilter

        Args:
            perfil(str): Nome do perfil

        Returns:
            `str` id do `perfil`
        """
        if not self.token:
            raise NaoLogado()

        if perfil in self.perfis:
            return self.perfis[perfil]

        corpo = Template(requests.getwebfilters).render(
                                    adom=self.adom,
                                    sessao=self.token)
        sopa = self.enviar(corpo)

        for entrada in sopa.findAll("data"):
            self.perfis[entrada.find("name").string] = entrada.id.string

        if perfil in self.perfis:
            return self.perfis[perfil]

        else:
            raise PerfilNaoExiste(perfil)

    def instalar(self, rev_nome="", rev_comentario="", preview=False):
        """Aplica as configurações no Firewall

        Note: É preciso estar logado

        Args:
            rev_nome(str): Um nome para a revisão que será criada
            rev_comentario(str): O comentário para a revisão criada
            preview(bool): Previsão da instalação

        Return:
            `BeautifulSoup` resultado da requisição
        """
        if not self.token: raise NaoLogado()
        revisao = len(rev_nome) > 0
        corpo = Template(requests.installconfig).render(
                                        adom=self.adom,
                                        revisao=revisao,
                                        rev_nome=rev_nome,
                                        rev_comentario=rev_comentario,
                                        sessao=self.token,
                                        preview=preview
                                    )
        return self.enviar(corpo)

    def is_seguro(self):
        resposta = self.instalar(preview=True)
        task_id = int(resposta.find("task").text)
        task = self.get_task(task_id)
        while int(task.find("percent").text) != 100:
            sleep(0.25)
            task = self.get_task(task_id)
        detail = task.find("line").find("detail").text
        return detail == "no installing devices/no changes on package"


    def get_task(self, task_id):
        if not self.token: raise NaoLogado()
        corpo = Template(requests.gettask).render(
                                task=task_id,
                                sessao=self.token
                            )
        return self.enviar(corpo)

    def cancelar(self):
        if not self.token: raise NaoLogado()
        corpo = Template(requests.cancel_install).render(
                                adom=self.adom,
                                sessao=self.token
                            )
        return self.enviar(corpo)

    def liberar(self, urls, perfis, tipo="simple", acao="exempt",
                status="enable", rev_nome="Liberação de urls via script",
                rev_comentario=""):
        """Libera as `urls` no Firewall para os perfis especificados

            Note: É preciso estar logado

            Args:
                urls(:obj:`list` of `str`): Lista de urls a serem liberadas
                perfis(:obj:`list` of `str`): Lista de perfis que devem
                    ter as `urls` liberadas
                tipo(str): Tipo de liberação para as urls. Podem ser
                    `regex`, `wildcard` ou `simple`
                acao(str): Ação que o Firewall tomará quando interceptar
                    essa url. Podem ser `block` `allow` `monitor` `exempt`
                status(str): Status desta url. Pode ser `enable` ou `disable`
                rev_nome(str): Nome da revisão a ser criada
                rev_comentario(str): Comentário para a revisão criada

            Returns:
                `BeautifulSoup` da requisição de instalação e um `dict`
                com as respostas das requisições enviadas uma para
                cada `perfil`
        """
        if not tipo in ["regex", "wildcard", "simple"]:
            raise ValueError(tipo+" não é um valor de tipo válido")
        if not acao in ["block", "allow", "monitor", "exempt"]:
            raise ValueError(acao+" não é um valor de acao válido")
        if not status in ["enable", "disable"]:
            raise ValueError(status+" não é um valor de status válido")

        if not self.token: raise NaoLogado()

        respostas = {}

        for perfil in perfis:
            try:
                perfil_id = self.idUrlFilter(perfil)

            except PerfilNaoExiste:
                print("[-] O perfil de WebUrlFilter '%s' não existe no Manager" % perfil)
                continue

            atual = self.obterUrlsLiberadosPerfil(perfil)
            urls = set(urls).difference(atual)

            if len(urls) == 0:
                continue

            corpo = Template(requests.seturl).render(
                                            adom=self.adom,
                                            urls=urls,
                                            urlfilter=perfil_id,
                                            tipo=tipo,
                                            acao=acao,
                                            status=status,
                                            sessao=self.token
                                        )
            respostas[perfil] = self.enviar(corpo)

        return respostas

    def liberarVideosYouTubePlaylist(self, perfis, playlist, quantidade=50, todos=False):
        """Libera `quantidade` ou todos os videos de uma playlist do
        YouTube.

        Note:
            É preciso estar logado no Manager. É preciso especificar
            o atributo YouTube. Os são obtidos por ordem de data de
            postagem, dos mais recentes para os mais antigos.

        Args:
            perfis(:obj:`list` of `str`): Perfis para os quais os videos
                serão liberados
            playlist(str): O id da playlist do YouTube
            quantidade(int): A quantidade de videos a serem liberados
                por padrão, são 50 (os 50 mais recentes da playlist)
            todos(bool): Todos os videos da playlist. Quando especificado
                como True, libera TODOS os videos, e ignora o parâmetro
                quantidade.

        Returns:
            `BeautifulSoup` resultado da requisição
        """
        if not self.token:
            raise NaoLogado()

        if todos:
            quantidade = 10000
        elif quantidade == 0:
            return None

        videos = self.youtube.obterVideosPlaylist(playlist, quantidade)

        if len(videos) > 0:
            urls = [self.youtube_regex + url for url in videos]
            resposta = self.liberar(urls, perfis, tipo="regex")
            return resposta
        else:
            return None

class NaoLogado(Exception):
    def __str__(self):
        return "É preciso ter uma sessão ativa para usar este recurso."


class PerfilNaoExiste(Exception):
    def __init__(self, perfil):
        self.perfil = perfil

    def __str__(self):
        return "O perfil "+self.perfil+" não existe no FortiManager"


class ErroDeOperacao(Exception):
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg

    def __str__(self):
        return "Houve um erro no processamento do Manager com status '"+self.status+"' e mensagem '"+self.msg+"'."

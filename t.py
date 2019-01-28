import fortimanager_yt as f

m = f.manager.Manager("https://10.205.1.4:8080", "root", "requests/", False)
m.iniciar("apiuser", "10a4v0tg5aq6et7v2aq7t8y22a")
u = m.obterUrlsLiberadosPerfil("grp_Internet_Estagiario")
m.destruir()

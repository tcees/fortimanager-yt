getwebfilters = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:r20="http://r200806.ws.fmg.fortinet.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <r20:getPmConfig54AdomObjWebfilterUrlfilter>
         <path>
            <adom>{{ adom }}</adom>
            {% if perfil_id %}
               <urlfilter>{{ perfil_id }}</urlfilter>
            {% endif %}
         </path>
         {% if not loadsub %}
            <loadsub>false</loadsub>
            <fields>id</fields>
            <fields>name</fields>
         {% endif %}
         <session>{{ sessao }}</session>
      </r20:getPmConfig54AdomObjWebfilterUrlfilter>
   </soapenv:Body>
</soapenv:Envelope>
"""

installconfig = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:r20="http://r200806.ws.fmg.fortinet.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <r20:execSecurityconsoleInstallPackage>
         <data>
            <adom>{{ adom }}</adom>
            <pkg>tcecluster</pkg>
            <flags>ifpolicy_only</flags>
            {% if revisao %}
               <flags>generate_rev</flags>
               <adom_rev_name>{{ rev_nome }}</adom_rev_name>
               <adom_rev_comments>{{ rev_comentario }}</adom_rev_comments>
            {% endif %}
            {% if preview %}
               <flags>preview</flags>
            {% endif %}
         </data>
         <session>{{ sessao }}</session>
      </r20:execSecurityconsoleInstallPackage>
   </soapenv:Body>
</soapenv:Envelope>
"""

login = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:r20="http://r200806.ws.fmg.fortinet.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <r20:execSysLoginUser>
         <data>
            <user>{{ usuario }}</user>
            <passwd>{{ senha }}</passwd>
         </data>
      </r20:execSysLoginUser>
   </soapenv:Body>
</soapenv:Envelope>
"""

logout = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:r20="http://r200806.ws.fmg.fortinet.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <r20:execSysLogout>
         <session>{{ sessao }}</session>
      </r20:execSysLogout>
   </soapenv:Body>
</soapenv:Envelope>
"""

seturl = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:r20="http://r200806.ws.fmg.fortinet.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <r20:addPmConfig54AdomObjWebfilterUrlfilterEntries>
         <path>
            <adom>{{ adom }}</adom> 
            <urlfilter>{{ urlfilter }}</urlfilter>
         </path>
         {% for url in urls %}
         <data>
            <url>{{ url }}</url>
            <type>{{ tipo }}</type>
            <action>{{ acao }}</action>
            <status>{{ status }}</status>
         </data>
         {% endfor %}
         <session>{{ sessao }}</session>
      </r20:addPmConfig54AdomObjWebfilterUrlfilterEntries>
   </soapenv:Body>
</soapenv:Envelope>
"""

gettask = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:r20="http://r200806.ws.fmg.fortinet.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <r20:getTaskTask>
         <path>
            <task>{{ task }}</task>
         </path>
         <session>{{ sessao }}</session>
      </r20:getTaskTask>
   </soapenv:Body>
</soapenv:Envelope>
"""

cancel_install = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:r20="http://r200806.ws.fmg.fortinet.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <r20:execSecurityconsolePackageCancelInstall>
         <data>
            <adom>{{ adom }}</adom>
         </data>
         <session>{{ sessao }}</session>
      </r20:execSecurityconsolePackageCancelInstall>
   </soapenv:Body>
</soapenv:Envelope>
"""
# Spyware via PythonSockets
**Authores:** @AlldDev, @YRammus
**Colaboradores:** @bcmarini, Alexandre Queiroz
**Equipe de Suporte:** Julio C. Fernandes, Diego S. Fernandes, Kayle, Jean

![](https://github.com/AlldDev/Spyware-PythonSocket-V1/blob/main/others/01.png)

![](https://github.com/AlldDev/Spyware-PythonSocket-V1/blob/main/others/02.png)

![](https://github.com/AlldDev/Spyware-PythonSocket-V1/blob/main/others/03.png)

![](https://github.com/AlldDev/Spyware-PythonSocket-V1/blob/main/others/04.png)

# Projeto de Demonstração de Riscos em Cibersegurança

Este projeto foi desenvolvido exclusivamente para servir como uma base e referência de estudo. Nosso objetivo é conscientizar sobre os perigos associados ao download de softwares não licenciados (crackeados), acesso a sites impróprios, clique em links duvidosos (phishing) e outras falhas, sejam elas humanas ou de sistema.

## Como Funciona?

O script estabelece uma conexão cliente/servidor, permitindo a troca de dados via sockets de rede. A peculiaridade surge quando invertemos essa conexão: em vez do cliente requisitar ações ao servidor, é o servidor que faz as requisições ao cliente. Utilizando bibliotecas específicas e engenharia reversa, conseguimos enviar comandos e parâmetros para execução na máquina da "vítima". Isso inclui a capacidade de navegar nas pastas, visualizar e até mesmo copiar arquivos para o servidor. O script pode ser hospedado em uma nuvem (por exemplo, AWS), permitindo a recepção de várias conexões (infecções) de diversos clientes (vítimas). Isso possibilita a criação de ataques coordenados ou individuais (em desenvolvimento).

> [!NOTE]
> Foi utilizado Python 3.11.4 para o desenvolvimento, juntamente com bibliotecas especificadas no início do código.

> [!IMPORTANT]
> Este é um projeto em desenvolvimento, portanto, erros e bugs podem ocorrer!

> [!WARNING]
> Este script pode causar problemas em sua máquina, com terceiros ou com a lei. Reforçamos que ele é exclusivamente destinado a fins educacionais. Não temos a intenção de causar danos a ninguém. Se você não compreende completamente o que está fazendo ou como funciona, por favor, NÃO INTERAJA.

## Ética e Responsabilidade

> Este projeto é uma ferramenta educacional destinada a ser usada de maneira ética, controlada e com o consentimento explícito de todas as partes envolvidas.
> É proibido utilizar este script para fins maliciosos ou ilegais. O uso indevido pode resultar em consequências legais sérias.

## Avisos Adicionais

NÃO use este script em sistemas ou redes sem autorização explícita. A invasão de privacidade é uma violação séria.

NÃO compartilhe este script com pessoas que possam usá-lo de maneira irresponsável. A conscientização é fundamental para evitar potenciais danos.

## Prevenção de Spywares e Segurança Cibernética

Mantenha seu sistema operacional e software sempre atualizados para corrigir vulnerabilidades conhecidas.

Use antivírus e programas de segurança confiáveis. Mantenha-os atualizados regularmente.

Evite clicar em links suspeitos ou baixar software de fontes não confiáveis.

Utilize firewalls para monitorar e controlar o tráfego de rede.

Eduque-se e sua equipe sobre as práticas seguras de navegação na internet e conscientização sobre phishing.

Realize auditorias de segurança regularmente para identificar e corrigir possíveis vulnerabilidades.

## Contribuições
> Contribuições são bem-vindas. Se você identificar melhorias, correções ou sugestões éticas, sinta-se à vontade para enviar pull requests ou abrir issues.

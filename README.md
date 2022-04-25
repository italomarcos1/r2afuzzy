# pyDash: A Framework Based Educational Tool for Adaptive Streaming Video Algorithms Study

![bigbuckbunny](https://user-images.githubusercontent.com/4336448/118493151-2b9fc380-b6f7-11eb-8a25-9134862da754.jpg) A Python Dash Project. 

PyDash is a framework for the development of adaptive streaming video algorithms. It is a learning tool designed to abstract the networking communication details, allowing e-students to focus exclusively on developing and evaluating ABR protocols.

# Who we are?

We are from the **Department of Computer Science** at the **University of Brasília (UnB)**, Brazil.

This project is leaded by [Prof. Dr. Marcos Caetano](mailto:mfcaetano@unb.br) and [Prof. Dr. Marcelo Marotta](mailto:marcelo.marotta@unb.br). 

If you have any questions regarding the pyDash project, please drop us an email.

# Installation Process

## Pré-requisitos

Para a utilização deste projeto é necessária a instalação de alguns pacotes  python descritos no arquivo [requirements.txt](requirements.txt). 

Para a utilização do reprodutor de mídia DASH, é necessário a instalação de alguns pacotes do framework GStreamer. Atualmente, só é possível ativá-lo em sistemas operacionais Linux. Logo, você encontrará instruções sobre como instalar tudo apenas em ambientes Linux. 

## Instalando o Gstreamer no Ubuntu, Debian, elementary OS, Pop!_OS
Instalar tudo o que precisamos no Ubuntu e sistemas operacionais relacionados é fácil! Basta executar o seguinte comando no terminal: 

```bash
sudo apt install libgstreamer1.0-0 gstreamer1.0-plugins-{base,good,bad,ugly} gstreamer1.0-tools python3-gi gir1.2-gstreamer-1.0
```
## Por onde eu começo?

Existem algumas formas de você configurar o seu ambiente. Nesta seção iremos apresentar apenas uma das formas possíveis.

* O primeiro passo é fazer o checkout do seu código. Utilizando um terminal, faça um clone do repositório.

```
git clone https://github.com/GuCosta/pydash_improvements.git
```
Em seguida, crie um ambiente virtual

```
python3 -m venv pydash_improvements/venv
```

* Entre no repositório

```
cd pydash_improvements
```

* O próximo passo é ativar o terminal e carregar as configurações python.

```
source venv/bin/activate
```

* Agora você precisa instalar as bibliotecas utilizadas pela ferramenta pyDash.
```
pip3 install -r requirements.txt
```

Pronto! Para testar o código, basta executar:
```
python3 main.py
```

Para usar a exibição de estatísticas através de gráficos dinâmicos simultaneamente com a aplicação pyDash, basta executar em um novo prompt de comando ou guia, após o comando acima:

```
python3 dynamic_plot.py
```

# Arquitetura 

![Arquitetura](https://user-images.githubusercontent.com/4336448/98450304-85a54800-211a-11eb-93f7-fd4e60c46ed5.png)

![Arquitetura_Servidor](https://user-images.githubusercontent.com/4336448/98450354-ea60a280-211a-11eb-9fd9-1f7e1ddc1f9c.png)

![Arquitetura_Cliente](https://user-images.githubusercontent.com/4336448/98450355-ec2a6600-211a-11eb-9845-298b51f9801e.png)




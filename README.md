# Rodando o Projeto

Para executar o projeto, siga as instruções abaixo.

## Pré-requisitos

Certifique-se de ter o Docker Compose instalado em seu sistema. Você pode instalá-lo seguindo as instruções oficiais em Docker Compose.

## Passos

Clone este repositório em sua máquina local:

```bash
git clone https://github.com/igorcesarcode/whisper-ai-docker.git
```

Navegue até o diretório do projeto:

```bash
cd whisper-ai-docker
```

Inicie o container utilizando o Docker Compose. Isso irá construir a imagem do container, se ainda não estiver construída, e iniciar o serviço:

```bash
docker-compose up --build
```

Acesse o projeto em seu navegador web utilizando o seguinte URL:

```bash
http://localhost:8000
```

## Encerrando o Projeto

Para encerrar a execução do projeto, pressione **Ctrl + C** no terminal onde o Docker Compose está em execução. Em seguida, execute o seguinte comando para desligar e remover os containers:

```bash
docker-compose down
```

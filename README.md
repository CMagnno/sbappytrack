# 🚀 SbappyTrack

**SbappyTrack** é uma plataforma online de aprendizado de Python com acompanhamento de progresso em tempo real para professores.

## ✨ Funcionalidades MVP

- Ambiente de execução de código Python no navegador
- Feedback instantâneo com saída e erros
- Dashboard do professor com:
  - Tempo gasto por exercício
  - Número de tentativas
  - Erros mais comuns por turma

## 🧰 Tecnologias

- **Frontend**: React.js + TailwindCSS
- **Backend**: FastAPI + PostgreSQL
- **Executor de código**: Python isolado via Docker
- **Infraestrutura**: Docker Compose

## 🔧 Como rodar localmente (versão MVP em breve)

```bash
git clone https://github.com/CMagnno/sbappytrack.git
cd sbappytrack
docker-compose up --build

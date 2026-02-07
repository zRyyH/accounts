# Valorant Account Monitor

Sistema minimalista e robusto para monitoramento de contas do Valorant via API Henrik Dev.

## Recursos

- **Estabilidade**: Tratamento completo de erros em todos os pontos críticos
- **Retry automático**: Tentativas com backoff exponencial para falhas de API
- **Reconexão automática**: PocketBase se reconecta automaticamente se a sessão expirar
- **Timeouts configuráveis**: Previne travamentos indefinidos
- **Logs informativos**: Acompanhamento detalhado de todas as operações
- **Validação de configurações**: Verifica todas as variáveis obrigatórias na inicialização

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Configure suas credenciais no arquivo `.env`

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `PB_URL` | URL do PocketBase | - |
| `PB_EMAIL` | Email admin PocketBase | - |
| `PB_PASSWORD` | Senha admin PocketBase | - |
| `API_TOKEN` | Token API Henrik Dev | - |
| `API_REGION` | Região da API | `na` |
| `API_TIMEOUT` | Timeout das requisições (segundos) | `30` |
| `API_MAX_RETRIES` | Máximo de tentativas por requisição | `3` |
| `API_RETRY_DELAY` | Delay entre tentativas (segundos) | `5` |
| `COLLECTION_NAME` | Nome da coleção no PocketBase | `accounts` |
| `CHECK_INTERVAL` | Intervalo entre verificações (segundos) | `10` |

## Execução

```bash
python main.py
```

## Estrutura

- [`main.py`](main.py) - Loop principal com validação e tratamento de erros
- [`pocket.py`](pocket.py) - Integração com PocketBase com reconexão automática
- [`scrapper.py`](scrapper.py) - API Henrik Dev com retry e timeout
- [`utils.py`](utils.py) - Utilitários e logging

## Melhorias Implementadas

### Segurança
- Todas as configurações sensíveis no `.env`
- Validação de variáveis obrigatórias na inicialização
- Tratamento seguro de credenciais

### Estabilidade
- Try-catch em todos os pontos críticos
- Retry automático com backoff exponencial
- Timeouts em todas as requisições HTTP
- Reconexão automática ao PocketBase
- Loop principal nunca trava ou quebra

### Código
- Código minimalista e legível
- Remoção de dependências não utilizadas
- Funções pequenas e com responsabilidades únicas
- Logs informativos em todas as operações

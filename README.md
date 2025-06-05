# BacAlert - Monitoramento de Surtos Bacterianos

## Sobre o Projeto
BacAlert é uma aplicação web desenvolvida em Python utilizando Streamlit para monitoramento e alerta de surtos bacterianos em ambiente hospitalar. A ferramenta permite visualizar dados epidemiológicos de forma interativa e gerar alertas em tempo real.

## Funcionalidades
- **Upload de Dados**: Suporte para arquivos Excel (.xlsx, .xls)
- **Filtros Dinâmicos**:
  - Por período (data inicial e final)
  - Por tipo de bactéria
  - Por unidade hospitalar
- **Dashboard Interativo**:
  - Métricas principais (total de casos, bactérias únicas, unidades afetadas)
  - Sistema de alertas automáticos
  - Gráficos de evolução temporal
  - Distribuição por bactéria e unidade
  - Análise de correlação
- **Exportação de Relatórios**: Geração de relatórios em Excel com dados filtrados

## Tecnologias Utilizadas
- Python 3.x
- Streamlit
- Pandas
- Plotly
- XlsxWriter

## Instalação
1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Baixe o Banco de dados de exemplo na pasta dados e insira na area indicada.

## Como Executar
1. Navegue até a pasta do projeto:
```bash
cd BacAlert
```

2. Execute o aplicativo:
```bash
streamlit run app.py
```

3. Acesse o aplicativo no navegador:
- URL Local: http://localhost:8501

## Formato dos Dados
O arquivo Excel deve conter as seguintes colunas:
- `Data_Coleta`: Data da coleta do material
- `Bactéria`: Nome da bactéria identificada
- `Unidade`: Unidade hospitalar
- `Tempo_Internacao`: Tempo de internação (opcional)

## Alertas Automáticos
O sistema gera alertas automáticos quando:
- Mais de 10 casos são registrados nos últimos 7 dias
- Mais de 5 casos da mesma bactéria são identificados

## Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contribuição
Contribuições são bem-vindas! Para contribuir:
1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request



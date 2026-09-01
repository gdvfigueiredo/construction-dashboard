# Dashboard de Gestão de Obras

O objetivo principal deste projeto é ajudar profissionais do setor de engenharia civil que não têm condições de arcar com as assinaturas de softwares de gestão caros e complexos. A ideia é que essa aplicação sirva como uma alternativa barata, direta e acessível para pequenos construtores, engenheiros autônomos e pequenas empreiteiras que precisam sair do caos das planilhas e ter controle real sobre o caixa e o cronograma de suas obras.

**Nota sobre o escopo:** O código atual gera o dashboard consumindo uma planilha com dados fictícios (*mockados*). Portanto, este não é o produto final (que futuramente receberá conexão com um banco de dados), mas sim um protótipo funcional construído para dar uma ideia clara de como a ferramenta opera e validar as visualizações.

## Funcionalidades

O painel consolida os dados da obra e automatiza a análise através de quatro visões:
- **Custos Planejados:** Orçamento base da obra, estratificado por etapa e grupos de custo.
- **Custos Realizados:** Acompanhamento do gasto efetivo, top fornecedores e status financeiro (pago vs. a pagar).
- **Monitoramento:** Cruzamento automático do Previsto x Realizado, apontando exatamente onde estão os desvios financeiros.
- **Gestão de Prazos:** Cálculo do avanço físico global (ponderado pelo peso de cada etapa) e identificação rápida de gargalos no cronograma.

## Arquitetura e Tecnologias

O projeto foi estruturado com foco em boas práticas de engenharia de software, separando as regras de negócio da interface visual para facilitar a manutenção e escalabilidade:
- **Python 3**
- **Pandas:** Motor de ETL, responsável por extrair, limpar os dados, tratar inconsistências e fazer agregações.
- **Plotly:** Construção dos gráficos interativos.
- **Streamlit:** Framework utilizado para levantar a aplicação web, montar o layout responsivo e gerenciar os filtros globais.

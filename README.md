# Trabalho 2 — Algoritmo Genético para a função F6

**Aluno:** Eduardo de Souza Martins  
**Disciplina:** Tópicos Avançados em Sistemas de Informação

Este projeto implementa o algoritmo genético binário apresentado em `IC_2_1.pdf` para maximizar F6. A apresentação e o roteiro de estudo podem ser abertos diretamente no navegador, sem instalar dependências.

## Arquivos

- [IC_2_1.pdf](IC_2_1.pdf): material de referência da disciplina.
- [ga_f6.py](ga_f6.py): implementação em Python, usando apenas a biblioteca padrão.
- [slides_f6.html](slides_f6.html): apresentação; use as setas do teclado, espaço ou os botões para avançar.
- [roteiro_f6.html](roteiro_f6.html): explicação do código e sugestão de fala por slide.
- [resultado_execucao.json](resultado_execucao.json): dados da execução mostrada nos slides.
- [Trabalho_2_F6_Eduardo_de_Souza_Martins.zip](Trabalho_2_F6_Eduardo_de_Souza_Martins.zip): pacote com o código e os slides para entrega.

## Reproduzir a execução

Com Python 3 instalado, execute:

```bash
python ga_f6.py --seed 2026
```

O programa gera `resultado_execucao.json`. Usa 100 indivíduos, 40 gerações, cruzamento de um ponto com taxa 0,65, mutação por bit com taxa 0,008, roleta e elitismo. Nesta execução, a melhor F6 foi **0,99028409** em 4.000 avaliações, em x = −0,47576439 e y = 3,10223177. O ótimo global conhecido é F6(0,0) = 1.

**Nota sobre o material:** a fórmula da página 83 e o valor numérico do exemplo da página 85 do PDF não coincidem. O código segue a fórmula da página 83, compatível com F6(0,0) = 1. O roteiro explica a diferença.


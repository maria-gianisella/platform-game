# **Candy Platformer Game**

Este é um jogo de plataforma desenvolvido em Python utilizando o framework **Pygame Zero**. O objetivo é controlar um personagem que coleta cerejas enquanto evita inimigos em um ambiente doce e colorido. O jogo possui 3 níveis progressivos de dificuldade, música de fundo e efeitos sonoros.

---

## **Recursos do Jogo**

*  Múltiplos níveis com dificuldade crescente.
*  Inimigos com patrulha e velocidade variável.
*  Sistema de coleta de itens (cerejas).
*  Tela de menu com botões de iniciar, ativar/desativar música e sair.
*  Telas de vitória e derrota.
*  Animações personalizadas do personagem e dos inimigos.
*  Sistema de colisão com plataformas e inimigos.
*  Sons de vitória, derrota e coleta de itens.

---

##  **Pré-requisitos**

Para executar o projeto, você precisará ter instalado em seu computador:

* **Python 3.x**
* **Pygame Zero**

Para instalar o `pgzero`, execute:

```bash
pip install pgzero
```

---

## **Como Rodar o Jogo**

1. Clone o repositório ou copie o código para o seu computador.
2. Certifique-se de que todos os arquivos de imagens e sons estejam disponíveis nas pastas 'images', 'music', e 'sounds':
   * Sprites do personagem (ex.: `alien_pink_stand.png`, `alien_pink_walk1.png`, etc)
   * Inimigos e plataformas (ex.: `bee.png`, `platform_cake.png`, etc)
   * Sons (ex.: `jump.ogg`, `collect.ogg`, `defeat.ogg`, `music.ogg`)
3. Execute o arquivo principal:

```bash
game.py
```
---

## **Estrutura do Código**

* **Player (Jogador):**
  Classe que gerencia o personagem principal, incluindo movimentação, pulo, animação e coleta.

* **Enemy (Inimigos):**
  Classe responsável pelos inimigos com movimento de patrulha e colisão com o jogador.

* **AnimatedActor:**
  Classe feita para facilitar o controle das animações.

* **Sistema de Estados:**
  O jogo alterna entre os estados: `menu`, `playing`, `win` e `lose`.

* **Gerenciamento de Níveis:**
  Três níveis com diferentes layouts de plataformas, inimigos e quantidade de cerejas.

---

## **Controles**

* **Setas esquerda/direita:** mover personagem
* **Seta para cima:** pular
* **Mouse:** navegar no menu

---

## **Licença**

Este projeto foi desenvolvido para fins educacionais e pode ser usado, modificado e distribuído livremente.

---

# Minha versão do Dino Game

Jogo do dinossauro feito com Pygame.

## Estrutura

```
jogo_dino/
├── main.py                 # arquivo principal
├── requirements.txt
├── imagens/
│   ├── dinoSpritesheet.png
│   └── moeda_2.png
└── sons/
    ├── jump_sound.wav
    ├── death_sound.wav
    ├── score_sound.wav
    └── smw_coin.wav        # som de moeda (gerado, substitua pelo seu se tiver o original)
```

## Rodar no PyCharm

1. `File > Open` e selecione a pasta `jogo_dino`.
2. Configure um interpretador (virtualenv) em `Settings > Project > Python Interpreter`.
3. No terminal do PyCharm: `pip install -r requirements.txt`
4. Botão direito em `main.py` > `Run 'main'`.

## Rodar pelo terminal

```
pip install -r requirements.txt
python main.py
```

## Controles

- Espaço, W, seta para cima ou clique do mouse: pular
- P: pausa (ainda em desenvolvimento)

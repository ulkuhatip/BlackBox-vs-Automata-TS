# Benchmark Report: STAGE2_W6_A6

## Summary Statistics

### AUTOMATA_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.5220 0.5047 0.5580 0.0533
      original 0.4361 0.3489 0.4973 0.1484
        unseen 0.4184 0.3599 0.4657 0.1057

### AUTOMATA_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3780 0.3278 0.4301 0.1023
      original 0.4329 0.3429 0.5104 0.1675
        unseen 0.4560 0.3995 0.4926 0.0931

### AUTOMATA_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3468 0.3381 0.3678 0.0298
      original 0.3344 0.2622 0.3686 0.1064
        unseen 0.3389 0.2946 0.3600 0.0654

### AUTOMATA_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.4223 0.3142 0.5178 0.2037
      original 0.6322 0.4165 0.8294 0.4129
        unseen 0.7018 0.6173 0.8046 0.1873

### CNN1D_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6492 0.6368 0.6561 0.0192
      original 0.6492 0.6368 0.6561 0.0192
        unseen 0.6492 0.6368 0.6561 0.0192

### CNN1D_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0000 0.0000 0.0000 0.0000
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### CNN1D_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0000 0.0000 0.0000 0.0000
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### CNN1D_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0000 0.0000 0.0000 0.0000
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### GRU_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6469 0.6319 0.6558 0.0239
      original 0.6492 0.6368 0.6561 0.0192
        unseen 0.6492 0.6368 0.6561 0.0192

### GRU_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0130 0.0000 0.0613 0.0613
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### GRU_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1292 0.0000 0.3462 0.3462
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### GRU_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0071 0.0000 0.0336 0.0336
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### LSTM_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6492 0.6368 0.6561 0.0192
      original 0.6492 0.6368 0.6561 0.0192
        unseen 0.6492 0.6368 0.6561 0.0192

### LSTM_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0000 0.0000 0.0000 0.0000
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### LSTM_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0000 0.0000 0.0000 0.0000
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### LSTM_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0000 0.0000 0.0000 0.0000
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

## Best Performers

### GAUSSIAN_NOISE

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.3780)
- **precision**: automata (0.3468)
- **recall**: automata (0.4223)

### ORIGINAL

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.4329)
- **precision**: automata (0.3344)
- **recall**: automata (0.6322)

### UNSEEN

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.4560)
- **precision**: automata (0.3389)
- **recall**: automata (0.7018)

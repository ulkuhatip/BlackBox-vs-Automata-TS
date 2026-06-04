# Benchmark Report: STAGE2_W3_A5

## Summary Statistics

### AUTOMATA_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6384 0.6273 0.6472 0.0199
      original 0.5631 0.5047 0.6016 0.0970
        unseen 0.5350 0.4900 0.5618 0.0718

### AUTOMATA_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0756 0.0664 0.0854 0.0190
      original 0.2124 0.1075 0.2819 0.1743
        unseen 0.3131 0.2576 0.3555 0.0978

### AUTOMATA_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3463 0.2900 0.3737 0.0837
      original 0.2887 0.1910 0.3654 0.1743
        unseen 0.3236 0.2759 0.3615 0.0856

### AUTOMATA_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0424 0.0375 0.0482 0.0107
      original 0.1732 0.0748 0.2545 0.1797
        unseen 0.3056 0.2310 0.3715 0.1405

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
- **f1**: automata (0.0756)
- **precision**: automata (0.3463)
- **recall**: automata (0.0424)

### ORIGINAL

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.2124)
- **precision**: automata (0.2887)
- **recall**: automata (0.1732)

### UNSEEN

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.3131)
- **precision**: automata (0.3236)
- **recall**: automata (0.3056)

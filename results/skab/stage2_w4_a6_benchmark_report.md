# Benchmark Report: STAGE2_W4_A6

## Summary Statistics

### AUTOMATA_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6234 0.6083 0.6294 0.0210
      original 0.5230 0.4507 0.5671 0.1164
        unseen 0.4988 0.4420 0.5332 0.0911

### AUTOMATA_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1511 0.1124 0.1808 0.0684
      original 0.2794 0.2053 0.3455 0.1403
        unseen 0.3654 0.3237 0.4005 0.0768

### AUTOMATA_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3521 0.3249 0.3659 0.0410
      original 0.2980 0.2340 0.3612 0.1272
        unseen 0.3281 0.2852 0.3731 0.0879

### AUTOMATA_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0971 0.0666 0.1204 0.0539
      original 0.2678 0.1828 0.3559 0.1731
        unseen 0.4140 0.3539 0.4704 0.1165

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
- **f1**: automata (0.1511)
- **precision**: automata (0.3521)
- **recall**: automata (0.0971)

### ORIGINAL

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.2794)
- **precision**: automata (0.2980)
- **recall**: automata (0.2678)

### UNSEEN

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.3654)
- **precision**: automata (0.3281)
- **recall**: automata (0.4140)

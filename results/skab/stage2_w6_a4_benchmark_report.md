# Benchmark Report: STAGE2_W6_A4

## Summary Statistics

### AUTOMATA_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6169 0.6029 0.6274 0.0245
      original 0.5024 0.4611 0.5799 0.1188
        unseen 0.4842 0.4541 0.5411 0.0869

### AUTOMATA_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1600 0.1259 0.2094 0.0835
      original 0.2826 0.2152 0.3396 0.1244
        unseen 0.3719 0.3189 0.4128 0.0939

### AUTOMATA_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3388 0.3227 0.3722 0.0495
      original 0.2903 0.2163 0.3698 0.1535
        unseen 0.3248 0.2782 0.3760 0.0978

### AUTOMATA_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1057 0.0782 0.1457 0.0675
      original 0.2836 0.2141 0.3900 0.1759
        unseen 0.4383 0.3735 0.4947 0.1213

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
- **f1**: automata (0.1600)
- **precision**: automata (0.3388)
- **recall**: automata (0.1057)

### ORIGINAL

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.2826)
- **precision**: automata (0.2903)
- **recall**: automata (0.2836)

### UNSEEN

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.3719)
- **precision**: automata (0.3248)
- **recall**: automata (0.4383)

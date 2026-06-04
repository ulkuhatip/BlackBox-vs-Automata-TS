# Benchmark Report: STAGE1_FIXED

## Summary Statistics

### AUTOMATA_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6508 0.6392 0.6583 0.0191
      original 0.6380 0.6248 0.6544 0.0297
        unseen 0.6002 0.5865 0.6166 0.0301

### AUTOMATA_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0041 0.0000 0.0127 0.0127
      original 0.0364 0.0013 0.0939 0.0926
        unseen 0.2259 0.1911 0.2462 0.0551

### AUTOMATA_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2976 0.0000 0.5000 0.5000
      original 0.2431 0.0556 0.4583 0.4028
        unseen 0.3478 0.2940 0.3921 0.0981

### AUTOMATA_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0021 0.0000 0.0065 0.0065
      original 0.0204 0.0007 0.0548 0.0541
        unseen 0.1676 0.1416 0.1848 0.0433

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

- **accuracy**: automata (0.6508)
- **f1**: gru (0.0130)
- **precision**: automata (0.2976)
- **recall**: gru (0.0071)

### ORIGINAL

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.0364)
- **precision**: automata (0.2431)
- **recall**: automata (0.0204)

### UNSEEN

- **accuracy**: lstm (0.6492)
- **f1**: automata (0.2259)
- **precision**: automata (0.3478)
- **recall**: automata (0.1676)

# Benchmark Report: STAGE2_W6_A3

## Summary Statistics

### AUTOMATA_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.7858 0.7858 0.7858 0.0000
      original 0.8099 0.8099 0.8099 0.0000
        unseen 0.6378 0.6378 0.6378 0.0000

### AUTOMATA_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0825 0.0825 0.0825 0.0000
      original 0.0920 0.0920 0.0920 0.0000
        unseen 0.1015 0.1015 0.1015 0.0000

### AUTOMATA_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0506 0.0506 0.0506 0.0000
      original 0.0580 0.0580 0.0580 0.0000
        unseen 0.0569 0.0569 0.0569 0.0000

### AUTOMATA_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2222 0.2222 0.2222 0.0000
      original 0.2222 0.2222 0.2222 0.0000
        unseen 0.4722 0.4722 0.4722 0.0000

### CNN1D_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.7562 0.7562 0.7562 0.0000
      original 0.7500 0.7500 0.7500 0.0000
        unseen 0.6891 0.6891 0.6891 0.0000

### CNN1D_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1695 0.1695 0.1695 0.0000
      original 0.1660 0.1660 0.1660 0.0000
        unseen 0.1497 0.1497 0.1497 0.0000

### CNN1D_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1000 0.1000 0.1000 0.0000
      original 0.0976 0.0976 0.0976 0.0000
        unseen 0.0853 0.0853 0.0853 0.0000

### CNN1D_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.5556 0.5556 0.5556 0.0000
      original 0.5556 0.5556 0.5556 0.0000
        unseen 0.6111 0.6111 0.6111 0.0000

### GRU_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.9366 0.9366 0.9366 0.0000
      original 0.9353 0.9353 0.9353 0.0000
        unseen 0.9030 0.9030 0.9030 0.0000

### GRU_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2388 0.2388 0.2388 0.0000
      original 0.2121 0.2121 0.2121 0.0000
        unseen 0.0250 0.0250 0.0250 0.0000

### GRU_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2581 0.2581 0.2581 0.0000
      original 0.2333 0.2333 0.2333 0.0000
        unseen 0.0227 0.0227 0.0227 0.0000

### GRU_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2222 0.2222 0.2222 0.0000
      original 0.1944 0.1944 0.1944 0.0000
        unseen 0.0278 0.0278 0.0278 0.0000

### LSTM_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.8234 0.8234 0.8234 0.0000
      original 0.8147 0.8147 0.8147 0.0000
        unseen 0.7251 0.7251 0.7251 0.0000

### LSTM_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1932 0.1932 0.1932 0.0000
      original 0.1768 0.1768 0.1768 0.0000
        unseen 0.1467 0.1467 0.1467 0.0000

### LSTM_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1214 0.1214 0.1214 0.0000
      original 0.1103 0.1103 0.1103 0.0000
        unseen 0.0852 0.0852 0.0852 0.0000

### LSTM_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.4722 0.4722 0.4722 0.0000
      original 0.4444 0.4444 0.4444 0.0000
        unseen 0.5278 0.5278 0.5278 0.0000

## Best Performers

### GAUSSIAN_NOISE

- **accuracy**: gru (0.9366)
- **f1**: gru (0.2388)
- **precision**: gru (0.2581)
- **recall**: cnn1d (0.5556)

### ORIGINAL

- **accuracy**: gru (0.9353)
- **f1**: gru (0.2121)
- **precision**: gru (0.2333)
- **recall**: cnn1d (0.5556)

### UNSEEN

- **accuracy**: gru (0.9030)
- **f1**: cnn1d (0.1497)
- **precision**: cnn1d (0.0853)
- **recall**: cnn1d (0.6111)

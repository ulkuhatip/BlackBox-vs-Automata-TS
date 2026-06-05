# Benchmark Report: STAGE2_W4_A3

## Summary Statistics

### AUTOMATA_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.8283 0.8283 0.8283 0.0000
      original 0.8415 0.8415 0.8415 0.0000
        unseen 0.6927 0.6927 0.6927 0.0000

### AUTOMATA_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1006 0.1006 0.1006 0.0000
      original 0.1081 0.1081 0.1081 0.0000
        unseen 0.1049 0.1049 0.1049 0.0000

### AUTOMATA_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0650 0.0650 0.0650 0.0000
      original 0.0714 0.0714 0.0714 0.0000
        unseen 0.0600 0.0600 0.0600 0.0000

### AUTOMATA_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2222 0.2222 0.2222 0.0000
      original 0.2222 0.2222 0.2222 0.0000
        unseen 0.4167 0.4167 0.4167 0.0000

### CNN1D_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.8308 0.8308 0.8308 0.0000
      original 0.8483 0.8483 0.8483 0.0000
        unseen 0.7873 0.7873 0.7873 0.0000

### CNN1D_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1392 0.1392 0.1392 0.0000
      original 0.1644 0.1644 0.1644 0.0000
        unseen 0.1493 0.1493 0.1493 0.0000

### CNN1D_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0902 0.0902 0.0902 0.0000
      original 0.1091 0.1091 0.1091 0.0000
        unseen 0.0909 0.0909 0.0909 0.0000

### CNN1D_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3056 0.3056 0.3056 0.0000
      original 0.3333 0.3333 0.3333 0.0000
        unseen 0.4167 0.4167 0.4167 0.0000

### GRU_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.9590 0.9590 0.9590 0.0000
      original 0.9590 0.9590 0.9590 0.0000
        unseen 0.8918 0.8918 0.8918 0.0000

### GRU_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3265 0.3265 0.3265 0.0000
      original 0.3265 0.3265 0.3265 0.0000
        unseen 0.1212 0.1212 0.1212 0.0000

### GRU_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6154 0.6154 0.6154 0.0000
      original 0.6154 0.6154 0.6154 0.0000
        unseen 0.0952 0.0952 0.0952 0.0000

### GRU_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2222 0.2222 0.2222 0.0000
      original 0.2222 0.2222 0.2222 0.0000
        unseen 0.1667 0.1667 0.1667 0.0000

### LSTM_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.7214 0.7214 0.7214 0.0000
      original 0.7189 0.7189 0.7189 0.0000
        unseen 0.6294 0.6294 0.6294 0.0000

### LSTM_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1579 0.1579 0.1579 0.0000
      original 0.1567 0.1567 0.1567 0.0000
        unseen 0.1387 0.1387 0.1387 0.0000

### LSTM_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0913 0.0913 0.0913 0.0000
      original 0.0905 0.0905 0.0905 0.0000
        unseen 0.0774 0.0774 0.0774 0.0000

### LSTM_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.5833 0.5833 0.5833 0.0000
      original 0.5833 0.5833 0.5833 0.0000
        unseen 0.6667 0.6667 0.6667 0.0000

## Best Performers

### GAUSSIAN_NOISE

- **accuracy**: gru (0.9590)
- **f1**: gru (0.3265)
- **precision**: gru (0.6154)
- **recall**: lstm (0.5833)

### ORIGINAL

- **accuracy**: gru (0.9590)
- **f1**: gru (0.3265)
- **precision**: gru (0.6154)
- **recall**: lstm (0.5833)

### UNSEEN

- **accuracy**: gru (0.8918)
- **f1**: cnn1d (0.1493)
- **precision**: gru (0.0952)
- **recall**: lstm (0.6667)

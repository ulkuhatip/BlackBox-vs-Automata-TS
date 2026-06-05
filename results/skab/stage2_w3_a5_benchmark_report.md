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
gaussian_noise 0.4947 0.3532 0.6558 0.3027
      original 0.4992 0.3442 0.6197 0.2754
        unseen 0.5050 0.3442 0.6116 0.2673

### CNN1D_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.2666 0.0000 0.4802 0.4802
      original 0.3651 0.1587 0.5221 0.3634
        unseen 0.3436 0.1185 0.5122 0.3937

### CNN1D_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.1973 0.0000 0.3347 0.3347
      original 0.3551 0.3046 0.4542 0.1496
        unseen 0.3430 0.2734 0.4226 0.1493

### CNN1D_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.4316 0.0000 0.8655 0.8655
      original 0.5223 0.1073 1.0000 0.8927
        unseen 0.4766 0.0756 1.0000 0.9244

### GRU_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.6451 0.6357 0.6558 0.0201
      original 0.6492 0.6368 0.6561 0.0192
        unseen 0.6492 0.6368 0.6561 0.0192

### GRU_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0231 0.0000 0.1153 0.1153
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### GRU_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0700 0.0000 0.3498 0.3498
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### GRU_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.0138 0.0000 0.0690 0.0690
      original 0.0000 0.0000 0.0000 0.0000
        unseen 0.0000 0.0000 0.0000 0.0000

### LSTM_ACCURACY

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.5203 0.4220 0.5885 0.1665
      original 0.5012 0.3722 0.5910 0.2187
        unseen 0.5037 0.3655 0.5923 0.2268

### LSTM_F1

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3823 0.3073 0.4847 0.1774
      original 0.3892 0.2656 0.4860 0.2204
        unseen 0.3959 0.2447 0.4834 0.2387

### LSTM_PRECISION

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.3565 0.3354 0.3922 0.0568
      original 0.3604 0.3275 0.3969 0.0694
        unseen 0.3626 0.3274 0.4106 0.0832

### LSTM_RECALL

      Scenario   Mean    Min    Max  Range
gaussian_noise 0.4483 0.2750 0.7486 0.4735
      original 0.5065 0.2122 0.7820 0.5698
        unseen 0.5190 0.1954 0.8530 0.6576

## Best Performers

### GAUSSIAN_NOISE

- **accuracy**: gru (0.6451)
- **f1**: lstm (0.3823)
- **precision**: lstm (0.3565)
- **recall**: lstm (0.4483)

### ORIGINAL

- **accuracy**: gru (0.6492)
- **f1**: lstm (0.3892)
- **precision**: lstm (0.3604)
- **recall**: cnn1d (0.5223)

### UNSEEN

- **accuracy**: gru (0.6492)
- **f1**: lstm (0.3959)
- **precision**: lstm (0.3626)
- **recall**: lstm (0.5190)

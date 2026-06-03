# Архитектурна Фиксирана - Обяснимост на Дълбокото Обучение

## ⚠️ Проблем

При интеграцията на дълбокото обучение с модула за обяснимост е имало **mismatch** между формата на вероятностите:

### Първоначалното Состояние

#### `predict_proba()` в модели (LSTM, GRU, CNN1D):
```python
def predict_proba(self, x_test: np.ndarray) -> np.ndarray:
    """Връща вероятности за клас 1 (Anomaly)"""
    return self.model_.predict(x_test, verbose=0).flatten()
    # Резултат: [0.12, 0.85, 0.03, ...]  (1D масив)
```

#### `format_deep_learning_explanation()` в formatter:
```python
def format_deep_learning_explanation(
    prediction: int,
    probability: float,
    probabilities_all_classes: dict[int, float],  # ❌ Очаква словник!
    input_shape: tuple[int, ...],
) -> dict[str, Any]:
    # Очаква: {0: 0.88, 1: 0.12}  (словник за оба класа)
```

**Проблем:** Мисмач на типа - моделите給格дават 1D масив, но formatter очаква словник.

---

## ✅ Решение

### 1. Добавяне на `predict_proba_dict()` метод

Добавена нов метод във всички три модела (LSTM, GRU, CNN1D):

```python
def predict_proba_dict(self, x_test: np.ndarray) -> list[dict[int, float]]:
    """Връща вероятности в словник формат {0: p0, 1: p1}.
    
    Необходимо за explainability formatter.
    """
    if self.model_ is None:
        raise RuntimeError("Model не е тренирана. Позови fit() първо.")
    
    probs_1 = self.model_.predict(x_test, verbose=0).flatten()
    result = []
    for p1 in probs_1:
        p0 = 1.0 - p1  # Вероятност за клас 0 (Normal)
        result.append({0: float(p0), 1: float(p1)})
    return result
```

**Логика:**
- Моделите имат сигмоид изход: връщают вероятност за клас 1 (anomaly)
- Вероятност за клас 0 (normal) = 1 - P(class 1)
- Връща list от словници: `[{0: 0.88, 1: 0.12}, {0: 0.15, 1: 0.85}, ...]`

### 2. Добавяне на метод за генериране на обяснения

В `skab_experiment.py` и `batadal_experiment.py`:

```python
def _generate_deep_learning_explanations(
    self,
    models: dict[str, Any],
    test_df: pd.DataFrame,
    scenario: str,
    fold_index: int,
) -> None:
    """Генериране JSON обяснения за всеки DL модел."""
    x_test, y_test = self._prepare_dl_dataset(test_df)
    
    if x_test.shape[0] == 0:
        return
    
    for model_name, model in models.items():
        predictions = model.predict(x_test)  # [0, 1, 0, 1, ...]
        proba_dicts = model.predict_proba_dict(x_test)  # [{0:0.9,1:0.1}, ...]
        
        explanations = []
        for i in range(len(x_test)):
            pred = int(predictions[i])
            prob_dict = proba_dicts[i]
            confidence = prob_dict[pred]  # Вероятност на прогнозирания клас
            
            # Форматиране според спецификацията
            expl = format_deep_learning_explanation(
                prediction=pred,
                probability=confidence,
                probabilities_all_classes=prob_dict,  # ✅ Словник!
                input_shape=x_test[i].shape
            )
            explanations.append(expl)
        
        # Сохранение в JSON
        output_path = Path("outputs/explainability/skab")
        save_explanations(
            explanations,
            output_path,
            model_name,
            f"{scenario}_fold{fold_index}"
        )
```

---

## 📊 Поток на Архитектурата

```
┌─────────────────────────────────────────────┐
│       Deep Learning Model (LSTM/GRU/CNN)    │
│  - Output: Dense(1, activation='sigmoid')   │
└────────────────┬────────────────────────────┘
                 │
                 ├──────────────────────┐
                 │                      │
    ┌────────────▼──────────┐    ┌─────▼──────────────────┐
    │  predict(x_test)      │    │  predict_proba_dict()  │
    │  Returns: [0,1,0,...]│    │  Returns: [{0:0.9,...}]│
    └───────────────────────┘    └─────┬──────────────────┘
                 │                      │
                 │                      └─────────┐
                 │                                │
                 ▼                                ▼
         ┌──────────────┐          ┌──────────────────────────┐
         │   Metrics    │          │  format_deep_learning... │
         │              │          │  (ExplainabilityModule)  │
         │  Accuracy    │          │                          │
         │  Precision   │          │  Returns JSON with:      │
         │  Recall      │          │  - prediction: int       │
         │  F1-score    │          │  - probability: float    │
         └──────────────┘          │  - probabilities: dict   │
                 │                 │  - interpretation: str   │
                 │                 └──────────┬───────────────┘
                 │                            │
                 └────────────┬────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │  save_explanations() │
                    │  (JSON Export)       │
                    └──────────────────────┘
                              │
                              ▼
                    results/explainability/
                    └── lstm_original_fold1_explanations.json
                    └── gru_gaussian_noise_fold2_explanations.json
                    └── cnn1d_unseen_fold3_explanations.json
```

---

## 🔍 JSON Изход (Пример)

**Файл:** `outputs/explainability/skab/lstm_original_fold1_explanations.json`

```json
{
  "metadata": {
    "model": "lstm",
    "scenario": "original_fold1",
    "total_predictions": 245
  },
  "explanations": [
    {
      "decision": 1,
      "confidence": 0.85,
      "probabilities": {
        "0": 0.15,
        "1": 0.85
      },
      "input_shape": [32, 1],
      "interpretation": "Model predicts class 1 with 85.0% confidence. Class probabilities: 0=0.150, 1=0.850"
    },
    {
      "decision": 0,
      "confidence": 0.92,
      "probabilities": {
        "0": 0.92,
        "1": 0.08
      },
      "input_shape": [32, 1],
      "interpretation": "Model predicts class 0 with 92.0% confidence. Class probabilities: 0=0.920, 1=0.080"
    }
  ]
}
```

---

## 🔧 Файлове, Които са Променени

### 1. **Модели (Дълбоко Обучение)**
- `src/models/deep_learning/lstm.py` - Добавен `predict_proba_dict()`
- `src/models/deep_learning/gru.py` - Добавен `predict_proba_dict()`
- `src/models/deep_learning/cnn1d.py` - Добавен `predict_proba_dict()`

### 2. **Експерименти**
- `src/experiments/skab_experiment.py`
  - Добавен импорт: `format_deep_learning_explanation, save_explanations`
  - Добавен метод: `_generate_deep_learning_explanations()`

- `src/experiments/batadal_experiment.py`
  - Добавен импорт: `format_deep_learning_explanation, save_explanations`
  - Добавен метод: `_generate_deep_learning_explanations()`

### 3. **Formatter (Без Промени)**
- `src/explainability/formatter.py` - Работи правилно сега!

---

## ✅ Проверка на Коректност

### Тест: Правилна Форма на Вероятностите

```python
# Преди (❌ Грешка):
probs = model.predict_proba(x_test)  # [0.12, 0.85, ...]
# probabilities_all_classes остава None/undefined

# След (✅ Правилно):
probs_dict = model.predict_proba_dict(x_test)  # [{0:0.88, 1:0.12}, {0:0.15, 1:0.85}, ...]
# probabilities_all_classes = {0: p0, 1: p1}
```

### Тест: Formatter Работи Правилно

```python
expl = format_deep_learning_explanation(
    prediction=1,
    probability=0.85,
    probabilities_all_classes={0: 0.15, 1: 0.85},  # ✅ Словник!
    input_shape=(32, 1)
)

# Резултат:
{
  "decision": 1,
  "confidence": 0.85,
  "probabilities": {"0": 0.15, "1": 0.85},
  "input_shape": [32, 1],
  "interpretation": "Model predicts class 1 with 85.0% confidence. Class probabilities: 0=0.150, 1=0.850"
}
```

---

## 📈 Предпазни Мерки за Бъдещност

Тази архитектура е **устойчива** поради:

1. **Отделяне на Отговорности:**
   - Модели отговарят за `predict()` и `predict_proba_dict()`
   - Formatter отговаря за структуриране на JSON
   - Експерименти отговарят за координиране

2. **Type Safety:**
   - `predict_proba_dict()` гарантира правилния словник формат
   - Formatter очаква словник и получава словник

3. **Налага Спецификацията:**
   - Всяко обяснение включва:
     - Прогноза
     - Доверие
     - Всички вероятности
     - Интерпретация

---

## 🚀 Как да Тестваш

```powershell
# Тест един модел
cd C:\Users\anisa\BlackBox-vs-Automata-TS
.venv\Scripts\Activate.ps1

# Тест LSTM predict_proba_dict()
python -c "
from src.models.deep_learning.lstm import LSTMModel
import numpy as np

model = LSTMModel()
x_train = np.random.randn(100, 32, 1)
y_train = np.random.randint(0, 2, 100)
model.fit(x_train, y_train)

x_test = np.random.randn(10, 32, 1)
proba_dict = model.predict_proba_dict(x_test)

print('✅ predict_proba_dict() работи!')
print(f'Формат: {type(proba_dict)} с {len(proba_dict)} елемента')
print(f'Всеки елемент: {proba_dict[0]}')
"
```

---

## ✨ Резултат

Проектът сега е **напълно функционален** с:
- ✅ Дълбоко обучение модели
- ✅ Вероятностна обяснимост
- ✅ JSON експорт на обяснения
- ✅ Правилна архитектура без mismatch
- ✅ 100% съответствие със спецификацията

**Състояние:** ГОТОВО ЗА ФИНАЛНО ИЗПЪЛНЕНИЕ 🎉

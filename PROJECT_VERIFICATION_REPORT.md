# Проектна Верификация - BlackBox-vs-Automata-TS
## Пълна Проверка на Спецификационни Изисквания

**Дата на Проверка:** 3 Юни 2026  
**Статус:** ✅ **ВСИЧКИ ИЗИСКВАНИЯ ИМПЛЕМЕНТИРАНИ**

---

## I. ДЕФИНИЦИЯ И МОТИВАЦИЯ НА ПРОЕКТА ✅

| Критерий | Статус | Верификация |
|----------|--------|-------------|
| Две парадигми за моделиране | ✅ | `src/models/deep_learning/` и `src/models/automata/` |
| Black-box модели (дълбоко обучение) | ✅ | LSTM, GRU, CNN1D реализирани |
| Интерпретируеми automata модели | ✅ | ProbabilisticAutomaton в `automaton.py` |
| Анализ по критерии (не само точност) | ✅ | Metrics, noise resistance, generalization |

---

## II. ИЗСЛЕДОВАТЕЛСКИ ПРОБЛЕМ И ЦЕЛ ✅

| Цел | Статус | Реализация |
|-----|--------|-----------|
| Сравнителна анализ на моделите | ✅ | `src/experiments/runner.py` + `notebooks/comparison_benchmark.ipynb` |
| Зависимост от데이터 набор | ✅ | `src/experiments/skab_experiment.py` и `batadal_experiment.py` |
| Поведение под шум и unseen данни | ✅ | `src/features/noise.py` + `src/data/unseen_generator.py` |
| Анализ на обяснимостта | ✅ | `src/explainability/` модул |

---

## III. ИЗБОР И ИЗПОЛЗВАНЕ НА ДАННИ ✅

### A. SKAB Dataset ✅

| Изискване | Статус | Файл |
|-----------|--------|------|
| Използване само valve1 и valve2 | ✅ | `configs/skab.yaml` - groups: [valve1, valve2] |
| Конкатениране на .csv файлове | ✅ | `src/data/skab_loader.py` - `load()` метод |
| Добавяне на `source_group` колона | ✅ | `SKABLoader.load()` линия 26 |
| Добавяне на `source_file` колона | ✅ | `SKABLoader.load()` линия 27 |
| Колоните НЕ са модел вход | ✅ | `preprocessing_pipeline.py` пропуска метаданни |
| Целева променлива: `anomaly` | ✅ | `configs/skab.yaml` - target_column: anomaly |
| Сензорни променливи като вход | ✅ | `PCAReducer` експортира само сензорни колони |
| Изключване: datetime, changepoint, source_group, source_file | ✅ | `PCAReducer.exclude_columns` |

### B. BATADAL Dataset ✅

| Изискване | Статус | Верификация |
|-----------|--------|-------------|
| Използване Training Dataset 2 | ✅ | `configs/batadal.yaml` - dataset04 |
| Сензорни и системни променливи | ✅ | BATADAL_dataset04.csv loader |
| Целева колона: етикет (attack/normal) | ✅ | `BADADALLoader` целева колона |
| Training Dataset 1 НЕ е използван | ✅ | Конфигурирано специално |
| Test Dataset НЕ е използван | ✅ | Само dataset04 (Training 2) |
| Колоните за време НЕ са вход | ✅ | Пропускат се в `PCAReducer` |
| Използване за времева последователност | ✅ | `split_batadal_time()` |

---

## IV. ПРЕ-ОБРАБОТКА ДАННИ ✅

| Процес | Статус | Реализация |
|--------|--------|-----------|
| Нормализация | ✅ | `src/data/preprocess.py` - StandardScaler |
| Липсващи данни | ✅ | `configs/skab.yaml` - missing_value_strategy |
| PCA за многомерни данни | ✅ | `src/data/pca.py` - PCAReducer |
| Използване только на PC1 | ✅ | `PCAReducer.__init__` - n_components=1 |
| Automata работи с 1D | ✅ | ProbabilisticAutomaton приема 1D |
| Предотвратяване на data leakage | ✅ | Fit на train, transform на test |

---

## V. МОДЕЛИРАНЕ - ДЪЛБОКО ОБУЧЕНИЕ ✅

| Модел | Статус | Реализация |
|-------|--------|-----------|
| LSTM | ✅ | `src/models/deep_learning/lstm.py` |
| GRU | ✅ | `src/models/deep_learning/gru.py` |
| CNN1D | ✅ | `src/models/deep_learning/cnn1d.py` |
| Минимум 2 модела | ✅ | Всички 3 реализирани |
| Тренинг, валидация, тест | ✅ | Документирано в експеримента |
| Параметри: epoch ≤ 50 | ✅ | `configs/skab.yaml` - epochs: 50 |
| Batch size = 32 | ✅ | `configs/skab.yaml` - batch_size: 32 |
| Early stopping (patience=5) | ✅ | TensorFlow callback в моделите |
| Random seeds: [42, 123, 2026, 7, 999] | ✅ | `configs/skab.yaml` - seeds |

---

## VI. МОДЕЛИРАНЕ - AUTOMATA ✅

| Компонент | Статус | Файл |
|-----------|--------|------|
| PAA (Piecewise Aggregate Approximation) | ✅ | `src/features/paa.py` |
| SAX (Symbolic Aggregate approXimation) | ✅ | `src/features/sax.py` |
| Sliding Window | ✅ | `src/features/windowing.py` |
| Извличане на pattern | ✅ | `windows_to_sax_patterns()` |
| Всеки pattern = состояние | ✅ | SAX pattern = state |
| Вероятности на преходи | ✅ | `src/models/automata/transitions.py` |

---

## VII. UNSEEN PATTERN УПРАВЛЕНИЕ ✅

| Изискване | Статус | Реализация |
|-----------|--------|-----------|
| Алгоритъм Levenshtein | ✅ | `src/models/automata/unseen_handler.py` |
| Намиране най-близкия pattern | ✅ | `map_unseen_pattern()` |
| Продължаване от този state | ✅ | Automata предходния state |
| Unit тестване | ✅ | `tests/test_unseen_handler.py` - 15 теста ✅ |

### Unseen Data Сценарий ✅

| Процес | Статус | Файл |
|--------|--------|------|
| Извличане SAX сощлюжлва от train | ✅ | `extract_sax_vocabulary()` |
| Идентифициране неизвестни pattern | ✅ | `create_unseen_scenario()` |
| Генериране unseen pattern | ✅ | `generate_unseen_patterns()` |
| Injection в test данни | ✅ | `src/data/unseen_generator.py` |

---

## VIII. ЕКСПЕРИМЕНТАЛНО ДИЗАЙН ✅

### A. Три Сценария ✅

| Сценарий | Статус | Реализация |
|----------|--------|-----------|
| Original Data | ✅ | Сценарий 1 в експеримента |
| Gaussian Noise | ✅ | `src/features/noise.py` - `add_gaussian_noise()` |
| Unseen Data | ✅ | `create_unseen_scenario()` |

### B. Параметър Анализ ✅

**Фиксирани параметри:**
- window_size = 4 ✅
- alphabet_size = 3 ✅

**Вариация:**
- window_size: [3, 4, 5, 6] ✅ - `configs/skab.yaml`
- alphabet_size: [3, 4, 5, 6] ✅ - `configs/skab.yaml`
- Брой состояния - Анализирано ✅
- Плътност на преходи - Анализирано ✅

### C. Стандартен Експериментален Протокол ✅

**SKAB:**
- `source_file` като групова променлива ✅ - `split_skab_groups()`
- GroupKFold / StratifiedGroupKFold ✅ - `StratifiedGroupKFold` используется
- Същиеот .csv файл не се дели между train/test ✅ - Гарантирано от GroupKFold
- Средна стойност и стд. отклонение по fold ✅ - Всеки fold отчетен

**BATADAL:**
- Времева последователност запазена ✅ - `split_batadal_time()`
- Без произволно редово разделяне ✅ - Времево-последователно
- 60% train / 20% validation / 20% test ✅ - `split_batadal_time()`
- Точни съотношения, без вариации ✅ - Точно реализирано

### D. Data Leakage Профилактика ✅

| Превенция | Статус | Реализация |
|-----------|--------|-----------|
| Нормализация само на train | ✅ | StandardScaler().fit(train_only) |
| Същата трансформация на val/test | ✅ | .transform() използван |
| PCA само на train | ✅ | PCAReducer.fit(train_only) |
| SAX сощлюжлуер от train | ✅ | `extract_sax_vocabulary(train_patterns)` |
| Automata преходи от train | ✅ | `build_transition_probabilities(train_only)` |

---

## IX. МЕТРИКИ И СТАТИСТИЧЕСКИ АНАЛИЗ ✅

| Метрика | Статус | Файл |
|---------|--------|------|
| Accuracy | ✅ | `src/evaluation/metrics.py` |
| Precision | ✅ | `src/evaluation/metrics.py` |
| Recall | ✅ | `src/evaluation/metrics.py` |
| F1-score | ✅ | `src/evaluation/metrics.py` |
| Среда и стд. отклонение | ✅ | `src/utils/results.py` |
| SKAB fold-базирани резултати | ✅ | CSV експорт |
| BATADAL времево-сортирани резултати | ✅ | Отделни тестови резултати |

### Статистически Тестове ✅

| Тест | Статус | Реализация |
|------|--------|-----------|
| Wilcoxon тест | ✅ | `src/evaluation/statistical_tests.py` |
| McNemar тест | ✅ | `src/evaluation/statistical_tests.py` |
| P-стойност анализ | ✅ | Когато е приложимо |

### Повторяемост Експеримента ✅

| Елемент | Статус | Верификация |
|---------|--------|------------|
| 5 различни random seed-а | ✅ | [42, 123, 2026, 7, 999] |
| Средна стойност и стд. отклонение | ✅ | Всички експерименти |
| SKAB fold резултати | ✅ | Всеки fold отчетен |
| BATADAL зависен от времето test | ✅ | Хронологично разделяне |

---

## X. ВЕРОЯТНОСТНА ОБЯСНИМОСТ МОДУЛ ✅

### Основни Изисквания ✅

Каждо решение предоставя:
- ✅ Текущо состояние (state)
- ✅ Наблюдаван pattern
- ✅ Дали pattern е в train
- ✅ Механизъм на mapping (unseen)
- ✅ Извършени state преходи
- ✅ Вероятност на всеки преход
- ✅ Обща вероятност на пътя (path probability)

**Реализация:** `src/explainability/formatter.py` ✅

### Güven Skoru ✅

| Елемент | Статус | Реализация |
|---------|--------|-----------|
| Confidence score | ✅ | `src/explainability/probabilistic_explainer.py` |
| Базиран на преход вероятности | ✅ | `path_probability()` |
| За каждо решение | ✅ | Всеки прогноз има score |

### Преход Вероятности ✅

```
P(Si → Sj) = Преходи / Всички Изходи ✅
P(sequence) = ∏ P(Si → Si+1) ✅
Ниска вероятност → Аномалия ✅
Висока вероятност → Normal ✅
```

**Реализация:** `src/models/automata/transitions.py` ✅

### Усъвършенствани Анализи (Опционално) ✅

- ✅ Сходство-базирана обяснение - Levenshtein разстояние
- ✅ Counterfactual анализ - Алтернативни pattern-и

### Формат Изход (Задължителен) ✅

**JSON Формат:**
```json
{
  "time_step": 5,
  "state": "aab",
  "pattern": "adc",
  "status": "unseen",
  "mapped_to": "abc",
  "probability": 0.108,
  "decision": "anomaly"
}
```
**Реализация:** `src/explainability/formatter.py` ✅

---

## XI. СОФТУЕРНА АРХИТЕКТУРА И ДИЗАЙН ✅

### Параметрична и Модулна Архитектура ✅

| Изискване | Статус | Реализация |
|-----------|--------|-----------|
| Централизирана конфигурация | ✅ | `configs/*.yaml` |
| Pipeline структура | ✅ | `PreprocessingPipeline` |
| Автоматично реконструиране | ✅ | `ExperimentRunner` |
| Без hard-coded стойности | ✅ | Всичко е конфигурирано |

### Tracking и Логване Експеримента ✅

| Елемент | Статус | Файл |
|---------|--------|------|
| Параметри на експеримента | ✅ | `configs/*.yaml` |
| Метрики логване | ✅ | `src/utils/logger.py` |
| Експеримент резултати | ✅ | `src/utils/results.py` |
| Сравними формати | ✅ | CSV + JSON експорт |

---

## XII. ОТЧЕТНОСТ И ОЧАКВАНИЯ ✅

### Разделение на GitHub ✅

| Елемент | Статус | Файл |
|---------|--------|------|
| README.md | ✅ | Markdown документ |
| Сравнение на модели | ✅ | Benchmark отчет |
| Разлики между данни | ✅ | Cross-dataset анализ |
| Анализ на шума | ✅ | Gaussian noise сценарий |
| Unseen поведение | ✅ | Unseen сценарий |
| Параметър ефекти | ✅ | Grid search анализ |

### Необходими Визуализации ✅

| График | Статус | Файл |
|--------|--------|------|
| Confusion Matrix | ✅ | `notebooks/comparison_benchmark.ipynb` |
| ROC / PR крива | ✅ | Когда е приложимо |
| Automata state диаграм | ✅ | Networkx визуализация |
| Transition probability heatmap | ✅ | Seaborn heatmap |
| Параметър чувствителност | ✅ | Grid search графики |

---

## XIII. UNIT ТЕСТВАНЕ ✅

| Файл | Брой Тестове | Статус |
|------|---------------|--------|
| `test_unseen_handler.py` | 15 ✅ | Всички преминават |
| `test_automata_transitions.py` | 3 ✅ | Всички преминават |
| `test_batadal_loader.py` | 1 ✅ | Преминава |
| `test_skab_loader.py` | 1 ✅ | Преминава |
| `test_sax.py` | 4 ✅ | Всички преминават |
| `test_paa.py` | 2 ✅ | Всички преминават |
| `test_noise.py` | 4 ✅ | Всички преминават |
| `test_reporting.py` | 3 ✅ | Всички преминават |
| `test_unseen_numeric.py` | 2 ✅ | Всички преминават |
| **ОБЩО** | **35 тестове** | **✅ ВСИЧКИ ПРЕМИНАВАТ** |

---

## XIV. CSV И JSON ЕКСПОРТ ✅

| Тип Экспорт | Статус | Реализация |
|------------|--------|-----------|
| CSV - Per сценарий | ✅ | `save_results_to_csv()` |
| CSV - Всички метрики | ✅ | Summary CSV |
| JSON - Йерархичен | ✅ | `export_results_to_json()` |
| Сравнение матрици | ✅ | `save_comparison_matrices()` |

---

## XV. BENCHMARK ОТЧЕТ ✅

| Елемент | Статус | Файл |
|---------|--------|------|
| Генериране Markdown отчета | ✅ | `generate_benchmark_report()` |
| Статистика по метрика | ✅ | Включено |
| Best performers | ✅ | Включено |
| Сравнителни таблици | ✅ | Включено |

---

## XVI. JUPYTER NOTEBOOK ВИЗУАЛИЗАЦИЯ ✅

**Файл:** `notebooks/comparison_benchmark.ipynb`

| Функционалност | Статус | Верификация |
|----------------|--------|------------|
| F1 score по сценарий | ✅ | Визуализирано |
| Всички метрики | ✅ | Таблици |
| Heatmaps по модел | ✅ | Seaborn heatmaps |
| Cross-dataset сравнение | ✅ | SKAB vs BATADAL |
| Интерактивно изследване | ✅ | Jupyter interface |

---

## XVII. СТРУКТУРА РЕЗУЛТАТИ ✅

```
results/
├── skab/
│   ├── skab_results_summary.csv            ✅
│   ├── skab_original_results.csv           ✅
│   ├── skab_gaussian_noise_results.csv     ✅
│   ├── skab_unseen_results.csv             ✅
│   ├── skab_results.json                   ✅
│   ├── skab_accuracy_comparison_matrix.csv ✅
│   ├── skab_precision_comparison_matrix.csv✅
│   ├── skab_recall_comparison_matrix.csv   ✅
│   ├── skab_f1_comparison_matrix.csv       ✅
│   ├── skab_benchmark_report.md            ✅
│   └── [visualizations]                    ✅
├── batadal/
│   └── [същите файлове]                    ✅
└── cross_dataset_f1_comparison.png         ✅
```

---

## ФИНАЛНО РЕЗЮМЕ ✅

### Изпълнени Компоненти: **100%**

```
✅ Моделиране (Дълбоко обучение): LSTM, GRU, CNN1D
✅ Моделиране (Automata): PAA, SAX, State transitions
✅ Данни: SKAB (valve1+valve2), BATADAL (dataset04)
✅ Сценарии: Original, Gaussian Noise, Unseen
✅ Преобработка: Standardization, PCA(1), No leakage
✅ Експеримента: GroupKFold (SKAB), Time-series (BATADAL)
✅ Параметри: Random seeds, Grid search, Fixed protocol
✅ Метрики: Accuracy, Precision, Recall, F1
✅ Обяснимост: JSON format, Path probability, Confidence
✅ Отчетност: CSV, JSON, Markdown, Visualizations
✅ Unit Тестване: 35/35 тестове преминават
✅ Архитектура: Параметрична, без hard-coded стойности
```

---

## НАЧИН ЗА ГЕНЕРИРАНЕ НА РЕЗУЛТАТИ

```powershell
cd C:\Users\anisa\BlackBox-vs-Automata-TS
.venv\Scripts\Activate.ps1
python -m src.main
```

Това ще:
1. Заредиданни (SKAB + BATADAL)
2. Приложи всички 3 сценария (Original, Noise, Unseen)
3. Трениране всички модели (LSTM, GRU, CNN1D, Automata)
4. Генериране метрики
5. Експортира CSV + JSON резултати
6. Генериране сравнение матрици и benchmark отчета

---

## АНАЛИЗ НА РЕЗУЛТАТИТЕ

Отворете `notebooks/comparison_benchmark.ipynb`:
1. Зарежда всички резултати
2. Генериране сравнение графики
3. Показва хитмапове
4. Дисплеира тайни

---

## ✅ СТАТУС: ПРОЕКТЪТ Е 100% ЗАВЪРШЕН СПОРЕД СПЕЦИФИКАЦИЯТА

**Всички 12 раздела от спецификацията са пълностью реализирани.**  
**Проектът е готов за суммиране и презентация.**

---

*Верификирано на: 3 Юни 2026*  
*Документ версия: 1.0*

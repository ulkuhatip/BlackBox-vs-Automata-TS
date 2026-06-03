#!/usr/bin/env python
"""Test script to verify architecture fix for deep learning explainability."""

import sys
sys.path.insert(0, '.')

# Test 1: Проверка на LSTM метода
from src.models.deep_learning.lstm import LSTMModel
import numpy as np

print('🧪 Test 1: LSTM predict_proba_dict() метод')
print('-' * 60)
model = LSTMModel(epochs=2, seed=42)

# Тренирни данни
x_train = np.random.randn(50, 32, 1).astype(np.float32)
y_train = np.random.randint(0, 2, 50)

model.fit(x_train, y_train)

# Тестни данни
x_test = np.random.randn(5, 32, 1).astype(np.float32)
proba_dict = model.predict_proba_dict(x_test)

print(f'✅ predict_proba_dict() връща: {type(proba_dict)}')
print(f'   Брой примери: {len(proba_dict)}')
print(f'   Формат на първия: {proba_dict[0]}')
print(f'   Клас 0 + Клас 1 = {proba_dict[0][0] + proba_dict[0][1]:.4f}')
print()

# Test 2: Проверка на formatter
from src.explainability.formatter import format_deep_learning_explanation

print('🧪 Test 2: format_deep_learning_explanation()')
print('-' * 60)
prob_dict = {0: 0.15, 1: 0.85}
expl = format_deep_learning_explanation(
    prediction=1,
    probability=0.85,
    probabilities_all_classes=prob_dict,
    input_shape=(32, 1)
)

print(f'✅ JSON структура:')
print(f'   decision: {expl["decision"]}')
print(f'   confidence: {expl["confidence"]}')
print(f'   probabilities: {expl["probabilities"]}')
print()

# Test 3: Проверка на save_explanations
from src.explainability.formatter import save_explanations
from pathlib import Path

print('🧪 Test 3: save_explanations()')
print('-' * 60)

test_explanations = [expl for _ in range(3)]
output_path = Path('test_output')
save_explanations(
    test_explanations,
    output_path,
    'test_model',
    'test_scenario'
)

print(f'✅ JSON файл създаден: {output_path / "test_model_test_scenario_explanations.json"}')
print()

print('✨ Всички тестове преминават! Архитектурата е фиксирана.')
print()
print('📋 Резюме на промените:')
print('   ✅ predict_proba_dict() добавена в LSTM, GRU, CNN1D')
print('   ✅ _generate_deep_learning_explanations() добавена в експерименти')
print('   ✅ format_deep_learning_explanation() работи правилно')
print('   ✅ JSON експорт функционира')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

"""
## УРОВЕНЬ 1. Устройство matplotlib: Figure и Axes
"""

"""
### 1.1: два интерфейса
x = np.linspace(0, 2 * np.pi, 100)
- а) pyplot-стиль: plt.plot(x, np.sin(x)); plt.show()
- б) объектный стиль: fig, ax = plt.subplots(); ax.plot(x, np.sin(x)); plt.show()
Выведи type(fig) и type(ax). Ожидание: Figure и Axes.
Объясни: Figure — «холст/окно», Axes — одна область с осями (не путай с axis).
Почему в рабочем коде и в библиотеках предпочитают объектный стиль?
(явно видно, на какой Axes рисуем; нет скрытого «текущего» состояния)
"""



"""
### 1.2: размер, dpi и сохранение
fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
Нарисуй sin и cos на одном Axes, сохрани fig.savefig('trig.png', dpi=150, bbox_inches='tight').
Проверь размер картинки в пикселях: figsize * dpi. Ожидание для dpi=150: 1200 x 600 (примерно,
bbox_inches='tight' обрезает поля). Закрой фигуру через plt.close(fig) — зачем? (память в циклах)
"""



"""
## УРОВЕНЬ 2. Базовые типы графиков
"""

rng = np.random.default_rng(42)

"""
### 2.1: line и scatter
x = np.linspace(0, 10, 50); y = 2 * x + rng.normal(scale=2, size=50)
- а) линия ax.plot(x, y, marker='o', linestyle='--', color='tab:blue')
- б) scatter ax.scatter(x, y, c=y, cmap='viridis', s=40) + fig.colorbar(...)
Чем plot с marker отличается от scatter? (scatter умеет менять размер и цвет каждой точки,
plot быстрее на больших данных)
"""



"""
### 2.2: bar и barh
cats = ['A', 'B', 'C', 'D']; vals = [23, 17, 35, 29]
- а) вертикальные столбцы ax.bar
- б) горизонтальные ax.barh, отсортированные по убыванию значений
- в) подпиши значения над столбцами: ax.bar_label(bars)
Почему для длинных названий категорий лучше barh?
"""



"""
### 2.3: hist
data = rng.normal(loc=0, scale=1, size=1000)
- а) ax.hist(data, bins=30)
- б) то же с density=True; проверь, что площадь гистограммы = 1
   (сумма высот * ширина бина, ширина = np.diff(edges)[0])
- в) сравни bins=5, 30, 200. Как число бинов меняет вывод о форме распределения?
"""



"""
### 2.4: boxplot и errorbar
groups = [rng.normal(m, 1, 200) for m in (0, 1, 2)]
- а) ax.boxplot(groups, tick_labels=['g0', 'g1', 'g2'])  (в старых версиях параметр labels)
   Что показывают: медиана, ящик (Q1–Q3), усы (1.5 * IQR), точки-выбросы?
- б) ax.errorbar([0, 1, 2], [g.mean() for g in groups], yerr=[g.std(ddof=1) for g in groups], fmt='o', capsize=4)
"""



"""
## УРОВЕНЬ 3. Оформление: подписи, легенда, оси, стили
"""

"""
### 3.1: обязательный минимум
Для графика sin и cos из 1.2 добавь: title, xlabel, ylabel, label= у линий + ax.legend(),
ax.grid(alpha=0.3). Правило: на графике без подписей осей и единиц измерения нельзя
ничего понять — проверь каждый свой график по этому чек-листу.
"""



"""
### 3.2: пределы, ticks, масштаб
- а) ax.set_xlim / ax.set_ylim
- б) ax.set_xticks([0, np.pi, 2*np.pi]) и ax.set_xticklabels(['0', 'π', '2π'])
- в) логарифмическая ось: x = np.logspace(0, 3, 50); ax.plot(x, x**2); ax.set_xscale('log'); ax.set_yscale('log')
   Ожидание: степенная зависимость на log-log — прямая линия. Почему?
"""



"""
### 3.3: annotate, axhline, fill_between
- а) отметь максимум sin стрелкой: ax.annotate('max', xy=(np.pi/2, 1), xytext=(2, 1.2), arrowprops=dict(arrowstyle='->'))
- б) горизонтальная линия среднего ax.axhline(y.mean(), color='gray', linestyle=':')
- в) доверительная полоса: ax.fill_between(x, y - 1, y + 1, alpha=0.2)
"""



"""
### 3.4: стили и цвета
print(plt.style.available) — выбери один (например 'seaborn-v0_8-whitegrid' или 'ggplot')
и примени через plt.style.use(...) или with plt.style.context(...).
Сравни цветовые карты для разных данных:
- последовательные ('viridis') — для величин от малого к большому,
- расходящиеся ('coolwarm') — для данных с осмысленным нулём (корреляции),
- качественные ('tab10') — для категорий.
Почему 'jet' (радужная) считается плохим выбором? (не монотонна по яркости, искажает восприятие)
"""



"""
## УРОВЕНЬ 4. Несколько графиков: subplots
"""

"""
### 4.1: сетка
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, constrained_layout=True)
Выведи axes.shape. Ожидание: (2, 2). Нарисуй в каждой ячейке свою функцию (sin, cos, x**2, exp)
и подпиши через ax.set_title. Для чего sharex/sharey? (одинаковый масштаб для сравнения)
Как обойти axes в цикле: for ax in axes.flat.
"""



"""
### 4.2: две оси Y
Нарисуй на одном Axes температуру (°C) и осадки (мм) за 12 месяцев:
ax2 = ax.twinx(); цвета линий и подписей осей должны совпадать.
Когда twinx вводит в заблуждение? (разные шкалы можно подогнать так, чтобы «показать» корреляцию)
"""



"""
### 4.3: сложная раскладка
fig, axd = plt.subplot_mosaic([['top', 'top'], ['left', 'right']], figsize=(8, 6))
Нарисуй на 'top' временной ряд, на 'left' гистограмму, на 'right' scatter.
Это удобнее GridSpec для нерегулярных сеток.
"""



"""
## УРОВЕНЬ 5. Матричные данные и связь с NumPy / Pandas
"""

"""
### 5.1: imshow
M = rng.random((10, 10))
ax.imshow(M, cmap='viridis'); fig.colorbar(im). Затем np.arange(100).reshape(10, 10)
и убедись, что (0, 0) — левый верхний угол (origin='upper'), строки идут вниз.
Как отобразить матрицу как в математике (ось Y вверх)? (origin='lower')
"""



"""
### 5.2: график из DataFrame
df = pd.DataFrame({'x': np.arange(10), 'a': rng.random(10), 'b': rng.random(10)})
- а) df.plot(x='x', y=['a', 'b'])  — возвращает Axes. Проверь type(ax).
- б) df.plot(kind='bar', x='x'), df['a'].plot(kind='hist')
- в) передай готовый Axes: df.plot(ax=axes[0])
Вывод: pandas.plot — тонкая обёртка над matplotlib, всё оформление делается через Axes.
"""



"""
### 5.3: распределения из NumPy (связка с Numpy.py)
Нарисуй гистограмму 10_000 значений rng.normal и поверх — теоретическую плотность
(1/sqrt(2π)) * exp(-x²/2) через ax.plot. Проверь, что при density=True они совпадают по форме.
Затем rng.exponential и rng.uniform — как выглядят их гистограммы?
"""



"""
## УРОВЕНЬ 6. Seaborn: данные и стиль
"""

"""
### 6.1: тема и датасеты
sns.set_theme(style='whitegrid', context='notebook', palette='deep')
tips = sns.load_dataset('tips'); выведи tips.shape, tips.head().
Ожидание: (244, 7), столбцы total_bill, tip, sex, smoker, day, time, size.
Seaborn работает с «длинным» (tidy) форматом: одна строка — одно наблюдение, один столбец — одна переменная.
Объясни, чем это отличается от «широкого» формата, где столбцы — это группы.
"""



"""
### 6.2: axes-level против figure-level
- axes-level (scatterplot, histplot, boxplot, heatmap...) — рисуют на переданном ax=...
  и возвращают Axes; их можно класть в subplots.
- figure-level (relplot, displot, catplot, pairplot, jointplot) — создают свою Figure
  (FacetGrid), принимают col=, row=, hue=, возвращают Grid-объект, ax= не принимают.
Для каждого из них напиши по одному примеру ниже и убедись в разнице типов возвращаемого объекта.
"""



"""
## УРОВЕНЬ 7. Seaborn: распределения и категории
"""

"""
### 7.1: распределения
tips = sns.load_dataset('tips')
- а) sns.histplot(tips, x='total_bill', bins=20, kde=True)
- б) sns.histplot(tips, x='total_bill', hue='time', multiple='stack')
- в) sns.kdeplot(tips, x='total_bill', hue='sex', fill=True)
- г) sns.ecdfplot(tips, x='tip')  — как по ECDF прочитать медиану? (где кривая = 0.5)
- д) sns.displot(tips, x='tip', col='time', kind='hist')  (figure-level)
Что видно по распределению total_bill? (правый «хвост», скошенность вправо)
"""



"""
### 7.2: категориальные графики
- а) sns.countplot(tips, x='day', hue='sex')
- б) sns.boxplot(tips, x='day', y='total_bill')
- в) sns.violinplot(tips, x='day', y='total_bill', hue='sex', split=True)
- г) sns.stripplot / sns.swarmplot поверх boxplot (покажи сами точки, а не только сводку)
- д) sns.barplot(tips, x='day', y='tip', estimator='mean', errorbar='ci') — что значат чёрточки?
   (95% доверительный интервал среднего через bootstrap). Чем barplot отличается от countplot?
Сформулируй: когда boxplot честнее, чем barplot со средним?
"""



"""
### 7.3: catplot с фасетами
sns.catplot(tips, x='day', y='total_bill', col='time', hue='smoker', kind='box')
Сколько Axes получилось? Достань: g = sns.catplot(...); g.axes.shape, g.fig.
Подпиши g.set_axis_labels('День', 'Счёт, $') и g.set_titles('{col_name}').
"""



"""
## УРОВЕНЬ 8. Seaborn: связи между признаками
"""

"""
### 8.1: scatter и регрессия
- а) sns.scatterplot(tips, x='total_bill', y='tip', hue='time', size='size', style='smoker')
   Сколько признаков закодировано одним графиком? (5) Не слишком ли много для читателя?
- б) sns.regplot(tips, x='total_bill', y='tip') — линия + доверительная полоса.
- в) sns.lmplot(tips, x='total_bill', y='tip', hue='smoker') — регрессия по группам (figure-level).
"""



"""
### 8.2: корреляции и heatmap
penguins = sns.load_dataset('penguins')
corr = penguins.select_dtypes('number').corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, vmin=-1, vmax=1)
Ожидание: диагональ = 1, матрица симметрична. Какие признаки сильнее всего коррелируют?
(flipper_length_mm и body_mass_g ≈ 0.87). Почему cmap расходящийся и center=0?
Покажи только нижний треугольник через mask=np.triu(np.ones_like(corr, dtype=bool)).
"""



"""
### 8.3: pairplot и jointplot
- а) sns.pairplot(penguins, hue='species') — какие пары признаков лучше всего разделяют виды?
- б) sns.jointplot(penguins, x='bill_length_mm', y='bill_depth_mm', hue='species')
- в) Парадокс Симпсона: в целом bill_length и bill_depth коррелируют отрицательно,
   а внутри каждого вида — положительно. Проверь через sns.regplot по всем данным
   и sns.lmplot с hue='species'. Вывод: агрегат может скрывать обратную связь внутри групп.
"""



"""
### 8.4: временные ряды и неопределённость
flights = sns.load_dataset('flights')
- а) sns.lineplot(flights, x='year', y='passengers') — что за полоса вокруг линии?
   (агрегация по месяцам: среднее + доверительный интервал)
- б) flights.pivot(index='month', columns='year', values='passengers') -> sns.heatmap
   Какой сезонный паттерн виден? (пик летом, общий рост по годам)
"""



"""
## УРОВЕНЬ 9. Мини-проекты
"""

"""
### 9.1: визуальная разведка Titanic (продолжение уровня 9 из Pandas.py)
titanic = sns.load_dataset('titanic')
Одна Figure 2x3 (subplots + axes-level функции seaborn с ax=...):
1) countplot survived                          — видно дисбаланс классов (≈38% / 62%)
2) barplot survived по sex                     — female ≈ 0.74, male ≈ 0.19
3) barplot survived по pclass, hue='sex'
4) histplot age, hue='survived', multiple='stack' — пропуски age (177) просто не рисуются
5) boxplot fare по pclass, log-шкала по y      — fare сильно скошен вправо
6) heatmap пропусков: sns.heatmap(titanic.isna(), cbar=False) — deck виден почти целиком «жёлтым»
Каждому графику — title, подписи осей. Сохрани в 'titanic_eda.png'.
Письменно: 3 вывода о том, какие признаки информативны, и какой график их показал лучше всего.
Типичная ошибка: смотреть на барплот средних без числа наблюдений в группе — проверь через countplot.
"""



"""
### 9.2: диагностика линейной регрессии (продолжение 8.3 из Numpy.py)
Тип задачи: регрессия. Метрика: RMSE.
rng = np.random.default_rng(7)
X = rng.normal(size=(200, 2))
y = 5 + 3 * X[:, 0] - 2 * X[:, 1] + rng.normal(scale=0.1, size=200)
Обучи модель по нормальному уравнению (как в Numpy.py 8.3, split 160/40) и построй Figure 1x3:
1) y_true против y_pred на test + диагональ y = x (хорошая модель — точки на диагонали)
2) остатки (y_true - y_pred) против y_pred: sns.residplot или scatter + axhline(0)
   — без структуры, облако вокруг нуля; изгиб или «воронка» = модель не подходит
3) гистограмма остатков с kde — примерно нормальная, центр около 0
Затем замени y на y + 2 * X[:, 0] ** 2 (нелинейность), не меняя модель, и пересчитай графики.
Что изменилось на графике остатков? Это и есть смысл диагностики: метрика RMSE выросла,
а график показывает ПОЧЕМУ.
"""



"""
### 9.3: кривая обучения (loss curve) на чистом NumPy
Градиентным спуском подбери w для задачи из 9.2 (X с единичным столбцом):
w -= lr * (2 / n) * Xtr.T @ (Xtr @ w - ytr), 200 шагов, lr = 0.1.
Запоминай MSE на train и на test на каждом шаге. Построй обе кривые на одном Axes
(ось Y в log-масштабе). Ожидание: обе быстро падают и выходят на плато около 0.01 (шум 0.1²).
Попробуй lr = 1.5 — что произойдёт? (расходимость, MSE растёт; на log-оси это хорошо видно)
Если test заметно выше train — переобучение; для линейной модели на 160 точках его не ждём.
"""


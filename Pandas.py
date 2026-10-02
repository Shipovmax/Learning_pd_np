import pandas as pd

"""
## УРОВЕНЬ 1. Series
"""

"""
### 1.1
sr = pd.Series([5, 6, 2, 9, 12], index=['a', 'b', 'c', 'd', 'e'])
Выведи: type(sr.values), sr.index, sr['b'], sr['b':'d'], sr.iloc[1:3].
Ожидание: numpy.ndarray; Index(['a','b','c','d','e']); 6;
  sr['b':'d'] -> три элемента b, c, d (правая граница ВКЛЮЧАЕТСЯ при явных метках);
  sr.iloc[1:3] -> два элемента b, c (при позиционных индексах граница НЕ включается).
"""



"""
### 1.2: Series из словаря
pop = pd.Series({'California': 38332521, 'Texas': 26448193, 'New York': 19651127,
                 'Florida': 19552860, 'Illinois': 12882135})
а) 'Texas' in pop                         -> True
б) pop[pop > 20_000_000]                  -> California, Texas
в) pop.sort_values()                      -> порядок: Illinois, Florida, New York, Texas, California
г) pop.sort_values(ascending=False).head(2).index.tolist() -> ['California', 'Texas']
"""



"""
### 1.3: ловушка целочисленного индекса
s = pd.Series(['a', 'b', 'c'], index=[1, 3, 5])
Выведи: s[1], s.loc[1], s.iloc[1], s.loc[1:3], s.iloc[1:3].
Ожидание: 'a', 'a', 'b', ['a','b'] (метки 1 и 3, граница включается), ['b','c'] (позиции 1 и 2).
Поведение s[1:3] (без loc/iloc) зависит от версии pandas и неочевидно — не используй его.
Вывод: в рабочем коде всегда явно пиши .loc или .iloc.
"""



"""
## УРОВЕНЬ 2. Создание DataFrame
"""

"""
### 2.1: DataFrame из двух Series
pop — Series из 1.2, area = pd.Series({'California': 423967, 'Texas': 695662,
  'New York': 141297, 'Florida': 170312, 'Illinois': 149995})
states = pd.DataFrame({'population': pop, 'area': area})
Выведи shape, columns, index. Ожидание: (5, 2).
Добавь столбец density = population / area.
Ожидание: California 90.41, Texas 38.02, New York 139.08, Florida 114.81, Illinois 85.88.
Далее в файле states означает этот DataFrame (с density).
"""



"""
### 2.2: из словаря списков
data = {'county': ['Cochice', 'Pima', 'Santa Cruz', 'Maricopa', 'Yuma'],
        'year': [2012, 2012, 2013, 2014, 2014],
        'reports': [4, 24, 31, 2, 3]}
Создай DataFrame с порядком столбцов ['reports', 'county'] и индексом ['a', 'b', 'c', 'd', 'e'].
Ожидание: shape (5, 2), столбец year отсутствует. Как называется параметр для выбора столбцов?
"""



"""
### 2.3: пропуски при создании
rows = [{'a': 1, 'c': 'Alpha'}, {'a': 0, 'b': 3, 'c': 'Beta'}]
Создай DataFrame из rows и выведи dtypes.
Ожидание: столбцы a, c, b; b = [NaN, 3.0], dtype float64.
Объясни, почему b стал float64, хотя 3 — целое.
"""



"""
### 2.4: pandas против NumPy: что такое df[1]
np1 = np.array([[1, 2, 3], [4, 5, 6]])
а) np1[1]               -> [4 5 6]  (строка!)
б) df = pd.DataFrame(np1); df[1] -> столбец: 0 -> 2, 1 -> 5
в) df2 = pd.DataFrame(np1, index=['la', 'lb'], columns=['cl1', 'cl2', 'cl3']);
   df2['cl2'] -> la 2, lb 5;  df2['cl2']['la'] -> 2
Сформулируй правило: квадратные скобки у DataFrame по умолчанию выбирают столбцы.
Как получить строку 1 из df? (df.iloc[1])
"""



"""
## УРОВЕНЬ 3. Индексация DataFrame
"""

"""
### 3.1: столбцы
а) states['area'] — тип? (Series)    б) states.area — то же, но когда это ломается?
   (имя совпадает с методом или содержит пробел)
в) states[['population', 'area']] — shape (5, 2) и тип DataFrame
"""



"""
### 3.2: loc и iloc
а) states.loc['Texas', 'area']                 -> 695662
б) states.loc['Texas':'New York']              -> 2 строки (Texas, New York), граница включается
в) states.iloc[1:3]                            -> те же две строки
г) states.loc[:, 'population':'area']          -> два столбца
д) states.iloc[0, 2]                           -> density Калифорнии ≈ 90.41
"""



"""
### 3.3: маски
а) states[states['density'] > 100]                    -> New York, Florida
б) states.loc[states['density'] > 100, ['population', 'density']]  -> shape (2, 2)
в) states[(states['population'] > 20_000_000) & (states['density'] < 100)]
   Ожидание: California, Texas.  Почему здесь & и скобки, а не and?
"""



"""
### 3.4: присваивание и цепные индексы
а) states.loc['Illinois', 'density'] = 90 — правильное присваивание.
б) states[states['density'] > 100]['area'] = 0 — цепное присваивание.
   Выполни и проверь states: area не изменилась (или pandas выдал предупреждение).
   Объясни: первая скобка возвращает копию/временный объект, запись идёт в него.
в) Как правильно обнулить area у строк с density > 100? (через .loc с маской)
"""



"""
## УРОВЕНЬ 4. Универсальные функции и выравнивание по индексу
"""

"""
### 4.1: ufunc сохраняют индекс
df = pd.DataFrame(np.arange(12).reshape(3, 4), columns=list('ABCD'))
np.sqrt(df) и df * 2 — убедись, что index и columns те же, исходный df не изменился.
"""



"""
### 4.2: выравнивание Series
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([10, 20, 30], index=['b', 'c', 'd'])
а) s1 + s2                      -> a NaN, b 12, c 23, d NaN
б) s1.add(s2, fill_value=0)     -> a 1, b 12, c 23, d 30
Почему в NumPy складывались бы позиции, а в pandas — метки?
"""



"""
### 4.3: выравнивание DataFrame
dfa = pd.DataFrame({'A': [1, 2], 'B': [3, 4]}, index=[0, 1])
dfb = pd.DataFrame({'B': [10, 20, 30], 'C': [1, 1, 1]}, index=[1, 2, 3])
Предскажи, сколько значений в dfa + dfb НЕ NaN, потом проверь через .notna().sum().sum().
Ожидание: 1 (только строка 1, столбец B: 4 + 10 = 14). Результат содержит объединение индексов
и объединение столбцов.
"""



"""
## УРОВЕНЬ 5. Пропуски
"""

"""
df = pd.DataFrame({'x': [1, np.nan, 3, np.nan],
                   'y': [np.nan, np.nan, 6, 7],
                   'z': [1, 2, 3, 4]})
"""

"""
### 5.1
а) df.isna().sum()      -> x 2, y 2, z 0
б) df.isna().mean()     -> x 0.5, y 0.5, z 0.0  (доля пропусков)
в) почему mean() от булевой маски даёт долю?
"""



"""
### 5.2: dropna
а) df.dropna()                  -> одна строка (индекс 2)
б) df.dropna(how='all')         -> все 4 строки
в) df.dropna(axis=1)            -> только столбец z
г) df.dropna(thresh=2)          -> строки 0, 2, 3 (минимум 2 непустых значения)
"""



"""
### 5.3: fillna
а) df.fillna(0)
б) df.fillna(df.mean())         -> x: [1, 2, 3, 2];  y: [6.5, 6.5, 6, 7]
в) df['x'].ffill()              -> [1, 1, 3, 3]
Методологическая заметка: б) на всём датасете перед split — утечка (среднее учитывает test).
В уровне 9 это делается правильно.
"""



"""
### 5.4: NaN и целые числа
pd.Series([1, 2, None]).dtype            -> float64
pd.Series([1, 2, None], dtype='Int64')   -> nullable-тип, пропуск показывается как <NA>
Объясни, почему обычный int-столбец не может хранить NaN.
"""



"""
## УРОВЕНЬ 6. Агрегирование
"""

"""
df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50]})
"""

"""
### 6.1
а) df.mean()            -> A 3.0, B 30.0           (по умолчанию axis=0)
б) df.mean(axis=1)      -> [5.5, 11.0, 16.5, 22.0, 27.5]
в) df.sum(), df.median(), df.min(), df.max()
"""



"""
### 6.2: ddof — частая ошибка
df['A'].std()           -> 1.5811 (pandas: ddof=1, выборочное)
df['A'].values.std()    -> 1.4142 (NumPy: ddof=0, генеральное)
df['A'].values.std(ddof=1) совпадает с pandas.
Объясни разницу формул (деление на n против n-1). Какой вариант использует StandardScaler в sklearn?
(ddof=0.) Это важно, когда сверяешь свою стандартизацию с sklearn.
"""



"""
### 6.3: describe, quantile, agg
а) df.describe()                          — 8 строк статистик
б) df.quantile([0.25, 0.5, 0.75])         -> A: 2, 3, 4;  B: 20, 30, 40
в) df.agg(['min', 'max', 'mean'])         -> shape (3, 2)
г) df.agg({'A': 'sum', 'B': 'max'})       -> A 15, B 50
"""



"""
## УРОВЕНЬ 7. Объединение таблиц
"""

"""
### 7.1: concat
df1 = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
а) pd.concat([df1, df2]).index              -> [0, 1, 0, 1] (индекс дублируется)
б) pd.concat([df1, df2], ignore_index=True) -> индекс 0..3
в) pd.concat([df1, df2], axis=1).shape      -> (2, 4)
Метод df.append из лекции в современных версиях не существует.
"""



"""
### 7.2: данные для merge
"""
employees = pd.DataFrame(
    {
        "employee": ["Bob", "Jake", "Lisa", "Sue"],
        "group": ["Accounting", "Engineering", "Engineering", "HR"],
    }
)
hire = pd.DataFrame(
    {"employee": ["Lisa", "Bob", "Jake", "Sue"], "hire_date": [2004, 2008, 2012, 2014]}
)
supervisors = pd.DataFrame(
    {
        "group": ["Accounting", "Engineering", "HR"],
        "supervisor": ["Carly", "Guido", "Steve"],
    }
)
skills = pd.DataFrame(
    {
        "group": ["Accounting", "Accounting", "Engineering", "Engineering", "HR", "HR"],
        "skills": [
            "math",
            "spreadsheets",
            "coding",
            "linux",
            "spreadsheets",
            "organization",
        ],
    }
)

"""
а) один-к-одному: employees + hire по employee.
   Ожидание: 4 строки; Bob 2008, Jake 2012, Lisa 2004, Sue 2014.
б) многие-к-одному: результат (а) + supervisors по group.
   Ожидание: Bob -> Carly, Jake -> Guido, Lisa -> Guido, Sue -> Steve.
в) многие-ко-многим: employees + skills по group.
   Ожидание: shape (8, 3), у каждого сотрудника по 2 строки.
   Объясни, почему строк стало больше, чем в employees.
"""



"""
### 7.3: разные имена ключей
"""
salary = pd.DataFrame(
    {"name": ["Bob", "Jake", "Lisa", "Sue"], "salary": [70000, 80000, 120000, 90000]}
)
"""
Соедини employees и salary по employee == name (left_on / right_on),
затем удали лишний столбец name через drop(columns='name') БЕЗ inplace.
Ожидание: shape (4, 3): employee, group, salary.
"""



"""
### 7.4: тип соединения how
"""
left = pd.DataFrame({"k": ["a", "b", "c"], "v1": [1, 2, 3]})
right = pd.DataFrame({"k": ["b", "c", "d"], "v2": [20, 30, 40]})
"""
Выполни merge с how='inner', 'left', 'right', 'outer' и выведи число строк.
Ожидание: 2, 3, 3, 4. Для 'left' в строке a значение v2 = NaN.
Какой how по умолчанию? (inner)  Когда inner молча теряет данные?
"""



"""
## УРОВЕНЬ 8. GroupBy: split -> apply -> combine
"""

sales = pd.DataFrame({"key": ["A", "B", "C", "A", "B", "C"], "data": range(1, 7)})

"""
### 8.1
а) sales.groupby('key') — какой тип объекта и почему вычислений ещё нет?
б) sales.groupby('key').sum()    -> A 5, B 7, C 9
в) sales.groupby('key')['data'].mean()   -> A 2.5, B 3.5, C 4.5
г) sales.groupby('key').size()   -> по 2 в каждой группе
"""



"""
### 8.2: agg
sales.groupby('key')['data'].agg(['min', 'max', 'mean'])
Ожидание: A: 1, 4, 2.5;  B: 2, 5, 3.5;  C: 3, 6, 4.5
"""



"""
### 8.3: filter
Оставь только группы, у которых сумма data > 6.
Ожидание: группы B и C, shape (4, 2), исходные индексы сохранены (1, 2, 4, 5).
"""



"""
### 8.4: transform
Вычти из data среднее по группе (центрирование внутри группы).
Результат должен иметь ту же длину, что и sales, и тот же индекс.
Ожидание: [-1.5, -1.5, -1.5, 1.5, 1.5, 1.5]
Чем transform отличается от agg по форме результата?
"""



"""
### 8.5: несколько ключей и pivot
"""
sales2 = pd.DataFrame(
    {
        "city": ["M", "M", "S", "S", "M", "S"],
        "product": ["x", "y", "x", "y", "x", "x"],
        "amount": [10, 20, 30, 40, 50, 60],
    }
)
"""
а) sales2.groupby(['city', 'product'])['amount'].sum()  -> MultiIndex: M-x 60, M-y 20, S-x 90, S-y 40
б) .unstack()                                           -> таблица city x product
в) pd.pivot_table(sales2, values='amount', index='city', columns='product', aggfunc='sum')
   Ожидание в) и б): M: x=60, y=20;  S: x=90, y=40.
"""



"""
### 8.6: реальные данные, планеты
import seaborn as sns
planets = sns.load_dataset('planets')
а) planets.shape                                  -> (1035, 6)
б) число открытий каждым методом (planets.groupby('method').size());
   Ожидание: Radial Velocity 553, Transit 397.
в) медиана orbital_period по методам;  Radial Velocity 360.2, Transit ≈ 5.71.
г) сколько планет открыто в каждый год; год 2011 -> 185. Посмотри на какие годы пришёлся пик.
д) добавь столбец orbital_period_normalized = orbital_period / минимум orbital_period
   в рамках года — через groupby(...).transform('min'), а не через apply с изменением x
   (как в лекции: функция, мутирующая входную группу, — плохая практика).
е) что покажет count() для каждого столбца и чем он отличается от size()?
   (count не считает NaN, size — все строки)
"""



"""
## УРОВЕНЬ 9. Мини-проект: подготовка Titanic без утечки данных
"""

"""
Тип задачи: бинарная классификация, цель survived.
Метрика (назови до работы с моделью и обоснуй): классы несбалансированы (≈38% / 62%),
поэтому одной accuracy мало — смотри ещё на F1 или ROC-AUC.
titanic = sns.load_dataset('titanic')
"""

"""
### 9.1: разведка
а) shape -> (891, 15)
б) число пропусков по столбцам: age 177, embarked 2, deck 688 (77% — столбец непригоден)
в) titanic['survived'].mean()  -> ≈ 0.384
г) доля выживших по sex:    female ≈ 0.74,  male ≈ 0.19
д) доля выживших по pclass: 1 ≈ 0.63,  2 ≈ 0.47,  3 ≈ 0.24
е) pivot_table по (sex, pclass) со средним survived
Запиши 2-3 вывода: какие признаки, судя по данным, самые информативные.
"""



"""
### 9.2: split и заполнение пропусков
1) Признаки: pclass, sex, age, sibsp, parch, fare, embarked. deck не берём (обоснуй).
2) ПЕРВЫМ шагом разбей на train/test: train_test_split(test_size=0.2,
   stratify=y, random_state=42). Почему stratify обязателен при дисбалансе классов?
   Ожидание: train 712 строк, test 179; доля survived в train и test ≈ 0.384 в обоих.
3) Медиану age считай ТОЛЬКО по train и заполни ею пропуски и в train, и в test.
4) Моду embarked считай ТОЛЬКО по train и заполни ею пропуски в обоих.
5) sex переведи в 0/1; embarked закодируй через pd.get_dummies на train, а для test сделай
   reindex(columns=train.columns, fill_value=0), чтобы набор столбцов совпал.
Проверки: нет NaN ни в train, ни в test; list(train.columns) == list(test.columns).
Письменно ответь: что именно утекло бы в test, если бы медиана age считалась до split
и по какой причине это завышает оценку качества модели.
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

books_df = pd.read_csv('books_data.csv')
books_df['Price_Cleaned'] = (
    books_df['Price']
    .str.replace('Â', '', regex=False)
    .str.replace('£', '', regex=False)
    .astype(float)
)
rating_map = {
    'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
}
books_df['Rating_Cleaned'] = books_df['Rating'].map(rating_map)

print("предобработка данных завершена")
print(books_df.head())

sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
plt.subplots_adjust(hspace=0.4, wspace=0.3)
# распределение цен
sns.histplot(books_df['Price_Cleaned'], bins=20, ax=axes[0, 0], color='lightcoral')
axes[0, 0].set_title('распределение цен на книги')
axes[0, 0].set_xlabel('цена (£)')
axes[0, 0].set_ylabel('частота')
# распределение рейтингов
sns.countplot(x='Rating_Cleaned', data=books_df, ax=axes[0, 1], color='lightcoral', order=sorted(books_df['Rating_Cleaned'].unique()))
axes[0, 1].set_title('распределение количества звезд')
axes[0, 1].set_xlabel('рейтинг (звезды)')
axes[0, 1].set_ylabel('количество книг')
# топ 10 по рейтингу
rating_counts = books_df['Rating_Cleaned'].value_counts().sort_index(ascending=False)
sns.barplot(x=rating_counts.index, y=rating_counts.values, ax=axes[0, 2], color='lightcoral')
axes[0, 2].set_title('обзор рейтингов (самые частые)')
axes[0, 2].set_xlabel('рейтинг (звезды)')
axes[0, 2].set_ylabel('количество')
# соотношение цены и рейтинга
sns.scatterplot(x='Price_Cleaned', y='Rating_Cleaned', data=books_df, ax=axes[1, 0], color='lightcoral', alpha=0.6)
axes[1, 0].set_title('соотношение цены и рейтинга')
axes[1, 0].set_xlabel('цена (£)')
axes[1, 0].set_ylabel('рейтинг (звезды)')
# средняя цена и рейтинг по страницам
agg_data = books_df.groupby('Page_Scraped')[['Price_Cleaned', 'Rating_Cleaned']].mean().reset_index()
agg_melted = pd.melt(agg_data, id_vars='Page_Scraped', var_name='Metric', value_name='Value')
sns.barplot(x='Page_Scraped', y='Value', hue='Metric', data=agg_melted, ax=axes[1, 1], palette={'Price_Cleaned': 'lightcoral', 'Rating_Cleaned': 'olivedrab'})
axes[1, 1].set_title('средняя цена и рейтинг по страницам')
axes[1, 1].set_xlabel('номер страницы')
axes[1, 1].set_ylabel('среднее значение')
axes[1, 1].legend(title='показатель')

corr_matrix = books_df[['Price_Cleaned', 'Rating_Cleaned']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='Reds', fmt=".2f", ax=axes[1, 2], cbar_kws={'label': 'Корреляция'})
axes[1, 2].set_title('корреляционная матрица (цена и рейтинг)')

plt.show()

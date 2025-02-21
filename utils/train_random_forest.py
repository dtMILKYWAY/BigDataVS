import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from flask import Flask, session, render_template, redirect, Blueprint
# 假设querys函数已在其他地方定义，这里直接使用
from utils import query  # 请将your_module替换为实际的模块名
from utils.getPublicData import getAlladlist


def preprocess_data(df):
    """
    数据预处理函数，包括文本清洗、特征提取等
    """
    def clean_text(text):
        if text is None or pd.isnull(text):
            return ""
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        return text.lower()

    df['Name'] = df['Name'].apply(clean_text)
    df['Author'] = df['Author'].apply(clean_text)
    df['Texture'] = df['Texture'].apply(lambda x: "" if pd.isnull(x) else x)
    df['combined_features'] = df['Name'] + " " + df['Author'] + " " + df['Texture']
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(df['combined_features'])
    return features, df['Type'].values


def train_random_forest(X, y):
    """
    训练随机森林分类器
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"随机森林模型准确率: {accuracy_score(y_test, y_pred)}")
    return clf


def getDataArticle(flag):
    if flag:
        tableListOld = getAlladlist()
        df = pd.DataFrame(tableListOld, columns=['ID', 'Name', 'ForeignName', 'time', 'Author', 'Texture', 'Type', 'institution', 'Period', 'description'])
        # 检查并处理Type列中的None值
        valid_indices = df['Type'].notnull()
        valid_df = df[valid_indices]
        features, y = preprocess_data(valid_df)
        clf = train_random_forest(features, y)
        predictions = clf.predict(features)
        tableList = []
        for index, item in enumerate(tableListOld):
            if valid_indices[index]:
                item = list(item)
                item.append(predictions[valid_indices[:index].sum()])
                tableList.append(item)
    else:
        tableList = getAlladlist()
    return tableList

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data():
    # 讀取 CSV 檔案並將日期欄設為索引
    df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")
    
    # 移除數據中的極端值 (去掉最上層 2.5% 和最下層 2.5%)
    lower_bound = df["value"].quantile(0.025)
    upper_bound = df["value"].quantile(0.975)
    df = df[(df["value"] >= lower_bound) & (df["value"] <= upper_bound)]
    
    return df

def draw_line_plot():
    # 載入清理後的數據
    df = load_and_clean_data()
    
    # 建立圖表
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["value"], color='red', linewidth=1)
    
    # 設定標題與軸標籤
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # 儲存圖表並回傳
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # 載入清理後的數據
    df = load_and_clean_data()
    
    # 新增年份與月份欄位
    df["year"] = df.index.year
    df["month"] = df.index.month
    
    # 計算每個月份的平均值，並將結果轉換為表格格式
    df_bar = df.groupby(["year", "month"])["value"].mean().unstack()
    
    # 繪製長條圖
    fig = df_bar.plot(kind='bar', figsize=(12, 6)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    
    # 設定圖例 (月份)
    plt.legend(title="Months", labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    plt.title("Average Daily Page Views per Month")
    
    # 儲存圖表並回傳
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # 載入清理後的數據
    df = load_and_clean_data()
    
    # 新增年份與月份名稱欄位
    df["year"] = df.index.year
    df["month"] = df.index.strftime('%b')
    
    # 設定月份的顯示順序
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # 建立圖表與子圖
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 年度趨勢箱型圖
    sns.boxplot(x="year", y="value", data=df, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # 月份趨勢箱型圖 (季節性)
    sns.boxplot(x="month", y="value", data=df, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    
    # 儲存圖表並回傳
    fig.savefig('box_plot.png')
    return fig

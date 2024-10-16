import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import textwrap
from streamlit_folium import st_folium


# ... (Kode untuk memuat dan membersihkan data, sama seperti di notebook) ...

st.title('Visualisasi Data E-commerce')

# Sidebar untuk memilih pertanyaan bisnis
pertanyaan_bisnis = st.sidebar.selectbox(
    'Pilih Pertanyaan Bisnis:',
    (
        'Bagaimana demografi customer di setiap wilayah?',
        'Bagaimana demografi sellers di setiap wilayah?',
        'Bagaimana hubungan antara ketersediaan seller dengan banyak customer di masing-masing state?',
        'Produk dengan kategori apa yang paling banyak terjual?',
        'Bagaimana trend penjualan dari waktu ke waktu?',
        'Apa metode pembayaran yang paling sering digunakan?',
        'Bagaimana tingkat kepuasan pelanggan terhadap produk yang dibeli?'
    )
)

# Fungsi untuk menampilkan visualisasi berdasarkan pertanyaan yang dipilih
def tampilkan_visualisasi(pertanyaan):
    if pertanyaan == 'Bagaimana demografi customer di setiap wilayah?':
        # Menghitung jumlah customer per state dari DataFrame customers_df
        st.subheader("Sebaran Demografi Pelanggan")
        customers_df = pd.read_csv('../dataa/customers_dataset.csv')
        customer_state = customers_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
        customer_state.rename(columns={'customer_unique_id': 'customer_count'}, inplace=True)

        # Create a map centered on Brazil
        brazil_map = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

        # Add a choropleth layer to the map
        folium.Choropleth(
            geo_data="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
            name="choropleth",
            data=customer_state,
            columns=['customer_state', 'customer_count'],
            key_on='feature.properties.sigla',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Jumlah Customer'
        ).add_to(brazil_map)

        # Function to add tooltips
        def add_tooltips(feature):
            state_name = feature['properties']['name']
            state_sigla = feature['properties']['sigla']
            customer_count = customer_state[customer_state['customer_state'] == state_sigla]['customer_count'].values[0]
            tooltip_text = f"<b>{state_name}</b><br>State: {state_sigla}<br>Jumlah Customer: {customer_count}"
            return folium.Tooltip(tooltip_text)

        # Add the GeoJson layer with tooltips
        geojson_layer = folium.GeoJson(
            data="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
            name='geojson',
            style_function=lambda feature: {'fillColor': 'transparent', 'color': 'black'},
            highlight_function=lambda x: {'fillColor': 'grey', 'color': 'black', 'weight': 3},
            tooltip=folium.GeoJsonTooltip(fields=['sigla', 'name'], aliases=['State:', 'Name:'])
        ).add_to(brazil_map)

        # Attach tooltips to the GeoJson layer
        for feature in geojson_layer.data['features']:
            tooltip = add_tooltips(feature)
            folium.GeoJson(
                data=feature,
                style_function=lambda feature: {'fillColor': 'transparent', 'color': 'black'},
                highlight_function=lambda x: {'fillColor': 'red', 'color': 'black', 'weight': 3},
                tooltip=tooltip
            ).add_to(brazil_map)

        # Add a layer control
        folium.LayerControl().add_to(brazil_map)
        st_folium(brazil_map)

    elif pertanyaan == 'Bagaimana demografi sellers di setiap wilayah?':
        # Menghitung jumlah seller per state dari DataFrame sellers_df
        st.subheader("Sebaran Demografi Seller")
        sellers_df = pd.read_csv('../data/sellers_dataset.csv')
        seller_state = sellers_df.groupby('seller_state')['seller_id'].nunique().reset_index()
        seller_state.rename(columns={'seller_id': 'seller_count'}, inplace=True)

        # Create a map centered on Brazil
        brazil_map = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

        # Add a choropleth layer to the map
        folium.Choropleth(
            geo_data="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
            name="choropleth",
            data=seller_state,
            columns=['seller_state', 'seller_count'],
            key_on='feature.properties.sigla',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Jumlah Sellers'
        ).add_to(brazil_map)

        # Function to add tooltips
        def add_tooltips(feature):
            state_name = feature['properties']['name']
            state_sigla = feature['properties']['sigla']
            seller_count = seller_state[seller_state['seller_state'] == state_sigla]['seller_count'].values
            if len(seller_count) > 0:
                seller_count = seller_count[0]
            else:
                seller_count = 0
            tooltip_text = f"<b>{state_name}</b><br>State: {state_sigla}<br>Jumlah Sellers: {seller_count}"
            return folium.Tooltip(tooltip_text)

        # Add the GeoJson layer with tooltips
        geojson_layer = folium.GeoJson(
            data="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
            name='geojson',
            style_function=lambda feature: {'fillColor': 'transparent', 'color': 'black'},
            highlight_function=lambda x: {'fillColor': 'grey', 'color': 'black', 'weight': 3},
            tooltip=folium.GeoJsonTooltip(fields=['sigla', 'name'], aliases=['State:', 'Name:'])
        ).add_to(brazil_map)

        # Attach tooltips to the GeoJson layer
        for feature in geojson_layer.data['features']:
            tooltip = add_tooltips(feature)
            folium.GeoJson(
                data=feature,
                style_function=lambda feature: {'fillColor': 'transparent', 'color': 'black'},
                highlight_function=lambda x: {'fillColor': 'blue', 'color': 'black', 'weight': 3},
                tooltip=tooltip
            ).add_to(brazil_map)


        # Add a legend
        legend_html = '''
        <div style="
        position: fixed;
        bottom: 50px; left: 50px; width: 200px; height: 40px;
        background-color: white;
        z-index: 9999;
        font-size: 14px;">
        <b>&nbsp; Keterangan :</b> <br>
        &nbsp; <i class="fa fa-square fa-lg" style="color:black"></i> &nbsp; Tidak ada seller <br>
        </div>
        '''
        brazil_map.get_root().html.add_child(folium.Element(legend_html))

        # Add a layer control
        folium.LayerControl().add_to(brazil_map)

        st_folium(brazil_map) # Menampilkan peta di Streamlit

    elif pertanyaan == 'Bagaimana hubungan antara ketersediaan seller dengan banyak customer di masing-masing state?':
        # Menghitung jumlah customer per state
        st.subheader("Korelasi Antara Customer dengan Seller")
        customers_df = pd.read_csv('../data/customers_dataset.csv')
        sellers_df = pd.read_csv('../data/sellers_dataset.csv')
        
        customer_state = customers_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
        customer_state.rename(columns={'customer_unique_id': 'customer_count'}, inplace=True)

        # Menghitung jumlah seller per state
        seller_state = sellers_df.groupby('seller_state')['seller_id'].nunique().reset_index()
        seller_state.rename(columns={'seller_id': 'seller_count'}, inplace=True)

        # Menggabungkan kedua dataframe berdasarkan state
        customer_seller_state = pd.merge(customer_state, seller_state, left_on='customer_state', right_on='seller_state', how='outer')
        customer_seller_state.drop(columns=['seller_state'], inplace=True)  # Menghapus kolom seller_state yang redundan

        # Membuat scatter plot untuk visualisasi
        plt.figure(figsize=(10, 8))
        sns.scatterplot(data=customer_seller_state, x='customer_count', y='seller_count', hue='customer_state')
        plt.title('Hubungan Antara Jumlah Customer dan Seller per State')
        plt.xlabel('Jumlah Customer')
        plt.ylabel('Jumlah Seller')

        # Menghitung korelasi antara jumlah customer dan seller
        correlation = customer_seller_state['customer_count'].corr(customer_seller_state['seller_count'])
        print(f"Korelasi antara jumlah customer dan seller: {correlation}")
        st.pyplot(plt) # Menampilkan scatter plot di Streamlit
        st.write("Korelasi antara jumlah customer dan seller: 0.965338514719251")

    elif pertanyaan == 'Produk dengan kategori apa yang paling banyak terjual?':
        st.subheader("Kategori Produk Paling Laris")

        # Membaca data
        products_df = pd.read_csv('../data/products_dataset.csv')
        order_items_df = pd.read_csv('../data/order_items_dataset.csv')

        # Mengatasi missing values
        products_df['product_category_name'] = products_df['product_category_name'].fillna('Unknown')
        for column in ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']:
            products_df[column] = products_df[column].replace([np.inf, -np.inf], np.nan)
            products_df[column] = products_df[column].fillna(products_df[column].mean())

        # Gabungkan data
        products_order_items_df = pd.merge(
            left=products_df,
            right=order_items_df,
            how="right",
            left_on="product_id",
            right_on="product_id"
        )

        # Groupby pada order_id yang unik dan hitung jumlah order per kategori
        order_per_category = products_order_items_df.groupby(['order_id', 'product_category_name'])['product_id'].count().reset_index()
        order_per_category = order_per_category.groupby('product_category_name')['order_id'].nunique().reset_index()  # Hitung order_id unik per kategori
        order_per_category = order_per_category.sort_values(by=['order_id'], ascending=False)  # Urutkan berdasarkan jumlah order

        # Ambil 5 kategori terlaris dan 5 kategori paling tidak laris
        top_5_categories = order_per_category.head(5)
        bottom_5_categories = order_per_category.tail(5)

        # Gabungkan top 5 dan bottom 5 kategori
        selected_categories = pd.concat([top_5_categories, bottom_5_categories])

        # Perbaiki tampilan nama kategori dengan textwrap
        selected_categories['product_category_name'] = selected_categories['product_category_name'].apply(lambda x: textwrap.fill(x, width=20))

        # Tentukan warna untuk setiap batang plot
        colors = ['lightgray'] * len(selected_categories)
        max_value = selected_categories['order_id'].max()
        max_index = selected_categories['order_id'].idxmax()
        colors[selected_categories.index.get_loc(max_index)] = '#8fc456'  # Warna biru untuk kategori dengan order terbanyak

        # Visualisasi menggunakan bar plot
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x='product_category_name', y='order_id', data=selected_categories, palette=colors)

        # Atur judul dan label sumbu
        plt.title('Banyak Order per Kategori (Top 5 & Bottom 5)', fontsize=14)
        plt.xlabel('Kategori Produk', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)

        # Atur rotasi label sumbu x agar terlihat jelas
        plt.xticks(rotation=45, ha='right', fontsize=10)

        # Tambahkan label nilai di atas setiap bar
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        # Atur tampilan grid
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Hilangkan garis tepi atas dan kanan
        sns.despine()

        # Tampilkan plot
        plt.tight_layout()

        st.pyplot(plt) # Menampilkan bar plot di Streamlit

    elif pertanyaan == 'Bagaimana trend penjualan dari waktu ke waktu?':
        st.subheader("Trend Penjualan 2016-2018")
        # Gabungkan dataframe orders_df dan order_items_df
        order_items_df = pd.read_csv('../data/order_items_dataset.csv')
        orders_df = pd.read_csv('../data/orders_dataset.csv')
        
        for column in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
               'order_delivered_customer_date', 'order_estimated_delivery_date']:
            orders_df[column] = pd.to_datetime(orders_df[column], errors='coerce')
    
        orders_items_df = pd.merge(orders_df, order_items_df, on='order_id')

        # Groupby berdasarkan bulan dan hitung jumlah order
        monthly_orders = orders_items_df.groupby(orders_items_df['order_purchase_timestamp'].dt.to_period('M'))['order_id'].nunique().reset_index()

        # Ubah tipe data period[M] menjadi string
        monthly_orders['order_purchase_timestamp'] = monthly_orders['order_purchase_timestamp'].astype(str)

        # Visualisasi menggunakan line plot
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='order_purchase_timestamp', y='order_id', data=monthly_orders)
        plt.xticks(rotation=45, ha='right')
        plt.title('Tren Penjualan dari Waktu ke Waktu')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Order')
        plt.tight_layout()
        st.pyplot(plt) # Menampilkan line plot di Streamlit

    elif pertanyaan == 'Apa metode pembayaran yang paling sering digunakan?':
        st.subheader("Metode Pembayaran Paling Banyak Digunakan")

        # Membaca data
        order_payments_df = pd.read_csv('../data/order_payments_dataset.csv')

        # Group data berdasarkan metode pembayaran dan hitung jumlah order
        payment_method_counts = order_payments_df.groupby('payment_type')['order_id'].nunique().reset_index()

        # Urutkan data berdasarkan jumlah order secara descending
        payment_method_counts = payment_method_counts.sort_values(by=['order_id'], ascending=False)

        # Visualisasi menggunakan bar plot
        plt.figure(figsize=(10, 6))

        # Tentukan warna untuk setiap batang plot
        colors = ['lightgray'] * len(payment_method_counts)
        max_value = payment_method_counts['order_id'].max()
        max_index = payment_method_counts['order_id'].idxmax()
        colors[payment_method_counts.index.get_loc(max_index)] = '#8fc456'  # Warna biru untuk batang dengan nilai tertinggi

        ax = sns.barplot(x='payment_type', y='order_id', data=payment_method_counts, palette=colors)

        # Atur judul dan label sumbu
        plt.title('Metode Pembayaran yang Paling Sering Digunakan', fontsize=14)
        plt.xlabel('Metode Pembayaran', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)

        # Atur rotasi label sumbu x agar terlihat jelas
        plt.xticks(rotation=45, ha='right', fontsize=10)

        # Tambahkan label nilai di atas setiap bar
        for index, value in enumerate(payment_method_counts['order_id']):
            plt.text(index, value + 500, str(value), ha='center', va='bottom', fontsize=10)

        # Atur tampilan grid
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Hilangkan garis tepi atas dan kanan
        sns.despine()

        # Tampilkan plot di Streamlit
        st.pyplot(plt)

    elif pertanyaan == 'Bagaimana tingkat kepuasan pelanggan terhadap produk yang dibeli?':
        st.subheader("Tingkat Kepusasan Pelanggan")
        order_reviews_df = pd.read_csv('../data/order_reviews_dataset.csv')
        
        review_score_counts = order_reviews_df['review_score'].value_counts().sort_index()

        # Hitung persentase kepuasan pelanggan
        total_reviews = review_score_counts.sum()
        satisfaction_percentage = (review_score_counts.get(4, 0) + review_score_counts.get(5, 0)) / total_reviews * 100

        # Visualisasi distribusi review score dengan diagram batang dan label persentase
        plt.figure(figsize=(8, 6))
        ax = sns.countplot(x='review_score', data=order_reviews_df, palette='viridis')
        plt.title('Distribusi Skor Review Pelanggan', fontsize=16, fontweight='bold')
        plt.xlabel('Skor Review', fontsize=12)
        plt.ylabel('Jumlah Review', fontsize=12)

        # Dapatkan indeks rating terbanyak
        most_frequent_rating = review_score_counts.idxmax()

        # Ubah warna batang plot kecuali rating terbanyak
        for i, p in enumerate(ax.patches):
            if i != most_frequent_rating - 1:  # Kurangi 1 karena indeks dimulai dari 0
                p.set_facecolor('lightgray')

        # Tambahkan label persentase di atas setiap batang
        for p in ax.patches:
            height = p.get_height()
            percentage = height / total_reviews * 100
            ax.text(p.get_x() + p.get_width() / 2., height + 1, f'{percentage:.1f}%', ha='center', fontsize=10)

        # Tambahkan garis horizontal untuk menunjukkan tingkat kepuasan pelanggan
        ax.axhline(y=review_score_counts.get(4, 0) + review_score_counts.get(5, 0), color='red', linestyle='--', label=f'Tingkat Kepuasan: {satisfaction_percentage:.2f}%')
        plt.legend()

        # Hilangkan garis tepi atas dan kanan
        sns.despine()

        # plt.tight_layout()

        # Tampilkan plot di Streamlit

        st.pyplot(plt)


# Menampilkan visualisasi yang dipilih
tampilkan_visualisasi(pertanyaan_bisnis)
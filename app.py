import streamlit as st
import pandas as pd
import yfinance as yf
import investpy as inv
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import plotly.graph_objects as go

def home():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image('logo.png', width=200)
        st.markdown('---')
        st.title('App Financeiro')
        st.markdown('---')

def panorama():
    st.title('Panorama do Mercado')
    st.markdown(date.today().strftime(('%d/%m/%Y')))

    st.subheader('Mercados pelo Mundo')

    dict_tickers= {
        'Bovespa': '^BVSP',
        'S&P500': '^GSPC',
        'NASDAQ':'^IXIC',
        'DAX':'^GDAXI',
        'FTSE 100': '^FTSE',
        'Cruid oil':'CL=F',
        'Gold':'GC=F',
        'BITCOIN':'BTC-USD',
        'ETHEREUM':'ETH-USD'
        }

    df_info =pd.DataFrame({'Ativo':dict_tickers.keys(), 'Ticker': dict_tickers.values()})
    df_info['Ult. Valor'] = ''
    df_info['%']= ''
    cont = 0
    with st.spinner('Baixando cotações...'):
        for ticker in dict_tickers.values():
            cotacoes = yf.download(ticker,period='5d')['Adj Close']
            variacao =((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
            df_info['Ult. Valor'][cont] = round(cotacoes.iloc[-1],2)
            df_info['%'][cont] = round(variacao,2)
            cont+=1

    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric(df_info['Ativo'][0],value=df_info['Ult. Valor'][0],delta=str(df_info['%'][0]) + '%')
        st.metric(df_info['Ativo'][1],value=df_info['Ult. Valor'][1],delta=str(df_info['%'][1]) + '%')
        st.metric(df_info['Ativo'][2],value=df_info['Ult. Valor'][2],delta=str(df_info['%'][2]) + '%')

    with col2:
        st.metric(df_info['Ativo'][3],value=df_info['Ult. Valor'][3],delta=str(df_info['%'][3]) + '%')
        st.metric(df_info['Ativo'][4],value=df_info['Ult. Valor'][4],delta=str(df_info['%'][4]) + '%')
        st.metric(df_info['Ativo'][5],value=df_info['Ult. Valor'][5],delta=str(df_info['%'][5]) + '%')

    with col3:
        st.metric(df_info['Ativo'][6],value=df_info['Ult. Valor'][6],delta=str(df_info['%'][6]) + '%')
        st.metric(df_info['Ativo'][7],value=df_info['Ult. Valor'][7],delta=str(df_info['%'][7]) + '%')
        st.metric(df_info['Ativo'][8],value=df_info['Ult. Valor'][8],delta=str(df_info['%'][8]) + '%')

    st.markdown('---')

    st.subheader('Comportamento durante o dia')

    lista_indices = ['IBOV','S&P500','NASDAQ']

    indice =st.selectbox('Selecione o Índice', lista_indices)

    if indice =='IBOV':
        indice_diario = yf.download('^BVSP', period='1d', interval='5m')
    if indice =='S&P500':
        indice_diario = yf.download('^GSPC', period='1d', interval='5m') 
    if indice =='NASDAQ':
        indice_diario = yf.download('^IXIC', period='1d', interval='5m')

    fig = go.Figure(data=[go.Candlestick(x=indice_diario.index,
                                        open=indice_diario['Open'],
                                        high=indice_diario['High'],
                                        low=indice_diario['Low'],
                                        close=indice_diario['Close'])])
    fig.update_layout(title=indice,xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

    indice_acoes = ['PETR4','VALE3.SA','EQTL3.SA','CSNA3.SA']
    acao =st.selectbox('Selecione a ação', indice_acoes)

    hiist_acao = yf.download(acao,period='1d',interval='5m')
    fig = go.Figure(data=[go.Candlestick(x=hiist_acao.index,
                                        open=hiist_acao['Open'],
                                        high=hiist_acao['High'],
                                        low=hiist_acao['Low'],
                                        close=hiist_acao['Close'])])
    fig.update_layout(title=acao,xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

def mapa_mensal():
    st.title('Análise Retornos Mensais')

    with st.expander('Escolha', expanded=True):
        opcao = st.radio('Selecione',['Índices','Ações'])
    if opcao =='Índices':
        with st.form(key='form_indice'):
            ticker = st.selectbox('Índice',['^BVSP','IFNC.SA','IMAT.SA'])
            analisar = st.form_submit_button('Analisar')
    else:
        with st.form(key='form_acoes'):
            ticker = st.selectbox('Ações',['PETR4.SA','EQTL3.SA','VALE3.SA'])
            analisar = st.form_submit_button('Analisar')

    if analisar:
        data_inicial = '1999-12-01'
        data_final = '2022-12-31'

        if opcao == 'Índices':
            # Obtenha dados históricos usando yfinance
            data = yf.download(ticker, start=data_inicial, end=data_final, interval='1mo')
            retornos = data['Close'].pct_change()
        else:
            # Obtenha dados históricos usando yfinance
            data = yf.download(ticker, start=data_inicial, end=data_final, interval='1mo')
            retornos = data['Close'].pct_change()


        retorno_mensal = retornos.groupby([retornos.index.year.rename('Year'), retornos.index.month.rename('Mounth')]).mean()

        tabela_retornos = pd.DataFrame(retorno_mensal)
        tabela_retornos = pd.pivot_table(tabela_retornos,values='Close',index='Year',columns='Mounth')
        tabela_retornos.columns=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        fig, ax =plt.subplots(figsize=(12,9))
        cmap = sns.color_palette('RdYlGn',50)
        sns.heatmap(tabela_retornos,cmap=cmap,annot=True, fmt='.2%',center=0,vmax=0.02,vmin=-0.02,cbar=False,
                    linewidths=1,xticklabels=True,yticklabels=True,ax=ax)
        ax.set_title(ticker,fontsize=18)
        ax.set_yticklabels(ax.get_yticklabels(),rotation=0,verticallignment='center',fontsize='12')
        ax.set_xticklabels(ax.get_xticklabels(),fontsize='12')
        ax.xaxis.tick_top()
        plt.ylabel('')
        st.pyplot(fig)



def fundamentos():
    import fundamentus as fd
    st.title('Informações de Fundamentos')

    lista_tickers=fd.list_papel_all()

    comparar = st.checkbox('Comprar 2 ativos')

    col1, col2 = st.columns(2)

    with col1:
        with st.expander('Ativo 1', expanded=True):
            papel1 = st.selectbox('Selecione o Papel 1', lista_tickers)
            info_papel1 = fd.get_detalhes_papel(papel1)

            st.write("**Empresas:**", info_papel1.get('Empresa', ['N/A'])[0])
            st.write("**Setor:**", info_papel1.get('Setor', ['N/A'])[0])
            st.write("**Subsetor:**", info_papel1.get('Subsetor', ['N/A'])[0])
            st.write("**Valor de Mercado:**", f"R$ {float(info_papel1.get('Valor_de_mercado', [0])[0]):,.2f}")
            st.write("**Patrimônio Líquido:**", f"R$ {float(info_papel1.get('Patrim_Liq', [0])[0]):,.2f}")
            st.write("**Receita Liq. 12m:**", f"R$ {float(info_papel1.get('Receita_Liquida_12m', [0])[0]):,.2f}")
            st.write("**Dívida Bruta:**", f"R$ {float(info_papel1.get('Div_Bruta', [0])[0]):,.2f}")
            st.write("**Dívida Líquida:**", f"R$ {float(info_papel1.get('Div_Liquida', [0])[0]):,.2f}")
            st.write("**P/L:**", f"{float(info_papel1.get('PL', [0])[0]):,.2f}")
            st.write("**Dividend Yield:**", info_papel1.get('Div_Yield', ['N/A'])[0])

    if comparar:
        with col2:
            with st.expander("Ativo 2", expanded=True):
                papel2 = st.selectbox('Selecione o Papel 2', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)

                st.write("**Empresas:**", info_papel2.get('Empresa', ['N/A'])[0])
                st.write("**Setor:**", info_papel2.get('Setor', ['N/A'])[0])
                st.write("**Subsetor:**", info_papel2.get('Subsetor', ['N/A'])[0])
                st.write("**Valor de Mercado:**", f"R$ {float(info_papel2.get('Valor_de_mercado', [0])[0]):,.2f}")
                st.write("**Patrimônio Líquido:**", f"R$ {float(info_papel2.get('Patrim_Liq', [0])[0]):,.2f}")
                st.write("**Receita Liq. 12m:**", f"R$ {float(info_papel2.get('Receita_Liquida_12m', [0])[0]):,.2f}")
                st.write("**Dívida Bruta:**", f"R$ {float(info_papel2.get('Div_Bruta', [0])[0]):,.2f}")
                st.write("**Dívida Líquida:**", f"R$ {float(info_papel2.get('Div_Liquida', [0])[0]):,.2f}")
                st.write("**P/L:**", f"{float(info_papel2.get('PL', [0])[0]):,.2f}")
                st.write("**Dividend Yield:**", info_papel2.get('Div_Yield', ['N/A'])[0])




def main():
    st.sidebar.image('logo.png')
    st.sidebar.title('App Financeiro')
    st.sidebar.markdown('---')
    lista_menu = ['Home', 'Panorama do Mercado','Rentabilidades Mensais','Fundamentos']
    escolha = st.sidebar.radio('Escolha a opção', lista_menu)

    if escolha =='Home':
        home()
    if escolha =='Panorama do Mercado':
        panorama()
    if escolha =='Rentabilidades Mensais':
        mapa_mensal()
    if escolha =='Fundamentos':
        fundamentos()
main()
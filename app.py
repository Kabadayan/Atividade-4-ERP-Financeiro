import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatórios Financeiros")
        
        # Fluxo de Caixa por Mês
        st.subheader("Fluxo de Caixa por Mês")
        df_fluxo = pd.read_sql_query("SELECT strftime('%Y-%m', data) as mes, tipo, SUM(valor) as total FROM lancamentos GROUP BY mes, tipo", conn)
        if not df_fluxo.empty:
            fig = px.bar(df_fluxo, x='mes', y='total', color='tipo', barmode='group', labels={'mes': 'Mês', 'total': 'Valor', 'tipo': 'Tipo'})
            st.plotly_chart(fig)
        else:
            st.write("Nenhum dado disponível.")
        
        # Distribuição das Contas a Pagar por Fornecedor
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
        df_pagar = pd.read_sql_query("SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor", conn)
        if not df_pagar.empty:
            fig = px.pie(df_pagar, names='fornecedor', values='total', title='Distribuição das Contas a Pagar')
            st.plotly_chart(fig)
        else:
            st.write("Nenhum dado disponível.")
        
        # Status das Contas a Pagar e Receber
        st.subheader("Status das Contas a Pagar e Receber")
        df_status_pagar = pd.read_sql_query("SELECT status, SUM(valor) as total FROM contas_pagar GROUP BY status", conn)
        df_status_receber = pd.read_sql_query("SELECT status, SUM(valor) as total FROM contas_receber GROUP BY status", conn)
        df_status_pagar['tipo'] = 'Contas a Pagar'
        df_status_receber['tipo'] = 'Contas a Receber'
        df_status = pd.concat([df_status_pagar, df_status_receber])
        
        if not df_status.empty:
            fig = px.bar(df_status, x='status', y='total', color='tipo', barmode='group', labels={'status': 'Status', 'total': 'Valor'})
            st.plotly_chart(fig)
        else:
            st.write("Nenhum dado disponível.")
    
    conn.close()
    
if __name__ == "__main__":
    main()

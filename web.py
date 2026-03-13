import streamlit as st
import app

st.set_page_config(layout="wide")

enemy_cards, my_cards = app.show_stats()


st.title("Clash Royale Stats", text_alignment="center")
st.header("was schreibt man hier", text_alignment="center")


tab1, tab2 = st.tabs(["Card Stats", "Deck Builder"])   


with tab1:


    area1, area2, area3, area4 = st.columns([5, 1, 5, 1])

    with area1:

        st.subheader("Opponent Cards")

        for wert in enemy_cards:

            spalte_1, spalte_2, spalte_3 = st.columns([1, 2, 2])

            with spalte_1:
                st.image(wert[4], width=90)
                st.markdown(wert[0])
        
            with spalte_2:
                spalte_2.metric("Winrate last 10 games", "upcoming", f"{5} %")
                spalte_2.metric("Winrate all-time", app.winrate_percent(wert[1], wert[2], wert[3]))

            with spalte_3:
                spalte_3.metric("Wins/Draws/Losses", f"{wert[1]}/{wert[2]}/{wert[3]- wert[1]-wert[2]}", f"{wert[3]} games", delta_color="off", delta_arrow="off")
                
            st.divider()

    with area3:

        st.subheader("My Cards")

        for wert in my_cards:

            spalte_1, spalte_2, spalte_3 = st.columns([1, 2, 2])

            with spalte_1:
                st.image(wert[4], width=90)
                st.markdown(wert[0])
        
            with spalte_2:
                spalte_2.metric("Winrate last 10 games", "upcoming", f"{5} %")
                spalte_2.metric("Winrate all-time", app.winrate_percent(wert[1], wert[2], wert[3]))

            with spalte_3:
                spalte_3.metric("Wins/Draws/Losses", f"{wert[1]}/{wert[2]}/{wert[3]- wert[1]-wert[2]}", f"{wert[3]} games", delta_color="off", delta_arrow="off")
                
            st.divider()

    with area4:
        if st.button("Reload games", ):
            with st.spinner("Loading...", show_time=False):
                st.cache_data.clear()
                app.update_games()
            
with tab2:

   pass
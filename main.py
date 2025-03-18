import streamlit as st


if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
if "chat_history1" not in st.session_state:
        st.session_state["chat_history1"] = []


def intro():
    from Backend.backendA import run_llm
    

    st.write("### NabuX")
    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []


    
    # Display chat messages from history
    for message_data in st.session_state.messages:
        with st.chat_message(message_data["role"]):
            st.markdown(message_data["content"])

    # Input box for user prompt
    if prompt := st.chat_input("Entrez votre message ici..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response using the LLM
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history"]
            )
            st.session_state["chat_history"].append(("human", prompt))
            st.session_state["chat_history"].append(("ai", generated_response))

            with st.chat_message("assistant"):
                st.markdown(generated_response)
            st.session_state.messages.append({"role": "assistant", "content": generated_response})


def understand():

    from Backend.backendB import run_llm

   
    st.write("### NabuX")

    if "messages1" not in st.session_state:
        st.session_state.messages1 = []
    
    # Display chat messages from history
    for message_data in st.session_state.messages1:
        with st.chat_message(message_data["role"]):
            st.markdown(message_data["content"])
    


    if prompt := st.chat_input("Entrez votre message ici..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages1.append({"role": "user", "content": prompt})

        # Generate response using the LLM
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history1"]
            )

            st.session_state["chat_history1"].append(("human", prompt))
            st.session_state["chat_history1"].append(("ai", generated_response))
            with st.chat_message("assistant"):
                st.markdown(generated_response)
            st.session_state.messages1.append({"role": "assistant", "content": generated_response})

        

def upgrade_page():
    """Displays a visually enhanced upgrade page in Streamlit while keeping content simple."""
    import streamlit as st
    
    # Page styling with enhanced but clean UI
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #6c5ce7 0%, #a29bfe 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 25px;
        }
        .plan-container {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            height: 100%;
            transition: all 0.3s ease;
        }
        .plan-container:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-5px);
        }
        .premium-plan {
            border: 2px solid #6c5ce7;
            background-color: #f8f7ff;
        }
        .feature-box {
            background-color: white;
            border-left: 4px solid #6c5ce7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        .feature-box:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .premium-tag {
            background-color: #6c5ce7;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        .btn-premium {
            background-color: #6c5ce7;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-premium:hover {
            background-color: #5344cf;
            box-shadow: 0 5px 15px rgba(108, 92, 231, 0.3);
        }
        .check-icon {
            color: #6c5ce7;
            font-weight: bold;
        }
        .faq-header {
            background-color: #f8f7ff;
            padding: 10px;
            border-radius: 8px;
        }
        .divider {
            height: 3px;
            background: linear-gradient(90deg, #6c5ce7 0%, #a29bfe 100%);
            border: none;
            margin: 30px 0;
        }
        .footer-cta {
            background-color: #f8f7ff;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Améliorez Votre Expérience NabuX</h1>
        <p>Débloquez des fonctionnalités premium pour enrichir votre apprentissage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Brief introduction
    st.markdown("Passez à la version premium pour accéder à des outils avancés et progresser plus rapidement.")
    
    # Enhanced pricing display
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="plan-container">', unsafe_allow_html=True)
        st.markdown("### Version Gratuite")
        st.markdown("**Votre plan actuel**")
        st.markdown('<span class="check-icon">✓</span> Accès aux cours fondamentaux', unsafe_allow_html=True)
        st.markdown('<span class="check-icon">✓</span> Quiz basiques', unsafe_allow_html=True)
        st.markdown('<span class="check-icon">✓</span> Ressources essentielles', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="plan-container premium-plan">', unsafe_allow_html=True)
        st.markdown("### Version Premium")
        st.markdown("**29,99€ / mois**")
        st.markdown('<span class="check-icon">✓</span> Tous les cours avancés', unsafe_allow_html=True)
        st.markdown('<span class="check-icon">✓</span> Projets pratiques guidés', unsafe_allow_html=True)
        st.markdown('<span class="check-icon">✓</span> Feedback personnalisé', unsafe_allow_html=True)
        st.markdown('<span class="check-icon">✓</span> Support prioritaire', unsafe_allow_html=True)
        st.markdown('<button class="btn-premium">🚀 Passer à Premium</button>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # Key premium features
    st.subheader("Fonctionnalités Premium")
    
    features = [
        {
            "title": "Transformez la connaissance en action créative",
            "description": "Mettez vos idées en pratique avec des outils avancés et des projets guidés."
        },
        {
            "title": "Explorez les secrets de l'analyse approfondie",
            "description": "Accédez à des analyses détaillées et des perspectives enrichies."
        },
        {
            "title": "Affinez vos compétences par l'évaluation continue",
            "description": "Profitez de tests interactifs et de feedback personnalisé."
        },
        {
            "title": "Libérez votre créativité et atteignez le sommet",
            "description": "Déverrouillez des fonctionnalités exclusives pour repousser vos limites."
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-box">
            <h4><span class="premium-tag">PREMIUM</span> {feature['title']}</h4>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Simple FAQ with enhanced styling
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="faq-header">', unsafe_allow_html=True)
    st.subheader("Questions fréquentes")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("Puis-je annuler à tout moment ?"):
        st.write("Oui, vous pouvez annuler votre abonnement premium à tout moment.")
    
    with st.expander("Y a-t-il une période d'essai ?"):
        st.write("Oui, profitez d'un essai gratuit de 7 jours de toutes les fonctionnalités premium.")
    
    # Final CTA with enhanced styling
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
   
   

with st.sidebar:
    
    st.sidebar.image("img/NabuX1.png", width=150, use_container_width=False)
    # CSS to hide the fullscreen button/icon from sidebar images
    hide_fullscreen_css = '''
    <style>
    div.stElementToolbar {
        display: none !important;
    }
    </style>
    '''

    st.markdown(hide_fullscreen_css, unsafe_allow_html=True)

    st.write("De la curiosité à la maîtrise, explorez et apprenez l'intelligence artificielle.")

    page_names_to_funcs = {
    "Découvrez le monde de l'intelligence artificielle": intro,
    "Approfondissez votre compréhension du domaine": understand,
    "Transformez la connaissance en action créative 🔒": upgrade_page,
    "Explorez les secrets de l'analyse approfondie 🔒": upgrade_page,
    "Affinez vos compétences par l'évaluation continue 🔒": upgrade_page,
    "Libérez votre créativité et atteignez l'excellence 🔒": upgrade_page
    
}
    st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break
    disabled_status = True
    demo_name = st.sidebar.selectbox("**Choisissez le niveau**", page_names_to_funcs.keys())

 
    st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break
    st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

        # Create a single column layout
    col1, col2, col3 = st.columns([1, 2, 1])  # You can adjust the ratios

    with col2:  # The center column
        # Button for new chat
        if st.button("Nouvelle conversation", use_container_width=True):
            st.session_state.messages = []  # Clear chat history on new chat
            st.session_state["chat_history"] = []
            st.session_state.messages1 = []  # Clear chat history on new chat
            st.session_state["chat_history1"] = []

    # Sidebar footer for license activation
    st.markdown("---")
    st.write("© 2025 NabuX. Tous droits réservés.")
    st.markdown(
        """
        <p>
        <a href="#" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/>
        </a>
        <a href="#" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/telegram-app.png"/>
        </a>
        <a href="#" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/email.png"/>
        </a>
        </p>
        """, unsafe_allow_html=True
    )



page_names_to_funcs[demo_name]()




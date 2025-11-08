import streamlit as st
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables (like GOOGLE_API_KEY) from .env file
load_dotenv()   

from trip_agents import TripCrew   # import AFTER .env is loaded

# Page config
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

# --- CSS LOADING FUNCTION ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

# Add fun travel quotes
travel_quotes = [
    "Adventure is worthwhile - Aesop",
    "Travel is the only thing you buy that makes you richer - Anonymous",
    "Life is either a daring adventure or nothing at all - Helen Keller",
    "Travel makes one modest. You see what a tiny place you occupy in the world - Gustav Flaubert",
    "The world is a book and those who do not travel read only one page - Saint Augustine"
]

# Function to calculate trip sentiment and recommendations
def get_trip_persona(interests, budget, duration):
    personas = {
        "Adventure Seeker": ["Adventure", "Nature", "Sports"],
        "Culture Explorer": ["Culture", "History", "Art", "Architecture"],
        "Urban Wanderer": ["Shopping", "Food", "Music", "Photography"],
        "Relaxation Enthusiast": ["Relaxation", "Beach", "Spa"]
    }
    
    user_interests = set(interests)
    max_matches = 0
    best_persona = "Balanced Traveler"
    
    for persona, persona_interests in personas.items():
        matches = len(user_interests.intersection(persona_interests))
        if matches > max_matches:
            max_matches = matches
            best_persona = persona
            
    return best_persona

# Load GOOGLE_API_KEY from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Sidebar for settings and tips
with st.sidebar:
    st.title("⚙️ Settings")
    # Check for GOOGLE_API_KEY
    if not GOOGLE_API_KEY:
        st.warning("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
    else:
        st.success("Google API key loaded successfully!")

    st.divider()
    st.markdown("### 💡 Trip Planning Tips")
    st.info("""
    - Enter both source and destination cities
    - Choose travel dates that work best for you
    - Select your interests to get personalized recommendations
    - Specify any special requirements
    - Consider weather preferences for better planning
    """)

# Main content
st.title("✈️ KARS LUX INTERNATIONAL TRAVELS")
st.markdown("##### Let us plan your perfect trip with personalized recommendations!")

# Display random travel quote
st.info(f"💭 *{travel_quotes[int(datetime.now().timestamp()) % len(travel_quotes)]}*")

# Add destination inspiration
with st.expander("🌟 Need Inspiration?"):
    st.markdown("""
    ### Popular Destinations by Interest
    
    🏛️ **History & Culture**
    - Rome, Italy
    - Kyoto, Japan
    - Athens, Greece
    
    🏖️ **Beach & Relaxation**
    - Maldives
    - Bali, Indonesia
    - Santorini, Greece
    
    🗺️ **Adventure**
    - New Zealand
    - Costa Rica
    - Iceland
    
    🍽️ **Food & Culinary**
    - Bangkok, Thailand
    - Barcelona, Spain
    - Tokyo, Japan
    """)

with st.form("travel_form"):
    tab1, tab2, tab3 = st.tabs(["🌍 Basic Info", "🎯 Preferences", "✨ Special Requests"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            source_city = st.text_input("Source City", "New York")
            departure_date = st.date_input(
                "Travel Date",
                min_value=datetime.now().date(),
                max_value=datetime.now().date() + timedelta(days=365)
            )
        with col2:
            destination_city = st.text_input("Destination City", "Paris")
            duration = st.slider("Duration (days)", 1, 30, 7)
            
        preferred_time = st.select_slider(
            "Preferred Flight Time",
            options=["Early Morning", "Morning", "Afternoon", "Evening", "Night"],
            value="Morning"
        )
    
    with tab2:
        st.markdown("### 🎨 Create Your Perfect Trip")
        
        col1, col2 = st.columns(2)
        with col1:
            travel_style = st.radio(
                "Travel Style",
                ["Solo Adventure", "Couple's Getaway", "Family Trip", "Friends' Adventure", "Business & Leisure"]
            )
            
            interests = st.multiselect(
                "Interests",
                ["Culture", "Food", "Nature", "Shopping", "History", "Adventure", 
                 "Art", "Music", "Architecture", "Sports", "Relaxation", "Photography",
                 "Local Experiences", "Festivals", "Wellness", "Technology"],
                ["Culture", "Food"]
            )
            
            weather_preference = st.select_slider(
                "Weather Preference",
                options=["Cold", "Mild", "Warm", "Hot"],
                value="Mild"
            )
            
        with col2:
            budget = st.selectbox(
                "Budget Level",
                ["Budget", "Moderate", "Luxury"],
                index=1
            )
            
            pace_preference = st.select_slider(
                "Travel Pace",
                options=["Relaxed", "Moderate", "Fast-paced"],
                value="Moderate"
            )
            
            location_preference = st.selectbox(
                "Preferred Location",
                ["City Center", "Near Attractions", "Quiet Neighborhood", "Beach Area", 
                 "Business District", "Historic Quarter", "Local Neighborhood"],
                index=0
            )
            
        # Show travel persona based on selections
        travel_persona = get_trip_persona(interests, budget, duration)
        st.markdown(f"### 🎭 Your Travel Persona: **{travel_persona}**")
    
    with tab3:
        st.markdown("### 🌈 Personalize Your Experience")
        
        # Special Requirements with categories
        st.subheader("Special Requirements")
        req_col1, req_col2 = st.columns(2)
        
        with req_col1:
            accessibility_needs = st.multiselect(
                "Accessibility Needs",
                ["Wheelchair Accessible", "Limited Mobility", "Visual Aids", "Hearing Aids", "None"],
                default=["None"]
            )
            
            dietary_restrictions = st.multiselect(
                "Dietary Preferences",
                ["Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-Free", "None"],
                default=["None"]
            )
        
        with req_col2:
            medical_needs = st.text_area(
                "Medical Considerations",
                placeholder="Any medical requirements we should consider..."
            )
            
            language_preference = st.multiselect(
                "Language Preferences",
                ["English Only", "Local Language", "Translator Needed", "None"],
                default=["English Only"]
            )
        
        # Experience Enhancements
        st.subheader("Enhance Your Trip")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_shopping = st.checkbox("🛍️ Shopping Guides")
            include_nightlife = st.checkbox("🌙 Nightlife Options")
            include_photography = st.checkbox("📸 Photo Spots")
        
        with col2:
            include_work_spaces = st.checkbox("💼 Work-Friendly Spaces")
            include_local_events = st.checkbox("🎪 Local Events")
            include_wellness = st.checkbox("🧘‍♀️ Wellness Activities")
            
        with col3:
            include_cooking = st.checkbox("👨‍🍳 Cooking Classes")
            include_workshops = st.checkbox("🎨 Local Workshops")
            include_volunteering = st.checkbox("🤝 Volunteering Opportunities")
            
        # Additional Notes
        special_requirements = st.text_area(
            "Additional Notes",
            placeholder="Any other preferences or requirements..."
        )
    
    submitted = st.form_submit_button("🎯 Plan My Trip")

if submitted:
    if not GOOGLE_API_KEY:
        st.error("Google API key missing. Please add it to your .env file.")
    else:
        try:
            with st.spinner("🔄 Planning your perfect trip... (This may take 1-2 minutes)"):
                inputs = {
                    "source_city": source_city,
                    "destination_city": destination_city,
                    "travel_date": departure_date.strftime("%Y-%m-%d"),
                    "duration": duration,
                    "preferred_time": preferred_time,
                    "interests": interests,
                    "budget": budget,
                    "weather_preference": weather_preference,
                    "location_preference": location_preference,
                    "special_requirements": special_requirements if special_requirements else "None",
                    
                    "accessibility_needs": accessibility_needs,
                    "dietary_restrictions": dietary_restrictions,
                    "medical_needs": medical_needs,
                    "language_preference": language_preference,
                    "include_shopping": include_shopping,
                    "include_nightlife": include_nightlife,
                    "include_photography": include_photography,
                    "include_work_spaces": include_work_spaces,
                    "include_local_events": include_local_events,
                    "include_wellness": include_wellness,
                    "include_cooking": include_cooking,
                    "include_workshops": include_workshops,
                    "include_volunteering": include_volunteering,
                    "travel_style": travel_style,
                    "pace_preference": pace_preference
                }
                
                trip_crew = TripCrew(inputs)
                result = trip_crew.crew.kickoff()
                
                task_outputs = result.tasks_output
                logistics_out = task_outputs[0].raw
                budget_out = task_outputs[1].raw
                plan_out = task_outputs[2].raw
                insights_out = task_outputs[3].raw
                experiences_out = task_outputs[4].raw

                st.success("✨ Your comprehensive travel plan is ready!")
                
                # Interactive Results Display
                overview_tab, plan_tab, logistics_tab, budget_tab, tips_tab, extras_tab = st.tabs([
                    "🌟 Overview", "📅 Itinerary", "✈️ Travel & Stay", "💰 Budget", "📝 Local Tips", "✨ Extras"
                ])
                
                with overview_tab:
                    st.markdown("### 🌟 Trip Overview")
                    col1, col2, col3 = st.columns([2,1,1])
                    
                    with col1:
                        st.markdown(f"""
                        #### 🎯 Trip Summary
                        - **Style**: {travel_style}
                        - **Duration**: {duration} days
                        - **Travel Persona**: {travel_persona}
                        - **Pace**: {pace_preference}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        #### 🎨 Interests
                        {', '.join([f'• {i}' for i in interests])}
                        """)
                    
                    with col3:
                        st.markdown(f"""
                        #### 📍 Key Details
                        - From: {source_city}
                        - To: {destination_city}
                        - When: {departure_date}
                        """)
                    st.divider()
                    st.markdown("### 💎 Special Experiences")
                    st.markdown(experiences_out)

                with plan_tab:
                    st.markdown("### 📅 Day-by-Day Itinerary")
                    st.info("💡 Here is your detailed, day-by-day plan.")
                    st.markdown(plan_out)
                
                with logistics_tab:
                    st.markdown("### ✈️ Travel & Accommodation Details")
                    st.markdown(logistics_out)
                        
                with budget_tab:
                    st.markdown("### 💰 Budget Breakdown")
                    st.markdown(budget_out)
                
                with tips_tab:
                    st.markdown("### 📝 Local Insights & Tips")
                    st.markdown(insights_out)
                            
                with extras_tab:
                    st.markdown("### ✨ Special Experiences")
                    st.markdown(experiences_out)
                
                # Combine all parts for the download file
                full_itinerary = f"""
TRIP PLAN FOR {destination_city.upper()}
================================
LOGISTICS
{logistics_out}
================================
BUDGET
{budget_out}
================================
ITINERARY
{plan_out}
================================
LOCAL INSIGHTS
{insights_out}
================================
EXPERIENCES
{experiences_out}
"""
                
                # Download button for the complete plan
                st.download_button(
                    label="📥 Download Complete Travel Plan",
                    data=full_itinerary,
                    file_name=f"travel_plan_{destination_city}_{departure_date}.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please check your GOOGLE_API_KEY in the .env file and ensure you have internet access.")
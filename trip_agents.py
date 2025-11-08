from crewai import Agent, Task, Crew, LLM
from datetime import datetime
import os

class TripCrew:
    def __init__(self, inputs):
        self.inputs = inputs
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")


        self.llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            temperature=0.7,
            api_key=api_key
        )

        self.crew = self._create_crew()
        
    def _get_season(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            month = date_obj.month
            if month in [12, 1, 2]: return "Winter"
            elif month in [3, 4, 5]: return "Spring"
            elif month in [6, 7, 8]: return "Summer"
            else: return "Fall"
        except:
            return "Any"
            
    def _get_experience_level(self, style, interests):
        if "Adventure" in interests or "Local Experiences" in interests:
            return "Explorer"
        elif style in ["Solo Adventure", "Friends' Adventure"]:
            return "Independent"
        elif "Culture" in interests or "History" in interests:
            return "Cultural Enthusiast"
        else:
            return "Casual Traveler"

    def _create_crew(self):
        season = self._get_season(self.inputs['travel_date'])
        experience_level = self._get_experience_level(
            self.inputs.get('travel_style', 'Casual'),
            self.inputs['interests']
        )
        
        travel_coordinator = Agent(
            role="Travel Coordinator",
            goal="Plan comprehensive travel logistics including flights and hotels",
            backstory="Senior travel coordinator with expertise in flight bookings, hotel arrangements, and travel logistics",
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )
        
        experience_curator = Agent(
            role="Experience Curator",
            goal="Design unique and memorable experiences based on traveler preferences",
            backstory="Creative experience designer who specializes in crafting unique, personalized travel moments",
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

        planner = Agent(
            role="Travel Planner",
            goal="Create a detailed itinerary based on preferences and logistics",
            backstory="Expert travel planner with years of experience in creating personalized travel plans",
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

        local_expert = Agent(
            role="Local Expert",
            goal="Provide authentic local insights and cultural recommendations",
            backstory="A knowledgeable local expert with deep understanding of the destination",
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

        budget_analyst = Agent(
            role="Budget Analyst",
            goal="Optimize travel expenses and provide cost estimates",
            backstory="Financial expert specializing in travel budgeting and cost optimization",
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

        logistics_task = Task(
            description=f"""
            Plan travel logistics from {self.inputs['source_city']} to {self.inputs['destination_city']}:
            1. Research and recommend flights:
               - Budget level: {self.inputs['budget']}
               - Travel date: {self.inputs['travel_date']}
               - Preferred time: {self.inputs['preferred_time']}
            2. Find suitable hotels/accommodations:
               - Budget level: {self.inputs['budget']}
               - Location preference: {self.inputs.get('location_preference', 'City Center')}
            3. Provide transportation options (airport transfers, local transit tips).
            """,
            expected_output="Detailed travel logistics report including flight options, accommodation recommendations with prices, and local transport details.",
            agent=travel_coordinator
        )

        budget_analysis_task = Task(
            description=f"""
            Analyze costs for the {self.inputs['duration']}-day trip to {self.inputs['destination_city']} with a {self.inputs['budget']} budget.
            Provide estimated cost ranges for: Flights, Accommodation, Daily expenses (food/activities).
            Include 3 specific money-saving tips for this destination.
            """,
            expected_output="Comprehensive budget breakdown by category with total estimated trip cost and money-saving tips.",
            agent=budget_analyst
        )

        planning_task = Task(
            description=f"""
            Create a {self.inputs['duration']}-day travel plan for {self.inputs['destination_city']}.
            Consider:
            - Interests: {', '.join(self.inputs['interests'])}
            - Pace: {self.inputs['pace_preference']}
            - Style: {self.inputs.get('travel_style', 'General')}
            For each day, include Morning, Afternoon, and Evening activities with dining suggestions.
            """,
            expected_output="A detailed day-by-day travel itinerary matching user preferences.",
            agent=planner
        )

        local_insights_task = Task(
            description=f"""
            Provide local insights for {self.inputs['destination_city']}:
            1. Cultural dos and don'ts.
            2. 2-3 hidden gems (non-touristy spots).
            3. Safety tips and practical advice.
            4. Must-try local food recommendations.
            """,
            expected_output="Structured report with cultural norms, hidden gems, safety tips, and food recommendations.",
            agent=local_expert
        )

        experiences_task = Task(
            description=f"""
            Design 3 unique, memorable experiences for a {experience_level} traveler in {self.inputs['destination_city']} during {season}.
            Base it on interests: {', '.join(self.inputs['interests'])}.
            Include if selected: Photography ({self.inputs.get('include_photography')}), Cooking ({self.inputs.get('include_cooking')}), Nightlife ({self.inputs.get('include_nightlife')}), Wellness ({self.inputs.get('include_wellness')}).
            """,
            expected_output="List of 3 unique, personalized experience descriptions with details on how to arrange them.",
            agent=experience_curator
        )

        return Crew(
            agents=[travel_coordinator, budget_analyst, planner, local_expert, experience_curator],
            tasks=[logistics_task, budget_analysis_task, planning_task, local_insights_task, experiences_task],
            verbose=True
        )
import streamlit as st
import time
import random
from datetime import datetime
from typing import List, Dict, Any
import json

# Mock LangChain-style classes
class MockAgent:
    def __init__(self, name: str, role: str, tools: List[str]):
        self.name = name
        self.role = role
        self.tools = tools
        self.status = "idle"
    
    def execute_task(self, task: str) -> Dict[str, Any]:
        """Mock task execution with realistic delays and responses"""
        self.status = "working"
        
        # Simulate processing time
        processing_time = random.uniform(1, 3)
        time.sleep(processing_time)
        
        # Mock success/failure (95% success rate)
        success = random.random() > 0.05
        
        result = {
            "agent": self.name,
            "task": task,
            "status": "completed" if success else "failed",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "processing_time": f"{processing_time:.1f}s",
            "details": self._generate_task_details(task, success)
        }
        
        self.status = "completed" if success else "failed"
        return result
    
    def _generate_task_details(self, task: str, success: bool) -> str:
        """Generate realistic task completion details"""
        if not success:
            return "❌ Task failed due to external dependency issue. Retrying..."
        
        task_lower = task.lower()
        if "venue" in task_lower or "book" in task_lower:
            venues = ["Conference Room A", "Main Auditorium", "Workshop Lab 1", "Innovation Hub"]
            return f"✅ Successfully booked {random.choice(venues)} for the event"
        elif "email" in task_lower or "contact" in task_lower:
            return f"✅ Email sent to coordinator. Response time: ~{random.randint(15, 60)} minutes"
        elif "poster" in task_lower or "design" in task_lower:
            return f"✅ Poster design completed. Template: Modern Tech v2.1"
        elif "schedule" in task_lower or "plan" in task_lower:
            return f"✅ Schedule created with {random.randint(3, 8)} time blocks"
        elif "budget" in task_lower or "cost" in task_lower:
            return f"✅ Budget analysis complete. Estimated cost: ${random.randint(500, 2000)}"
        elif "research" in task_lower or "find" in task_lower:
            return f"✅ Research completed. Found {random.randint(5, 15)} relevant resources"
        elif "prepare" in task_lower or "setup" in task_lower:
            return f"✅ Setup instructions prepared. Items needed: {random.randint(3, 7)}"
        else:
            return f"✅ Task completed successfully with standard protocol"

class MockTaskPlanner:
    """Mock LangChain-style task planner"""
    
    @staticmethod
    def break_down_query(query: str) -> List[Dict[str, str]]:
        """Break down user query into subtasks"""
        query_lower = query.lower()
        
        # Define task patterns for different types of requests
        if "robotics workshop" in query_lower or ("robotics" in query_lower and "workshop" in query_lower):
            return [
                {"task": "Research robotics workshop requirements", "agent": "research_agent"},
                {"task": "Book appropriate venue with power outlets", "agent": "logistics_agent"},
                {"task": "Email workshop coordinator for availability", "agent": "communication_agent"},
                {"task": "Prepare promotional poster and materials", "agent": "design_agent"},
                {"task": "Create detailed workshop schedule", "agent": "planning_agent"},
                {"task": "Estimate budget for materials and equipment", "agent": "finance_agent"}
            ]
        elif "birthday party" in query_lower or ("birthday" in query_lower and "party" in query_lower):
            return [
                {"task": "Find suitable party venue", "agent": "logistics_agent"},
                {"task": "Create guest invitation list", "agent": "planning_agent"},
                {"task": "Design birthday invitations", "agent": "design_agent"},
                {"task": "Contact catering service", "agent": "communication_agent"},
                {"task": "Plan party activities and games", "agent": "planning_agent"},
                {"task": "Calculate total party budget", "agent": "finance_agent"}
            ]
        elif "conference" in query_lower:
            return [
                {"task": "Research conference venues and dates", "agent": "research_agent"},
                {"task": "Contact potential speakers", "agent": "communication_agent"},
                {"task": "Design conference branding materials", "agent": "design_agent"},
                {"task": "Create conference agenda and timeline", "agent": "planning_agent"},
                {"task": "Setup registration system", "agent": "logistics_agent"},
                {"task": "Prepare conference budget proposal", "agent": "finance_agent"}
            ]
        elif "hackathon" in query_lower:
            return [
                {"task": "Find hackathon venue with coding setup", "agent": "logistics_agent"},
                {"task": "Recruit judges and mentors", "agent": "communication_agent"},
                {"task": "Create hackathon promotional materials", "agent": "design_agent"},
                {"task": "Setup team registration process", "agent": "planning_agent"},
                {"task": "Arrange food and refreshments", "agent": "logistics_agent"},
                {"task": "Estimate prizes and operational costs", "agent": "finance_agent"}
            ]
        elif "meeting" in query_lower:
            return [
                {"task": "Book meeting room", "agent": "logistics_agent"},
                {"task": "Send meeting invitations to attendees", "agent": "communication_agent"},
                {"task": "Prepare meeting agenda", "agent": "planning_agent"},
                {"task": "Setup technical equipment for presentation", "agent": "logistics_agent"}
            ]
        elif "training" in query_lower or "course" in query_lower:
            return [
                {"task": "Research training curriculum requirements", "agent": "research_agent"},
                {"task": "Book training facility", "agent": "logistics_agent"},
                {"task": "Contact training instructors", "agent": "communication_agent"},
                {"task": "Prepare training materials and handouts", "agent": "design_agent"},
                {"task": "Create training schedule", "agent": "planning_agent"},
                {"task": "Calculate training costs and fees", "agent": "finance_agent"}
            ]
        else:
            # Generic task breakdown for unknown queries
            return [
                {"task": f"Research requirements for: {query}", "agent": "research_agent"},
                {"task": f"Plan logistics for: {query}", "agent": "logistics_agent"},
                {"task": f"Coordinate communications for: {query}", "agent": "communication_agent"},
                {"task": f"Prepare materials for: {query}", "agent": "design_agent"}
            ]

class MockAgentOrchestrator:
    """Mock LangChain-style agent orchestrator"""
    
    def __init__(self):
        self.agents = {
            "research_agent": MockAgent("Research Agent", "Information Gathering", ["web_search", "database_lookup"]),
            "logistics_agent": MockAgent("Logistics Agent", "Resource Management", ["booking_system", "inventory_check"]),
            "communication_agent": MockAgent("Communication Agent", "Correspondence", ["email_client", "messaging_api"]),
            "design_agent": MockAgent("Design Agent", "Creative Tasks", ["design_tools", "template_engine"]),
            "planning_agent": MockAgent("Planning Agent", "Scheduling & Organization", ["calendar_api", "project_manager"]),
            "finance_agent": MockAgent("Finance Agent", "Budget & Cost Analysis", ["accounting_tools", "cost_calculator"])
        }
    
    def execute_workflow(self, query: str):
        """Execute the complete workflow for a query"""
        # Break down the query into subtasks
        subtasks = MockTaskPlanner.break_down_query(query)
        
        st.write("🔄 **Breaking down your request into subtasks...**")
        st.write(f"📝 **Query**: {query}")
        st.write(f"🎯 **Identified {len(subtasks)} subtasks**")
        
        # Create progress containers
        progress_bar = st.progress(0)
        status_container = st.container()
        
        results = []
        
        for i, subtask in enumerate(subtasks):
            with status_container:
                st.write(f"🤖 **{self.agents[subtask['agent']].name}** is working on: *{subtask['task']}*")
                
                with st.spinner(f"Processing subtask {i+1}/{len(subtasks)}..."):
                    result = self.agents[subtask['agent']].execute_task(subtask['task'])
                    results.append(result)
                
                # Display result
                if result['status'] == 'completed':
                    st.success(f"✅ **{result['agent']}** completed in {result['processing_time']}")
                    st.info(result['details'])
                else:
                    st.error(f"❌ **{result['agent']}** failed after {result['processing_time']}")
                    st.warning(result['details'])
                
                # Update progress
                progress_bar.progress((i + 1) / len(subtasks))
                
                st.write("---")
        
        # Final summary
        successful_tasks = len([r for r in results if r['status'] == 'completed'])
        st.write("## 📊 **Workflow Summary**")
        st.write(f"✅ **Completed**: {successful_tasks}/{len(subtasks)} tasks")
        st.write(f"🕒 **Total Time**: {sum(float(r['processing_time'].rstrip('s')) for r in results):.1f}s")
        
        if successful_tasks == len(subtasks):
            st.balloons()
            st.success("🎉 All tasks completed successfully! Your request has been fully processed.")
        else:
            st.warning(f"⚠️ {len(subtasks) - successful_tasks} tasks need attention. Please review the failed items above.")

# Streamlit App
def main():
    st.set_page_config(
        page_title="Agentic Chatbot Demo",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Agentic Chatbot Demo")
    st.markdown("*Powered by Mock LangChain Agents*")
    
    st.markdown("""
    This demo simulates how an agentic AI system breaks down complex queries into subtasks 
    and distributes them across specialized agents. Try asking to organize different types of events!
    """)
    
    # Sidebar with example queries
    with st.sidebar:
        st.header("💡 Example Queries")
        example_queries = [
            "Organize a robotics workshop",
            "Plan a birthday party",
            "Setup a tech conference",
            "Organize a hackathon",
            "Schedule a team meeting",
            "Create a training course"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{query}"):
                st.session_state.query_input = query
        
        st.markdown("---")
        st.markdown("### 🔧 Available Agents")
        st.markdown("- 🔍 **Research Agent**")
        st.markdown("- 📋 **Logistics Agent**") 
        st.markdown("- 📧 **Communication Agent**")
        st.markdown("- 🎨 **Design Agent**")
        st.markdown("- 📅 **Planning Agent**")
        st.markdown("- 💰 **Finance Agent**")
    
    # Initialize session state
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = MockAgentOrchestrator()
    
    if 'query_input' not in st.session_state:
        st.session_state.query_input = ""
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_query = st.text_input(
            "What would you like me to help organize?",
            value=st.session_state.query_input,
            placeholder="e.g., Organize a robotics workshop",
            key="main_query"
        )
    
    with col1:
        execute_button = st.button("🚀 Execute", type="primary")
    
    # Execute workflow when button is clicked or Enter is pressed
    if execute_button and user_query:
        st.markdown("---")
        st.session_state.orchestrator.execute_workflow(user_query)
    
    elif execute_button and not user_query:
        st.warning("Please enter a query to process!")
    
    # Clear query input after processing
    if execute_button:
        st.session_state.query_input = ""

if __name__ == "__main__":
    main()
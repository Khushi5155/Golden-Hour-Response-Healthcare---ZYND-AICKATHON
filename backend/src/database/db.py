from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# ============================================
# DATABASE CONNECTION
# ============================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./emergency_system.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================
# TABLE 1: EMERGENCIES
# ============================================
class Emergency(Base):
    """Stores all emergency incidents reported by users"""
    __tablename__ = "emergencies"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Location Information
    location = Column(String(500), nullable=False)  # "Connaught Place, Delhi"
    latitude = Column(Float, nullable=False)        # 28.6289
    longitude = Column(Float, nullable=False)       # 77.2065
    
    # Patient Information
    symptoms = Column(JSON, nullable=False)         # ["chest_pain", "unconscious"]
    age_group = Column(String(50), nullable=False)  # "60+", "19-60", "0-18"
    vitals = Column(JSON, nullable=True)            # {"bp": "180/100"} - OPTIONAL
    
    # Triage Results (filled by Triage Agent)
    severity = Column(String(20), nullable=True)    # "RED", "YELLOW", "GREEN"
    priority = Column(Integer, nullable=True)       # 1 (highest), 2, 3
    
    # Status Tracking
    status = Column(String(50), nullable=False, default="REGISTERED")
    # Possible values: 
    # - REGISTERED (just created)
    # - TRIAGED (severity assigned)
    # - HOSPITAL_ASSIGNED (hospital selected)
    # - AMBULANCE_DISPATCHED (ambulance on the way)
    # - IN_TRANSIT (moving to hospital)
    # - ARRIVED (reached hospital)
    # - COMPLETED (incident closed)
    
    # Assignments (filled by Hospital & Routing Agents)
    assigned_hospital_id = Column(String(100), nullable=True)
    assigned_ambulance_id = Column(String(100), nullable=True)
    estimated_arrival_time = Column(String(50), nullable=True)  # "12 minutes"
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Emergency(id={self.id}, severity={self.severity}, status={self.status})>"


# ============================================
# TABLE 2: AGENT LOGS
# ============================================
class AgentLog(Base):
    """Tracks every action taken by each agent (with Zynd DIDs)"""
    __tablename__ = "agent_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Agent Identification (Zynd Protocol DIDs)
    agent_id = Column(String(200), nullable=False, index=True)  # "did:zynd:agent:triage:abc123"
    agent_type = Column(String(50), nullable=False, index=True) # "triage", "hospital", "routing", "notification"
    agent_name = Column(String(100), nullable=True)             # "Emergency Triage Agent"
    
    # Emergency Reference
    emergency_id = Column(Integer, nullable=False, index=True)  # Links to emergencies.id
    
    # Action Details
    action = Column(String(500), nullable=False)                # "Classified severity as RED"
    input_data = Column(JSON, nullable=True)                    # What agent received
    output_data = Column(JSON, nullable=True)                   # What agent produced
    
    # Performance Metrics
    processing_time_ms = Column(Integer, nullable=True)         # Execution time
    success = Column(String(20), nullable=False, default="SUCCESS")  # "SUCCESS", "FAILED"
    error_message = Column(Text, nullable=True)                 # Error details if failed
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<AgentLog(id={self.id}, type={self.agent_type}, action={self.action})>"


# ============================================
# TABLE 3: HOSPITALS
# ============================================
class Hospital(Base):
    """Stores hospital information and bed availability"""
    __tablename__ = "hospitals"
    
    # Primary Key
    id = Column(String(100), primary_key=True)  # "max_hospital_saket"
    
    # Basic Information
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Bed Availability
    icu_beds_available = Column(Integer, default=0)
    icu_beds_total = Column(Integer, default=0)
    general_beds_available = Column(Integer, default=0)
    general_beds_total = Column(Integer, default=0)
    
    # Capabilities
    has_cardiologist = Column(String(10), default="false")     # "true" or "false"
    has_trauma_center = Column(String(10), default="false")
    has_neurosurgeon = Column(String(10), default="false")
    
    # Contact Information
    phone = Column(String(20), nullable=True)
    emergency_contact = Column(String(20), nullable=True)
    
    # Metadata
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Hospital(id={self.id}, name={self.name})>"


# ============================================
# DATABASE HELPER FUNCTIONS
# ============================================

def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def get_db():
    """Get database session (for FastAPI dependency injection)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def drop_all_tables():
    """WARNING: Deletes all data! Use only for testing"""
    Base.metadata.drop_all(bind=engine)
    print("🗑️  All tables dropped!")


# ============================================
# RUN THIS FILE TO CREATE TABLES
# ============================================
if __name__ == "__main__":
    print("🔧 Initializing Emergency System Database...")
    print(f"📁 Database Location: {DATABASE_URL}")
    print()
    
    # Create tables
    init_db()
    
    # Show created tables
    print("\n📋 Created Tables:")
    print("   1. emergencies - Stores emergency incidents")
    print("   2. agent_logs - Tracks agent actions with DIDs")
    print("   3. hospitals - Hospital information and availability")
    print()
    print("✅ Database setup complete!")
    print(f"💾 Database file: emergency_system.db")

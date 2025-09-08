import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.analysis_engine import UserBehaviorAnalysisEngine
from config.settings import settings

def demo_analysis():
    print("🎯 User Behavior Analysis Engine Demo")
    print("=" * 60)
    
    engine = UserBehaviorAnalysisEngine()
    
    try:
        users_summary = engine.get_all_users_summary(settings.CSV_FILE_PATH)
        print(f"📊 Loaded {len(users_summary)} users")
        
        demo_users = users_summary[:3]
        
        for i, user in enumerate(demo_users, 1):
            print(f"\n👤 User {i}: {user['name']} ({user['email']})")
            print(f"   ID: {user['user_id']}")
            print(f"   Total events: {user['total_events']}")
            
            try:
                interests = engine.get_user_interests(user['user_id'], settings.CSV_FILE_PATH)
                
                print(f"   📈 Interest analysis:")
                print(f"   - Top tags ({len(interests.top_tags)}):")
                for j, tag in enumerate(interests.top_tags[:3], 1):
                    print(f"     {j}. {tag}")
                
                print(f"   - Top tools ({len(interests.top_tools)}):")
                for j, tool in enumerate(interests.top_tools[:3], 1):
                    print(f"     {j}. {tool}")
                
                print(f"   - Total interactions: {interests.total_interactions}")
                
            except Exception as e:
                print(f"   ❌ Analysis error: {e}")
        
        if demo_users:
            print(f"\n🔍 Detailed analysis for user: {demo_users[0]['name']}")
            user_id = demo_users[0]['user_id']
            
            events = engine.generate_mock_events(user_id, demo_users[0]['total_events'])
            print(f"   Generated {len(events)} events")
            
            user_profile = engine.analyze_user_interests(user_id, events)
            
            print(f"   📊 Analysis results:")
            print(f"   - Total interests: {len(user_profile.interests)}")
            print(f"   - Top-5 interests:")
            
            for i, interest in enumerate(user_profile.interests[:5], 1):
                print(f"     {i}. {interest.tag_or_tool}: {interest.score:.2f} "
                      f"({interest.interaction_count} interactions)")
        
        print(f"\n⚖️  Event weights:")
        for event_type, weight in engine.event_weights.items():
            print(f"   - {event_type}: {weight}")
        
        print(f"\n⏰ Time decay factor: {engine.time_decay_factor}")
        print(f"📊 Minimum interactions: {engine.min_interactions}")
        print(f"🔝 Max top items: {engine.max_top_items}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")
    print("\n💡 To start API server run:")
    print("   python -m src.main")
    print("\n🌐 After starting server API will be available at:")
    print("   http://localhost:8000")
    print("\n📚 API Documentation:")
    print("   http://localhost:8000/docs")

if __name__ == "__main__":
    demo_analysis()
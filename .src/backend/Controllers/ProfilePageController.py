from flask import request, jsonify
from Entities.Activity import Activity
from Entities.DatabaseController import DatabaseController

class ProfilePageController:
    def __init__(self):
        self.db_controller = DatabaseController()
    
    def get_cycling_statistics(self, user_id, period="week"):
        try:
            # Get activities for the period
            activities = self.db_controller.get_user_activities(user_id, period)
            
            # Calculate statistics
            total_distance = sum(activity.distance for activity in activities)
            total_time = sum(activity.duration for activity in activities)
            total_rides = len(activities)
            
            return {
                "total_distance": total_distance,
                "total_time": total_time,
                "total_rides": total_rides,
                "activities": [activity.to_dict() for activity in activities]
            }
        except Exception as e:
            return {"error": str(e)}, 400
    
    def get_recent_activities(self, user_id, limit=3):
        try:
            # Get recent activities
            activities = self.db_controller.get_user_activities(user_id, limit=limit)
            
            return {
                "activities": [activity.to_dict() for activity in activities]
            }
        except Exception as e:
            return {"error": str(e)}, 400
    
    def get_all_ride_history(self, user_id):
        try:
            # Get all activities
            activities = self.db_controller.get_user_activities(user_id)
            
            return {
                "activities": [activity.to_dict() for activity in activities]
            }
        except Exception as e:
            return {"error": str(e)}, 400
    
    def delete_ride_history(self, user_id, activity_id):
        try:
            # Delete activity
            self.db_controller.delete_activity(user_id, activity_id)
            
            return {"message": "Activity deleted successfully"}
        except Exception as e:
            return {"error": str(e)}, 400
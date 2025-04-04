from flask import request, jsonify
from Entities.Activity import Activity
from Entities.DatabaseController import DatabaseController
import polyline

class ProfilePageController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def fetch_activies(self, user_UID):
        act_ref = db.collection("users").document(user_UID).collection("activities").stream()
        activities = []
        for doc in act_ref:
            data = doc.to_dict()
            data = to_serializable(data)
            data["id"] = doc.id
            activities.append(data)
        return jsonify(activities), 200
    def get_username(self, user_UID):
        if not user_UID:
            return jsonify({"message": "User UID required"}), 400

        try:
            username = self.db_controller.get_username_by_uid(user_UID)
            if username:
                return jsonify({"username": username}), 200
            else:
                return jsonify({"message": "Username not found"}), 404
        except Exception as e:
            print("Error fetching username:", e)
            return jsonify({"message": "Server error"}), 500
        
    def get_profile_pic(self, user_UID):
        if not user_UID:
            return jsonify({"message": "User UID required"}), 400

        try:
            profile_pic = self.db_controller.get_profile_picture(user_UID)
            if not profile_pic == '':
                return jsonify({"profilePic": profile_pic}), 200
            else:
                return jsonify({"message": "Profile picture not found"}), 404
        except Exception as e:
            print("Error fetching profile picture:", e)
            return jsonify({"message": "Server error"}), 500
    
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
    
    def get_personal_best(self, user_id):
        try:
            # Get all activities
            activities = self.db_controller.get_user_activities(user_id)
            
            # Find personal bests
            best_distance = max(activities, key=lambda x: x.distance, default=None)
            best_speed = max(activities, key=lambda x: x.average_speed, default=None)
            
            return {
                "best_distance": best_distance.to_dict() if best_distance else None,
                "best_speed": best_speed.to_dict() if best_speed else None
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